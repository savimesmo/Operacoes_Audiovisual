"""Relatório semanal de ajustes e refações: origem, gravidade, solicitante e reincidência.

Lê estado/<dia>/19h/report_data.py (e data.py) dos dias úteis da semana, soma os pedidos
de ajuste (DET) e escreve saida/relatorio-semanal.md e saida/relatorio-semanal.html.

Uso: python semanal.py [AAAA-MM-DD]   (qualquer dia da semana; padrão: a semana do último estado)
"""
import datetime, html, os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ESTADO = os.path.join(HERE, "estado")
SAIDA = os.environ.get("PAUTA_SAIDA", os.path.join(HERE, "saida"))
LINK = "https://app.iclips.com.br/vanguarda/JobPeca/Atividade/"
ORIGEM = {"edi": "Erro de edição", "brf": "Briefing sem as informações", "cli": "Alteração do cliente", "art": "Outros", "out": "Outros"}
GRAV = {"alta": "Alta", "media": "Média", "baixa": "Baixa", "sem": "Sem gravidade"}


def dias_da_semana(ref):
    seg = ref - datetime.timedelta(days=ref.weekday())
    return [seg + datetime.timedelta(days=i) for i in range(5)]


def ultimo_estado():
    ds = sorted(d for d in os.listdir(ESTADO) if len(d) == 10 and os.path.isdir(os.path.join(ESTADO, d, "19h")))
    return datetime.date.fromisoformat(ds[-1]) if ds else datetime.date.today()


ref = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else ultimo_estado()
semana = dias_da_semana(ref)

det, flags, titulos, dias_lidos = {}, {}, {}, []
for d in semana:
    pasta = os.path.join(ESTADO, d.isoformat(), "19h")
    rp = os.path.join(pasta, "report_data.py")
    if not os.path.exists(rp):
        continue
    dias_lidos.append(d)
    rd = runpy.run_path(rp)
    for k, v in rd.get("DET", {}).items():
        det[k] = v  # o último dia lido vale
    for k, v in rd.get("FLAGS", {}).items():
        flags[k] = v
    for r in list(rd.get("EXEC", [])) + list(rd.get("SUP", [])):
        titulos[str(r[0])] = (r[1], r[2])
    dp = os.path.join(pasta, "data.py")
    if os.path.exists(dp):
        for r in runpy.run_path(dp).get("D", []):
            titulos[str(r[1])] = (r[2], r[3])


def tit(i):
    c, t = titulos.get(str(i), ("", ""))
    return (c + " · " + t.replace(" | ", " ")).strip(" ·") or f"Job {i}"


pedidos = []
for jid, itens in det.items():
    for it in itens:
        pedidos.append(dict(id=jid, quem=it.get("quem", ""), c=it.get("c") if it.get("c") in ORIGEM else "out",
                            g=it.get("g") if it.get("g") in GRAV else "sem", q=it.get("q", ""), o=it.get("o", "")))


def conta(chave):
    r = {}
    for p in pedidos:
        r[chave(p)] = r.get(chave(p), 0) + 1
    return r


por_origem = conta(lambda p: ORIGEM[p["c"]])
por_grav = conta(lambda p: GRAV[p["g"]])
por_quem = {}
for p in pedidos:
    q = por_quem.setdefault(p["quem"], {"n": 0, "brf": 0, "cli": 0, "edi": 0, "out": 0, "jobs": {}})
    q["n"] += 1
    q[p["c"] if p["c"] in ("brf", "cli", "edi") else "out"] += 1
    q["jobs"].setdefault(p["id"], []).append(p)
reinc = sorted(((jid, sum(flags.get(jid, [0, 0, 1])[:2]) or len(its), its) for jid, its in det.items()
                if (sum(flags.get(jid, [0, 0, 1])[:2]) or len(its)) >= 3), key=lambda x: -x[1])

titulo = f"Relatório semanal de ajustes e refações: {semana[0]:%d/%m} a {semana[-1]:%d/%m}"
md = [f"# {titulo}", "",
      f"Dias lidos: {', '.join(f'{d:%d/%m}' for d in dias_lidos) or 'nenhum'}. {len(pedidos)} pedidos de ajuste em {len(det)} jobs.", "",
      "## Por origem", ""] + [f"- {k}: {v}" for k, v in sorted(por_origem.items(), key=lambda x: -x[1])] + \
     ["", "## Por gravidade", ""] + [f"- {k}: {v}" for k, v in sorted(por_grav.items(), key=lambda x: -x[1])] + \
     ["", "## Por solicitante", ""]
for q, v in sorted(por_quem.items(), key=lambda x: -x[1]["n"]):
    md.append(f"### {q or 'não identificado'} ({v['n']} pedidos: {v['brf']} briefing, {v['cli']} cliente, {v['edi']} edição, {v['out']} outros)")
    md.append("")
    for jid, its in v["jobs"].items():
        md.append(f"- [{jid}]({LINK}{jid}) {tit(jid)}: " + "; ".join(f"{p['q']} {p['o'][:110]} [{GRAV[p['g']].lower()}]" for p in its))
    md.append("")
md += ["## Reincidência (3 ou mais pedidos no mesmo job)", ""]
md += [f"- [{jid}]({LINK}{jid}) {tit(jid)}: {n} pedidos" for jid, n, _ in reinc] or ["- Nenhum job nesta semana."]
md += ["", "Contagem: só pedidos de alteração da peça e comentários de ajuste; reagendamentos de data não contam. Gravidade e origem seguem a régua do ROTINA.md."]

os.makedirs(SAIDA, exist_ok=True)
with open(os.path.join(SAIDA, "relatorio-semanal.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")


def tabela(d):
    return "<table>" + "".join(f"<tr><td>{html.escape(k)}</td><td>{v}</td></tr>" for k, v in sorted(d.items(), key=lambda x: -x[1])) + "</table>"


h = [f"<!doctype html><html lang='pt-BR'><meta charset='utf-8'><title>{html.escape(titulo)}</title>",
     "<style>body{font:14px Arial,sans-serif;max-width:900px;margin:24px auto;color:#111}td{padding:4px 12px;border-bottom:1px solid #ddd}h2{margin-top:24px}</style>",
     f"<h1>{html.escape(titulo)}</h1><p>{len(pedidos)} pedidos em {len(det)} jobs.</p>",
     "<h2>Por origem</h2>" + tabela(por_origem), "<h2>Por gravidade</h2>" + tabela(por_grav), "<h2>Por solicitante</h2>"]
for q, v in sorted(por_quem.items(), key=lambda x: -x[1]["n"]):
    h.append(f"<h3>{html.escape(q or 'não identificado')} ({v['n']})</h3><ul>")
    for jid, its in v["jobs"].items():
        h.append(f"<li><a href='{LINK}{jid}'>{jid}</a> {html.escape(tit(jid))}: " + html.escape("; ".join(f"{p['q']} {p['o'][:110]} [{GRAV[p['g']].lower()}]" for p in its)) + "</li>")
    h.append("</ul>")
h.append("<h2>Reincidência</h2><ul>" + ("".join(f"<li><a href='{LINK}{jid}'>{jid}</a> {html.escape(tit(jid))}: {n} pedidos</li>" for jid, n, _ in reinc) or "<li>Nenhum job nesta semana.</li>") + "</ul>")
with open(os.path.join(SAIDA, "relatorio-semanal.html"), "w", encoding="utf-8") as f:
    f.write("\n".join(h))
print("ok", len(pedidos), "pedidos,", len(det), "jobs, dias:", [d.isoformat() for d in dias_lidos])
