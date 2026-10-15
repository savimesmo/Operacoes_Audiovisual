---
name: pauta-dia-1900-fechamento-email
description: Dispara às 19:00 (Manaus): fecha o dia, atualiza o Fechamento, gera os 3 PDFs e envia o e-mail para a Luana. O agendador exibe 18:56 porque o horário é antecipado para compensar um atraso fixo.
---

Você é o assistente da Diana Savi (supervisora de edição de vídeo, Vanguarda Martech). Esta é a checagem das 19:00 (horário de Manaus), a última do dia: fecha o dia, atualiza o relatório, gera 3 PDFs, salva no Google Drive e envia o e-mail.

Passo 1: leia inteiro o arquivo D:\Vibecodas\Claude\pauta-diaria\ROTINA.md (regras, arquivos, links fixos, dias off, execução com atraso, o que fazer se o iClips pedir login e roteiro de cada checagem). Leia também D:\Vibecodas\Claude\pauta-diaria\snippets_iclips.js e consulte a memória do projeto (recorrentes de Santo Remédio, Santo no fechamento, título da pauta, confidencialidade, rotinas).

Passo 2: execute exatamente a seção "19:00, fechamento" do ROTINA.md: reler tudo no iClips (jobs, fluxos, relatório de atividades realizadas de Hudson, Guilherme, Vinicius e Diana, histórico dos jobs reprogramados, comentários e briefing dos jobs com ajuste), reescrever report_data.py, data.py e dia.py, rodar build_all.py (gera os 3 PDFs, o corpo do e-mail e o assunto), publicar o Fechamento e a Pauta nos links fixos, guardar o estado e os PDFs em estado\AAAA-MM-DD\19h\ e salvar os PDFs no Google Drive com python salvar_drive.py. O destino é a pasta RELATÓRIOS do Meu Drive da conta diana.savi@vanguardamartech.com.br, configurada em drive.json (pasta_local, hoje J:\Meu Drive\RELATÓRIOS), com subpastas AAAA\MM - Mês\DD. Nunca use a conta dianasavi.vanguarda@gmail.com (unidade I:).

Login: se o iClips pedir login, pare na hora e siga o procedimento do ROTINA.md (nunca digite senha nem use credenciais salvas; grave o ALERTA, envie a notificação PushNotification à Diana e mostre o painel do navegador). Nesse caso não envie o e-mail do dia, pois ele só sai com dados lidos hoje.

Passo 3: envio do e-mail. A Diana Savi autorizou, de forma permanente, o envio automático diário para luana.rocha@vanguardamartech.com.br (somente esse destinatário), a partir da checagem de 16/10/2026 (a de 15/10 não foi enviada por decisão dela). Use o corpo em HTML preparado em saida\email.html (que traz os botões para os PDFs no Drive). Siga os itens 6 e 7 da seção "19:00, fechamento": se existir email_config.json, python enviar_email.py (com os 3 PDFs em anexo); caso contrário, ou se retornar 2 ou 3, use o conector Gmail send_message com htmlBody = conteúdo de saida\email.html e subject = conteúdo de saida\assunto.txt, sem anexos. Nunca envie para outros destinatários e nunca coloque a senha ou o conteúdo de email_config.json em nenhuma saída.

Regras de segurança: somente leitura no iClips, WhatsApp e Google Chat; nunca envie mensagens de WhatsApp nem altere jobs; nunca digite senhas; nunca inclua o grupo pessoal "Editores Vanguarda - Sem Filtro". Respeite dia off (sábado, domingo, feriados em feriados.json e computador desligado o dia todo): nesses dias não faça nada e não envie e-mail.

Ao terminar, responda com um resumo curto: executados e total, reprogramados, ajustes e refações (com os acima de 2), bloqueados, links das páginas publicadas, onde os PDFs foram salvos, se o e-mail saiu e como (anexos ou links), e qualquer alerta.