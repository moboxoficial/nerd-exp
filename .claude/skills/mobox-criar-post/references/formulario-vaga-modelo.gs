/**
 * MOBOX · Formulário de candidatura — Vaga de trabalho em IA e Automação
 *
 * Como usar:
 * 1. Abra https://script.google.com (logado na conta da Mobox) → "Novo projeto".
 * 2. Apague o que estiver no editor, cole este arquivo inteiro e salve.
 * 3. Clique em "Executar" (função criarFormulario) e autorize o acesso.
 * 4. Os links aparecem em "Registro de execução": formulário (para a bio),
 *    edição e a planilha de respostas.
 */
function criarFormulario() {
  var form = FormApp.create('Vaga de trabalho em IA e Automação · MOBOX Produções');
  form.setDescription(
    'A MOBOX está procurando um profissional que resolve problemas com IA: ' +
    'alguém curioso, que testa ferramentas novas e transforma processos em fluxos automatizados ' +
    '(produção de eventos, escrita de editais, comunicação e marketing).\n\n' +
    'Você não precisa saber tudo. Precisa saber perguntar, testar e validar até chegar no resultado. ' +
    'E gasto de token não vai ser problema.\n\n' +
    'Leva uns 10 minutos. Capricha no projeto: é a parte que a gente mais vai olhar.'
  );
  form.setConfirmationMessage(
    'Recebemos sua candidatura! Vamos olhar com carinho e, se fizer sentido, entramos em contato. ' +
    'Enquanto isso, acompanha a gente no @moboxproducoes. Produzindo o impossível. 💜'
  );
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false); // true exigiria login Google do candidato
  form.setProgressBar(true);

  var email = FormApp.createTextValidation().requireTextIsEmail()
    .setHelpText('Digite um e-mail válido.').build();
  var url = FormApp.createTextValidation().requireTextIsUrl()
    .setHelpText('Cole um link começando com https://').build();

  // ── 1. Sobre você ─────────────────────────────────────────────
  form.addSectionHeaderItem().setTitle('Sobre você');
  form.addTextItem().setTitle('Nome completo').setRequired(true);
  form.addTextItem().setTitle('E-mail').setValidation(email).setRequired(true);
  form.addTextItem().setTitle('WhatsApp (com DDD)').setRequired(true);
  form.addTextItem().setTitle('Cidade / Estado').setRequired(true);
  form.addTextItem().setTitle('Currículo ou LinkedIn (link)')
    .setHelpText('Link do LinkedIn ou do currículo no Drive/Dropbox (com acesso liberado).')
    .setValidation(url).setRequired(true);
  form.addTextItem().setTitle('GitHub, portfólio ou Instagram (opcional)');

  // ── 2. Você e a IA ────────────────────────────────────────────
  form.addPageBreakItem().setTitle('Você e a IA');

  form.addCheckboxItem()
    .setTitle('Quais ferramentas de IA você usa de verdade?')
    .setChoiceValues([
      'ChatGPT', 'Claude', 'Claude Code', 'Codex', 'Cursor', 'Gemini',
      'n8n / Make / Zapier', 'Lovable / Bolt / v0', 'Midjourney / geradores de imagem',
      'CapCut / ferramentas de vídeo com IA'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addGridItem()
    .setTitle('Qual sua intimidade com:')
    .setRows(['APIs', 'MCP (Model Context Protocol)', 'Banco de dados',
              'Automação de processos', 'Agentes de IA'])
    .setColumns(['Nunca usei', 'Já testei', 'Uso com frequência', 'Domino'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('Mostra pra gente: link de um projeto que você fez com IA')
    .setHelpText('Site, app, sistema, automação, repositório... Vale projeto pessoal ' +
                 '(app pra organizar sua coleção, ficha de RPG, controle de finanças).')
    .setValidation(url).setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Conta a história desse projeto')
    .setHelpText('Que problema ele resolve, como você usou a IA e o que deu errado no caminho.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Uma vez em que a IA travou ou errou feio: como você destravou?')
    .setRequired(true);

  // ── 3. Você na MOBOX ─────────────────────────────────────────
  form.addPageBreakItem().setTitle('Você na MOBOX');

  form.addParagraphTextItem()
    .setTitle('Se você começasse amanhã, qual processo de uma produtora de eventos e cultura ' +
              'você automatizaria primeiro? Por quê?')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Disponibilidade para começar')
    .setChoiceValues(['Imediata', 'Em até 15 dias', 'Em até 30 dias', 'Mais de 30 dias'])
    .setRequired(true);

  form.addTextItem().setTitle('Pretensão salarial').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Como ficou sabendo da vaga?')
    .setChoiceValues(['Instagram da MOBOX', 'Stories de alguém do time', 'Indicação de amigo', 'LinkedIn'])
    .showOtherOption(true)
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('Consentimento (LGPD)')
    .setChoiceValues(['Autorizo a MOBOX Produções a usar meus dados apenas para este processo seletivo.'])
    .setRequired(true);

  // ── Planilha de respostas ────────────────────────────────────
  var ss = SpreadsheetApp.create('Respostas · Vaga IA e Automação · MOBOX');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('Formulário (link para a bio): ' + form.shortenFormUrl(form.getPublishedUrl()));
  Logger.log('Editar formulário: ' + form.getEditUrl());
  Logger.log('Planilha de respostas: ' + ss.getUrl());
}
