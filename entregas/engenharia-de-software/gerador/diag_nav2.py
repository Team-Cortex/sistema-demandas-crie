W, H = 1300, 900
o = []; A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
A('<defs><marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>')
A(f'<rect width="{W}" height="{H}" fill="#fff"/>')
def box(x, y, w, h, tid, linhas, tipo='normal'):
    fill = {'normal': '#EEF2FA', 'dir': '#FFF7E6', 'dlg': '#F3F3F3'}[tipo]
    dash = ' stroke-dasharray="7 5"' if tipo == 'dlg' else ''
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#1F3864" stroke-width="2"{dash}/>')
    yy = y + 26
    if tid:
        A(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="19" font-weight="700" fill="#1F3864">{tid}</text>')
        yy += 24
    else:
        yy = y + h/2 - (len(linhas)-1)*11 + 7
    for i, l in enumerate(linhas):
        A(f'<text x="{x+w/2}" y="{yy+i*22}" text-anchor="middle" font-size="19">{l}</text>')
    return (x, y, w, h)
def seta(x1, y1, x2, y2, dash=False):
    d = ' stroke-dasharray="6 4"' if dash else ''
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="2"{d} marker-end="url(#s)"/>')
def baixo(a, b):
    seta(a[0]+a[2]/2, a[1]+a[3], b[0]+b[2]/2, b[1]-2)
CW, G = 240, 15
xs = [20 + i*(CW+G) for i in range(5)]
t01 = box(520, 15, 260, 62, 'T-01', ['Entrar'])
t02 = box(520, 115, 260, 62, 'T-02', ['Painel (tela inicial)'])
baixo(t01, t02)
box(1010, 115, 270, 62, None, ['Sair, de qualquer tela,', 'volta para T-01'], 'dlg')
# barramento do nível 1
A(f'<line x1="650" y1="177" x2="650" y2="205" stroke="#333" stroke-width="2"/>')
A(f'<line x1="{xs[0]+CW/2}" y1="205" x2="{xs[4]+CW/2}" y2="205" stroke="#333" stroke-width="2"/>')
n1 = []
for x, (tid, nome) in zip(xs, [('T-03', 'Minhas demandas'), ('T-04', 'Demandas'), ('T-07', 'Reuniões'), ('T-10', 'Assistidos'), ('T-15', 'Encaminhamentos')]):
    seta(x+CW/2, 205, x+CW/2, 233)
    n1.append(box(x, 235, CW, 62, tid, [nome]))
# Demandas
t05 = box(xs[1], 335, CW, 62, 'T-05', ['Registrar demanda']); baixo(n1[1], t05)
dc = box(xs[1], 425, CW, 56, None, ['confirmar registro'], 'dlg'); baixo(t05, dc)
t06 = box(xs[1], 510, CW, 62, 'T-06', ['Demanda (detalhe)']); baixo(dc, t06)
d1 = box(xs[1], 600, CW, 44, None, ['mudar estado'], 'dlg')
d2 = box(xs[1], 652, CW, 44, None, ['trocar responsável'], 'dlg')
d3 = box(xs[1], 704, CW, 44, None, ['anotar'], 'dlg')
baixo(t06, d1)
# Minhas -> detalhe
A(f'<path d="M{xs[0]+CW/2},297 L{xs[0]+CW/2},541 L{xs[1]-3},541" fill="none" stroke="#333" stroke-width="2" marker-end="url(#s)"/>')
# Reuniões
t08 = box(xs[2], 335, CW, 62, 'T-08', ['Registrar ou editar']); baixo(n1[2], t08)
t09 = box(xs[2], 425, CW, 62, 'T-09', ['Reunião (ficha)'])
A(f'<path d="M{xs[2]+CW-10},297 L{xs[2]+CW-10},318 L{xs[2]+CW+7},318 L{xs[2]+CW+7},456 L{xs[2]+CW+1},456" fill="none" stroke="#333" stroke-width="2" marker-end="url(#s)"/>')
A(f'<path d="M{xs[2]+CW/2},487 L{xs[2]+CW/2},530 L{xs[1]+CW+3},530" fill="none" stroke="#333" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#s)"/>')
A(f'<text x="{xs[2]+12}" y="560" font-size="16" fill="#333">nova demanda desta reunião</text>')
# Assistidos
t11 = box(xs[3], 335, CW, 62, 'T-11', ['Cadastrar assistido']); baixo(n1[3], t11)
t12 = box(xs[3], 425, CW, 62, 'T-12', ['Ficha do assistido'])
A(f'<path d="M{xs[3]+CW-10},297 L{xs[3]+CW-10},318 L{xs[3]+CW+7},318 L{xs[3]+CW+7},456 L{xs[3]+CW+1},456" fill="none" stroke="#333" stroke-width="2" marker-end="url(#s)"/>')
t13 = box(xs[3], 515, CW, 62, 'T-13', ['Lançar evolução']); baixo(t12, t13)
t14 = box(xs[3], 605, CW, 62, 'T-14', ['Evolução (versões)']); baixo(t13, t14)
# Encaminhamentos
de = box(xs[4], 335, CW, 56, None, ['desfecho (uma vez)'], 'dlg'); baixo(n1[4], de)
t16 = box(xs[4], 425, CW, 62, 'T-16', ['Novo encaminhamento'])
A(f'<text x="{xs[4]+CW/2}" y="512" text-anchor="middle" font-size="16" fill="#333">aberto pela demanda (T-06)</text>')
A(f'<text x="{xs[4]+CW/2}" y="532" text-anchor="middle" font-size="16" fill="#333">ou pela ficha (T-12)</text>')
# Direção
A(f'<rect x="{xs[3]-5}" y="700" width="{2*CW+G+10}" height="185" rx="8" fill="none" stroke="#B07A1C" stroke-width="2" stroke-dasharray="8 5"/>')
A(f'<text x="{xs[3]+5}" y="724" font-size="17" font-weight="700" fill="#7A5310">Só a Direção (fora do menu dos outros perfis)</text>')
box(xs[3]+5, 740, 150, 62, 'T-17', ['Usuários'], 'dir')
box(xs[3]+5+165, 740, 150, 62, 'T-18', ['Relatórios'], 'dir')
box(xs[3]+5+330, 740, 150, 62, 'T-19', ['Auditoria'], 'dir')
A(f'<text x="{xs[3]+5}" y="835" font-size="16" fill="#333">Acesso pelo menu lateral, a partir de</text>')
A(f'<text x="{xs[3]+5}" y="855" font-size="16" fill="#333">qualquer tela, como os itens do nível 1.</text>')
# legenda
A('<rect x="20" y="790" width="26" height="18" fill="#EEF2FA" stroke="#1F3864"/><text x="56" y="805" font-size="17">tela para todos os perfis</text>')
A('<rect x="20" y="820" width="26" height="18" fill="#FFF7E6" stroke="#1F3864"/><text x="56" y="835" font-size="17">tela só da Direção</text>')
A('<rect x="20" y="850" width="26" height="18" fill="#F3F3F3" stroke="#1F3864" stroke-dasharray="4 3"/><text x="56" y="865" font-size="17">diálogo ou ação dentro da tela</text>')
A('<text x="300" y="805" font-size="17">Profundidade máxima: três níveis</text>')
A('<text x="300" y="827" font-size="17">a partir do Painel.</text>')
A('</svg>')
open('diag/fig04_mapa_navegacao.svg', 'w', encoding='utf-8').write('\n'.join(o))
