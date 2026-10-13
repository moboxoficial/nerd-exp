import crypto from 'node:crypto'
import express from 'express'
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js'
import { loadConfig } from './config.js'
import { createGraph } from './graph.js'
import { Accounts } from './accounts.js'
import { createSigner, mediaRoute } from './media.js'
import { Publisher } from './publisher.js'
import { buildServer } from './tools.js'

const TOKEN_REFRESH_INTERVAL_MS = 6 * 3600 * 1000

function sameSecret(a, b) {
  const x = Buffer.from(String(a || ''))
  const y = Buffer.from(String(b))
  return x.length === y.length && crypto.timingSafeEqual(x, y)
}

export function createApp({ config, fetchImpl = fetch }) {
  const graph = createGraph({ apiHost: config.apiHost, apiVersion: config.apiVersion, fetchImpl })
  const accounts = new Accounts({ tokens: config.tokens, dataDir: config.dataDir, graph })
  const signer = createSigner(config.mediaSigningKey)
  const publisher = new Publisher({
    accounts,
    graph,
    signer,
    publicBaseUrl: config.publicBaseUrl,
    dataDir: config.dataDir,
    prepareLeadMinutes: config.prepareLeadMinutes
  })

  const app = express()
  app.disable('x-powered-by')

  app.get('/health', (req, res) => res.json({ ok: true }))

  // A Meta baixa as mídias daqui. Links são assinados e expiram.
  app.get('/media/:token', mediaRoute({ signer, fetchImpl }))

  // O claude.ai não envia cabeçalhos customizados em conectores, então a chave pode vir na URL
  // (/mcp/<chave>) ou como "Authorization: Bearer <chave>" (Claude Code e outros clientes).
  const handleMcp = async (req, res) => {
    const bearer = (req.headers.authorization || '').replace(/^Bearer\s+/i, '')
    if (!sameSecret(req.params.key || bearer, config.accessKey)) {
      return res.status(401).json({ error: 'não autorizado' })
    }
    if (req.method !== 'POST') {
      return res.status(405).set('Allow', 'POST').json({ error: 'use POST' })
    }
    const server = buildServer({ config, accounts, graph, publisher, signer, fetchImpl })
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true })
    res.on('close', () => {
      transport.close()
      server.close()
    })
    await server.connect(transport)
    await transport.handleRequest(req, res, req.body)
  }
  app.all('/mcp', express.json({ limit: '1mb' }), handleMcp)
  app.all('/mcp/:key', express.json({ limit: '1mb' }), handleMcp)

  return { app, accounts, publisher }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const config = loadConfig()
  const { app, accounts, publisher } = createApp({ config })

  setInterval(() => publisher.tick().catch((e) => console.error('[worker]', e)), config.workerIntervalMs)
  const refresh = () =>
    accounts
      .refreshStale()
      .then((r) => r.length && console.log('[tokens]', JSON.stringify(r)))
      .catch((e) => console.error('[tokens]', e))
  refresh()
  setInterval(refresh, TOKEN_REFRESH_INTERVAL_MS)

  app.listen(config.port, () => {
    console.log(`nxp-instagram MCP ouvindo na porta ${config.port} — contas: ${accounts.names().join(', ')}`)
  })
}
