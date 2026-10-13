import crypto from 'node:crypto'
import path from 'node:path'
import { JsonFile } from './store.js'

const fingerprint = (token) => crypto.createHash('sha256').update(token).digest('hex').slice(0, 16)

// Contas configuradas em IG_TOKENS. Tokens renovados ficam em DATA_DIR/tokens.json e valem
// enquanto o token original do ambiente não for trocado.
export class Accounts {
  constructor({ tokens, dataDir, graph, now = () => Date.now() }) {
    this.envTokens = tokens
    this.graph = graph
    this.now = now
    this.file = new JsonFile(path.join(dataDir, 'tokens.json'), {})
    this.profiles = new Map()
  }

  names() {
    return Object.keys(this.envTokens)
  }

  token(name) {
    const envToken = this.envTokens[name]
    if (!envToken) throw new Error(`Conta desconhecida: "${name}". Contas configuradas: ${this.names().join(', ')}`)
    const stored = this.file.read()[name]
    if (stored && stored.source === fingerprint(envToken)) return stored.token
    return envToken
  }

  // Resolve o ID do usuário do Instagram a partir do token (cacheado em memória).
  async get(name) {
    const token = this.token(name)
    let profile = this.profiles.get(name)
    if (!profile || profile.token !== token) {
      const me = await this.graph.get(token, 'me', { fields: 'user_id,username' })
      profile = { token, userId: me.user_id || me.id, username: me.username }
      this.profiles.set(name, profile)
    }
    return { name, ...profile }
  }

  async refresh(name) {
    const current = this.token(name)
    const res = await this.graph.refreshToken(current)
    const all = this.file.read()
    all[name] = {
      token: res.access_token,
      source: fingerprint(this.envTokens[name]),
      refreshedAt: new Date(this.now()).toISOString(),
      expiresAt: new Date(this.now() + Number(res.expires_in || 0) * 1000).toISOString()
    }
    this.file.write(all)
    this.profiles.delete(name)
    return { conta: name, expira_em: all[name].expiresAt }
  }

  async refreshAll(names = this.names()) {
    const results = []
    for (const name of names) {
      try {
        results.push(await this.refresh(name))
      } catch (e) {
        results.push({ conta: name, erro: e.message })
      }
    }
    return results
  }

  // Renova tokens nunca renovados aqui ou renovados há mais de maxAgeDays (tokens duram 60 dias).
  refreshStale(maxAgeDays = 7) {
    const stored = this.file.read()
    const limit = this.now() - maxAgeDays * 24 * 3600 * 1000
    const stale = this.names().filter((name) => {
      const entry = stored[name]
      return !entry || entry.source !== fingerprint(this.envTokens[name]) || Date.parse(entry.refreshedAt) < limit
    })
    return this.refreshAll(stale)
  }
}
