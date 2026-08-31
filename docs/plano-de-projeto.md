# Plano de Projeto — Sistema de Gestão de Demandas do CRIE

**Projeto de extensão:** Sistemas em Ação — Desenvolvimento de Soluções Digitais para Demandas Comunitárias
**Disciplina:** Extensão como Metodologia de Ensino 2 (BRAEXT2) — Prof. Luiz Gustavo Diniz de Oliveira Véras
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas — IFSP Câmpus Bragança Paulista
**Instituição parceira:** CRIE — Centro de Integração Especial / APAE de Extrema
**Versão:** 1.0 — agosto de 2026

---

## 1. Para que serve este documento

Reunir, num único lugar, tudo o que a equipe precisa saber para trabalhar de forma coordenada: o que vamos construir, por que, quem faz o quê, quando cada coisa precisa estar pronta e de que forma as frentes dependem umas das outras.

Não substitui o Documento de Requisitos, que detalha cada requisito individualmente. Este aqui é o mapa; o outro é a especificação.

---

## 2. O problema

O CRIE é uma organização sem fins lucrativos fundada em 1991 em Extrema (MG), filiada à Federação das APAEs, que atende pessoas com deficiência e suas famílias por meio de atendimento educacional especializado, saúde, assistência social e oficinas.

A equipe da instituição realiza reuniões semanais em que discute casos e levanta demandas: providências que precisam ser tomadas por um ou mais profissionais. Hoje essas demandas são anotadas em papel e em planilhas, sem controle centralizado de andamento.

A direção relatou duas consequências:

1. Perde-se tempo toda vez que é preciso retomar uma demanda antiga, porque não há histórico organizado;
2. Demandas são esquecidas e ficam sem conclusão, porque nada avisa que estão paradas.

Nas palavras da própria direção, o sucesso do sistema será medido por "agilidade e organização das demandas".

---

## 3. O que vamos construir

Um sistema web para registrar, acompanhar e consultar as demandas levantadas nas reuniões de equipe do CRIE, do registro inicial até a conclusão, incluindo o registro de evoluções e encaminhamentos vinculados aos assistidos.

### 3.1 Funcionalidades centrais

- Registro de reuniões de equipe e das demandas nelas levantadas
- Acompanhamento do estado de cada demanda: aberta, em andamento, aguardando terceiros, concluída, cancelada
- Histórico completo e imutável de tudo o que aconteceu com cada demanda
- Cadastro de assistidos e vinculação de demandas, evoluções e encaminhamentos
- Painel com demandas em aberto e destaque para prazos vencidos
- Relatórios por período e relatório de acompanhamento por assistido
- Controle de acesso por perfil de usuário

### 3.2 O que ficou fora, e por quê

| Item | Motivo |
| --- | --- |
| Controle de estoque de alimentos e materiais | A direção também levantou essa necessidade, mas indicou a gestão de demandas como prioridade. São dois domínios distintos; construir os dois em 12 semanas significaria entregar dois sistemas incompletos. Registrado como trabalho futuro no relatório. |
| Anexo de laudos e documentos digitalizados | Guardar arquivos com dados de saúde exigiria controles que não cabem no prazo. |
| Integração com o aplicativo de cadastro já usado pelo CRIE | Depende de informação técnica que ainda não temos. |
| Funcionamento sem internet, com sincronização | Complexidade incompatível com o prazo e com o nível técnico da equipe. |
| Envio automático por WhatsApp | A API oficial é paga e exige aprovação. Faremos notificação dentro do sistema e por e-mail. |

### 3.3 Uma regra que vale para todos

O sistema tratará dados de pessoas com deficiência, boa parte menores de idade. Isso impõe três regras que ninguém do grupo pode flexibilizar:

1. **Nenhum dado real** em repositório de código, protótipo, planilha, apresentação ou ambiente de testes. Sempre dados fictícios.
2. **Nada de dado real na EXPOEX.** A mostra é pública e o banner fica exposto.
3. **Nenhum print de tela com dado real** em relatório, slide ou grupo de conversa da equipe.

Isso não é excesso de zelo: é requisito não funcional formal do projeto (RNF06 e RNF07) e será cobrado na avaliação de qualidade de software.

---

## 4. Tecnologias

| Camada | Tecnologia | Disciplina |
| --- | --- | --- |
| Front-end | React | BRADWFR |
| Back-end | Python com Flask, orientado a objetos | BRAPROB |
| Banco de dados | Relacional | BRABCD1 |
| Comunicação | API web com contrato documentado | BRAPROB + BRADWFR |
| Versionamento | Git | BRAENSO |
| Gestão | Kanban no Trello | BRAEXT2 |
| Prototipação | Figma | BRAINHC |

---

## 5. Quem faz o quê

| Integrante | Cargo | Disciplina |
| --- | --- | --- |
| Vinícius Marrocos | Gerente de Projeto e Analista de Requisitos | Engenharia de Software (BRAENSO) |
| Henry Claro | Analista de Banco de Dados | Banco de Dados 1 (BRABCD1) |
| Inácio Fontes | Analista de Interface e Experiência do Usuário | Interface Humano-Computador (BRAINHC) |
| Miguel Vaz de Souza | Desenvolvedor Back-end | Programação Orientada a Objetos (BRAPROB) |
| Gabriel Borba | Desenvolvedor Front-end | Desenvolvimento Web Front End (BRADWFR) |

Cada um é **dono** da sua frente: responde pela entrega, cobra quem precisa contribuir e apresenta o resultado. Não significa trabalhar sozinho — a partir de outubro, quem estiver com carga menor migra para o desenvolvimento.

### 5.1 Responsabilidades compartilhadas

| Responsabilidade | Descrição | Responsável |
| --- | --- | --- |
| Compilação do relatório | Consolidar as seções escritas por cada frente em documento único, padronizado em ABNT, antes de cada entrega. Não escreve tudo: padroniza. | Inácio Fontes |
| Contato com o CRIE | Manter a comunicação com a direção. Exige disponibilidade em horário comercial, já que a instituição responde durante o dia. | *A definir* |
| Registro de evidências | Arquivar prints de conversas, fotos, formulários assinados e documentos. Vão para os anexos do relatório. | *A definir* |

---

## 6. Como cada frente se desenvolve ao longo do semestre

### 6.1 Vinícius Marrocos — Gerente de Projeto e Analista de Requisitos

**Agosto e início de setembro**
Criar o board no Trello, com as colunas Backlog / A Fazer / Em Andamento / Em Revisão / Concluído e as cores por disciplina definidas pelo professor. Adicionar o professor como membro. Criar o repositório Git e definir padrão de commits e branches. Montar a versão 1 do relatório.

**Setembro**
Consolidar o documento de requisitos com base nas respostas do CRIE. Separar requisitos funcionais de não funcionais. Manter o board atualizado a cada ciclo.

**Outubro**
Planejar verificação, validação e testes de software. Escrever a discussão sobre qualidade de software. Acompanhar o desenvolvimento e sinalizar atrasos.

**Novembro**
Consolidar o relatório final. Garantir que o board reflita o estado real do projeto antes da última apresentação.

**Cuidado principal:** o board desatualizado é perda de nota direta e recorrente, em todas as cinco entregas.

---

### 6.2 Henry Claro — Analista de Banco de Dados

**Setembro**
Escrever a especificação do minimundo a partir do que for levantado com o CRIE. Produzir o Diagrama Entidade-Relacionamento com as entidades: usuário, assistido, reunião, demanda, evolução, encaminhamento e histórico de alterações.

**Até 01/10 — prazo crítico**
Fechar o modelo relacional com tabelas, atributos e restrições. Escrever os scripts de criação e de carga inicial com dados fictícios.

**Outubro**
Escrever as consultas de demonstração exigidas pela disciplina. Apoiar o back-end na integração. A partir daqui, migrar para o desenvolvimento junto ao Miguel.

**Novembro**
Escrever a seção de banco de dados do relatório e apoiar o desenvolvimento.

**Cuidado principal:** o modelo relacional é o gargalo do projeto inteiro. Se escorregar para o fim de outubro, back-end e front-end ficam espremidos em três semanas.

---

### 6.3 Inácio Fontes — Analista de Interface e Experiência do Usuário

**Setembro**
Construir personas e cenários a partir do contato com o CRIE. Levantar com a instituição a terminologia usada internamente, quantos computadores existem e onde ficam.

**Setembro e outubro**
Prototipar no Figma, em média ou alta fidelidade, com navegação entre telas. Validar o protótipo com a equipe do CRIE antes de o front-end começar a codificar.

**Outubro**
Planejar os testes de usabilidade: metodologia, perfil dos participantes, tarefas baseadas nos cenários. Executar os testes medindo tempo, número de passos, taxa de erro e satisfação. Produzir o relatório de usabilidade com tabelas e gráficos.

**Novembro**
Produzir o banner e conduzir a apresentação na EXPOEX.

**Cuidado principal:** esta frente carrega o maior peso na nota. A EXPOEX vale 35% da média final, mais que a entrega final do sistema. O protótipo também precisa estar pronto cedo, porque o front-end depende dele.

---

### 6.4 Miguel Vaz de Souza — Desenvolvedor Back-end

**Setembro**
Participar da modelagem junto ao Henry. Definir com o Vinícius o contrato da API: quais endpoints existirão, o que cada um recebe e devolve. Isso é feito no papel, antes de existir código.

**Outubro**
Modelar as classes aplicando encapsulamento, herança e polimorfismo — a disciplina cobra esses conceitos explicitamente, não basta o código funcionar. A hierarquia de perfis de usuário, com permissões resolvidas por polimorfismo, é o caminho natural. Implementar a API em Flask e integrar ao banco.

**Novembro**
Concluir as funcionalidades, apoiar a integração com o front-end e escrever a seção de POO do relatório.

**Cuidado principal:** o back-end não começa antes de o modelo relacional estar fechado. Cobrar o prazo de 01/10 é responsabilidade compartilhada com o Henry.

---

### 6.5 Gabriel Borba — Desenvolvedor Front-end

**Setembro**
Apoiar o Gabriel na prototipação, já pensando em como as telas viram componentes. Definir com o Miguel o contrato da API.

**Outubro**
Montar a estrutura do projeto React e os componentes reutilizáveis. Implementar as telas com dados simulados enquanto a API não estiver pronta — isso evita ficar bloqueado esperando o back-end.

**Novembro**
Integrar com a API real. Implementar validações de formulário e requisições assíncronas. Garantir responsividade e acessibilidade. Escrever a seção de front-end do relatório.

**Cuidado principal:** não esperar a API ficar pronta para começar. Com o contrato definido em setembro, dá para desenvolver as telas em paralelo.

---

## 7. Ordem de dependência

Quem atrasa, trava o próximo:

1. Contato com o CRIE → define o problema
2. Requisitos (Vinícius) → transformam o problema em especificação
3. Minimundo e DER (Henry) → estruturam os dados
4. Personas e protótipo (Inácio) → definem as telas
5. **Modelo relacional fechado (Henry)** → libera o back-end
6. API (Miguel) → libera a integração do front-end
7. Testes de usabilidade (Inácio) → validam com o público-alvo

O passo 5 é o gargalo mais provável do semestre.

---

## 8. Calendário

| Entrega | Data | Peso | O que precisa estar pronto | Quem lidera |
| --- | --- | --- | --- | --- |
| ET1 | 03/09 | 5% | Desafio apresentado, board Kanban montado, versão 1 do relatório | Inácio |
| ET2 | 01/10 | 10% | Requisitos consolidados, DER e modelo relacional, personas e início do protótipo, versão 2 do relatório | Inácio, Henry, Gabriel |
| ET3 | 22/10 | 10% | Banco implementado, início do back-end, protótipo validado, versão 3 do relatório | Henry, Miguel |
| ET4 | 05/11 | 15% | API funcionando, telas integradas, testes de usabilidade em execução, versão 4 do relatório | Miguel, Vinícius |
| EXPOEX | 18/11 | 35% | Banner, sistema demonstrável com dados fictícios | Gabriel — mas todos apresentam |
| ET5 | 26/11 | 20% | Sistema final com correções da EXPOEX, relatório final | Todos |
| Simulado ENADE | — | 5% | — | Individual |

**Média final:** `MF = ET1×0,05 + ET2×0,10 + ET3×0,10 + ET4×0,15 + ME×0,35 + ET5×0,20 + EN×0,05`

Vale notar: a Mostra de Extensão pesa mais que a entrega final do sistema. Saber apresentar vale mais que a última linha de código.

---

## 9. Pendências imediatas

| Pendência | Prazo | Responsável |
| --- | --- | --- |
| Criar board no Trello e adicionar o professor | Antes de 03/09 | Inácio |
| Criar repositório Git e adicionar todos | Antes de 03/09 | Inácio |
| Enviar Formulário de Manifestação de Interesse ao CRIE para assinatura | Imediato | Contato com o CRIE |
| Obter autorização para citar o nome do CRIE no relatório e no banner | Antes de 03/09 | Contato com o CRIE |
| Obter respostas do bloco 1 de perguntas (escopo de "evolução", permissões, fluxo da reunião) | Antes de 03/09 | Contato com o CRIE |
| Definir responsáveis pelo contato com o CRIE e pelo registro de evidências | Imediato | Equipe |
| Confirmar com cada professor se este projeto atende à avaliação da respectiva disciplina | Setembro | Cada frente com seu professor |

---

## 10. Questões ainda em aberto com o CRIE

| Questão | Impacto |
| --- | --- |
| O que a direção chama de "evolução": acompanhamento do assistido, andamento da demanda, ou ambos | Alto — define metade do escopo |
| Quem enxerga o quê dentro do sistema | Alto — define o controle de acesso |
| Como funciona uma reunião de equipe hoje | Alto — define a modelagem |
| Formato do relatório enviado à Prefeitura | Alto — define os relatórios |
| Categorias de demanda e áreas de atuação usadas pela instituição | Médio |
| Campos de identificação do assistido considerados necessários | Médio |
| Qual aplicativo de cadastro já está em uso | Médio |
| Prazo de guarda dos registros | Médio |

Enquanto as quatro primeiras não forem respondidas, o que está no Documento de Requisitos é hipótese fundamentada, não especificação fechada.

---

## 11. Combinados da equipe

- Ciclos de duas semanas, com o board atualizado antes de cada apresentação
- Contrato da API definido no papel em setembro, antes de existir código
- Toda decisão tomada com o CRIE registrada por escrito e compartilhada com o grupo
- Cada frente escreve sua seção do relatório ao longo do ciclo, não na véspera
- Nenhum dado real do CRIE em qualquer artefato do projeto
- Todos participam da apresentação na EXPOEX
