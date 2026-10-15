# Exemplo (dados fictícios) de dia.py. Copie para a raiz como dia.py e reescreva todo dia.
DIA = "15/10"; DIA_EXT = "quinta, 15/10"; ANT = "14/10"; PROX = "16/10"
TODAY = {"d": 15, "m": 10}
FRASE = "Frase curta de jargão publicitário, nova a cada dia."
LIDO = "15/10 às 09:00"
PEDIDOS = {
  "WA 16:50": {"n": "Fulano de Tal", "t": "5592999990000", "c": "WhatsApp, grupo VGRDA/ JOBS Accounts"},
  "Chat 15:44": {"n": "Ciclana da Silva", "c": "Google Chat, espaço Tráfego | Social Media"},
}
RESERVA = {  # id do job: edição/animação já atribuída a um editor, travada por etapa anterior
  100001: {"p": "Hudson Soares", "e": "Animação", "b": "Arte · Nome da pessoa"},
}
EXCL = set()  # ids de jobs só de arte a deixar fora
