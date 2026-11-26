W, H = 1400, 1110
o = []; A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
A('<defs><marker id="aberta" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto"><path d="M0,0 L12,6 L0,12" fill="none" stroke="#222" stroke-width="1.5"/></marker>'
  '<marker id="heranca" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="16" markerHeight="16" orient="auto"><path d="M0,0 L13,7 L0,14 z" fill="#fff" stroke="#222" stroke-width="1.3"/></marker></defs>')
A(f'<rect width="{W}" height="{H}" fill="#fff"/>')
A('<rect x="300" y="40" width="1060" height="1050" fill="#FAFBFD" stroke="#1F3864" stroke-width="2"/>')
A('<text x="830" y="70" text-anchor="middle" font-size="20" font-weight="700" fill="#1F3864">Sistema de Demandas do CRIE</text>')
def ator(x, y, nome, sub=None):
    A(f'<circle cx="{x}" cy="{y}" r="16" fill="#fff" stroke="#222" stroke-width="2"/>')
    A(f'<line x1="{x}" y1="{y+16}" x2="{x}" y2="{y+60}" stroke="#222" stroke-width="2"/>')
    A(f'<line x1="{x-30}" y1="{y+32}" x2="{x+30}" y2="{y+32}" stroke="#222" stroke-width="2"/>')
    A(f'<line x1="{x}" y1="{y+60}" x2="{x-24}" y2="{y+95}" stroke="#222" stroke-width="2"/>')
    A(f'<line x1="{x}" y1="{y+60}" x2="{x+24}" y2="{y+95}" stroke="#222" stroke-width="2"/>')
    A(f'<text x="{x}" y="{y+120}" text-anchor="middle" font-size="21" font-weight="700">{nome}</text>')
    if sub:
        for i, s in enumerate(sub):
            A(f'<text x="{x}" y="{y+142+i*18}" text-anchor="middle" font-size="16">{s}</text>')
def uc(cx, cy, cod, nome, rx=185, ry=36):
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" stroke="#222" stroke-width="1.8"/>')
    A(f'<text x="{cx}" y="{cy-5}" text-anchor="middle" font-size="16" font-weight="700">{cod}</text>')
    A(f'<text x="{cx}" y="{cy+17}" text-anchor="middle" font-size="17">{nome}</text>')
c1, c2 = 560, 1110
ys = {'UC-001':110,'UC-004':196,'UC-005':282,'UC-006':368,'UC-007':454,'UC-008':540,'UC-009':626,'UC-010':712,'UC-003':836,'UC-011':922,'UC-012':1008}
nomes = {'UC-001':'Entrar no sistema','UC-004':'Registrar reunião de setor','UC-005':'Registrar demanda','UC-006':'Atualizar andamento da demanda',
 'UC-007':'Consultar demandas e histórico','UC-008':'Cadastrar e consultar assistido','UC-009':'Lançar e retificar evolução',
 'UC-010':'Registrar encaminhamento e desfecho','UC-003':'Gerir usuários','UC-011':'Emitir relatório','UC-012':'Consultar auditoria'}
# atores
ator(140, 300, 'Profissional', ['assistente social,', 'equipe pedagógica'])
ator(140, 840, 'Direção')
# herança Direção -> Profissional
A('<line x1="140" y1="822" x2="140" y2="482" stroke="#222" stroke-width="1.6" marker-end="url(#heranca)"/>')
# associações
for k in ['UC-001','UC-004','UC-005','UC-006','UC-007','UC-008','UC-009','UC-010']:
    A(f'<line x1="172" y1="340" x2="{c1-185}" y2="{ys[k]}" stroke="#222" stroke-width="1.3"/>')
for k in ['UC-003','UC-011','UC-012']:
    A(f'<line x1="172" y1="880" x2="{c1-185}" y2="{ys[k]}" stroke="#222" stroke-width="1.3"/>')
for k, y in ys.items():
    uc(c1, y, k, nomes[k])
# coluna 2
uc(c2, 110, 'UC-002', 'Ver aviso de prazo', rx=170)
uc(c2, 325, 'UC-014', 'Gravar histórico da demanda', rx=170)
uc(c2, 626, 'UC-013', 'Registrar auditoria', rx=170)
def dep(x1, y1, x2, y2, rot, lx, ly):
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="1.4" stroke-dasharray="7 5" marker-end="url(#aberta)"/>')
    A(f'<text x="{lx}" y="{ly}" font-size="15" fill="#222">{rot}</text>')
# extend: UC-002 -> UC-001
dep(c2-170, 110, c1+185, 110, '«extend»', 815, 100)
A('<text x="842" y="134" text-anchor="middle" font-size="12" fill="#222">[prazo vencido ou próximo]</text>')
# include para UC-014
dep(c1+185, 282, c2-170, 318, '«include»', 772, 280)
dep(c1+185, 368, c2-170, 334, '«include»', 772, 378)
# include para UC-013
dep(c1+185, 540, c2-170, 600, '«include»', 790, 544)
dep(c1+185, 626, c2-170, 620, '«include»', 790, 615)
dep(c1+185, 712, c2-170, 642, '«include»', 800, 718)
dep(c1+170, 908, c2-150, 660, '«include»', 812, 842)
# nota
A('<text x="830" y="1070" text-anchor="middle" font-size="13" fill="#444">UC-013 e UC-014 são executados pelo próprio sistema, sem ação direta do usuário.</text>')
A('</svg>')
open('diag/fig03_casos_de_uso.svg', 'w', encoding='utf-8').write('\n'.join(o))
