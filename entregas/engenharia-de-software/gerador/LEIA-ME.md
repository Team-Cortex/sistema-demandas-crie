# Gerador do trabalho final Volere

Scripts que preencheram o **modelo oficial** de Engenharia de Software (`Template_Trabalho_Final_Documentacao_Projeto_Volere.docx`, Moodle, seção "25-11 trabalho final e apresentação") e geraram `../Trabalho_Final_Volere_Equipe_Cortex.docx`.

| Arquivo | Conteúdo |
|---|---|
| `monta.py` | Ponto de entrada: abre o modelo, preenche cada parte e salva o .docx |
| `fill_lib.py` | Funções para achar títulos e tabelas do modelo e escrever nelas |
| `c1_inicio.py` | Capa, histórico e Parte I (introdução e elicitação) |
| `c2_volere_1_9.py` | Volere 1 a 9 |
| `c3_requisitos.py` | Volere 10 a 27, com os requisitos e os cartões dos requisitos Must |
| `c4_vv.py` | Parte V (V&V): casos de teste CT e CB ligados aos testes automatizados |
| `c5_resto.py` | Partes III, IV, VI, VII e VIII |
| `diag_contexto.py`, `diag_uc.py`, `diag_nav2.py` | Desenham os diagramas de `../diagramas/` |

## Como gerar de novo
1. Copie o modelo oficial para esta pasta com o nome `template.docx`.
2. Nesta pasta, rode `python monta.py ../Trabalho_Final_Volere_Equipe_Cortex.docx` (requer `python-docx` e `Pillow`).
3. Abra o .docx no Word, atualize o sumário (F9) e exporte o PDF.

O texto final passou por revisões feitas direto nos arquivos `c*.py`. Para pequenas correções, editar o .docx no Word é mais simples.
