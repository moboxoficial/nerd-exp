#!/usr/bin/env bash
# Sobe o conector do Instagram no seu computador e liga no Claude Code.
# Uso (de dentro de mcp/instagram):  ./scripts/rodar-local.sh
# Ctrl+C desliga tudo.
set -euo pipefail

cd "$(dirname "$0")/.."
PORT="${PORT:-3000}"
CONTAS=(nerdexperience nerdverso)
LOGS="$(pwd)/data/logs"
mkdir -p "$LOGS"

passo() { printf '\n\033[1;35m▶ %s\033[0m\n' "$1"; }
erro() { printf '\n\033[1;31m✖ %s\033[0m\n' "$1" >&2; exit 1; }

# ---------- 1. Pré-requisitos ----------
passo "Conferindo pré-requisitos"
command -v node >/dev/null || erro "Node não encontrado. Instale o Node 20+ em https://nodejs.org"
[ "$(node -p 'process.versions.node.split(".")[0]')" -ge 20 ] || erro "Precisa do Node 20 ou mais novo (você tem $(node -v))"
if ! command -v cloudflared >/dev/null; then
  if [[ "$(uname)" == "Darwin" ]] && command -v brew >/dev/null; then
    echo "Instalando o cloudflared pelo Homebrew..."
    brew install cloudflared
  else
    erro "cloudflared não encontrado. Instale em https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
  fi
fi
[ -d node_modules ] || npm install --silent
echo "ok"

# ---------- 2. Configuração (.env) ----------
if [ ! -f .env ]; then
  passo "Configurando pela primeira vez"
  echo "Cole o token de cada conta (começa com IGAA). O texto não aparece na tela."
  tokens_json="{}"
  for conta in "${CONTAS[@]}"; do
    read -r -s -p "  Token de $conta: " token
    echo
    [ -n "$token" ] || erro "Token de $conta vazio"
    tokens_json="$(node -e 'const o=JSON.parse(process.argv[1]);o[process.argv[2]]=process.argv[3];console.log(JSON.stringify(o))' "$tokens_json" "$conta" "$token")"
  done
  umask 077
  {
    echo "MCP_ACCESS_KEY=$(node -e 'console.log(require("crypto").randomBytes(24).toString("hex"))')"
    echo "PUBLIC_BASE_URL=http://localhost:$PORT"
    echo "IG_TOKENS=$tokens_json"
    echo "DATA_DIR=./data"
  } > .env
  echo ".env criado (só você tem acesso a ele)."
fi

ler_env() { grep -E "^$1=" .env | head -1 | cut -d= -f2-; }
MCP_ACCESS_KEY="$(ler_env MCP_ACCESS_KEY)"
IG_TOKENS="$(ler_env IG_TOKENS)"

# ---------- 3. Confere os tokens direto na Meta ----------
passo "Conferindo os tokens na Meta"
node --input-type=module -e '
const tokens = JSON.parse(process.argv[1])
let falhou = false
for (const [conta, token] of Object.entries(tokens)) {
  const r = await fetch(`https://graph.instagram.com/me?fields=username&access_token=${encodeURIComponent(token)}`)
  const b = await r.json()
  if (b.username) console.log(`  ${conta} → @${b.username}`)
  else { falhou = true; console.log(`  ${conta} → ERRO: ${b.error?.message || r.status}`) }
}
if (falhou) { console.log("\nGere o token de novo no painel da Meta e apague o arquivo .env para recomeçar."); process.exit(1) }
' "$IG_TOKENS" || erro "Algum token não funcionou"

# ---------- 4. Túnel público (a Meta baixa as mídias por ele) ----------
passo "Abrindo endereço público temporário"
pids=()
encerrar() {
  echo
  echo "Desligando..."
  for p in "${pids[@]}"; do kill "$p" 2>/dev/null || true; done
}
trap encerrar EXIT INT TERM

cloudflared tunnel --no-autoupdate --url "http://localhost:$PORT" > "$LOGS/tunel.log" 2>&1 &
pids+=($!)
url=""
for _ in $(seq 1 60); do
  url="$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOGS/tunel.log" | head -1 || true)"
  [ -n "$url" ] && break
  sleep 1
done
[ -n "$url" ] || erro "O túnel não abriu. Veja $LOGS/tunel.log"
echo "$url"

# ---------- 5. Servidor ----------
passo "Ligando o servidor"
PUBLIC_BASE_URL="$url" PORT="$PORT" node --env-file=.env src/server.js > "$LOGS/servidor.log" 2>&1 &
pids+=($!)
for _ in $(seq 1 30); do
  curl -sf "http://localhost:$PORT/health" >/dev/null && break
  sleep 1
done
curl -sf "http://localhost:$PORT/health" >/dev/null || erro "O servidor não subiu. Veja $LOGS/servidor.log"
echo "ok"

# ---------- 6. Liga no Claude Code ----------
if command -v claude >/dev/null; then
  passo "Conectando no Claude Code"
  # Escopo local: o conector só existe quando o Claude Code é aberto na pasta deste repositório,
  # sem aparecer nos seus outros projetos.
  REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || (cd ../.. && pwd))"
  (
    cd "$REPO_ROOT"
    claude mcp remove instagram-nxp --scope local >/dev/null 2>&1 || true
    claude mcp add --scope local --transport http instagram-nxp "http://localhost:$PORT/mcp" \
      --header "Authorization: Bearer $MCP_ACCESS_KEY" >/dev/null
  )
  echo "Conector \"instagram-nxp\" adicionado só para o projeto em $REPO_ROOT."
else
  echo
  echo "Claude Code não encontrado. Para conectar manualmente:"
  echo "  URL:   http://localhost:$PORT/mcp"
  echo "  Header Authorization: Bearer <MCP_ACCESS_KEY do .env>"
fi

printf '\n\033[1;32m✔ Tudo no ar.\033[0m Abra outro terminal NA PASTA DO REPOSITÓRIO, rode "claude" e peça: "lista as contas do Instagram".\n'
echo "Deixe esta janela aberta: os agendamentos só saem enquanto ela estiver rodando. Ctrl+C desliga."
echo "Logs: $LOGS"
wait
