# Gerador do relatório v5

Scripts que montam `../Relatorio_de_Projeto_v5.docx` e o `.pdf` (python-docx + LibreOffice), em três passagens para acertar a numeração das figuras, quadros, tabelas e páginas do sumário.

| Arquivo | Conteúdo |
|---|---|
| `gerar.py` | Ponto de entrada: gera o .docx, converte para PDF e confere a numeração |
| `build_lib.py` | Classe `Relatorio`: estilos ABNT, sumário, listas, figuras, quadros e tabelas |
| `conteudo_a.py` | Elementos pré-textuais, introdução e relato do contato com o CRIE |
| `conteudo_b.py` | Desenvolvimento por disciplina (seção 3) |
| `conteudo_c.py` | Resultados, validação, conclusão, referências e apêndices |

## Como gerar
Requisitos: Python 3 com `python-docx` e `pymupdf`, e o LibreOffice instalado (`SOFFICE` em `gerar.py`).

```bash
python entregas/extensao/gerador/gerar.py
```

As figuras vêm de `../figuras/`. Os prints ainda pendentes aparecem como caixas cinzas "[FIGURA N: …]"; a lista completa está em `../README.md`. Quem preferir editar à mão pode abrir o `.docx` direto no Word. Nesse caso, atualize o sumário e as listas pelo próprio Word.
