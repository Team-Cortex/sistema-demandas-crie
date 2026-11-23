# Ferramentas do documento e dos slides de BD1

Scripts que geraram os resultados das consultas, o documento ABNT (`../Documento_BD1_Equipe_Cortex.pdf`) e os slides do seminário (`../Slides_Seminario_BD1_Equipe_Cortex.pdf`).

| Arquivo | O que faz |
|---|---|
| `rodar_consultas.py` | Roda os scripts SQL num MySQL 8 e salva os resultados em `resultados.json` |
| `conteudo.py`, `dicionario.tsv` | Textos do documento e dicionário de dados |
| `gerar_documento_abnt.py` | Monta o documento ABNT em HTML e imprime em PDF pelo Microsoft Edge (sumário com páginas, 2 passadas) |
| `gerar_documento.py` | Versão anterior do documento (sem ABNT), mantida para histórico |
| `gerar_slides.py` | Gera os slides do seminário em PDF |
| `logos/` | Logos do IFSP e do CRIE usados na capa |

## Como regenerar

Os scripts esperam a estrutura em que foram escritos: uma pasta raiz com `entrega/` (os quatro `.sql` e o PDF) e `apresentacao/`. Para regenerar a partir do repositório:

1. Crie `docs/modelagem/bd1/entrega/` e copie para ela os quatro scripts de `docs/modelagem/sql/`.
2. Em `docs/modelagem/bd1/ferramentas/`, rode:
   - `python gerar_documento_abnt.py` para o documento;
   - `python gerar_slides.py` para os slides.
3. Copie os PDFs gerados de volta para `docs/modelagem/bd1/`.

O caminho do Edge está em `gerar_documento_abnt.py` (constante `EDGE`).
