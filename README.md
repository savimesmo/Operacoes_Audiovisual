# Pauta do dia - Edição e Fechamento

Rotina automática da supervisão de edição de vídeo da Vanguarda Martech. Três checagens por dia útil (09:00, 14:00 e 19:00, horário de Manaus) leem o iClips, o WhatsApp e o Google Chat, publicam a página **Pauta do dia - Edição**, o **Fechamento** do dia, geram 3 PDFs, guardam no Google Drive e enviam um e-mail para a Luana.

Este repositório é privado e guarda o código, os modelos, o roteiro e as tarefas agendadas. **Dados reais, segredos e fontes licenciadas ficam fora** (veja "O que não está aqui").

## Como funciona
1. Três tarefas agendadas do Claude (ver `tarefas-agendadas/`) abrem o iClips e o Google Chat no navegador integrado, ligam a ponte do WhatsApp e seguem o roteiro de [`ROTINA.md`](ROTINA.md).
2. O agente reescreve `dia.py`, `data.py` e `report_data.py` com o que leu (modelos em `exemplos/`).
3. `build_all.py` gera as duas páginas, os 3 PDFs (Edge ou Chrome sem janela), o corpo do e-mail e o assunto em `saida/`.
4. `salvar_drive.py` copia os PDFs para a pasta RELATÓRIOS do Drive (ano / mês / dia).
5. O e-mail sai pelo conector do Gmail, com botões para os PDFs. Com `email_config.json` (senha de app), `enviar_email.py` anexa os PDFs.

Dias off: sábado, domingo, feriados (`feriados.json`) e computador desligado o dia todo. Detalhes em `ROTINA.md`.

## Estrutura
| Caminho | Conteúdo |
| --- | --- |
| `ROTINA.md` | Regras completas, roteiro de cada checagem, dias off e execução com atraso |
| `build_all.py` | Monta páginas, PDFs, e-mail e assunto a partir dos dados do dia |
| `template.html`, `fechamento.html` | Modelos da Pauta do dia e do Fechamento (artefatos do Claude) |
| `snippets_iclips.js` | Trechos de leitura do iClips para o navegador integrado (somente leitura) |
| `salvar_drive.py`, `enviar_email.py`, `iniciar_ponte.ps1` | Salvar no Drive, enviar com anexos por SMTP, ligar a ponte do WhatsApp |
| `feriados.json` | Feriados de Manaus (dias off) |
| `ponte-whatsapp/` | Código da ponte do WhatsApp somente leitura (fork do lharries/whatsapp-mcp) e do servidor MCP |
| `tarefas-agendadas/` | Texto das 3 tarefas agendadas do Claude |
| `exemplos/` | Modelos com dados fictícios: `dia`, `data`, `report_data`, `drive`, `email_config` |

## Primeiro uso em um computador novo
1. Python 3 e Microsoft Edge ou Chrome. Opcional: Node (checagem de sintaxe) e Go 1.27 (compilar a ponte).
2. Copiar `exemplos/*.exemplo.py` para a raiz sem o `.exemplo` e `exemplos/drive.exemplo.json` para `drive.json`, ajustando `pasta_local`.
3. Colocar as fontes Monument Extended (`MonumentExtended-Ultrabold.otf` e `-Regular.otf`) em `fontes/`.
4. `python build_all.py` gera tudo em `saida/`.
5. Ponte do WhatsApp: compilar `ponte-whatsapp/whatsapp-bridge`, criar `allowed_chats.txt` (um JID por linha) e parear por QR. O servidor MCP em `ponte-whatsapp/whatsapp-mcp-server` só lê o banco.
6. Criar as tarefas agendadas com o conteúdo de `tarefas-agendadas/` (cron `46 8 * * 1-5`, `48 13 * * 1-5` e `56 18 * * 1-5`, que compensam o atraso fixo do agendador).
7. Para anexar PDFs ao e-mail: criar `email_config.json` a partir de `exemplos/email_config.exemplo.json` com uma senha de app do Google, criada pela própria usuária.

## O que não está aqui
- `dia.py`, `data.py`, `report_data.py`, `estado/` e `saida/`: dados reais de jobs, clientes e pessoas.
- `email_config.json` e qualquer senha ou token.
- `drive.json`, banco do WhatsApp, sessão, `allowed_chats.txt`, `names.json` e executáveis.
- `fontes/`: fontes licenciadas.

## Regras e limites
O arquivo `ROTINA.md` é a referência. Em resumo: somente leitura nas fontes; nunca enviar mensagens nem alterar jobs; nunca digitar senhas; o grupo pessoal da Diana com os editores nunca entra; "reprogramado" é inferido do histórico; a classificação dos ajustes é leitura de texto e deve ser conferida.

Documento vivo do processo: https://claude.ai/artifact/BRCS18JMFugf7ArdUbhEXw
