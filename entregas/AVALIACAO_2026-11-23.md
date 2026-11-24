# Avaliação do projeto CRIE contra todas as exigências (23/11/2026, gerada por IA, conferir)

## Base da avaliação
- **Enunciados oficiais** de Extensão 2, Front End, POO, BD1, Eng. de Software e IHC, baixados do Moodle até 13/11. Detalhes e citações no levantamento.
- **Auditoria da `upstream/main` (764e548)**:
  - lint, build e testes do front: ok;
  - testes do back-end não rodaram aqui, porque uma política do Windows bloqueou a DLL.
- **Teste do site no ar:** tela de entrar, API e banco ok.

## Situação geral
- **O sistema está muito bom tecnicamente:**
  - as 14 telas foram feitas e estão ligadas à API;
  - os requisitos de acessibilidade, erro e rascunho estão no código;
  - não há sobras de código;
  - as dependências estão documentadas;
  - só há dados fictícios.
- **O que ameaça a nota máxima não é o código, e sim:**
  - entregas que ainda não existem: Volere final, relatório v5, testes de usabilidade;
  - a produção sem nenhum usuário;
  - três exigências literais dos enunciados: SQLite3 em POO, "React sob o paradigma de OO" em Front End, colunas e cores do board.

## Por entrega: o que vale e o que está em risco

| Data | Entrega | Critérios (peso) | Situação | Em risco |
|---|---|---|---|---|
| **25/11** | Eng. Software: trabalho final Volere + apresentação | I 10%, II 40% (1–9: 20, 10–17: 15, 18–27: 5), III protótipos com validação 10%, IV MoSCoW e rastreabilidade 10%, V casos de teste ligados a requisitos e executados 10%, VI GitHub 10%, VII 5%, VIII 5% | Material quase todo existe (requisitos, specs, protótipo, ~570 testes, GitHub), mas **o documento no template oficial não foi encontrado** | Quase tudo, se não for montado até 25/11 |
| **26/11** | Extensão: ET5 (20%) | Sistema 5,5 · relatório v5 3,0 · board 1,5 | Sistema completo, **mas ninguém consegue entrar em produção**. **v5 não está no repositório.** Board de 28/10 fora do padrão (colunas Backlog / A Fazer / Em Andamento / Em Revisão / Concluído; cores por disciplina; professor como membro) | 3,0 (v5) + 1,5 (board) + parte dos 5,5 |
| 29/11 | BD1: projeto (8 de 10, 4 da final) | Apresentação 1,0 · minimundo, DER e notação 1,0 · scripts e carga 1,0 · 12+ consultas 5,0 | **Pronto:** documento ABNT de 46 págs. e 17 consultas | Pouco: falta o .zip (PDF + .sql comentados), o upload de **cada integrante** e o sobrenome da professora |
| 01/12 | POO: projeto (9 de 10) | API Flask OO + **SQLite3** + 4 tabelas (7,5) · apresentação e GitHub (1,5) | API completa, mas **em PostgreSQL**. O back-end já roda em SQLite (testes de migração) | Exigência literal de "SQLite3"; falta mostrar onde estão encapsulamento, herança e polimorfismo; README "como usar"; link da API |
| 04/12 | Front End: projeto (10) | React consumindo a API + README + bibliotecas + Vercel (8,0) · apresentação (2,0) | Atende quase tudo. **Faltam:** login funcionando em produção; o "paradigma de OO" (não há nenhuma classe); link e prints no README | "Exibir os dados registrados no banco" depende do login em produção |
| ? | IHC: projeto (40%) | Protótipo de alta fidelidade + AI + testes de usabilidade com tabelas, gráficos e problemas | Cenários, AI, fluxos, telas, plano de testes e protótipo HTML: ok. **Testes não feitos** (relatório só com o modelo). Personas P2 e P3 incompletas. Enunciado e data não encontrados | Toda a parte de validação |

## Riscos que valem para todas as matérias
1. **Autoria concentrada.** Todo o front e o IHC estão em commits do Miguel. Os professores de Front End e POO cobram "mostrar divisão de tarefas" e que **todos** apresentem e expliquem o código. O `divisao-de-papeis.md` ainda tem letras no lugar de nomes.
2. **Sinais de IA no histórico:**
   - 12 commits de 16/10 com `Co-authored-by: Cursor`;
   - merges feitos pelo bot;
   - a frase "elaborado com apoio de IA" em `bd1/README.md`.

   Reescrever o histórico da `main` é arriscado. Recomendação: não reescrever e tirar só a frase do README.
3. **Documentação desatualizada:**
   - `estado-do-projeto.md` ainda diz que o front tem só o esqueleto;
   - o contrato diz que o cliente "ainda não existe";
   - o README não tem o link de produção.

## Plano de ação para a nota máxima

### O tutor pode fazer (alterações no repositório e na produção só com aprovação do Miguel)
1. **Produção com acesso:**
   - abrir o PR da branch `miguel/primeira-direcao`, que já tem o comando e os testes;
   - criar o 1º usuário da direção. O Miguel digita a senha no terminal; ninguém mais a vê.
2. **Volere final (25/11):** preencher o template oficial com o que já existe:
   - RF/RNF com critério de ajuste;
   - MoSCoW;
   - rastreabilidade RF → tela → rota → teste;
   - casos de teste CT-xx ligados aos testes automatizados;
   - gerenciamento no GitHub (PRs, branches).
3. **Relatório v5 ABNT (26/11):**
   - todas as seções do §5;
   - prints reais com dados fictícios;
   - Validação com a estrutura pronta para os resultados reais dos testes.
4. **Ajustes no código (PRs pequenos):**
   - fazer o merge do PR #18;
   - remover a rota `/api/teste`;
   - deixar o aviso de prazo (RF40) visível;
   - colocar a mensagem de vazio no painel;
   - padronizar o "carregando";
   - encerrar a sessão por inatividade (RF02/RNF05);
   - **cliente da API como classe** (`ClienteApi`), que responde ao "paradigma de OO" do Front;
   - remover o React Compiler e o `@types`;
   - deixar a fonte local.
5. **Documentação:**
   - README com link, prints e uma seção "Rodar com SQLite3" (POO);
   - `docs/poo-no-backend.md` (onde estão encapsulamento, herança e polimorfismo);
   - atualizar o estado do projeto e o contrato.
6. **BD1:** montar o .zip (PDF + .sql com o propósito de cada consulta nos comentários) e corrigir o nome da professora.
7. **Testes de usabilidade:** fazer um roteiro de 15 min por voluntário, com uma planilha. Depois o tutor consolida tabelas, gráficos e a lista de problemas, sem inventar nada.

### Só a equipe pode fazer
1. **Aplicar os 8 testes de usabilidade até 25/11 à noite**, com voluntários reais (no CRIE, com colegas ou com a família).
2. **Trello:**
   - colunas: Backlog, A Fazer, Em Andamento, Em Revisão, Concluído;
   - cores: IHC azul, BD1 laranja, POO roxo, Front verde, ENSO amarelo;
   - professor como membro;
   - atualizar antes de 26/11.
3. **Personas P2 e P3** completas (Inácio).
4. **Perguntar às professoras:** POO aceita PostgreSQL, com SQLite3 mostrado localmente? O que Front End quer dizer com "React sob OO"?
5. **IHC:** enunciado e data da apresentação final; Figma em alta fidelidade (Inácio).
6. **Cada integrante estuda a parte que vai apresentar.** Os parágrafos "Como explicar" dos PRs servem de roteiro.
7. **BD1:** cada integrante faz o próprio upload até 29/11.

## O que não foi verificado
- Execução dos testes do back-end (bloqueio do Windows).
- Telas internas em produção, porque não há usuário.
- Estado atual do Trello e do Figma.
- Feedback da EXPOEX.
- Se o v4 foi entregue no Moodle.
- Conteúdo dos relatórios v1 a v3.
