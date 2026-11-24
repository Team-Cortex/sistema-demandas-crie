"""Construtor do relatório em .docx no padrão visual do relatório v3 (ABNT).

Marcações aceitas nos textos:
  **negrito**   ->  negrito
  [[texto]]     ->  [texto] com realce amarelo (item a preencher pela equipe)
"""
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX,
                            WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONTE = "Arial"
LARGURA_TEXTO = 16.0  # cm (21 - 3 - 2)
TOKENS = re.compile(r"(\*\*.+?\*\*|\[\[.+?\]\])")


def _fonte_rpr(rpr_parent, nome=FONTE):
    """Força Arial em todos os alfabetos, removendo fontes de tema."""
    rpr = rpr_parent.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for att in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(att)) is not None:
            del rfonts.attrib[qn(att)]
    for att in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(att), nome)


def _sombrear(celula, cor="E6E6E6"):
    tcpr = celula._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), cor)
    tcpr.append(shd)


def _bordas(tabela, cor="555555", tam="6"):
    tblpr = tabela._tbl.tblPr
    bordas = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{lado}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), tam)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), cor)
        bordas.append(b)
    tblpr.append(bordas)


def _margens_celula(tabela, cm=0.12):
    tblpr = tabela._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for lado in ("top", "left", "bottom", "right"):
        m = OxmlElement(f"w:{lado}")
        m.set(qn("w:w"), str(int(cm * 567)))
        m.set(qn("w:type"), "dxa")
        mar.append(m)
    tblpr.append(mar)


def _larguras(tabela, larguras):
    """Largura fixa das colunas (tblGrid), respeitada pelo Word e pelo LibreOffice."""
    tblpr = tabela._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblpr.append(lay)
    tblw = tblpr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        tblpr.append(tblw)
    tblw.set(qn("w:w"), str(int(sum(larguras) * 567)))
    tblw.set(qn("w:type"), "dxa")
    for i, w in enumerate(larguras):
        tabela.columns[i].width = Cm(w)


def _cabecalho_repete(linha):
    trpr = linha._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trpr.append(el)


def _nao_quebrar_linha(linha):
    trpr = linha._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    trpr.append(el)


def _campo_pagina(paragrafo):
    run = paragrafo.add_run()
    ini = OxmlElement("w:fldChar")
    ini.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "1"
    fim = OxmlElement("w:fldChar")
    fim.set(qn("w:fldCharType"), "end")
    for el in (ini, instr, sep, txt, fim):
        run._r.append(el)
    run.font.name = FONTE
    run.font.size = Pt(10)
    _fonte_rpr(run._r)


class Relatorio:
    def __init__(self, registro):
        # registro: rótulo -> número, vindo da passagem anterior
        self.registro_anterior = registro or {}
        self.registro = {}
        self.cont = {"Figura": 0, "Quadro": 0, "Tabela": 0}
        self.titulos = []        # (nivel, texto)
        self.ilustracoes = []    # (tipo, numero, titulo)
        self.doc = Document()
        self._estilos()
        sec = self.doc.sections[0]
        sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
        sec.top_margin, sec.left_margin = Cm(3), Cm(3)
        sec.bottom_margin, sec.right_margin = Cm(2), Cm(2)
        sec.header_distance, sec.footer_distance = Cm(2), Cm(1.25)

    # ---------- estilos ----------
    def _estilos(self):
        st = self.doc.styles
        normal = st["Normal"]
        normal.font.name = FONTE
        normal.font.size = Pt(12)
        normal.font.color.rgb = RGBColor(0, 0, 0)
        _fonte_rpr(normal.element)
        pf = normal.paragraph_format
        pf.line_spacing = 1.5
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        from docx.enum.style import WD_STYLE_TYPE
        for tipo in ("Figura", "Quadro", "Tabela"):
            lg = st.add_style(f"Legenda {tipo}", WD_STYLE_TYPE.PARAGRAPH)
            lg.base_style = normal
            lg.font.size = Pt(10)
            lg.font.bold = True
            lp = lg.paragraph_format
            lp.first_line_indent = Cm(0)
            lp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            lp.space_before = Pt(6)
            lp.space_after = Pt(3)
            lp.line_spacing = 1.0
            lp.keep_with_next = True
        for nivel in (1, 2, 3, 4):
            tc = st.add_style(f"TOC {nivel}", WD_STYLE_TYPE.PARAGRAPH)
            tc.element.name_val = f"toc {nivel}"
            tc.base_style = normal
            tc.font.bold = nivel == 1
            tp = tc.paragraph_format
            tp.first_line_indent = Cm(0)
            tp.left_indent = Cm(0)
            tp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            tp.line_spacing = 1.5
            tp.tab_stops.add_tab_stop(Cm(LARGURA_TEXTO), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        for nivel in (1, 2, 3):
            h = st[f"Heading {nivel}"]
            h.font.name = FONTE
            h.font.size = Pt(12)
            h.font.bold = True
            h.font.italic = False
            h.font.color.rgb = RGBColor(0, 0, 0)
            _fonte_rpr(h.element)
            hp = h.paragraph_format
            hp.line_spacing = 1.5
            hp.space_before = Pt(18 if nivel == 1 else 12)
            hp.space_after = Pt(12 if nivel == 1 else 6)
            hp.keep_with_next = True
            hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            hp.first_line_indent = Cm(0)

    # ---------- referências cruzadas ----------
    def R(self, rotulo):
        return str(self.registro_anterior.get(rotulo, "?"))

    def _numerar(self, tipo, rotulo, titulo):
        self.cont[tipo] += 1
        n = self.cont[tipo]
        if len(f"{tipo} {n} — {titulo}") > 70:
            print("LEGENDA LONGA:", tipo, n, titulo)
        if rotulo:
            self.registro[rotulo] = n
        self.ilustracoes.append((tipo, n, titulo))
        return n

    # ---------- texto ----------
    def _runs(self, par, texto, tamanho=None, negrito=False, italico=False):
        for parte in TOKENS.split(texto):
            if not parte:
                continue
            if parte.startswith("**") and parte.endswith("**"):
                r = par.add_run(parte[2:-2])
                r.bold = True
            elif parte.startswith("[[") and parte.endswith("]]"):
                r = par.add_run("[" + parte[2:-2] + "]")
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW
                if negrito:
                    r.bold = True
            else:
                r = par.add_run(parte)
                if negrito:
                    r.bold = True
            if italico:
                r.italic = True
            if tamanho:
                r.font.size = Pt(tamanho)
        return par

    def p(self, texto, recuo=True, alinhamento=None, tamanho=None, espaco_depois=0,
          negrito=False, entrelinha=None, italico=False):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(1.25) if recuo else Cm(0)
        if alinhamento is not None:
            pf.alignment = alinhamento
        if espaco_depois:
            pf.space_after = Pt(espaco_depois)
        if entrelinha:
            pf.line_spacing = entrelinha
        self._runs(par, texto, tamanho=tamanho, negrito=negrito, italico=italico)
        return par

    def alineas(self, itens):
        for item in itens:
            par = self.doc.add_paragraph()
            pf = par.paragraph_format
            pf.left_indent = Cm(1.25)
            pf.first_line_indent = Cm(-0.6)
            self._runs(par, item)

    def quebra(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def titulo_sem_numero(self, texto, sumario=True):
        """Título centralizado (RESUMO, SUMÁRIO, REFERÊNCIAS...)."""
        par = self.doc.add_paragraph(style="Heading 1" if sumario else None)
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.space_after = Pt(18)
        r = par.add_run(texto)
        r.bold = True
        r.font.size = Pt(12)
        if sumario:
            self.titulos.append((0, texto))
        return par

    def h1(self, texto, nova_pagina=True):
        if nova_pagina:
            self.quebra_antes = True
        par = self.doc.add_paragraph(style="Heading 1")
        par.paragraph_format.page_break_before = nova_pagina
        par.paragraph_format.space_before = Pt(0)
        par.add_run(texto)
        self.titulos.append((1, texto))

    def h2(self, texto):
        par = self.doc.add_paragraph(style="Heading 2")
        par.add_run(texto)
        self.titulos.append((2, texto))

    def h3(self, texto):
        par = self.doc.add_paragraph(style="Heading 3")
        par.add_run(texto)
        self.titulos.append((3, texto))

    # ---------- ilustrações ----------
    def _legenda(self, tipo, n, titulo):
        par = self.doc.add_paragraph(style=f"Legenda {tipo}")
        par.add_run(f"{tipo} {n} — {titulo}")

    def _fonte(self, texto):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(3)
        pf.space_after = Pt(10)
        pf.line_spacing = 1.0
        self._runs(par, "Fonte: " + texto, tamanho=10)

    def figura(self, rotulo, titulo, caminho, fonte, largura_cm=LARGURA_TEXTO, nota=None):
        n = self._numerar("Figura", rotulo, titulo)
        self._legenda("Figura", n, titulo)
        par = self.doc.add_paragraph()
        par.paragraph_format.first_line_indent = Cm(0)
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.line_spacing = 1.0
        par.paragraph_format.keep_with_next = True
        par.add_run().add_picture(caminho, width=Cm(largura_cm))
        self._fonte(fonte if not nota else fonte + " " + nota)
        return n

    def figura_pendente(self, rotulo, titulo, descricao, arquivo, fonte):
        n = self._numerar("Figura", rotulo, titulo)
        self._legenda("Figura", n, titulo)
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        _bordas(t, cor="888888")
        _margens_celula(t, 0.3)
        _larguras(t, [LARGURA_TEXTO])
        _nao_quebrar_linha(t.rows[0])
        c = t.rows[0].cells[0]
        c.width = Cm(LARGURA_TEXTO)
        _sombrear(c, "F2F2F2")
        par = c.paragraphs[0]
        par.paragraph_format.first_line_indent = Cm(0)
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.line_spacing = 1.15
        par.paragraph_format.space_before = Pt(30)
        par.paragraph_format.space_after = Pt(6)
        r = par.add_run(f"[FIGURA {n}: {descricao}]")
        r.font.size = Pt(10)
        r.bold = True
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        par2 = c.add_paragraph()
        par2.paragraph_format.first_line_indent = Cm(0)
        par2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par2.paragraph_format.line_spacing = 1.15
        par2.paragraph_format.space_after = Pt(30)
        r2 = par2.add_run(f"Arquivo esperado: {arquivo}. Usar somente dados fictícios.")
        r2.font.size = Pt(10)
        r2.italic = True
        self._fonte(fonte)
        return n

    def _tabela(self, tipo, rotulo, titulo, cabecalho, linhas, fonte, larguras=None,
                tamanho=10, nota=None):
        n = self._numerar(tipo, rotulo, titulo)
        self._legenda(tipo, n, titulo)
        t = self.doc.add_table(rows=1, cols=len(cabecalho))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        _bordas(t)
        _margens_celula(t)
        larguras = larguras or [LARGURA_TEXTO / len(cabecalho)] * len(cabecalho)
        _larguras(t, larguras)
        for i, txt in enumerate(cabecalho):
            c = t.rows[0].cells[i]
            c.width = Cm(larguras[i])
            _sombrear(c)
            par = c.paragraphs[0]
            par.paragraph_format.first_line_indent = Cm(0)
            par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            par.paragraph_format.line_spacing = 1.0
            self._runs(par, txt, tamanho=tamanho, negrito=True)
        _cabecalho_repete(t.rows[0])
        for linha in linhas:
            row = t.add_row()
            _nao_quebrar_linha(row)
            for i, txt in enumerate(linha):
                c = row.cells[i]
                c.width = Cm(larguras[i])
                partes = str(txt).split("\n")
                for k, parte in enumerate(partes):
                    par = c.paragraphs[0] if k == 0 else c.add_paragraph()
                    par.paragraph_format.first_line_indent = Cm(0)
                    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    par.paragraph_format.line_spacing = 1.0
                    self._runs(par, parte, tamanho=tamanho)
        self._fonte(fonte if not nota else fonte + " " + nota)
        return n

    def quadro(self, rotulo, titulo, cabecalho, linhas, fonte, larguras=None, tamanho=10, nota=None):
        return self._tabela("Quadro", rotulo, titulo, cabecalho, linhas, fonte, larguras, tamanho, nota)

    def tabela(self, rotulo, titulo, cabecalho, linhas, fonte, larguras=None, tamanho=10, nota=None):
        return self._tabela("Tabela", rotulo, titulo, cabecalho, linhas, fonte, larguras, tamanho, nota)

    def codigo(self, titulo_quadro, texto, fonte, rotulo=None):
        n = self._numerar("Quadro", rotulo, titulo_quadro)
        self._legenda("Quadro", n, titulo_quadro)
        t = self.doc.add_table(rows=1, cols=1)
        _bordas(t, cor="888888")
        _margens_celula(t, 0.2)
        _larguras(t, [LARGURA_TEXTO])
        c = t.rows[0].cells[0]
        c.width = Cm(LARGURA_TEXTO)
        linhas = texto.rstrip("\n").split("\n")
        for k, linha in enumerate(linhas):
            par = c.paragraphs[0] if k == 0 else c.add_paragraph()
            par.paragraph_format.first_line_indent = Cm(0)
            par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            par.paragraph_format.line_spacing = 1.0
            r = par.add_run(linha if linha else " ")
            r.font.name = "Courier New"
            _fonte_rpr(r._r, "Courier New")
            r.font.size = Pt(8.5)
        self._fonte(fonte)
        return n

    # ---------- pré-textuais ----------
    def linha_centro(self, texto, negrito=False, espaco_antes=0, maiuscula=False, tamanho=12):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(espaco_antes)
        r = par.add_run(texto.upper() if maiuscula else texto)
        r.bold = negrito
        r.font.size = Pt(tamanho)
        return par

    def natureza(self, texto, espaco_antes=0):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.left_indent = Cm(8)
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(espaco_antes)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = par.add_run(texto)
        r.font.size = Pt(10)
        return par

    def nova_secao(self, reiniciar_em=None, numerar=False):
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        sec.top_margin, sec.left_margin = Cm(3), Cm(3)
        sec.bottom_margin, sec.right_margin = Cm(2), Cm(2)
        sec.header_distance, sec.footer_distance = Cm(2), Cm(1.25)
        sec.header.is_linked_to_previous = False
        sec.footer.is_linked_to_previous = False
        if reiniciar_em is not None:
            pg = OxmlElement("w:pgNumType")
            pg.set(qn("w:start"), str(reiniciar_em))
            sec._sectPr.append(pg)
        hp = sec.header.paragraphs[0]
        hp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.paragraph_format.first_line_indent = Cm(0)
        if numerar:
            _campo_pagina(hp)
        return sec

    def indice(self, instrucao, entradas):
        """Campo de índice (sumário ou lista) com o resultado já calculado.

        entradas: lista de (estilo, texto, pagina). No Word, "Atualizar campo" refaz o índice.
        """
        for k, (estilo, texto, pagina) in enumerate(entradas):
            par = self.doc.add_paragraph(style=estilo.lower())
            if k == 0:
                for tipo in ("begin", "instr", "separate"):
                    run = par.add_run()
                    if tipo == "instr":
                        el = OxmlElement("w:instrText")
                        el.set(qn("xml:space"), "preserve")
                        el.text = f" {instrucao} "
                    else:
                        el = OxmlElement("w:fldChar")
                        el.set(qn("w:fldCharType"), tipo)
                    run._r.append(el)
            par.add_run(f"{texto}	{pagina}")
            if k == len(entradas) - 1:
                el = OxmlElement("w:fldChar")
                el.set(qn("w:fldCharType"), "end")
                par.add_run()._r.append(el)

    def entrada_lista(self, texto, pagina, negrito=False, maiuscula=False, recuo_cm=0):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(recuo_cm)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.tab_stops.add_tab_stop(Cm(LARGURA_TEXTO), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r = par.add_run((texto.upper() if maiuscula else texto) + "\t" + str(pagina))
        r.bold = negrito
        return par

    def entrada_ilustracao(self, texto, pagina):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.line_spacing = 1.5
        pf.tab_stops.add_tab_stop(Cm(LARGURA_TEXTO), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        par.add_run(texto + "\t" + str(pagina))
        return par

    def referencia(self, texto):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.line_spacing = 1.0
        pf.space_after = Pt(12)
        self._runs(par, texto)
        return par

    def salvar(self, caminho):
        self.doc.save(caminho)
