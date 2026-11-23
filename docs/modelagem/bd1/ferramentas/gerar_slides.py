# Gera os slides do seminário de BD1 (16:9, HTML -> PDF com o Edge sem interface).
import html, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conteudo import EQUIPE, RELACIONAMENTOS
from gerar_documento import der_svg, notacao_textual

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
e = html.escape

# Fala curta de cada consulta no slide (o detalhe está no documento e no guia).
RESUMO = {
    'Q01': 'LIKE com % aceita qualquer texto antes e depois; com OR basta uma condição.',
    'Q02': 'IN testa uma lista de valores; BETWEEN inclui os dois extremos; DATE_FORMAT só muda a exibição.',
    'Q03': 'WHERE tira as encerradas e as de prazo futuro; DATEDIFF calcula o atraso linha a linha.',
    'Q04': 'Janela de hoje até hoje + 7 dias com ADDDATE(... INTERVAL 7 DAY).',
    'Q05': 'Quatro tabelas ligadas pelas chaves estrangeiras; o INNER descarta demanda sem assistido.',
    'Q06': 'LEFT JOIN mantém todos os assistidos; IS NULL acha os que ficaram sem par.',
    'Q07': 'Filtro no ON, não no WHERE, para manter quem tem zero; COUNT(coluna) ignora NULL.',
    'Q08': 'HAVING filtra grupos depois do AVG; a prioridade alta (23,2 dias) sai.',
    'Q09': 'GROUP BY com duas colunas; a subconsulta devolve o total para o percentual.',
    'Q10': 'YEAR e MONTH formam um grupo por mês; COUNT(DISTINCT) conta categorias diferentes.',
    'Q11': 'A subconsulta devolve um valor (MIN), comparado com = pela consulta de fora.',
    'Q12': 'A subconsulta calcula a média uma vez; ficam as concluídas acima dela.',
    'Q13': 'A subconsulta devolve uma lista; NOT IN mantém quem não está nela.',
    'Q14': 'Passa pela tabela associativa do N:N; AVG em meses com ROUND, anos com FLOOR.',
    'Q15': 'Autojunção: evolucao duas vezes (original e nova), ligadas por retifica_id.',
    'Q16': 'NOT IN descarta versões substituídas; HAVING sobre MAX(data).',
    'Q17': 'RIGHT JOIN mantém todas as reuniões; COUNT(d.id) dá 0 nas sem demanda.',
}


def tabela(colunas, linhas, limite=7):
    def cel(v):
        v = str(v)
        return e(v if len(v) <= 48 else v[:46] + '…')
    th = ''.join(f'<th>{e(c)}</th>' for c in colunas)
    tr = ''.join('<tr>' + ''.join(f'<td>{cel(v)}</td>' for v in l) + '</tr>' for l in linhas[:limite])
    resto = f'<p class="mais">+ {len(linhas) - limite} linhas no documento</p>' if len(linhas) > limite else ''
    return f'<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{resto}'


def slide(titulo, corpo, classe=''):
    return f'<section class="s {classe}"><h2>{titulo}</h2><div class="c">{corpo}</div><footer>Equipe Cortex · BD1 · CRIE</footer></section>'


def slides():
    dados = json.load(open(os.path.join(AQUI, 'resultados.json'), encoding='utf-8'))
    s = [f'''<section class="s capa"><div>
<p class="topo">IFSP Bragança Paulista · ADS · Banco de Dados I</p>
<h1>Sistema de Gestão de Demandas de Articulação</h1>
<p class="sub">CRIE / APAE de Extrema-MG · Projeto Interdisciplinar</p>
<p class="eq">Equipe Cortex: {", ".join(EQUIPE)}</p></div></section>''']
    s.append(slide('O problema', '''<ul>
<li>O CRIE discute em <b>reuniões semanais</b> de cada setor as situações que exigem articulação com famílias e serviços da rede.</li>
<li>Cada situação vira uma <b>demanda</b>, com responsável, prazo e estado; hoje isso se perde em papel e mensagens.</li>
<li>Os profissionais registram <b>evoluções</b> dos assistidos, que nunca podem ser apagadas, só retificadas.</li>
<li>Dados de pessoas com deficiência: só o mínimo necessário (LGPD) e tudo fictício nesta entrega.</li></ul>'''))
    s.append(slide('Recorte desta disciplina: 6 tabelas', '''<ul>
<li>O sistema completo tem 12 entidades; BD1 pede de 4 a 6 tabelas.</li>
<li>Recorte central: <b>usuario, assistido, assistido_profissional, reuniao, demanda, evolucao</b>.</li>
<li>Os nomes são os mesmos do back-end (Flask), então o banco da disciplina e o do sistema contam a mesma história.</li>
<li>Ficaram de fora: encaminhamento, retorno, histórico, auditoria e participantes da reunião.</li></ul>'''))
    s.append(slide('Diagrama Entidade-Relacionamento', f'<div class="der">{der_svg()}</div>', 'cheio'))
    linhas = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td><b>{e(c)}</b></td><td>{e(d)}</td></tr>' for a, b, c, _, d in RELACIONAMENTOS)
    s.append(slide('Os três tipos de relacionamento', f'<table class="rel"><thead><tr><th>Relacionamento</th><th>Entidades</th><th>Tipo</th><th>Implementação</th></tr></thead><tbody>{linhas}</tbody></table>'))
    s.append(slide('Notação textual (modelo relacional)', f'<div class="nt">{notacao_textual()}</div><p class="obs">PK sublinhada · FK em itálico · tabelas em 3FN: o setor da demanda vem da reunião, sem cópia.</p>'))
    s.append(slide('Scripts de criação e carga', '''<div class="duas"><div><h3>01_criacao_banco.sql</h3><ul>
<li>DROP / CREATE DATABASE e CREATE TABLE das 6 tabelas</li><li>PK, FK, UNIQUE, NOT NULL, DEFAULT, AUTO_INCREMENT</li>
<li>ENUM para domínios fechados (estado, prioridade, setor, perfil)</li><li><b>ALTER TABLE</b> cria o 1:1: FK retifica_id com UNIQUE</li></ul></div>
<div><h3>02_carga_dados.sql</h3><ul><li>103 registros fictícios, pensados para cada consulta ter resultado</li>
<li>5 estados, 3 prioridades, prazos vencidos e próximos</li><li>Senhas só como hash: SHA2(..., 256)</li>
<li>Cadeia de retificações: 5 → 16 → 17</li></ul></div></div>'''))
    for q in dados:
        sql = re.sub(r'\n\s*\n', '\n', q['sql'])
        sql = re.sub(r'(?<=\S) {2,}', ' ', sql)  # tira o alinhamento extra antes do AS
        longa = ' class="longa"' if sql.count('\n') >= 12 else ''
        limite = 4 if len(q['colunas']) >= 6 else 6
        s.append(slide(f'{q["num"]}. {e(q["enunciado"])}', f'''<div class="duas q"><pre{longa}>{e(sql)}</pre>
<div>{tabela(q["colunas"], q["linhas"], limite)}</div></div><p class="fala"><b>Como processa:</b> {e(RESUMO[q["num"]])}</p>''', 'consulta'))
    s.append(slide('Manutenção: INSERT, UPDATE e DELETE', '''<ul>
<li><b>INSERT</b> de demanda sem estado: o DEFAULT a faz nascer <i>aberta</i>.</li>
<li><b>UPDATE</b> muda o estado e reatribui o responsável (sempre com WHERE).</li>
<li>Usuário é <b>desativado</b> com UPDATE, nunca excluído.</li>
<li><b>DELETE</b> só no vínculo de acompanhamento lançado por engano.</li>
<li>Integridade referencial: apagar reunião com demandas gera <b>erro 1451</b>.</li></ul>'''))
    s.append(slide('Do banco para o sistema', '''<table class="rel"><thead><tr><th>Consulta</th><th>Função no sistema</th><th>Rota do back-end</th></tr></thead><tbody>
<tr><td>Q03, Q11</td><td>Painel: demandas vencidas e a mais antiga</td><td>GET /api/demandas/painel</td></tr>
<tr><td>Q04</td><td>Aviso de prazo próximo ao entrar</td><td>login (card 25)</td></tr>
<tr><td>Q01, Q05</td><td>Busca e filtros de demandas</td><td>GET /api/demandas</td></tr>
<tr><td>Q07</td><td>Minhas demandas</td><td>GET /api/demandas/minhas</td></tr>
<tr><td>Q15, Q16</td><td>Retificação e evoluções vigentes</td><td>/api/evolucoes, /api/assistidos/&lt;id&gt;/evolucoes</td></tr>
<tr><td>Q02, Q17</td><td>Reuniões e demandas levantadas</td><td>GET /api/reunioes</td></tr>
<tr><td>Q08, Q09, Q10, Q12</td><td>Indicadores e relatórios da direção</td><td>/api/relatorios (card 24)</td></tr></tbody></table>'''))
    s.append('<section class="s capa"><div><h1>Obrigado!</h1><p class="sub">Perguntas?</p><p class="eq">Scripts e documento: 01 a 04 .sql + Documento_BD1_Equipe_Cortex.pdf</p></div></section>')
    return s


def pagina():
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Seminário BD1 - Equipe Cortex</title><style>
@page {{ size: 1280px 720px; margin: 0; }}
html {{ color-scheme: light; }}
body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #16231a; background: #fff; }}
.s {{ width: 1280px; height: 720px; box-sizing: border-box; padding: 46px 64px 40px; position: relative; page-break-after: always; overflow: hidden; }}
.s h2 {{ margin: 0 0 18px; font-size: 32px; color: #1f7a33; border-bottom: 3px solid #2f9e41; padding-bottom: 10px; }}
.s.consulta h2 {{ font-size: 24px; line-height: 1.25; }}
.c {{ font-size: 24px; line-height: 1.45; }}
.c li {{ margin: 0 0 12px; }}
footer {{ position: absolute; bottom: 16px; right: 64px; font-size: 13px; color: #8a958d; }}
.capa {{ display: flex; align-items: center; background: #1f7a33; color: #fff; }}
.capa h1 {{ font-size: 50px; margin: 10px 0; }} .capa .sub {{ font-size: 26px; }} .capa .topo {{ font-size: 18px; opacity: .85; }}
.capa .eq {{ font-size: 18px; margin-top: 40px; opacity: .9; }}
.cheio .c {{ height: 560px; }} .der svg {{ height: 550px; width: auto; display: block; margin: 0 auto; }}
pre.longa {{ font-size: 12.5px !important; }}
table {{ border-collapse: collapse; width: 100%; font-size: 17px; }}
th {{ background: #1f7a33; color: #fff; text-align: left; padding: 6px 8px; }} td {{ border-bottom: 1px solid #dfe8e1; padding: 5px 8px; }}
.q table {{ font-size: 13px; }} .q td, .q th {{ padding: 3px 5px; }}
.duas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }} .duas h3 {{ margin: 0 0 8px; font-size: 22px; }}
.duas.q {{ grid-template-columns: 1.05fr 1fr; }}
pre {{ margin: 0; font: 15px/1.35 Consolas, monospace; background: #f4f7f4; border-left: 4px solid #1f7a33; padding: 12px 14px; white-space: pre-wrap; }}
.fala {{ position: absolute; left: 64px; right: 64px; bottom: 44px; font-size: 19px; background: #eef6ef; padding: 10px 14px; margin: 0; }}
.mais {{ font-size: 13px; color: #5f6d63; margin: 4px 0 0; }}
.nt .rel-txt {{ font: 19px/1.4 Consolas, monospace; margin: 6px 0 0; }} .nt .ref {{ font-size: 14px; color: #5f6d63; margin: 0 0 6px 20px; }}
.obs {{ font-size: 17px; color: #5f6d63; }} table.rel {{ font-size: 18px; }}
</style></head><body>{"".join(slides())}</body></html>'''


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    destino = os.path.join(AQUI, 'slides.html')
    open(destino, 'w', encoding='utf-8').write(pagina())
    pdf = os.path.join(RAIZ, 'apresentacao', 'Slides_Seminario_BD1_Equipe_Cortex.pdf')
    os.makedirs(os.path.dirname(pdf), exist_ok=True)
    edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    r = subprocess.run([edge, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}',
                        'file:///' + destino.replace('\\', '/')], capture_output=True, text=True, timeout=120)
    print('PDF:', pdf, os.path.exists(pdf) and os.path.getsize(pdf), r.returncode)
