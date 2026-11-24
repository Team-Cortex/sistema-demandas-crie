# Gera o documento único de BD1 (HTML -> PDF com o Edge sem interface).
# Uso: python -I ferramentas/gerar_documento.py   (rodar a partir de projetos/bd1-projeto)
import html, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conteudo import EQUIPE, UNIVERSO, RECORTE, RELACIONAMENTOS, DESCRICOES, CONSULTAS, NORMALIZACAO

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ENTREGA = os.path.join(RAIZ, 'entrega')
e = html.escape


def ler(nome):
    return open(os.path.join(ENTREGA, nome), encoding='utf-8').read()


# ---------------------------------------------------------------- DER (SVG)
def entidade(x, y, nome, atributos, w=190):
    h = 30 + 18 * len(atributos) + 8
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" class="ent"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" class="enth"/>',
         f'<text x="{x + w / 2}" y="{y + 18}" class="entn">{nome}</text>']
    for i, a in enumerate(atributos):
        pk = a.startswith('*')
        a = a.lstrip('*')
        cy = y + 44 + 18 * i
        s.append(f'<circle cx="{x + 14}" cy="{cy - 4}" r="4" class="{"pk" if pk else "at"}"/>')
        s.append(f'<text x="{x + 24}" y="{cy}" class="{"atpk" if pk else "att"}">{a}</text>')
    return '\n'.join(s)


def losango(cx, cy, rotulo, w=124, h=50):
    return (f'<polygon points="{cx - w / 2},{cy} {cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2}" class="rel"/>'
            f'<text x="{cx}" y="{cy + 4}" class="reln">{rotulo}</text>')


def linha(*pts):
    return '<polyline points="' + ' '.join(f'{x},{y}' for x, y in pts) + '" class="lig"/>'


def card(x, y, t, anchor='start'):
    return f'<text x="{x}" y="{y}" class="card" text-anchor="{anchor}">{t}</text>'


def der_svg():
    p = []
    # Entidades (atributo com * = identificador)
    p.append(entidade(405, 20, 'REUNIÃO', ['*id', 'data', 'setor', 'criado_em']))
    p.append(entidade(405, 250, 'DEMANDA', ['*id', 'descricao', 'categoria', 'prioridade', 'prazo', 'estado', 'criado_em', 'atualizado_em']))
    p.append(entidade(30, 250, 'USUÁRIO', ['*id', 'nome', 'email', 'senha_hash', 'perfil', 'ativo', 'criado_em']))
    p.append(entidade(780, 270, 'ASSISTIDO', ['*id', 'nome_tratamento', 'ativo', 'criado_em']))
    p.append(entidade(600, 580, 'EVOLUÇÃO', ['*id', 'data', 'area_atuacao', 'descricao', 'ocorrido_em']))
    # origina (Reunião 1:N Demanda)
    p.append(linha((500, 130), (500, 165))); p.append(linha((500, 215), (500, 250)))
    p.append(losango(500, 190, 'origina'))
    p.append(card(508, 148, '(0,N)')); p.append(card(508, 244, '(1,1)'))
    # é responsável por (Usuário 1:N Demanda)
    p.append(linha((220, 300), (250, 300))); p.append(linha((374, 300), (405, 300)))
    p.append(losango(312, 300, 'responde por'))
    p.append(card(224, 292, '(0,N)')); p.append(card(401, 292, '(1,1)', 'end'))
    # refere-se a (Assistido 0..1:N Demanda)
    p.append(linha((595, 325), (625, 325))); p.append(linha((749, 325), (780, 325)))
    p.append(losango(687, 325, 'refere-se a'))
    p.append(card(599, 317, '(0,1)')); p.append(card(776, 317, '(0,N)', 'end'))
    # acompanha (N:N) com atributo data_inicio
    p.append(linha((125, 414), (125, 500), (438, 500))); p.append(linha((562, 500), (875, 500), (875, 380)))
    p.append(losango(500, 500, 'acompanha'))
    p.append(linha((500, 525), (500, 548)))
    p.append('<circle cx="500" cy="552" r="4" class="at"/><text x="510" y="556" class="att">data_inicio</text>')
    p.append(card(131, 434, '(0,N)')); p.append(card(869, 398, '(0,N)', 'end'))
    # possui (Assistido 1:N Evolução)
    p.append(linha((930, 380), (930, 619))); p.append(linha((868, 644), (790, 644)))
    p.append(losango(930, 644, 'possui'))
    p.append(card(936, 398, '(0,N)')); p.append(card(796, 636, '(1,1)'))
    # escreve (Usuário 1:N Evolução)
    p.append(linha((70, 414), (70, 644), (268, 644))); p.append(linha((392, 644), (600, 644)))
    p.append(losango(330, 644, 'escreve'))
    p.append(card(76, 434, '(0,N)')); p.append(card(594, 636, '(1,1)', 'end'))
    # retifica (Evolução 1:1 Evolução, autorrelacionamento)
    p.append(linha((640, 708), (640, 752), (650, 752))); p.append(linha((740, 752), (750, 752), (750, 708)))
    p.append(losango(695, 752, 'retifica', 92, 40))
    p.append(card(634, 728, '(0,1)', 'end')); p.append(card(756, 728, '(0,1)'))
    p.append('<text x="634" y="742" class="papel" text-anchor="end">original</text>')
    p.append('<text x="756" y="742" class="papel">nova versão</text>')
    estilo = ('<style>.ent{fill:#fff;stroke:#1f7a33;stroke-width:1.6}.enth{fill:#1f7a33}'
              '.entn{fill:#fff;font:700 13px Arial;text-anchor:middle}.att,.atpk{font:12px Arial;fill:#1b1b1b}'
              '.atpk{text-decoration:underline;font-weight:700}.pk{fill:#1b1b1b}.at{fill:#fff;stroke:#1b1b1b;stroke-width:1.2}'
              '.rel{fill:#eef6ef;stroke:#1f7a33;stroke-width:1.6}.reln{font:600 11.5px Arial;text-anchor:middle;fill:#1b1b1b}'
              '.lig{fill:none;stroke:#1b1b1b;stroke-width:1.3}.card{font:700 12px Arial;fill:#cd191e}'
              '.papel{font:italic 10.5px Arial;fill:#555}</style>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 790" width="100%">{estilo}{"".join(p)}</svg>'


# ---------------------------------------------------------------- tabelas e textos
def tabela(colunas, linhas, classe='res'):
    th = ''.join(f'<th>{e(c)}</th>' for c in colunas)
    tr = ''.join('<tr>' + ''.join(f'<td>{e(v)}</td>' for v in l) + '</tr>' for l in linhas)
    return f'<table class="{classe}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def notacao_textual():
    def t(nome, cols, pks, fks):
        partes = []
        for c in cols:
            s = e(c)
            if c in pks:
                s = f'<u><b>{s}</b></u>'
            if c in fks:
                s = f'<i>{s}</i>'
            partes.append(s)
        return f'<p class="rel-txt"><b>{nome}</b> (' + ', '.join(partes) + ')</p>'
    return ''.join([
        t('Usuario', ['id', 'nome', 'email', 'senha_hash', 'perfil', 'ativo', 'criado_em'], {'id'}, set()),
        t('Assistido', ['id', 'nome_tratamento', 'ativo', 'criado_em'], {'id'}, set()),
        t('AssistidoProfissional', ['assistido_id', 'profissional_id', 'data_inicio'], {'assistido_id', 'profissional_id'}, {'assistido_id', 'profissional_id'}),
        '<p class="ref">assistido_id referencia Assistido; profissional_id referencia Usuario</p>',
        t('Reuniao', ['id', 'data', 'setor', 'criado_em'], {'id'}, set()),
        t('Demanda', ['id', 'descricao', 'categoria', 'prioridade', 'prazo', 'estado', 'responsavel_id', 'reuniao_id', 'assistido_id', 'criado_em', 'atualizado_em'], {'id'}, {'responsavel_id', 'reuniao_id', 'assistido_id'}),
        '<p class="ref">responsavel_id referencia Usuario; reuniao_id referencia Reuniao; assistido_id referencia Assistido (opcional, aceita nulo)</p>',
        t('Evolucao', ['id', 'assistido_id', 'profissional_id', 'data', 'area_atuacao', 'descricao', 'ocorrido_em', 'retifica_id'], {'id'}, {'assistido_id', 'profissional_id', 'retifica_id'}),
        '<p class="ref">assistido_id referencia Assistido; profissional_id referencia Usuario; retifica_id referencia Evolucao (único, o que torna o relacionamento 1:1)</p>',
    ])


def dicionario():
    texto = open(os.path.join(AQUI, 'dicionario.tsv'), encoding='utf-8').read()
    linhas = [(l.rstrip('\r').split('\t') + [''] * 7)[:7] for l in texto.split('\n')[1:] if l.strip()]
    blocos, atual, tab = [], [], None
    nomes = {'usuario': 'USUARIO', 'assistido': 'ASSISTIDO', 'assistido_profissional': 'ASSISTIDO_PROFISSIONAL',
             'reuniao': 'REUNIAO', 'demanda': 'DEMANDA', 'evolucao': 'EVOLUCAO'}
    for t_, col, tipo, nulo, chave, padrao, extra in linhas:
        if t_ != tab:
            if atual:
                blocos.append((tab, atual))
            tab, atual = t_, []
        restr = []
        if chave == 'PRI':
            restr.append('PK')
        if col.endswith('_id'):
            restr.append('FK')
        if chave == 'UNI':
            restr.append('UNIQUE')
        restr.append('NULL' if nulo == 'YES' else 'NOT NULL')
        if 'auto_increment' in extra:
            restr.append('AUTO_INCREMENT')
        if padrao:
            restr.append('DEFAULT ' + padrao.replace('CURRENT_TIMESTAMP', 'agora').replace("'", ''))
        atual.append((col, tipo.replace("'", ''), ', '.join(restr), DESCRICOES.get(f'{t_}.{col}', '')))
    blocos.append((tab, atual))
    return ''.join(f'<h4>{nomes[t_]}</h4>' + tabela(['Coluna', 'Tipo', 'Restrições', 'Descrição'], cols, 'dic') for t_, cols in blocos)


def consultas_html():
    dados = json.load(open(os.path.join(AQUI, 'resultados.json'), encoding='utf-8'))
    out = []
    for q in dados:
        proc, sistema = CONSULTAS[q['num']]
        out.append(f'''<section class="consulta">
<h3>{q["num"]}. {e(q["enunciado"])}</h3>
<p class="cmd"><b>Comandos:</b> {e(q["comandos"])}</p>
<pre>{e(q["sql"])}</pre>
<p class="lbl">Resultado ({len(q["linhas"])} {"linha" if len(q["linhas"]) == 1 else "linhas"}):</p>
{tabela(q["colunas"], q["linhas"])}
<p><b>Como o banco processa:</b> {proc}</p>
<p class="sis"><b>No sistema:</b> {sistema}</p>
</section>''')
    return '\n'.join(out)


def carga_resumo():
    return tabela(['Tabela', 'Registros', 'Diversidade dos dados'], [
        ('usuario', '10', '2 da direção, 3 assistentes sociais, 5 da equipe pedagógica; 1 desativado; 1 sem nenhum acompanhamento'),
        ('assistido', '12', '11 ativos e 1 desligado; 2 sem nenhuma demanda'),
        ('assistido_profissional', '21', 'acompanhamentos iniciados entre 2020 e 2026; assistidos com 1 a 3 profissionais'),
        ('reuniao', '13', 'os três setores, de agosto a novembro de 2026; 2 reuniões sem demandas'),
        ('demanda', '29', 'os cinco estados, as três prioridades, seis categorias, 5 sem assistido, prazos vencidos, próximos e futuros'),
        ('evolucao', '18', '15 lançamentos e 3 retificações, incluindo uma cadeia de duas versões'),
    ], 'dic')


# ---------------------------------------------------------------- documento
def documento():
    rel = tabela(['Relacionamento', 'Entidades', 'Tipo', 'Cardinalidades', 'Implementação'], RELACIONAMENTOS, 'dic')
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Projeto Interdisciplinar - Banco de Dados I - Equipe Cortex</title>
<style>
@page {{ size: A4; margin: 2cm 1.8cm; }}
html {{ color-scheme: light; }}
body {{ font: 11pt/1.5 Arial, Helvetica, sans-serif; color: #1b1b1b; background: #fff; }}
h1 {{ font-size: 17pt; color: #1f7a33; margin: 0 0 6px; }}
h2 {{ font-size: 14pt; color: #1f7a33; border-bottom: 2px solid #1f7a33; padding-bottom: 3px; margin: 26px 0 10px; page-break-after: avoid; }}
h3 {{ font-size: 11.5pt; margin: 18px 0 6px; page-break-after: avoid; }}
h4 {{ font-size: 10.5pt; margin: 14px 0 4px; }}
p {{ margin: 6px 0; text-align: justify; }}
code {{ font: 9.5pt Consolas, monospace; background: #f1f4f2; padding: 0 3px; }}
pre {{ font: 8.6pt/1.35 Consolas, monospace; background: #f6f8f6; border: 1px solid #dfe8e1; border-left: 3px solid #1f7a33; padding: 8px 10px; white-space: pre-wrap; page-break-inside: avoid; }}
pre.script {{ page-break-inside: auto; font-size: 7.8pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 6px 0 8px; font-size: 8.6pt; page-break-inside: avoid; }}
th {{ background: #1f7a33; color: #fff; text-align: left; padding: 3px 5px; }}
td {{ border-bottom: 1px solid #dfe8e1; padding: 3px 5px; vertical-align: top; }}
table.dic {{ font-size: 9pt; }}
.capa {{ height: 25.5cm; display: flex; flex-direction: column; justify-content: space-between; text-align: center; page-break-after: always; }}
.capa .topo {{ font-size: 11.5pt; font-weight: 700; line-height: 1.6; }}
.capa .titulo {{ font-size: 20pt; font-weight: 700; color: #1f7a33; }}
.capa .sub {{ font-size: 13pt; margin-top: 10px; }}
.capa .equipe {{ font-size: 11.5pt; line-height: 1.7; }}
.sumario li {{ margin: 3px 0; }}
.consulta {{ page-break-inside: auto; border-top: 1px solid #dfe8e1; margin-top: 10px; }}
.cmd {{ color: #444; font-size: 10pt; }}
.lbl {{ font-weight: 700; font-size: 10pt; margin-bottom: 2px; }}
.sis {{ background: #eef6ef; padding: 5px 8px; border-radius: 3px; }}
.rel-txt {{ font: 10.5pt Consolas, monospace; margin: 8px 0 2px; text-align: left; }}
.ref {{ font-size: 9.5pt; color: #444; margin: 0 0 8px 16px; }}
.quebra {{ page-break-before: always; }}
.der {{ border: 1px solid #dfe8e1; padding: 6px; }}
.nota {{ font-size: 9.5pt; color: #444; }}
</style></head><body>

<div class="capa">
  <div class="topo">INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO<br>CÂMPUS BRAGANÇA PAULISTA<br>TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS</div>
  <div>
    <div class="titulo">Projeto Interdisciplinar<br>Banco de Dados I</div>
    <div class="sub">Sistema de Gestão de Demandas de Articulação<br>CRIE / APAE de Extrema-MG</div>
    <div class="sub">Disciplina: Banco de Dados I (BRABCD1)<br>Profª Letícia Souza Netto Brandi</div>
  </div>
  <div class="equipe"><b>Equipe Cortex</b><br>{"<br>".join(EQUIPE)}</div>
  <div class="topo">Bragança Paulista<br>Novembro de 2026</div>
</div>

<h1>Sumário</h1>
<ol class="sumario">
<li>Universo de discurso</li>
<li>Diagrama Entidade-Relacionamento</li>
<li>Notação textual das tabelas (modelo relacional)</li>
<li>Dicionário de dados</li>
<li>Scripts de implementação e carga dos dados</li>
<li>Consultas em SQL (17 consultas)</li>
<li>Manutenção dos dados (INSERT, UPDATE e DELETE)</li>
<li>Arquivos entregues e como executar</li>
<li>Apêndice: script de carga dos dados</li>
</ol>

<h2 class="quebra">1. Universo de discurso</h2>
{"".join(f"<p>{p}</p>" for p in UNIVERSO)}
<h3>1.1 Recorte implementado nesta disciplina</h3>
<p>{RECORTE}</p>

<h2 class="quebra">2. Diagrama Entidade-Relacionamento</h2>
<p class="nota">Notação (mínimo, máximo) de Elmasri e Navathe, a mesma da Figura 7.15 da Aula 02: retângulos são entidades, losangos são relacionamentos e o par junto a cada entidade indica de quantas ocorrências do relacionamento cada ocorrência dela participa. Atributo com círculo preenchido e sublinhado é o identificador.</p>
<div class="der">{der_svg()}</div>
<h3>2.1 Relacionamentos e cardinalidades</h3>
<p>O modelo tem relacionamentos dos três tipos pedidos: <b>1:1</b> (retifica), <b>1:N</b> (origina, é responsável por, refere-se a, possui, escreve) e <b>N:N</b> (acompanha).</p>
{rel}

<h2 class="quebra">3. Notação textual das tabelas (modelo relacional)</h2>
<p class="nota">Chave primária sublinhada e em negrito; chave estrangeira em itálico, com a tabela referenciada logo abaixo. Mapeamento pelas regras da Aula 03: cada entidade vira uma tabela; nos relacionamentos 1:N a chave do lado 1 vai como chave estrangeira para o lado N; o N:N vira a tabela associativa com chave primária composta; o 1:1 vira uma chave estrangeira com restrição UNIQUE.</p>
{notacao_textual()}
<h3>3.1 Verificação das formas normais (Aula 09)</h3>
{"".join(f"<p>{p}</p>" for p in NORMALIZACAO)}

<h2 class="quebra">4. Dicionário de dados</h2>
<p>Domínios usados: numérico (INT e BOOLEAN), texto (VARCHAR, TEXT e ENUM, para os domínios fechados de perfil, setor, prioridade e estado), data (DATE) e data e hora (DATETIME).</p>
{dicionario()}

<h2 class="quebra">5. Scripts de implementação e carga dos dados</h2>
<p>O script <code>01_criacao_banco.sql</code> apaga o banco, se existir (<code>DROP DATABASE IF EXISTS</code>), cria o banco (<code>CREATE DATABASE</code>) e as seis tabelas (<code>CREATE TABLE</code>) com chaves primárias, chaves estrangeiras, UNIQUE, NOT NULL, DEFAULT e AUTO_INCREMENT. A chave do autorrelacionamento de evolução é acrescentada depois, com <code>ALTER TABLE ... ADD CONSTRAINT</code>, como visto na Aula 04. O script <code>02_carga_dados.sql</code> popula as tabelas. A carga foi planejada para que cada consulta tenha resultado significativo:</p>
{carga_resumo()}
<p>As senhas são gravadas com <code>SHA2(..., 256)</code>, de modo que nenhuma senha fica legível no banco. O script completo de criação está a seguir; o de carga está no apêndice e no arquivo .sql.</p>
<pre class="script">{e(ler("01_criacao_banco.sql"))}</pre>

<h2 class="quebra">6. Consultas em SQL</h2>
<p>São 17 consultas, cada uma com propósito e forma diferentes. Juntas, usam seleção com LIKE, IN, BETWEEN e NOT IN; funções de data (CURDATE, DATEDIFF, ADDDATE, DATE_FORMAT, YEAR, MONTH, DATE); funções matemáticas e de agregação (ROUND, FLOOR, cálculo de percentual, COUNT, COUNT DISTINCT, AVG, MIN e MAX); INNER JOIN, LEFT JOIN, RIGHT JOIN e autojunção; GROUP BY com uma e duas colunas; HAVING; e subconsultas que devolvem um valor e uma lista.</p>
<p class="nota">Ordem lógica em que o banco processa uma consulta: FROM e JOIN, depois WHERE, GROUP BY, HAVING, SELECT e, por fim, ORDER BY. As consultas que usam CURDATE() dependem do dia da execução; os resultados abaixo foram obtidos com a data do seminário, 30/11/2026, no MySQL 8.4.</p>
{consultas_html()}

<h2 class="quebra">7. Manutenção dos dados (INSERT, UPDATE e DELETE)</h2>
<p>O script <code>04_manutencao_dados.sql</code> mostra as operações do dia a dia, respeitando as regras do minimundo: a demanda nova nasce aberta pelo DEFAULT; a mudança de estado e a reatribuição são UPDATE com WHERE; o usuário é desativado em vez de excluído; e o DELETE só é usado para um vínculo de acompanhamento lançado por engano. O script também mostra a integridade referencial: apagar uma reunião que tem demandas é recusado pelo banco (erro 1451).</p>
<pre>{e(ler("04_manutencao_dados.sql"))}</pre>

<h2>8. Arquivos entregues e como executar</h2>
{tabela(['Arquivo', 'Conteúdo'], [
    ('01_criacao_banco.sql', 'DROP/CREATE DATABASE, CREATE TABLE das 6 tabelas e ALTER TABLE'),
    ('02_carga_dados.sql', 'INSERT dos dados fictícios em todas as tabelas'),
    ('03_consultas.sql', 'as 17 consultas, com o propósito de cada uma comentado'),
    ('04_manutencao_dados.sql', 'INSERT, UPDATE e DELETE de manutenção'),
    ('Documento_BD1_Equipe_Cortex.pdf', 'este documento'),
], 'dic')}
<p>Execução no MySQL 8 (Workbench ou linha de comando), nesta ordem: 01, 02, 03 e 04. Os quatro scripts foram executados do zero, sem erro, no MySQL 8.4.</p>

<h2 class="quebra">9. Apêndice: script de carga dos dados</h2>
<pre class="script">{e(ler("02_carga_dados.sql"))}</pre>

<h2>Referências</h2>
<p>HEUSER, Carlos Alberto. <i>Projeto de banco de dados</i>. 3. ed. Porto Alegre: Sagra Luzzatto, 2000.</p>
<p>ELMASRI, Ramez; NAVATHE, Shamkant B. <i>Sistemas de banco de dados: fundamentos e aplicações</i>. 3. ed. Rio de Janeiro: LTC, 2002.</p>
<p>EQUIPE CORTEX. <i>Especificação do minimundo: Sistema de Gestão de Demandas de Articulação</i>, versão 1.0. Bragança Paulista: IFSP, 2026.</p>
</body></html>'''


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    destino_html = os.path.join(RAIZ, 'ferramentas', 'documento.html')
    open(destino_html, 'w', encoding='utf-8').write(documento())
    open(os.path.join(RAIZ, 'entrega', 'DER_recorte_BD1.svg'), 'w', encoding='utf-8').write(der_svg())
    pdf = os.path.join(ENTREGA, 'Documento_BD1_Equipe_Cortex.pdf')
    edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    r = subprocess.run([edge, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={pdf}', 'file:///' + destino_html.replace('\\', '/')],
                       capture_output=True, text=True, timeout=120)
    print('PDF:', pdf, os.path.exists(pdf) and os.path.getsize(pdf), r.returncode)
