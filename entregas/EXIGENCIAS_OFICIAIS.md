# Exigências oficiais do projeto integrado, por disciplina

Levantamento dos documentos publicados no Moodle até 13/11/2026, com citação literal e fonte. Os professores podem ter publicado algo depois disso. **ESP** = "[BRAEXT2] Documento de Especificação de Projeto Integrado de Extensão 2026/2" (Moodle de Extensão 2, seção Geral).

## Extensão como Metodologia de Ensino 2
1. **ET5, 26/11, 20% da média:** "Entrega e apresentação da versão final do sistema web com correções da EXPOEX, do board Kanban e do relatório de projeto" (ESP p.6 §7).
2. **Critérios da ET5** (ESP p.7 §8; confirmados nas colunas "Entrega 5" da planilha de correções):

   | Critério | Peso | Texto do documento |
   |---|---|---|
   | Atualização do Projeto (board) | 1,5 | |
   | Qualidade e evolução de sistema | 5,5 | "verificando códigos, design, modelagem do banco de dados e a funcionalidade" |
   | Evolução do Relatório | 3,0 | "clareza, organização e completude das seções" |
3. **Board** (ESP p.5 §6):
   - cores: "BRAINHC (Azul), BRABCD1 (Laranja), BRAPROB (Roxo), BRADWFR (Verde) e BRAENSO (Amarelo)";
   - colunas: "Backlog, A Fazer, Em Andamento, Em Revisão e Concluído";
   - o professor deve ser membro do board;
   - "É obrigatório que o board seja atualizado antes de cada apresentação".
4. **Produto final** (ESP p.1 §2): relatório ABNT, evidências de método ágil e "Repositórios de código e demonstrações das funcionalidades".
5. **Relatório** (ESP p.4–5 §5): monografia ABNT, apresentada como "sugestão de estrutura". Seções:
   - Introdução;
   - Relato de Contato com a Comunidade Externa;
   - Desenvolvimento, que "Deverá ser subdividida" nas 5 disciplinas, com "imagens e evidências visuais… screenshots, diagramas, e protótipos";
   - Resultados do Sistema;
   - Validação;
   - Conclusão;
   - Anexos (documentos da comunidade) e Apêndices (código).

   O ESP pede confirmar com cada professor se o documento "será aceito como a entrega final" (p.5).
6. **Envio** (padrão das entregas anteriores): print do board; link do board; o relatório; link do GitHub do front e do back.

## Front End (Profa. Ana Paula Müller Giancoli)
Tarefa "Entrega PROJETO SEMESTRAL: Entrega em EQUIPES [04-12-2026]". Prazo 04/12, 23:59. Vale "10,0 - 100%".
1. **Parte I (8,0):**
   - aplicação "REACT JS sob o paradigma de Orientação a Objetos";
   - como a equipe também faz POO com a professora, vale "consumir a API da aplicação Python desenvolvida no componente curricular BRAPROB (Flask ou Fast API)".
2. README.md "com as instruções de instalação"; "Indicar as bibliotecas utilizadas"; "Publicar na plataforma Vercel.com".
3. **Parte II (2,0):** apresentação e GitHub (ver "Apresentações" abaixo).
4. **ESP §4.5:** interface "responsiva, acessível e interativa", "validações de formulário e requisições assíncronas", "componentes reutilizáveis".
5. **Entrega:**
   - .zip "sem a pasta no de_modules" (sic), enviado pelo Líder da Equipe;
   - "Verifique o link antes de entregar em outro navegador em que você não esteja logado."

## POO (Profa. Ana Paula Müller Giancoli)
Tarefa "Entrega PROJETO SEMESTRAL: Entrega em EQUIPES [01-12-2026]". Prazo 01/12, 23:59. Vale "9,0 - 90%".
1. **Parte I (7,5):**
   - "aplicação python sob o paradigma da orientação a objetos, integrado ao banco de dados SQLite3";
   - feita com "FLASK ou a FAST API";
   - "no mínimo 4 tabelas relacionais".
2. README.md "com as instruções de instalação e execução", "Indicar as bibliotecas", "Indicar as instruções de como utilizá-la"; "Publicar na plataforma Vercel.com"; "código zipado… da aplicação API".
3. **Parte II (1,5):** apresentação e GitHub.
4. **ESP §4.4:** "instância de objetos, métodos, encapsulamento, herança e polimorfismo"; API em Flask; integração com o banco.

## Banco de Dados 1 (Profª Letícia Souza Netto Brandi)
`2026s2Projeto_BD_interdisciplinar2.modulo.pdf`. Vale "Até 8 pontos"; a média final é (A1+A2+SQL+SIM+Proj)/2 (`Aula00 - Planejamento.pdf`, p.5).
1. **Regras (p.1 §3.1):** "no mínimo quatro e no máximo seis tabelas"; tipos "numérico, texto, data"; relacionamentos "1:1, 1:N e N:N".
2. **Critérios:**

   | Critério | Peso |
   |---|---|
   | Apresentação | 1,0 |
   | Universo de discurso, DER e notação textual | 1,0 |
   | Scripts "create table /database/drop/alter table" e carga "com diversidade de registros" | 1,0 |
   | "mínimo de 12 queries… diferentes nas suas formas e conteúdo… funções matemáticas e ou datas, ligação de tabelas/group by" | 5,0 |
3. **Apresentação (p.2):** "explicar o processamento das consultas", 20 minutos.
4. **Entrega:**
   - um arquivo compactado com um único PDF (capa com os nomes) mais os .sql separados, "nos comentários o propósito de cada query";
   - "Cada integrante do grupo deve fazer o upload usando seu login";
   - prazo 29/11 no PDF e na tarefa (o Planejamento diz 28/11).

## Engenharia de Software
`Template_Trabalho_Final_Documentacao_Projeto_Volere.docx` (seção "25-11 trabalho final e apresentação").
1. **O documento:** "modelo oficial do Trabalho Final… reunindo todas as entregas realizadas ao longo do semestre em uma única documentação formal".
2. **Pesos:**

   | Parte | Peso | Observação do template |
   |---|---|---|
   | I – Introdução e elicitação | 10% | |
   | II – Volere 1 a 9 | 20% | |
   | II – Volere 10 a 17 | 15% | "Requisitos não funcionais mensuráveis, com critério de ajuste" |
   | II – Volere 18 a 27 | 5% | |
   | III – Protótipos | 10% | "validação com usuários" |
   | IV – MoSCoW e rastreabilidade | 10% | |
   | V – V&V e testes | 10% | "Casos de teste ligados aos requisitos e executados" |
   | VI – Gerenciamento | 10% | "uso efetivo do GitHub" |
   | VII – Qualidade | 5% | |
   | VIII – Conclusão e apresentação | 5% | |
3. **Regras do template:**
   - item que não se aplica: "Não se aplica a este projeto, porque [justificativa]";
   - identificadores RF-001, UC-001, CT-01 iguais em todo o documento;
   - diagramas como imagem com legenda;
   - "Cartão Volere preenchido para cada requisito Must have";
   - "Sumário atualizado e blocos 'Conteúdo' removidos".
4. **Apresentação** (critérios do pitch de 19/08): "Postura… Organização… Clareza na explicação… Conteúdo e domínio do projeto… Utilização adequada dos recursos". "O tempo de apresentação não será um critério avaliativo".
5. **Atividade prática de V&V** (seção "Validação e Verificação"):
   - 3 casos de teste unitário, 1 teste de integração, um roteiro de aceitação e "dois feedbacks reais";
   - pesos 20/40/30/10%.

## IHC (Prof. André Gelschleiter)
1. **Peso:** "Projeto (PJ): 40%" (`IHC Aula 01_2026 b.pdf`, p.6). Enunciado do projeto final: não encontrado.
2. **Pista da tarefa da Aula 6:** "Esse protótipo/tema será utilizado até o final do curso para sua apresentação final", com protótipo "EM ALTA FIDELIDADE + a Arquitetura da Informação".
3. **ESP §4.2:**
   - protótipo de "média ou alta fidelidade funcional" com "fluxos e hotspots";
   - plano de testes com "tarefas baseadas nos cenários das personas";
   - medir "desempenho (tempo e passos), precisão (taxa de erros) e resposta emocional";
   - relatório com "perfil dos voluntários, tabelas e gráficos… lista detalhada dos problemas… sugestões de correção".

## Apresentações de POO e Front End (texto idêntico nos dois enunciados)
- "Duração máxima: 20 minutos".
- "Todos devem apresentar".
- "Exibir o Front-end, Back-end e os dados registrados no banco de dados".
- "Mostrar divisão de tarefas".
- "Apresentar trecho relevante do código".

## Ambiguidades e o que não foi encontrado
1. **Banco:** POO pede "SQLite3"; a produção usa PostgreSQL (Neon); as aulas de BD1 usam MySQL. Confirmar com a professora de POO.
2. **Front End:** "React sob o paradigma de Orientação a Objetos" não está detalhado. Confirmar com a professora.
3. **Eng. de Software:** tarefa de envio, formato (docx ou PDF) e peso na média não encontrados.
4. **IHC:** enunciado, data e formato do projeto final não encontrados.
5. **Extensão:**
   - enunciado da ET5 no Moodle não encontrado;
   - tempo de apresentação não encontrado;
   - feedback da EXPOEX não encontrado (o ESP diz que os requisitos "podem diferir", p.1).
6. **Board:** em 28/10 as colunas do Trello eram outras (Backlog / Fazendo / Esperando Teste / Testando / A Fazer / Concluído), e as cores por disciplina não foram conferidas.
