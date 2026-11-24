"""Gera Relatorio_de_Projeto_v5.docx e .pdf em duas passagens (referências e páginas)."""
import os
import subprocess
import tempfile
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_lib import Relatorio  # noqa: E402
import conteudo_a as A  # noqa: E402
import conteudo_b as B  # noqa: E402
import conteudo_c as C  # noqa: E402

SAIDA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # entregas/extensao
TRAB = os.path.join(tempfile.gettempdir(), "crie-relatorio-v5")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
NOME = "Relatorio_de_Projeto_v5"


def montar(registro, paginas):
    d = Relatorio(registro)
    R = d.R
    A.capa(d)
    d.nova_secao(reiniciar_em=1, numerar=False)
    A.folha_de_rosto(d)
    A.resumo(d)
    A.historico(d, R)
    A.listas(d, paginas)
    A.sumario(d, paginas)
    d.nova_secao(reiniciar_em=paginas.get("_inicio", 13), numerar=True)
    A.secao1(d, R)
    A.secao2(d, R)
    B.secao3(d, R)
    C.secao4(d, R)
    C.secao5(d, R)
    C.secao6(d, R)
    C.secao7(d, R)
    C.finais(d, R)
    return d


def converter(docx):
    perfil = "file:///" + os.path.join(TRAB, "lo_perfil").replace("\\", "/")
    subprocess.run([SOFFICE, f"-env:UserInstallation={perfil}", "--headless", "--convert-to", "pdf",
                    "--outdir", os.path.dirname(docx), docx], check=True, capture_output=True, timeout=600)
    return docx[:-5] + ".pdf"


def _norm(s):
    return " ".join(s.split())


def localizar(pdf, d):
    doc = pymupdf.open(pdf)
    linhas = [[_norm(l) for l in p.get_text().split("\n") if l.strip()] for p in doc]
    inicio = next(i for i, ls in enumerate(linhas) if any("A curricularização da extensão" in l for l in ls))
    pag = {}
    atual = inicio
    for _nivel, texto in d.titulos:
        alvo = _norm(texto)[:45]
        for i in range(atual, len(linhas)):
            if any(l.startswith(alvo) or (len(l) > 20 and alvo.startswith(l)) for l in linhas[i]):
                pag["T:" + texto] = i  # capa não conta: índice 0-based = número exibido
                atual = i
                break
        else:
            print("NÃO ACHEI título:", texto)
    for tipo in ("Figura", "Quadro", "Tabela"):
        atual = 1
        for (t, n, _tit) in d.ilustracoes:
            if t != tipo:
                continue
            alvo = f"{t} {n} — "
            achou = False
            for i in range(atual, len(linhas)):
                if i < inicio and not (t == "Quadro" and n == 1):
                    continue
                if any(l.startswith(alvo) for l in linhas[i]):
                    pag[f"{t} {n}"] = i
                    atual = i
                    achou = True
                    break
            if not achou:
                print("NÃO ACHEI ilustração:", alvo)
    pag["_inicio"] = inicio
    pag["_titulos"] = list(d.titulos)
    pag["_ilustracoes"] = list(d.ilustracoes)
    return pag, len(doc)


def main():
    os.makedirs(TRAB, exist_ok=True)
    # passagem 1: números de figuras, quadros e tabelas
    d1 = montar({}, {"_titulos": [], "_ilustracoes": []})
    registro = d1.registro
    # passagem 2: com listas e sumário de tamanho final, ainda sem páginas
    d2 = montar(registro, {"_titulos": d1.titulos, "_ilustracoes": d1.ilustracoes})
    tmp = os.path.join(TRAB, NOME + ".docx")
    d2.salvar(tmp)
    paginas, n = localizar(converter(tmp), d2)
    print("passagem 2:", n, "páginas")
    # passagem 3: com as páginas
    d3 = montar(registro, paginas)
    final = os.path.join(SAIDA, NOME + ".docx")
    d3.salvar(final)
    pdf = converter(final)
    conferido, n3 = localizar(pdf, d3)
    dif = [k for k in paginas if not k.startswith("_") and paginas[k] != conferido.get(k)]
    print("passagem 3:", n3, "páginas; divergências:", dif)
    faltando = [k for k, v in d3.registro.items() if registro.get(k) != v]
    print("rótulos divergentes:", faltando)
    print("figuras:", d3.cont)
    print(pdf)


if __name__ == "__main__":
    main()
