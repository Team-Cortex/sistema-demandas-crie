"""Funções auxiliares para preencher o modelo oficial (.docx) mantendo a formatação."""
import copy
import re

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

CINZA = {'7F7F7F', '595959'}


def W(tag):
    return qn('w:' + tag)


def texto(el):
    return ''.join(t.text or '' for t in el.iter(W('t')))


def corpo(doc):
    return list(doc.element.body.iterchildren())


def acha_paragrafo(doc, alvo, depois=None, exato=True):
    """Primeiro parágrafo do corpo com o texto pedido (depois de um elemento, se informado)."""
    ativo = depois is None
    for el in doc.element.body.iterchildren():
        if not ativo:
            if el is depois:
                ativo = True
            continue
        if el.tag == W('p'):
            t = texto(el).strip()
            if (t == alvo) if exato else t.startswith(alvo):
                return el
    raise KeyError(alvo)


def proxima_tabela(el):
    x = el.getnext()
    while x is not None and x.tag != W('tbl'):
        x = x.getnext()
    if x is None:
        raise KeyError('sem tabela depois de ' + texto(el)[:40])
    return x


def tabela_apos(doc, titulo, exato=True, depois=None):
    p = acha_paragrafo(doc, titulo, depois=depois, exato=exato)
    return Table(proxima_tabela(p), doc)


def _rpr_base(tc_ou_p, tamanho=None):
    """rPr do primeiro run com propriedades, sem cor cinza nem itálico de instrução."""
    rpr = None
    for r in tc_ou_p.iter(W('r')):
        x = r.find(W('rPr'))
        if x is not None and len(x):
            rpr = copy.deepcopy(x)
            break
    if rpr is None:
        rpr = OxmlElement('w:rPr')
        f = OxmlElement('w:rFonts')
        f.set(W('eastAsia'), 'Arial')
        f.set(W('cs'), 'Arial')
        rpr.append(f)
    for tag in ('color', 'i', 'iCs'):
        for x in rpr.findall(W(tag)):
            if tag != 'color' or x.get(W('val')) in CINZA:
                rpr.remove(x)
    if tamanho:
        for tag in ('sz', 'szCs'):
            for x in rpr.findall(W(tag)):
                rpr.remove(x)
        for tag in ('sz', 'szCs'):
            e = OxmlElement('w:' + tag)
            e.set(W('val'), str(tamanho))
            rpr.append(e)
    return rpr


def _sem_negrito(rpr):
    for tag in ('b', 'bCs'):
        for x in rpr.findall(W(tag)):
            rpr.remove(x)
    return rpr


def _com_negrito(rpr):
    _sem_negrito(rpr)
    b = OxmlElement('w:b')
    bcs = OxmlElement('w:bCs')
    # w:b deve vir depois de rFonts
    f = rpr.find(W('rFonts'))
    if f is not None:
        f.addnext(b)
        b.addnext(bcs)
    else:
        rpr.insert(0, bcs)
        rpr.insert(0, b)
    return rpr


def escreve_runs(p_el, conteudo, rpr, negrito_base=False):
    """Escreve texto com **negrito** marcado; quebra de linha com \n."""
    partes = re.split(r'(\*\*.+?\*\*|~~.+?~~)', conteudo, flags=re.S)
    for parte in partes:
        if not parte:
            continue
        neg = parte.startswith('**') and parte.endswith('**')
        peq = parte.startswith('~~') and parte.endswith('~~')
        s = parte[2:-2] if (neg or peq) else parte
        if peq:
            s = s.replace('_', '_​').replace('::', '::​').replace('; ', ';​ ')
        linhas = s.split('\n')
        for i, linha in enumerate(linhas):
            r = OxmlElement('w:r')
            rp = copy.deepcopy(rpr)
            if neg or negrito_base:
                _com_negrito(rp)
            else:
                _sem_negrito(rp)
            if peq:
                for tag in ('sz', 'szCs'):
                    for x in rp.findall(W(tag)):
                        rp.remove(x)
                for tag in ('sz', 'szCs'):
                    e = OxmlElement('w:' + tag)
                    e.set(W('val'), '15')
                    rp.append(e)
                cor = OxmlElement('w:color'); cor.set(W('val'), '404040'); rp.append(cor)
            r.append(rp)
            if i > 0:
                r.append(OxmlElement('w:br'))
            t = OxmlElement('w:t')
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            t.text = linha
            r.append(t)
            p_el.append(r)


def preenche_celula(cell, conteudo, negrito=None, tamanho=None, alinhamento=None):
    """conteudo: str ou lista de str (um parágrafo por item)."""
    tc = cell._tc if isinstance(cell, _Cell) else cell
    ps = tc.findall(W('p'))
    ppr = copy.deepcopy(ps[0].find(W('pPr'))) if ps and ps[0].find(W('pPr')) is not None else None
    rpr = _rpr_base(tc, tamanho)
    if rpr.find(W('sz')) is None:
        tbl = tc.getparent().getparent() if tc.getparent() is not None else None
        sz = None
        if tbl is not None:
            for x in tbl.iter(W('sz')):
                if x.getparent().tag == W('rPr') and x.getparent().getparent().tag == W('r'):
                    sz = x.get(W('val'))
                    break
        if sz:
            for tag in ('sz', 'szCs'):
                e = OxmlElement('w:' + tag)
                e.set(W('val'), sz)
                rpr.append(e)
    if negrito is None:
        negrito = rpr.find(W('b')) is not None
    for p in ps:
        tc.remove(p)
    if isinstance(conteudo, str):
        conteudo = [conteudo]
    if not conteudo:
        conteudo = ['']
    for item in conteudo:
        p = OxmlElement('w:p')
        if ppr is not None:
            pp = copy.deepcopy(ppr)
            if alinhamento:
                for j in pp.findall(W('jc')):
                    pp.remove(j)
                jc = OxmlElement('w:jc')
                jc.set(W('val'), alinhamento)
                pp.append(jc)
            p.append(pp)
        escreve_runs(p, item, rpr, negrito_base=negrito)
        tc.append(p)


def preenche_linhas(table, linhas, prototipo=1, cabecalho=1):
    """Substitui as linhas de dados da tabela por 'linhas' (lista de listas)."""
    tbl = table._tbl
    trs = tbl.findall(W('tr'))
    proto = copy.deepcopy(trs[prototipo])
    for tr in trs[cabecalho:]:
        tbl.remove(tr)
    for valores in linhas:
        novo = copy.deepcopy(proto)
        # tira o cabeçalho repetido, se houver
        trpr = novo.find(W('trPr'))
        if trpr is not None:
            for x in trpr.findall(W('tblHeader')):
                trpr.remove(x)
        tbl.append(novo)
        tcs = novo.findall(W('tc'))
        for tc, v in zip(tcs, valores):
            preenche_celula(_Cell(tc, table), v)


def preenche_chave_valor(table, valores, col=1):
    """valores: dict rótulo -> conteúdo; ou lista na ordem das linhas."""
    for i, row in enumerate(table.rows):
        rot = row.cells[0].text.strip()
        if isinstance(valores, dict):
            if rot in valores:
                preenche_celula(row.cells[col], valores[rot])
        else:
            if i < len(valores) and valores[i] is not None:
                preenche_celula(row.cells[col], valores[i])


def remove(el):
    el.getparent().remove(el)


def paragrafo_depois(ref_el, conteudo, modelo_el=None, tamanho=None, negrito=False, alinhamento=None, estilo=None):
    """Cria parágrafo depois de ref_el copiando o pPr de modelo_el (ou um pPr padrão)."""
    p = OxmlElement('w:p')
    if modelo_el is not None and modelo_el.find(W('pPr')) is not None:
        ppr = copy.deepcopy(modelo_el.find(W('pPr')))
        for x in ppr.findall(W('sectPr')):
            ppr.remove(x)
        for x in ppr.findall(W('keepNext')):
            ppr.remove(x)
    else:
        ppr = OxmlElement('w:pPr')
        ps = OxmlElement('w:pStyle')
        ps.set(W('val'), 'Normal')
        ppr.append(ps)
        sp = OxmlElement('w:spacing')
        sp.set(W('lineRule'), 'auto')
        sp.set(W('line'), '276')
        sp.set(W('before'), '0')
        sp.set(W('after'), '120')
        ppr.append(sp)
        jc = OxmlElement('w:jc')
        jc.set(W('val'), 'both')
        ppr.append(jc)
    if estilo:
        ps = ppr.find(W('pStyle'))
        ps.set(W('val'), estilo)
    if alinhamento:
        for j in ppr.findall(W('jc')):
            ppr.remove(j)
        jc = OxmlElement('w:jc')
        jc.set(W('val'), alinhamento)
        ppr.append(jc)
    p.append(ppr)
    rpr = OxmlElement('w:rPr')
    f = OxmlElement('w:rFonts')
    f.set(W('eastAsia'), 'Arial')
    f.set(W('cs'), 'Arial')
    rpr.append(f)
    if tamanho:
        for tag in ('sz', 'szCs'):
            e = OxmlElement('w:' + tag)
            e.set(W('val'), str(tamanho))
            rpr.append(e)
    escreve_runs(p, conteudo, rpr, negrito_base=negrito)
    ref_el.addnext(p)
    return p


def substitui_texto_paragrafo(p_el, novo, manter_negrito=True):
    """Troca o texto do parágrafo (que pode ter runs cinza de instrução)."""
    rpr = _rpr_base(p_el)
    for r in p_el.findall(W('r')):
        p_el.remove(r)
    escreve_runs(p_el, novo, rpr)


def figura_na_celula(doc, table, imagem, legenda, fonte, largura_cm=15.5):
    """Coloca a imagem no lugar do marcador e ajusta a legenda e a fonte."""
    tc = table.rows[0].cells[0]._tc
    ps = tc.findall(W('p'))
    leg_rpr = None
    ppr = copy.deepcopy(ps[0].find(W('pPr')))
    for p in ps:
        if texto(p).startswith('Figura'):
            leg_rpr = _rpr_base(p)
        tc.remove(p)
    # imagem
    p_img = OxmlElement('w:p')
    pi = copy.deepcopy(ppr)
    jc = OxmlElement('w:jc'); jc.set(W('val'), 'center'); pi.append(jc)
    p_img.append(pi)
    tc.append(p_img)
    par = Paragraph(p_img, table._parent)
    par.add_run().add_picture(imagem, width=Cm(largura_cm))
    # legenda
    p_leg = OxmlElement('w:p')
    pl = copy.deepcopy(ppr)
    jc = OxmlElement('w:jc'); jc.set(W('val'), 'center'); pl.append(jc)
    p_leg.append(pl)
    escreve_runs(p_leg, legenda, leg_rpr if leg_rpr is not None else _rpr_base(tc), negrito_base=True)
    tc.append(p_leg)
    p_fonte = OxmlElement('w:p')
    pf = copy.deepcopy(ppr)
    jc = OxmlElement('w:jc'); jc.set(W('val'), 'center'); pf.append(jc)
    p_fonte.append(pf)
    escreve_runs(p_fonte, fonte, _rpr_base(tc, tamanho=17))
    tc.append(p_fonte)


def clona_depois(ref_el, *els):
    """Copia els (na ordem) para depois de ref_el; devolve as cópias e o último elemento."""
    copias = []
    atual = ref_el
    for e in els:
        c = copy.deepcopy(e)
        atual.addnext(c)
        atual = c
        copias.append(c)
    return copias, atual


def paragrafo_vazio_depois(ref_el):
    p = OxmlElement('w:p')
    ppr = OxmlElement('w:pPr')
    ps = OxmlElement('w:pStyle'); ps.set(W('val'), 'Normal'); ppr.append(ps)
    sp = OxmlElement('w:spacing'); sp.set(W('before'), '0'); sp.set(W('after'), '0'); ppr.append(sp)
    p.append(ppr)
    ref_el.addnext(p)
    return p


def remove_blocos_conteudo(doc):
    """Remove os rótulos 'Conteúdo'/'Orientação' e o parágrafo de instrução (itálico cinza) que vem depois."""
    removidos = 0
    for el in list(doc.element.body.iterchildren()):
        if el.tag != W('p'):
            continue
        t = texto(el).strip()
        if t in ('Conteúdo', 'Orientação'):
            prox = el.getnext()
            remove(el)
            removidos += 1
            if prox is not None and prox.tag == W('p'):
                cores = {c.get(W('val')) for c in prox.iter(W('color'))}
                italico = prox.find('.//' + W('i')) is not None
                if italico and cores & CINZA:
                    remove(prox)
    return removidos


def larguras(table, lista):
    tbl = table._tbl
    grid = tbl.find(W('tblGrid'))
    for gc, w in zip(grid.findall(W('gridCol')), lista):
        gc.set(W('w'), str(w))
    for tr in tbl.findall(W('tr')):
        for tc, w in zip(tr.findall(W('tc')), lista):
            tcw = tc.find(W('tcPr')).find(W('tcW'))
            tcw.set(W('w'), str(w))
