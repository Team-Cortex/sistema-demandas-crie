import copy
import re
import sys

import docx
from docx.table import Table, _Cell
from PIL import Image

from fill_lib import *
from c1_inicio import *
from c2_volere_1_9 import *
from c3_requisitos import *
from c4_vv import *
from c5_resto import *

MODELO = 'template.docx'
SAIDA = sys.argv[1] if len(sys.argv) > 1 else 'saida.docx'
DIAG = '../diagramas/'
TELAS = '../telas/'
DER = '../../../docs/modelagem/DER_CRIE_v2.png'

doc = docx.Document(MODELO)
body = doc.element.body
T = lambda el: Table(el, doc)


def cab(titulo, exato=False, depois=None):
    """Parágrafo de título (Heading) que começa com o texto."""
    return acha_paragrafo(doc, titulo, exato=exato, depois=depois)


def tabelas_apos(titulo, n=1, exato=False):
    p = cab(titulo, exato)
    res = []
    x = p
    for _ in range(n):
        x = proxima_tabela(x)
        res.append(T(x))
    return res


def resposta(titulo, paragrafos, idx=0):
    t = tabelas_apos(titulo, idx + 1)[idx]
    preenche_celula(t.rows[0].cells[0], paragrafos)
    return t


def troca_tabela_por_texto(tbl_el, texto_):
    p = paragrafo_depois(tbl_el, texto_)
    remove(tbl_el)
    return p


def largura_img(caminho, max_l=15.3, max_a=15.5):
    w, h = Image.open(caminho).size
    l = max_l
    if h / w * l > max_a:
        l = max_a * w / h
    return l


# cópias limpas para reaproveitar depois
tab_historico_modelo = copy.deepcopy(tabelas_apos('Histórico de Revisões', exato=True)[0]._tbl)

# ---------------- Capa ----------------
substitui_texto_paragrafo(cab('[NOME DA INSTITUIÇÃO DE ENSINO]', True), CAPA['instituicao'])
substitui_texto_paragrafo(cab('[Curso]', True), CAPA['curso'])
substitui_texto_paragrafo(cab('[NOME DO SISTEMA]', True), CAPA['sistema'])
substitui_texto_paragrafo(cab('Equipe:', True), CAPA['equipe_rotulo'])
preenche_linhas(T(proxima_tabela(cab('Equipe Cortex:', True))), CAPA['equipe'])
substitui_texto_paragrafo(cab('[Cidade]', True), CAPA['cidade'])
substitui_texto_paragrafo(cab('[Mês e ano]', True), CAPA['mes'])

# ---------------- Controle ----------------
preenche_chave_valor(tabelas_apos('Controle do Documento', exato=True)[0], CONTROLE)
preenche_linhas(tabelas_apos('Histórico de Revisões', exato=True)[0], HISTORICO)
preenche_linhas(tabelas_apos('Papéis da Equipe', exato=True)[0], PAPEIS)
remove(cab('Após preencher o documento, atualize o sumário'))

# ---------------- Organização do documento ----------------
h = cab('Instruções de Preenchimento', True)
substitui_texto_paragrafo(h, 'Organização do Documento')
p0 = cab('Este documento é o modelo oficial')
substitui_texto_paragrafo(p0, ORGANIZACAO_INTRO[0])
paragrafo_depois(p0, ORGANIZACAO_INTRO[1], modelo_el=p0)
rg = cab('Regras gerais', True)
x = rg.getnext()
while x is not None and texto(x).strip() != 'Mapa das entregas':
    nxt = x.getnext()
    remove(x)
    x = nxt
remove(rg)
mapa = tabelas_apos('Mapa das entregas', exato=True)[0]
for i, txt in enumerate(MAPA_ENTREGAS_COL4, start=1):
    preenche_celula(mapa.rows[i].cells[3], txt)

# ---------------- Parte I ----------------
resposta('I.1 Propósito', I1)
resposta('I.2 Visão Geral', I2)
preenche_chave_valor(tabelas_apos('I.2 Visão Geral', 2)[1], I2_TABELA)
preenche_chave_valor(tabelas_apos('I.3 Processo de Software', 1)[0], I3)
preenche_linhas(tabelas_apos('I.3a', 1)[0], I3A)
preenche_chave_valor(tabelas_apos('I.3b', 1)[0], I3B)
preenche_linhas(tabelas_apos('I.4a', 1)[0], I4A)
substitui_texto_paragrafo(cab('Justificativa da escolha das técnicas'), I4A_JUSTIFICATIVA)
preenche_chave_valor(tabelas_apos('I.4b', 1)[0], I4B)
preenche_chave_valor(tabelas_apos('I.4c', 1)[0], I4C)
preenche_chave_valor(tabelas_apos('I.4d', 1)[0], I4D)
preenche_linhas(tabelas_apos('I.4e', 1)[0], NECESSIDADES)
resposta('I.4f', I4F)

# ---------------- Volere 1 a 9 ----------------
resposta('1a.', V1A)
preenche_linhas(tabelas_apos('1b.', 1)[0], V1B)
resposta('2a.', [V2A])
resposta('2b.', [V2B])
preenche_linhas(tabelas_apos('2c.', 1)[0], V2C)
preenche_linhas(tabelas_apos('2d.', 1)[0], V2D)
preenche_linhas(tabelas_apos('2e.', 1)[0], V2E)
preenche_linhas(tabelas_apos('2f.', 1)[0], V2F)
resposta('2g.', V2G)
resposta('2h.', [V2H])
preenche_linhas(tabelas_apos('3a.', 1)[0], V3A)
resposta('3b.', [V3B])
resposta('3c.', [V3C])
resposta('3d.', [V3D])
resposta('3e.', [V3E])
preenche_linhas(tabelas_apos('3f.', 1)[0], V3F)
resposta('3g.', [V3G])
preenche_linhas(tabelas_apos('4a.', 1)[0], GLOSSARIO)
resposta('5a.', ['• ' + f for f in V5A])
preenche_linhas(tabelas_apos('5b.', 1)[0], RN)
preenche_linhas(tabelas_apos('5c.', 1)[0], V5C)
resposta('6a.', V6A)
figura_na_celula(doc, tabelas_apos('6b.', 1)[0], DIAG + 'fig01_contexto.png', 'Figura 1 – Diagrama de contexto do trabalho', 'Fonte: elaborado pela equipe (2026), a partir do relatório v3 e de docs/requisitos.md.', 15.3)
preenche_linhas(tabelas_apos('6c.', 1)[0], EVENTOS)

# 6d: um quadro por evento
t6d = tabelas_apos('6d.', 1)[0]
modelo6d = copy.deepcopy(t6d._tbl)
ultimo = t6d._tbl
for i, (ev, ent, passos, sai) in enumerate(ESPEC_EVENTOS):
    if i == 0:
        tb = t6d
    else:
        sep = paragrafo_vazio_depois(ultimo)
        novo = copy.deepcopy(modelo6d)
        sep.addnext(novo)
        tb = T(novo)
    preenche_chave_valor(tb, [ev, ent, passos, sai])
    ultimo = tb._tbl

# 7
t7 = tabelas_apos('7a.', 1)[0]
figura_na_celula(doc, t7, DER, 'Figura 2 – Modelo de dados do negócio (DER conceitual, versão 2)', 'Fonte: frente de Banco de Dados da equipe, docs/modelagem/DER_CRIE_v2.png (2026).', 13.5)
paragrafo_depois(t7._tbl, V7_NOTA)
preenche_linhas(tabelas_apos('7b.', 1)[0], DICIONARIO)

# 8
t8 = tabelas_apos('8a.', 2)
figura_na_celula(doc, t8[0], DIAG + 'fig03_casos_de_uso.png', 'Figura 3 – Diagrama de casos de uso', 'Fonte: elaborado pela equipe (2026), a partir das specs 01 a 09.', 15.3)
preenche_chave_valor(t8[1], [V8A_FARA, V8A_NAO])
preenche_linhas(tabelas_apos('8b.', 1)[0], UCS)
t8c = tabelas_apos('8c.', 1)[0]
modelo8c = copy.deepcopy(t8c._tbl)
ultimo = t8c._tbl
for i, u in enumerate(UC_DETALHE):
    if i == 0:
        tb = t8c
    else:
        sep = paragrafo_vazio_depois(ultimo)
        novo = copy.deepcopy(modelo8c)
        sep.addnext(novo)
        tb = T(novo)
    preenche_chave_valor(tb, [u['id'], u['objetivo'], u['ator'], u['secundarios'], u['prioridade'], u['pre'], u['fluxo'], u['alt'], u['exc'], u['pos'], u['req']])
    ultimo = tb._tbl

# 9a
preenche_linhas(tabelas_apos('9a.', 1)[0], [[r['id'], r['desc'], r['origem'], r['uc'], r['criterio'], r['moscow']] for r in RF])

# 9b cartões
NOMES_SECAO = {
    '10a': '10a – Aparência', '10b': '10b – Estilo', '11a': '11a – Facilidade de uso', '11c': '11c – Aprendizagem',
    '11d': '11d – Compreensão e cortesia', '11e': '11e – Acessibilidade', '12a': '12a – Velocidade e latência',
    '12c': '12c – Precisão', '12e': '12e – Robustez', '12f': '12f – Capacidade', '13a': '13a – Ambiente físico',
    '13b': '13b – Interfaces com sistemas adjacentes', '13c': '13c – Produção', '13d': '13d – Lançamento',
    '14a': '14a – Manutenção', '14c': '14c – Adaptabilidade', '15a': '15a – Acesso', '15b': '15b – Integridade',
    '15c': '15c – Privacidade', '15d': '15d – Auditoria', '15e': '15e – Imunidade', '16a': '16a – Culturais',
    '16b': '16b – Políticos', '17a': '17a – Conformidade legal', '17b': '17b – Padrões',
}
ORIGEM_N = {n[0]: n[2] for n in NECESSIDADES}


def origem_cartao(o):
    ids = re.findall(r'N-\d\d', o)
    if ids:
        return o + ' – ' + ORIGEM_N[ids[0]]
    return o


t9b = tabelas_apos('9b.', 1)[0]
p_regra = paragrafo_depois(cab('9b.').getnext() if False else cab('9b.'), REGRA_NOTAS)
# o parágrafo da regra fica logo depois do título; o bloco "Conteúdo" é removido no fim
modelo9b = copy.deepcopy(t9b._tbl)
cartoes = [r for r in RF if r['moscow'] == 'Must'] + [r for r in RNF if r['moscow'] == 'Must']
ultimo = t9b._tbl
for i, r in enumerate(cartoes):
    if i == 0:
        tb = t9b
    else:
        sep = paragrafo_vazio_depois(ultimo)
        novo = copy.deepcopy(modelo9b)
        sep.addnext(novo)
        tb = T(novo)
    if r['id'].startswith('RF'):
        tipo = '9 – Funcional'
        ev = r['evento'] + ' / ' + r['uc']
    else:
        tipo = NOMES_SECAO[r['secao']] + ' (não funcional)'
        ev = r.get('uc', '—')
    preenche_chave_valor(tb, [r['id'], tipo, ev, r['desc'], r['just'], origem_cartao(r['origem']), r['criterio'],
                              f"{r['sat']} (estimada)", f"{r['insat']} (estimada)", 'Must', r['conf'], r['mat'], r['hist']])
    ultimo = tb._tbl
N_CARTOES = len(cartoes)

# ---------------- 10 a 17 ----------------
RNF_POR_ID = {r['id']: r for r in RNF}
for secao, ids in SECOES_RNF.items():
    p = cab(secao + '.')
    tbl = proxima_tabela(p)
    if ids is None:
        troca_tabela_por_texto(tbl, NAO_SE_APLICA[secao])
    else:
        preenche_linhas(T(tbl), [[i, RNF_POR_ID[i]['desc'], RNF_POR_ID[i]['just'], RNF_POR_ID[i]['criterio'], RNF_POR_ID[i]['moscow']] for i in ids])

# ---------------- 18 a 27 ----------------
preenche_linhas(tabelas_apos('18. Temas Abertos', 1)[0], TEMAS)
resposta('19a.', V19A)
resposta('19b.', [V19B])
resposta('19c.', [V19C])
for k, v in V20.items():
    resposta(k + '.', [v])
resposta('21a.', [V21A])
preenche_linhas(tabelas_apos('21b.', 1)[0], V21B)
resposta('22a.', V22A)
preenche_linhas(tabelas_apos('22b.', 1)[0], V22B)
preenche_linhas(tabelas_apos('23. Riscos', 1)[0], RISCOS)
preenche_linhas(tabelas_apos('24. Custos', 1)[0], CUSTOS)
substitui_texto_paragrafo(cab('Método de estimativa utilizado'), CUSTOS_METODO)
preenche_linhas(tabelas_apos('25a.', 1)[0], V25A)
resposta('25b.', [V25B])
preenche_linhas(tabelas_apos('26. Sala de Espera', 1)[0], SALA)
resposta('27. Ideias', ['• ' + i for i in V27])

# ---------------- Parte III ----------------
preenche_chave_valor(tabelas_apos('III.1', 1)[0], III1)
preenche_chave_valor(tabelas_apos('III.2', 1)[0], III2)
figura_na_celula(doc, tabelas_apos('III.3', 1)[0], DIAG + 'fig04_mapa_navegacao.png', 'Figura 4 – Mapa de navegação entre telas', 'Fonte: elaborado pela equipe (2026), a partir de docs/ihc/arquitetura-da-informacao.md.', 15.3)
preenche_linhas(tabelas_apos('III.4', 1)[0], TELAS_INV)

h_tela = cab('Tela T-01')
t_fig = h_tela.getnext()
while t_fig.tag != W('tbl'):
    t_fig = t_fig.getnext()
x = t_fig.getnext()
while x.tag != W('tbl'):
    x = x.getnext()
t_det = x
m_h, m_fig, m_det = copy.deepcopy(h_tela), copy.deepcopy(t_fig), copy.deepcopy(t_det)
ultimo = t_det
fig_n = 5
for i, tl in enumerate(TELAS_DESC):
    if i == 0:
        hh, ff, dd = h_tela, t_fig, t_det
    else:
        sep = paragrafo_vazio_depois(ultimo)
        hh = copy.deepcopy(m_h); sep.addnext(hh)
        ff = copy.deepcopy(m_fig); hh.addnext(ff)
        s2 = paragrafo_vazio_depois(ff)
        dd = copy.deepcopy(m_det); s2.addnext(dd)
    substitui_texto_paragrafo(hh, f"Tela {tl['t']} – {tl['nome']}")
    img = TELAS + tl['img']
    figura_na_celula(doc, T(ff), img, f"Figura {fig_n} – Protótipo da tela {tl['t']} ({tl['nome']})", 'Fonte: protótipo clicável (docs/ihc/prototipo/index.html), captura de 23/11/2026, dados fictícios.', largura_img(img, 14.5, 13.5))
    preenche_chave_valor(T(dd), [tl['obj'], tl['el'], tl['reg'], tl['msg'], tl['nav'], tl['req']])
    ultimo = dd
    fig_n += 1

t36 = tabelas_apos('III.6', 1)[0]
preenche_linhas(t36, III6)
paragrafo_depois(t36._tbl, III6_TEXTO)

# ---------------- Parte IV ----------------
resposta('IV.1', IV1)
preenche_linhas(tabelas_apos('IV.2', 1)[0], IV2)
resposta('IV.3', IV3)


def expande(txt, prefixo):
    ids = set()
    for a, b in re.findall(prefixo + r'-(\d{3}) a ' + prefixo + r'-(\d{3})', txt):
        for n in range(int(a), int(b) + 1):
            ids.add(f'{prefixo}-{n:03d}')
    for a in re.findall(prefixo + r'-(\d{3})', txt):
        ids.add(f'{prefixo}-{a}')
    return ids


def reqs_de(txt):
    return expande(txt, 'RF') | expande(txt, 'RNF')


ct_por_req, cb_por_req = {}, {}
for c in CT:
    for r in reqs_de(c[1]):
        ct_por_req.setdefault(r, []).append(c[0])
for c in CB:
    for r in reqs_de(c[1]):
        cb_por_req.setdefault(r, []).append(c[0])
pb_por_req = {}
for pb in BACKLOG:
    for r in reqs_de(pb[2]):
        pb_por_req.setdefault(r, []).append(f"{pb[0]} / C{pb[5]}" if pb[5] not in ('—',) else pb[0])

SITUACAO = {
    'RF-002': 'Implementado em parte: expiração fixa de 30 min (Q-15)',
    'RF-005': 'Implementado; regra restritiva desligada por decisão da direção',
    'RF-037': 'Implementado (impressão pelo navegador); teste pendente',
    'RF-041': 'Não implementado (Won’t)',
    'RNF-006': 'Implementado; revisão manual pendente', 'RNF-007': 'Implementado; revisão manual pendente',
    'RNF-009': 'Pendente: orientação não elaborada', 'RNF-010': 'Pendente: procedimento não documentado',
    'RNF-011': 'Implementado; validação com usuários pendente', 'RNF-013': 'Implementado; validação com usuários pendente',
    'RNF-029': 'Validação com usuários pendente', 'RNF-036': 'Validação com usuários pendente',
    'RNF-012': 'Implementado; verificado manualmente; T3 pendente',
    'RNF-015': 'Implementado; verificação parcial',
    'RNF-016': 'Implementado; verificado (PR #18 e teste do cliente)',
    'RNF-017': 'Não medido', 'RNF-018': 'Não medido',
    'RNF-024': 'Atendido em parte (4 de 5 integrantes)',
    'RNF-025': 'Implementado; HTTPS verificado; planos a conferir',
    'RNF-026': 'Parcial: instalação documentada; manual pendente',
    'RNF-031': 'Verificação no CRIE pendente',
    'RNF-032': 'Parcial: CI no PR #19, ainda não integrado',
    'RNF-004': 'Atendido pela hospedagem; verificado em 23/11/2026',
    'RNF-027': 'Implementado; autorização do logotipo pendente',
    'RNF-028': 'Implementado; verificado (PR #18)', 'RNF-033': 'Implementado; verificado (PR #18)',
    'RNF-035': 'Implementado; verificado (PR #18)',
    'RNF-021': 'Implementado; lint e build sem erro',
    'RNF-023': 'Implementado; contrato conferido',
}
linhas_mat = []
for r in RF + RNF:
    rid = r['id']
    testes = ct_por_req.get(rid, []) + cb_por_req.get(rid, [])
    sit = SITUACAO.get(rid, 'Implementado; testes aprovados (CI de 23/11/2026)')
    linhas_mat.append([f"{rid} ({r['moscow']})", r['origem'].replace('Criado em 23/11/2026 neste documento, a partir de ', ''), r.get('uc', '—'),
                       ', '.join(testes) if testes else '—', ', '.join(dict.fromkeys(pb_por_req.get(rid, []))) or '—', sit])
preenche_linhas(tabelas_apos('IV.4', 1)[0], linhas_mat)
print('sem backlog:', [l[0] for l in linhas_mat if l[4] == '—'])
print('sem teste:', [l[0] for l in linhas_mat if l[3] == '—'])

# ---------------- Parte V ----------------
preenche_linhas(tabelas_apos('V.1', 1)[0], V1)
tv2 = tabelas_apos('V.2', 1)[0]
for i, (at, prob) in enumerate(V2, start=1):
    preenche_celula(tv2.rows[i].cells[1], at)
    preenche_celula(tv2.rows[i].cells[2], prob)
preenche_chave_valor(tabelas_apos('V.3', 1)[0], V3)
tv4 = tabelas_apos('V.4', 1)[0]
preenche_linhas(tv4, CT)
larguras(tv4, [820, 1100, 2101, 1350, 1500, 1150, 1050])
CB_FMT = [[c[0], c[1], c[2], re.sub(r'\(((?:test_|frontend/|backend/)[^()]*)\)', lambda mm: '~~(' + mm.group(1) + ')~~', c[3]), c[4], ('Conforme (CI)' if c[5] == CI else c[5]), c[6]] for c in CB]
tv5 = tabelas_apos('V.5', 1)[0]
preenche_linhas(tv5, CB_FMT)
larguras(tv5, [820, 1100, 1450, 2451, 1250, 950, 1050])
preenche_linhas(tabelas_apos('V.6', 1)[0], V6)
preenche_linhas(tabelas_apos('V.7', 1)[0], BUGS)
# resumo: mantém a quebra de página do parágrafo
pres = cab('Resumo da execução')
quebras = [r for r in pres.findall(W('r')) if any(b.get(W('type')) == 'page' for b in r.iter(W('br')))]
rpr0 = OxmlElement('w:rPr')
for r in pres.findall(W('r')):
    if r not in quebras:
        pres.remove(r)
tmp = OxmlElement('w:p')
f = OxmlElement('w:rFonts'); f.set(W('eastAsia'), 'Arial'); f.set(W('cs'), 'Arial'); rpr0.append(f)
escreve_runs(tmp, RESUMO, rpr0)
ins = pres.find(W('pPr'))
pos = list(pres).index(ins) + 1 if ins is not None else 0
for k, r in enumerate(list(tmp.findall(W('r')))):
    pres.insert(pos + k, r)

# ---------------- Parte VI ----------------
tb1 = tabelas_apos('VI.1', 1)[0]
preenche_linhas(tb1, BACKLOG)
paragrafo_depois(tb1._tbl, BACKLOG_NOTA)
preenche_linhas(tabelas_apos('VI.2', 1)[0], CICLOS)
preenche_linhas(tabelas_apos('VI.3', 1)[0], CRONOGRAMA)
resposta('VI.4', VI4)
FERR = [
    ['IDE / editor', 'Não padronizado', 'O repositório não registra o editor usado por cada integrante'],
    ['Controle de versão', 'Git e GitHub (organização Team-Cortex)', 'Monorepo; uma branch por funcionalidade; PR para a development; main como produção (VI.6)'],
    ['Gestão de tarefas', 'Trello, quadro “Equipe Cortex”', 'Kanban com checklists e etiquetas por frente (VI.4)'],
    ['Modelagem e diagramas', 'draw.io; SVG', 'DER em docs/modelagem/DER_CRIE_v2.drawio; diagramas deste documento em entregas/engenharia-de-software/diagramas'],
    ['Prototipação', 'Figma; HTML', 'Telas iniciais no Figma; protótipo clicável em docs/ihc/prototipo'],
    ['Testes', 'pytest; node:test', 'Back-end com o test client do Flask e SQLite em memória; funções do cliente React'],
    ['Build e dependências', 'pip, npm, Vite, Docker Compose, Alembic', 'Dependências travadas (requirements.txt e package-lock.json); PostgreSQL local; migrações versionadas'],
    ['Integração e entrega contínuas', 'GitHub Actions; Vercel', 'Workflow “Testes” em todo PR (PR #19, em revisão); a Vercel publica a cada merge na main'],
    ['Análise estática', 'ESLint; check-segredo.mjs', 'Front-end sem erro de lint no CI de 23/11/2026; verificação de segredos no CI. O back-end não tem linter; SonarQube não foi usado'],
]
preenche_linhas(tabelas_apos('VI.5', 1)[0], FERR)
preenche_chave_valor(tabelas_apos('VI.6', 1)[0], VI6)

# ---------------- Parte VII ----------------
preenche_linhas(tabelas_apos('VII.1', 1)[0], VII1)
preenche_linhas(tabelas_apos('VII.2', 1)[0], VII2)
t73 = tabelas_apos('VII.3', 1)[0]
for i, vals in enumerate(VII3, start=1):
    for j, v in enumerate(vals, start=1):
        preenche_celula(t73.rows[i].cells[j], v)
resposta('VII.4', VII4)

# ---------------- Parte VIII ----------------
resposta('VIII.1', VIII1)
resposta('VIII.2', VIII2)
t83 = tabelas_apos('VIII.3', 1)[0]
preenche_linhas(t83, VIII3)
paragrafo_depois(t83._tbl, VIII3_NOTA)

# referências em ordem alfabética
p_ref1 = cab('PRESSMAN, Roger')
modelo_ref = copy.deepcopy(p_ref1)
refs_modelo = []
x = p_ref1
while x is not None and not texto(x).startswith('VIII.5'):
    nxt = x.getnext()
    t_ = texto(x).strip()
    if t_ and not t_.startswith('['):
        refs_modelo.append(t_)
    if not t_.startswith('VIII.5'):
        remove(x)
    x = nxt
todas = sorted(refs_modelo + REFERENCIAS_EXTRA, key=lambda s: s.upper().replace('Ç', 'C'))
h85 = cab('VIII.5')
ant = h85.getprevious()
for ref in todas:
    novo = copy.deepcopy(modelo_ref)
    substitui_texto_paragrafo(novo, ref)
    ant.addnext(novo)
    ant = novo

t85 = tabelas_apos('VIII.5', 1)[0]
for i, txt in enumerate(ANEXOS, start=1):
    preenche_celula(t85.rows[i].cells[1], txt)
leg = paragrafo_depois(t85._tbl, 'Quadro C.1 – Pull requests do repositório até 23/11/2026 (Anexo C)', negrito=True)
tprs = copy.deepcopy(tab_historico_modelo)
leg.addnext(tprs)
tp = T(tprs)
for j, v in enumerate(['Nº', 'Aberto por', 'Conteúdo', 'Integrado em']):
    preenche_celula(tp.rows[0].cells[j], v)
preenche_linhas(tp, PRS)

t86 = tabelas_apos('VIII.6', 1)[0]
larguras(t86, [5271, 3800])
for i, txt in enumerate(CHECKLIST, start=1):
    preenche_celula(t86.rows[i].cells[1], txt)

# cabeçalho
for s in doc.sections:
    for hdr in (s.header, s.first_page_header, s.even_page_header):
        for p in hdr.paragraphs:
            for r in p.runs:
                if '[Nome do Sistema]' in r.text or '[1.0]' in r.text:
                    r.text = r.text.replace('[Nome do Sistema]', SISTEMA).replace('[1.0]', VERSAO)

n = remove_blocos_conteudo(doc)
doc.save(SAIDA)

# conferências
restos = []
for el in doc.element.body.iter(W('t')):
    if el.text and re.search(r'\[[^\]]*\]', el.text) and 'erro' not in el.text:
        restos.append(el.text)
print('blocos removidos:', n, '| cartões:', N_CARTOES, '| CT:', len(CT), '| CB:', len(CB))
print('textos com colchetes restantes:', restos[:20])
