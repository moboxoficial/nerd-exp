import path from 'node:path'

function required(env, name) {
  const value = env[name]
  if (!value) throw new Error(`Variável de ambiente obrigatória ausente: ${name}`)
  return value
}

function parseTokens(raw) {
  let parsed
  try {
    parsed = JSON.parse(raw)
  } catch {
    throw new Error('IG_TOKENS precisa ser um JSON, ex: {"nerdexperience":"IGAA...","nerdverso":"IGAA..."}')
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed) || Object.keys(parsed).length === 0) {
    throw new Error('IG_TOKENS precisa ter pelo menos uma conta')
  }
  for (const [name, token] of Object.entries(parsed)) {
    if (typeof token !== 'string' || !token) throw new Error(`Token vazio para a conta "${name}" em IG_TOKENS`)
  }
  return parsed
}

export function loadConfig(env = process.env) {
  const accessKey = required(env, 'MCP_ACCESS_KEY')
  if (accessKey.length < 24) throw new Error('MCP_ACCESS_KEY precisa ter pelo menos 24 caracteres')

  const publicBaseUrl = required(env, 'PUBLIC_BASE_URL').replace(/\/+$/, '')
  if (!/^https:\/\//.test(publicBaseUrl) && !/^http:\/\/(localhost|127\.0\.0\.1)/.test(publicBaseUrl)) {
    throw new Error('PUBLIC_BASE_URL precisa ser https (a Meta baixa as mídias por essa URL)')
  }

  return {
    port: Number(env.PORT || 3000),
    accessKey,
    // Chave separada para assinar os links de mídia; se ausente, deriva da chave de acesso.
    mediaSigningKey: env.MEDIA_SIGNING_KEY || `media:${accessKey}`,
    publicBaseUrl,
    tokens: parseTokens(required(env, 'IG_TOKENS')),
    apiHost: env.IG_API_HOST || 'https://graph.instagram.com',
    apiVersion: env.IG_API_VERSION || 'v25.0',
    dataDir: path.resolve(env.DATA_DIR || './data'),
    // Horários sem fuso informado são interpretados neste offset (Brasília).
    defaultUtcOffset: env.DEFAULT_UTC_OFFSET || '-03:00',
    // Quanto antes do horário agendado o vídeo começa a ser enviado para a Meta processar.
    prepareLeadMinutes: Number(env.PREPARE_LEAD_MINUTES || 20),
    workerIntervalMs: Number(env.WORKER_INTERVAL_MS || 30000)
  }
}
