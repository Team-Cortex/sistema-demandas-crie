# Trabalho final de Engenharia de Software (BRAENSO)

Entrega e apresentação em **25/11/2026**. Projeto: Sistema de Demandas do CRIE, Equipe Cortex, ADS 2º semestre de 2026, IFSP Bragança Paulista.

| Arquivo | O que é |
| --- | --- |
| `Trabalho_Final_Volere_Equipe_Cortex.docx` | O modelo oficial da professora, preenchido (versão 0.9, 135 páginas). É este arquivo que a equipe edita. |
| `Trabalho_Final_Volere_Equipe_Cortex.pdf` | O mesmo documento em PDF, com o sumário atualizado. |
| `diagramas/` | Diagramas de contexto, casos de uso e navegação em SVG (fonte) e PNG (Anexo D do documento). |
| `telas/` | Capturas das telas do protótipo clicável, com dados fictícios, em tamanho original (Anexo B). |

Depois de editar o `.docx`: clique com o botão direito no sumário, escolha "Atualizar campo" e depois "Atualizar o índice inteiro". Em seguida, salve de novo como PDF.

---

## 1. O que a professora pede

Fonte: modelo oficial `Template_Trabalho_Final_Documentacao_Projeto_Volere.docx` (Moodle, seção "25-11 trabalho final e apresentação"), quadro "Critérios de avaliação".

| Parte | Peso | O que é observado |
| --- | --- | --- |
| I – Introdução e elicitação | 10% | Problema bem definido; processo justificado; técnicas de elicitação aplicadas com evidências |
| II – Volere 1 a 9 | 20% | Interessados, restrições, escopo, casos de uso e requisitos funcionais completos e verificáveis |
| II – Volere 10 a 17 | 15% | Requisitos não funcionais mensuráveis, com critério de ajuste |
| II – Volere 18 a 27 | 5% | Riscos, custos, migração e sala de espera registrados |
| III – Protótipos | 10% | Telas ligadas aos requisitos; guia de estilo; validação com usuários |
| IV – Priorização e rastreabilidade | 10% | MoSCoW justificado; matriz de rastreabilidade completa |
| V – V&V e testes | 10% | Casos de teste ligados aos requisitos e executados |
| VI – Gerenciamento e ferramentas | 10% | Backlog, sprints e uso efetivo do GitHub |
| VII – Qualidade | 5% | Características priorizadas e técnicas de QA aplicadas |
| VIII – Conclusão e apresentação | 5% | Reflexão crítica e contribuição de cada integrante |

Regras do modelo: item que não se aplica fica no documento com "Não se aplica a este projeto, porque [justificativa]"; identificadores iguais em todo o documento (RF-001, UC-001, CT-01...); diagramas como imagem com legenda; blocos "Conteúdo" removidos e sumário atualizado (lista VIII.6).

Critérios da apresentação: o Moodle não publicou critérios próprios para a apresentação final. A referência é a atividade "Apresentação do Projeto" (rótulo da Aula 3, 19/08): postura, organização, clareza na explicação, conteúdo e domínio do projeto e uso adequado dos recursos. O tempo não é critério, mas deve ser coerente com o conteúdo.

---

## 2. Situação item a item

Legenda: **Feito** = está no documento com evidência no repositório. **Pendente (equipe)** = depende de alguém da equipe ou do CRIE; o documento já marca o item como pendente, sem resultado inventado.

### Lista VIII.6 do modelo

| Item da lista | Situação | O que falta |
| --- | --- | --- |
| Capa, controle do documento e histórico de revisões | Pendente (equipe) | Prontuário de cada integrante na capa. Na entrega: versão 1.0 no histórico e "Final" no controle do documento |
| Processo de software escolhido e justificado | Feito | — |
| Elicitação documentada, com evidências nos anexos | Feito | As evidências estão nos anexos do relatório v3 (`docs/relatorios`) |
| Seções Volere 1 a 27 preenchidas ou "Não se aplica" | Feito | — |
| Diagramas de contexto, casos de uso e dados, com legenda | Feito | — |
| Todos os requisitos com critério de ajuste mensurável | Feito | Confirmar com a direção as metas numéricas propostas pela equipe (por exemplo, 6 de 8 participantes) |
| Cartão Volere para cada requisito Must | Feito | 49 cartões. As notas de satisfação e insatisfação são estimativas da equipe; confirmar com a direção |
| Protótipos inseridos, ligados aos requisitos e validados | Pendente (equipe) | Validação com usuários (III.6) |
| MoSCoW justificado e matriz de rastreabilidade completa | Feito | — |
| Casos de teste executados e com resultados | Feito em parte | Automatizados executados no CI. Faltam 13 casos manuais (ver abaixo) |
| Backlog, sprints e link do repositório | Feito | Anexar uma captura atual do quadro Trello |
| Características e técnicas de qualidade | Feito | — |
| Sumário atualizado e blocos "Conteúdo" removidos | Feito | Atualizar de novo depois de qualquer edição |

### Pendências da equipe, por item do modelo

| Item do modelo | Pendência | Sugestão de responsável |
| --- | --- | --- |
| Capa | Prontuários dos cinco integrantes | Cada integrante |
| I.4f | Conferir se a versão 4.0 do documento de requisitos (citada no relatório v3, não versionada) tem requisito que ficou de fora | Vinícius Marrocos |
| Volere 2e (D3) | Transcrever do Trello o texto das personas P2 e P3 para `docs/ihc/personas.md` e para a tabela 2e | Inácio Fontes |
| III.1 | Registrar o link do Figma | Inácio Fontes |
| III.6, V.3, CT-82, CT-84, CT-85, CT-102 | Aplicar os 8 testes de usabilidade (`docs/ihc/plano-de-testes.md`), preencher `docs/ihc/relatorio-de-usabilidade.md` e atualizar III.6 e V.4 com os números reais | Inácio Fontes, com a equipe |
| Atividade prática de V&V (2.2) | Validação cruzada: um integrante de outro grupo usa o fluxo de registro de demanda; anotar dois retornos reais | Equipe |
| V.3 | Apresentar o sistema à direção e verificar os critérios de aceitação 1 a 7 | Vinícius Marrocos |
| V.4 (CT-71, CT-78, CT-89, CT-90, CT-95, CT-98) | Imprimir relatório; revisar dados reais no material; medir tempo de resposta e 10 usuários; conferir planos da Vercel e do Neon; testar num computador do CRIE | Equipe |
| Volere 25a, RNF-009, RNF-010, RNF-026 (CT-80, CT-81, CT-96) | Orientação sobre a LGPD para a direção, procedimento de cópia de segurança e manual de uso | A definir |
| Volere 18 (Q-15, Q-16, Q-17) | Expiração por inatividade (PR de ajustes do front-end); autorização por escrito do logotipo; integrar o PR #19 e criar a conta da direção em produção | Gabriel Borba; direção; Miguel Vaz de Souza |
| VI.4 e Anexo C | Captura atual do quadro Trello | Vinícius Marrocos |
| VIII.3 e CT-94 | Cada integrante revisa a própria linha. Inácio Fontes não tem commits: o commit das personas P2 e P3 resolve isso | Cada integrante |
| VIII.6 | Marcar os itens concluídos depois das pendências acima | Vinícius Marrocos |

---

## 3. Roteiro curto da apresentação (cerca de 15 minutos)

Cada integrante fala da própria frente, como na divisão de papéis. Mostrar o documento e o sistema, não ler slide.

| Tempo | Quem | O que mostrar |
| --- | --- | --- |
| 2 min | Vinícius Marrocos | O CRIE, o problema (demandas em papel, esquecidas, histórico perdido) e o processo: Kanban em ciclos, specs antes do código. As três hipóteses erradas que a escuta corrigiu (I.4f) |
| 3 min | Vinícius Marrocos | Volere: interessados, restrições, um caso de uso (UC-005) e um cartão Volere com critério de ajuste. MoSCoW e a matriz de rastreabilidade (IV.4) |
| 2 min | Henry Claro | Modelo de dados (Figura 2) e as regras que o banco garante: histórico sem exclusão, estado fechado, auditoria só de inserção |
| 3 min | Inácio Fontes e Gabriel Borba | Mapa de navegação (Figura 4), guia de estilo (III.2) e demonstração: painel com vencidas, registrar demanda com confirmação, ficha do assistido. Dizer com clareza que os testes com usuários estão pendentes e qual é o plano |
| 3 min | Miguel Vaz de Souza | V&V: um caso de caixa preta e um de caixa branca ligados a requisitos, o CI do PR #19 (587 testes do servidor aprovados) e o registro de defeitos. GitHub: branches, PRs e padrão de commits |
| 2 min | Todos | Qualidade (segurança, usabilidade, confiabilidade), lições aprendidas e o que falta |

Para os critérios da professora:

- **Postura:** todos de pé e atentos enquanto o colega fala; quem não está falando cuida da navegação no computador.
- **Organização:** a ordem acima segue a ordem do documento (Partes I a VIII). Ensaiar a passagem de um para o outro.
- **Clareza:** frases curtas, termos do CRIE (demanda, assistido, encaminhamento). Mostrar o que é pendente como pendente.
- **Domínio do projeto:** cada um deve saber responder sobre a própria frente e explicar um requisito com o critério de ajuste e o teste que o verifica.
- **Recursos:** ter o PDF aberto nas páginas certas. Para a demonstração, usar o protótipo clicável (`docs/ihc/prototipo/index.html`), que funciona sem internet. O sistema publicado só deixa entrar depois que a conta da direção for criada (PR #19).
