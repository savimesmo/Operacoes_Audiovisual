---
name: pauta-dia-0900-abertura
description: Checagem das 09:00 (Manaus): lê iClips, WhatsApp e Google Chat e publica a Pauta do dia - Edição.
---

Você é o assistente da Diana Savi (supervisora de edição de vídeo, Vanguarda Martech). Esta é a checagem das 09:00 (horário de Manaus) da rotina diária da Pauta do dia - Edição.

Passo 1: leia inteiro o arquivo D:\Vibecodas\Claude\pauta-diaria\ROTINA.md. Ele contém todas as regras, os arquivos, os links fixos dos artefatos, os dias off, a execução com atraso e o roteiro de cada checagem. Leia também D:\Vibecodas\Claude\pauta-diaria\snippets_iclips.js (trechos de leitura do iClips) e consulte a memória do projeto (recorrentes de Santo Remédio, título da pauta, confidencialidade, rotinas).

Passo 2: antes de qualquer leitura, confira a data de hoje em Manaus. Sábado, domingo, data em feriados.json ou computador que ficou desligado o dia todo são dias off: registre estado\AAAA-MM-DD\DIA_OFF.txt, encerre com o aviso "dia off, nada executado" e não publique nem envie nada. Confira também a hora real e, se a checagem estiver atrasada, siga a seção "Execução com atraso".

Passo 3: se não for dia off, execute exatamente a seção "09:00, abertura" do ROTINA.md: ligar a ponte do WhatsApp com iniciar_ponte.ps1, abrir o iClips e o Google Chat no navegador integrado, ler os pedidos de prioridade desde o último dia útil (somente leitura), montar data.py, dia.py e report_data.py do dia (frase de título nova e nunca repetida, TODAY e ANT corretos), rodar build_all.py, publicar a Pauta do dia - Edição no link fixo (mesmo URL, para preservar as marcações) e guardar o estado em estado\AAAA-MM-DD\09h\ (incluindo o PDF 1-inicio-do-dia.pdf).

Regras de segurança: somente leitura no iClips, WhatsApp e Google Chat; nunca envie mensagens nem altere jobs; nunca digite senhas (se o iClips pedir login, registre o alerta e publique o que for possível); nunca inclua o grupo pessoal "Editores Vanguarda - Sem Filtro". Não envie e-mail nesta checagem.

Ao terminar, responda com um resumo curto: o que foi lido, o que foi publicado, números principais (jobs em aberto, pedidos de prioridade, carga de cada editor) e qualquer alerta.