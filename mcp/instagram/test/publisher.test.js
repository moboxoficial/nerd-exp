import { test, beforeEach } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { GraphError } from '../src/graph.js'
import { createSigner } from '../src/media.js'
import { Publisher } from '../src/publisher.js'

const MIN = 60 * 1000
let clock, calls, statuses, failNext, publisher

function fakeGraph() {
  let n = 0
  return {
    async get(token, p) {
      calls.push(['GET', p])
      if (p === 'me') return { user_id: '17841', username: 'nerdexperience' }
      if (p.startsWith('media_')) return { permalink: `https://instagram.com/p/${p}` }
      return { status_code: statuses[p] || 'FINISHED' }
    },
    async post(token, p, params) {
      calls.push(['POST', p, params])
      if (failNext) {
        const e = failNext
        failNext = null
        throw e
      }
      if (p.endsWith('/media_publish')) return { id: `media_${params.creation_id}` }
      return { id: `c${++n}` }
    }
  }
}

function accountsFor(graph) {
  return {
    token: (name) => {
      if (name !== 'nerdexperience') throw new Error('Conta desconhecida')
      return 'tok'
    },
    get: async () => ({ name: 'nerdexperience', token: 'tok', userId: '17841', username: 'nerdexperience' })
  }
}

beforeEach(() => {
  clock = Date.parse('2026-10-14T12:00:00Z')
  calls = []
  statuses = {}
  failNext = null
  const graph = fakeGraph()
  publisher = new Publisher({
    accounts: accountsFor(graph),
    graph,
    signer: createSigner('k'),
    publicBaseUrl: 'https://mcp.exemplo.com',
    dataDir: fs.mkdtempSync(path.join(os.tmpdir(), 'nxp-ig-')),
    prepareLeadMinutes: 20,
    now: () => clock,
    log: { error() {} }
  })
})

const publishCalls = () => calls.filter((c) => c[0] === 'POST' && c[1].endsWith('/media_publish'))

test('imagem agendada só é publicada no horário', async () => {
  const job = publisher.create({
    conta: 'nerdexperience',
    formato: 'imagem',
    payload: { midia: { url: 'https://x/a.png', corte: '4:5' }, legenda: 'Oi #nxp', colaboradores: ['nerdverso.nxp'] },
    runAt: clock + 60 * MIN
  })
  await publisher.tick()
  assert.equal(publisher.get(job.id).status, 'agendado')

  clock += 59 * MIN
  await publisher.tick()
  const preparing = publisher.get(job.id)
  assert.equal(preparing.status, 'preparando')
  const create = calls.find((c) => c[1] === '17841/media')
  assert.match(create[2].image_url, /^https:\/\/mcp\.exemplo\.com\/media\//)
  assert.deepEqual(create[2].collaborators, ['nerdverso.nxp'])
  assert.equal(publishCalls().length, 0)

  clock += 1 * MIN
  await publisher.tick()
  const done = publisher.get(job.id)
  assert.equal(done.status, 'publicado')
  assert.equal(done.permalink, 'https://instagram.com/p/media_c1')
  await publisher.tick()
  assert.equal(publishCalls().length, 1)
})

test('reels começa a subir antes e espera a Meta terminar de processar', async () => {
  const job = publisher.create({
    conta: 'nerdexperience',
    formato: 'reels',
    payload: { video: { drive_file_id: 'abc123456789' }, legenda: 'reels' },
    runAt: clock + 20 * MIN
  })
  statuses.c1 = 'IN_PROGRESS'
  await publisher.tick()
  assert.equal(publisher.get(job.id).status, 'preparando')
  const create = calls.find((c) => c[1] === '17841/media')
  assert.equal(create[2].media_type, 'REELS')
  assert.equal(create[2].share_to_feed, true)

  clock += 20 * MIN
  await publisher.tick()
  assert.equal(publisher.get(job.id).status, 'preparando')
  statuses.c1 = 'FINISHED'
  await publisher.tick()
  assert.equal(publisher.get(job.id).status, 'publicado')
})

test('carrossel cria o container pai só depois dos itens', async () => {
  const job = publisher.create({
    conta: 'nerdexperience',
    formato: 'carrossel',
    payload: {
      itens: [
        { url: 'https://x/1.jpg', tipo: 'imagem' },
        { url: 'https://x/2.mp4', tipo: 'video' }
      ],
      legenda: 'carrossel'
    },
    runAt: clock
  })
  statuses.c2 = 'IN_PROGRESS'
  await publisher.tick()
  let j = publisher.get(job.id)
  assert.equal(j.containers.parent, null)
  assert.deepEqual(j.containers.children, ['c1', 'c2'])
  assert.equal(calls.find((c) => c[2]?.video_url).at(2).media_type, 'VIDEO')

  statuses.c2 = 'FINISHED'
  await publisher.tick()
  j = publisher.get(job.id)
  const parent = calls.find((c) => c[2]?.media_type === 'CAROUSEL')
  assert.equal(parent[2].children, 'c1,c2')
  assert.equal(j.status, 'publicado')
})

test('erro temporário tenta de novo; erro definitivo marca erro', async () => {
  const job = publisher.create({
    conta: 'nerdexperience',
    formato: 'story',
    payload: { midia: { url: 'https://x/s.jpg', tipo: 'imagem' } },
    runAt: clock
  })
  failNext = new GraphError('instável', { transient: true })
  await publisher.tick()
  let j = publisher.get(job.id)
  assert.equal(j.status, 'agendado')
  assert.equal(j.tentativas, 1)

  clock += 3 * MIN
  failNext = new GraphError('mídia inválida')
  await publisher.tick()
  j = publisher.get(job.id)
  assert.equal(j.status, 'erro')
  assert.equal(j.erro, 'mídia inválida')

  publisher.reschedule(job.id, clock + MIN)
  clock += MIN
  await publisher.tick()
  assert.equal(publisher.get(job.id).status, 'publicado')
})

test('container já publicado não é publicado de novo', async () => {
  const job = publisher.create({
    conta: 'nerdexperience',
    formato: 'imagem',
    payload: { midia: { url: 'https://x/a.jpg' } },
    runAt: clock
  })
  statuses.c1 = 'PUBLISHED'
  await publisher.tick()
  assert.equal(publisher.get(job.id).status, 'publicado')
  assert.equal(publishCalls().length, 0)
})

test('post que perdeu o horário por mais de 2h não é publicado', async () => {
  const job = publisher.create({
    conta: 'nerdexperience',
    formato: 'imagem',
    payload: { midia: { url: 'https://x/a.jpg' } },
    runAt: clock - 3 * 60 * MIN
  })
  await publisher.tick()
  const j = publisher.get(job.id)
  assert.equal(j.status, 'erro')
  assert.match(j.erro, /Horário perdido/)
  assert.equal(calls.length, 0)
})

test('cancelar só vale para agendados', async () => {
  const job = publisher.create({ conta: 'nerdexperience', formato: 'imagem', payload: { midia: { url: 'https://x/a.jpg' } }, runAt: clock + 999 * MIN })
  assert.equal(publisher.cancel(job.id).status, 'cancelado')
  assert.throws(() => publisher.cancel(job.id), /agendado/)
  assert.throws(() => publisher.create({ conta: 'outra', formato: 'imagem', payload: {}, runAt: clock }), /desconhecida/)
})
