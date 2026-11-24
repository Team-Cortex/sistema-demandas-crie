# Gera o deck do seminário de BD1 (equipe Cortex) na identidade visual do CRIE.
# Saídas: deck/index.html (arquivo único, abre offline) e, com --pdf, deck/Seminario_BD1_Equipe_Cortex.pdf.
# Identidade: handoff do site do CRIE (site-crie/docs/handoff/README.md, "Design Tokens"): tinta e papel,
# acentos magenta, amarelo, roxo, ciano e verde, barra de quatro cores, Bricolage Grotesque 800, Archivo e
# IBM Plex Mono, cantos vivos, sem sombras e sem ícones.
# Dados: scripts 01 a 04 da entrega e ferramentas/resultados.json (17 consultas rodadas no MySQL 8.4 com
# SET TIMESTAMP de 30/11/2026 19:00). Todos fictícios.
import ast
import base64
import html
import json
import math
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FERR = os.path.join(RAIZ, 'ferramentas')
# Scripts .sql: em entrega/ na pasta do projeto; no repositório do sistema, em docs/modelagem/sql/.
ENTREGA = next((p for p in (os.path.join(RAIZ, 'entrega'), os.path.join(RAIZ, '..', 'sql'))
                if os.path.exists(os.path.join(p, '01_criacao_banco.sql'))), os.path.join(RAIZ, 'entrega'))
sys.path.insert(0, FERR)
from conteudo import RELACIONAMENTOS  # noqa: E402
sys.path.insert(0, AQUI)
import notas  # noqa: E402

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
e = html.escape

# ------------------------------------------------------------------ identidade (tokens do site do CRIE)
TINTA9, TINTA8, TINTA6, TINTA5 = '#0E1013', '#16181C', '#2A2D33', '#3A3D44'
CINZA, PAPEL, LINHA = '#5A5D64', '#F6F5F2', '#E2DFD8'
CORPO_ESCURO, MUDO_ESCURO = '#B9B5AC', '#8C8880'
MAGENTA, AMARELO, ROXO, CIANO, VERDE, ROXO_CLARO = '#E5006E', '#F2B300', '#8A21CE', '#12A9E0', '#2E9E63', '#E7CBFA'
TEXTO_SOBRE = {MAGENTA: '#FFFFFF', ROXO: '#FFFFFF', AMARELO: TINTA8, CIANO: TINTA8, VERDE: TINTA8, TINTA8: '#FFFFFF'}
NO_ESCURO = {ROXO: ROXO_CLARO}  # roxo sobre a tinta não passa no contraste; usa o roxo claro do site
BARRA4 = (MAGENTA, AMARELO, ROXO, CIANO)  # ordem fixa do handoff


def ler(*partes):
    with open(os.path.join(*partes), encoding='utf-8') as f:
        return f.read()


def resumo_das_consultas():
    """Lê o dicionário RESUMO de gerar_slides.py sem executar o arquivo."""
    for no in ast.parse(ler(FERR, 'gerar_slides.py')).body:
        if isinstance(no, ast.Assign) and getattr(no.targets[0], 'id', '') == 'RESUMO':
            return ast.literal_eval(no.value)
    raise SystemExit('RESUMO não encontrado')


RESUMO = resumo_das_consultas()
CONSULTAS = json.load(open(os.path.join(FERR, 'resultados.json'), encoding='utf-8'))
SQL01 = ler(ENTREGA, '01_criacao_banco.sql')

# Registros por tabela depois do 02_carga_dados.sql (COUNT(*) no MySQL 8.4, 23/11/2026).
CARGA = [('usuario', 10), ('assistido', 12), ('assistido_profissional', 21), ('reuniao', 13), ('demanda', 29), ('evolucao', 18)]
COR_TABELA = {'usuario': ROXO, 'assistido': MAGENTA, 'assistido_profissional': AMARELO,
              'reuniao': CIANO, 'demanda': VERDE, 'evolucao': TINTA8}

# Quem fala em cada parte e em cada bloco de consultas está no GUIA_APRESENTACAO.md; os slides mostram só partes e blocos.
PARTES = [
    (1, AMARELO, '0:00', '2:00', 'Abertura', 'O CRIE, as regras do minimundo e o recorte'),
    (2, VERDE, '2:00', '5:00', 'Modelagem', 'DER, relacionamentos, notação textual, 3FN e scripts'),
    (3, MAGENTA, '5:00', '17:00', 'Consultas', 'As 17 consultas: cada integrante explica 3 ou 4'),
    (4, ROXO, '17:00', '18:30', 'Manutenção e sistema', 'Script 04, o banco no sistema e os critérios'),
    (5, TINTA8, '18:30', '20:00', 'Perguntas', 'Toda a equipe'),
]
COR_PARTE = {n: c for n, c, *_ in PARTES}
# Cada integrante explica um bloco de consultas (a ordem de quem fala está no guia).
BLOCOS = [('Q01', 'Q03', AMARELO, '6:00', '8:00'), ('Q04', 'Q06', VERDE, '8:00', '10:00'),
          ('Q07', 'Q10', CIANO, '10:00', '12:40'), ('Q11', 'Q14', MAGENTA, '12:40', '15:20'),
          ('Q15', 'Q17', ROXO, '15:20', '17:00')]

# Títulos curtos (o enunciado completo fica nas notas do apresentador).
TITULO_Q = {
    'Q01': 'Demandas que citam o CRAS ou o Conselho Tutelar',
    'Q02': 'Reuniões de outubro de 2026 (pedagógico e saúde)',
    'Q03': 'Demandas em aberto com prazo vencido',
    'Q04': 'Demandas em aberto que vencem nos próximos 7 dias',
    'Q05': 'Prioridade alta com assistido, reunião e responsável',
    'Q06': 'Assistidos ativos sem nenhuma demanda',
    'Q07': 'Demandas em aberto por profissional, inclusive zero',
    'Q08': 'Tempo médio para concluir, por prioridade',
    'Q09': 'Demandas por setor e estado, com percentual',
    'Q10': 'Demandas abertas por mês e categorias diferentes',
    'Q11': 'A demanda em aberto mais antiga',
    'Q12': 'Concluídas que demoraram mais que a média',
    'Q13': 'Profissionais ativos sem assistido para acompanhar',
    'Q14': 'Quantos assistidos cada profissional acompanha (N:N)',
    'Q15': 'Evoluções retificadas, a antiga ao lado da nova (1:1)',
    'Q16': 'Assistidos sem evolução vigente há mais de 20 dias',
    'Q17': 'Todas as reuniões e quantas demandas cada uma originou',
}
# Recursos de cada consulta, resumidos do campo "comandos" do resultados.json.
CHIPS_Q = {
    'Q01': ['LIKE com %', 'OR', 'ORDER BY'],
    'Q02': ['IN', 'BETWEEN com datas', 'DATE_FORMAT'],
    'Q03': ['CURDATE', 'DATEDIFF', 'NOT IN', 'ORDER BY DESC'],
    'Q04': ['ADDDATE + INTERVAL', 'BETWEEN', 'CURDATE', 'DATEDIFF'],
    'Q05': ['INNER JOIN de 4 tabelas', 'apelidos (AS)', 'DATE_FORMAT'],
    'Q06': ['LEFT JOIN', 'IS NULL'],
    'Q07': ['LEFT JOIN com condição no ON', 'COUNT(coluna)', 'GROUP BY'],
    'Q08': ['GROUP BY', 'HAVING', 'AVG', 'ROUND', 'DATEDIFF', 'MIN', 'MAX'],
    'Q09': ['INNER JOIN', 'GROUP BY com 2 colunas', 'subconsulta no SELECT', 'ROUND'],
    'Q10': ['YEAR', 'MONTH', 'COUNT(DISTINCT)', 'GROUP BY'],
    'Q11': ['subconsulta com MIN', 'JOIN', 'DATEDIFF'],
    'Q12': ['subconsulta com AVG', 'DATEDIFF', 'ROUND'],
    'Q13': ['subconsulta que devolve lista', 'NOT IN'],
    'Q14': ['JOIN pela associativa', 'AVG', 'DATEDIFF', 'FLOOR', 'ROUND'],
    'Q15': ['autojunção', 'DATEDIFF', 'DATE_FORMAT'],
    'Q16': ['NOT IN com subconsulta', 'GROUP BY', 'MAX', 'HAVING'],
    'Q17': ['RIGHT JOIN', 'COUNT(coluna)', 'GROUP BY'],
}
# Quebras só de exibição (o SQL é o mesmo; muda a linha para caber a 24 px).
QUEBRAS = {'Q16': ('NOT IN (SELECT retifica_id FROM evolucao WHERE', 'NOT IN (SELECT retifica_id FROM evolucao\n{ind}WHERE')}


notas._PARTES_TXT = {n: oque for n, _c, _i, _f, _n, oque in PARTES}


def bloco_da_consulta(num):
    n = int(num[1:])
    for a, b, cor, _ini, _fim in BLOCOS:
        if int(a[1:]) <= n <= int(b[1:]):
            return f'{a} a {b}', cor
    raise ValueError(num)


# ------------------------------------------------------------------ SQL
PALAVRAS = set('''SELECT FROM WHERE JOIN LEFT RIGHT INNER OUTER ON GROUP BY HAVING ORDER LIMIT AS AND OR NOT IN IS NULL
BETWEEN LIKE DISTINCT CASE WHEN THEN ELSE END ASC DESC UNION EXISTS INTERVAL DAY TRUE FALSE INSERT INTO VALUES
UPDATE SET DELETE CREATE TABLE DATABASE DROP IF ALTER ADD CONSTRAINT PRIMARY KEY FOREIGN REFERENCES UNIQUE DEFAULT
AUTO_INCREMENT CASCADE USE ENUM INT VARCHAR TEXT DATE DATETIME BOOLEAN CURRENT_TIMESTAMP CHARACTER COLLATE'''.split())
FUNCOES = set('COUNT SUM AVG MIN MAX ROUND FLOOR DATEDIFF DATE_FORMAT CURDATE ADDDATE YEAR MONTH TIMESTAMPDIFF CONCAT COALESCE IFNULL NOW'.split())
TOKEN = re.compile(r"(--[^\n]*)|('(?:[^'\\]|\\.)*')|(\b\d+(?:[.,]\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+)|(.)", re.S)


def colorir(sql):
    saida = []
    for m in TOKEN.finditer(sql):
        com, txt, num, pal, esp, outro = m.groups()
        if com:
            saida.append(f'<span class="k-com">{e(com)}</span>')
        elif txt:
            saida.append(f'<span class="k-txt">{e(txt)}</span>')
        elif num:
            saida.append(f'<span class="k-num">{num}</span>')
        elif pal:
            alto = pal.upper()
            classe = 'k-fn' if alto in FUNCOES else 'k-kw' if alto in PALAVRAS else ''
            saida.append(f'<span class="{classe}">{e(pal)}</span>' if classe else e(pal))
        else:
            saida.append(e(esp or outro))
    return ''.join(saida)


def compactar(sql, num=None):
    """Tira o alinhamento largo do script (só espaços) e realinha os AS de cada bloco."""
    if num in QUEBRAS:
        velho, novo = QUEBRAS[num]
        for linha in sql.split('\n'):
            if velho in linha:
                ind = ' ' * (linha.index('(SELECT') + 1)
                sql = sql.replace(velho, novo.format(ind=ind))
    linhas = []
    for linha in sql.strip('\n').split('\n'):
        ind = len(linha) - len(linha.lstrip(' '))
        partes = re.split(r"('(?:[^'\\]|\\.)*')", linha.strip())
        corpo = ''.join(p if i % 2 else re.sub(r' {2,}', ' ', p) for i, p in enumerate(partes))
        linhas.append(' ' * ind + corpo)
    padrao = re.compile(r'^(.*?\S) AS (\w+.*)$')
    i = 0
    while i < len(linhas):
        j = i
        while j < len(linhas) and padrao.match(linhas[j]) and not linhas[j].lstrip().startswith(('FROM', 'WHERE')):
            j += 1
        if j - i > 1:
            pares = [padrao.match(linhas[k]).groups() for k in range(i, j)]
            larg = max(len(a) for a, _ in pares)
            for k, (a, b) in zip(range(i, j), pares):
                linhas[k] = a.ljust(larg) + ' AS ' + b
        i = max(j, i + 1)
    return linhas


ORDEM = [('FROM', 1), ('LEFT JOIN', 1), ('RIGHT JOIN', 1), ('INNER JOIN', 1), ('JOIN', 1), ('WHERE', 2),
         ('GROUP BY', 3), ('HAVING', 4), ('SELECT', 5), ('ORDER BY', 6)]
COR_ETAPA = {1: CIANO, 2: AMARELO, 3: VERDE, 4: VERDE, 5: MAGENTA, 6: ROXO}


def etapa(n):
    c = COR_ETAPA[n]
    return f'<span class="et" style="background:{c};color:{TEXTO_SOBRE[c]}">{n}</span>'


def sql_com_ordem(linhas):
    """Cada cláusula do SELECT externo ganha o número da etapa em que o MySQL a processa."""
    saida, prof = [], 0
    for linha in linhas:
        topo = linha.strip().upper()
        n = None
        if prof == 0:
            for chave, k in ORDEM:
                if topo.startswith(chave + ' ') or topo == chave:
                    n = k
                    break
        marca = etapa(n) if n else '<span class="et vazio"></span>'
        saida.append(f'<div class="ln">{marca}<code>{colorir(linha)}</code></div>')
        prof += linha.count('(') - linha.count(')')
    return ''.join(saida)


# ------------------------------------------------------------------ dicionário a partir do 01
def tabelas_do_ddl():
    tabelas = []
    for nome, corpo in re.findall(r'CREATE TABLE (\w+) \((.*?)\n\);', SQL01, re.S):
        colunas, pk, fks, uq = [], [], set(), set()
        # Junta as linhas (uma definição pode ocupar duas) e separa pelas vírgulas fora de parênteses.
        texto = ' '.join(l.split('--')[0].strip() for l in corpo.split('\n'))
        defs, prof, atual = [], 0, ''
        for ch in texto:
            prof += (ch == '(') - (ch == ')')
            if ch == ',' and prof == 0:
                defs.append(atual)
                atual = ''
            else:
                atual += ch
        defs.append(atual)
        for s in defs:
            s = re.sub(r'\s+', ' ', s).strip()
            if not s:
                continue
            m = re.match(r'(?:CONSTRAINT \w+ )?PRIMARY KEY \(([^)]+)\)', s)
            if m:
                pk = [c.strip() for c in m.group(1).split(',')]
                continue
            m = re.match(r'(?:CONSTRAINT \w+ )?FOREIGN KEY \((\w+)\)', s)
            if m:
                fks.add(m.group(1))
                continue
            m = re.match(r'(?:CONSTRAINT \w+ )?UNIQUE \((\w+)\)', s)
            if m:
                uq.add(m.group(1))
                continue
            if s.upper().startswith(('ON ', 'CONSTRAINT', 'REFERENCES')):
                continue
            m = re.match(r'(\w+)\s+(ENUM\([^)]*\)|\w+(?:\(\d+\))?)(.*)', s)
            if m:
                resto = m.group(3).upper()
                colunas.append({'nome': m.group(1), 'tipo': m.group(2), 'nulo': 'NOT NULL' not in resto and 'PRIMARY' not in resto})
        if nome == 'evolucao' and 'uq_evolucao_retifica' in SQL01:  # o ALTER TABLE do 1:1
            fks.add('retifica_id')
            uq.add('retifica_id')
        tabelas.append({'nome': nome, 'colunas': colunas, 'pk': pk, 'fk': fks, 'uq': uq})
    return tabelas


def tipo_curto(tipo):
    return 'ENUM' if tipo.upper().startswith('ENUM') else tipo.upper()


def selos(c, t):
    s = ''
    if c['nome'] in t['pk']:
        s += '<b class="sl pk">PK</b>'
    if c['nome'] in t['fk']:
        s += '<b class="sl fk">FK</b>'
    if c['nome'] in t['uq']:
        s += '<b class="sl uq">UQ</b>'
    return s


def cartao_tabela(t, classe=''):
    linhas = ''
    for c in t['colunas']:
        nulo = ' <span class="nulo">NULL</span>' if c['nulo'] and c['nome'] not in t['pk'] else ''
        linhas += (f'<div class="sc-l"><span class="sc-s">{selos(c, t)}</span><span class="sc-n">{c["nome"]}</span>'
                   f'<span class="sc-t">{tipo_curto(c["tipo"])}{nulo}</span></div>')
    return f'<div class="schema {classe}" style="--c:{COR_TABELA[t["nome"]]}"><div class="sc-nome">{t["nome"]}</div>{linhas}</div>'


# ------------------------------------------------------------------ peças
def barra4(classe=''):
    return f'<div class="barra4 {classe}" aria-hidden="true">' + ''.join(f'<i style="background:{c}"></i>' for c in BARRA4) + '</div>'


def seta(cor=ROXO):
    return (f'<svg class="seta" viewBox="0 0 56 24" width="56" height="24" aria-hidden="true">'
            f'<path d="M2 12H50M40 3l10 9-10 9" fill="none" stroke="{cor}" stroke-width="3.5"/></svg>')


def titulo(texto, num=None):
    n = f'<span class="qnum">{num}</span>' if num else ''
    return f'<h2 class="titulo">{n}<span>{texto}</span></h2>'


SLIDES = []


def slide(corpo, classe='', secao='', pessoa=None, notas='', ident=None, rotulo=''):
    SLIDES.append({'corpo': corpo, 'classe': classe, 'secao': secao, 'pessoa': pessoa, 'notas': notas, 'id': ident, 'rotulo': rotulo})


# ------------------------------------------------------------------ medidas para o layout das consultas
# Fonte do SQL e do resultado escolhida por slide: a maior (até 30 px) em que tudo cabe; nunca abaixo de 24 px.
LARG = 1728        # 1920 menos as margens de 96 px
ALTURA_CORPO = 800  # do fim do título até perto do rodapé


def larguras_tabela(colunas, linhas, disponivel, r):
    num = [bool(linhas) and all(re.fullmatch(r'-?\d+(?:[.,]\d+)?', str(l[i])) for l in linhas) for i in range(len(colunas))]
    minimo = [len(c) * 0.62 * r + 38 for c in colunas]
    natural = [max(minimo[i], max([len(str(l[i])) for l in linhas] or [0]) * 0.56 * r + 38) for i in range(len(colunas))]
    w = natural[:]
    piso = [w[i] if num[i] else max(minimo[i], 11 * r) for i in range(len(w))]
    while sum(w) > disponivel:  # encolhe por igual as colunas de texto mais largas
        candidatas = [k for k in range(len(w)) if w[k] - piso[k] > 0.5]
        if not candidatas:
            break
        j = max(candidatas, key=lambda k: w[k])
        w[j] -= min(4, sum(w) - disponivel, w[j] - piso[j])
    return [round(x) for x in w], num, natural


def tabela_resultado(colunas, linhas, disponivel, altura_max, r):
    """Tabela do resultado: texto longo quebra linha (nada cortado); mostra as linhas que cabem na altura."""
    w, num, natural = larguras_tabela(colunas, linhas, disponivel, r)
    lh = 1.42 * r
    cg = ''.join(f'<col style="width:{x}px">' for x in w)
    cab = ''.join(f'<th class="{"n" if num[i] else ""}">{e(c)}</th>' for i, c in enumerate(colunas))
    corpo, usada, mostradas = '', lh + 18, 0
    for l in linhas[:9]:
        n_linhas = max([1] + [math.ceil(len(str(v)) * 0.56 * r * 1.08 / (w[i] - 28)) for i, v in enumerate(l) if w[i] < natural[i] - 1])
        h = n_linhas * lh + 11
        if usada + h > altura_max and mostradas >= 2:
            break
        usada += h
        mostradas += 1
        corpo += '<tr>' + ''.join(f'<td class="{"n" if num[i] else ""}">{e(str(v))}</td>' for i, v in enumerate(l)) + '</tr>'
    html_ = f'<table class="res" style="width:{sum(w)}px"><colgroup>{cg}</colgroup><thead><tr>{cab}</tr></thead><tbody>{corpo}</tbody></table>'
    return html_, mostradas, usada


def altura_chips(chips, largura):
    linhas, x = 1, 0
    for c in chips:
        w = len(c) * 14.4 + 32 + 12
        if x + w > largura and x > 0:
            linhas += 1
            x = 0
        x += w
    return linhas * 52 - 12


def altura_texto(texto, largura, px=26):
    return math.ceil(len(texto) * 0.54 * px / max(largura - 28, 1)) * px * 1.4


def plano_consulta(q, s):
    """Monta a consulta com o SQL em s px. Devolve (html, cabe_tudo, altura estimada)."""
    num = q['num']
    r = min(s, 28)
    linhas_sql = compactar(q['sql'], num)
    sql_w = round(max(len(l) for l in linhas_sql) * 0.6 * s + 1.6 * s + 16 + 48 + 8)
    sql_h = len(linhas_sql) * 1.5 * s + 48
    chips, resumo = CHIPS_Q[num], RESUMO[num]
    _, _, natural = larguras_tabela(q['colunas'], q['linhas'], 99999, r)
    lado_w = LARG - sql_w - 48
    total = len(q['linhas'])
    chips_html = ''.join(f'<span class="cmd">{e(c)}</span>' for c in chips)
    estilo = f'grid-template-columns:{sql_w}px 1fr;--fs:{s}px;--fr:{r}px'
    nota_h = 12 + 34

    def nota_res(mostra):
        mais = f'+ {total - mostra} linhas · ' if total > mostra else ''
        return f'<p class="q-nota">{mais}Dados fictícios · MySQL 8.4 com a data fixa de 30/11/2026</p>'

    if sql_w > LARG:
        return '', False, 99999
    if sum(natural) <= lado_w:  # SQL à esquerda; recursos, explicação e resultado à direita
        topo = altura_chips(chips, lado_w) + 24 + altura_texto(resumo, lado_w) + 24
        tab, mostra, tab_h = tabela_resultado(q['colunas'], q['linhas'], lado_w, ALTURA_CORPO - topo - nota_h, r)
        altura = max(sql_h, topo + tab_h + nota_h)
        html_ = (f'<div class="q-corpo lado" style="{estilo}"><div class="sql">{sql_com_ordem(linhas_sql)}</div>'
                 f'<div class="q-lado"><div class="chips">{chips_html}</div><p class="q-resumo">{e(resumo)}</p>'
                 f'<div class="q-res">{tab}{nota_res(mostra)}</div></div></div>')
    else:  # SQL em cima; resultado embaixo em toda a largura
        com_lado = lado_w >= 420
        if com_lado:
            topo = max(sql_h, altura_chips(chips, lado_w) + 24 + altura_texto(resumo, lado_w))
            lado = f'<div class="q-lado"><div class="chips">{chips_html}</div><p class="q-resumo">{e(resumo)}</p></div>'
        else:
            topo = sql_h + 28 + altura_chips(chips, LARG)
            lado = f'<div class="chips largo">{chips_html}</div>'
        tab, mostra, tab_h = tabela_resultado(q['colunas'], q['linhas'], LARG, ALTURA_CORPO - topo - 28 - nota_h, r)
        altura = topo + 28 + tab_h + nota_h
        html_ = (f'<div class="q-corpo pilha" style="{estilo}"><div class="sql">{sql_com_ordem(linhas_sql)}</div>{lado}'
                 f'<div class="q-res largo">{tab}{nota_res(mostra)}</div></div>')
    return html_, mostra == min(total, 9) and altura <= ALTURA_CORPO, altura


def passos_da_consulta(q):
    """As cláusulas do SELECT externo, na ordem em que o MySQL as processa."""
    blocos, prof = [], 0
    for linha in compactar(q['sql'], q['num']):
        topo = linha.strip().upper()
        achou = None
        if prof == 0:
            for chave, k in ORDEM:
                if topo.startswith(chave + ' ') or topo == chave:
                    achou = (k, chave)
                    break
        if achou:
            blocos.append([achou[0], achou[1], linha.strip()])
        elif blocos:
            blocos[-1][2] += ' ' + linha.strip()
        prof += linha.count('(') - linha.count(')')
    saida = [(n, k, re.sub(r'\s+', ' ', txt[len(k):]).strip().rstrip(';')) for n, k, txt in blocos]
    return sorted(saida, key=lambda x: x[0])


def dados_da_consulta(q):
    n = len(q['linhas'])
    prim = ', '.join(f'{c} = {v}' for c, v in list(zip(q['colunas'], q['linhas'][0]))[:6]) if n else ''
    res = (f'{n} linha{"s" if n > 1 else ""} (dados fictícios, data de 30/11/2026). Primeira linha: {prim}.' if n else 'Nenhuma linha.')
    return {'enunciado': q['enunciado'], 'passos': passos_da_consulta(q), 'resultado': res, 'chips': CHIPS_Q[q['num']]}


def slide_consulta(q):
    num = q['num']
    for s in (30, 28, 26, 24):
        corpo, cabe, _ = plano_consulta(q, s)
        if cabe:
            break
    else:
        corpo, _, _ = plano_consulta(q, 24)
    notas = ''
    slide(titulo(e(TITULO_Q[num]), num) + corpo, 'q', 'Consultas', None, notas, ident=num.lower(), rotulo=f'{num}: {TITULO_Q[num]}')
    SLIDES[-1]['q'] = q


# ------------------------------------------------------------------ DER para o telão (atributos ficam na notação e no dicionário)
def der_deck():
    W, H = 1728, 790
    ent = {  # canto superior esquerdo; caixas de 280 x 88
        'REUNIÃO': (724, 0), 'DEMANDA': (724, 300), 'USUÁRIO': (0, 300), 'ASSISTIDO': (1448, 300), 'EVOLUÇÃO': (1010, 600),
    }
    p = []

    def caixa(nome):
        x, y = ent[nome]
        p.append(f'<rect x="{x}" y="{y}" width="280" height="88" class="ent"/><rect x="{x}" y="{y}" width="280" height="10" class="ent-t"/>'
                 f'<text x="{x + 140}" y="{y + 60}" class="ent-n">{nome}</text>')

    def linha(*pts):
        p.append('<polyline class="lig" points="' + ' '.join(f'{a},{b}' for a, b in pts) + '"/>')

    def losango(cx, cy, nome, w=230, h=88):
        p.append(f'<polygon class="rel" points="{cx - w / 2},{cy} {cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2}"/>'
                 f'<text x="{cx}" y="{cy + 9}" class="rel-n">{nome}</text>')

    def card(x, y, t, ancora='start'):
        p.append(f'<text x="{x}" y="{y}" class="card" text-anchor="{ancora}">{t}</text>')

    for n in ent:
        caixa(n)
    # origina: Reunião (1,1) e Demanda (0,N)
    linha((864, 88), (864, 300)); losango(864, 194, 'origina', 200, 84)
    card(880, 128, '(0,N)'); card(880, 284, '(1,1)')
    # responde por: Usuário (1,1) e Demanda (0,N)
    linha((280, 344), (724, 344)); losango(502, 344, 'responde por', 250, 88)
    card(290, 330, '(0,N)'); card(714, 330, '(1,1)', 'end')
    # refere-se a: Assistido (0,1) e Demanda (0,N)
    linha((1004, 344), (1448, 344)); losango(1226, 344, 'refere-se a', 236, 88)
    card(1014, 330, '(0,1)'); card(1438, 330, '(0,N)', 'end')
    # acompanha: Usuário (0,N) e Assistido (0,N), com data_inicio
    linha((180, 388), (180, 500), (1548, 500), (1548, 388)); losango(864, 500, 'acompanha', 236, 88)
    linha((864, 544), (864, 566))
    p.append('<circle cx="864" cy="574" r="8" class="at"/><text x="884" y="583" class="att">data_inicio</text>')
    card(194, 428, '(0,N)'); card(1534, 428, '(0,N)', 'end')
    # possui: Assistido (1,1) e Evolução (0,N)
    linha((1690, 388), (1690, 644), (1290, 644)); losango(1500, 644, 'possui', 190, 80)
    card(1676, 428, '(0,N)', 'end'); card(1300, 630, '(1,1)')
    # escreve: Usuário (1,1) e Evolução (0,N)
    linha((60, 388), (60, 644), (1010, 644)); losango(560, 644, 'escreve', 190, 80)
    card(74, 428, '(0,N)'); card(1000, 630, '(1,1)', 'end')
    # retifica: Evolução (0,1) e Evolução (0,1), autorrelacionamento 1:1
    linha((1060, 688), (1060, 744), (1065, 744)); linha((1235, 744), (1240, 744), (1240, 688))
    losango(1150, 744, 'retifica', 170, 76)
    card(1046, 722, '(0,1)', 'end'); card(1254, 722, '(0,1)')
    p.append('<text x="1046" y="774" class="papel" text-anchor="end">versão corrigida</text>')
    p.append('<text x="1254" y="774" class="papel">nova versão</text>')
    return f'<svg class="der-svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="DER do recorte: 5 entidades e 7 relacionamentos">{"".join(p)}</svg>'


# ------------------------------------------------------------------ os slides
def montar():
    logo = ler(AQUI, 'assets', 'logos', 'crie-logo-vetor.svg').replace('<svg ', '<svg class="logo-crie" role="img" aria-label="CRIE, Centro de Integração Especial" ', 1)
    ifsp = re.sub(r'<\?xml[^>]*>', '', ler(AQUI, 'assets', 'logos', 'ifsp-marca-horizontal-2015.svg'))
    ifsp = ifsp.replace('<svg ', '<svg class="logo-ifsp" role="img" aria-label="Instituto Federal de São Paulo" ', 1)
    tabelas = {t['nome']: t for t in tabelas_do_ddl()}

    # 1. Capa (faixa clara com a marca, como o cabeçalho do site; área escura, como o hero)
    slide(f'''<div class="capa-topo"><div class="lockup">{logo}<span>Centro de Integração<br>Especial</span></div>{ifsp}</div>
<div class="capa-hero"><div class="capa-txt">{barra4()}
<h1>O banco de dados das demandas do CRIE</h1>
<p class="capa-sub">Projeto interdisciplinar de Banco de Dados I: do minimundo às 17 consultas em MySQL.</p>
<p class="capa-equipe">Equipe Cortex</p>
<p class="capa-rod">IFSP Bragança Paulista · ADS, 2º semestre · 30/11/2026</p></div>
<figure class="capa-fig">{cartao_tabela(tabelas["demanda"], "escuro")}<figcaption>A tabela central do recorte, como o script 01 a cria</figcaption></figure></div>''',
          'capa escuro', 'Abertura', 'Vinícius', 'Apresentar a equipe Cortex, o parceiro (CRIE) e o que vamos mostrar: modelagem, scripts e 17 consultas.',
          ident='capa', rotulo='Capa')

    # 2. Roteiro
    def seg(t):
        m, s = t.split(':')
        return int(m) * 60 + int(s)
    blocos = ''
    for n, cor, ini, fim, nome, oque in PARTES:
        if n == 3:  # a parte das consultas mostra os blocos de cada integrante
            faixa = (f'<span style="flex:60;background:{MAGENTA};color:#fff">Mapa</span>' +
                     ''.join(f'<span style="flex:{seg(f) - seg(i)};background:{c};color:{TEXTO_SOBRE[c]}">{a} a {b[1:]}</span>'
                             for a, b, c, i, f in BLOCOS))
            blocos += (f'<div class="bloco p3" style="flex:{seg(fim) - seg(ini)}"><div class="p3-cab"><span class="b-t">{ini}</span>'
                       f'<b>{n:02d}</b><span class="b-o">{e(nome)}</span></div><div class="p3-faixa">{faixa}</div></div>')
            continue
        blocos += (f'<div class="bloco" style="flex:{seg(fim) - seg(ini)};background:{cor};color:{TEXTO_SOBRE[cor]}">'
                   f'<span class="b-t">{ini}</span><b>{n:02d}</b><span class="b-o">{e(nome)}</span></div>')
    itens = ''.join(f'<li><span class="r-cor" style="background:{c}"></span><b>{n:02d} · {e(nome)}</b><span>{e(o)}</span><em>{ini} a {fim}</em></li>'
                    for n, c, ini, fim, nome, o in PARTES)
    slide(titulo('Roteiro: 20 minutos, cinco partes') + f'<div class="linha-tempo">{blocos}</div><ul class="roteiro">{itens}</ul>'
          '<p class="nota-baixo">Na parte 3, cada integrante explica 3 ou 4 consultas: Q01 a 03, Q04 a 06, Q07 a 10, Q11 a 14 e Q15 a 17.</p>',
          '', 'Abertura', 'Vinícius', 'Cada integrante apresenta um bloco e explica o processamento das próprias consultas, como pede o enunciado.',
          ident='roteiro', rotulo='Roteiro')

    # 3. O CRIE e o problema
    setores = ''.join(f'<li style="--c:{c}"><b>{n}</b></li>' for n, c in (('Pedagógico', MAGENTA), ('Saúde', AMARELO), ('Serviço de convivência', CIANO)))
    garantias = [('Origem', 'cada demanda nasce em uma reunião'), ('Andamento', 'cinco estados, e toda demanda nasce aberta'),
                 ('Histórico', 'evolução não se apaga; corrige-se com nova versão')]
    g = ''.join(f'<div class="gar"><b>{a}</b><span>{e(b)}</span></div>' for a, b in garantias)
    slide(titulo('O CRIE e o problema') + f'''<div class="crie">
<div class="crie-esq"><p class="lead">O CRIE atende pessoas com deficiência em Extrema (MG). Cada setor faz uma reunião semanal de equipe.</p>
<ul class="setores">{setores}</ul></div>
<div class="crie-dir"><div class="bloco-tinta"><b>Demandas de articulação</b>
<p>O que a instituição não resolve sozinha: providências com famílias e com a rede pública, como CRAS, unidades de saúde, escolas e Conselho Tutelar.</p></div>
<p class="g-tit">O banco precisa garantir</p><div class="gars">{g}</div></div></div>''',
          '', 'Universo de discurso', 'Vinícius', 'O minimundo: três setores, reuniões semanais e as demandas que dependem da rede. O banco garante origem, andamento e histórico.',
          ident='crie', rotulo='O CRIE e o problema')

    # 4. Regras do minimundo viram restrições
    regras = [
        ('Toda demanda nasce numa reunião', 'reuniao_id INT NOT NULL + FOREIGN KEY'),
        ('O estado tem 5 valores; toda demanda nasce aberta', "ENUM(...) NOT NULL DEFAULT 'aberta'"),
        ('Um responsável e, no máximo, um assistido', 'responsavel_id NOT NULL · assistido_id NULL'),
        ('E-mail único; senha só como hash', 'UNIQUE (email) · senha_hash VARCHAR(255)'),
        ('Do assistido, só o nome de tratamento (LGPD)', 'nome_tratamento VARCHAR(120)'),
        ('Evolução não se apaga: corrige-se com nova versão', 'retifica_id + UNIQUE + FK para evolucao'),
    ]
    linhas = ''.join(f'<div class="regra"><p>{e(r)}</p>{seta()}<code>{colorir(c)}</code></div>' for r, c in regras)
    slide(titulo('Cada regra do minimundo vira uma restrição') + f'<div class="regras">{linhas}</div>',
          '', 'Universo de discurso', 'Vinícius', 'Quem garante a regra é o próprio MySQL, não a boa vontade de quem digita.',
          ident='regras', rotulo='Regras e restrições')

    # 5. Recorte
    chips = ''.join(f'<span class="tab-chip" style="--c:{COR_TABELA[n]}">{n}</span>' for n, _ in CARGA)
    fora = ''.join(f'<li>{e(x)}</li>' for x in ('Serviço da Rede', 'Encaminhamento', 'Ação', 'Retorno de Acompanhamento', 'Histórico de Demanda', 'Registro de Auditoria'))
    slide(titulo('O recorte: 13 entidades no DER, 6 tabelas no banco') + f'''<div class="recorte">
<div class="rec-esq"><div class="num-grande"><div><span>13</span><small>entidades no DER<br>do sistema (v2.0)</small></div>{seta(MAGENTA)}
<div><span class="seis">6</span><small>tabelas nesta disciplina<br>(o enunciado pede de 4 a 6)</small></div></div>
<p class="conta"><b>5</b> viraram tabelas · <b>2</b> viraram colunas · <b>6</b> ficaram fora</p></div>
<div class="rec-dir"><h3>Viraram tabelas: 5 entidades e a associativa do N:N</h3><div class="chips-tab">{chips}</div>
<h3>Viraram colunas</h3><ul class="fora"><li>Setor: <code>reuniao.setor</code> (ENUM)</li><li>Categoria de Demanda: <code>demanda.categoria</code></li></ul>
<h3>Ficaram fora</h3><ul class="fora duas-col">{fora}</ul></div></div>''',
          '', 'Universo de discurso', 'Vinícius', 'Escolhemos o núcleo do sistema. O resto do DER continua no sistema, fora desta entrega.',
          ident='recorte', rotulo='Recorte')

    def divisor(parte):
        n, cor, ini, fim, nome, oque = parte
        slide(f'''{barra4()}<div class="div-corpo"><span class="div-num" style="color:{NO_ESCURO.get(cor, cor)}">0{n}</span>
<div><h2>{e(nome)}</h2><p>{e(oque)}</p><div class="div-pessoa"><i style="background:{cor}"></i><b>Parte {n}</b><em>{ini} a {fim}</em></div></div></div>''',
              'divisor escuro', nome, None, '', ident=f'parte{n}', rotulo=f'Parte {n}: {nome}')
        SLIDES[-1]['parte_n'] = n

    divisor(PARTES[1])

    # DER
    slide(titulo('DER do recorte') + f'<div class="der">{der_deck()}<div class="der-leitura"><b>Como ler (Aula 02)</b>'
          '<p>O par (mín, máx) junto a cada entidade diz de quantas ocorrências do relacionamento cada ocorrência dela participa.</p>'
          '<p>Em origina: DEMANDA (1,1), cada demanda nasce em uma só reunião; REUNIÃO (0,N), uma reunião origina nenhuma ou várias.</p></div></div>',
          'der-slide', 'Modelagem', 'Henry', 'Ler pelos verbos: reunião origina demanda; usuário responde por demanda; usuário acompanha assistido (N:N, com data_inicio); evolução retifica evolução (1:1).',
          ident='der', rotulo='DER')

    # Relacionamentos
    cor_tipo = {'1:N': CIANO, '1:N (opcional)': CIANO, 'N:N': AMARELO, '1:1': MAGENTA}
    linhas = ''
    for verbo, ents, tipo, card, impl in RELACIONAMENTOS:
        c = cor_tipo.get(tipo, CIANO)
        linhas += (f'<tr><td><b>{e(verbo)}</b></td><td>{e(ents)}</td><td><span class="tipo" style="background:{c};color:{TEXTO_SOBRE[c]}">{e(tipo)}</span></td>'
                   f'<td class="impl">{e(impl)}</td></tr>')
    slide(titulo('Os 7 relacionamentos e como ficam no banco') +
          f'<table class="tab rel"><thead><tr><th>Relacionamento</th><th>Entidades</th><th>Tipo</th><th>No banco</th></tr></thead><tbody>{linhas}</tbody></table>'
          '<div class="dupla"><p><b>N:N</b> vira a tabela associativa assistido_profissional, com chave primária composta.</p>'
          '<p><b>1:1</b> é o UNIQUE em retifica_id: sem ele, uma versão poderia ser corrigida várias vezes (1:N).</p></div>',
          '', 'Modelagem', 'Henry', 'O enunciado pede os três tipos: 1:N (cinco deles), N:N (acompanha) e 1:1 (retifica).',
          ident='rel', rotulo='Relacionamentos')

    # Notação textual
    notacao = [
        ('Usuario', [('id', 'pk'), ('nome', ''), ('email', ''), ('senha_hash', ''), ('perfil', ''), ('ativo', ''), ('criado_em', '')]),
        ('Assistido', [('id', 'pk'), ('nome_tratamento', ''), ('ativo', ''), ('criado_em', '')]),
        ('AssistidoProfissional', [('assistido_id', 'pk fk'), ('profissional_id', 'pk fk'), ('data_inicio', '')]),
        ('Reuniao', [('id', 'pk'), ('data', ''), ('setor', ''), ('criado_em', '')]),
        ('Demanda', [('id', 'pk'), ('descricao', ''), ('categoria', ''), ('prioridade', ''), ('prazo', ''), ('estado', ''),
                     ('responsavel_id', 'fk'), ('reuniao_id', 'fk'), ('assistido_id', 'fk'), ('criado_em', ''), ('atualizado_em', '')]),
        ('Evolucao', [('id', 'pk'), ('assistido_id', 'fk'), ('profissional_id', 'fk'), ('data', ''), ('area_atuacao', ''),
                      ('descricao', ''), ('ocorrido_em', ''), ('retifica_id', 'fk')]),
    ]
    linhas = ''.join(f'<p><b>{tab}</b> (' + ', '.join(f'<span class="{t}">{c}</span>' if t else c for c, t in cols) + ')</p>' for tab, cols in notacao)
    slide(titulo('Notação textual do modelo relacional') + f'<div class="notacao">{linhas}</div>'
          '<p class="nota-baixo"><span class="pk">sublinhado</span> = chave primária · <span class="fk">itálico em roxo</span> = chave estrangeira · '
          'em AssistidoProfissional a chave é composta pelas duas chaves estrangeiras</p>',
          '', 'Modelagem', 'Henry', 'Mostrar a chave composta da associativa e as três chaves estrangeiras da demanda.',
          ident='notacao', rotulo='Notação textual')

    # Normalização
    fns = [('1FN', CIANO, 'Atributos atômicos, sem grupos repetidos. Os profissionais de um assistido viram linhas de assistido_profissional, não uma lista.'),
           ('2FN', AMARELO, 'A única chave composta é (assistido_id, profissional_id), e data_inicio depende dela inteira. As outras chaves são simples.'),
           ('3FN', MAGENTA, 'Sem dependência transitiva: o setor da demanda vem da reunião pela junção (Q09), não é copiado. Nada calculado é guardado.')]
    cards = ''.join(f'<div class="card-c" style="--c:{c}"><span class="fn">{n}</span><p>{e(t)}</p></div>' for n, c, t in fns)
    slide(titulo('Normalizado até a 3ª forma normal') + f'<div class="tres">{cards}</div>',
          '', 'Modelagem', 'Henry', 'Exemplo que convence: o setor não está na demanda; vem da reunião. Dias de atraso e médias são calculados nas consultas.',
          ident='fn', rotulo='Normalização')

    # Dicionário
    ordem = ['demanda', 'evolucao', 'usuario', 'assistido', 'reuniao', 'assistido_profissional']
    cartoes = ''.join(cartao_tabela(tabelas[n]) for n in ordem)
    slide(titulo('As 6 tabelas como o script 01 as cria') + f'<div class="schemas">{cartoes}</div>'
          '<p class="nota-baixo">Tipos numérico (INT, BOOLEAN), texto (VARCHAR, TEXT, ENUM) e data (DATE, DATETIME) · lido do 01_criacao_banco.sql</p>',
          'denso', 'Modelagem', 'Henry', 'O enunciado pede tipos numérico, texto e data: estão todos aqui. PK, FK e UQ marcam as chaves.',
          ident='dic', rotulo='Dicionário de dados')

    # Script 01
    trecho = '''DROP DATABASE IF EXISTS crie_demandas;
CREATE DATABASE crie_demandas DEFAULT CHARACTER SET utf8mb4;

CREATE TABLE demanda (
  id         INT  NOT NULL AUTO_INCREMENT,
  prioridade ENUM('baixa', 'media', 'alta') NOT NULL,
  prazo      DATE NOT NULL,
  estado     ENUM(...) NOT NULL DEFAULT 'aberta',
  reuniao_id INT  NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (reuniao_id) REFERENCES reuniao (id)
);

ALTER TABLE evolucao
  ADD CONSTRAINT uq_evolucao_retifica UNIQUE (retifica_id),
  ADD CONSTRAINT fk_evolucao_retifica
      FOREIGN KEY (retifica_id) REFERENCES evolucao (id);'''
    anot = [('DROP e CREATE DATABASE', 'roda do zero quantas vezes for preciso'),
            ('ENUM com DEFAULT', "domínio fechado; nasce 'aberta'"),
            ('FOREIGN KEY NOT NULL', 'não existe demanda sem reunião'),
            ('ALTER TABLE', 'FK para a própria tabela; o UNIQUE faz o 1:1')]
    lista = ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in anot)
    slide(titulo('Script 01: criação do banco') + f'<div class="codigo"><pre class="sql-pre">{colorir(trecho)}</pre><ul class="anot">{lista}</ul></div>'
          '<p class="nota-baixo">Trecho resumido da tabela demanda; o script completo cria as 6 tabelas e roda do zero no MySQL 8.4.</p>',
          '', 'Scripts', 'Henry', 'DROP e CREATE DATABASE, CREATE TABLE com ENUM e DEFAULT e o ALTER TABLE que faz o 1:1.',
          ident='s01', rotulo='Script 01')

    # Script 02
    maior = max(n for _, n in CARGA)
    barras = ''.join(f'<div class="barra"><span class="bn">{t}</span><span class="bb"><i style="width:{n / maior * 100:.1f}%;background:{COR_TABELA[t]}"></i></span><b>{n}</b></div>' for t, n in CARGA)
    q09 = next(q for q in CONSULTAS if q['num'] == 'Q09')
    por_setor = {}
    for l in q09['linhas']:
        por_setor.setdefault(l[0], []).append((l[1], int(l[2])))
    cor_estado = {'aberta': CIANO, 'em_andamento': ROXO, 'aguardando_terceiros': AMARELO, 'concluida': VERDE, 'cancelada': MAGENTA}
    pilhas = ''
    for setor, itens in por_setor.items():
        partes = ''.join(f'<span style="flex:{n};background:{cor_estado[est]};color:{TEXTO_SOBRE[cor_estado[est]]}">{n}</span>' for est, n in itens)
        pilhas += f'<div class="pilha"><b>{e(setor)}</b><div class="pilha-b">{partes}</div></div>'
    leg = ''.join(f'<span><i style="background:{c}"></i>{e(n.replace("_", " "))}</span>' for n, c in cor_estado.items())
    slide(titulo('Script 02: 103 registros fictícios') + f'''<div class="carga">
<div><h3>Registros por tabela</h3><div class="barras">{barras}</div></div>
<div><h3>Demandas por setor e estado (Q09)</h3>{pilhas}<div class="leg">{leg}</div></div></div>
<p class="nota-baixo">A carga tem os 5 estados, as 3 prioridades e prazos vencidos, próximos e futuros, para toda consulta ter resultado.</p>''',
          '', 'Scripts', 'Henry', 'A diversidade da carga é o que faz cada consulta mostrar algo: estados, prioridades, prazos e assistidos sem demanda.',
          ident='s02', rotulo='Script 02')

    divisor(PARTES[2])

    # Mapa das consultas
    recursos = [('Texto', lambda s: 'LIKE' in s), ('IN / BETWEEN', lambda s: ' IN (' in s or 'BETWEEN' in s),
                ('Datas', lambda s: any(f in s for f in ('CURDATE', 'DATEDIFF', 'DATE_FORMAT', 'ADDDATE', 'YEAR(', 'MONTH(', 'TIMESTAMPDIFF'))),
                ('Cálculo', lambda s: any(f in s for f in ('ROUND(', 'FLOOR(', 'AVG(', 'SUM(', '* 100', ' / '))),
                ('JOIN', lambda s: 'JOIN' in s), ('GROUP BY', lambda s: 'GROUP BY' in s), ('HAVING', lambda s: 'HAVING' in s),
                ('Subconsulta', lambda s: bool(re.search(r'\(\s*SELECT', s))), ('ORDER BY', lambda s: 'ORDER BY' in s)]
    cab = ''.join(f'<th>{e(r)}</th>' for r, _ in recursos)
    corpo_m, totais = '', [0] * len(recursos)
    for q in CONSULTAS:
        s = q['sql'].upper()
        cels = ''
        for i, (_, f) in enumerate(recursos):
            tem = f(s)
            totais[i] += tem
            cels += f'<td class="{"sim" if tem else ""}">{"<i></i>" if tem else ""}</td>'
        corpo_m += f'<tr><th style="--c:{bloco_da_consulta(q["num"])[1]}">{q["num"]}</th>{cels}</tr>'
    tot = ''.join(f'<td class="tot">{t}</td>' for t in totais)
    slide(titulo('17 consultas, cada uma com um recurso diferente') +
          f'<table class="mapa"><thead><tr><th></th>{cab}</tr></thead><tbody>{corpo_m}<tr class="t"><th>total</th>{tot}</tr></tbody></table>',
          'denso', 'Consultas', 'Inácio', 'O enunciado pede no mínimo 12 consultas diferentes, com funções de data ou matemáticas, junção e GROUP BY. A contagem foi feita no próprio SQL. A cor de cada linha é a do bloco de quem apresenta a consulta.',
          ident='mapa', rotulo='Mapa das consultas')

    # Ordem de processamento
    etapas = [(1, 'FROM e JOIN', 'lê as tabelas e liga as linhas pelas chaves'), (2, 'WHERE', 'filtra linha a linha'),
              (3, 'GROUP BY', 'junta em grupos'), (4, 'HAVING', 'filtra os grupos'), (5, 'SELECT', 'calcula as colunas'),
              (6, 'ORDER BY', 'ordena o resultado')]
    pipe = ''.join(f'<div class="passo" style="--c:{COR_ETAPA[n]}">{etapa(n)}<b>{k}</b><span>{t}</span></div>' for n, k, t in etapas)
    slide(titulo('A ordem em que o MySQL processa um SELECT') + f'''<div class="pipeline">{pipe}</div>
<p class="frase">Escrevemos SELECT primeiro, mas o banco começa pelo FROM: monta as linhas, filtra, agrupa, calcula e só então ordena.</p>
<p class="nota-baixo">Nos slides das consultas, cada cláusula traz o número da etapa em que é processada.</p>''',
          '', 'Consultas', 'Inácio', 'Frase que serve para qualquer consulta: o FROM e os JOIN montam as linhas; o WHERE filtra linha a linha; o GROUP BY junta em grupos; o HAVING filtra os grupos; o SELECT calcula as colunas; o ORDER BY ordena.',
          ident='ordem', rotulo='Ordem de processamento')

    for q in CONSULTAS:
        slide_consulta(q)
    divisor(PARTES[3])

    # Script 04
    ops = [('INSERT', VERDE, "Nova reunião e uma demanda sem estado: o DEFAULT a faz nascer 'aberta'."),
           ('UPDATE', CIANO, "A demanda 13 vira 'concluida'; atualizado_em muda sozinho (ON UPDATE)."),
           ('UPDATE', AMARELO, 'As demandas em aberto de uma profissional passam para outra, nas férias da titular.'),
           ('UPDATE no lugar de DELETE', ROXO, 'O usuário é desativado (ativo = FALSE), para preservar a autoria.'),
           ('DELETE', MAGENTA, 'Sai um vínculo de acompanhamento lançado por engano; assistido e profissional ficam.'),
           ('Recusado', TINTA8, 'Apagar a reunião 1, que tem demandas: o banco recusa com o erro 1451.')]
    cards = ''.join(f'<div class="op{" op-tinta" if c == TINTA8 else ""}" style="--c:{c}"><span>{e(o)}</span><p>{e(t)}</p></div>' for o, c, t in ops)
    slide(titulo('Script 04: manutenção sem perder histórico') + f'<div class="ops">{cards}</div>'
          '<p class="nota-baixo">Demandas e evoluções nunca são apagadas; usuários são desativados. Executado sem erro no MySQL 8.4.</p>',
          '', 'Scripts', 'Miguel', 'Destacar a integridade referencial: a chave estrangeira de demanda não tem ON DELETE CASCADE, então o banco recusa apagar uma reunião com demandas.',
          ident='s04', rotulo='Script 04')

    # Do banco ao sistema
    mapa_sis = [('Q03 · Q11', 'Painel: vencidas e a mais antiga'), ('Q04', 'Aviso de prazo próximo'),
                ('Q01 · Q05', 'Busca e filtros de demandas'), ('Q07', 'Minhas demandas'),
                ('Q15 · Q16', 'Retificação e evoluções'), ('Q02 · Q17', 'Reuniões e o que originaram'),
                ('Q08 a Q10 · Q12', 'Relatórios da direção')]
    linhas_s = ''.join(f'<li><code>{e(a)}</code><span>{e(b)}</span></li>' for a, b in mapa_sis)
    img = base64.b64encode(open(os.path.join(AQUI, 'assets', 'telas', 'painel-direcao-prototipo-recorte.jpg'), 'rb').read()).decode()
    slide(titulo('Do banco ao sistema') + f'''<div class="sistema"><ul class="mapa-sis">{linhas_s}</ul>
<figure class="tela"><img src="data:image/jpeg;base64,{img}" width="895" height="700" alt="Painel de demandas da direção no protótipo do sistema, com dados fictícios">
<figcaption>Trecho do painel da direção no protótipo do sistema. Os dados do protótipo são outros (fictícios, de 23/11): não são os 103 registros do banco.</figcaption></figure></div>''',
          '', 'Integração', 'Miguel', 'As consultas não são só exercício: cada uma responde à pergunta de uma tela do sistema da equipe.',
          ident='sistema', rotulo='Do banco ao sistema')

    # Critérios
    crit = [('Apresentação', '1,0', '5 partes; cada integrante explica 3 ou 4 consultas', '{{roteiro}} e {{q01}} a {{q17}}'),
            ('Universo de discurso, DER e notação textual', '1,0', 'minimundo, regras, DER (mín, máx), notação, 3FN e dicionário', '{{crie}} a {{dic}}'),
            ('Scripts e carga com diversidade', '1,0', 'DROP e CREATE DATABASE, CREATE e ALTER TABLE, 103 registros, manutenção', '{{s01}}, {{s02}} e {{s04}}'),
            ('Mínimo de 12 consultas', '5,0', '17 consultas com datas, cálculo, junções, GROUP BY, HAVING e subconsultas', '{{mapa}} a {{q17}}'),
            ('Regras do modelo', 'requisito', '6 tabelas; tipos numérico, texto e data; 1:1, 1:N e N:N', '{{recorte}}, {{rel}} e {{dic}}')]
    linhas_c = ''.join(f'<tr><td><b>{e(a)}</b></td><td class="pts">{b}</td><td>{e(c)}</td><td class="onde">{d}</td></tr>' for a, b, c, d in crit)
    slide(titulo('O que o enunciado pede e onde está') +
          f'<table class="tab crit"><thead><tr><th>Critério</th><th>Pontos</th><th>Como atendemos</th><th>Slides</th></tr></thead><tbody>{linhas_c}</tbody></table>'
          '<p class="nota-baixo">Entrega no Moodle: o documento em PDF (ABNT) e os quatro scripts .sql comentados, num arquivo .zip.</p>',
          '', 'Fechamento', 'Miguel', 'Fechar mostrando que cada critério do enunciado foi atendido e onde está no deck.',
          ident='criterios', rotulo='Critérios do enunciado')

    # Encerramento
    slide(f'''<div class="capa-topo"><div class="lockup">{logo}<span>Centro de Integração<br>Especial</span></div>{ifsp}</div>
<div class="fim">{barra4()}<h2>Obrigado.</h2><p class="fim-sub">Perguntas?</p>
<p class="fim-equipe">Equipe Cortex</p>
<p class="capa-rod">Documento ABNT, scripts .sql e este deck no repositório da equipe Cortex · todos os dados são fictícios</p></div>''',
          'capa fim-slide escuro', 'Perguntas', None, '', ident='fim', rotulo='Encerramento')


# ------------------------------------------------------------------ página
def fonte(caminho, familia, peso):
    dados = base64.b64encode(open(os.path.join(AQUI, 'assets', 'fontes', caminho), 'rb').read()).decode()
    return f"@font-face{{font-family:'{familia}';font-weight:{peso};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{dados}) format('woff2')}}"


CSS = r'''
:root{--t9:#0E1013;--t8:#16181C;--t6:#2A2D33;--t5:#3A3D44;--cinza:#5A5D64;--papel:#F6F5F2;--linha:#E2DFD8;--ce:#B9B5AC;--me:#8C8880;
--mag:#E5006E;--ama:#F2B300;--rox:#8A21CE;--cia:#12A9E0;--ver:#2E9E63;--rcl:#E7CBFA}
*{box-sizing:border-box}html,body{margin:0;background:#0E1013;height:100%}
body{font:400 28px/1.4 'Archivo',system-ui,sans-serif;color:var(--t5);overflow:hidden;-webkit-font-smoothing:antialiased}
.palco{position:fixed;inset:0;display:grid;place-items:center}
.slide{position:absolute;width:1920px;height:1080px;background:#fff;overflow:hidden;padding:56px 96px 0;display:none;transform-origin:center center}
.slide.ativo{display:block}
code,pre,.sql,.schema,.mapa,.cmd,.qnum,.et{font-family:'IBM Plex Mono',ui-monospace,monospace}
h1,h2,h3,p{margin:0}
.titulo{display:flex;align-items:center;gap:24px;font:800 56px/1.05 'Bricolage Grotesque',sans-serif;letter-spacing:-.025em;color:var(--t8);margin:0 0 44px;max-width:1728px;text-wrap:pretty}
.slide.q .titulo{font-size:48px;margin-bottom:32px}
.qnum{flex:none;font:600 32px/1 'IBM Plex Mono',monospace;letter-spacing:0;color:#fff;background:var(--t8);padding:14px 16px;border-radius:2px}
.lead{font-size:38px;line-height:1.35;color:var(--t8)}
.nota-baixo{position:absolute;left:96px;right:96px;bottom:96px;font-size:24px;color:var(--cinza)}
.nota{font-size:24px;color:var(--cinza)}
h3{font:600 28px/1.2 'Archivo',sans-serif;color:var(--t8);margin:0 0 20px}
.seta{flex:none}
.barra4{display:flex;gap:8px}.barra4 i{display:block;width:66px;height:10px}

/* rodapé */
.rodape{position:absolute;left:96px;right:96px;bottom:0;height:76px;border-top:1px solid var(--linha);display:flex;align-items:center;justify-content:space-between;font-size:24px}
.rod-secao{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--cinza)}
.rod-dir{display:flex;align-items:center;gap:36px}
.rod-pessoa{display:flex;align-items:center;gap:12px;font-weight:600;color:var(--t8)}.rod-pessoa i{width:18px;height:18px;display:block}
.rod-num{font:500 24px 'IBM Plex Mono',monospace;color:var(--cinza)}
.escuro{background:var(--t9);color:var(--ce)}
.escuro .rodape{border-top-color:var(--t6)}.escuro .rod-secao,.escuro .rod-num{color:var(--me)}.escuro .rod-pessoa{color:var(--papel)}

/* capa */
.slide.capa{padding:0}
.capa-topo{height:176px;background:var(--papel);border-bottom:1px solid var(--linha);display:flex;align-items:center;justify-content:space-between;padding:0 96px}
.lockup{display:flex;align-items:center;gap:28px}.lockup .logo-crie{width:240px;height:auto;display:block}
.lockup span{padding-left:28px;border-left:2px solid #DCD8D0;font:600 26px/1.25 'Archivo',sans-serif;color:var(--t5)}
.logo-ifsp{height:84px;width:auto}
.capa-hero{height:904px;display:grid;grid-template-columns:1fr 600px;gap:96px;padding:80px 96px 0;align-items:start}
.capa-txt .barra4{margin-bottom:44px}
.capa h1{font:800 100px/1.0 'Bricolage Grotesque',sans-serif;letter-spacing:-.03em;color:var(--papel);margin:0 0 32px;text-wrap:pretty}
.capa-sub{font-size:32px;line-height:1.4;color:var(--ce);max-width:960px;margin-bottom:44px}
.equipe{list-style:none;padding:0;margin:0 0 48px;display:grid;grid-template-columns:1fr 1fr;gap:10px 48px;font:600 28px 'Archivo',sans-serif;color:var(--papel)}
.capa-rod{font-size:24px;color:var(--ce)}
.capa-equipe,.fim-equipe{font:600 32px 'Archivo',sans-serif;color:var(--papel);margin:0 0 40px}
.capa-fig{margin:0}.capa-fig figcaption{font-size:24px;color:var(--me);margin-top:20px}

/* cartões de tabela (dicionário) */
.schema{background:var(--papel);border-top:10px solid var(--c)}
.sc-nome{font:600 28px 'IBM Plex Mono',monospace;color:var(--t8);padding:14px 20px 10px}
.sc-l{display:grid;grid-template-columns:96px 1fr auto;align-items:center;gap:8px;padding:2px 20px;font-size:24px;line-height:32px}
.sc-l:last-child{padding-bottom:16px}
.sc-n{color:var(--t8)}.sc-t{color:var(--cinza)}.nulo{color:var(--rox);font-weight:600}
.sl{display:inline-block;font:600 24px/28px 'IBM Plex Mono',monospace;padding:0 5px;border-radius:2px;margin-right:5px}
.sl.pk{background:var(--ama);color:var(--t8)}.sl.fk{background:var(--cia);color:var(--t8)}.sl.uq{background:var(--rox);color:#fff}
.schema.escuro{background:var(--t8);border:1px solid var(--t6);border-top:10px solid var(--mag)}
.schema.escuro .sc-nome{color:var(--papel);font-size:32px;padding:22px 28px 14px}
.schema.escuro .sc-l{padding:4px 28px;font-size:26px;line-height:38px;grid-template-columns:104px 1fr auto}
.schema.escuro .sc-l:last-child{padding-bottom:24px}
.schema.escuro .sc-n{color:var(--papel)}.schema.escuro .sc-t{color:var(--ce)}.schema.escuro .nulo{color:var(--rcl)}
.schemas{display:grid;grid-template-columns:1.12fr 1fr 1fr;gap:24px 28px;align-items:start}

/* roteiro */
.linha-tempo{display:flex;height:250px;gap:6px;margin-bottom:44px}
.bloco.p3{background:var(--t8);color:#fff;padding:0;gap:0}.p3-cab{padding:22px 20px 12px;display:flex;flex-direction:column;gap:6px}
.p3-faixa{display:flex;gap:3px;flex:1;padding:0 3px 3px}.p3-faixa span{display:grid;place-items:center;font:600 24px 'IBM Plex Mono',monospace;min-width:0;white-space:nowrap}
.bloco{padding:22px 20px;display:flex;flex-direction:column;gap:6px;min-width:0}
.bloco .b-t{font:500 24px 'IBM Plex Mono',monospace}.bloco b{font:800 34px/1.05 'Bricolage Grotesque',sans-serif}.bloco .b-o{font-size:24px;line-height:1.2}
.roteiro{list-style:none;padding:0;margin:0;display:grid;gap:14px}
.roteiro li{display:grid;grid-template-columns:22px 440px 1fr 220px;align-items:center;gap:20px;font-size:28px;padding-bottom:14px;border-bottom:1px solid var(--linha)}
.roteiro .r-cor{width:22px;height:22px}.roteiro b{color:var(--t8)}.roteiro em{font:500 26px 'IBM Plex Mono',monospace;font-style:normal;text-align:right;color:var(--cinza)}

/* universo */
.crie{display:grid;grid-template-columns:.9fr 1.1fr;gap:80px}
.setores{list-style:none;padding:0;margin:44px 0 0;display:grid;gap:16px}
.setores li{background:var(--papel);border-left:12px solid var(--c);padding:30px 32px}.setores b{font:800 42px 'Bricolage Grotesque',sans-serif;color:var(--t8)}
.bloco-tinta{background:var(--t8);padding:44px 48px;margin-bottom:48px}
.bloco-tinta b{display:block;font:800 56px/1.05 'Bricolage Grotesque',sans-serif;color:var(--papel);margin-bottom:16px}
.bloco-tinta p{font-size:31px;line-height:1.4;color:var(--ce)}
.g-tit{font-weight:600;font-size:30px;color:var(--t8);margin-bottom:18px}
.gars{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.gar{border-top:4px solid var(--t8);padding-top:14px}.gar b{display:block;font:800 36px 'Bricolage Grotesque',sans-serif;color:var(--t8);margin-bottom:8px}.gar span{font-size:28px;line-height:1.35}
.regras{display:grid;gap:0}
.regra{display:grid;grid-template-columns:1fr 56px 860px;align-items:center;gap:32px;padding:30px 0;border-bottom:1px solid var(--linha)}
.regra:first-child{border-top:2px solid var(--t8)}.regra:last-child{border-bottom:2px solid var(--t8)}
.regra p{font-size:33px;font-weight:600;color:var(--t8)}
.regra code{font-size:28px;background:var(--t8);color:var(--papel);padding:14px 20px;white-space:pre}
.recorte{display:grid;grid-template-columns:.9fr 1.1fr;gap:72px}
.conta{font-size:30px;color:var(--t8);margin-top:44px;border-top:2px solid var(--t8);padding-top:18px}.conta b{font:800 40px 'Bricolage Grotesque',sans-serif}
.fora.duas-col{columns:2;column-gap:40px}.fora code{font-size:26px;color:var(--rox)}.rec-dir h3{margin-top:30px}.rec-dir h3:first-child{margin-top:0}
.num-grande{display:flex;align-items:center;gap:40px}
.num-grande span{display:block;font:800 240px/.9 'Bricolage Grotesque',sans-serif;color:var(--t8);letter-spacing:-.04em}.num-grande .seis{color:var(--rox)}
.num-grande small{display:block;font-size:26px;line-height:1.3;margin-top:16px}
.rec-dir h3+.chips-tab{margin-bottom:44px}
.chips-tab{display:flex;flex-wrap:wrap;gap:12px}
.tab-chip{font:500 26px 'IBM Plex Mono',monospace;color:var(--t8);background:var(--papel);border-left:10px solid var(--c);padding:8px 18px}
.fora{font-size:28px;margin:0 0 32px;padding-left:32px;line-height:1.5}

/* divisores */
.divisor{padding:120px 120px 0}
.div-corpo{display:flex;align-items:flex-start;gap:72px;margin-top:150px}
.div-num{font:600 220px/.8 'IBM Plex Mono',monospace;letter-spacing:-.04em}
.divisor h2{font:800 120px/1 'Bricolage Grotesque',sans-serif;letter-spacing:-.03em;color:var(--papel);margin-bottom:28px}
.divisor p{font-size:34px;color:var(--ce);margin-bottom:56px;max-width:1100px}
.div-pessoa{display:flex;align-items:center;gap:20px}.div-pessoa i{width:28px;height:28px;display:block}
.div-pessoa b{font:600 44px 'Bricolage Grotesque',sans-serif;color:var(--papel)}.div-pessoa em{font:500 30px 'IBM Plex Mono',monospace;font-style:normal;color:var(--me);margin-left:12px}

/* DER */
.der{display:flex;justify-content:center;position:relative}
.der-leitura{position:absolute;left:0;top:0;width:640px;background:var(--papel);border-left:10px solid var(--mag);padding:18px 24px;font-size:24px;line-height:1.38;color:var(--t8)}
.der-leitura b{display:block;font:600 24px 'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px}.der-leitura p{margin:6px 0 0}
.der-svg{display:block;flex:none;width:1728px;height:790px;font-family:'Archivo',sans-serif}
.der-slide .titulo{margin-bottom:20px}
.ent{fill:#F6F5F2;stroke:#16181C;stroke-width:2.5}.ent-t{fill:#16181C}
.ent-n{font:800 32px 'Bricolage Grotesque',sans-serif;fill:#16181C;text-anchor:middle;letter-spacing:.02em}
.rel{fill:#fff;stroke:#16181C;stroke-width:2.5}.rel-n{font:600 26px 'Archivo',sans-serif;fill:#16181C;text-anchor:middle}
.lig{fill:none;stroke:#16181C;stroke-width:2.5}
.card{font:600 26px 'IBM Plex Mono',monospace;fill:#C4005E}
.at{fill:#fff;stroke:#16181C;stroke-width:2.5}.att{font:500 26px 'IBM Plex Mono',monospace;fill:#16181C}
.papel{font:italic 400 24px 'Archivo',sans-serif;fill:#3A3D44}
.der-slide .nota-baixo{bottom:92px}

/* tabelas de texto */
.tab{border-collapse:collapse;width:100%;font-size:28px}
.tab th{text-align:left;font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;color:var(--cinza);border-bottom:2px solid var(--t8);padding:10px 14px}
.tab td{border-bottom:1px solid var(--linha);padding:15px 14px;vertical-align:middle}
.tab td b{color:var(--t8)}
.tipo{display:inline-block;font:600 24px 'IBM Plex Mono',monospace;padding:2px 10px;border-radius:2px;white-space:nowrap}
.rel .impl{font-size:26px}
.dupla{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:36px}
.dupla p{background:var(--papel);padding:20px 26px;font-size:26px}.dupla b{font-family:'IBM Plex Mono',monospace;color:var(--t8)}
.notacao p{font-size:40px;line-height:1.42;margin:0 0 32px;color:var(--t5)}
.notacao b{font:800 44px 'Bricolage Grotesque',sans-serif;color:var(--t8)}
.notacao .pk{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:7px;font-weight:600;color:var(--t8)}
.notacao .fk{font-style:italic;color:var(--rox);font-weight:600}
.nota-baixo .pk{text-decoration:underline;text-underline-offset:5px;font-weight:600;color:var(--t8)}.nota-baixo .fk{font-style:italic;color:var(--rox);font-weight:600}
.tres{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.card-c{background:var(--papel);border-top:10px solid var(--c);padding:44px 40px 48px;min-height:600px}
.card-c .fn{display:block;font:800 120px/1 'Bricolage Grotesque',sans-serif;color:var(--t8);margin-bottom:36px;letter-spacing:-.03em}.card-c p{font-size:36px;line-height:1.4;color:var(--t8)}

/* código */
.codigo{display:grid;grid-template-columns:1080px 1fr;gap:56px}
.sql-pre{background:var(--t8);color:var(--papel);font-size:24px;line-height:34px;padding:28px 32px;margin:0;white-space:pre}
.k-kw{color:#F2B300;font-weight:600}.k-fn{color:#12A9E0}.k-txt{color:#2E9E63}.k-num{color:#E7CBFA}.k-com{color:#8C8880;font-style:italic}
.anot{list-style:none;padding:0;margin:0;display:grid;gap:30px}
.anot li{border-top:4px solid var(--t8);padding-top:14px}.anot b{display:block;font:800 34px 'Bricolage Grotesque',sans-serif;color:var(--t8);margin-bottom:8px}.anot span{font-size:29px}
.carga{display:grid;grid-template-columns:1fr 1fr;gap:80px}
.barras{display:grid;gap:30px}
.barra{display:grid;grid-template-columns:330px 1fr 56px;align-items:center;gap:16px}
.barra .bn{font:500 24px 'IBM Plex Mono',monospace;color:var(--t8)}.bb{height:58px;background:var(--papel)}.bb i{display:block;height:100%}
.barra b{font:800 34px 'Bricolage Grotesque',sans-serif;color:var(--t8);text-align:right}
.pilha{display:grid;grid-template-columns:190px 1fr;align-items:center;gap:20px;margin-bottom:20px}.pilha b{font-size:28px;color:var(--t8)}
.pilha-b{display:flex;height:72px;gap:3px}.pilha-b span{display:grid;place-items:center;min-width:44px;font:600 24px 'IBM Plex Mono',monospace}
.leg{display:flex;flex-wrap:wrap;gap:10px 26px;font-size:24px;margin-top:28px}.leg i{display:inline-block;width:20px;height:20px;margin-right:10px;vertical-align:-3px}

/* mapa e ordem */
.mapa{border-collapse:collapse;width:100%;font-size:24px}
.mapa thead th{font:600 24px 'Archivo',sans-serif;color:var(--t8);padding:0 6px 10px;text-align:center;border-bottom:2px solid var(--t8)}
.mapa tbody th{text-align:left;padding:0 14px;font-weight:600;color:var(--t8);border-left:10px solid var(--c);width:120px}
.mapa td{text-align:center;border-bottom:1px solid var(--linha);height:37px}
.mapa td.sim i{display:inline-block;width:22px;height:22px;background:var(--t8);vertical-align:middle}
.mapa tr.t th{border-left-color:transparent;color:var(--cinza);font-weight:500}.mapa td.tot{font:800 30px 'Bricolage Grotesque',sans-serif;color:var(--t8);border-bottom:0;padding-top:8px}
.pipeline{display:grid;grid-template-columns:repeat(6,1fr);gap:18px;margin:56px 0 88px}
.passo{background:var(--papel);border-top:10px solid var(--c);padding:30px 20px 36px;display:grid;gap:16px;justify-items:start;align-content:start;min-height:300px}
.passo b{font:600 32px 'IBM Plex Mono',monospace;color:var(--t8)}.passo span:last-child{font-size:28px;line-height:1.3}
.frase{font:600 46px/1.3 'Bricolage Grotesque',sans-serif;color:var(--t8);max-width:1500px;border-left:12px solid var(--mag);padding-left:36px}
.et{display:inline-grid;place-items:center;width:38px;height:34px;font:600 24px/1 'IBM Plex Mono',monospace;border-radius:2px;flex:none}
.et.vazio{background:transparent}

/* consulta */
.q-corpo{display:grid;gap:28px 48px;align-items:start}
.sql{background:var(--t8);color:var(--papel);padding:24px 28px 24px 20px}
.ln{display:flex;gap:16px;align-items:center;min-height:calc(var(--fs) * 1.5)}.ln code{white-space:pre;font-size:var(--fs);line-height:calc(var(--fs) * 1.5)}
.sql .et{width:calc(var(--fs) * 1.6);height:calc(var(--fs) * 1.4);font-size:var(--fs)}
.q-lado{display:grid;gap:24px;align-content:start}
.chips{display:flex;flex-wrap:wrap;gap:12px}.chips.largo{grid-column:1/-1}
.cmd{font:500 24px 'IBM Plex Mono',monospace;color:var(--t8);border:2px solid var(--t8);padding:5px 14px;border-radius:2px;white-space:nowrap}
.q-resumo{font-size:26px;line-height:1.4;color:var(--t5);border-left:8px solid var(--mag);padding-left:20px}
.q-res.largo{grid-column:1/-1}
.res{border-collapse:collapse;table-layout:fixed;font-size:var(--fr)}
.res th{background:var(--papel);color:var(--t8);text-align:left;font:600 var(--fr)/1.42 'Archivo',sans-serif;padding:8px 14px;border-bottom:2px solid var(--t8);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.res td{padding:5px 14px;border-bottom:1px solid var(--linha);white-space:normal;line-height:1.42;color:var(--t8);vertical-align:top}
.res .n{text-align:right;font-variant-numeric:tabular-nums}
.q-nota{font-size:24px;color:var(--cinza);margin-top:12px}

/* manutenção, sistema, critérios */
.ops{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.op{background:var(--papel);border-top:10px solid var(--c);padding:36px 38px 40px;min-height:370px}
.op span{display:block;font:600 32px 'IBM Plex Mono',monospace;color:var(--t8);margin-bottom:18px}.op p{font-size:31px;line-height:1.38;color:var(--t8)}
.op-tinta{background:var(--t8);border-top-color:var(--mag)}.op-tinta span{color:var(--papel)}.op-tinta p{color:var(--ce)}
.sistema{display:grid;grid-template-columns:640px 1000px;gap:88px;align-items:start}
.mapa-sis{list-style:none;padding:0;margin:0}
.mapa-sis li{display:grid;grid-template-columns:1fr;gap:4px;padding:16px 0;border-bottom:1px solid var(--linha);font-size:27px;color:var(--t8)}
.mapa-sis li:first-child{border-top:2px solid var(--t8)}
.mapa-sis code{font:600 24px 'IBM Plex Mono',monospace;color:var(--rox)}
.tela{margin:0}.tela img{display:block;width:auto;height:660px;max-width:100%;border:1px solid var(--linha)}
.tela figcaption{font-size:24px;color:var(--cinza);margin-top:16px}
.crit td{font-size:29px;padding:32px 14px}.crit .pts{font:600 26px 'IBM Plex Mono',monospace;color:var(--t8);white-space:nowrap}.crit .onde{font:500 24px 'IBM Plex Mono',monospace;white-space:nowrap;color:var(--t8)}

/* encerramento */
.fim{padding:190px 96px 0}
.fim .barra4{margin-bottom:44px}
.placa{display:inline-block;background:var(--papel);padding:22px 30px;border-radius:4px;margin-bottom:56px}.placa .logo-crie{width:260px;height:auto;display:block}
.fim h2{font:800 150px/1 'Bricolage Grotesque',sans-serif;letter-spacing:-.03em;color:var(--papel);margin-bottom:18px}
.fim-sub{font-size:44px;color:var(--ce);margin-bottom:56px}
.equipe.linha{display:flex;flex-wrap:wrap;gap:10px 44px;margin-bottom:40px}

/* interface do deck (fora da impressão) */
.ui{position:fixed;left:0;right:0;bottom:0;height:4px;background:#2A2D33;z-index:10}.ui i{display:block;height:100%;background:#E5006E;width:0}
/* notas do apresentador: só com a tecla N; o slide encolhe para cima em vez de ficar coberto */
.notas{position:fixed;left:0;right:0;bottom:0;height:46vh;background:#16181C;color:#F6F5F2;z-index:11;display:none;overflow:auto;padding:16px 28px 28px;font:18px/1.5 'Archivo',sans-serif;border-top:4px solid #E5006E}
body.com-notas .notas{display:block}body.com-notas .palco{bottom:46vh}
.relogio{position:fixed;right:20px;top:14px;z-index:12;background:#16181C;color:#F6F5F2;font:600 22px 'IBM Plex Mono',monospace;padding:6px 14px;display:none}body.modo-apresentador .relogio{display:block}
.n-cab{display:flex;justify-content:space-between;gap:20px;font:500 15px 'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#B9B5AC;margin-bottom:12px}
.n-corpo{display:grid;grid-template-columns:1.15fr .85fr;gap:36px}
.n-bloco{margin-bottom:16px}.n-bloco h4{margin:0 0 6px;font:600 14px 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:#F2B300}
.notas p{margin:0}.notas dl{margin:0}.notas dt{font-weight:600;color:#fff;margin-top:8px}.notas dd{margin:2px 0 0;color:#D9D6CF}
.notas ul,.notas ol{margin:0;padding-left:22px}.notas li{margin:5px 0}.notas li b{color:#fff}
.notas code{font:500 15px 'IBM Plex Mono',monospace;color:#7FD3F2;background:#0E1013;padding:1px 6px;overflow-wrap:anywhere}
@media (max-width:900px){.notas{height:60vh;font-size:16px;padding:12px 16px 24px}body.com-notas .palco{bottom:60vh}.n-corpo{grid-template-columns:1fr;gap:0}}
@media (prefers-reduced-motion:no-preference){.slide.ativo{animation:entra .16s ease-out}@keyframes entra{from{opacity:.5}to{opacity:1}}}
@page{size:1920px 1080px;margin:0}
@media print{html,body{background:#fff;height:auto;overflow:visible}.palco{position:static;display:block}
.slide{display:block!important;position:relative;transform:none!important;animation:none!important;opacity:1!important;page-break-after:always;break-after:page}.ui,.notas{display:none!important}}
'''

JS = r'''
const slides=[...document.querySelectorAll('.slide')];let atual=0;
const palco=document.querySelector('.palco'),barra=document.querySelector('.ui i'),notas=document.querySelector('.notas');
function ajustar(){const s=Math.min(palco.clientWidth/1920,palco.clientHeight/1080);slides.forEach(x=>x.style.transform=`scale(${s})`)}
function mostrar(n){atual=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.classList.toggle('ativo',i===atual));
barra.style.width=((atual+1)/slides.length*100)+'%';const a=slides[atual].querySelector('.nota');notas.innerHTML=a?a.innerHTML:'';notas.scrollTop=0;
history.replaceState(null,'',location.search+'#'+(atual+1));if(typeof avisar==='function')avisar()}
const aberto=()=>document.body.classList.contains('com-notas');
// Janela do apresentador (tecla P): abre as notas numa segunda janela, sincronizada com esta.
const apresentador=new URLSearchParams(location.search).has('apresentador');
const canal='BroadcastChannel' in window?new BroadcastChannel('deck-bd1-cortex'):null;
let recebendo=false;
function avisar(){if(recebendo)return;if(canal)canal.postMessage({slide:atual});try{localStorage.setItem('deck-bd1-slide',JSON.stringify({slide:atual,t:Date.now()}))}catch(_){}}
if(canal)canal.onmessage=ev=>{if(ev.data&&Number.isInteger(ev.data.slide)&&ev.data.slide!==atual){recebendo=true;mostrar(ev.data.slide);recebendo=false}};
addEventListener('storage',ev=>{if(ev.key!=='deck-bd1-slide'||!ev.newValue)return;const d=JSON.parse(ev.newValue);if(d.slide!==atual){recebendo=true;mostrar(d.slide);recebendo=false}});
if(apresentador){document.body.classList.add('com-notas','modo-apresentador');const r=document.querySelector('.relogio'),t0=Date.now();
setInterval(()=>{const s=Math.floor((Date.now()-t0)/1000);r.textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')},1000)}
addEventListener('keydown',ev=>{const k=ev.key;
if(['ArrowRight','PageDown',' ','Enter'].includes(k)){ev.preventDefault();mostrar(atual+1)}
else if(['ArrowLeft','PageUp','Backspace'].includes(k)){ev.preventDefault();mostrar(atual-1)}
else if(k==='Home')mostrar(0);else if(k==='End')mostrar(slides.length-1);
else if((k==='ArrowDown'||k==='ArrowUp')&&aberto()){ev.preventDefault();notas.scrollBy(0,k==='ArrowDown'?140:-140)}
else if(k==='n'||k==='N'){document.body.classList.toggle('com-notas');ajustar()}
else if((k==='p'||k==='P')&&!apresentador){window.open(location.pathname+'?apresentador#'+(atual+1),'apresentador-bd1','width=1280,height=860')}
else if(k==='f'||k==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}});
addEventListener('click',ev=>{if(ev.target.closest('.notas'))return;if(ev.clientX>innerWidth/2)mostrar(atual+1);else mostrar(atual-1)});
addEventListener('resize',ajustar);ajustar();mostrar((parseInt(location.hash.slice(1))||1)-1);
'''


def rotulo_da_parte(s, parte):
    if s.get('q'):
        bloco, cor = bloco_da_consulta(s['q']['num'])
        return f'Parte {parte} · {bloco}', cor
    return ('Perguntas' if parte == 5 else f'Parte {parte}'), COR_PARTE[parte]


def rodape(s, i, total, parte):
    rotulo, cor = rotulo_da_parte(s, parte)
    return (f'<footer class="rodape"><span class="rod-secao">{e(s["secao"])}</span><span class="rod-dir">'
            f'<span class="rod-pessoa"><i style="background:{cor}"></i>{rotulo}</span><span class="rod-num">{i:02d} / {total}</span></span></footer>')


def pagina():
    fontes = ''.join([
        fonte('bricolage-grotesque/bricolage-grotesque-latin-600-normal.woff2', 'Bricolage Grotesque', 600),
        fonte('bricolage-grotesque/bricolage-grotesque-latin-800-normal.woff2', 'Bricolage Grotesque', 800),
        fonte('archivo/archivo-latin-400-normal.woff2', 'Archivo', 400),
        fonte('archivo/archivo-latin-600-normal.woff2', 'Archivo', 600),
        fonte('ibm-plex-mono/ibm-plex-mono-latin-500-normal.woff2', 'IBM Plex Mono', 500),
        fonte('ibm-plex-mono/ibm-plex-mono-latin-600-normal.woff2', 'IBM Plex Mono', 600)])
    total = len(SLIDES)
    numero = {s['id']: i for i, s in enumerate(SLIDES, 1) if s['id']}
    corpo, parte = '', 1
    for i, s in enumerate(SLIDES, 1):
        conteudo = re.sub(r'\{\{(\w+)\}\}', lambda m: f'{numero[m.group(1)]:02d}', s['corpo'])
        parte = s.get('parte_n', 5 if s['id'] == 'fim' else parte)
        rod = '' if 'capa' in s['classe'] else rodape(s, i, total, parte)
        extra = dados_da_consulta(s['q']) if s.get('q') else None
        nota_html = notas.montar(s['id'], parte, extra)
        assert not re.search('[\u2013\u2014]', notas.texto_puro(nota_html)), f'travessão nas notas do slide {i}'
        cab = f'<header class="n-cab"><b>{i:02d} / {total} · {e(s["rotulo"])}</b><span>{rotulo_da_parte(s, parte)[0]}</span></header>'
        corpo += (f'<section class="slide {s["classe"]}" aria-label="Slide {i} de {total}: {e(s["rotulo"])}">{conteudo}{rod}'
                  f'<aside class="nota" hidden>{cab}<div class="n-corpo">{nota_html}</div></aside></section>\n')
    return f'''<!doctype html>
<!-- FONTES
  Identidade: handoff do site do CRIE (site-crie/docs/handoff/README.md, Design Tokens): cores, barra de quatro cores,
  tipografia, cantos vivos, sem sombras e sem ícones.
  Logo do CRIE: recriado em vetor a partir de crie-logo-oficial.png (site-crie/public/brand, 150x70), com as 5 cores do original.
  Logo do IFSP: marca horizontal 2015. Tela: recorte do protótipo do sistema (telas/T-02.png do trabalho Volere), dados fictícios.
  Fontes (SIL OFL 1.1), embutidas: Bricolage Grotesque, Archivo, IBM Plex Mono. Licenças em licencas/ (site) e assets/fontes/*/OFL.txt.
  Dados: scripts 01 a 04 da entrega e ferramentas/resultados.json (17 consultas no MySQL 8.4, SET TIMESTAMP 30/11/2026 19:00).
  Todos os dados são fictícios. -->
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seminário BD1 · Equipe Cortex · O banco de dados das demandas do CRIE</title><style>{fontes}{CSS}</style></head>
<body><main class="palco">{corpo}</main><div class="ui"><i></i></div><div class="notas" role="region" aria-label="Notas do apresentador"></div><div class="relogio" aria-label="Tempo decorrido">00:00</div>
<script>{JS}</script></body></html>'''


def main():
    montar()
    destino = os.path.join(AQUI, 'index.html')
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(pagina())
    print(len(SLIDES), 'slides ->', destino, os.path.getsize(destino), 'bytes')
    if '--pdf' in sys.argv:
        pdf = os.path.join(AQUI, 'Seminario_BD1_Equipe_Cortex.pdf')
        perfil = os.path.join(os.environ.get('TEMP', AQUI), 'perfil-edge-deck')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--user-data-dir={perfil}',
                        '--virtual-time-budget=8000', f'--print-to-pdf={pdf}', 'file:///' + destino.replace('\\', '/')],
                       check=True, timeout=240)
        print('PDF ->', pdf, os.path.getsize(pdf), 'bytes')


if __name__ == '__main__':
    main()
