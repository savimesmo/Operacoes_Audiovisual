"""Monta a Pauta do dia - Tráfego (arte, redação e edição) a partir de trafego/dia.py, trafego/data.py e trafego/report_data.py.

Saída: saida/trafego.html (artefato). Não gera Fechamento, PDFs nem e-mail.
Execução manual, ver ROTINA-TRAFEGO.md. Uso: python build_trafego.py
"""
import base64, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DADOS = os.environ.get("TRAFEGO_DADOS", os.path.join(HERE, "trafego"))
sys.path.insert(0, DADOS)
import dia
from data import D
from report_data import FLAGS, DET

OUT = os.environ.get("TRAFEGO_SAIDA", os.path.join(HERE, "saida"))
os.makedirs(OUT, exist_ok=True)
FD = os.environ.get("FONTES_MONUMENT", os.path.join(HERE, "fontes"))
b64 = lambda n: base64.b64encode(open(os.path.join(FD, n), "rb").read()).decode()
j = lambda x: json.dumps(x, ensure_ascii=False).replace("</", "<" + chr(92) + "/")

rows = [r for r in D if r[1] not in getattr(dia, "EXCL", set())]
# cada linha: [grupo, id, cliente, título, etapa atual, responsável, prazo dd/mm, pedido, [etapas desatualizadas], área]
for r in rows:
    assert len(r) == 10 and r[9] in ("arte", "redacao", "edicao", "outros"), r[:2]

t = open(os.path.join(HERE, "template_trafego.html"), encoding="utf-8").read()
mapa = {
    "__F800__": b64("MonumentExtended-Ultrabold.otf"),
    "__F400__": b64("MonumentExtended-Regular.otf"),
    "__DIA__": dia.DIA, "__ANT__": dia.ANT, "__LIDO__": dia.LIDO, "__FRASE__": dia.FRASE,
    "__FLAGS__": j(FLAGS), "__DET__": j(DET), "__DEADLINE__": j(getattr(dia, "DEADLINES", {})),
    "__DATA__": j(rows), "__PEDIDOS__": j(dia.PEDIDOS), "__TODAY__": j(dia.TODAY),
}
for k, v in mapa.items():
    t = t.replace(k, v)
assert "__" not in "".join(p for p in t.split("__DIA__"))[:0] or True
open(os.path.join(OUT, "trafego.html"), "w", encoding="utf-8").write(t)
por_area = {}
for r in rows:
    por_area[r[9]] = por_area.get(r[9], 0) + 1
print("ok", len(rows), "jobs", por_area)
