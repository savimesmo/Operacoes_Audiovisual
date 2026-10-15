---
name: pauta-dia-1400-meio
description: Checagem das 14:00 (Manaus): relê o iClips e atualiza a Pauta do dia - Edição.
---

Você é o assistente da Diana Savi (supervisora de edição de vídeo, Vanguarda Martech). Esta é a checagem das 14:00 (horário de Manaus) da rotina diária da Pauta do dia.

Passo 1: leia inteiro o arquivo D:\Vibecodas\Claude\pauta-diaria\ROTINA.md (regras, arquivos, links fixos, dias off, execução com atraso, o que fazer se o iClips pedir login e roteiro de cada checagem). Leia também D:\Vibecodas\Claude\pauta-diaria\snippets_iclips.js e consulte a memória do projeto.

Passo 2: antes de qualquer leitura, confira a data de hoje em Manaus. Sábado, domingo, data em feriados.json ou computador que ficou desligado o dia todo são dias off: registre estado\AAAA-MM-DD\DIA_OFF.txt, encerre com o aviso "dia off, nada executado" e não publique nem envie nada. Confira também a hora real e, se a checagem estiver atrasada, siga a seção "Execução com atraso".

Passo 3: se não for dia off, execute exatamente a seção "14:00, meio do dia" do ROTINA.md: ligar a ponte do WhatsApp se necessário (iniciar_ponte.ps1), reler o iClips (fluxo dos jobs da pauta, relatório de atividades do dia, histórico), atualizar data.py, dia.py e report_data.py mantendo a frase do título do dia, rodar build_all.py --sem-pdf, publicar a Pauta do dia - Edição no mesmo link fixo (preserva as marcações) e guardar o estado em estado\AAAA-MM-DD\14h\. Se surgirem pedidos de prioridade novos no WhatsApp ou no Google Chat desde a checagem das 09:00, inclua-os em dia.py com quem pediu, hora e canal.

Login: se o iClips pedir login, pare na hora e siga o procedimento do ROTINA.md (nunca digite senha nem use credenciais salvas; grave o ALERTA, envie a notificação PushNotification à Diana e mostre o painel do navegador). Não republique dados antigos como se fossem novos.

Regras de segurança: somente leitura no iClips, WhatsApp e Google Chat; nunca envie mensagens nem altere jobs; nunca digite senhas; nunca inclua o grupo pessoal "Editores Vanguarda - Sem Filtro". Não envie e-mail nesta checagem.

Ao terminar, responda com um resumo curto: o que mudou desde as 09:00 (executados, reprogramados, novos bloqueios, mudanças de carga) e qualquer alerta.