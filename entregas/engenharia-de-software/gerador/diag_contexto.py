# Diagrama de contexto do trabalho (Volere 6b)
W, H = 1400, 900
cx, cy = 700, 450
out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
A('<defs><marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker></defs>')
A(f'<rect width="{W}" height="{H}" fill="#fff"/>')
# trabalho no centro
A(f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="120" fill="#EEF2FA" stroke="#1F3864" stroke-width="2.5"/>')
for i, t in enumerate(["Trabalho estudado:", "registro e acompanhamento das", "demandas de articulação de rede", "do CRIE (com o sistema web)"]):
    A(f'<text x="{cx}" y="{cy-40+i*28}" text-anchor="middle" font-size="{22 if i==0 else 21}" font-weight="{700 if i==0 else 400}" fill="#1F3864">{t}</text>')
def caixa(x, y, w, h, linhas, tracejada=False):
    dash = ' stroke-dasharray="8 6"' if tracejada else ''
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="#222" stroke-width="2"{dash}/>')
    for i, t in enumerate(linhas):
        A(f'<text x="{x+w/2}" y="{y+29+i*23}" text-anchor="middle" font-size="{20 if i==0 else 16}" font-weight="{700 if i==0 else 400}" fill="#222">{t}</text>')
def seta(x1, y1, x2, y2, rot, lx, ly, anchor="middle", tracejada=False):
    dash = ' stroke-dasharray="8 6"' if tracejada else ''
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="1.6" marker-end="url(#seta)"{dash}/>')
    for i, t in enumerate(rot):
        A(f'<text x="{lx}" y="{ly+i*21}" text-anchor="{anchor}" font-size="17" fill="#222">{t}</text>')
# entidades externas
caixa(40, 60, 300, 80, ["Direção do CRIE", "cliente; perfil Direção"])
caixa(1060, 60, 300, 80, ["Profissionais do CRIE", "assistente social, equipe pedagógica"])
caixa(40, 740, 330, 100, ["Rede de serviços públicos", "CRAS, CAPSi, UBS, escola, conselho", "(sem integração com o sistema)"])
caixa(1060, 750, 300, 80, ["Família da pessoa atendida", "(não usa o sistema)"])
caixa(560, 40, 280, 80, ["Prefeitura de Extrema", "fora do escopo (seção 8a)"], tracejada=True)
# Direção <-> trabalho
seta(320, 140, 560, 345, ["cadastro de profissionais,", "pedido de relatório,", "decisão de acesso"], 470, 200, "start")
seta(480, 420, 150, 140, ["painel de pendências,", "relatórios do período,", "registros de auditoria"], 290, 330, "end")
# Profissionais <-> trabalho
seta(1080, 140, 840, 345, ["demandas, andamento,", "anotações, evoluções,", "encaminhamentos"], 915, 205, "end")
seta(920, 420, 1250, 140, ["aviso de prazo,", "minhas demandas,", "histórico consultado"], 1110, 330, "start")
# Rede
seta(540, 535, 300, 740, ["encaminhamento", "(ofício, ligação, visita)"], 430, 650, "start")
seta(120, 740, 490, 505, ["retorno da rede", "(registrado como", "desfecho)"], 225, 600, "end")
# Família
seta(1280, 750, 910, 505, ["pedido de informação", "sobre o que já foi feito"], 1175, 640, "start")
seta(860, 560, 1100, 750, ["resposta da equipe", "a partir do histórico"], 960, 680, "end")
# Prefeitura (tracejada)
seta(700, 330, 700, 122, ["resumo de atendimento", "feito por profissional"], 712, 150, "start", tracejada=True)
A('</svg>')
open('diag/fig01_contexto.svg', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
