# Documento de Requisitos de Software

**Projeto:** Sistema de Gestão de Demandas de Reuniões de Equipe
**Instituição parceira:** CRIE — Centro de Integração Especial / APAE de Extrema
**Disciplina:** Extensão como Metodologia de Ensino 2 (BRAEXT2) — Tecnologia em Análise e Desenvolvimento de Sistemas
**Instituição:** Instituto Federal de São Paulo — Câmpus Bragança Paulista
**Equipe:** Gabriel Borba, Henry Claro, Inácio Fontes, Miguel Vaz de Souza, Vinicius Marrocos
**Versão:** 2.0 — agosto de 2026

---

## 1. Introdução

### 1.1 Objetivo do documento

Este documento especifica os requisitos funcionais e não funcionais do sistema a ser desenvolvido para o CRIE — Centro de Integração Especial de Extrema, no âmbito do projeto de extensão "Sistemas em Ação: Desenvolvimento de Soluções Digitais para Demandas Comunitárias". Destina-se à equipe de desenvolvimento, aos docentes responsáveis pelas disciplinas do 2º módulo e à instituição parceira, servindo como referência para o desenvolvimento e para a validação da solução entregue.

### 1.2 Escopo do produto

O sistema tem por finalidade registrar, acompanhar e consultar as demandas levantadas nas reuniões semanais de equipe do CRIE, desde o registro inicial até a conclusão, mantendo histórico consultável. Compreende ainda o registro das evoluções e dos encaminhamentos vinculados aos assistidos, conforme solicitado pela direção da instituição durante o levantamento de requisitos.

Não fazem parte do escopo desta versão: controle de estoque de materiais de consumo e substituição do aplicativo de cadastro de usuários já utilizado pela instituição.

### 1.3 Definições

| Termo | Definição |
| --- | --- |
| **Assistido** | Pessoa atendida pelo CRIE. |
| **Demanda** | Necessidade ou pendência identificada em reunião de equipe, que exige providência de um ou mais profissionais. |
| **Evolução** | Registro do acompanhamento de um assistido, elaborado por profissional da instituição. |
| **Encaminhamento** | Direcionamento de um assistido ou de uma demanda a um serviço, órgão ou setor externo ou interno. |
| **Reunião de equipe** | Encontro semanal em que a equipe discute casos e levanta demandas. |
| **Profissional** | Membro da equipe do CRIE que utiliza o sistema. |
| **Dado pessoal sensível** | Conforme a Lei nº 13.709/2018, dado sobre saúde, entre outras categorias, exigindo tratamento com salvaguardas específicas. |

### 1.4 Referências

- Documento de Especificação de Projeto Integrado de Extensão — BRAEXT2, IFSP Câmpus Bragança Paulista, 2026.
- Formulário de Levantamento de Requisitos respondido pela direção do CRIE, agosto de 2026.
- BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais.

---

## 2. Descrição geral

### 2.1 Contexto e justificativa

O CRIE é uma organização da sociedade civil sem fins lucrativos, fundada em 1991 no município de Extrema (MG) e filiada à Federação das APAEs, que oferece atendimento educacional especializado, atendimentos de saúde, assistência social e oficinas a pessoas com deficiência e suas famílias.

Em levantamento realizado junto à direção da instituição, identificou-se que as demandas levantadas nas reuniões semanais de equipe são registradas atualmente em papel e em planilhas, sem controle centralizado de andamento. A direção relatou duas consequências desse processo: o tempo despendido para retomar demandas anteriores e a ocorrência de demandas esquecidas, que permanecem sem conclusão.

O sistema proposto responde a essa necessidade ao centralizar o registro das demandas, tornar seu andamento visível e preservar o histórico de forma consultável, incluindo as evoluções e os encaminhamentos vinculados aos assistidos.

### 2.2 Perfis de usuário

| Perfil | Descrição | Atribuições previstas |
| --- | --- | --- |
| **Direção** | Direção da instituição. | Acesso integral ao sistema, cadastro de usuários e profissionais, emissão de relatórios, definição de permissões. |
| **Assistente social** | Profissional do serviço social. | Registro e atualização de demandas, registro de evoluções e encaminhamentos, consulta ao histórico dos assistidos que acompanha. |
| **Equipe pedagógica** | Profissionais da área pedagógica. | Registro e atualização de demandas, registro de evoluções, consulta ao histórico dos assistidos que acompanha. |

Estima-se, conforme informado pela instituição, cerca de seis usuários simultâneos.

### 2.3 Ambiente de operação

O sistema será acessado exclusivamente nas dependências do CRIE, por meio de navegador web em computadores da instituição. A conexão de internet local foi descrita como de estabilidade intermitente, o que impõe requisitos específicos de tolerância a falhas de comunicação, tratados na seção 4.

### 2.4 Restrições de projeto

- Prazo de desenvolvimento limitado ao calendário letivo, com entrega final em 26 de novembro de 2026.
- Stack tecnológica definida pelas disciplinas do módulo: back-end em Python com framework Flask, banco de dados relacional, front-end em React.
- Ausência de previsão orçamentária, tanto por parte da instituição parceira quanto da equipe, o que restringe a solução a serviços de hospedagem e ferramentas gratuitos.
- Equipe composta por cinco estudantes, com dedicação parcial.

### 2.5 Premissas e dependências

- A instituição disponibilizará profissionais para validação do protótipo e participação nos testes de usabilidade.
- Os dados utilizados durante o desenvolvimento, os testes e as demonstrações públicas serão exclusivamente fictícios.
- O aplicativo de cadastro de usuários já utilizado pela instituição permanecerá em operação, sem integração automática com o sistema nesta versão.
- A instituição, na condição de controladora dos dados pessoais tratados, definirá as regras de acesso e a política de retenção aplicáveis.

---

## 3. Requisitos funcionais

Os requisitos estão classificados por prioridade segundo a escala: **Essencial** (indispensável à entrega), **Importante** (agrega valor significativo, previsto para desenvolvimento após os essenciais) e **Desejável** (implementado se houver disponibilidade de tempo).

### 3.1 Autenticação e controle de acesso

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF01 | O sistema deve permitir que o usuário se autentique por meio de identificador e senha. | Essencial |
| RF02 | O sistema deve encerrar a sessão do usuário mediante solicitação e após período de inatividade. | Essencial |
| RF03 | O sistema deve restringir as funcionalidades e os registros disponíveis conforme o perfil do usuário autenticado. | Essencial |
| RF04 | O sistema deve permitir que o perfil Direção cadastre, edite e desative usuários. | Essencial |
| RF05 | O sistema deve restringir o acesso às evoluções de um assistido aos profissionais autorizados e ao perfil Direção. | Essencial |

### 3.2 Gestão de reuniões

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF06 | O sistema deve permitir o registro de uma reunião de equipe, contendo data e profissionais participantes. | Essencial |
| RF07 | O sistema deve permitir a consulta às reuniões registradas, ordenadas por data. | Essencial |
| RF08 | O sistema deve exibir, ao consultar uma reunião, a relação das demandas nela levantadas e seus respectivos estados. | Essencial |
| RF09 | O sistema deve permitir a edição dos dados de uma reunião registrada. | Importante |

### 3.3 Gestão de demandas

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF10 | O sistema deve permitir o registro de uma demanda, contendo descrição, categoria, prioridade, profissional responsável, prazo previsto e reunião de origem. | Essencial |
| RF11 | O sistema deve permitir a associação opcional de uma demanda a um assistido. | Essencial |
| RF12 | O sistema deve controlar o estado de cada demanda entre os valores: aberta, em andamento, aguardando terceiros, concluída e cancelada. | Essencial |
| RF13 | O sistema deve permitir a alteração do estado de uma demanda por usuário autenticado. | Essencial |
| RF14 | O sistema deve registrar automaticamente, a cada alteração de estado, o autor, a data e a hora da alteração. | Essencial |
| RF15 | O sistema deve permitir o registro de anotações de acompanhamento vinculadas a uma demanda. | Essencial |
| RF16 | O sistema deve permitir a reatribuição de uma demanda a outro profissional responsável. | Importante |
| RF17 | O sistema deve exibir o histórico completo de alterações e anotações de uma demanda. | Essencial |

### 3.4 Cadastro de assistidos

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF18 | O sistema deve permitir o cadastro de assistidos, contendo os dados de identificação definidos pela instituição. | Essencial |
| RF19 | O sistema deve permitir a consulta e a edição dos assistidos cadastrados. | Essencial |
| RF20 | O sistema deve exibir, na ficha do assistido, o histórico de demandas, evoluções e encaminhamentos a ele vinculados. | Essencial |

### 3.5 Evoluções

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF21 | O sistema deve permitir o registro de evoluções vinculadas a um assistido, contendo data, profissional responsável, área de atuação e descrição. | Essencial |
| RF22 | O sistema deve registrar automaticamente a autoria, a data e a hora de cada evolução lançada. | Essencial |
| RF23 | O sistema deve exibir as evoluções de um assistido em ordem cronológica. | Essencial |
| RF24 | O sistema deve permitir a retificação de uma evolução, preservando a versão anterior e registrando o autor e o momento da alteração. | Importante |
| RF25 | O sistema deve permitir a filtragem das evoluções de um assistido por período e por área de atuação. | Importante |
| RF26 | O sistema não deve permitir a exclusão definitiva de evoluções registradas. | Essencial |

### 3.6 Encaminhamentos

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF27 | O sistema deve permitir o registro de encaminhamentos vinculados a um assistido ou a uma demanda, contendo destino, data, profissional responsável e observação. | Essencial |
| RF28 | O sistema deve permitir o registro do desfecho de um encaminhamento. | Importante |
| RF29 | O sistema deve exibir a relação dos encaminhamentos pendentes de desfecho. | Importante |

### 3.7 Consulta e acompanhamento

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF30 | O sistema deve apresentar um painel com as demandas em aberto, organizadas por estado. | Essencial |
| RF31 | O sistema deve permitir a filtragem de demandas por estado, responsável, categoria, período e assistido. | Essencial |
| RF32 | O sistema deve permitir a busca textual na descrição das demandas. | Importante |
| RF33 | O sistema deve destacar visualmente as demandas com prazo vencido. | Importante |
| RF34 | O sistema deve apresentar ao usuário autenticado a relação das demandas sob sua responsabilidade. | Essencial |

### 3.8 Relatórios

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF35 | O sistema deve gerar relatório das demandas de um período determinado, com filtros por estado, categoria e responsável. | Essencial |
| RF36 | O sistema deve gerar relatório de acompanhamento de um assistido, reunindo evoluções e encaminhamentos de um período. | Essencial |
| RF37 | O sistema deve permitir a exportação de relatórios em formato adequado à impressão. | Importante |
| RF38 | O sistema deve registrar a emissão de relatórios que contenham dados de assistidos, indicando autor e data. | Importante |
| RF39 | O sistema deve apresentar indicadores consolidados de demandas abertas, concluídas e vencidas em determinado período. | Desejável |

### 3.9 Notificações

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF40 | O sistema deve sinalizar ao usuário, ao acessá-lo, as demandas sob sua responsabilidade com prazo vencido ou próximo do vencimento. | Importante |
| RF41 | O sistema deve permitir o envio de notificações por correio eletrônico aos profissionais responsáveis por demandas com prazo vencido. | Desejável |

**Observação sobre notificações por aplicativo de mensagens.** A instituição manifestou interesse no envio de avisos aos profissionais por meio de aplicativo de mensagens. O envio automatizado por WhatsApp requer contratação da API oficial da plataforma, com custo e processo de aprovação incompatíveis com as restrições deste projeto. Optou-se, portanto, por notificações internas ao sistema e, subsidiariamente, por correio eletrônico. Nenhuma notificação deve conter dados de saúde ou conteúdo de evolução, limitando-se a indicar a existência de pendência no sistema.

---

## 4. Requisitos não funcionais

### 4.1 Proteção de dados pessoais e sigilo

A instituição informou, no levantamento de requisitos, que o sistema tratará dados de saúde dos assistidos e declarou desconhecer as exigências legais aplicáveis. Diante disso, a equipe estabeleceu como restrição de projeto o conjunto de salvaguardas a seguir. Considerando que parte expressiva dos assistidos é composta por menores de idade, essas salvaguardas são tratadas como requisitos essenciais, e não como funcionalidades opcionais.

| ID | Requisito |
| --- | --- |
| RNF01 | O acesso às evoluções e aos demais dados sensíveis deve observar o princípio da necessidade, sendo restrito aos profissionais autorizados pela instituição. |
| RNF02 | As senhas dos usuários devem ser armazenadas de forma criptografada, vedado o armazenamento em texto legível. |
| RNF03 | O sistema deve manter registro de auditoria das operações de criação, alteração, consulta e emissão de relatório que envolvam dados de assistidos, indicando autor, data e hora. |
| RNF04 | A comunicação entre o navegador e o servidor deve ocorrer por canal criptografado (HTTPS). |
| RNF05 | O sistema deve encerrar automaticamente sessões inativas, considerando o uso em computadores compartilhados. |
| RNF06 | Durante o desenvolvimento, os testes de usabilidade e as demonstrações públicas, incluída a Mostra de Extensão, devem ser utilizados exclusivamente dados fictícios. |
| RNF07 | Nenhum dado real de assistidos ou de suas famílias deve ser inserido em repositório de código, protótipo, ambiente de desenvolvimento ou material de apresentação. |
| RNF08 | Os dados de identificação coletados devem limitar-se ao necessário à finalidade do sistema, observado o princípio da minimização previsto na LGPD. |
| RNF09 | A entrega deve ser acompanhada de orientação formal à instituição quanto à sua condição de controladora dos dados pessoais tratados, incluindo as responsabilidades de definição de permissões, política de retenção, rotina de cópia de segurança e comunicação de incidentes. |
| RNF10 | O sistema deve dispor de rotina de cópia de segurança dos dados, com procedimento documentado para a instituição. |

### 4.2 Usabilidade

| ID | Requisito |
| --- | --- |
| RNF11 | A interface deve ser projetada para usuários com pouca familiaridade com tecnologia, conforme indicado pela instituição, privilegiando linguagem simples e fluxos curtos. |
| RNF12 | O registro de uma nova demanda não deve exigir mais que um formulário e uma confirmação. |
| RNF13 | O sistema deve empregar a terminologia utilizada pela instituição, evitando jargão técnico. |
| RNF14 | O sistema deve apresentar mensagens de erro compreensíveis, indicando a ação corretiva cabível. |
| RNF15 | A interface deve observar critérios de acessibilidade, incluindo contraste adequado e navegação por teclado. |

### 4.3 Confiabilidade e desempenho

| ID | Requisito |
| --- | --- |
| RNF16 | O sistema deve informar o usuário quando uma operação não for concluída em razão de falha de conexão, preservando os dados preenchidos no formulário. |
| RNF17 | As operações de consulta devem responder em até três segundos em condições normais de uso. |
| RNF18 | O sistema deve suportar o uso simultâneo de até dez usuários. |
| RNF19 | O sistema não deve permitir a exclusão definitiva de demandas, evoluções ou encaminhamentos; a supressão deve ocorrer por alteração de estado, preservando o histórico. |

### 4.4 Requisitos técnicos e de manutenção

| ID | Requisito |
| --- | --- |
| RNF20 | O back-end deve ser desenvolvido em linguagem Python, com uso do framework Flask, estruturado segundo o paradigma de orientação a objetos. |
| RNF21 | O front-end deve ser desenvolvido com o framework React, organizado em componentes reutilizáveis. |
| RNF22 | A persistência deve ser realizada em banco de dados relacional. |
| RNF23 | A comunicação entre front-end e back-end deve ocorrer por meio de API web, com contrato documentado. |
| RNF24 | O código-fonte deve ser versionado em repositório Git, com histórico de contribuições dos integrantes da equipe. |
| RNF25 | A solução deve ser implantada em serviço de hospedagem sem custo para a instituição, em provedor que ofereça conexão criptografada. |
| RNF26 | O sistema deve ser entregue acompanhado de documentação de instalação e de manual de uso destinado à instituição. |

---

## 5. Fora de escopo

| Item | Justificativa |
| --- | --- |
| Controle de estoque de materiais de consumo | Constitui domínio distinto, com entidades e regras próprias. A direção da instituição indicou a gestão de demandas como prioridade. Registrado como possibilidade de trabalho futuro. |
| Anexo de laudos e documentos digitalizados | O armazenamento de arquivos contendo dados de saúde exigiria controles adicionais de armazenamento e retenção incompatíveis com o prazo do projeto. O sistema registra a existência do encaminhamento, não o documento. |
| Integração com o aplicativo de cadastro em uso | Depende de informações técnicas ainda não levantadas e de disponibilidade de interface de integração por parte do fornecedor. |
| Funcionamento offline com sincronização posterior | Solução de complexidade elevada, incompatível com o prazo e com o nível de maturidade técnica da equipe. |
| Envio automatizado por WhatsApp | Requer API oficial paga, com processo de aprovação incompatível com as restrições do projeto. |

---

## 6. Questões em aberto

| ID | Questão | Impacto |
| --- | --- | --- |
| QA01 | Definição precisa das permissões por perfil: todos os profissionais devem visualizar todas as demandas e evoluções, ou cada profissional deve visualizar apenas aquelas relativas aos assistidos que atende? | Alto — condiciona a modelagem de controle de acesso e os requisitos RF03 e RF05. |
| QA02 | Esclarecimento quanto ao termo "evolução" empregado no levantamento: refere-se ao acompanhamento clínico ou pedagógico do assistido, ao andamento da demanda levantada em reunião, ou a ambos? | Alto — condiciona a modelagem das entidades e o alcance dos requisitos da seção 3.5. |
| QA03 | Identificação do aplicativo de cadastro de usuários já utilizado pela instituição e verificação da possibilidade de exportação de dados. | Médio — evita duplicidade de cadastro. |
| QA04 | Obtenção de exemplar de relatório efetivamente encaminhado à Prefeitura, com dados suprimidos, para definição do formato e dos campos exigidos. | Alto — condiciona os requisitos RF35, RF36 e RF37. |
| QA05 | Descrição detalhada do fluxo atual de uma reunião de equipe: o que é anotado, por quem, e onde o registro é arquivado. | Alto — condiciona a modelagem das entidades Reunião e Demanda. |
| QA06 | Definição das categorias de demanda e das áreas de atuação utilizadas pela instituição. | Médio — condiciona os requisitos RF10, RF21 e RF31. |
| QA07 | Definição dos campos de identificação do assistido considerados necessários pela instituição. | Médio — condiciona o requisito RF18 e o princípio de minimização. |
| QA08 | Definição, pela instituição, do prazo de retenção dos registros e da política de acesso após o encerramento do acompanhamento. | Médio — condiciona os requisitos RNF08 e RNF09. |

---

## 7. Rastreabilidade

| Informação prestada pela instituição | Requisitos correspondentes |
| --- | --- |
| Dificuldade em retomar demandas anteriores | RF17, RF31, RF32 |
| Ocorrência de demandas esquecidas sem conclusão | RF12, RF30, RF33, RF40 |
| Registro atual em papel e planilhas | RF06, RF10 |
| Necessidade de guardar dados dos assistidos | RF18, RF19 |
| Necessidade de registrar evoluções | RF21 a RF26 |
| Necessidade de registrar encaminhamentos | RF27, RF28, RF29 |
| Necessidade de emissão de relatórios para a Prefeitura e uso interno | RF35, RF36, RF37 |
| Interesse em avisos a profissionais | RF40, RF41 |
| Tratamento de dados sensíveis de assistidos | RNF01 a RNF10 |
| Acesso restrito às dependências da instituição | RNF05 |
| Usuários com pouca familiaridade com tecnologia | RNF11 a RNF15 |
| Instabilidade da conexão de internet | RNF16 |
| Expectativa de agilidade e organização das demandas | RF30, RF31, RF34 |

---

## 8. Critérios de aceitação

O sistema será considerado adequado às necessidades da instituição quando, em validação conduzida junto à equipe do CRIE:

1. Um profissional conseguir registrar uma demanda levantada em reunião sem auxílio da equipe de desenvolvimento;
2. For possível localizar uma demanda registrada anteriormente e consultar seu histórico completo em menos de um minuto;
3. For possível identificar, em uma única tela, todas as demandas em aberto com prazo vencido;
4. For possível registrar uma evolução e consultá-la posteriormente na ficha do assistido;
5. For possível emitir relatório das demandas de um período determinado e relatório de acompanhamento de um assistido;
6. Um profissional não autorizado não conseguir acessar as evoluções de assistidos fora de sua atribuição;
7. A equipe da instituição avaliar a interface como compreensível nos testes de usabilidade previstos na disciplina de Interface Humano-Computador.

---

## 9. Histórico de revisões

| Versão | Data | Descrição | Responsável |
| --- | --- | --- | --- |
| 1.0 | Agosto de 2026 | Versão inicial, elaborada a partir do formulário de levantamento respondido pela direção do CRIE. | Equipe do projeto |
| 2.0 | Agosto de 2026 | Inclusão das evoluções e dos encaminhamentos no escopo, conforme solicitado pela instituição, com a correspondente ampliação dos requisitos de proteção de dados pessoais. | Equipe do projeto |
