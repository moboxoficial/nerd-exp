import { test, before, after } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import sharp from 'sharp'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js'
import { loadConfig } from '../src/config.js'
import { createApp } from '../src/server.js'

const KEY = 'chave-de-teste-com-mais-de-24-caracteres'
let server, base, graphCalls

before(async () => {
  graphCalls = []
  const image = await sharp({ create: { width: 1080, height: 1350, channels: 3, background: '#123456' } }).png().toBuffer()
  const json = (body) => new Response(JSON.stringify(body), { headers: { 'content-type': 'application/json' } })
  const fakeFetch = async (input, init = {}) => {
    const url = new URL(input)
    if (url.hostname === 'graph.instagram.com') {
      graphCalls.push([init.method || 'GET', url.pathname, init.body ? JSON.parse(init.body) : null])
      const p = url.pathname.replace('/v25.0/', '')
      if (p === 'me') return json({ user_id: url.searchParams.get('access_token') === 'tok-nxp' ? '111' : '222', username: 'conta' })
      if (p === '111') return json({ username: 'nerdexperience', followers_count: 5000 })
      if (p === '222') return json({ username: 'nerdverso.nxp', followers_count: 3000 })
      if (p === '111/media' && init.method === 'POST') return json({ id: 'cont1' })
      if (p === '111/media_publish') return json({ id: 'midia1' })
      if (p === 'cont1') return json({ status_code: 'FINISHED' })
      if (p === 'midia1') return json({ permalink: 'https://www.instagram.com/p/abc/' })
      return json({ error: { message: `rota não simulada: ${p}`, code: 100 } })
    }
    if (url.hostname === 'arte.exemplo.com') return new Response(image, { headers: { 'content-type': 'image/png' } })
    return fetch(input, init)
  }

  const dataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nxp-ig-srv-'))
  const config = loadConfig({
    MCP_ACCESS_KEY: KEY,
    PUBLIC_BASE_URL: 'http://localhost:0',
    IG_TOKENS: JSON.stringify({ nerdexperience: 'tok-nxp', nerdverso: 'tok-verso' }),
    DATA_DIR: dataDir
  })
  const { app, publisher } = createApp({ config, fetchImpl: fakeFetch })
  await new Promise((resolve) => {
    server = app.listen(0, resolve)
  })
  base = `http://127.0.0.1:${server.address().port}`
  config.publicBaseUrl = base
  publisher.publicBaseUrl = base
})

after(() => server.close())

async function connect(url) {
  const client = new Client({ name: 'teste', version: '1.0.0' })
  await client.connect(new StreamableHTTPClientTransport(new URL(url)))
  return client
}

test('rejeita acesso sem a chave', async () => {
  const res = await fetch(`${base}/mcp/chave-errada`, { method: 'POST', body: '{}', headers: { 'content-type': 'application/json' } })
  assert.equal(res.status, 401)
  const res2 = await fetch(`${base}/mcp`, { method: 'POST', body: '{}', headers: { 'content-type': 'application/json' } })
  assert.equal(res2.status, 401)
})

test('lista ferramentas e contas pelo protocolo MCP', async () => {
  const client = await connect(`${base}/mcp/${KEY}`)
  const { tools } = await client.listTools()
  const names = tools.map((t) => t.name)
  for (const n of ['publicar_imagem', 'publicar_carrossel', 'publicar_reels', 'publicar_story', 'listar_agendamentos', 'comentarios_recentes', 'enviar_dm', 'metricas_conta']) {
    assert.ok(names.includes(n), `faltando ${n}`)
  }
  const res = await client.callTool({ name: 'listar_contas', arguments: {} })
  const contas = JSON.parse(res.content[0].text)
  assert.deepEqual(contas.map((c) => [c.conta, c.username]), [['nerdexperience', 'nerdexperience'], ['nerdverso', 'nerdverso.nxp']])
  await client.close()
})

test('publica imagem na hora e serve a mídia convertida para a Meta', async () => {
  const client = await connect(`${base}/mcp/${KEY}`)
  const res = await client.callTool({
    name: 'publicar_imagem',
    arguments: { conta: 'nerdexperience', midia: { url: 'https://arte.exemplo.com/post.png', corte: '4:5' }, legenda: 'Bora pro NXP! #nerdexperience', id_planilha: '2026-10-14_NXP_11h' }
  })
  assert.equal(res.isError, undefined, res.content[0].text)
  const job = JSON.parse(res.content[0].text)
  assert.equal(job.status, 'publicado')
  assert.equal(job.permalink, 'https://www.instagram.com/p/abc/')
  assert.equal(job.id_planilha, '2026-10-14_NXP_11h')

  const create = graphCalls.find((c) => c[1] === '/v25.0/111/media')
  const media = await fetch(create[2].image_url)
  assert.equal(media.headers.get('content-type'), 'image/jpeg')
  const meta = await sharp(Buffer.from(await media.arrayBuffer())).metadata()
  assert.equal(meta.width / meta.height, 0.8)

  const lista = await client.callTool({ name: 'listar_agendamentos', arguments: { status: 'publicado' } })
  assert.equal(JSON.parse(lista.content[0].text).length, 1)
  await client.close()
})

test('erros de validação voltam como erro da ferramenta', async () => {
  const client = await connect(`${base}/mcp/${KEY}`)
  const res = await client.callTool({
    name: 'publicar_imagem',
    arguments: { conta: 'nerdverso', midia: { url: 'https://arte.exemplo.com/post.png' }, legenda: 'x'.repeat(2300) }
  })
  assert.equal(res.isError, true)
  assert.match(res.content[0].text, /2200/)
  const res2 = await client.callTool({
    name: 'publicar_imagem',
    arguments: { conta: 'nerdverso', midia: { url: 'https://arte.exemplo.com/post.png' }, agendar_para: '2020-01-01T10:00' }
  })
  assert.match(res2.content[0].text, /já passou/)
  await client.close()
})
