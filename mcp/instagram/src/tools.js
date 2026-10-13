import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { z } from 'zod'
import { CROPS, preflight, publicMediaUrl } from './media.js'
import { FINAL_STATUSES } from './publisher.js'
import { formatLocal, parseWhen } from './time.js'

const MAX_CAPTION = 2200
const MAX_HASHTAGS = 30

const ok = (data) => ({ content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] })
const fail = (e) => ({ isError: true, content: [{ type: 'text', text: `Erro: ${e.message}` }] })

function validateCaption(legenda) {
  if (!legenda) return
  if (legenda.length > MAX_CAPTION) throw new Error(`Legenda com ${legenda.length} caracteres (máximo ${MAX_CAPTION})`)
  const hashtags = legenda.match(/#[\p{L}\p{N}_]+/gu) || []
  if (hashtags.length > MAX_HASHTAGS) throw new Error(`Legenda com ${hashtags.length} hashtags (máximo ${MAX_HASHTAGS})`)
}

export function buildServer({ config, accounts, graph, publisher, signer, fetchImpl = fetch }) {
  const server = new McpServer({ name: 'nxp-instagram', version: '0.1.0' })
  const offset = config.defaultUtcOffset
  const names = accounts.names()

  const tool = (name, def, handler) =>
    server.registerTool(name, def, async (args) => {
      try {
        return ok(await handler(args))
      } catch (e) {
        return fail(e)
      }
    })

  const conta = z.enum(names).describe(`Conta do Instagram: ${names.join(' ou ')}`)
  const fonte = {
    url: z.string().optional().describe('URL https da mídia (export do Canva, link do Google Drive etc.)'),
    drive_file_id: z.string().optional().describe('ID do arquivo no Google Drive (precisa estar compartilhado como "Qualquer pessoa com o link")'),
    corte: z
      .enum(Object.keys(CROPS))
      .optional()
      .describe('Corte central aplicado em imagens antes de publicar. Feed: 4:5 (recomendado) ou 1:1. Story: 9:16. Padrão: original')
  }
  const fonteSchema = z.object(fonte)
  const comTipo = z.object({
    ...fonte,
    tipo: z.enum(['imagem', 'video']),
    alt_text: z.string().optional().describe('Texto alternativo (acessibilidade), só para imagens')
  })
  const legenda = z.string().optional().describe(`Legenda completa com hashtags (até ${MAX_CAPTION} caracteres)`)
  const colaboradores = z
    .array(z.string())
    .max(3)
    .optional()
    .describe('Usernames convidados para post em collab (sem @, até 3). O convite precisa ser aceito no app.')
  const agendarPara = z
    .string()
    .optional()
    .describe('Quando publicar, ex: "2026-10-14T11:00" (horário de Brasília se não tiver fuso). Vazio = publicar agora.')
  const idPlanilha = z.string().optional().describe('ID do post na planilha de calendário, ex: 2026-10-14_NXP_11h')

  const view = (job) => ({
    id: job.id,
    conta: job.conta,
    formato: job.formato,
    status: job.status,
    agendado_para: formatLocal(job.run_at, offset),
    id_planilha: job.id_planilha,
    permalink: job.permalink,
    media_id: job.media_id,
    erro: job.erro,
    tentativas: job.tentativas,
    legenda: job.payload.legenda || null,
    criado_em: job.criado_em
  })

  async function enqueue({ conta, formato, payload, agendar_para, id_planilha, checks }) {
    validateCaption(payload.legenda)
    await Promise.all(checks.map((c) => preflight({ ...c, fetchImpl })))
    const now = Date.now()
    const runAt = agendar_para ? parseWhen(agendar_para, offset) : now
    if (runAt < now - 60 * 1000) throw new Error(`O horário ${formatLocal(runAt, offset)} já passou`)
    let job = publisher.create({ conta, formato, payload, runAt, idPlanilha: id_planilha })
    if (runAt <= now + 60 * 1000) {
      job = await publisher.runNow(job.id)
      if (!FINAL_STATUSES.includes(job.status)) {
        return { ...view(job), aviso: 'A Meta ainda está processando. Consulte com ver_agendamento em alguns minutos.' }
      }
    }
    return view(job)
  }

  // ---------- Contas ----------

  tool(
    'listar_contas',
    { title: 'Listar contas', description: 'Lista as contas do Instagram conectadas com seguidores e número de posts.', inputSchema: {} },
    async () =>
      Promise.all(
        names.map(async (name) => {
          try {
            const acc = await accounts.get(name)
            const p = await graph.get(acc.token, acc.userId, {
              fields: 'username,name,account_type,followers_count,follows_count,media_count'
            })
            return { conta: name, user_id: acc.userId, ...p }
          } catch (e) {
            return { conta: name, erro: e.message }
          }
        })
      )
  )

  tool(
    'limite_publicacao',
    {
      title: 'Limite de publicação',
      description: 'Quantos posts a conta já publicou via API nas últimas 24h e o limite da Meta.',
      inputSchema: { conta }
    },
    async ({ conta }) => {
      const acc = await accounts.get(conta)
      return graph.get(acc.token, `${acc.userId}/content_publishing_limit`, { fields: 'quota_usage,config' })
    }
  )

  tool(
    'renovar_tokens',
    {
      title: 'Renovar tokens',
      description: 'Renova os tokens de acesso (valem 60 dias). O servidor já faz isso sozinho; use se aparecer erro de token expirado.',
      inputSchema: {}
    },
    () => accounts.refreshAll()
  )

  // ---------- Publicação ----------

  tool(
    'verificar_midia',
    {
      title: 'Verificar mídia',
      description:
        'Baixa e valida uma mídia antes de publicar (acesso, formato, proporção) e devolve um link de prévia com o corte aplicado.',
      inputSchema: { ...fonte, tipo: z.enum(['imagem', 'video']), feed: z.boolean().optional().describe('Validar proporção de feed (padrão true)') }
    },
    async ({ tipo, feed, ...source }) => {
      const info = await preflight({ source, kind: tipo === 'video' ? 'video' : 'image', feed: feed !== false, fetchImpl })
      const previa = publicMediaUrl({ signer, publicBaseUrl: config.publicBaseUrl, source, kind: tipo === 'video' ? 'video' : 'image' })
      return { ...info, previa_url: previa }
    }
  )

  tool(
    'publicar_imagem',
    {
      title: 'Publicar imagem no feed',
      description: 'Publica ou agenda um post estático (uma imagem) no feed.',
      inputSchema: { conta, midia: fonteSchema, legenda, alt_text: z.string().optional(), colaboradores, agendar_para: agendarPara, id_planilha: idPlanilha }
    },
    ({ conta, midia, legenda, alt_text, colaboradores, agendar_para, id_planilha }) =>
      enqueue({
        conta,
        formato: 'imagem',
        payload: { midia, legenda, alt_text, colaboradores },
        agendar_para,
        id_planilha,
        checks: [{ source: midia, kind: 'image', feed: true }]
      })
  )

  tool(
    'publicar_carrossel',
    {
      title: 'Publicar carrossel',
      description: 'Publica ou agenda um carrossel de 2 a 10 imagens e/ou vídeos. Use o mesmo corte em todas as imagens.',
      inputSchema: { conta, itens: z.array(comTipo).min(2).max(10), legenda, colaboradores, agendar_para: agendarPara, id_planilha: idPlanilha }
    },
    ({ conta, itens, legenda, colaboradores, agendar_para, id_planilha }) =>
      enqueue({
        conta,
        formato: 'carrossel',
        payload: { itens, legenda, colaboradores },
        agendar_para,
        id_planilha,
        checks: itens.map((i) => ({ source: i, kind: i.tipo === 'video' ? 'video' : 'image', feed: true }))
      })
  )

  tool(
    'publicar_reels',
    {
      title: 'Publicar reels',
      description:
        'Publica ou agenda um reels (vídeo vertical 9:16, MP4/H.264). Vídeos começam a subir alguns minutos antes do horário para a Meta processar. Música da biblioteca do Instagram não é suportada pela API.',
      inputSchema: {
        conta,
        video: fonteSchema,
        legenda,
        capa: fonteSchema.optional().describe('Imagem de capa (opcional)'),
        thumb_offset_ms: z.number().int().min(0).optional().describe('Se não tiver capa, momento do vídeo (ms) usado como capa'),
        mostrar_no_feed: z.boolean().optional().describe('Também aparece na grade do perfil (padrão true)'),
        nome_audio: z.string().optional().describe('Nome do áudio original exibido no reels'),
        colaboradores,
        agendar_para: agendarPara,
        id_planilha: idPlanilha
      }
    },
    ({ conta, video, legenda, capa, thumb_offset_ms, mostrar_no_feed, nome_audio, colaboradores, agendar_para, id_planilha }) =>
      enqueue({
        conta,
        formato: 'reels',
        payload: { video, legenda, capa, thumb_offset_ms, mostrar_no_feed, nome_audio, colaboradores },
        agendar_para,
        id_planilha,
        checks: [{ source: video, kind: 'video' }, ...(capa ? [{ source: capa, kind: 'image', feed: false }] : [])]
      })
  )

  tool(
    'publicar_story',
    {
      title: 'Publicar story',
      description:
        'Publica ou agenda um story (imagem ou vídeo, 9:16). Figurinhas (link, enquete, música, menção) não são suportadas pela API — essas precisam ser postadas pelo app.',
      inputSchema: { conta, midia: comTipo, agendar_para: agendarPara, id_planilha: idPlanilha }
    },
    ({ conta, midia, agendar_para, id_planilha }) =>
      enqueue({
        conta,
        formato: 'story',
        payload: { midia },
        agendar_para,
        id_planilha,
        checks: [{ source: midia, kind: midia.tipo === 'video' ? 'video' : 'image', feed: false }]
      })
  )

  // ---------- Agendamentos ----------

  tool(
    'listar_agendamentos',
    {
      title: 'Listar agendamentos',
      description: 'Lista posts agendados/publicados por este servidor, em ordem de horário.',
      inputSchema: {
        conta: conta.optional(),
        status: z.enum(['agendado', 'preparando', 'publicado', 'erro', 'cancelado']).optional(),
        desde: z.string().optional().describe('Data/hora inicial, ex: 2026-10-14'),
        ate: z.string().optional().describe('Data/hora final, ex: 2026-10-20T23:59')
      }
    },
    ({ conta, status, desde, ate }) => {
      const from = desde ? parseWhen(desde.length === 10 ? `${desde}T00:00` : desde, offset) : -Infinity
      const to = ate ? parseWhen(ate.length === 10 ? `${ate}T23:59:59` : ate, offset) : Infinity
      return publisher
        .all()
        .filter((j) => (!conta || j.conta === conta) && (!status || j.status === status) && j.run_at >= from && j.run_at <= to)
        .sort((a, b) => a.run_at - b.run_at)
        .map(view)
    }
  )

  tool(
    'ver_agendamento',
    { title: 'Ver agendamento', description: 'Mostra o status de um post agendado.', inputSchema: { id: z.string() } },
    ({ id }) => view(publisher.get(id))
  )

  tool(
    'cancelar_agendamento',
    { title: 'Cancelar agendamento', description: 'Cancela um post que ainda está "agendado".', inputSchema: { id: z.string() } },
    ({ id }) => view(publisher.cancel(id))
  )

  tool(
    'reagendar',
    {
      title: 'Reagendar',
      description: 'Muda o horário de um post "agendado" ou tenta de novo um post com "erro".',
      inputSchema: { id: z.string(), agendar_para: z.string().describe('Novo horário, ex: 2026-10-14T18:00') }
    },
    ({ id, agendar_para }) => {
      const runAt = parseWhen(agendar_para, offset)
      if (runAt < Date.now() - 60 * 1000) throw new Error(`O horário ${formatLocal(runAt, offset)} já passou`)
      return view(publisher.reschedule(id, runAt))
    }
  )

  // ---------- Posts e métricas ----------

  tool(
    'listar_posts',
    {
      title: 'Listar posts',
      description: 'Últimos posts publicados na conta, com curtidas e comentários.',
      inputSchema: { conta, limite: z.number().int().min(1).max(50).optional() }
    },
    async ({ conta, limite }) => {
      const acc = await accounts.get(conta)
      const res = await graph.get(acc.token, `${acc.userId}/media`, {
        fields: 'id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count',
        limit: limite || 12
      })
      return res.data
    }
  )

  tool(
    'metricas_post',
    {
      title: 'Métricas do post',
      description: 'Métricas de um post, reels ou story (alcance, visualizações, interações, salvamentos, compartilhamentos).',
      inputSchema: {
        conta,
        media_id: z.string(),
        metricas: z.string().optional().describe('Lista separada por vírgula para sobrescrever as métricas padrão')
      }
    },
    async ({ conta, media_id, metricas }) => {
      const acc = await accounts.get(conta)
      const media = await graph.get(acc.token, media_id, { fields: 'media_product_type,permalink,timestamp' })
      const metric =
        metricas ||
        (media.media_product_type === 'STORY'
          ? 'reach,views,replies,shares,total_interactions'
          : 'reach,views,likes,comments,shares,saved,total_interactions')
      const res = await graph.get(acc.token, `${media_id}/insights`, { metric })
      const valores = Object.fromEntries(res.data.map((m) => [m.name, m.total_value?.value ?? m.values?.[0]?.value]))
      return { ...media, metricas: valores }
    }
  )

  tool(
    'metricas_conta',
    {
      title: 'Métricas da conta',
      description: 'Totais da conta num período (máximo 30 dias): alcance, visualizações, contas engajadas, interações.',
      inputSchema: {
        conta,
        desde: z.string().describe('Data inicial, ex: 2026-10-01'),
        ate: z.string().describe('Data final, ex: 2026-10-13'),
        metricas: z.string().optional().describe('Lista separada por vírgula para sobrescrever as métricas padrão')
      }
    },
    async ({ conta, desde, ate, metricas }) => {
      const acc = await accounts.get(conta)
      const since = Math.floor(parseWhen(desde.length === 10 ? `${desde}T00:00` : desde, offset) / 1000)
      const until = Math.floor(parseWhen(ate.length === 10 ? `${ate}T23:59:59` : ate, offset) / 1000)
      const res = await graph.get(acc.token, `${acc.userId}/insights`, {
        metric: metricas || 'reach,views,accounts_engaged,total_interactions,likes,comments,shares,saves',
        period: 'day',
        metric_type: 'total_value',
        since,
        until
      })
      return Object.fromEntries(res.data.map((m) => [m.name, m.total_value?.value ?? m.values]))
    }
  )

  // ---------- Comunidade: comentários ----------

  tool(
    'comentarios_recentes',
    {
      title: 'Comentários recentes',
      description:
        'Junta os comentários dos últimos posts da conta, para triagem da comunidade. Pode filtrar só os que ainda não têm resposta da conta.',
      inputSchema: {
        conta,
        posts: z.number().int().min(1).max(30).optional().describe('Quantos posts recentes olhar (padrão 10)'),
        desde: z.string().optional().describe('Só comentários a partir desta data/hora'),
        sem_resposta: z.boolean().optional().describe('Só comentários sem resposta da conta (padrão true)')
      }
    },
    async ({ conta, posts, desde, sem_resposta }) => {
      const acc = await accounts.get(conta)
      const from = desde ? parseWhen(desde.length === 10 ? `${desde}T00:00` : desde, offset) : 0
      const media = await graph.get(acc.token, `${acc.userId}/media`, {
        fields: 'id,caption,permalink,timestamp,comments_count',
        limit: posts || 10
      })
      const out = []
      for (const m of media.data.filter((x) => x.comments_count > 0)) {
        const res = await graph.get(acc.token, `${m.id}/comments`, {
          fields: 'id,text,username,timestamp,like_count,hidden,replies{id,text,username,timestamp}',
          limit: 50
        })
        for (const c of res.data) {
          if (Date.parse(c.timestamp) < from) continue
          const replies = c.replies?.data || []
          const answered = replies.some((r) => r.username === acc.username)
          if (sem_resposta !== false && answered) continue
          out.push({
            comentario_id: c.id,
            usuario: c.username,
            texto: c.text,
            quando: c.timestamp,
            curtidas: c.like_count,
            oculto: c.hidden,
            respostas: replies.map((r) => ({ usuario: r.username, texto: r.text })),
            post: { id: m.id, link: m.permalink, legenda: (m.caption || '').slice(0, 80) }
          })
        }
      }
      return out
    }
  )

  tool(
    'responder_comentario',
    {
      title: 'Responder comentário',
      description: 'Responde publicamente a um comentário. Só use depois que a pessoa responsável aprovar o texto.',
      inputSchema: { conta, comentario_id: z.string(), mensagem: z.string().min(1) }
    },
    async ({ conta, comentario_id, mensagem }) => {
      const acc = await accounts.get(conta)
      return graph.post(acc.token, `${comentario_id}/replies`, { message: mensagem })
    }
  )

  tool(
    'ocultar_comentario',
    {
      title: 'Ocultar comentário',
      description: 'Oculta (ou volta a mostrar) um comentário. Use para spam e ofensas.',
      inputSchema: { conta, comentario_id: z.string(), ocultar: z.boolean().optional().describe('false para reexibir (padrão true)') }
    },
    async ({ conta, comentario_id, ocultar }) => {
      const acc = await accounts.get(conta)
      return graph.post(acc.token, comentario_id, { hide: ocultar !== false })
    }
  )

  tool(
    'apagar_comentario',
    {
      title: 'Apagar comentário',
      description: 'Apaga um comentário de forma definitiva. Prefira ocultar; apague só com confirmação explícita.',
      inputSchema: { conta, comentario_id: z.string() }
    },
    async ({ conta, comentario_id }) => {
      const acc = await accounts.get(conta)
      return graph.del(acc.token, comentario_id)
    }
  )

  // ---------- Comunidade: DMs ----------

  async function messageDetails(token, ids) {
    return Promise.all(
      ids.map(async (id) => {
        const m = await graph.get(token, id, { fields: 'id,created_time,from,to,message' })
        return { id: m.id, quando: m.created_time, de: m.from?.username || m.from?.id, de_id: m.from?.id, texto: m.message }
      })
    )
  }

  tool(
    'listar_conversas',
    {
      title: 'Listar DMs',
      description: 'Conversas de DM mais recentes, com a última mensagem de cada uma.',
      inputSchema: { conta, limite: z.number().int().min(1).max(25).optional() }
    },
    async ({ conta, limite }) => {
      const acc = await accounts.get(conta)
      const res = await graph.get(acc.token, 'me/conversations', { platform: 'instagram', limit: limite || 10 })
      return Promise.all(
        res.data.map(async (c) => {
          const conv = await graph.get(acc.token, c.id, { fields: 'messages' })
          const [ultima] = await messageDetails(acc.token, (conv.messages?.data || []).slice(0, 1).map((m) => m.id))
          return { conversa_id: c.id, atualizada_em: c.updated_time, ultima_mensagem: ultima || null }
        })
      )
    }
  )

  tool(
    'ler_conversa',
    {
      title: 'Ler DM',
      description: 'Mensagens mais recentes de uma conversa (a API só devolve as 20 últimas).',
      inputSchema: { conta, conversa_id: z.string(), limite: z.number().int().min(1).max(20).optional() }
    },
    async ({ conta, conversa_id, limite }) => {
      const acc = await accounts.get(conta)
      const conv = await graph.get(acc.token, conversa_id, { fields: 'messages' })
      const ids = (conv.messages?.data || []).slice(0, limite || 10).map((m) => m.id)
      return messageDetails(acc.token, ids)
    }
  )

  tool(
    'enviar_dm',
    {
      title: 'Enviar DM',
      description:
        'Envia uma DM de texto. A Meta só permite responder até 24h depois da última mensagem da pessoa (até 7 dias com agente_humano). Só envie com aprovação.',
      inputSchema: {
        conta,
        destinatario_id: z.string().describe('ID da pessoa (campo de_id em ler_conversa)'),
        texto: z.string().min(1).max(1000),
        agente_humano: z.boolean().optional().describe('Resposta escrita/aprovada por uma pessoa da equipe, permite responder até 7 dias')
      }
    },
    async ({ conta, destinatario_id, texto, agente_humano }) => {
      const acc = await accounts.get(conta)
      return graph.post(acc.token, 'me/messages', {
        recipient: { id: destinatario_id },
        message: { text: texto },
        ...(agente_humano ? { messaging_type: 'MESSAGE_TAG', tag: 'HUMAN_AGENT' } : {})
      })
    }
  )

  return server
}
