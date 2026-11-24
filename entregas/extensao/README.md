# Extensão como Metodologia de Ensino 2: ET5 (26/11/2026)

Entrega final de BRAEXT2 (Prof. Luiz Gustavo Diniz de Oliveira Véras). Esta pasta guarda o relatório de projeto v5, as figuras já incluídas nele e o lugar dos prints que a equipe ainda precisa capturar.

Fonte das exigências: **ESP** = "[BRAEXT2] Documento de Especificação de Projeto Integrado de Extensão 2026/2" (Moodle de Extensão 2, seção Geral).

## O que a ET5 pede

- **Entrega:** "Entrega e apresentação da versão final do sistema web com correções da EXPOEX, do board Kanban e do relatório de projeto" (ESP p. 6, §7). Vale 20% da média final (ESP p. 7, §8).
- **Critérios das entregas 3, 4 e 5** (ESP p. 7, §8):

  | Critério | Pontos | Texto do documento |
  | --- | --- | --- |
  | Qualidade e evolução de sistema | 5,5 | "Mede a evolução da implementação verificando códigos, design, modelagem do banco de dados e a funcionalidade da parte do sistema desenvolvida no ciclo." |
  | Evolução do Relatório | 3,0 | "A clareza, organização e completude das seções do documento de projeto apresentadas em cada ciclo." |
  | Atualização do Projeto | 1,5 | "Registro do progresso do desenvolvimento do sistema com a atualização do board Kanban." |

- **Board Kanban** (ESP p. 5, §6):
  - colunas "Backlog, A Fazer, Em Andamento, Em Revisão e Concluído";
  - cores por disciplina: BRAINHC azul, BRABCD1 laranja, BRAPROB roxo, BRADWFR verde, BRAENSO amarelo;
  - o professor de BRAEXT2 como membro do board;
  - "É obrigatório que o board seja atualizado antes de cada apresentação".
- **Relatório** (ESP p. 4 e 5, §5): ABNT, com Introdução; Relato de Contato com a Comunidade Externa; Desenvolvimento dividido em BRAENSO, BRAINHC, BRABCD1, BRAPROB e BRADWFR, "enriquecido com imagens e evidências visuais do processo de desenvolvimento, como screenshots, diagramas, e protótipos"; Resultados do Sistema Desenvolvido; Validação; Conclusão; Anexos; Apêndices.
- **Envio** (padrão das entregas anteriores, conforme `entregas/EXIGENCIAS_OFICIAIS.md` do PR #20): print do board, link do board, o relatório e o link do GitHub.

## Arquivos

| Arquivo | O que é |
| --- | --- |
| `Relatorio_de_Projeto_v5.docx` | Relatório v5, **arquivo para editar**. Mesma capa, estrutura e formatação do v3 (Arial 12, espaço 1,5, margens 3 e 2 cm, quadros com cabeçalho cinza). |
| `Relatorio_de_Projeto_v5.pdf` | PDF gerado do .docx pelo LibreOffice em 23/11/2026 (84 páginas). Refazer depois de preencher o .docx. |
| `figuras/` | As 13 figuras já incluídas: diagramas (arquitetura, classes, estados), DER do sistema e do recorte de BD1, telas do protótipo clicável e capturas públicas do GitHub. |
| `prints/` | Lugar dos prints que faltam (lista abaixo). Vazia por enquanto. |

No relatório, tudo que a equipe precisa completar está **realçado em amarelo** e entre colchetes: procure por `[a preencher`, `[a completar`, `[FIGURA` e `[confirmar`. Nenhum número, depoimento ou resultado foi inventado: o que não está no repositório ficou como lacuna.

## Checklist da ET5

### Sistema (5,5)
- [x] Sistema publicado em https://sistema-demandas-crie.vercel.app, com React e API Flask no mesmo endereço e banco no Neon. Conferido em 23/11/2026: a interface carrega, `/api/saude` responde `ok` e `/api/demandas` sem token responde 401.
- [x] Testes: 570 do back-end aprovados na `development` (execução local em 23/11) e 587 no GitHub Actions do PR #19; front-end com lint, build e 4 testes aprovados.
- [ ] Revisar e integrar os PRs #19 (CI e primeira direção), #20 (pasta de entregas) e #21 (ajustes finais do front e sessão por inatividade); levar a `development` para a `main`.
- [ ] **Criar a primeira conta da direção em produção** pelo fluxo do PR #19. Sem isso, ninguém entra no sistema publicado nem dá para tirar os prints.
- [ ] Confirmar que as três migrações (`b0f13416410c`, `3df29fd96f0b`, `3f00c11df825`) foram aplicadas no Neon. Sem `token_revogado`, as rotas com token respondem 500.
- [ ] Cadastrar pela tela Usuários as contas fictícias da demonstração (domínio `exemplo.test`) e registrar dados fictícios para os prints e para a apresentação.

### Board (1,5)
- [ ] Colunas Backlog, A Fazer, Em Andamento, Em Revisão e Concluído (no v3 eram Backlog, A Fazer, Fazendo, Esperando Teste, Testando e Concluído).
- [ ] Etiquetas com as cores por disciplina (no v3 as etiquetas eram por frente: Banco de Dados, UI/UX, Backend, Frontend e Comunidade Externa).
- [ ] Professor de BRAEXT2 como membro (o v3 registra que foi incluído; conferir).
- [ ] Mover os cartões dos ciclos 4 e 5 conforme o Quadro 18 do relatório e atualizar tudo antes da apresentação de 26/11.
- [ ] Capturar os prints 17, 18 e 19 e preencher o Quadro 17 (seção 4.3).

### Relatório (3,0)
- [x] Todas as seções do ESP §5, com o Desenvolvimento dividido nas cinco disciplinas.
- [x] Evolução desde o v3: PRs #5 a #21 (Quadro 3) e planejado no v3 × realizado (Quadro 18).
- [x] Discussão de qualidade de software (seção 3.1.6), pedida em BRAENSO e que faltava no v3.
- [x] Validação estruturada (método, participantes, tarefas, métricas, tabelas vazias com "Resultados a preencher após as sessões").
- [ ] Capturar os 22 prints da lista abaixo e trocar cada caixa cinza pela imagem.
- [ ] Preencher os itens da lista "O que a equipe precisa preencher".
- [ ] Fazer os 8 testes de usabilidade (`docs/ihc/plano-de-testes.md`; roteiro de bolso no PR #20) e preencher a seção 6.3.
- [ ] Registrar o feedback da EXPOEX (seções 2.7 e 4.6).
- [ ] Atualizar sumário e listas, tirar os realces amarelos, exportar o PDF e conferir página por página.

## Prints a capturar

Regras:
- **Só dados fictícios.** Contas `@exemplo.test`, nomes como "Bruna Fictícia" e "Assistido Fictício A". Nenhum dado de pessoa atendida, nenhum nome real, nenhum e-mail ou senha real. Há menores e dados de saúde no público do CRIE.
- Largura 1280 px no computador; 360 px nos de celular (DevTools do Edge ou do Chrome, "Alternar barra de ferramentas de dispositivo", largura 360).
- Salvar em `entregas/extensao/prints/` com o nome indicado. No .docx, apagar a caixa cinza da figura, inserir a imagem com 16 cm de largura (ou menos, se for alta) e completar a data na linha "Fonte".

| Figura | Arquivo | O que mostrar | Largura | Seção |
| --- | --- | --- | --- | --- |
| 1 | `prints/20-banner-expoex.png` | Arte final do banner da EXPOEX (foto só com integrantes que autorizarem) | ≥ 1280 px | 2.7 |
| 4 | `prints/22-personas.png` | As três personas (direção, assistente social, equipe pedagógica), do Trello ou do Figma, sem foto de pessoa real | ≥ 1280 px | 3.2.2 |
| 15 | `prints/01-entrar.png` | Tela Entrar, campos vazios | 1280 px | 3.5.6 |
| 16 | `prints/02-painel-direcao.png` | Painel logado como direção, aviso de prazo aberto, totais e as três colunas, com ao menos uma demanda vencida | 1280 px | 3.5.6 |
| 17 | `prints/03-painel-celular.png` | Painel com o menu recolhido e o botão Menu | 360 px | 3.5.6 |
| 18 | `prints/04-registrar-demanda-validacao.png` | Registrar demanda após enviar com campos obrigatórios vazios (mensagens junto aos campos) | 1280 px | 3.5.6 |
| 19 | `prints/05-confirmacao-demanda.png` | Diálogo de confirmação sobre o formulário preenchido | 1280 px | 3.5.6 |
| 20 | `prints/06-detalhe-demanda.png` | Detalhe com uma mudança de estado e uma anotação no histórico numerado | 1280 px | 3.5.6 |
| 21 | `prints/07-falha-conexao-rascunho.png` | Formulário preenchido após falha de envio com a rede desligada no DevTools, com a mensagem de que os dados continuam no formulário | 1280 px | 3.5.6 |
| 22 | `prints/17-kanban-vista-1.png` | Trello em 26/11: Backlog, A Fazer, Em Andamento, com as etiquetas coloridas | ≥ 1280 px | 4.1 |
| 23 | `prints/18-kanban-vista-2.png` | Trello em 26/11: Em Revisão e Concluído | ≥ 1280 px | 4.1 |
| 24 | `prints/19-kanban-etiquetas-membros.png` | Menu de etiquetas com as cinco cores e lista de membros com o professor | 1280 px | 4.1 |
| 25 | `prints/08-demandas-busca.png` | Demandas com "material adaptado" na busca e um filtro de estado aplicado | 1280 px | 5.2 |
| 26 | `prints/09-ficha-reuniao.png` | Ficha de uma reunião do setor de saúde com participantes e demandas | 1280 px | 5.2 |
| 27 | `prints/10-ficha-assistido.png` | Ficha do Assistido Fictício A com demandas, evoluções e encaminhamentos | 1280 px | 5.2 |
| 28 | `prints/11-versoes-evolucao.png` | Versões de uma evolução já retificada (vigente e anterior) | 1280 px | 5.2 |
| 29 | `prints/12-encaminhamentos-pendentes.png` | Encaminhamentos aberta nos pendentes, com ao menos dois itens | 1280 px | 5.2 |
| 30 | `prints/15-usuarios.png` | Usuários (direção) com as contas fictícias e uma desativada | 1280 px | 5.2 |
| 31 | `prints/13-relatorio-periodo.png` | Relatório de demandas de um período emitido, com totais e "Emitido por" | 1280 px | 5.2 |
| 32 | `prints/14-auditoria.png` | Auditoria (direção) com filtros e a primeira página | 1280 px | 5.2 |
| 33 | `prints/16-detalhe-celular.png` | Detalhe de uma demanda com as ações empilhadas | 360 px | 5.2 |
| 34 | `prints/21-graficos-usabilidade.png` | Gráficos da planilha dos testes: conclusão por tarefa e tempos com mediana e tempo-limite | 1280 px | 6.3.5 |

## O que a equipe precisa preencher

| Seção | Item |
| --- | --- |
| Resumo | Atualizar depois dos testes e do registro da EXPOEX |
| Quadro 1 | Conteúdo da versão 4 (ET4, 05/11); o arquivo não está em `docs/relatorios` |
| 2.7 | Se o bloco de perguntas foi enviado ao CRIE, quando, por qual canal e com quais respostas |
| 2.7 | Quem apresentou na EXPOEX, público e perguntas; **Feedback recebido na EXPOEX** |
| 2.7 e 6.4 | Se o sistema publicado foi mostrado à direção do CRIE e qual foi o retorno |
| 3.1.2 | Se a numeração do documento de requisitos v4.0 coincide com a de `docs/requisitos.md`; se a v4.0 foi atualizada |
| 3.1.4 | Como foi a revisão entre integrantes fora do GitHub (nenhum PR do período tem revisão registrada) e a contribuição de cada integrante (os 159 commits desde 22/10 saíram de uma única conta) |
| 3.2.2 | Texto das personas P2 e P3 (só a da direção está em `docs/ihc/personas.md`) |
| 3.2.6 | Situação final do protótipo no Figma e o link |
| 3.4.5 | Data em que a primeira direção foi criada em produção (sem e-mail nem senha) |
| 3.5.1 | Se o PR #21 for integrado: atualizar a seção e as linhas RF02 e RNF05 dos Quadros 21 e 22 |
| 3.5.6 | Se a revisão visual (PR #18) respondeu a alguma observação da EXPOEX |
| 4.1 | Colunas, etiquetas e membros do board em 26/11 |
| 4.2 | Participação de cada integrante nos ciclos 4 e 5 |
| 4.3 | Quadro 17 com as tarefas do board em 26/11 e o total de itens de verificação |
| 4.4 | Situação de três itens do Quadro 18 (bloco de perguntas, Figma, apoio à prototipação) |
| 4.5 | Confirmar as migrações no Neon (Quadro 20) |
| 4.6 | Feedback da EXPOEX e a relação entre cada observação e a alteração feita |
| 5.3 | Plano gratuito da Vercel e do Neon e transferência à instituição (RNF25) |
| 6.2 | Coluna "Resultado" do Quadro 24, depois das sessões |
| 6.3 | Ambiente, datas, versão testada, perfil dos participantes, Tabelas 3 e 4, gráficos, comentários e problemas (Quadro 29) |
| 7 | Parágrafo final com a síntese da validação |
| Anexos | Registro escrito do retorno da EXPOEX, se houver |

Termos de participação assinados têm nome real: ficam com a equipe, fora do repositório e fora do relatório.

## Como atualizar o PDF depois de editar

1. Editar `Relatorio_de_Projeto_v5.docx` no Word ou no LibreOffice.
2. Atualizar sumário e listas, que são campos de índice:
   - Word: `Ctrl+A`, depois `F9`, e escolher "Atualizar o índice inteiro";
   - LibreOffice: Ferramentas > Atualizar > Atualizar tudo.
3. Conferir que a numeração das páginas começa em 13 na Introdução (a capa não conta; a contagem começa na folha de rosto).
4. Exportar como PDF com o mesmo nome e conferir página por página: figuras, legendas, realces amarelos removidos.

## O que não foi verificado

- O quadro no Trello é privado: o estado do board em 23/11 não foi conferido.
- As telas internas do sistema publicado não foram abertas, porque não há usuário em produção; os prints do protótipo clicável (Figuras 5 a 9) mostram o protótipo, que ainda tem ícones e selos removidos do sistema pelo PR #18.
- A aplicação das migrações no Neon e o plano de cobrança da Vercel e do Neon.
- O conteúdo do documento de requisitos v4.0 (Apêndice A), que não está no repositório.
- O conteúdo do PR #21 não foi testado; o relatório descreve a `development` de 23/11 e cita o PR #21 como aberto.
