"""Monta tudo do dia a partir de dia.py, data.py e report_data.py.

Saídas em ./saida/:
  prioridades.html       Pauta do dia - Edição (artefato)
  fechamento.out.html    Fechamento (artefato)
  pdf_inicio.html        PDF do início do dia (resumo objetivo)
  pdf_fim.html           PDF do fim do dia
  email.html             Corpo do e-mail
  e os 3 PDFs: 1-inicio-do-dia.pdf, 2-fim-do-dia.pdf, 3-relatorio-do-dia.pdf
"""
import base64, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# PAUTA_DADOS: pasta com dia.py, data.py e report_data.py a usar (padrão: esta pasta).
# PAUTA_SAIDA: pasta de saída (padrão: ./saida). Servem para refazer o relatório de um dia anterior sem tocar nos arquivos do dia.
DADOS = os.environ.get("PAUTA_DADOS", HERE)
sys.path.insert(0, DADOS)
import dia
from data import D
from report_data import EXEC, SUP, RECORRENTES, MOVED, FLAGS, DET

OUT = os.environ.get("PAUTA_SAIDA", os.path.join(HERE, "saida"))
os.makedirs(OUT, exist_ok=True)
FD = r"D:\Temp\claude\D--Vibecodas-Claude\d7bc8586-2a3a-483a-a1fb-14d6f15fbfb9\scratchpad\artifact-files\e164898b-05e7-4d78-bd2f-f6628b1c9343\project\fonts"
FD = os.environ.get("FONTES_MONUMENT", os.path.join(HERE, "fontes"))
b64 = lambda n: base64.b64encode(open(os.path.join(FD, n), "rb").read()).decode()
j = lambda x: json.dumps(x, ensure_ascii=False).replace("</", "<\\/")
esc = lambda s: html.escape(str(s))

rows = [r for r in D if r[1] not in dia.EXCL]
PED = {r[7]: 1 for r in rows if r[7]}
RES = {k: f"{v['e']} reservada para {v['p']}, travada pela etapa anterior ({v['b']})." for k, v in dia.RESERVA.items()}


def sub(t, mapa):
    for k, v in mapa.items():
        t = t.replace(k, v)
    return t


COMUM = {
    "__F800__": b64("MonumentExtended-Ultrabold.otf"),
    "__DIA__": dia.DIA, "__DIA_EXT__": dia.DIA_EXT, "__ANT__": dia.ANT, "__PROX__": dia.PROX,
    "__LIDO__": dia.LIDO, "__FRASE__": dia.FRASE,
}

# 1) Pauta do dia
t = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
t = sub(t, {
    "__F400__": b64("MonumentExtended-Regular.otf"),
    "__FLAGS__": j(FLAGS), "__DET__": j(DET), "__DEADLINE__": j(getattr(dia, "DEADLINES", {})), "__DATA__": j(rows),
    "__RESERVA__": j(dia.RESERVA), "__PEDIDOS__": j(dia.PEDIDOS), "__TODAY__": j(dia.TODAY),
})
t = sub(t, COMUM)
open(os.path.join(OUT, "prioridades.html"), "w", encoding="utf-8").write(t)

# 2) Fechamento
f = open(os.path.join(HERE, "fechamento.html"), encoding="utf-8").read()
f = sub(f, {
    "__EXEC__": j(EXEC), "__SUP__": j(SUP), "__REC__": j(RECORRENTES), "__MOVED__": j(MOVED),
    "__ROWS__": j(rows), "__RES__": j(RES), "__PEDIDO__": j(PED), "__FLAGS__": j(FLAGS), "__DET__": j(DET),
})
f = sub(f, COMUM)
open(os.path.join(OUT, "fechamento.out.html"), "w", encoding="utf-8").write(f)

# ---------- números comuns aos PDFs e ao e-mail ----------
TEAM = [("Hudson Soares", "Hudson"), ("Vinicius Alves", "Vinicius"), ("Guilherme Benevides", "Guilherme Benevides")]
NOTA = {"Vinicius": "Pega os VTs semanais esporádicos"}
CAP_MIN, CAP_MAX = 6, 8


def dn(p):
    d, m = p.split("/")[:2]
    return int(m) * 31 + int(d)


def carga(ref=None):
    """Capacidade do DIA: só conta job com prazo até o dia de referência. O que é de dias seguintes aparece à parte (later)."""
    lim = dn(ref or dia.DIA)
    res = []
    for nome, match in TEAM:
        meus = [r for r in rows if r[0] == 1 and r[5].startswith(match)]
        prod = sum(1 for r in meus if r[6] and dn(r[6]) <= lim)
        rsv_all = [v for v in dia.RESERVA.values() if v["p"] == nome]
        rsv = sum(1 for v in rsv_all if not v.get("d") or dn(v["d"]) <= lim)
        later = (len(meus) - prod) + (len(rsv_all) - rsv)
        tot = prod + rsv
        st = "over" if tot > CAP_MAX else ("ok" if tot >= CAP_MIN else "low")
        res.append(dict(nome=nome, curto=nome.split(" ")[0], prod=prod, rsv=rsv, later=later, tot=tot, st=st, nota=NOTA.get(nome.split(" ")[0], "")))
    dm = [r for r in rows if r[0] == 1 and r[5].startswith("Diana")]
    dprod = sum(1 for r in dm if r[6] and dn(r[6]) <= lim)
    drsv = sum(1 for v in dia.RESERVA.values() if v["p"] == "Diana" and (not v.get("d") or dn(v["d"]) <= lim))
    return res, dprod, drsv


def prazo(p):
    if not p:
        return "sem prazo", ""
    d, m = (int(x) for x in p.split("/"))
    k = (m - dia.TODAY["m"]) * 31 + (d - dia.TODAY["d"])
    if k < 0:
        return f"vencido {p}", "late"
    if k == 0:
        return "vence hoje", "hoje"
    if k == 1:
        return f"amanhã {p}", ""
    return f"prazo {p}", ""


def nice(s):
    s = (s or "").lower()
    return s[:1].upper() + s[1:]


def pedido(r):
    partes = []
    for k in r[7].split("+"):
        p = dia.PEDIDOS.get(k)
        if not p:
            continue
        quem = p.get("n") or ("+" + p.get("t", ""))
        partes.append(f"{quem}, {p.get('d') or dia.ANT} às {k.split(' ')[1]}")
    return "; ".join(partes)


def ajustes_do(ids):
    """Ajustes e refações (jobs em ids) com quem pediu, tipo e briefing."""
    out = []
    for i in ids:
        f = FLAGS.get(str(i), [0, 0, 1])
        n = f[0] + f[1]
        if n or f[2] > 1:
            out.append((i, f, DET.get(str(i), [])))
    return out


CSS_BASE = """
@font-face{font-family:"Monument Extended";font-weight:800;src:url(data:font/otf;base64,__F800__) format("opentype")}
@page{size:A4;margin:11mm}
:root{--bg:#0a0a0a;--surface:#131313;--surface-2:#1b1b1b;--line:#2a2a2a;--line-2:#3a3a3a;--ink:#f5f5f5;--ink-2:#c4c4c4;--mute:#8d8d8d;--red:#e11121;--red-soft:#3a0d11;--ok:#2fcf7f;
--display:"Monument Extended","Archivo",system-ui,sans-serif;--body:"Archivo",system-ui,"Segoe UI",sans-serif}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{background:var(--bg);color:var(--ink);margin:0;font:400 10.5px/1.45 var(--body)}
.pg{padding:0}
.kicker{font:600 8.5px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
h1{margin:6px 0 4px;font:800 24px/1.08 var(--display)}
h1 span{color:var(--red)}
.stamp{color:var(--mute);font-size:9.5px}
h2{margin:16px 0 7px;font:800 11.5px/1.2 var(--display);padding-bottom:6px;border-bottom:1px solid var(--line-2)}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 12px;break-inside:avoid}
.tile b{display:block;font:800 22px/1 var(--display)}
.tile span{display:block;margin-top:4px;color:var(--ink-2);font-size:9.5px}
.tile.alert{border-color:var(--red);background:var(--red-soft)}
.cargas{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.lc{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 12px;break-inside:avoid}
.lc.over{border-color:var(--red);background:var(--red-soft)}
.lc.sup{background:var(--surface-2);border-color:var(--line-2)}
.lc .n{font:800 10.5px/1 var(--display)}
.lc .s{margin-top:4px;font:600 8px/1.3 var(--body);letter-spacing:.07em;text-transform:uppercase;color:var(--mute)}
.lc.over .s{color:#fff;background:var(--red);display:inline-block;padding:3px 6px;border-radius:99px}
.lc .big{margin-top:6px;font:800 24px/1 var(--display)}
.lc .big small{font:400 9px/1 var(--body);color:var(--mute)}
.lc .d{margin-top:5px;font-size:9px;color:var(--ink-2)}
.lc .nota{margin-top:5px;display:inline-block;border:1px dashed var(--ink-2);border-radius:99px;padding:3px 7px;font:600 8.5px/1.2 var(--body)}
table{width:100%;border-collapse:collapse}
th{text-align:left;font:600 8px/1 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--mute);padding:0 6px 5px 0}
td{padding:6px 6px 6px 0;border-top:1px solid var(--line);vertical-align:top}
tr{break-inside:avoid}
.cli{font:600 8px/1 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2)}
.tt{font-weight:600;margin-top:2px}
.tag{display:inline-block;font:500 8.5px/1 var(--body);border:1px solid var(--line-2);border-radius:99px;padding:3px 6px;color:var(--ink-2);margin-right:3px;white-space:nowrap}
.tag.late{border-color:var(--red);color:#ff6b75;background:var(--red-soft)}
.tag.prio{background:var(--red);border-color:var(--red);color:#fff;font-weight:700}
.tag.hot{background:var(--red);border-color:var(--red);color:#fff}
.tag.ok{color:var(--ok);border-color:var(--ok)}
.aj{border:1px solid var(--ink-2);background:var(--surface-2);border-radius:10px;padding:8px 10px;margin-bottom:7px;break-inside:avoid}
.aj.hot{border-color:var(--red);background:var(--red-soft)}
.aj .h{font:700 9px/1.2 var(--body);letter-spacing:.05em;text-transform:uppercase}
.aj.hot .h{color:#ff6b75}
.aj ul{margin:5px 0 0;padding:0;list-style:none}
.aj li{margin-top:4px;color:var(--ink-2);font-size:9.5px}
.aj li b{color:var(--ink)}
.aj .br{color:var(--mute);font-size:8.5px}
.vazio{color:var(--mute);padding:6px 0}
.foot{margin-top:14px;color:var(--mute);font-size:8.5px}
"""


def tipo_tag(d):
    return f'<span class="tag">{esc(d["tipo"])}</span>'


def blocos_ajuste(ids, titulos):
    html_ = []
    for i, f, dets in ajustes_do(ids):
        n = f[0] + f[1]
        hot = n > 2
        titulo = titulos.get(i, str(i))
        cab = f"{n} ajuste{'s' if n != 1 else ''} ou refação" if n else "Mais de uma etapa de edição"
        if hot:
            cab += " · acima de 2, triar"
        li = ""
        for d in dets:
            li += f'<li>{tipo_tag(d)}<b>{esc(d["quem"])}</b> · {esc(d["q"])}: {esc(d["o"])}'
            if d.get("b"):
                li += f'<div class="br">Briefing: {esc(d["b"])}</div>'
            li += "</li>"
        if not li:
            li = '<li>Sem comentários registrados no job.</li>'
        html_.append(f'<div class="aj{" hot" if hot else ""}"><div class="h">{esc(titulo)} · {cab}</div><ul>{li}</ul></div>')
    return "".join(html_)


def titulo_job(i):
    for r in rows:
        if r[1] == i:
            return f"{r[2]} · {r[3].replace(' | ', ' ').replace(' - ', ' ')}"
    for r in EXEC + SUP:
        if r[0] == i:
            return f"{r[1]} · {r[2]}"
    return str(i)


# 3) PDF do início do dia
cargas, dprod, drsv = carga()
por_grupo = {g: sum(1 for r in rows if r[0] == g) for g in range(1, 6)}
com_pedido = [r for r in rows if r[7]]
venc = [r for r in rows if prazo(r[6])[1] in ("late", "hoje")]
ids_aj = [r[1] for r in rows]


def card_carga(c):
    s = {"over": "ACIMA DA CAPACIDADE", "ok": "Dentro da capacidade", "low": "" if c["nota"] else "Com folga"}[c["st"]]
    return (f'<div class="lc {c["st"]}"><div class="n">{esc(c["curto"])}</div>' + (f'<div class="s">{s}</div>' if s else "") +
            (f'<div class="nota">{esc(c["nota"])}</div>' if c["nota"] else "") +
            f'<div class="big">{c["tot"]} <small>de {CAP_MIN} a {CAP_MAX} jobs</small></div>'
            f'<div class="d">{c["prod"]} em produção hoje · {c["rsv"]} reservados hoje' + (f' · {c["later"]} para outros dias, fora da conta' if c["later"] else '') + '</div></div>')


linhas_ped = ""
for r in sorted(com_pedido, key=lambda x: x[7].split(" ")[1]):
    pz, cl = prazo(r[6])
    linhas_ped += (f'<tr><td><div class="cli">{esc(r[2])}</div><div class="tt">{esc(r[3].replace(" | ", " "))}</div></td>'
                   f'<td>{esc(nice(r[4]))}<br><span style="color:var(--mute)">{esc("Tráfego" if r[5] == "TRÁFEGO" else r[5])}</span></td>'
                   f'<td><span class="tag {cl}">{esc(pz)}</span></td><td>{esc(pedido(r))}</td></tr>')
if not linhas_ped:
    linhas_ped = '<tr><td colspan="4" class="vazio">Nenhum pedido de prioridade registrado.</td></tr>'

bloq = [r for r in rows if r[0] in (2, 3, 5)]
linhas_bloq = ""
for r in bloq[:14]:
    pz, cl = prazo(r[6])
    linhas_bloq += (f'<tr><td><div class="cli">{esc(r[2])}</div><div class="tt">{esc(r[3].replace(" | ", " "))}</div></td>'
                    f'<td>{esc(nice(r[4]))}<br><span style="color:var(--mute)">{esc("Tráfego" if r[5] == "TRÁFEGO" else r[5])}</span></td>'
                    f'<td><span class="tag {cl}">{esc(pz)}</span></td></tr>')

pdf_ini = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Início do dia {dia.DIA}</title><style>{CSS_BASE}</style>
<body><div class="pg">
<div class="kicker">Vanguarda · Produção de vídeo e criação · Início do dia</div>
<h1>{esc(dia.FRASE)} <span>Pauta do dia - {dia.DIA}</span></h1>
<div class="stamp">Como a operação começou. Leitura do iClips em {esc(dia.LIDO)}.</div>
<div class="tiles">
<div class="tile"><b>{len(rows)}</b><span>jobs de vídeo em aberto</span></div>
<div class="tile{' alert' if com_pedido else ''}"><b>{len(com_pedido)}</b><span>com pedido de prioridade</span></div>
<div class="tile{' alert' if any(prazo(r[6])[1]=='late' for r in rows) else ''}"><b>{len(venc)}</b><span>com prazo vencido ou hoje</span></div>
<div class="tile"><b>{por_grupo[3]}</b><span>bloqueados em aprovação interna</span></div>
</div>
<h2>Carga da equipe de vídeo</h2>
<div class="cargas">{''.join(card_carga(c) for c in cargas)}
<div class="lc sup"><div class="n">Diana</div><div class="s">Supervisão · fora da capacidade</div><div class="big">{dprod + drsv} <small>jobs</small></div><div class="d">{dprod} em produção · {drsv} reservados</div></div></div>
<h2>Solicitados como prioridade</h2>
<table><tr><th>Job</th><th>Etapa e responsável</th><th>Prazo</th><th>Pedido por</th></tr>{linhas_ped}</table>
<h2>Ajustes e refações em aberto</h2>
{blocos_ajuste(ids_aj, {r[1]: titulo_job(r[1]) for r in rows}) or '<div class="vazio">Nenhum job em aberto com ajuste depois da primeira etapa de vídeo.</div>'}
<h2>Sem editor ou travados em aprovação</h2>
<table><tr><th>Job</th><th>Etapa e responsável</th><th>Prazo</th></tr>{linhas_bloq or '<tr><td colspan="3" class="vazio">Nada travado.</td></tr>'}</table>
<div class="foot">Distribuição por grupo: {por_grupo[1]} com editor, {por_grupo[2]} com o Tráfego em edição ou animação, {por_grupo[3]} em aprovação interna, {por_grupo[4]} em outras etapas, {por_grupo[5]} com o Tráfego em outra etapa. Pauta completa e marcações no artefato Pauta do dia - Edição.</div>
</div></body></html>"""
pdf_ini = sub(pdf_ini, {"__F800__": COMUM["__F800__"]})
open(os.path.join(OUT, "pdf_inicio.html"), "w", encoding="utf-8").write(pdf_ini)

# 4) PDF do fim do dia
ALL = []
vistos = set()
for r in EXEC + SUP:
    if r[0] not in vistos:
        vistos.add(r[0])
        ALL.append(r)
feitos = sum(1 for r in ALL if r[5] == "done")
mv = [r for r in rows if r[1] in MOVED]
bl = [r for r in rows if r[1] not in MOVED]
tot_aj = sum(FLAGS.get(str(r[0]), [0, 0, 1])[0] for r in ALL)
tot_rf = sum(FLAGS.get(str(r[0]), [0, 0, 1])[1] for r in ALL)
pessoas = ["Hudson Soares", "Guilherme Benevides", "Vinicius Alves", "Diana Savi"]


def por_pessoa(n):
    lst = [r for r in (SUP if n == "Diana Savi" else EXEC) if r[5] == "done" and n in r[3]]
    rec = [r for r in lst if "FDS Fraldas" in r[2] or "Fitness" in r[2]]
    return len(lst), len(rec)


cards_pess = ""
for n in pessoas:
    q, rc = por_pessoa(n)
    cards_pess += f'<div class="lc{" sup" if n == "Diana Savi" else ""}"><div class="n">{esc(n.split(" ")[0])}</div><div class="big">{q} <small>executados</small></div>' + (f'<div class="d">{rc} recorrentes de Santo Remédio</div>' if rc else '<div class="d">&nbsp;</div>') + '</div>'

lin_exec = ""
for r in ALL:
    f = FLAGS.get(str(r[0]), [0, 0, 1])
    tg = ""
    if f[0]:
        tg += f'<span class="tag{" hot" if f[0] > 2 else ""}">Ajuste{" ×%d" % f[0] if f[0] > 1 else ""}</span>'
    if f[1]:
        tg += f'<span class="tag{" hot" if f[1] > 2 else ""}">Refação{" ×%d" % f[1] if f[1] > 1 else ""}</span>'
    if f[2] > 1:
        tg += f'<span class="tag">Mais de uma etapa de edição ({f[2]})</span>'
    lin_exec += (f'<tr><td><span class="tag {"ok" if r[5]=="done" else "late"}">{"Executado" if r[5]=="done" else "Parcial"}</span></td>'
                 f'<td><div class="cli">{esc(r[1])}</div><div class="tt">{esc(r[2])}</div>{tg}</td><td>{esc(r[3])}</td><td>{esc(r[4])}</td></tr>')

lin_mv = ""
for r in mv:
    lin_mv += (f'<tr><td><div class="cli">{esc(r[2])}</div><div class="tt">{esc(r[3].replace(" | ", " "))}</div></td>'
               f'<td>{esc("Tráfego" if r[5]=="TRÁFEGO" else r[5])}</td><td style="color:var(--ink-2)">{esc(MOVED[r[1]])}</td></tr>')

ids_aj_fim = list(dict.fromkeys([r[0] for r in ALL] + [r[1] for r in mv]))
titulos_fim = {r[0]: f"{r[1]} · {r[2]}" for r in ALL}
titulos_fim.update({r[1]: titulo_job(r[1]) for r in mv})
pdf_fim = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Fim do dia {dia.DIA}</title><style>{CSS_BASE}</style>
<body><div class="pg">
<div class="kicker">Vanguarda · Produção de vídeo e criação · Fim do dia</div>
<h1>Fechamento de <span>{esc(dia.DIA_EXT)}</span></h1>
<div class="stamp">Como a operação terminou. Leitura do iClips em {esc(dia.LIDO)}.</div>
<div class="tiles">
<div class="tile"><b>{feitos} de {len(ALL)}</b><span>jobs executados no dia</span></div>
<div class="tile"><b>{len(mv)}</b><span>reprogramados para {dia.PROX}</span></div>
<div class="tile"><b>{tot_aj}</b><span>ajustes · {tot_rf} refações</span></div>
<div class="tile"><b>{len(bl)}</b><span>ainda bloqueados</span></div>
</div>
<h2>Quem executou</h2>
<div class="cargas">{cards_pess}</div>
<h2>Ajustes e refações do dia</h2>
{blocos_ajuste(ids_aj_fim, titulos_fim) or '<div class="vazio">Sem ajustes depois da primeira etapa de vídeo.</div>'}
<h2>Executados</h2>
<table><tr><th></th><th>Job</th><th>Quem</th><th>Horário</th></tr>{lin_exec}</table>
<h2>Reprogramados para {dia.PROX}</h2>
<table><tr><th>Job</th><th>Responsável</th><th>O que aconteceu</th></tr>{lin_mv or '<tr><td colspan="3" class="vazio">Nenhum.</td></tr>'}</table>
<div class="foot">{esc(RECORRENTES)} Relatório completo, com motivos, no PDF 3 e no artefato Fechamento.</div>
</div></body></html>"""
pdf_fim = sub(pdf_fim, {"__F800__": COMUM["__F800__"]})
open(os.path.join(OUT, "pdf_fim.html"), "w", encoding="utf-8").write(pdf_fim)

# Pastas e links do Drive: RELATORIOS/ANO/MÊS/DIA em "Meu Drive"
import datetime, urllib.parse
ANO = datetime.date.today().year
_dd, _mm = dia.DIA.split("/")
ISO = f"{ANO}-{_mm}-{_dd}"
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
_dj0 = os.path.join(HERE, "drive.json")
_base = json.load(open(_dj0, encoding="utf-8")).get("pasta_local", "") if os.path.exists(_dj0) else ""
PASTA_DRIVE = os.path.join(_base, str(ANO), f"{_mm} - {MESES[int(_mm) - 1]}", _dd) if _base else ""
NOMES_DRIVE = {"1-inicio-do-dia.pdf": f"{ISO} - 1 Início do dia.pdf", "2-fim-do-dia.pdf": f"{ISO} - 2 Fim do dia.pdf", "3-relatorio-do-dia.pdf": f"{ISO} - 3 Relatório do dia.pdf"}
LINK_BUSCA = "https://drive.google.com/drive/search?q=" + urllib.parse.quote(ISO)
_dj = os.path.join(HERE, "drive.json")
LINK_RAIZ = json.load(open(_dj, encoding="utf-8")).get("pasta_raiz_url", "") if os.path.exists(_dj) else ""
json.dump({"iso": ISO, "pasta": PASTA_DRIVE, "nomes": NOMES_DRIVE, "link_busca": LINK_BUSCA}, open(os.path.join(OUT, "drive_info.json"), "w", encoding="utf-8"), ensure_ascii=False)


def botao(txt, url, cor="#e11121"):
    return f'<a href="{url}" style="display:inline-block;background:{cor};color:#fff;text-decoration:none;border-radius:99px;padding:10px 18px;font:700 13px Arial,sans-serif;margin:0 8px 8px 0">{esc(txt)}</a>'


# 5) corpo do e-mail (HTML com estilos inline, compatível com clientes de e-mail)
def pilula(txt, cor="#2a2a2a", fg="#f5f5f5"):
    return f'<span style="display:inline-block;background:{cor};color:{fg};border-radius:99px;padding:3px 9px;font:600 11px Arial,sans-serif;margin:0 4px 4px 0">{esc(txt)}</span>'


def li_aj(i, f, dets):
    n = f[0] + f[1]
    hot = n > 2
    cor = "#e11121" if hot else "#2a2a2a"
    cab = f"{n} ajuste{'s' if n != 1 else ''} ou refação" if n else "Mais de uma etapa de edição"
    itens = ""
    for d in dets:
        itens += (f'<div style="margin:4px 0;font:13px/1.45 Arial,sans-serif;color:#222"><b>{esc(d["quem"])}</b> '
                  f'<span style="color:#666">· {esc(d["q"])}</span> {pilula(d["tipo"], "#eee", "#111")}<br>{esc(d["o"])}'
                  + (f'<br><span style="color:#777;font-size:12px">Briefing: {esc(d["b"])}</span>' if d.get("b") else "") + "</div>")
    if not itens:
        itens = '<div style="font:13px Arial,sans-serif;color:#777">Sem comentários registrados no job.</div>'
    return (f'<div style="border-left:4px solid {cor};background:#fafafa;padding:8px 12px;margin:0 0 10px;border-radius:0 8px 8px 0">'
            f'<div style="font:700 13px Arial,sans-serif;color:#111">{esc(titulos_fim.get(i, str(i)))} '
            f'{pilula(cab + (" · acima de 2" if hot else ""), cor, "#fff")}</div>{itens}</div>')


aj_fim = ajustes_do(ids_aj_fim)
bloco_aj = "".join(li_aj(i, f, d) for i, f, d in aj_fim) or '<div style="font:13px Arial,sans-serif;color:#777">Nenhum ajuste depois da primeira etapa de vídeo hoje.</div>'
quentes = [i for i, f, d in aj_fim if (f[0] + f[1]) > 2]
aviso_quente = (f'<div style="background:#e11121;color:#fff;border-radius:8px;padding:10px 14px;margin:0 0 14px;font:700 14px Arial,sans-serif">'
                f'Atenção: {len(quentes)} job(s) com mais de 2 ajustes ou refações, para triagem.</div>') if quentes else ""
cargas_email, _dp, _dr = carga(dia.PROX)
acima = [c for c in cargas_email if c["st"] == "over"]
aviso_cap = (f'<div style="background:#e11121;color:#fff;border-radius:8px;padding:10px 14px;margin:0 0 14px;font:700 14px Arial,sans-serif">'
             f'Acima da capacidade amanhã: {", ".join(c["curto"] for c in acima)}.</div>') if acima else ""


def celula(n, txt, cor="#111"):
    return (f'<td style="width:25%;padding:6px"><div style="background:#f3f3f3;border-radius:10px;padding:12px;text-align:left">'
            f'<div style="font:800 24px Arial,sans-serif;color:{cor}">{n}</div><div style="font:12px Arial,sans-serif;color:#555;margin-top:3px">{txt}</div></div></td>')


linhas_carga = "".join(
    f'<tr><td style="padding:5px 0;font:14px Arial,sans-serif;color:#111"><b>{esc(c["curto"])}</b></td>'
    f'<td style="font:14px Arial,sans-serif;color:#111">{c["tot"]} jobs <span style="color:#777">({c["prod"]} em produção, {c["rsv"]} reservados{(", " + str(c["later"]) + " para outros dias") if c["later"] else ""})</span></td>'
    f'<td style="font:600 12px Arial,sans-serif;color:{"#e11121" if c["st"]=="over" else "#555"}">'
    f'{"ACIMA DA CAPACIDADE" if c["st"]=="over" else ("dentro da capacidade" if c["st"]=="ok" else (c["nota"] or "com folga"))}</td></tr>'
    for c in cargas_email)

email = f"""<!doctype html><html lang="pt-BR"><body style="margin:0;background:#e9e9e9;padding:18px 0">
<table align="center" width="640" cellpadding="0" cellspacing="0" style="max-width:640px;width:100%;background:#ffffff;border-radius:14px;overflow:hidden">
<tr><td style="background:#0a0a0a;padding:22px 26px">
<div style="font:600 11px Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8d8d8d">Vanguarda · Produção de vídeo e criação</div>
<div style="font:800 26px/1.15 Arial,sans-serif;color:#fff;margin-top:8px">Pauta do dia <span style="color:#e11121">{dia.DIA}</span></div>
<div style="font:13px Arial,sans-serif;color:#c4c4c4;margin-top:6px">{esc(dia.FRASE)} Resumo do dia, de como a operação começou até como terminou.</div></td></tr>
<tr><td style="padding:20px 26px 6px">
{aviso_quente}{aviso_cap}
<table width="100%" cellpadding="0" cellspacing="0"><tr>
{celula(f"{feitos} de {len(ALL)}", "jobs executados")}{celula(len(mv), "reprogramados para " + dia.PROX)}{celula(f"{tot_aj} · {tot_rf}", "ajustes · refações", "#e11121" if quentes else "#111")}{celula(len(bl), "ainda bloqueados")}
</tr></table></td></tr>
<tr><td style="padding:10px 26px 0"><div style="font:800 15px Arial,sans-serif;color:#111;margin:10px 0 6px">Ajustes e refações do dia</div>
<div style="font:13px Arial,sans-serif;color:#555;margin-bottom:8px">Cada pedido foi cruzado com o briefing do job. Se o briefing já indicava, é erro de edição. Se não, é briefing sem as informações solicitadas.</div>
{bloco_aj}</td></tr>
<tr><td style="padding:10px 26px 0"><div style="font:800 15px Arial,sans-serif;color:#111;margin:10px 0 6px">Carga da equipe para {dia.PROX}</div>
<table width="100%" cellpadding="0" cellspacing="0">{linhas_carga}</table>
<div style="font:12px Arial,sans-serif;color:#777;margin-top:6px">Capacidade de 6 a 8 jobs por editor. A Diana, supervisora, fica fora do cálculo.</div></td></tr>
<tr><td style="padding:14px 26px 22px"><div style="font:800 15px Arial,sans-serif;color:#111;margin:10px 0 6px">Relatórios do dia</div>
<div style="font:14px/1.6 Arial,sans-serif;color:#222">1. Início do dia: como a operação começou, em uma página.<br>2. Fim do dia: como a operação terminou.<br>3. Relatório completo, com todos os jobs, motivos e briefing.</div>
<div style="margin-top:12px">{botao("Abrir os 3 PDFs do dia", LINK_BUSCA)}{botao("Pasta RELATORIOS", LINK_RAIZ, "#0a0a0a") if LINK_RAIZ else ""}</div>
<div style="font:12px Arial,sans-serif;color:#777">Os arquivos ficam em RELATORIOS / {ANO} / {_mm} - {MESES[int(_mm) - 1]} / {_dd} no Google Drive.</div>
<div style="font:12px Arial,sans-serif;color:#888;margin-top:14px">Enviado automaticamente. Dados lidos no iClips em {esc(dia.LIDO)}.</div></td></tr>
</table></body></html>"""
open(os.path.join(OUT, "email.html"), "w", encoding="utf-8").write(email)
open(os.path.join(OUT, "assunto.txt"), "w", encoding="utf-8").write(
    f"Pauta do dia {dia.DIA}: {feitos} de {len(ALL)} jobs executados"
    + (f", {len(quentes)} com mais de 2 ajustes" if quentes else "") + (", acima da capacidade" if acima else ""))

# 6) PDFs com Edge headless
EDGE = next(p for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe") if os.path.exists(p))


def pdf(src, dst):
    url = "file:///" + src.replace("\\", "/")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={dst}", url], check=True, timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if "--sem-pdf" not in sys.argv:
    for src, dst in (("pdf_inicio.html", "1-inicio-do-dia.pdf"), ("pdf_fim.html", "2-fim-do-dia.pdf"), ("fechamento.out.html", "3-relatorio-do-dia.pdf")):
        pdf(os.path.join(OUT, src), os.path.join(OUT, dst))
        print(dst, os.path.getsize(os.path.join(OUT, dst)))
print("ok")
