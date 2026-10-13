import crypto from 'node:crypto'
import path from 'node:path'
import { JsonFile } from './store.js'
import { publicMediaUrl } from './media.js'

// Fila de publicação. A API do Instagram não agenda posts: ela cria um "container" de mídia,
// a Meta processa, e depois publicamos. Aqui cada post vira um job que o worker leva de
// agendado → preparando → publicado (ou erro / cancelado), respeitando o horário marcado.

export const FINAL_STATUSES = ['publicado', 'erro', 'cancelado']
const MAX_ATTEMPTS = 3
const RETRY_DELAY_MS = 2 * 60 * 1000
const IMAGE_LEAD_MS = 2 * 60 * 1000

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export function jobHasVideo(job) {
  const p = job.payload
  if (job.formato === 'reels') return true
  if (job.formato === 'story') return p.midia.tipo === 'video'
  if (job.formato === 'carrossel') return p.itens.some((i) => i.tipo === 'video')
  return false
}

export class Publisher {
  constructor({
    accounts,
    graph,
    signer,
    publicBaseUrl,
    dataDir,
    prepareLeadMinutes = 20,
    maxLateMinutes = 120,
    now = () => Date.now(),
    log = console
  }) {
    this.accounts = accounts
    this.graph = graph
    this.signer = signer
    this.publicBaseUrl = publicBaseUrl
    this.file = new JsonFile(path.join(dataDir, 'jobs.json'), { jobs: [] })
    this.videoLeadMs = prepareLeadMinutes * 60 * 1000
    this.maxLateMs = maxLateMinutes * 60 * 1000
    this.now = now
    this.log = log
    this.locks = new Set()
    this.ticking = false
  }

  all() {
    return this.file.read().jobs
  }

  get(id) {
    const job = this.all().find((j) => j.id === id)
    if (!job) throw new Error(`Agendamento não encontrado: ${id}`)
    return job
  }

  save(job) {
    const data = this.file.read()
    const i = data.jobs.findIndex((j) => j.id === job.id)
    job.atualizado_em = new Date(this.now()).toISOString()
    if (i === -1) data.jobs.push(job)
    else data.jobs[i] = job
    this.file.write(data)
    return job
  }

  create({ conta, formato, payload, runAt, idPlanilha }) {
    this.accounts.token(conta) // valida a conta
    return this.save({
      id: crypto.randomUUID(),
      conta,
      formato,
      payload,
      run_at: runAt,
      id_planilha: idPlanilha || null,
      status: 'agendado',
      tentativas: 0,
      containers: null,
      media_id: null,
      permalink: null,
      erro: null,
      criado_em: new Date(this.now()).toISOString()
    })
  }

  cancel(id) {
    const job = this.get(id)
    if (job.status !== 'agendado') {
      throw new Error(`Só dá para cancelar posts com status "agendado" (este está "${job.status}")`)
    }
    job.status = 'cancelado'
    return this.save(job)
  }

  reschedule(id, runAt) {
    const job = this.get(id)
    if (job.status !== 'agendado' && job.status !== 'erro') {
      throw new Error(`Só dá para reagendar posts "agendado" ou "erro" (este está "${job.status}")`)
    }
    Object.assign(job, { run_at: runAt, status: 'agendado', tentativas: 0, erro: null, retry_at: null, containers: null })
    return this.save(job)
  }

  prepareAt(job) {
    return job.run_at - (jobHasVideo(job) ? this.videoLeadMs : IMAGE_LEAD_MS)
  }

  async tick() {
    if (this.ticking) return
    this.ticking = true
    try {
      for (const job of this.all()) {
        if (FINAL_STATUSES.includes(job.status)) continue
        await this.step(job.id)
      }
    } finally {
      this.ticking = false
    }
  }

  // Publica (ou continua publicando) um job agora, esperando até waitMs pela conclusão.
  async runNow(id, waitMs = 40000, pollMs = 4000) {
    const start = this.now()
    for (;;) {
      await this.step(id)
      const job = this.get(id)
      if (FINAL_STATUSES.includes(job.status) || this.now() - start >= waitMs) return job
      await sleep(pollMs)
    }
  }

  async step(id) {
    if (this.locks.has(id)) return
    this.locks.add(id)
    try {
      const job = this.get(id)
      const now = this.now()
      if (job.status === 'agendado') {
        if (now < this.prepareAt(job) || (job.retry_at && now < job.retry_at)) return
        if (now - job.run_at > this.maxLateMs) {
          return this.fail(job, 'Horário perdido: o servidor estava fora do ar no horário agendado. Reagende o post.')
        }
        await this.attempt(job, () => this.createContainers(job))
      }
      if (job.status === 'preparando') {
        await this.attempt(job, () => this.advance(job))
      }
    } finally {
      this.locks.delete(id)
    }
  }

  async attempt(job, fn) {
    try {
      await fn()
    } catch (e) {
      job.tentativas += 1
      job.erro = e.message
      if (e.transient && job.tentativas < MAX_ATTEMPTS) {
        job.retry_at = this.now() + RETRY_DELAY_MS
        this.save(job)
      } else {
        this.fail(job, e.message)
      }
      this.log.error(`[job ${job.id}] ${e.message}`)
    }
  }

  fail(job, message) {
    job.status = 'erro'
    job.erro = message
    return this.save(job)
  }

  mediaParams(source, tipo, extra = {}) {
    const url = publicMediaUrl({ signer: this.signer, publicBaseUrl: this.publicBaseUrl, source, kind: tipo === 'video' ? 'video' : 'image' })
    return tipo === 'video' ? { media_type: 'VIDEO', video_url: url, ...extra } : { image_url: url, ...extra }
  }

  async createContainer(acc, params) {
    const res = await this.graph.post(acc.token, `${acc.userId}/media`, params)
    return res.id
  }

  async createContainers(job) {
    const acc = await this.accounts.get(job.conta)
    const p = job.payload
    const shared = { caption: p.legenda, collaborators: p.colaboradores?.length ? p.colaboradores : undefined }
    let containers
    if (job.formato === 'imagem') {
      containers = {
        children: [],
        parent: await this.createContainer(acc, { ...this.mediaParams(p.midia, 'imagem'), ...shared, alt_text: p.alt_text })
      }
    } else if (job.formato === 'carrossel') {
      const children = []
      for (const item of p.itens) {
        const extra = { is_carousel_item: true }
        if (item.tipo !== 'video' && item.alt_text) extra.alt_text = item.alt_text
        children.push(await this.createContainer(acc, this.mediaParams(item, item.tipo, extra)))
      }
      containers = { children, parent: null }
    } else if (job.formato === 'reels') {
      const params = { ...this.mediaParams(p.video, 'video'), ...shared, media_type: 'REELS', share_to_feed: p.mostrar_no_feed !== false }
      if (p.capa) params.cover_url = publicMediaUrl({ signer: this.signer, publicBaseUrl: this.publicBaseUrl, source: p.capa, kind: 'image' })
      if (p.thumb_offset_ms !== undefined) params.thumb_offset = p.thumb_offset_ms
      if (p.nome_audio) params.audio_name = p.nome_audio
      containers = { children: [], parent: await this.createContainer(acc, params) }
    } else if (job.formato === 'story') {
      const params = this.mediaParams(p.midia, p.midia.tipo)
      params.media_type = 'STORIES'
      containers = { children: [], parent: await this.createContainer(acc, params) }
    } else {
      throw new Error(`Formato desconhecido: ${job.formato}`)
    }
    job.containers = containers
    job.status = 'preparando'
    job.retry_at = null
    this.save(job)
  }

  async containerStatus(acc, id) {
    const res = await this.graph.get(acc.token, id, { fields: 'status_code,status' })
    return { code: res.status_code, detail: res.status }
  }

  async advance(job) {
    const acc = await this.accounts.get(job.conta)
    const c = job.containers

    if (c.children.length && !c.parent) {
      for (const child of c.children) {
        const s = await this.containerStatus(acc, child)
        if (s.code === 'ERROR' || s.code === 'EXPIRED') {
          return this.fail(job, `Item do carrossel falhou no processamento da Meta (${s.code}): ${s.detail || ''}`.trim())
        }
        if (s.code !== 'FINISHED') return
      }
      const p = job.payload
      c.parent = await this.createContainer(acc, {
        media_type: 'CAROUSEL',
        children: c.children.join(','),
        caption: p.legenda,
        collaborators: p.colaboradores?.length ? p.colaboradores : undefined
      })
      this.save(job)
    }

    const s = await this.containerStatus(acc, c.parent)
    if (s.code === 'PUBLISHED') return this.markPublished(job, acc, null)
    if (s.code === 'ERROR' || s.code === 'EXPIRED') {
      return this.fail(job, `A Meta não conseguiu processar a mídia (${s.code}): ${s.detail || ''}`.trim())
    }
    if (s.code !== 'FINISHED' || this.now() < job.run_at) return

    const published = await this.graph.post(acc.token, `${acc.userId}/media_publish`, { creation_id: c.parent })
    return this.markPublished(job, acc, published.id)
  }

  async markPublished(job, acc, mediaId) {
    job.status = 'publicado'
    job.media_id = mediaId
    job.erro = null
    job.publicado_em = new Date(this.now()).toISOString()
    this.save(job)
    if (mediaId) {
      try {
        const media = await this.graph.get(acc.token, mediaId, { fields: 'permalink' })
        job.permalink = media.permalink || null
        this.save(job)
      } catch (e) {
        this.log.error(`[job ${job.id}] publicado, mas não consegui buscar o link: ${e.message}`)
      }
    }
    return job
  }
}
