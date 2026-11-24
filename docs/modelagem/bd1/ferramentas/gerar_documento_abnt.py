# Gera o documento de BD1 no padrão ABNT (NBR 14724, 6024, 6027, 6023, 10520 e normas
# de apresentação tabular do IBGE): A4, Arial 12, espaço 1,5, margens 3/2 cm, tudo em preto.
#
# Como funciona:
#   - HTML -> PDF com o Edge sem interface, em duas partes: a capa (não contada) e o corpo,
#     que começa na folha de rosto com o contador de páginas em 1;
#   - o número da página fica no canto superior direito (margin box do @page) e é escondido
#     nas páginas pré-textuais (página nomeada "pre");
#   - duas passadas: a primeira descobre, pelos destinos do PDF, em que página caiu cada
#     seção e cada legenda; a segunda escreve o sumário e as listas com os números certos;
#   - as duas partes são juntadas com pypdf, com marcadores (bookmarks) das seções.
#
# Uso (a partir de projetos/bd1-projeto):  python -I ferramentas/gerar_documento_abnt.py
import base64, html, io, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from conteudo import EQUIPE, UNIVERSO, RECORTE, RELACIONAMENTOS, CONSULTAS, NORMALIZACAO
import gerar_documento as antigo  # reaproveita der_svg(), notacao_textual() e dicionario()

RAIZ = os.path.dirname(AQUI)
ENTREGA = os.path.join(RAIZ, 'entrega')
LOGOS = os.path.join(AQUI, 'logos')
PDF_FINAL = os.path.join(ENTREGA, 'Documento_BD1_Equipe_Cortex.pdf')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
LOGOS_COLORIDAS = False  # True usa as logos nas cores originais; False, em tons de cinza
FONTE = 'Fonte: elaborado pelos autores (2026).'
e = html.escape

INSTITUICAO = 'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO'
CAMPUS = 'CÂMPUS BRAGANÇA PAULISTA'
CURSO = 'TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS'
TITULO = 'PROJETO INTERDISCIPLINAR DE BANCO DE DADOS I'
TITULO_PDF = 'Projeto Interdisciplinar de Banco de Dados I'
SUBTITULO = 'Sistema de Gestão de Demandas de Articulação do CRIE/APAE de Extrema-MG'
LOCAL, ANO = 'BRAGANÇA PAULISTA', '2026'
NATUREZA = ('Trabalho apresentado à disciplina de Banco de Dados I (BRABCD1) do curso de Tecnologia em '
            'Análise e Desenvolvimento de Sistemas do Instituto Federal de Educação, Ciência e Tecnologia '
            'de São Paulo, Câmpus Bragança Paulista, como requisito parcial para avaliação do Projeto '
            'Interdisciplinar.')
PROFESSORA = 'Professora: Letícia Souza Netto Brandi'
CIT_IFSP = 'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO, 2026'

# Títulos curtos das subseções da Seção 6 (o enunciado completo vem logo abaixo de cada uma).
TITULOS_CONSULTAS = {
    'Q01': 'demandas com o CRAS ou o Conselho Tutelar',
    'Q02': 'reuniões pedagógicas e de saúde em outubro',
    'Q03': 'demandas em aberto com prazo vencido',
    'Q04': 'demandas que vencem nos próximos 7 dias',
    'Q05': 'demandas de prioridade alta ligadas a assistidos',
    'Q06': 'assistidos ativos sem nenhuma demanda',
    'Q07': 'demandas em aberto por profissional',
    'Q08': 'tempo médio de conclusão por prioridade',
    'Q09': 'distribuição das demandas por setor e por estado',
    'Q10': 'demandas abertas por mês',
    'Q11': 'demanda em aberto mais antiga',
    'Q12': 'demandas concluídas acima do tempo médio',
    'Q13': 'profissionais ativos sem acompanhamento',
    'Q14': 'acompanhamentos por profissional',
    'Q15': 'evoluções retificadas',
    'Q16': 'assistidos sem evolução há mais de 20 dias',
    'Q17': 'demandas originadas por reunião',
}

ARQUIVOS = [
    ('01_criacao_banco.sql', 'DROP/CREATE DATABASE, CREATE TABLE das 6 tabelas e ALTER TABLE'),
    ('02_carga_dados.sql', 'INSERT dos dados fictícios em todas as tabelas'),
    ('03_consultas.sql', 'as 17 consultas, com o propósito de cada uma comentado'),
    ('04_manutencao_dados.sql', 'INSERT, UPDATE e DELETE de manutenção'),
    ('Documento_BD1_Equipe_Cortex.pdf', 'este documento'),
]

CARGA = [
    ('usuario', '10', '2 da direção, 3 assistentes sociais, 5 da equipe pedagógica; 1 desativado; 1 sem nenhum acompanhamento'),
    ('assistido', '12', '11 ativos e 1 desligado; 2 sem nenhuma demanda'),
    ('assistido_profissional', '21', 'acompanhamentos iniciados entre 2020 e 2026; assistidos com 1 a 3 profissionais'),
    ('reuniao', '13', 'os três setores, de agosto a novembro de 2026; 2 reuniões sem demandas'),
    ('demanda', '29', 'os cinco estados, as três prioridades, seis categorias, 5 sem assistido, prazos vencidos, próximos e futuros'),
    ('evolucao', '18', '15 lançamentos e 3 retificações, incluindo uma cadeia de duas versões'),
]

REFERENCIAS = [  # NBR 6023, em ordem alfabética
    'ELMASRI, Ramez; NAVATHE, Shamkant B. <i>Sistemas de banco de dados</i>: fundamentos e aplicações. 3. ed. Rio de Janeiro: LTC, 2002.',
    'EQUIPE CORTEX. <i>Especificação do minimundo</i>: Sistema de Gestão de Demandas de Articulação. Versão 1.0. Bragança Paulista: IFSP, 2026.',
    'HEUSER, Carlos Alberto. <i>Projeto de banco de dados</i>. 3. ed. Porto Alegre: Sagra Luzzatto, 2000.',
    'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO. <i>Projeto Interdisciplinar</i>: especificação para Banco de Dados I. Bragança Paulista, 2026.',
]


def ler(nome):
    return open(os.path.join(ENTREGA, nome), encoding='utf-8').read()


# ---------------------------------------------------------------- logos (capa)
def _cinza_hex(m):
    h = m.group(1)
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    y = round(0.299 * r + 0.587 * g + 0.114 * b)
    return '#%02x%02x%02x' % (y, y, y)


def logo_if():
    """Marca horizontal do IFSP (Wikimedia Commons, domínio público)."""
    svg = open(os.path.join(LOGOS, 'ifsp-marca-horizontal-2015.svg'), encoding='utf-8').read()
    svg = svg.replace("font-family:'Open Sans'", "font-family:'Open Sans',Arial,sans-serif")
    if not LOGOS_COLORIDAS:
        svg = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', _cinza_hex, svg)
        open(os.path.join(LOGOS, 'ifsp-marca-horizontal-2015-cinza.svg'), 'w', encoding='utf-8').write(svg)
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode('utf-8')).decode()


def logo_crie():
    """Logo oficial do CRIE (repositório miguelvzs/site-crie, public/brand)."""
    from PIL import Image
    im = Image.open(os.path.join(LOGOS, 'crie-logo-oficial.png')).convert('RGBA')
    fundo = Image.new('RGBA', im.size, (255, 255, 255, 255))
    fundo.alpha_composite(im)
    im = fundo.convert('RGB' if LOGOS_COLORIDAS else 'L')
    im = im.resize((im.width * 4, im.height * 4), Image.LANCZOS)  # suaviza a ampliação na impressão
    if not LOGOS_COLORIDAS:
        im.save(os.path.join(LOGOS, 'crie-logo-oficial-cinza.png'))
    buf = io.BytesIO()
    im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- DER em preto e branco
ESTILO_DER_PB = ('<style>.ent{fill:#fff;stroke:#000;stroke-width:1.6}.enth{fill:#e6e6e6;stroke:#000;stroke-width:1.6}'
                 '.entn{fill:#000;font:700 13px Arial;text-anchor:middle}.att,.atpk{font:12px Arial;fill:#000}'
                 '.atpk{text-decoration:underline;font-weight:700}.pk{fill:#000}.at{fill:#fff;stroke:#000;stroke-width:1.2}'
                 '.rel{fill:#fff;stroke:#000;stroke-width:1.6}.reln{font:600 11.5px Arial;text-anchor:middle;fill:#000}'
                 '.lig{fill:none;stroke:#000;stroke-width:1.3}.card{font:700 12px Arial;fill:#000}'
                 '.papel{font:italic 10.5px Arial;fill:#000}</style>')


def der_pb():
    return re.sub(r'<style>.*?</style>', ESTILO_DER_PB, antigo.der_svg(), flags=re.S)


# ---------------------------------------------------------------- tabelas, quadros e códigos
NUM = re.compile(r'^-?\d+([.,]\d+)?$')


def tabela_ibge(colunas, linhas, total=None):
    """Tabela no estilo IBGE: sem bordas laterais; traço no topo, abaixo do cabeçalho e no fim."""
    numericas = [bool(linhas) and all(NUM.match(str(l[i]) or '') for l in linhas) for i in range(len(colunas))]
    al = lambda i: ' class="dir"' if numericas[i] else ''
    # cabeçalhos como versao_corrigida podem quebrar depois do sublinhado, para caber na mancha
    th = ''.join(f'<th{al(i)}>{e(c).replace("_", "_<wbr>")}</th>' for i, c in enumerate(colunas))
    corpo = ''.join('<tr>' + ''.join(f'<td{al(i)}>{e(str(v))}</td>' for i, v in enumerate(l)) + '</tr>' for l in linhas)
    if total:
        corpo += '<tr class="total">' + ''.join(f'<td{al(i)}>{e(v)}</td>' for i, v in enumerate(total)) + '</tr>'
    return f'<table class="tab"><thead><tr>{th}</tr></thead><tbody>{corpo}</tbody></table>'


def quadro_tabela(colunas, linhas):
    th = ''.join(f'<th>{e(c)}</th>' for c in colunas)
    corpo = ''.join('<tr>' + ''.join(f'<td>{e(v)}</td>' for v in l) + '</tr>' for l in linhas)
    return f'<table class="qd"><thead><tr>{th}</tr></thead><tbody>{corpo}</tbody></table>'


def codigo(sql):
    linhas = sql.strip('\n').split('\n')
    return '<div class="codigo">' + ''.join(f'<div class="cl">{e(l) if l.strip() else "&nbsp;"}</div>' for l in linhas) + '</div>'


def dicionario_blocos():
    """Separa o dicionário do gerador antigo em um bloco (nome, tabela HTML) por tabela."""
    blocos = re.findall(r'<h4>(.*?)</h4>(<table class="dic">.*?</table>)', antigo.dicionario(), flags=re.S)
    # Os ENUM não têm espaço (enum(aberta,em_andamento,...)): permite quebrar depois de cada vírgula,
    # senão a tabela fica mais larga que a mancha e o Edge reduz o documento inteiro.
    quebra_enum = lambda m: m.group(0).replace(',', ',<wbr>')
    return [(nome, re.sub(r'enum\([^)]*\)', quebra_enum, tab.replace('class="dic"', 'class="qd"'))) for nome, tab in blocos]


# ---------------------------------------------------------------- estrutura do documento
class Legenda:
    def __init__(self, tipo, num, titulo, id_):
        self.tipo, self.num, self.titulo, self.id = tipo, num, titulo, id_

    @property
    def rotulo(self):
        return f'{self.tipo} {self.num}'

    def bloco(self, corpo, livre=False, fonte=FONTE):
        cls = 'ilus livre' if livre else 'ilus'
        return (f'<div class="{cls}"><p class="legenda" id="{self.id}">{self.rotulo} – {self.titulo}</p>'
                f'{corpo}<p class="fonte">{fonte}</p></div>')


class Documento:
    def __init__(self, paginas):
        self.paginas = paginas      # id -> número da página (da passada anterior)
        self.secoes = []            # (nivel, indicativo, titulo, id)
        self.ilustracoes, self.tabelas = [], []
        self.cont = {'Figura': 0, 'Quadro': 0, 'Tabela': 0, 'Código': 0}
        self.ind = [0, 0, 0]

    def pag(self, id_):
        return str(self.paginas.get(id_, '00'))

    def secao(self, nivel, titulo):
        self.ind[nivel - 1] += 1
        for i in range(nivel, 3):
            self.ind[i] = 0
        indicativo = '.'.join(str(n) for n in self.ind[:nivel])
        id_ = 'sec-' + indicativo.replace('.', '-')
        titulo = titulo.upper() if nivel == 1 else titulo
        self.secoes.append((nivel, indicativo, titulo, id_))
        return f'<h{nivel} id="{id_}">{indicativo} {titulo}</h{nivel}>'

    def secao_sem_numero(self, titulo, id_):
        self.secoes.append((0, '', titulo, id_))
        return f'<h1 class="centro" id="{id_}">{titulo}</h1>'

    def legenda(self, tipo, titulo):
        self.cont[tipo] += 1
        id_ = f'{tipo[:3].lower().replace("ó", "o")}-{self.cont[tipo]}'
        leg = Legenda(tipo, self.cont[tipo], titulo, id_)
        (self.tabelas if tipo == 'Tabela' else self.ilustracoes).append(leg)
        return leg

    # ---- elementos pré-textuais
    def lista(self, titulo, itens):
        linhas = ''.join(
            f'<a class="item" href="#{l.id}"><span class="it">{l.rotulo} – {l.titulo}</span>'
            f'<span class="pontos"></span><span class="pg">{self.pag(l.id)}</span></a>' for l in itens)
        return f'<section class="pre lista"><h1 class="centro pre-tit">{titulo}</h1>{linhas}</section>'

    def sumario(self):
        linhas = []
        for nivel, ind, tit, id_ in self.secoes:
            num = f'<span class="ind">{ind}</span>' if nivel else ''
            linhas.append(f'<a class="item n{nivel}" href="#{id_}">{num}<span class="it">{tit}</span>'
                          f'<span class="pontos"></span><span class="pg">{self.pag(id_)}</span></a>')
        return f'<section class="pre lista sumario"><h1 class="centro pre-tit">SUMÁRIO</h1>{"".join(linhas)}</section>'


CSS = '''
@page { size: A4; margin: 3cm 2cm 2cm 3cm;
  @top-right { content: counter(page); font: 10pt Arial, sans-serif; color: #000;
               vertical-align: top; text-align: right; padding-top: 2cm; } }
@page pre { @top-right { content: none; } }
html { color-scheme: light; }
body { margin: 0; font: 12pt/1.5 Arial, Helvetica, sans-serif; color: #000; background: #fff; }
.pre { page: pre; }
p { margin: 0; text-align: justify; text-indent: 1.25cm; }
b, strong { font-weight: bold; }
code { font-family: 'Courier New', Courier, monospace; font-size: 11pt; }
h1, h2, h3 { font-size: 12pt; line-height: 1.5; text-align: left; margin: 0; break-after: avoid; }
h1 { font-weight: bold; break-before: page; margin-bottom: 18pt; }
h1.centro { text-align: center; }
h2 { font-weight: bold; margin: 18pt 0; }
h3 { font-weight: normal; margin: 18pt 0; }

/* folha de rosto */
.rosto { height: 24.6cm; display: flex; flex-direction: column; justify-content: space-between; text-align: center; }
.rosto .natureza { margin-left: 8cm; text-align: justify; line-height: 1.15; }
.rosto .natureza p { text-indent: 0; }

/* sumário e listas */
.lista a.item { display: flex; align-items: flex-end; color: #000; text-decoration: none; }
.lista .it { flex: 0 1 auto; }
.lista .pontos { flex: 1 1 0.6cm; border-bottom: 1.2pt dotted #000; margin: 0 3pt 5pt; min-width: 0.6cm; }
.lista .pg { flex: 0 0 auto; text-align: right; }
.sumario .ind { flex: 0 0 1.2cm; align-self: flex-start; }
.sumario .n1 { font-weight: bold; }
.sumario .n2 { font-weight: bold; }
.sumario .n0 { font-weight: bold; }
.sumario .n2 .it, .sumario .n3 .it { font-weight: inherit; }
.sumario .n3 { font-weight: normal; }

/* ilustrações e tabelas */
.ilus { margin: 12pt 0 18pt; break-inside: avoid; }
.ilus.livre { break-inside: auto; }
.legenda { text-indent: 0; text-align: center; font-size: 10pt; line-height: 1.15; margin-bottom: 4pt; break-after: avoid; }
.fonte { text-indent: 0; text-align: left; font-size: 10pt; line-height: 1.15; margin-top: 4pt; break-before: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 10pt; line-height: 1.15; }
th, td { text-align: left; vertical-align: top; padding: 2pt 4pt; overflow-wrap: break-word; }
.dir { text-align: right; }
table.tab th { font-weight: normal; border-top: 1pt solid #000; border-bottom: 0.75pt solid #000; }
table.tab tbody tr:last-child td { border-bottom: 1pt solid #000; }
table.tab tr.total td { border-top: 0.75pt solid #000; }
table.qd th, table.qd td { border: 0.75pt solid #000; }
table.qd th { font-weight: bold; }
.quadro-borda { border: 0.75pt solid #000; padding: 4pt 8pt; font-size: 10pt; line-height: 1.3; }
.quadro-borda .rel-txt { text-indent: 0; text-align: left; margin: 4pt 0 0; }
.quadro-borda .ref { text-indent: 0; text-align: left; margin: 0 0 4pt 0.6cm; }
.der svg { display: block; width: 100%; height: auto; }
.codigo { font: 10pt/1.15 'Courier New', Courier, monospace; border: 0.75pt solid #000; padding: 4pt 6pt;
          box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.codigo .cl { white-space: pre-wrap; overflow-wrap: anywhere; padding-left: 2ch; text-indent: -2ch; }

/* referências */
.referencias p { text-indent: 0; text-align: left; line-height: 1.15; margin: 0 0 14pt; }
'''


def corpo_html(paginas):
    d = Documento(paginas)
    dados = json.load(open(os.path.join(AQUI, 'resultados.json'), encoding='utf-8'))
    par = lambda t: f'<p>{t}</p>'
    t = []  # partes textuais e pós-textuais (montadas antes para numerar legendas e seções)

    # 1 INTRODUÇÃO
    t.append(d.secao(1, 'Introdução'))
    t.append(par('Este documento apresenta o projeto de banco de dados desenvolvido pela Equipe Cortex para a disciplina '
                 'de Banco de Dados I (BRABCD1) do curso de Tecnologia em Análise e Desenvolvimento de Sistemas do '
                 'Instituto Federal de Educação, Ciência e Tecnologia de São Paulo, Câmpus Bragança Paulista, como parte '
                 f'do Projeto Interdisciplinar ({CIT_IFSP}).'))
    t.append(par('O banco modela parte do Sistema de Gestão de Demandas de Articulação, que a equipe desenvolve para o CRIE '
                 '(Centro de Integração Especial, ligado à APAE de Extrema/MG) no âmbito do projeto de extensão “Sistemas em '
                 'Ação: Desenvolvimento de Soluções Digitais para Demandas Comunitárias”, da disciplina Extensão como '
                 'Metodologia de Ensino 2 (BRAEXT2). O sistema registra as reuniões semanais de equipe, as demandas de '
                 'articulação nelas levantadas e as evoluções dos assistidos, conforme o minimundo da equipe '
                 '(EQUIPE CORTEX, 2026).'))
    t.append(par('O objetivo do trabalho é modelar, implementar e consultar um banco de dados relacional para o recorte '
                 'central desse sistema, com seis tabelas, relacionamentos dos tipos 1:1, 1:N e N:N e dados fictícios, '
                 'com base na bibliografia da disciplina (HEUSER, 2000; ELMASRI; NAVATHE, 2002). Os scripts foram '
                 'executados no MySQL 8.4.'))
    t.append(par('O documento está organizado da seguinte forma: a Seção 2 descreve o universo de discurso e o recorte '
                 'implementado; a Seção 3 apresenta o modelo conceitual, com o Diagrama Entidade-Relacionamento; a Seção 4 '
                 'traz o modelo lógico, a verificação das formas normais e o dicionário de dados; a Seção 5 descreve a '
                 'criação e a carga do banco; a Seção 6 apresenta as 17 consultas em SQL, cada uma com o resultado e a '
                 'explicação; a Seção 7 trata da manutenção dos dados; e a Seção 8 traz as considerações finais. Os '
                 'scripts completos de criação e de carga estão nos Apêndices A e B.'))

    # 2 UNIVERSO DE DISCURSO
    t.append(d.secao(1, 'Universo de discurso'))
    t.append(par('O universo de discurso a seguir resume o minimundo especificado pela equipe (EQUIPE CORTEX, 2026).'))
    t.extend(par(p) for p in UNIVERSO)
    t.append(d.secao(2, 'Recorte implementado'))
    t.append(par(RECORTE))

    # 3 MODELO CONCEITUAL
    t.append(d.secao(1, 'Modelo conceitual'))
    fig = d.legenda('Figura', 'Diagrama Entidade-Relacionamento do recorte')
    t.append(par(f'O modelo conceitual do recorte é representado pelo Diagrama Entidade-Relacionamento (DER) da {fig.rotulo}, '
                 'com as restrições estruturais na notação (mínimo, máximo) de Elmasri e Navathe (2002), a mesma da Figura 7.15 da '
                 'Aula 02: retângulos são entidades, losangos são relacionamentos e o par junto a cada entidade indica de quantas '
                 'ocorrências do relacionamento cada ocorrência dela participa. Por exemplo, em origina, Demanda (1,1) diz que cada '
                 'demanda nasce em exatamente uma reunião, e Reunião (0,N) diz que uma reunião origina nenhuma, uma ou várias demandas. '
                 'Atributo com círculo preenchido e sublinhado é o identificador.'))
    t.append(fig.bloco(f'<div class="der">{der_pb()}</div>'))
    t.append(d.secao(2, 'Relacionamentos e cardinalidades'))
    q = d.legenda('Quadro', 'Relacionamentos e cardinalidades do modelo')
    t.append(par('O modelo tem relacionamentos dos três tipos pedidos: <b>1:1</b> (retifica), <b>1:N</b> (origina, é '
                 'responsável por, refere-se a, possui, escreve) e <b>N:N</b> (acompanha). O '
                 f'{q.rotulo} resume as entidades, as cardinalidades e a implementação de cada relacionamento.'))
    t.append(q.bloco(quadro_tabela(['Relacionamento', 'Entidades', 'Tipo', 'Cardinalidades', 'Implementação'], RELACIONAMENTOS)))

    # 4 MODELO LÓGICO
    t.append(d.secao(1, 'Modelo lógico'))
    t.append(par('Esta seção apresenta o modelo lógico (relacional) obtido a partir do DER, a verificação das formas '
                 'normais e o dicionário de dados.'))
    t.append(d.secao(2, 'Notação textual'))
    q = d.legenda('Quadro', 'Notação textual das tabelas (modelo relacional)')
    t.append(par('O mapeamento seguiu as regras da Aula 03: cada entidade vira uma tabela; nos relacionamentos 1:N a chave '
                 'do lado 1 vai como chave estrangeira para o lado N; o N:N vira a tabela associativa com chave primária '
                 f'composta; o 1:1 vira uma chave estrangeira com restrição UNIQUE. No {q.rotulo}, a chave primária está '
                 'sublinhada e em negrito; a chave estrangeira está em itálico, com a tabela referenciada logo abaixo.'))
    t.append(q.bloco(f'<div class="quadro-borda">{antigo.notacao_textual()}</div>'))
    t.append(d.secao(2, 'Verificação das formas normais'))
    t.append(par('A verificação considerou a primeira, a segunda e a terceira formas normais, vistas na Aula 09.'))
    t.extend(par(p) for p in NORMALIZACAO)
    t.append(d.secao(2, 'Dicionário de dados'))
    blocos = dicionario_blocos()
    legs = [d.legenda('Quadro', f'Dicionário de dados da tabela {nome}') for nome, _ in blocos]
    t.append(par('Domínios usados: numérico (INT e BOOLEAN), texto (VARCHAR, TEXT e ENUM, para os domínios fechados de '
                 'perfil, setor, prioridade e estado), data (DATE) e data e hora (DATETIME). Os '
                 f'Quadros {legs[0].num} a {legs[-1].num} apresentam o dicionário de dados de cada tabela, gerado a partir '
                 'dos metadados do MySQL.'))
    t.extend(leg.bloco(tab) for leg, (_, tab) in zip(legs, blocos))

    # 5 IMPLEMENTAÇÃO DO BANCO
    t.append(d.secao(1, 'Implementação do banco'))
    t.append(par('Esta seção descreve os scripts de criação e de carga do banco e a ordem de execução dos arquivos entregues.'))
    t.append(d.secao(2, 'Criação'))
    t.append(par('O script <code>01_criacao_banco.sql</code> apaga o banco, se existir (<code>DROP DATABASE IF EXISTS</code>), '
                 'cria o banco (<code>CREATE DATABASE</code>) e as seis tabelas (<code>CREATE TABLE</code>) com chaves '
                 'primárias, chaves estrangeiras, UNIQUE, NOT NULL, DEFAULT e AUTO_INCREMENT. A chave do autorrelacionamento '
                 'de evolução é acrescentada depois, com <code>ALTER TABLE ... ADD CONSTRAINT</code>, como visto na Aula 04. '
                 'O script completo está no Apêndice A.'))
    t.append(d.secao(2, 'Carga de dados'))
    tb = d.legenda('Tabela', 'Registros inseridos em cada tabela pela carga de dados')
    t.append(par('O script <code>02_carga_dados.sql</code> popula as tabelas. A carga foi planejada para que cada consulta '
                 f'tenha resultado significativo, como mostra a {tb.rotulo}.'))
    total = str(sum(int(c[1]) for c in CARGA))
    t.append(tb.bloco(tabela_ibge(['Tabela', 'Registros', 'Diversidade dos dados'], CARGA, ('Total', total, ''))))
    t.append(par('As senhas são gravadas com <code>SHA2(..., 256)</code>, de modo que nenhuma senha fica legível no banco. '
                 'O script completo de carga está no Apêndice B.'))
    t.append(d.secao(2, 'Arquivos entregues e ordem de execução'))
    q = d.legenda('Quadro', 'Arquivos entregues')
    t.append(par(f'O {q.rotulo} relaciona os arquivos entregues. A execução é feita no MySQL 8 (Workbench ou linha de '
                 'comando), nesta ordem: 01, 02, 03 e 04. Os quatro scripts foram executados do zero, sem erro, no MySQL 8.4.'))
    t.append(q.bloco(quadro_tabela(['Arquivo', 'Conteúdo'], ARQUIVOS)))

    # 6 CONSULTAS EM SQL
    t.append(d.secao(1, 'Consultas em SQL'))
    t.append(par('São 17 consultas, cada uma com propósito e forma diferentes. Juntas, usam seleção com LIKE, IN, BETWEEN e '
                 'NOT IN; funções de data (CURDATE, DATEDIFF, ADDDATE, DATE_FORMAT, YEAR, MONTH, DATE); funções matemáticas '
                 'e de agregação (ROUND, FLOOR, cálculo de percentual, COUNT, COUNT DISTINCT, AVG, MIN e MAX); INNER JOIN, '
                 'LEFT JOIN, RIGHT JOIN e autojunção; GROUP BY com uma e duas colunas; HAVING; e subconsultas que devolvem '
                 'um valor e uma lista.'))
    t.append(par('Ordem lógica em que o banco processa uma consulta: FROM e JOIN, depois WHERE, GROUP BY, HAVING, SELECT e, '
                 'por fim, ORDER BY. As consultas que usam CURDATE() dependem do dia da execução; os resultados a seguir '
                 'foram obtidos com a data do seminário, 30/11/2026, no MySQL 8.4.'))
    t.append(par('Cada subseção apresenta o objetivo da consulta, os comandos usados, a instrução SQL, o resultado, a forma '
                 'como o banco a processa e a relação da consulta com o sistema.'))
    for c in dados:
        num = c['num']
        proc, sistema = CONSULTAS[num]
        n = len(c['linhas'])
        t.append(d.secao(2, f'Consulta {num}: {TITULOS_CONSULTAS[num]}'))
        cod = d.legenda('Código', f'Consulta {num}')
        tab = d.legenda('Tabela', f'Resultado da consulta {num}')
        cmds = c['comandos'].rstrip('.')
        t.append(par(f'<b>Objetivo:</b> {e(c["enunciado"])}'))
        t.append(par(f'<b>Comandos usados:</b> {e(cmds)}.'))
        t.append(par(f'O {cod.rotulo} apresenta a instrução SQL, e a {tab.rotulo}, o resultado obtido, com {n} '
                     f'{"linha" if n == 1 else "linhas"}.'))
        t.append(cod.bloco(codigo(c['sql'])))
        t.append(tab.bloco(tabela_ibge(c['colunas'], c['linhas'])))
        t.append(par(f'<b>Processamento:</b> {proc}'))
        t.append(par(f'<b>Relação com o sistema:</b> {sistema}'))

    # 7 MANUTENÇÃO DOS DADOS
    t.append(d.secao(1, 'Manutenção dos dados'))
    cod = d.legenda('Código', 'Script de manutenção dos dados (04_manutencao_dados.sql)')
    t.append(par('O script <code>04_manutencao_dados.sql</code> mostra as operações do dia a dia, respeitando as regras do '
                 'minimundo: a demanda nova nasce aberta pelo DEFAULT; a mudança de estado e a reatribuição são UPDATE com '
                 'WHERE; o usuário é desativado em vez de excluído; e o DELETE só é usado para um vínculo de acompanhamento '
                 'lançado por engano. O script também mostra a integridade referencial: apagar uma reunião que tem demandas '
                 f'é recusado pelo banco (erro 1451). O script completo está no {cod.rotulo}.'))
    t.append(cod.bloco(codigo(ler('04_manutencao_dados.sql')), livre=True))

    # 8 CONSIDERAÇÕES FINAIS
    t.append(d.secao(1, 'Considerações finais'))
    t.append(par('Este trabalho apresentou o projeto e a implementação de um banco de dados relacional para o recorte central '
                 'do Sistema de Gestão de Demandas de Articulação do CRIE. A partir do universo de discurso, a equipe '
                 'elaborou o DER com a notação (mínimo, máximo), mapeou-o para seis tabelas com relacionamentos 1:1, 1:N e N:N, '
                 'verificou a primeira, a segunda e a terceira formas normais e documentou cada coluna no dicionário de dados.'))
    t.append(par(f'A carga de {total} registros fictícios foi planejada para dar resultado significativo às 17 consultas, que '
                 'usam seleção, funções de data e matemáticas, agregação, junções interna, externa e autojunção, '
                 'agrupamento com HAVING e subconsultas. Os quatro scripts foram executados do zero, sem erro, no MySQL 8.4.'))
    t.append(par('Como os nomes de tabelas e colunas são os mesmos do back-end do sistema, o banco desta disciplina e o do '
                 'servidor contam a mesma história, e cada consulta corresponde a requisitos e rotas do sistema. As '
                 'entidades que ficaram fora do recorte (Serviço da Rede, Encaminhamento, Ação, Retorno de Acompanhamento, '
                 'Histórico de Demanda e Registro de Auditoria) fazem parte do sistema completo descrito no minimundo.'))

    # REFERÊNCIAS e APÊNDICES
    t.append(d.secao_sem_numero('REFERÊNCIAS', 'referencias'))
    t.append('<div class="referencias">' + ''.join(f'<p>{r}</p>' for r in REFERENCIAS) + '</div>')
    for letra, titulo, arquivo, secao in [('A', 'SCRIPT DE CRIAÇÃO DO BANCO', '01_criacao_banco.sql', '5.1'),
                                         ('B', 'SCRIPT DE CARGA DOS DADOS', '02_carga_dados.sql', '5.2')]:
        t.append(d.secao_sem_numero(f'APÊNDICE {letra} – {titulo}', f'apendice-{letra.lower()}'))
        cod = d.legenda('Código', f'Script de {"criação do banco" if letra == "A" else "carga dos dados"} ({arquivo})')
        t.append(par(f'O {cod.rotulo} apresenta o script <code>{arquivo}</code> completo, descrito na Seção {secao}.'))
        t.append(cod.bloco(codigo(ler(arquivo)), livre=True))

    # Elementos pré-textuais (folha de rosto, listas e sumário), montados depois do texto
    rosto = f'''<section class="pre rosto">
  <div><b>{"<br>".join(n.upper() for n in EQUIPE)}</b></div>
  <div><b>{TITULO}:</b><br>{SUBTITULO}</div>
  <div class="natureza"><p>{NATUREZA}</p><p>&nbsp;</p><p>{PROFESSORA}</p></div>
  <div><b>{LOCAL}<br>{ANO}</b></div>
</section>'''
    pre = rosto + d.lista('LISTA DE ILUSTRAÇÕES', d.ilustracoes) + d.lista('LISTA DE TABELAS', d.tabelas) + d.sumario()
    doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>{TITULO_PDF}: {SUBTITULO}</title><style>{CSS}</style></head><body>
{pre}
<main>{"".join(t)}</main>
</body></html>'''
    return doc, d


def capa_html():
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Capa</title><style>
@page {{ size: A4; margin: 3cm 2cm 2cm 3cm; }}
html {{ color-scheme: light; }}
body {{ margin: 0; font: bold 12pt/1.5 Arial, Helvetica, sans-serif; color: #000; background: #fff; }}
.capa {{ height: 24.6cm; display: flex; flex-direction: column; justify-content: space-between; text-align: center; }}
.logos {{ display: flex; justify-content: center; align-items: center; gap: 1.8cm; margin-bottom: 0.6cm; }}
.logos img {{ height: 1.9cm; width: auto; }}
.sub {{ font-weight: normal; }}
</style></head><body><div class="capa">
  <div><div class="logos"><img src="{logo_if()}" alt="Instituto Federal de São Paulo"><img src="{logo_crie()}" alt="CRIE"></div>
  {INSTITUICAO}<br>{CAMPUS}<br>{CURSO}</div>
  <div>{"<br>".join(n.upper() for n in EQUIPE)}</div>
  <div>{TITULO}:<br><span class="sub">{SUBTITULO}</span></div>
  <div>{LOCAL}<br>{ANO}</div>
</div></body></html>'''


# ---------------------------------------------------------------- impressão e montagem
def imprimir(conteudo, html_path, pdf_path, perfil):
    open(html_path, 'w', encoding='utf-8').write(conteudo)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run', '--no-pdf-header-footer',
                    f'--user-data-dir={perfil}', f'--print-to-pdf={pdf_path}', Path(html_path).as_uri()],
                   capture_output=True, text=True, timeout=300)
    if not os.path.exists(pdf_path):
        raise RuntimeError(f'O Edge não gerou {pdf_path}')


def destinos(pdf_path):
    """id do elemento -> número da página no corpo (a folha de rosto é a página 1)."""
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    return {nome.lstrip('/'): r.get_destination_page_number(dest) + 1 for nome, dest in r.named_destinations.items()}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    from pypdf import PdfReader, PdfWriter
    tmp = tempfile.mkdtemp(prefix='bd1_abnt_')
    perfil = os.path.join(tmp, 'perfil-edge')
    try:
        capa_pdf, corpo_pdf = os.path.join(tmp, 'capa.pdf'), os.path.join(tmp, 'corpo.pdf')
        imprimir(capa_html(), os.path.join(AQUI, 'capa_abnt.html'), capa_pdf, perfil)
        paginas = {}
        for passada in range(1, 5):
            html_txt, doc = corpo_html(paginas)
            imprimir(html_txt, os.path.join(AQUI, 'documento_abnt.html'), corpo_pdf, perfil)
            novas = destinos(corpo_pdf)
            faltando = [s[3] for s in doc.secoes if s[3] not in novas]
            print(f'passada {passada}: {len(novas)} destinos, {len(PdfReader(corpo_pdf).pages)} páginas no corpo'
                  + (f', sem destino: {faltando}' if faltando else ''))
            if novas == paginas:
                break
            paginas = novas
        else:
            raise RuntimeError('a paginação não estabilizou')

        w = PdfWriter()
        w.append(PdfReader(capa_pdf))
        w.append(PdfReader(corpo_pdf))
        pais = {}
        for nivel, ind, tit, id_ in doc.secoes:  # marcadores do PDF (+1 por causa da capa)
            pagina = paginas[id_]  # 1 = folha de rosto = página física 2 = índice 1
            rotulo = f'{ind} {tit}'.strip()
            if nivel == 2:
                w.add_outline_item(rotulo, pagina, parent=pais.get(1))
            else:
                pais[1] = w.add_outline_item(rotulo, pagina)
        w.add_metadata({'/Title': f'{TITULO_PDF}: {SUBTITULO}', '/Author': '; '.join(EQUIPE),
                        '/Subject': 'Banco de Dados I (BRABCD1) - IFSP Câmpus Bragança Paulista'})
        with open(PDF_FINAL, 'wb') as f:
            w.write(f)
        print('PDF:', PDF_FINAL, os.path.getsize(PDF_FINAL), 'bytes,', len(PdfReader(PDF_FINAL).pages), 'páginas')
        print('Introdução na página', paginas['sec-1'], '| Referências na página', paginas['referencias'])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
