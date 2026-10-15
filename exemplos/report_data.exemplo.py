# Exemplo (dados fictícios) de report_data.py.
# EXEC / SUP: [idJob, cliente, título, quem, horário, "done" ou "partial", etapa agora]
EXEC = [[100001, "Cliente Exemplo", "Edição Reels · Título do job", "Hudson Soares", "09:15 às 12:31", "done", "Aprovação interna · Nome da pessoa"]]
SUP = []
RECORRENTES = "Os VTs recorrentes de Santo Remédio (FDS Fraldas) aparecem só neste fechamento e ficam fora da pauta de prioridades."
MOVED = {100002: "Reprogramado pelo Tráfego às 17:12"}      # id: evidência
FLAGS = {"100001": [1, 0, 1]}                                  # id: [ajustes, refações, etapas de edição]
DET = {"100001": [{"quem": "Nome da pessoa", "tipo": "Erro de edição", "c": "edi", "q": "hoje", "o": "o que foi pedido", "b": "sinalizado: trecho do briefing"}]}
