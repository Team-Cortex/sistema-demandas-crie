# Confere o deck gerado: texto >= 24 px (a 1920x1080), contraste AA, nada fora do slide ou sobre o rodapé,
# nenhum corte de texto e nenhum travessão. Com --prints, salva um PNG por slide e folhas de contato.
# Uso: python qa_deck.py [--prints]
import json
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PERFIL = os.path.join(tempfile.gettempdir(), 'perfil-edge-qa')

QA_JS = r'''
(async()=>{
await document.fonts.ready;
const lum=c=>{const m=c.match(/[\d.]+/g).map(Number);const v=m.slice(0,3).map(x=>{x/=255;return x<=0.03928?x/12.92:Math.pow((x+0.055)/1.055,2.4)});return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]};
const alfa=c=>{const m=c.match(/[\d.]+/g);return m&&m.length>3?Number(m[3]):1};
function fundo(el){while(el&&el.nodeType===1){const b=getComputedStyle(el).backgroundColor;if(b&&alfa(b)>0.5&&!/^rgba?\(0, 0, 0, 0\)/.test(b))return b;el=el.parentElement}return 'rgb(255, 255, 255)'}
const saida=[];
slides.forEach((s,i)=>{mostrar(i);const sr=s.getBoundingClientRect();const p=[];
 const rod=s.querySelector('.rodape'),nota=s.querySelector('.nota-baixo');
 const limRod=rod?rod.getBoundingClientRect().top:sr.bottom,limNota=nota?nota.getBoundingClientRect().top:limRod;
 let fundoConteudo=0;
 for(const el of s.querySelectorAll('*')){
  if(el.closest('svg')&&!['text'].includes(el.tagName))continue;
  const r=el.getBoundingClientRect();if(r.width===0&&r.height===0)continue;
  const dentroRod=rod&&rod.contains(el),dentroNota=nota&&nota.contains(el);
  if(r.right>sr.right+1||r.bottom>sr.bottom+1||r.left<sr.left-1||r.top<sr.top-1)p.push(['fora_do_slide',String(el.className||el.tagName),(el.textContent||'').trim().slice(0,40)]);
  if(!dentroRod&&!dentroNota&&!el.closest('.capa-hero,.capa-topo')&&!el.classList.contains('blob'))fundoConteudo=Math.max(fundoConteudo,r.bottom);
  const texto=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
  if(!texto)continue;
  const cs=getComputedStyle(el);let fs=parseFloat(cs.fontSize);
  if(el.tagName==='text'){const svg=el.ownerSVGElement;fs=fs*svg.getBoundingClientRect().width/svg.viewBox.baseVal.width/(sr.width/1920)}
  if(fs<23.5)p.push(['fonte_pequena',String(el.className||el.tagName),el.textContent.trim().slice(0,40),fs.toFixed(1)]);
  if(el.tagName==='TD'){if(el.scrollWidth>el.clientWidth+1)p.push(['reticencias',el.textContent.trim().slice(0,40)])}
  else if(el.tagName==='TH'){if(el.scrollWidth>el.clientWidth+1)p.push(['cabecalho_cortado',el.textContent.trim()])}
  else if(el.scrollWidth>el.clientWidth+2&&cs.overflow!=='visible')p.push(['corte',String(el.className||el.tagName),el.textContent.trim().slice(0,40)]);
  const cor=el.tagName==='text'?cs.fill:cs.color,bg=fundo(el);
  const L1=lum(cor),L2=lum(bg),cr=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
  const grande=fs>=31.5||(fs>=23.5&&parseInt(cs.fontWeight)>=700);
  if(cr<(grande?3:4.5))p.push(['contraste',String(el.className||el.tagName),el.textContent.trim().slice(0,30),cr.toFixed(2),cor,bg]);
  if(/[\u2013\u2014]/.test(el.textContent))p.push(['travessao',el.textContent.trim().slice(0,40)]);
 }
 const alvo=nota?limNota:limRod;
 if(fundoConteudo>alvo-6)p.push(['encosta_'+(nota?'na_nota':'no_rodape'),Math.round(fundoConteudo-sr.top),Math.round(alvo-sr.top)]);
 saida.push({n:i+1,rotulo:s.getAttribute('aria-label'),folga:Math.round(alvo-fundoConteudo),p});
});
const pre=document.createElement('pre');pre.id='qa';pre.textContent=JSON.stringify(saida);document.body.appendChild(pre);
})();
'''


def edge(*args, timeout=120):
    return subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={PERFIL}',
                           '--window-size=1920,1080', *args], capture_output=True, text=True, encoding='utf-8', timeout=timeout)


def checar():
    html = open(os.path.join(AQUI, 'index.html'), encoding='utf-8').read()
    tmp = os.path.join(tempfile.gettempdir(), 'deck-qa.html')
    open(tmp, 'w', encoding='utf-8').write(html.replace('</body>', f'<script>{QA_JS}</script></body>'))
    r = edge('--virtual-time-budget=15000', '--dump-dom', 'file:///' + tmp.replace('\\', '/'))
    m = re.search(r'<pre id="qa">(.*?)</pre>', r.stdout, re.S)
    if not m:
        print('QA não rodou', r.stderr[-800:])
        sys.exit(1)
    dados = json.loads(html_unescape(m.group(1)))
    total = 0
    for s in dados:
        tipos = {}
        for prob in s['p']:
            tipos.setdefault(prob[0], []).append(prob[1:])
        if tipos:
            total += len(s['p'])
            print(f"{s['n']:02d} {s['rotulo']} (folga {s['folga']} px)")
            for t, itens in tipos.items():
                print('   ', t, len(itens), itens[:3])
    print('slides:', len(dados), '· problemas:', total, '· folgas:', [s['folga'] for s in dados])
    return dados


def html_unescape(t):
    import html
    return html.unescape(t)


def prints(n):
    """Um PNG 1920x1080 por página do PDF (o PDF sai do mesmo HTML, sem escala)."""
    import fitz
    from PIL import Image
    pasta = os.path.join(AQUI, 'prints')
    os.makedirs(pasta, exist_ok=True)
    for velho in os.listdir(pasta):
        os.remove(os.path.join(pasta, velho))
    doc = fitz.open(os.path.join(AQUI, 'Seminario_BD1_Equipe_Cortex.pdf'))
    if len(doc) != n:
        print('ATENÇÃO: o PDF tem', len(doc), 'páginas e o deck tem', n, 'slides')
    for i, pag in enumerate(doc, 1):
        zoom = 1920 / pag.rect.width
        pag.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(os.path.join(pasta, f'slide-{i:02d}.png'))
    arquivos = sorted(f for f in os.listdir(pasta) if f.startswith('slide-'))
    for k in range(0, len(arquivos), 9):
        folha = Image.new('RGB', (1920, 1080), '#0E1013')
        for j, nome in enumerate(arquivos[k:k + 9]):
            im = Image.open(os.path.join(pasta, nome)).convert('RGB').resize((632, 356), Image.LANCZOS)
            folha.paste(im, (6 + (j % 3) * 638, 6 + (j // 3) * 360))
        folha.save(os.path.join(pasta, f'folha-{k // 9 + 1}.png'))
    print('prints em', pasta)


if __name__ == '__main__':
    d = checar()
    if '--prints' in sys.argv:
        prints(len(d))
