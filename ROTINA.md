# Rotina diária: Pauta do dia - Edição, Fechamento e e-mail

Documento de referência das três checagens automáticas. Leia inteiro antes de agir. Fuso: Manaus (UTC-4), o mesmo do computador.
Documento vivo com o processo completo: https://claude.ai/artifact/BRCS18JMFugf7ArdUbhEXw

## Calendário e horários
- Três tarefas agendadas, **de segunda a sexta**, disparando às 09:00, 14:00 e 19:00 de Manaus (programadas 08:46, 13:48 e 18:56 para compensar o atraso fixo do agendador). Sábado, domingo e feriados (`feriados.json`) são dias off.
- Dia off, atraso e computador desligado: seguir as regras da seção "As três checagens" mais abaixo.

## Entregas e links fixos (sempre atualizar o mesmo link)
- Pauta do dia - Edição (artefato): https://claude.ai/artifact/VE85kUEmeMFVZfrbfQKzjM. Publicar com a ferramenta Artifact usando `file_path` = `saida\prioridades.html` e `url` acima (mesma página, o banco de marcações é preservado).
- Fechamento (artefato): https://claude.ai/artifact/1gu1mT55CDPnUkdpbWutfJ. Publicar `saida\fechamento.out.html` no mesmo `url`.
- PDFs do dia no Google Drive da conta diana.savi@vanguardamartech.com.br: pasta RELATÓRIOS (https://drive.google.com/drive/folders/11_HweEj_5lGI9BqI5acSKdH95-OlVCM9), subpastas ANO / MM - Mês / DD, arquivos com a data no nome.
- E-mail diário para luana.rocha@vanguardamartech.com.br ao fim da checagem das 19:00, com botões para os PDFs no Drive (e os 3 PDFs em anexo apenas se existir `email_config.json`).

## Pasta e arquivos
`D:\Vibecodas\Claude\pauta-diaria\`
- `dia.py`: configuração do dia (datas, frase do título, pedidos de prioridade com quem pediu, reservas de editor, jobs só de arte a excluir). Reescrever todo dia.
- `data.py`: lista `D` com os jobs da pauta. Cada linha: `[grupo, idJob, cliente, título, etapa atual, responsável, prazo dd/mm, pedido ("WA hh:mm", "Chat hh:mm" ou ""), [[etapa desatualizada, data, responsável], ...]]`. Responsável do Tráfego = "TRÁFEGO". Nome do editor: "Guilherme Benevides".
- `report_data.py`: dados do fechamento. `EXEC` (executados pelos editores), `SUP` (executados pela Diana), `MOVED` (id do job reprogramado: evidência), `FLAGS` (id: [ajustes, refações, etapas de edição]), `DET` (id: lista de motivos), `RECORRENTES` (texto).
- `template.html` (Pauta), `fechamento.html` (Fechamento): modelos. Não mudar, a não ser por pedido.
- `build_all.py`: gera tudo em `saida\` (HTML das duas páginas, HTML dos dois PDFs, corpo do e-mail e os 3 PDFs). `python build_all.py`.
- `snippets_iclips.js`: trechos de leitura do iClips que funcionam no navegador integrado.
- `enviar_email.py`: envia o e-mail com anexos por SMTP (precisa de `email_config.json`, criado só pela Diana).
- `iniciar_ponte.ps1`: liga a ponte do WhatsApp, se estiver desligada.
- `salvar_drive.py`: copia os 3 PDFs para `pasta_local` (em `drive.json`) na estrutura ANO / MM - Mês / DD. Sai com código 4 se `pasta_local` estiver vazio.
- `drive.json`: `pasta_raiz_url` (botão da pasta no e-mail) e `pasta_local` (hoje `J:\Meu Drive\RELATÓRIOS`, conta diana.savi@vanguardamartech.com.br). A letra da unidade pode mudar; conferir pela descrição "diana.savi@vanguardamartech" em `Get-PSDrive` e atualizar se preciso. Nunca usar a unidade da conta dianasavi.vanguarda@gmail.com.
- `feriados.json`: feriados de Manaus (dias off), mantido pela Diana.
- `estado\AAAA-MM-DD\`: cópia de `dia.py`, `data.py` e `report_data.py` de cada checagem (09h, 14h, 19h). Guardar sempre.

## Regras da Pauta do dia
- Só jobs de vídeo (etapa de edição, animação ou vídeo aberta). Jobs só de arte (embalagem, flâmula, carrossel, card, KV, adesivo, cartela) ficam fora, salvo se tiverem edição de vídeo reservada a um editor.
- Recorrentes fora da pauta: VTs MAO e BVB adulto e infantil (FDS Fraldas) e VTs Fitness MAO e BVB de 15 e 30 (terça e quarta) do Santo Remédio. Qualquer outro job do cliente é normal. Identificar pelo título.
- Cinco grupos: 1 já com edição/animação (editor definido); 2 com o Tráfego em edição/animação; 3 bloqueado em aprovação interna; 4 em outras etapas e fora do Tráfego; 5 com o Tráfego em outra etapa. Etapa sem responsável pertence ao Tráfego.
- Cada job: título com link (https://app.iclips.com.br/vanguarda/JobPeca/Atividade/ID), prazo, etapa atual, responsável, etapas anteriores com data antes de hoje como "etapa X desatualizada - responsável".
- Pedidos de prioridade: selo SOLICITADA PRIORIDADE com quem pediu (nome como link wa.me; no Chat o nome), dia, hora e canal. Pedido sem nome salvo: número como link. Pedidos do dia anterior, lidos no grupo WhatsApp "VGRDA/ JOBS Accounts" e nos espaços do Google Chat "Tráfego | Mídia Paga" e "Tráfego | Social Media".
- Carga: editores Hudson Soares, Guilherme Benevides e Vinicius Alves. Capacidade 6 a 8 jobs por editor. Conta jobs em produção (etapa atual de vídeo com ele) mais reservados (etapa de vídeo atribuída a ele, travada por etapa anterior; registrar em `RESERVA` no `dia.py`). Acima de 8: ACIMA DA CAPACIDADE em vermelho. Abaixo de 6: com folga. Vinicius nunca mostra "com folga": mostra "Pega os VTs semanais esporádicos". Diana é supervisora, aparece à parte e fica fora do cálculo.
- Ajustes e refações: contam só etapas de ajuste ou refação depois da primeira etapa de vídeo do job. Claquete e arquivamento não contam como etapa de edição. Marcador por job; acima de 2 fica vermelho. Mais de uma etapa de edição/animação também recebe marcador.
- Para cada job com ajuste, ler a aba Comentários e o Briefing do job no iClips e classificar cada motivo: quem pediu, quando, o que pediu e o tipo. Briefing já indicava: **Erro de edição**. Briefing não indicava: **Briefing sem as informações solicitadas**. Veio do cliente: **Alteração do cliente**. Outros: Material errado, Conteúdo, Informação do VT. Gravar em `DET` com a linha "b" (evidência do briefing) e `FLAGS`.
- Título da página: uma frase curta de jargão publicitário, **nova a cada dia, nunca repetida** (a de 15/10 foi "Menos briefing, mais render."), mais "Pauta do dia - DD/MM". Texto de abertura fixo, já no modelo.

## Regras do Fechamento
- Executado: jobs de vídeo trabalhados pelos três editores e pela Diana, segundo o relatório Atividades realizadas por colaborador (sessões do dia). Cada job conta uma vez na soma ("X de Y"). Ajuste conta como execução. Parcial = ajuste aberto na etapa de vídeo.
- Recorrentes de Santo Remédio aparecem só aqui, por editor, com quantidade e quais VTs.
- Reprogramado: job com editor definido cuja etapa de vídeo não saiu no dia, ficou com prazo no dia seguinte e teve a data alterada no dia (histórico/auditoria). Reatribuir a outro editor conta como movimentação. Registrar em `MOVED` quem alterou e a que horas. O iClips não guarda a data anterior.
- Sinalizado sem movimentação: pedido de prioridade do dia, etapa aberta, nenhuma alteração depois do pedido. Se não houver, a seção diz isso.
- Bloqueado: aprovação interna parada, etapa anterior ao vídeo, sem responsável. Mostrar editor reservado e a etapa que trava.
- Motivo dos reprogramados: seletor com "Limite de pauta" como padrão (banco da página).

## As três checagens
Dias off de calendário (regra da Diana): **sábado, domingo e feriados são dias off**, sem nenhuma rotina, publicação ou e-mail. As tarefas agendadas já só disparam de segunda a sexta. Mesmo assim, antes de qualquer leitura, conferir a data de hoje no fuso de Manaus: se for sábado ou domingo, ou se a data (AAAA-MM-DD) estiver em `feriados.json`, criar `estado\AAAA-MM-DD\DIA_OFF.txt` com o motivo (fim de semana ou nome do feriado), encerrar com o aviso "dia off, nada executado" e não enviar e-mail. A lista `feriados.json` vale para Manaus e deve ser mantida pela Diana. Dia seguinte (`PROX`) = próximo dia útil, pulando fim de semana e feriados. Pedidos de prioridade lidos na abertura = tudo o que chegou desde o fechamento do último dia útil, inclusive no fim de semana ou feriado, com o dia e a hora reais de cada pedido (`ANT` = último dia útil anterior).

Antes de tudo: rodar `powershell -File D:\Vibecodas\Claude\pauta-diaria\iniciar_ponte.ps1`; abrir o iClips (https://app.iclips.com.br/vanguarda/DashTrafego/Lista/) e o Google Chat (https://chat.google.com) no navegador integrado. Se o iClips pedir login (a página vai para `/vanguarda/Login`), **parar na hora, não digitar senha nem usar credenciais salvas**, e fazer três coisas: (1) gravar o aviso em `estado\AAAA-MM-DD\ALERTA.txt` com a hora; (2) enviar uma notificação à Diana com a ferramenta PushNotification (status "proactive"), em uma linha e sem Markdown, por exemplo "iClips pediu login: entre no painel do navegador do Claude e rode a tarefa pauta-dia-HHMM de novo" (trocar HHMM pela checagem); (3) abrir o painel do navegador com `show_pane` (pane "preview") para ela ver a tela de login. Depois encerrar com um resumo curto dizendo que nada foi publicado e que o link fixo continua com a última versão. Na checagem das 19:00, o e-mail só sai com dados lidos hoje: se o iClips estiver no login, não enviar e-mail e avisar pelo mesmo caminho (notificação e ALERTA).

### Execução com atraso (computador desligado ou app fechado)
O agendador só dispara com o app aberto. Se estiver fechado na hora, a tarefa roda na próxima abertura, com os dados daquele momento. Por isso, em toda checagem:
1. Rodar `Get-Date` e comparar com o horário programado (09:00, 14:00 ou 19:00, de Manaus).
2. Escrever em `dia.py` o horário **real** de leitura em `LIDO` (nunca o horário programado). Se o atraso passar de 60 minutos, acrescentar " (checagem atrasada, programada para HH:00)" em `LIDO`; isso aparece na página, nos PDFs e no e-mail.
3. Checagens das 09:00 e das 14:00: se já for outro dia, ou se já passou do horário da checagem seguinte, não publicar nada para o dia antigo. Registrar o ocorrido em `estado\AAAA-MM-DD\ALERTA.txt` e encerrar com um aviso. A próxima checagem normal cobre o dia.
4. **Dia off.** Se o computador ficou desligado o dia todo, a Diana quer que o dia seja considerado "dia off": nenhuma rotina roda, não se publica nada e **não se envia e-mail**. Como reconhecer: a checagem das 19:00 está rodando em outro dia (depois da meia-noite ou na manhã seguinte) e não existe nenhum arquivo em `estado\<dia programado>\` (nem 09h, nem 14h). Então criar `estado\<dia programado>\DIA_OFF.txt` com a data e a hora atuais, encerrar com o aviso "dia off, nada executado" e não ler iClips, WhatsApp ou Google Chat para esse dia. Também não é dia off se o computador só ligou no fim do dia e as checagens atrasadas do próprio dia já geraram `estado\<dia>\`.
5. Checagem das 19:00 fora do dia off: é a que fecha o dia e sempre roda, mesmo atrasada, **no mesmo dia em que estava programada**. Se rodar no dia seguinte e já existir estado do dia programado (09h ou 14h), fechar o dia programado: usar relatório de atividades, fluxo e histórico do iClips pela data daquele dia, avisar no corpo do e-mail e no resumo que o fechamento saiu com atraso e que etapas e responsáveis refletem o momento da leitura, e usar `DIA`, `DIA_EXT` e `PROX` do dia fechado.
6. Se duas checagens rodarem em sequência na abertura do app, executar uma por vez, nunca em paralelo.

### 09:00, abertura
0. **Revisão do dia anterior (nova regra da Diana, 16/10/2026).** Os editores costumam trabalhar além do horário (depois das 19:00 e às vezes até a manhã seguinte), então o que o fechamento das 19:00 mostrou como parcial, reprogramado ou não concluído pode já ter sido resolvido. Antes de montar a pauta de hoje, fazer, para o último dia útil anterior (use `estado\<dia anterior>\19h\` como ponto de partida):
   1. Ler o relatório Atividades realizadas por colaborador desse dia **inteiro** e também as sessões de hoje de madrugada e manhã até agora, para Hudson, Guilherme, Vinicius e Diana. Sessões que começaram depois das 19:00 são "fora do horário" e devem aparecer assim no relatório (campo de horário com o aviso, por exemplo "20:10 às 21:45, fora do horário").
   2. Reler o fluxo e o histórico dos jobs que ficaram como parcial ou reprogramado. O que foi concluído passa a **executado**: sai de `MOVED`, `partial` vira `done`, e entra em `EXEC` ou `SUP` com o horário real. Ajustes e refações novos entram em `FLAGS` e `DET` (ler comentários e briefing). O que continua aberto segue como está.
   3. A Diana autorizou **sobrescrever tudo do dia anterior** (PDFs no Drive, Fechamento publicado, arquivos em `estado\<dia anterior>\19h\`); não precisa guardar versões antigas. O que não pode ser sobrescrito são os arquivos de trabalho de hoje (`dia.py`, `data.py`, `report_data.py` na raiz). Por isso, copiar `estado\<dia anterior>\19h\{dia,data,report_data}.py` para `estado\<dia anterior>\revisao\`, aplicar as correções ali, gerar com `PAUTA_DADOS=<essa pasta> PAUTA_SAIDA=<essa pasta>\saida python build_all.py` (nunca sobrescrever o `dia.py` de hoje). Salvar os PDFs 2 e 3 no Drive por cima dos do dia anterior com `PAUTA_SAIDA=<essa pasta>\saida python salvar_drive.py 2 3` e publicar o Fechamento atualizado (`<pasta>\saida\fechamento.out.html`) no link fixo. Não enviar e-mail por causa da revisão.
   4. Registrar no resumo final o que mudou (quantos jobs passaram de não concluído para concluído, por quem e em que horário).
1. Ler pedidos de prioridade do dia anterior (WhatsApp via MCP `whatsapp`, só leitura, grupo "VGRDA/ JOBS Accounts"; Google Chat nos dois espaços). Identificar quem pediu. Remetente do WhatsApp: telefone pelo mapa de LID e nome pela agenda sincronizada (tabelas whatsmeow_lid_map e whatsmeow_contacts em `whatsapp-bridge\store\whatsapp.db`, abrir somente leitura).
2. Ler no iClips os jobs de vídeo em aberto e o fluxo de cada um. Montar `data.py`, `dia.py` (DIA = hoje, ANT = dia anterior, TODAY = hoje, frase nova), reservas e pedidos.
3. Jobs com ajuste: ler comentários e briefing, preencher `FLAGS` e `DET`.
4. `python build_all.py --sem-pdf`, publicar a Pauta no link fixo, copiar os três arquivos para `estado\AAAA-MM-DD\09h\`.
5. Não enviar e-mail. O PDF "início do dia" precisa refletir 09:00: rodar `python build_all.py` e copiar `saida\1-inicio-do-dia.pdf` para `estado\AAAA-MM-DD\09h\`.

### 14:00, meio do dia
1. Reler o iClips (fluxo dos jobs da pauta, relatório de atividades do dia, histórico).
2. Atualizar `data.py` e `dia.py` (etapas, responsáveis, reservas, `LIDO`), manter a mesma frase do título do dia. Atualizar `report_data.py` com o que já foi executado.
3. Publicar a Pauta no mesmo link. Copiar o estado para `estado\AAAA-MM-DD\14h\`. Não enviar e-mail.

### 19:00, fechamento
1. Reler tudo (iClips completo, relatório de atividades realizadas de editores e Diana para o dia, histórico de cada job reprogramado, comentários e briefing dos jobs com ajuste).
2. Reescrever `report_data.py` (EXEC, SUP, MOVED, FLAGS, DET, RECORRENTES), `data.py` e `dia.py` (LIDO, DIA_EXT, PROX = próximo dia útil ou dia seguinte).
3. `python build_all.py` gera os 3 PDFs, o corpo do e-mail e o assunto em `saida\`.
4. Publicar o Fechamento e a Pauta nos links fixos.
5. Copiar o estado para `estado\AAAA-MM-DD\19h\` e os PDFs de `saida` para `estado\AAAA-MM-DD\19h\pdfs\`.
6. Salvar os PDFs no Google Drive: `python salvar_drive.py`. Estrutura `<pasta_local>\AAAA\MM - Mês\DD\`, onde `pasta_local` (em `drive.json`) é a pasta **RELATÓRIOS do Meu Drive da conta diana.savi@vanguardamartech.com.br** (link https://drive.google.com/drive/folders/11_HweEj_5lGI9BqI5acSKdH95-OlVCM9), vista no computador pelo Google Drive para computador. Nunca usar a conta dianasavi.vanguarda@gmail.com (unidade I:). Se `pasta_local` estiver vazio, o script sai com código 4 e nada é salvo; nesse caso avisar no e-mail e no resumo que os PDFs ficaram só em `estado\AAAA-MM-DD\19h\pdfs\`. Arquivos `AAAA-MM-DD - 1 Início do dia.pdf`, `... - 2 Fim do dia.pdf` e `... - 3 Relatório do dia.pdf`. A pasta RELATORIOS é compartilhada com a Luana pela Diana (somente leitura) e as subpastas herdam o acesso. Se existir `drive.json` com `pasta_raiz_url`, o e-mail também mostra o botão da pasta raiz.
7. Enviar o e-mail para luana.rocha@vanguardamartech.com.br, somente para ela:
   - Se existir `email_config.json`: `python enviar_email.py` (anexa os 3 PDFs e mantém os botões do Drive). Código 0 = enviado.
   - Senão, ou se o código for 2 ou 3: conector Gmail `send_message` com `htmlBody` = conteúdo de `saida\email.html`, `subject` = conteúdo de `saida\assunto.txt`, sem anexos. Os PDFs chegam pelo botão "Abrir os 3 PDFs do dia" (busca no Drive pela data) e pela estrutura de pastas.
   - Se `salvar_drive.py` falhar (Drive desconectado), enviar mesmo assim e avisar no corpo e no resumo que os PDFs ficaram só em `estado\AAAA-MM-DD\19h\pdfs\`.
8. Resumo final: o que foi lido, o que foi publicado, se o e-mail saiu e com quais anexos ou links, qualquer alerta.

## Limites e cuidados
- Somente leitura no iClips, WhatsApp e Google Chat. Nunca enviar mensagens de WhatsApp, nunca alterar jobs.
- Nunca incluir dados de canais pessoais da Diana com os editores (o grupo "Editores Vanguarda - Sem Filtro" está fora da lista de permissão e nunca entra).
- Linguagem de trabalho nos relatórios: tarefas, etapas, prazos. Sem comentários pessoais.
- Nunca digitar senhas, nunca ler `email_config.json` em voz alta nem colocá-lo em saídas.
- Reprogramado é inferido do histórico; o motivo "Limite de pauta" é padrão não verificado. Dizer isso quando relevante.
- Se faltar dado (ponte desligada, sessão expirada), publicar com o que há, registrar o alerta e dizer no e-mail e no resumo.
