// Trechos que funcionaram no navegador integrado, logado no iClips (mesma origem). Somente leitura.
// Cole com javascript_tool na aba certa. Tempo limite do tool: 45 s, então use laços assíncronos e consulte depois.

// --- 1. Gestão de atividades (aba /vanguarda/DashTrafego/Lista, visão Lista) ---
// IDs de colaborador: Tráfego 3262, Hudson 3819, Guilherme 2878, Vinicius 4000, Diana 3439, Beatriz 4048, Gabrielle 3553, Ronai 2549
// SituacaoInt: 0 não planejadas, 1 planejadas, 2 em andamento, 3 aguardando aprovação, 6 finalizadas
const g = jQuery('#grid-peca'); window.__base = JSON.parse(JSON.stringify(g.data('filtroInicial') || []));
window.__gq = async (o) => { const f = JSON.parse(JSON.stringify(window.__base));
  const set = (id, v) => { let x = f.find(a => a.Id === id); if (!x) { x = { Id: id, Value: '' }; f.push(x) } x.Value = v };
  set('ResponsavelListStr', o.resp || ''); set('SituacaoInt', o.situ === undefined ? '' : String(o.situ));
  set('periodoBuscaAvancada-inicio', o.ini || ''); set('periodoBuscaAvancada-fim', o.fim || '');
  const grid = { tamanhoPagina: o.size || 300, pagina: o.page || 0, modeloStr: g.data('modelo'), propriedadeStr: g.data('propriedade'), propriedadeClickStr: g.data('propriedade-click'), idFk: 0, destinoClick: 4, desabilitarClick: '', temCheckBox: true, temEdicao: false, temCabecalho: false, temExclusao: true, temVerLayout: false, temComentario: false, temLayout: true, temSomatorio: false, gridControlArray: f, ordemPropriedade: '', ordemDirecao: '' };
  const r = await fetch('/vanguarda/DashTrafego/BuscaAvancada?propriedade=FimDate&direcao=ASC', { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }, body: JSON.stringify({ grid, incluirInativos: false }) });
  const j = await r.json(); return { total: j.Retorno.TotalRegistros, html: j.Retorno.LinhasTabela } };
// linhas: html.split('<tr class="j-abre-detalhe').slice(1); id em data-id="(\d+)"

// --- 2. Fluxo (etapas) de um job: nome, concluída, responsável, fim ---
window.__wf = async (id) => { const t = await fetch('/vanguarda/DashTrafego/CarregaWorflowJobPeca', { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest' }, body: 'idJobPeca=' + id }).then(r => r.text());
  const names = {}; for (const m of t.matchAll(/ResponsavelWorkflowStr_(\d+)"\),\s*(\[[\s\S]*?\])\s*\)/g)) { names[m[1]] = [...m[2].matchAll(/data-nome=\\"([^\]*)\\"/g)].map(x => x[1]) }
  return t.split('class="wf-item').slice(1).map(p => { const c = p.replace(/<script[\s\S]*?<\/script>/g, '').replace(/\s+/g, ' ');
    const sid = (c.match(/data-id="(\d+)"/) || [])[1]; const done = /^\s*(?:"\s*)?concluido/.test(c) || /data-concluido="True"/.test(c.slice(0, 300));
    const name = (c.match(/id="NomeStr"[^>]*value="([^"]*)"/) || c.match(/value="([^"]*)"[^>]*id="NomeStr"/) || [])[1] || (c.match(/wf-header[^"]*">\s*([^<]+?)\s*</) || [])[1] || '';
    const inputs = [...c.matchAll(/<input[^>]*>/g)].map(m => m[0]); const val = i => (i.match(/value="([^"]*)"/) || [])[1] || '';
    const fimIn = inputs.find(i => /dtFim/.test(i) && /mask-data/.test(i)); const wid = (c.match(/data-id-workflow="(\d+)"/) || [])[1] || sid;
    return { name: name.trim(), done, fim: fimIn ? val(fimIn) : '', resp: (names[wid] || names[sid] || []).join(', ') } }) };
// Responsável vazio ou "TRÁFEGO" = etapa do Tráfego.

// --- 3. Título e projeto de um job ---
// POST /vanguarda/DashTrafego/ModalDetalhe  body 'id=<idJobPeca>' -> título em <span class='title my-2'>, projeto em class='link-projeto'

// --- 4. Histórico (auditoria) de um job: quem alterou, o quê, quando ---
window.__hist = async (id) => { const dec = s => String(s).replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]*>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim(); const ev = [];
  for (let pag = 0; pag < 4; pag++) { const t = await fetch('/vanguarda/Auditoria/Listar', { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest' }, body: new URLSearchParams({ tPag: 100, pag, idEntidade: id, fullname: 'iClips.Models.Objetos.JobPeca' }).toString() }).then(r => r.text());
    const li = t.split('<li id="interacao"').slice(1); if (!li.length) break;
    for (const x of li) { const actor = dec((x.match(/<strong>([\s\S]*?)<\/strong>/) || [])[1] || ''); const body = dec((x.match(/<div class="historico-title">([\s\S]*?)<div class="collapse-content/) || x.match(/<div class="historico-title">([\s\S]*?)<\/div>/) || [])[1] || ''); const ts = (x.match(/title="(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2})"/) || [])[1] || ''; ev.push({ actor, act: body.replace(actor, '').trim(), ts }) }
    if (li.length < 100) break } return ev };

// --- 5. Atividades realizadas por colaborador (aba /vanguarda/AtividadeRealizadaFuncionario/Relatorio) ---
window.__rq = async (url, extra, p) => { const f = getFiltro().map(x => Object.assign({}, x)); const set = (id, v) => { const x = f.find(a => a.Id === id); if (x) x.Value = v };
  set('IdFuncionario', extra.resp || ''); set('data-de-inicioI', extra.di || ''); set('data-de-fimI', extra.df || ''); set('data-de-inicioF', extra.dif || ''); set('data-de-fimF', extra.dff || '');
  const r = await fetch(url, { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }, body: JSON.stringify({ grid: Object.assign({ gridControlArray: f }, p || {}) }) }); return await r.json() };
// Uso: await __rq('/vanguarda/AtividadeRealizadaFuncionario/BuscaAvancada', {resp:'3819', di:'DD/MM/AAAA', dff:'DD/MM/AAAA'}, {})
// Sessões: r.Retorno.LinhasTabela.split('<tr class="sub-tabela-relatorio"').slice(1); id do job em <td class="pl-9" id="(\d+)">; título em <span class="primaria">; início e fim em <td class="td-legenda"> dd/mm/aaaa hh:mm:ss <span ...>.

// --- 6. Briefing e comentários de um job ---
// Navegar para https://app.iclips.com.br/vanguarda/JobPeca/Atividade/<idJobPeca>, esperar ~5,5 s e ler document.querySelector('#Detalhe').innerText.
// Briefing = texto entre 'Briefing' e 'Comentários'. Comentários = texto depois de 'Comentários' até 'Press Alt+0'.
