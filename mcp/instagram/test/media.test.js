import { test } from 'node:test'
import assert from 'node:assert/strict'
import sharp from 'sharp'
import { createSigner, driveIdFromUrl, preflight, toJpeg, upstreamUrl } from '../src/media.js'
import { formatLocal, parseWhen } from '../src/time.js'

test('assinatura de links de mídia valida, rejeita adulteração e expira', () => {
  const signer = createSigner('segredo')
  const token = signer.sign({ u: 'https://x/a.jpg', e: 2000 })
  assert.deepEqual(signer.verify(token, 1000), { u: 'https://x/a.jpg', e: 2000 })
  assert.equal(signer.verify(token, 3000), null)
  assert.equal(signer.verify(token.replace(/.$/, 'A'), 1000), null)
  assert.equal(createSigner('outro').verify(token, 1000), null)
})

test('reconhece links do Google Drive e exige https', () => {
  assert.equal(driveIdFromUrl('https://drive.google.com/file/d/1AbCdEfGhIjK_lm/view?usp=sharing'), '1AbCdEfGhIjK_lm')
  assert.equal(driveIdFromUrl('https://drive.google.com/open?id=1AbCdEfGhIjK_lm'), '1AbCdEfGhIjK_lm')
  assert.match(upstreamUrl({ drive_file_id: 'abc123456789' }), /drive\.usercontent\.google\.com\/download\?id=abc123456789/)
  assert.throws(() => upstreamUrl({ url: 'http://inseguro/a.jpg' }), /https/)
  assert.throws(() => upstreamUrl({}), /url/)
})

test('converte para JPEG e aplica corte central', async () => {
  const png = await sharp({ create: { width: 1000, height: 1000, channels: 4, background: '#ff000080' } }).png().toBuffer()
  const out = await toJpeg(png, '4:5')
  assert.equal(out.width, 800)
  assert.equal(out.height, 1000)
  const meta = await sharp(out.data).metadata()
  assert.equal(meta.format, 'jpeg')
  assert.equal(meta.width, 800)
})

test('preflight barra proporção fora do feed e página HTML do Drive', async () => {
  const tall = await sharp({ create: { width: 900, height: 1600, channels: 3, background: '#000' } }).jpeg().toBuffer()
  const fetchImg = async () => new Response(tall, { headers: { 'content-type': 'image/jpeg' } })
  await assert.rejects(preflight({ source: { url: 'https://x/a.jpg' }, kind: 'image', feed: true, fetchImpl: fetchImg }), /4:5/)
  const ok = await preflight({ source: { url: 'https://x/a.jpg', corte: '4:5' }, kind: 'image', feed: true, fetchImpl: fetchImg })
  assert.equal(ok.largura / ok.altura, 0.8)
  await preflight({ source: { url: 'https://x/a.jpg' }, kind: 'image', feed: false, fetchImpl: fetchImg })

  const fetchHtml = async () => new Response('<html>', { headers: { 'content-type': 'text/html' } })
  await assert.rejects(
    preflight({ source: { drive_file_id: 'abc123456789' }, kind: 'image', feed: true, fetchImpl: fetchHtml }),
    /Qualquer pessoa com o link/
  )
})

test('horários sem fuso são de Brasília', () => {
  const ms = parseWhen('2026-10-14T11:00', '-03:00')
  assert.equal(new Date(ms).toISOString(), '2026-10-14T14:00:00.000Z')
  assert.equal(parseWhen('2026-10-14 11:00', '-03:00'), ms)
  assert.equal(parseWhen('2026-10-14T14:00:00Z', '-03:00'), ms)
  assert.equal(formatLocal(ms, '-03:00'), '2026-10-14T11:00:00-03:00')
  assert.throws(() => parseWhen('amanhã', '-03:00'), /inválida/)
})
