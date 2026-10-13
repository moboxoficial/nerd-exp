function offsetMinutes(offset) {
  const m = /^([+-])(\d\d):?(\d\d)$/.exec(offset)
  if (!m) throw new Error(`Offset inválido: ${offset}`)
  return (m[1] === '-' ? -1 : 1) * (Number(m[2]) * 60 + Number(m[3]))
}

// Aceita ISO 8601. Sem fuso explícito, usa o offset padrão (Brasília).
export function parseWhen(value, defaultOffset) {
  const str = String(value).trim().replace(' ', 'T')
  const withZone = /([zZ]|[+-]\d\d:?\d\d)$/.test(str) ? str : `${str}${defaultOffset}`
  const ms = Date.parse(withZone)
  if (Number.isNaN(ms)) throw new Error(`Data/hora inválida: "${value}". Use o formato 2026-10-14T11:00`)
  return ms
}

export function formatLocal(ms, offset) {
  if (ms === undefined || ms === null) return null
  const shifted = new Date(ms + offsetMinutes(offset) * 60000).toISOString()
  return `${shifted.slice(0, 19)}${offset}`
}
