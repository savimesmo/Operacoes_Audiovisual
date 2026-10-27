# Pauta do dia - Tráfego (execução manual)

Artefato: https://claude.ai/artifact/PtkWPSjnq8PUrmY1e9oVWv (link fixo; as marcações compartilhadas ficam no banco da própria página).
Escopo: jobs de **arte, redação e edição/animação** com prazo até amanhã (ou vencido nos últimos 7 dias), todo job com **prioridade solicitada**, e os **sem Deadline**. Sem capacidade por pessoa, sem Fechamento, PDFs ou e-mail. Sem tarefa agendada: roda quando a Diana pedir.

## Arquivos
- `template_trafego.html` (modelo), `build_trafego.py` (gera `saida\trafego.html`).
- `trafego\data.py`, `trafego\dia.py`, `trafego\report_data.py`: dados do dia (não vão para o GitHub). `trafego\montar.py` gera os três a partir de `rows1.json`, `rows2.json` e `dl.txt`.
- Linha de `D`: `[grupo, id, cliente, título, etapa atual, responsável, prazo dd/mm, pedido ("WA hh:mm"), [[etapa, data, resp]], área]`; área = `arte` | `redacao` | `edicao` | `outros`.

## Passos
1. `iniciar_ponte.ps1` (WhatsApp). iClips logado no navegador integrado; se pedir login, parar e avisar.
2. **Lista** (`DashTrafego/BuscaAvancada` via `__gq`, sem filtro de responsável, situações 0, 1, 2 e 3, início 7 dias atrás, fim = amanhã). Descartar tarefas (id menor que 100000) e os recorrentes de Santo Remédio (FDS Fraldas e Fitness).
3. **Fluxo e Deadline** de cada job (`CarregaWorflowJobPeca` e `ModalDetalhe`, campo `ProgramacaoDate`; em lotes de 25 em paralelo, até 45 s por chamada). Etapa atual = primeira etapa não concluída.
4. **Quem entra e o grupo.** Entra se houver etapa de produção ou ajuste aberta (arte, criação, design, direção de criação, cartelas, texto, redação, edição, animação, storyboard, gravação, ajuste, refação). Fica de fora o job cuja etapa atual é aprovação e não resta produção depois (etapa final sem fechamento = concluído) e os de planejamento, mídia ou publicação sem produção. Grupos: 1 produção com responsável; 2 Tráfego (sem responsável) em etapa de produção; 3 aprovação com produção depois; 4 ajuste, refação ou outra etapa com responsável; 5 Tráfego em outra etapa.
5. **Área** pela etapa atual (arte: ARTE, CRIAÇÃO, DESIGN, DIREÇÃO, CARTELAS, DIAGRAMAÇÃO; redação: TEXTO, REDAÇÃO; edição: EDIÇÃO, ANIMAÇÃO, STORYBOARD, GRAVAÇÃO). Etapa de aprovação, ajuste ou briefing usa a área da próxima etapa de produção.
6. **Pedidos**: `messages.db`, todos os grupos, mensagens com "prioridade" e links do iClips desde o último dia útil. Cada pedido vira uma chave "WA hh:mm" em `PEDIDOS` (nome, telefone, dia, grupo). Job citado entra mesmo com prazo depois de amanhã, se tiver produção aberta.
7. **Deadline**: `DEADLINES = {id: {"d": "dd/mm/aaaa", "s": "account e analista (responsáveis das etapas de aprovação)"}}`. Vazia = tag SEM DEADLINE; anterior a hoje com job aberto = DEADLINE VENCIDA; devolver ao solicitante.
8. **Ajustes e refações**: jobs com etapa de ajuste ou refação: contar só pedidos reais (`Auditoria/Listar` + `RetornaAlteracao`, "Solicitou alteração da peça"), ler comentários e classificar origem e gravidade pela régua de `ROTINA.md`. Em 26/10 a origem foi classificada só pelo pedido, sem cruzar com o briefing; o carimbo da página diz isso.
9. `python trafego\montar.py` (ou escrever os três arquivos) e `python build_trafego.py`; `node --check` no script; publicar `saida\trafego.html` no `url` acima.

## Regras herdadas de ROTINA.md
Título com frase nova por dia; pedido com quem, dia, hora e grupo; etapas atuais relidas; grupo específico do job (ler antes de marcar parado); Deadline e devolução ao solicitante; ajustes com origem e gravidade; autoria só com confirmação da Diana.

## Limites da primeira leitura (26/10)
Google Chat e grupos específicos de job não foram lidos; etapas desatualizadas ("old") não preenchidas; briefing não cruzado; só jobs com etapa de produção ou ajuste entram, então planejamento, mídia e publicação ficam fora.

## Google Chat (leitura dos pedidos de prioridade)
- Abrir https://chat.google.com no navegador integrado (sessão da Diana), localizar os espaços "Tráfego | Mídia Paga", "Tráfego | Social Media" e "Tráfego - Vanguarda" com `find`, clicar e ler `document.body.innerText`.
- Só espaços; mensagens diretas não são lidas. Pedido novo de prioridade entra como `Chat HH:MM` em PEDIDOS, como o WhatsApp.
- Link fixo do artefato: https://claude.ai/artifact/PtkWPSjnq8PUrmY1e9oVWv (publicar sempre nele).
