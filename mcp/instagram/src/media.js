import crypto from 'node:crypto'
import { Readable } from 'node:stream'
import sharp from 'sharp'

// A API do Instagram não recebe upload: ela baixa a mídia de uma URL pública.
// Este módulo gera URLs assinadas no próprio servidor que buscam o arquivo de origem
// (Drive, Canva, qualquer https), convertem imagens para JPEG e aplicam o corte pedido.

export const CROPS = {
  original: null,
  '4:5': 4 / 5,
  '1:1': 1,
  '1.91:1': 1.91,
  '9:16': 9 / 16
}

// Faixa de proporção aceita pelo Instagram para imagens de feed/carrossel.
const FEED_MIN_RATIO = 0.8
const FEED_MAX_RATIO = 1.91
const MAX_WIDTH = 1440

export function createSigner(key) {
  const sign = (data) => crypto.createHmac('sha256', key).update(data).digest('base64url')
  return {
    sign(payload) {
      const data = Buffer.from(JSON.stringify(payload)).toString('base64url')
      return `${data}.${sign(data)}`
    },
    verify(token, now = Date.now()) {
      const [data, sig] = String(token).split('.')
      if (!data || !sig) return null
      const expected = Buffer.from(sign(data))
      const given = Buffer.from(sig)
      if (expected.length !== given.length || !crypto.timingSafeEqual(expected, given)) return null
      const payload = JSON.parse(Buffer.from(data, 'base64url').toString())
      if (payload.e && payload.e < now) return null
      return payload
    }
  }
}

export function driveIdFromUrl(url) {
  const m = /drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?(?:.*&)?id=)([\w-]{10,})/.exec(url) ||
    /docs\.google\.com\/uc\?(?:.*&)?id=([\w-]{10,})/.exec(url)
  return m ? m[1] : null
}

export function upstreamUrl(source) {
  const driveId = source.drive_file_id || (source.url && driveIdFromUrl(source.url))
  if (driveId) return `https://drive.usercontent.google.com/download?id=${encodeURIComponent(driveId)}&export=download&confirm=t`
  if (!source.url) throw new Error('Informe "url" ou "drive_file_id" para cada mídia')
  if (!/^https:\/\//.test(source.url)) throw new Error(`A URL da mídia precisa ser https: ${source.url}`)
  return source.url
}

export function publicMediaUrl({ signer, publicBaseUrl, source, kind, ttlMs = 3 * 24 * 3600 * 1000, now = Date.now() }) {
  const token = signer.sign({ u: upstreamUrl(source), k: kind, c: source.corte || 'original', e: now + ttlMs })
  return `${publicBaseUrl}/media/${token}`
}

export async function toJpeg(buffer, crop = 'original') {
  const rotated = await sharp(buffer).rotate().toBuffer({ resolveWithObject: true })
  let { width, height } = rotated.info
  let img = sharp(rotated.data)
  const ratio = CROPS[crop]
  if (ratio) {
    if (width / height > ratio) {
      const w = Math.round(height * ratio)
      img = img.extract({ left: Math.floor((width - w) / 2), top: 0, width: w, height })
      width = w
    } else {
      const h = Math.round(width / ratio)
      img = img.extract({ left: 0, top: Math.floor((height - h) / 2), width, height: h })
      height = h
    }
  }
  if (width > MAX_WIDTH) {
    height = Math.round((height * MAX_WIDTH) / width)
    width = MAX_WIDTH
    img = img.resize({ width })
  }
  const data = await img.flatten({ background: '#ffffff' }).jpeg({ quality: 90, mozjpeg: true }).toBuffer()
  return { data, width, height }
}

async function fetchUpstream(fetchImpl, url) {
  const res = await fetchImpl(url, { redirect: 'follow' })
  const contentType = res.headers.get('content-type') || ''
  if (!res.ok) throw new Error(`Não consegui baixar a mídia (HTTP ${res.status}): ${url}`)
  if (contentType.startsWith('text/html')) {
    await res.body?.cancel()
    throw new Error(
      'A origem devolveu uma página em vez do arquivo. Se for do Google Drive, compartilhe como ' +
        '"Qualquer pessoa com o link" (leitor) e tente de novo.'
    )
  }
  return { res, contentType }
}

// Baixa e valida a mídia antes de criar o post, para o erro aparecer na hora e não só no horário agendado.
export async function preflight({ source, kind, feed, fetchImpl = fetch }) {
  const url = upstreamUrl(source)
  const { res, contentType } = await fetchUpstream(fetchImpl, url)
  if (kind === 'video') {
    await res.body?.cancel()
    if (contentType && !/^(video\/|application\/octet-stream|binary\/octet-stream)/.test(contentType)) {
      throw new Error(`Esperava um vídeo e recebi "${contentType}": ${url}`)
    }
    return { tipo: 'video', content_type: contentType }
  }
  const { width, height } = await toJpeg(Buffer.from(await res.arrayBuffer()), source.corte || 'original')
  const ratio = width / height
  if (feed && (ratio < FEED_MIN_RATIO - 0.005 || ratio > FEED_MAX_RATIO + 0.005)) {
    throw new Error(
      `Proporção ${width}x${height} (${ratio.toFixed(2)}) fora do aceito no feed (entre 4:5 e 1.91:1). ` +
        'Use corte "4:5" ou "1:1".'
    )
  }
  return { tipo: 'imagem', largura: width, altura: height }
}

export function mediaRoute({ signer, fetchImpl = fetch }) {
  return async (req, res) => {
    const payload = signer.verify(req.params.token)
    if (!payload) return res.status(404).send('link inválido ou expirado')
    try {
      const { res: upstream, contentType } = await fetchUpstream(fetchImpl, payload.u)
      if (payload.k === 'image') {
        const { data } = await toJpeg(Buffer.from(await upstream.arrayBuffer()), payload.c)
        return res.type('image/jpeg').send(data)
      }
      res.setHeader('Content-Type', contentType.startsWith('video/') ? contentType : 'video/mp4')
      const length = upstream.headers.get('content-length')
      if (length) res.setHeader('Content-Length', length)
      Readable.fromWeb(upstream.body).pipe(res)
    } catch (e) {
      res.status(502).send(e.message)
    }
  }
}
