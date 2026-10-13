// Cliente mínimo da API do Instagram (Instagram API with Instagram Login, graph.instagram.com).

export class GraphError extends Error {
  constructor(message, { status, code, subcode, transient, fbtraceId } = {}) {
    super(message)
    this.name = 'GraphError'
    this.status = status
    this.code = code
    this.subcode = subcode
    this.transient = Boolean(transient)
    this.fbtraceId = fbtraceId
  }
}

function toQuery(params) {
  const qs = new URLSearchParams()
  for (const [key, value] of Object.entries(params || {})) {
    if (value === undefined || value === null) continue
    qs.set(key, typeof value === 'object' ? JSON.stringify(value) : String(value))
  }
  return qs
}

export function createGraph({ apiHost, apiVersion, fetchImpl = fetch }) {
  async function parse(res) {
    const text = await res.text()
    let body
    try {
      body = text ? JSON.parse(text) : {}
    } catch {
      body = { raw: text }
    }
    if (!res.ok || body.error) {
      const err = body.error || {}
      const message = err.error_user_msg || err.message || `HTTP ${res.status}`
      throw new GraphError(message, {
        status: res.status,
        code: err.code,
        subcode: err.error_subcode,
        transient: err.is_transient || res.status >= 500 || res.status === 429,
        fbtraceId: err.fbtrace_id
      })
    }
    return body
  }

  async function request(token, method, path, params) {
    const url = new URL(`${apiHost}/${apiVersion}/${path.replace(/^\/+/, '')}`)
    const init = { method }
    if (method === 'GET' || method === 'DELETE') {
      const qs = toQuery(params)
      qs.set('access_token', token)
      url.search = qs.toString()
    } else {
      url.searchParams.set('access_token', token)
      init.headers = { 'Content-Type': 'application/json' }
      init.body = JSON.stringify(params || {})
    }
    let res
    try {
      res = await fetchImpl(url, init)
    } catch (e) {
      throw new GraphError(`Falha de rede ao chamar a API do Instagram: ${e.message}`, { transient: true })
    }
    return parse(res)
  }

  return {
    get: (token, path, params) => request(token, 'GET', path, params),
    post: (token, path, params) => request(token, 'POST', path, params),
    del: (token, path, params) => request(token, 'DELETE', path, params),
    // Renova um token de longa duração (válido por 60 dias). Só funciona com tokens com mais de 24h.
    async refreshToken(token) {
      const url = new URL(`${apiHost}/refresh_access_token`)
      url.search = toQuery({ grant_type: 'ig_refresh_token', access_token: token }).toString()
      return parse(await fetchImpl(url))
    }
  }
}
