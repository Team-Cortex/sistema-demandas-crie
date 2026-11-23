"""Seção 3 (Desenvolvimento por disciplina)."""
import os
import re

WT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # raiz do repositório
FIG = os.path.join(WT, "entregas", "extensao", "figuras")


def fig(nome):
    return os.path.join(FIG, nome)


def consultas_sql():
    """Lê título e comandos de cada consulta em 03_consultas.sql."""
    txt = open(os.path.join(WT, "docs", "modelagem", "sql", "03_consultas.sql"), encoding="utf-8").read()
    itens = []
    for m in re.finditer(r"(Q\d\d)\.\s+(.*?)\n\s*Comandos:\s*(.*?)\n\s*-{5,}", txt, re.S):
        titulo = " ".join(m.group(2).split())
        comandos = " ".join(m.group(3).split())
        itens.append((m.group(1), titulo, comandos))
    return itens


def secao3(d, R):
    d.h1("3 DESENVOLVIMENTO")
    d.p("Esta seção detalha o trabalho realizado em cada disciplina do 2º módulo. Na primeira versão, "
        "Engenharia de Software encontrava-se em estágio adiantado e as demais frentes apresentavam decisões "
        "estruturais. Na segunda, a frente de Banco de Dados concluiu o minimundo e o Diagrama "
        "Entidade-Relacionamento, a de Interface iniciou as personas e o protótipo, e a de Front End montou "
        "a estrutura do projeto React. Na terceira, a frente de Interface concluiu as personas e a de "
        "Programação Orientada a Objetos estruturou o servidor, especificou as primeiras funcionalidades e "
        "propôs o contrato da API, enquanto o modelo relacional permanecia parado.")
    d.p("Ao final do quinto ciclo, todas as frentes têm artefatos concluídos no repositório. O modelo "
        "relacional, ponto crítico das versões 2 e 3, foi concluído e implementado; a API atende às nove "
        "especificações de comportamento; a interface consome a API real; e o sistema está publicado. A "
        "frente de Interface concluiu os cenários de uso, a arquitetura da informação, os fluxos, a "
        "especificação das telas, um protótipo clicável e o plano de testes de usabilidade, cuja execução "
        "permanece pendente.")

    # ------------------------------------------------------------------ 3.1
    d.h2("3.1 Engenharia de Software (BRAENSO)")
    d.h3("3.1.1 Processo de desenvolvimento")
    d.p("Adotou-se processo iterativo e incremental, com ciclos alinhados às datas das entregas parciais "
        "definidas no cronograma da unidade curricular. Cada ciclo compreende: revisão do que foi "
        "produzido, atualização do quadro de tarefas, execução das atividades planejadas e consolidação da "
        "versão correspondente deste relatório. A presente versão corresponde ao encerramento do quinto e "
        "último ciclo, com entrega em 26/11/2026.")
    d.p("A escolha decorre da natureza do projeto: os requisitos foram levantados junto a interlocutor "
        "externo cuja disponibilidade é limitada, e demonstraram-se sujeitos a revisão à medida que o "
        "entendimento do domínio se aprofundou, conforme documentado na seção 2.3. Um processo prescritivo, "
        "com requisitos congelados no início, teria conduzido à implementação de um sistema que não "
        "corresponderia à necessidade real da instituição.")
    d.p(f"A partir do terceiro ciclo, o processo passou a ter uma etapa intermediária entre requisito e "
        f"código: a especificação de comportamento (spec), documento curto que fixa as regras, as mensagens "
        f"de erro e os testes que provarão o comportamento, e que prevalece sobre o código em caso de "
        f"divergência. Nos ciclos 4 e 5, essa sequência foi aplicada a todas as funcionalidades do servidor: "
        f"as nove specs do diretório docs/specs foram escritas antes do código correspondente "
        f"(Quadro {R('q-specs')}). O mesmo princípio foi estendido à interface, com a especificação tela a "
        f"tela (docs/ihc/telas.md), que fixou objetivos, textos, estados e mensagens antes da implementação "
        f"em React.")
    d.p("Na prática, cada funcionalidade percorreu a seguinte sequência: spec; modelo e serviço, com testes; "
        "rota, com testes; atualização do contrato da API; tela; pull request para a branch development; e "
        "integração na branch main, que publica o sistema (seção 3.1.4).")

    d.h3("3.1.2 Documentação de requisitos")
    d.p("O documento de requisitos em versão 4.0, apresentado na versão anterior, contém cinquenta "
        "requisitos funcionais e vinte e oito requisitos não funcionais, classificados por prioridade nas "
        "categorias Essencial, Importante e Desejável, com matriz de rastreabilidade, registro de questões em "
        "aberto, delimitação do que não integra o escopo, critérios de aceitação verificáveis e histórico de "
        "revisões. O documento integral constitui o Apêndice A.")
    d.p("No repositório, o arquivo docs/requisitos.md mantém a versão 2.0, de agosto de 2026, com 41 "
        "requisitos funcionais (RF01 a RF41) e 26 não funcionais (RNF01 a RNF26). Foi essa numeração que as "
        "specs, o contrato da API e a especificação de telas passaram a citar, e é ela que a seção 5.3 usa "
        "para relacionar requisitos e implementação. [[a preencher pela equipe: confirmar se a numeração da "
        "versão 4.0 coincide com a do repositório; se não coincidir, incluir a correspondência no "
        "Apêndice A]].")
    d.p(f"A versão 3 registrou como precedência incorporar aos requisitos as decisões tomadas nas specs, "
        f"para que os dois artefatos não divergissem. Essa precedência foi atendida de forma parcial: as "
        f"decisões estão registradas nas próprias specs, no contrato da API e no mapa do projeto "
        f"(docs/estado-do-projeto.md), com as decisões em aberto numeradas de A1 a A10 "
        f"(Quadro {R('q-decisoes')}), mas o documento de requisitos do repositório não foi revisado no "
        f"período. [[a preencher pela equipe: informar se a versão 4.0 foi atualizada]].")

    d.h3("3.1.3 Requisitos não funcionais de proteção de dados")
    d.p("Dada a natureza dos dados tratados, os requisitos de proteção receberam tratamento destacado. A "
        "instituição informou que o sistema armazenaria dados de saúde de pessoas com deficiência, parcela "
        "expressiva das quais menores de idade, e declarou desconhecer as exigências legais aplicáveis "
        "(BRASIL, 2018a).")
    d.p("A equipe apresentou à direção duas alternativas de modelo de visibilidade: acesso restrito, em que "
        "cada profissional visualizaria apenas os registros das pessoas que acompanha, e acesso aberto a "
        "todos os profissionais cadastrados. A instituição, na condição de responsável pelos dados que "
        "trata, optou pelo acesso aberto. Registrada a decisão, a equipe estabeleceu como compensação o "
        "registro de auditoria de todas as operações que envolvam dados de pessoas atendidas, incluindo as "
        "consultas, com identificação de autor, data e hora, de modo que a instituição possa verificar "
        "posteriormente quem acessou cada informação. A alternativa restritiva foi mantida no código, "
        "desligada, disponível caso a instituição reveja sua decisão.")
    d.p("Nos ciclos 4 e 5, as restrições definidas para o desenvolvimento passaram das especificações para "
        "o código e para o banco de dados:")
    d.alineas([
        "a) **dados fictícios:** a carga de demonstração (backend/seed.py) usa nomes como \"Bruna "
        "Fictícia\" e \"Assistido Fictício A\" e e-mails do domínio reservado exemplo.test, e recusa "
        "execução no ambiente de produção; o protótipo e as telas deste relatório usam os mesmos dados;",
        "b) **nenhum dado real nem segredo no repositório:** a verificação automática de segredos examinou "
        "213 arquivos sem achados na execução de 23/11/2026, e as credenciais de produção ficam em "
        "variáveis de ambiente da plataforma de hospedagem;",
        "c) **senha apenas como hash:** o atributo da senha é privado à classe Usuario e só é manipulado "
        "pelos métodos definir_senha e senha_confere (seção 3.4.2); a senha nunca volta em resposta da API;",
        "d) **nenhuma exclusão definitiva:** nenhum recurso da API aceita o método DELETE; no mapeamento "
        "objeto-relacional, histórico, evolução e auditoria recusam alteração e exclusão, e demanda e "
        "encaminhamento recusam exclusão; no PostgreSQL, gatilhos (triggers) repetem essas regras para "
        "quem acessar o banco diretamente;",
        "e) **auditoria:** toda operação que envolve dado de pessoa assistida, inclusive a consulta e a "
        "emissão de relatório, grava autor, ação, recurso e momento em tabela que só admite inserção, "
        "consultada pela direção na tela Auditoria;",
        "f) **minimização:** a pessoa assistida é cadastrada apenas pelo nome de tratamento enquanto a "
        "instituição não define os campos necessários (decisão A3)."])
    d.p("Permanecem pendentes dois requisitos de proteção que não dependem de código: a orientação formal à "
        "instituição sobre sua condição de controladora dos dados (RNF09) e a rotina documentada de cópia "
        "de segurança (RNF10).")

    d.h3("3.1.4 Controle de versão")
    d.p("O código-fonte e a documentação do projeto são versionados em repositório Git hospedado no "
        "GitHub, sob organização criada para a equipe (Team-Cortex/sistema-demandas-crie), de modo que "
        "todos os integrantes detenham igual controle sobre o repositório após o encerramento do semestre. "
        "O repositório é público e reúne, em estrutura de monorepo, os diretórios backend, frontend e docs, "
        "além dos arquivos de publicação (vercel.json e api/index.py) e da pasta entregas, que organiza o "
        "material de cada disciplina.")
    d.p(f"A branch main corresponde à versão publicada: cada integração nela gera nova publicação na "
        f"Vercel. O desenvolvimento ocorre em branches temáticas — por exemplo, miguel/cards-backend, "
        f"front/base-telas-prioridade-1 e ihc/documentos —, integradas por pull request na branch "
        f"development, que depois é levada à main. O Quadro {R('q-prs')} registra os pull requests a partir "
        f"da versão 3, e a Figura {R('f-prs')} mostra a lista no GitHub.")
    d.quadro("q-prs", "Pull requests do repositório entre 22/10 e 23/11/2026",
             ["Nº", "Conteúdo", "Origem → destino", "Situação"],
             [["5", "Estrutura inicial do servidor Flask e specs do back-end", "miguel/estrutura-servidor → "
               "development", "Integrado em 05/11/2026"],
              ["6 e 7", "Relatórios de projeto v1 a v3", "docs/relatorio-v3 → development → main",
               "Integrados em 22/10/2026"],
              ["8", "BD1: modelo relacional do recorte, scripts, 17 consultas e seminário",
               "miguel/bd1-projeto-interdisciplinar → development", "Integrado em 16/11/2026"],
              ["9", "Publicação na Vercel: cliente e API no mesmo projeto, banco no Neon",
               "miguel/deploy-vercel → development", "Integrado em 16/11/2026"],
              ["10", "Leva a development para a main e publica em produção", "development → main",
               "Integrado em 16/11/2026"],
              ["11", "BD1: documento no padrão ABNT", "miguel/bd1-documento-abnt → development",
               "Integrado em 17/11/2026"],
              ["12", "Cartões de back-end: autenticação, perfis, auditoria e API de reuniões, demandas, "
               "assistidos, evoluções, encaminhamentos e relatórios", "miguel/cards-backend → development",
               "Integrado em 17/11/2026"],
              ["13", "Leva os PRs 11 e 12 para a main", "development → main", "Integrado em 17/11/2026"],
              ["14", "IHC: cenários, arquitetura da informação, fluxos, telas, plano de testes e protótipo "
               "clicável", "ihc/documentos → development", "Integrado em 18/11/2026"],
              ["15", "Front-end: cliente da API, layout base e telas de prioridade 1",
               "front/base-telas-prioridade-1 → development", "Integrado em 18/11/2026"],
              ["16", "Front-end: telas de prioridade 2 e 3", "front/telas-prioridade-2 → development",
               "Integrado em 18/11/2026"],
              ["17", "Front-end e material de IHC em produção", "development → main", "Integrado em 18/11/2026"],
              ["18", "Revisão visual da interface: texto no lugar de ícones e selos",
               "front/visual-sem-enfeite → development", "Integrado em 23/11/2026"],
              ["19", "Integração contínua de testes e criação da primeira conta da direção em produção",
               "ci/testes-e-primeira-direcao → development", "Aberto em 23/11/2026"],
              ["20", "Pasta de entregas: exigências oficiais, checklists e pacote de BD1",
               "docs/entregas → development", "Aberto em 23/11/2026"],
              ["21", "Ajustes finais: orientação a objetos no cliente, sessão por inatividade, aviso de prazo "
               "e documentação de POO", "front/ajustes-finais → development", "Aberto em 23/11/2026, "
               "aguardando revisão"]],
             "elaborado pelos autores a partir do repositório no GitHub (2026). Datas no horário de Brasília.",
             larguras=[1.3, 7.0, 4.9, 2.8], tamanho=9)
    d.figura("f-prs", "Lista de pull requests do repositório no GitHub", fig("github-pull-requests.png"),
             "captura de tela da página pública do repositório Team-Cortex/sistema-demandas-crie, elaborada "
             "pelos autores (23/11/2026).", largura_cm=14.5)
    d.p("Três observações decorrem do quadro. Primeira: o pull request 5, que aguardava revisão desde "
        "16/10/2026, foi integrado em 05/11/2026, cumprindo a primeira atividade planejada na versão 3; a "
        "partir dele, a integração passou a acompanhar a produção, e os pull requests 8 a 17 foram "
        "integrados no mesmo dia da abertura ou no dia seguinte. Segunda: nenhum pull request do período "
        "registra revisão formal no GitHub, o que não atende à regra definida na versão 3, de revisão por ao "
        "menos um integrante antes da integração; como medida, o pull request 19 passa a executar os testes "
        "automaticamente em cada pull request (seção 3.1.5). [[a preencher pela equipe: como a revisão "
        "entre integrantes foi feita fora do GitHub, se foi]]. Terceira: os 159 commits feitos entre 22/10 "
        "e 23/11/2026, sem contar os de integração, foram registrados a partir de uma única conta, a do "
        "integrante da frente de back-end, que também consolidou no repositório os artefatos de IHC e de "
        "BD1. [[a preencher pela equipe: contribuição de cada integrante no período, inclusive a realizada "
        "fora do repositório — quadro Kanban, Figma, banner, contato com a instituição e testes]].")
    d.p("A convenção de commits unitários com mensagem no padrão tipo(escopo): efeito, em português, "
        "registrada na versão 3, foi seguida: 156 dos 159 commits do período usam um dos tipos feat (79), "
        "docs (33), fix (20), test (7), refactor (7), chore (6) e style (4). Os pull requests de código "
        "foram integrados por merge commit, que preserva os commits individuais.")

    d.h3("3.1.5 Verificação, validação e testes")
    d.p("O planejamento de testes prevê três níveis: testes unitários das regras de negócio, independentes "
        "da camada de apresentação; testes de integração dos endpoints da API; e validação junto à "
        "instituição parceira, mediante demonstração do sistema e verificação dos critérios de aceitação. "
        "Os dois primeiros níveis foram implementados e são executados automaticamente; o terceiro é "
        "tratado na seção 6.")
    d.p(f"No servidor, a suíte pytest cresceu de sete testes, na versão 3, para 570 testes na branch "
        f"development, todos aprovados na execução do GitHub Actions de 23/11/2026, em banco SQLite em memória "
        f"(Tabela {R('t-testes')}). Os testes estão organizados em 28 arquivos e cobrem as regras dos "
        f"modelos (transições de estado da demanda, imutabilidade do histórico e das evoluções, desfecho "
        f"único do encaminhamento, hash de senha); as rotas de cada recurso, com os códigos de resposta do "
        f"contrato; as permissões por perfil, inclusive com a regra restritiva de acesso ligada; a "
        f"auditoria das leituras; as migrações; e a ausência de consultas repetidas por linha nos "
        f"relatórios. As 25 combinações de estado de origem e de destino da demanda são testadas tanto na "
        f"rota quanto no serviço.")
    d.p("No cliente, a verificação compreende a análise estática com ESLint, a geração do build de "
        "produção e quatro testes executados com o executor nativo do Node.js, que cobrem as regras de "
        "validação do formulário de demanda, as transições oferecidas na tela e a preservação do rascunho "
        "do formulário por conta de usuário (RNF16).")
    d.p(f"O pull request 19, aberto em 23/11/2026, acrescenta um fluxo de integração contínua no GitHub "
        f"Actions (.github/workflows/testes.yml), que executa, a cada pull request e a cada envio às "
        f"branches development e main, a suíte do servidor, a verificação de segredos e, no cliente, "
        f"instalação, lint, build e testes. Na primeira execução, sobre o próprio pull request 19, os dois "
        f"trabalhos foram concluídos com sucesso: 587 testes do servidor aprovados — os 570 da branch "
        f"development e 17 do novo comando de criação da primeira conta da direção —, verificação de "
        f"segredos sem achados em 213 arquivos, e lint, build e quatro testes do cliente aprovados "
        f"(Figura {R('f-ci')}).")
    d.tabela("t-testes", "Verificação automatizada em 23/11/2026",
             ["Camada", "Ferramenta", "Escopo", "Resultado"],
             [["Servidor (GitHub Actions, PR 19)", "pytest", "28 arquivos de teste da development e os testes do comando de "
               "criação da primeira direção", "587 aprovados, 0 falhas"],
              ["Servidor (GitHub Actions, PR 19)", "check-segredo", "arquivos versionados", "213 arquivos, "
               "sem achados"],
              ["Cliente (GitHub Actions, PR 19)", "ESLint", "código do cliente", "sem erros"],
              ["Cliente (GitHub Actions, PR 19)", "node --test", "2 arquivos de teste", "4 aprovados, 0 falhas"],
              ["Cliente (GitHub Actions, PR 19)", "Vite", "build de produção", "concluído"]],
             "elaborado pelos autores a partir do registro da execução 45199075617 do "
             "GitHub Actions (23/11/2026).", larguras=[4.4, 2.6, 5.0, 4.0])
    d.figura("f-ci", "Execução dos testes no GitHub Actions (pull request 19)",
             fig("github-actions-ci.png"),
             "captura de tela da página pública da execução, elaborada pelos autores (23/11/2026).",
             largura_cm=14.5)

    d.h3("3.1.6 Qualidade de software")
    d.p(f"A discussão de qualidade adota como referência o modelo de qualidade de produto da norma ISO/IEC "
        f"25010 (INTERNATIONAL ORGANIZATION FOR STANDARDIZATION, 2011), que organiza a qualidade em "
        f"características como adequação funcional, eficiência de desempenho, compatibilidade, usabilidade, "
        f"confiabilidade, segurança, manutenibilidade e portabilidade. O Quadro {R('q-qualidade')} relaciona "
        f"as características mais relevantes para o contexto da instituição às evidências produzidas e às "
        f"limitações conhecidas.")
    d.quadro("q-qualidade", "Características de qualidade, evidências e limitações",
             ["Característica", "Evidência no projeto", "Limitação conhecida"],
             [["Adequação funcional", "Requisitos rastreados até specs, rotas, telas e testes (seção 5.3); "
               "587 testes do servidor aprovados no GitHub Actions", "RF02, RF18 e RF37 atendidos em parte; RF41 não "
               "implementado"],
              ["Usabilidade", "Personas, cenários, arquitetura da informação e especificação de telas com "
               "estados e mensagens; formulário único com confirmação (RNF12); rascunho preservado (RNF16)",
               "Testes com usuários não realizados até 23/11/2026; card sorting simulado pela equipe"],
              ["Segurança", "Hash de senha; token de 30 minutos revogado no logout; limite de tentativas de "
               "login; auditoria somente inserção, inclusive de leituras; verificação de segredos; HTTPS",
               "Acesso aberto por decisão da instituição; o limite de tentativas fica na memória de cada "
               "instância do servidor, o que o enfraquece na Vercel; uso de cookie HttpOnly em aberto (A5)"],
              ["Confiabilidade", "Nenhuma exclusão definitiva (ORM e gatilhos); bloqueio de linha nas escritas "
               "concorrentes; formato de erro único em português", "Sem rotina de cópia de segurança "
               "documentada (RNF10); migrações testadas em SQLite, sem verificação automática no PostgreSQL"],
              ["Manutenibilidade", "Camadas schemas, routes, services e models; cliente de API único; "
               "contrato documentado; specs; convenção de commits; integração contínua (PR 19)",
               "Commits concentrados em uma conta; revisão de pull request não registrada no GitHub"],
              ["Eficiência de desempenho", "Leituras auditadas sem consulta por linha, com teste específico",
               "Tempo de resposta (RNF17) e uso simultâneo (RNF18) não medidos"],
              ["Portabilidade", "O mesmo código roda em desenvolvimento (Docker Compose), em teste (SQLite) "
               "e em produção (Vercel e Neon)", "—"]],
             "elaborado pelos autores com base na ISO/IEC 25010 (2011) e no repositório (2026).",
             larguras=[3.2, 6.6, 6.2], tamanho=9)
    d.p("Do ponto de vista do processo, a qualidade foi tratada em três frentes: prevenção, com as specs "
        "escritas antes do código e o contrato da API como referência comum às duas pontas; detecção, com "
        "testes automatizados a cada funcionalidade e, a partir do pull request 19, execução automática no "
        "GitHub; e revisão, com uma revisão independente do código do servidor registrada na descrição do "
        "pull request 12, que encontrou seis problemas corrigidos antes da integração — entre eles, valores "
        "de evolução e nomes de assistidos que iriam para o log em caso de erro do banco, e a possibilidade "
        "de dois pedidos simultâneos gravarem dois desfechos para o mesmo encaminhamento. A principal "
        "fragilidade de processo foi a ausência de revisão registrada entre integrantes nos pull requests.")

    # ------------------------------------------------------------------ 3.2
    d.h2("3.2 Interface Humano-Computador (BRAINHC)")
    d.h3("3.2.1 Análise do perfil de usuário")
    d.p("O levantamento junto à instituição forneceu os elementos iniciais para a caracterização dos "
        "usuários. A direção informou que os profissionais possuem, em geral, baixa familiaridade com "
        "tecnologia, indicando expressamente a necessidade de que o sistema seja \"bem simples\". Informou "
        "ainda que o acesso ocorrerá exclusivamente nas dependências da instituição, por computador, e que "
        "a conexão de internet local apresenta instabilidade intermitente. Estima-se cerca de seis usuários "
        "simultâneos, distribuídos entre a direção e os profissionais das equipes pedagógica, de saúde e do "
        "serviço de convivência.")
    d.p("Da análise decorreram os requisitos não funcionais de usabilidade: linguagem simples e "
        "terminologia da própria instituição; registro de nova demanda em um único formulário e uma "
        "confirmação; mensagens de erro compreensíveis, com indicação da ação corretiva; critérios de "
        "acessibilidade, incluindo contraste adequado e navegação por teclado; e preservação dos dados "
        "preenchidos quando a operação falhar por indisponibilidade de conexão (RNF11 a RNF16).")
    d.h3("3.2.2 Personas")
    d.p("Foram elaboradas três personas, concluídas em 08/10/2026 e anexadas ao cartão correspondente no "
        "quadro de gestão: a persona da Direção, primária, a do Assistente Social e a da Equipe Pedagógica. "
        "A persona da direção, Júlia Costa, diretora fictícia do CRIE, tem como dores a perda de tempo para "
        "localizar o histórico de demandas antigas e o excesso de processos em papel, e como desejo "
        "centralizar a gestão das demandas em uma única tela — desejo que fundamenta o critério de aceitação "
        "de identificar, em tela única, as demandas em aberto com prazo vencido. As duas outras personas "
        "representam os profissionais das equipes, cujo diferencial é a baixa familiaridade tecnológica, "
        "determinante para o grau de simplicidade das telas de registro.")
    d.p(f"No repositório (docs/ihc/personas.md), apenas a persona da direção está transcrita. [[a preencher "
        f"pela equipe: transcrever as personas do assistente social e da equipe pedagógica — nome fictício, "
        f"frase, proficiência tecnológica, contexto, objetivos e frustrações — e inserir a imagem das três "
        f"personas na Figura {R('f-personas')}]]. O perfil de coordenação de setor, mencionado na versão 2, "
        f"não recebeu persona nem classe própria, porque a instituição não distinguiu permissões para ele "
        f"(decisão A4).")
    d.figura_pendente("f-personas", "Personas dos três perfis de usuário",
                      "imagem das três personas (direção, assistente social e equipe pedagógica) exportada do "
                      "cartão do Trello ou do Figma, largura de pelo menos 1280 px, sem foto de pessoa real",
                      "entregas/extensao/prints/22-personas.png",
                      "[[elaborado pelos autores (2026)]].")
    d.h3("3.2.3 Cenários de uso")
    d.p(f"A partir das personas, foram escritos seis cenários de uso (docs/ihc/cenarios-de-uso.md), ao "
        f"menos um por persona, cada um ligado aos requisitos que exercita e a uma tarefa do teste de "
        f"usabilidade (Quadro {R('q-cenarios')}). As duas inconsistências apontadas na versão 3 foram "
        f"corrigidas: não há cenário de relatório para a Prefeitura, requisito retirado do escopo, "
        f"substituído pelo cenário C2, de consulta ao que já foi feito quando uma demanda se repete; e "
        f"nenhum cenário supõe telas escondidas por perfil, exceto as funções administrativas da direção, "
        f"em respeito ao acesso aberto. Os nomes de profissionais e de pessoas atendidas usados nos cenários "
        f"são fictícios e coincidem com os da carga de demonstração.")
    d.quadro("q-cenarios", "Cenários de uso, requisitos exercitados e tarefas de teste",
             ["Cenário", "Persona", "Objetivo", "Requisitos", "Tarefa"],
             [["C1", "Direção", "Começar o dia vendo o que está atrasado e cobrar quem precisa",
               "RF30, RF33, RF16", "T1, T6"],
              ["C2", "Direção", "Achar o que já foi feito numa demanda que voltou a aparecer",
               "RF31, RF32, RF17", "T2"],
              ["C3", "Assistente social", "Registrar a demanda que saiu da reunião de saúde",
               "RF10, RF11, RNF12, RNF16", "T3"],
              ["C4", "Assistente social", "Atualizar o andamento e registrar o encaminhamento à rede",
               "RF13, RF15, RF27", "T4"],
              ["C5", "Equipe pedagógica", "Entrar, ver o aviso de prazo e concluir a própria demanda",
               "RF40, RF34, RF13", "T5"],
              ["C6", "Equipe pedagógica", "Lançar a evolução de um assistido depois da oficina",
               "RF21, RF20", "T7"]],
             "elaborado pelos autores a partir de docs/ihc/cenarios-de-uso.md (2026).",
             larguras=[1.6, 3.0, 6.4, 3.3, 1.7])
    d.h3("3.2.4 Arquitetura da informação")
    d.p("A arquitetura da informação (docs/ihc/arquitetura-da-informacao.md) seguiu as etapas de "
        "diagnóstico, card sorting, mapa do site, wireframe e tree testing, e organizou-se pelos quatro "
        "sistemas descritos por Rosenfeld, Morville e Arango (2015): organização, navegação, rotulação e "
        "busca. O diagnóstico de usuários, conteúdo e contexto identificou a demanda como objeto central e a "
        "baixa familiaridade tecnológica dos profissionais como restrição principal.")
    d.p("O card sorting foi simulado pela própria equipe, a partir das personas e dos cenários, com 22 "
        "cartões correspondentes às funções do sistema na linguagem da instituição. Ele não foi realizado "
        "com profissionais do CRIE, o que limita sua validade e está registrado no documento. Os grupos "
        "formados deram origem aos itens do menu: Painel, Minhas demandas, Demandas, Reuniões, Assistidos e "
        "Encaminhamentos para todos os perfis, e Usuários, Relatórios e Auditoria apenas para a direção. A "
        "profundidade máxima é de três níveis a partir do painel, e cada tela tem uma única ação principal. "
        "O tree testing foi proposto, com uma pergunta por cenário, mas não foi executado.")
    d.p(f"A rotulação adotou a palavra da instituição, e não a do sistema (RNF13), conforme exemplos do "
        f"Quadro {R('q-rotulos')}.")
    d.quadro("q-rotulos", "Rótulos adotados e evitados na interface",
             ["Usamos", "Evitamos", "Motivo"],
             [["Entrar / Sair", "Login / Logout", "Português de uso comum"],
              ["Registrar demanda", "Nova demanda, Criar, Adicionar", "Verbo usado pela direção para reunião e "
               "demanda"],
              ["Aberta, Em andamento, Aguardando terceiros, Concluída, Cancelada", "Status, Pendente, Fechada",
               "Os cinco estados do RF12"],
              ["Vencida", "Atrasada, Expirada", "Palavra do RF33 e da spec 02"],
              ["Assistido / Nome de tratamento", "Paciente, Cliente, Usuário", "Termo da instituição"],
              ["Evolução / Retificar", "Prontuário, Editar", "Retificar deixa claro que a versão anterior fica"],
              ["Cancelar demanda", "Excluir, Apagar", "Nada é apagado (RNF19)"]],
             "elaborado pelos autores a partir de docs/ihc/arquitetura-da-informacao.md (2026).",
             larguras=[5.4, 4.6, 6.0])
    d.h3("3.2.5 Fluxos de navegação")
    d.p(f"Os nove fluxos principais foram descritos passo a passo (docs/ihc/fluxos.md), com a contagem "
        f"mínima de passos — cada clique, escolha numa lista ou campo preenchido conta um passo —, que serve "
        f"de referência para medir a eficiência nos testes de usabilidade (Quadro {R('q-fluxos')}). Foram "
        f"descritos também os fluxos de exceção comuns a todas as telas: falta de conexão, sessão encerrada, "
        f"perfil sem acesso, registro inexistente e regra de negócio recusada.")
    d.quadro("q-fluxos", "Fluxos de navegação e passos mínimos",
             ["Fluxo", "Cenário", "Passos mínimos", "Telas percorridas"],
             [["F1 Entrar", "todos", "3", "Entrar → Painel"],
              ["F2 Registrar demanda", "C3", "7", "Painel → Registrar demanda → confirmação → Demanda"],
              ["F3 Mudar estado", "C4, C5", "4", "Demanda → diálogo → Demanda"],
              ["F4 Anotar", "C4", "3", "Demanda"],
              ["F5 Trocar responsável", "C1", "4", "Demanda → diálogo → Demanda"],
              ["F6 Achar demanda antiga", "C2", "3", "Demandas → Demanda"],
              ["F7 Do aviso de prazo à demanda", "C5", "1", "Painel → Demanda"],
              ["F8 Lançar evolução", "C6", "7", "Assistidos → Ficha → Lançar evolução → Ficha"],
              ["F9 Sair", "todos", "1", "qualquer tela → Entrar"]],
             "elaborado pelos autores a partir de docs/ihc/fluxos.md (2026).", larguras=[4.6, 2.0, 2.4, 7.0])
    d.h3("3.2.6 Especificação das telas e protótipo interativo")
    d.p("A especificação tela a tela (docs/ihc/telas.md) define, para as treze telas do sistema, o "
        "objetivo, quem a vê, a rota da API consumida, o conteúdo, a ação principal, os estados (carregando, "
        "vazio, erro e sucesso) e os textos exibidos. Ela estabelece regras comuns: menu lateral só com "
        "texto; título da página igual ao item do menu; estado da demanda escrito por extenso e nunca "
        "indicado apenas por cor; contraste mínimo de 4,5:1; foco visível; navegação por teclado; alvos de "
        "clique de pelo menos 44 px; e texto-base de 16 px, com referência às diretrizes de acessibilidade "
        "WCAG 2.2 (W3C, 2023).")
    d.p(f"O protótipo interativo foi produzido em duas formas. No Figma, ferramenta adotada desde o segundo "
        f"ciclo, [[a preencher pela equipe: situação final do protótipo no Figma, telas concluídas e "
        f"link]]. No repositório, há um protótipo clicável em HTML (docs/ihc/prototipo/index.html), que "
        f"funciona sem internet, navega entre as telas por fluxos e áreas clicáveis (hotspots), permite "
        f"simular os três perfis e traz um roteiro com as tarefas T1 a T7 para conduzir as sessões de teste "
        f"(Figuras {R('f-proto-painel')} a {R('f-proto-roteiro')}). O protótipo usa somente dados fictícios "
        f"e guarda as alterações apenas na memória da aba; autenticação, permissões, API, banco de dados e "
        f"retificação de evoluções existem só no sistema real. O protótipo foi gerado antes da revisão "
        f"visual do pull request 18 e ainda exibe ícones e selos coloridos que o sistema publicado "
        f"substituiu por texto (seção 3.5.6).")
    fonte_proto = ("captura do protótipo clicável (docs/ihc/prototipo/index.html) em largura de 1280 px, com "
                   "dados fictícios, elaborada pelos autores (23/11/2026).")
    d.figura("f-proto-painel", "Protótipo clicável: painel da direção",
             fig("prototipo-painel-direcao.png"), fonte_proto, largura_cm=13.5)
    d.figura("f-proto-registrar", "Protótipo clicável: formulário Registrar demanda",
             fig("prototipo-registrar-demanda.png"), fonte_proto, largura_cm=13.5)
    d.figura("f-proto-detalhe", "Protótipo clicável: detalhe da demanda",
             fig("prototipo-detalhe-demanda.png"), fonte_proto, largura_cm=13.5)
    d.figura("f-proto-ficha", "Protótipo clicável: ficha do assistido",
             fig("prototipo-ficha-assistido.png"), fonte_proto, largura_cm=13.5)
    d.figura("f-proto-roteiro", "Protótipo clicável: roteiro das tarefas T1 a T7",
             fig("prototipo-roteiro-fluxos.png"), fonte_proto, largura_cm=13.5)
    d.h3("3.2.7 Planejamento da avaliação de usabilidade")
    d.p("O plano de testes (docs/ihc/plano-de-testes.md) define o método, o perfil dos participantes, as "
        "tarefas, as métricas, a classificação de gravidade dos problemas, o roteiro do moderador, o "
        "questionário de satisfação e confiança e o termo de participação voluntária, além de modelos de "
        "planilha para registro anonimizado. O pull request 20, ainda em aberto, acrescenta um roteiro de "
        "bolso de quinze minutos por participante (entregas/ihc/roteiro-de-bolso.md). Esses elementos são "
        "apresentados na seção 6.3, junto à validação. O relatório de usabilidade "
        "(docs/ihc/relatorio-de-usabilidade.md) está estruturado — perfil dos voluntários, resultados por "
        "tarefa, gráficos, resposta emocional e problemas com sugestão de correção —, mas permanece sem "
        "dados, porque os testes ainda não foram realizados.")

    # ------------------------------------------------------------------ 3.3
    d.h2("3.3 Banco de Dados 1 (BRABCD1)")
    d.h3("3.3.1 Especificação do minimundo")
    d.p("A partir da leitura do documento de requisitos, foi elaborada a especificação do minimundo. A "
        "instituição atende pessoas assistidas, organizadas em setores de atendimento. Cada setor realiza "
        "reuniões semanais, das quais decorrem demandas de articulação. Cada demanda origina ações definidas "
        "em reunião, atribuídas a profissionais responsáveis, e pode resultar em encaminhamentos a serviços "
        "da rede externa, os quais podem exigir retornos de acompanhamento periódicos até o desfecho. "
        "Registram-se ainda as evoluções referentes ao acompanhamento das pessoas assistidas e o histórico "
        "de todas as alterações realizadas. O minimundo e o DER foram integrados ao repositório em "
        "13/10/2026, no diretório docs/modelagem.")
    d.h3("3.3.2 Entidades do domínio")
    d.p(f"O Quadro {R('q-entidades')} relaciona as entidades do minimundo à forma como foram implementadas "
        f"no banco do sistema.")
    d.quadro("q-entidades", "Entidades do domínio e sua implementação",
             ["Entidade", "Descrição", "Implementação no sistema"],
             [["Usuário", "Pessoa que acessa o sistema, com especialização por perfil",
               "Tabela usuario, com herança de tabela única pela coluna perfil"],
              ["Pessoa assistida", "Pessoa atendida pela instituição", "Tabela assistido, só com o nome de "
               "tratamento (A3)"],
              ["Setor", "Pedagógico, saúde ou serviço de convivência", "Enumeração fechada na coluna "
               "reuniao.setor"],
              ["Reunião", "Encontro semanal de um setor", "Tabelas reuniao e reuniao_participante"],
              ["Demanda", "Situação que exige articulação com a rede", "Tabela demanda"],
              ["Categoria de demanda", "Classificação da demanda", "Campo de texto opcional em demanda, sem "
               "catálogo (A2)"],
              ["Ação", "Providência definida em reunião, com responsável", "Sem tabela própria: as "
               "providências são anotações no histórico da demanda"],
              ["Serviço da rede", "Serviço externo acionado: CRAS, unidade de saúde, escola, conselho",
               "Não implementado; o destino do encaminhamento é texto livre (A1)"],
              ["Encaminhamento", "Direcionamento a serviço da rede ou a profissional interno",
               "Tabela encaminhamento, com desfecho único"],
              ["Retorno de acompanhamento", "Registro periódico do acompanhamento de um encaminhamento",
               "Não implementado nesta versão"],
              ["Evolução", "Registro do acompanhamento da pessoa assistida", "Tabela evolucao, com versões "
               "por retificação"],
              ["Histórico de demanda", "Registro imutável das alterações de estado e anotações",
               "Tabela historico_demanda, somente inserção"],
              ["Registro de auditoria", "Quem fez o quê, quando, com dado de pessoa assistida",
               "Tabela auditoria, somente inserção"]],
             "elaborado pelos autores a partir do minimundo e de backend/app/models (2026).",
             larguras=[3.4, 6.2, 6.4], tamanho=9)
    d.h3("3.3.3 Diagrama Entidade-Relacionamento")
    d.p(f"O Diagrama Entidade-Relacionamento (DER) do sistema representa as entidades, seus atributos e os "
        f"relacionamentos com as respectivas cardinalidades (Figura {R('f-der')}). A versão integral do "
        f"diagrama, em formato editável, consta do Apêndice D.")
    d.figura("f-der", "Diagrama Entidade-Relacionamento do sistema", fig("der-sistema-v2.png"),
             "elaborado pelos autores (2026). Arquivo docs/modelagem/DER_CRIE_v2.png do repositório.")
    d.h3("3.3.4 Modelo relacional e implementação no PostgreSQL")
    d.p(f"A derivação do modelo relacional, que permaneceu parada entre 08/10 e 22/10/2026, foi concluída "
        f"no quarto ciclo e implementada como migração do Alembic (b0f13416410c, de 04/11/2026), que cria as "
        f"tabelas do domínio no PostgreSQL. Duas migrações de 16/11/2026 completaram o esquema: "
        f"3df29fd96f0b, com a tabela token_revogado, usada para invalidar o token no logout, e "
        f"3f00c11df825, com a tabela auditoria (Quadro {R('q-tabelas')}). As decisões que a versão 3 havia "
        f"fixado na lista de verificação do cartão, e os dois cartões de proteção de dados criados em "
        f"21/10/2026, foram atendidos:")
    d.alineas([
        "a) estados da demanda modelados como domínio fechado (enumeração estado_demanda), assim como a "
        "prioridade e o setor;",
        "b) hierarquia de perfis em tabela única usuario, com a coluna perfil;",
        "c) histórico, evolução e auditoria somente com inserção, e demanda e encaminhamento sem exclusão, "
        "garantidos no ORM e por gatilhos no PostgreSQL; a retificação de evolução cria nova linha que "
        "aponta para a anterior;",
        "d) restrições de verificação (CHECK) no encaminhamento: vínculo obrigatório com pessoa assistida, "
        "com demanda ou com ambas, e desfecho, autor do desfecho e momento gravados em conjunto;",
        "e) senha armazenada apenas como hash e pessoa assistida limitada ao nome de tratamento."])
    d.p("O destino do encaminhamento (decisão A1) não foi definido e permanece como texto livre de até 200 "
        "caracteres; a entidade serviço da rede e o retorno de acompanhamento ficaram fora desta versão.")
    d.quadro("q-tabelas", "Tabelas do banco do sistema e restrições relevantes",
             ["Tabela", "Conteúdo", "Restrições relevantes"],
             [["usuario", "nome, e-mail, perfil, situação, hash da senha, data de cadastro",
               "e-mail único; perfil define a subclasse; desativação no lugar de exclusão"],
              ["assistido", "nome de tratamento, situação, data de cadastro", "minimização de dados (A3)"],
              ["assistido_profissional", "quem acompanha quem, data de início",
               "chave composta; alimenta a regra restritiva desligada"],
              ["reuniao", "data, setor, data de registro", "setor em enumeração"],
              ["reuniao_participante", "participantes de cada reunião", "tabela associativa"],
              ["demanda", "descrição, categoria, prioridade, prazo, estado, responsável, reunião de origem, "
               "pessoa assistida opcional", "estado e prioridade em enumeração; gatilho recusa DELETE"],
              ["historico_demanda", "autor, tipo (estado ou anotação), estados anterior e novo, texto, "
               "momento", "gatilho recusa UPDATE e DELETE"],
              ["evolucao", "pessoa assistida, profissional, data, área de atuação, descrição, momento, versão "
               "retificada", "gatilho recusa UPDATE e DELETE"],
              ["encaminhamento", "pessoa assistida e/ou demanda, destino, data, responsável, observação, "
               "desfecho", "CHECK de vínculo e de desfecho completo; gatilho recusa DELETE"],
              ["auditoria", "autor, ação, recurso, identificador, pessoa assistida, detalhe, momento",
               "gatilho recusa UPDATE e DELETE"],
              ["token_revogado", "identificador do token encerrado e sua validade",
               "linha removida após a expiração original"]],
             "elaborado pelos autores a partir de backend/migrations e docs/estado-do-projeto.md (2026).",
             larguras=[3.6, 6.6, 5.8], tamanho=9)

    d.h3("3.3.5 Projeto da disciplina: recorte, scripts e consultas")
    d.p(f"Para a avaliação de Banco de Dados 1, cujo enunciado pede de quatro a seis tabelas, a equipe "
        f"implementou em MySQL 8.4 o recorte central do sistema (pull requests 8 e 11): usuario, assistido, "
        f"assistido_profissional, reuniao, demanda e evolucao, com os mesmos nomes de tabelas e colunas do "
        f"servidor. O recorte tem relacionamentos dos três tipos — 1:1 (retificação de evolução, com chave "
        f"estrangeira única), 1:N e N:N (acompanhamento) — e está documentado com universo de discurso, DER "
        f"na notação de Heuser (2000) (Figura {R('f-der-bd1')}), notação textual, verificação da primeira à "
        f"terceira forma normal e dicionário de dados no documento "
        f"docs/modelagem/bd1/Documento_BD1_Equipe_Cortex.pdf, elaborado no padrão ABNT (EQUIPE CORTEX, 2026a).")
    d.figura("f-der-bd1", "DER do recorte de Banco de Dados 1",
             fig("der-recorte-bd1.png"),
             "elaborado pelos autores (2026). Arquivo docs/modelagem/bd1/DER_recorte_BD1.svg do repositório.",
             largura_cm=14.0)
    d.p(f"Quatro scripts compõem a entrega (docs/modelagem/sql) e, segundo o registro do pull request 8, "
        f"foram executados em sequência, a partir de um banco vazio, sem erro: 01_criacao_banco.sql, com "
        f"DROP e CREATE DATABASE, CREATE TABLE e ALTER TABLE; 02_carga_dados.sql, com 103 registros "
        f"fictícios distribuídos para que cada consulta tenha resultado (Tabela {R('t-carga')}); "
        f"03_consultas.sql, com 17 consultas comentadas (Quadro {R('q-consultas')}); e "
        f"04_manutencao_dados.sql, com inserção, atualização e remoção que respeitam as regras do "
        f"minimundo, incluindo a desativação de usuário no lugar da exclusão e uma exclusão recusada pelo "
        f"banco por integridade referencial. O Apêndice I reproduz duas das consultas.")
    d.tabela("t-carga", "Registros inseridos pela carga de dados do recorte",
             ["Tabela", "Registros", "Diversidade dos dados"],
             [["usuario", "10", "2 da direção, 3 assistentes sociais e 5 da equipe pedagógica; 1 desativado; 1 "
               "sem acompanhamento"],
              ["assistido", "12", "11 ativos e 1 desligado; 2 sem nenhuma demanda"],
              ["assistido_profissional", "21", "acompanhamentos iniciados entre 2020 e 2026; de 1 a 3 "
               "profissionais por assistido"],
              ["reuniao", "13", "os três setores, de agosto a novembro de 2026; 2 reuniões sem demandas"],
              ["demanda", "29", "os cinco estados, as três prioridades e seis categorias; 5 sem assistido; "
               "prazos vencidos, próximos e futuros"],
              ["evolucao", "18", "15 lançamentos e 3 retificações, incluindo uma cadeia de duas versões"],
              ["Total", "103", ""]],
             "Equipe Cortex (2026a, Tabela 1).", larguras=[4.0, 2.2, 9.8])
    linhas = [[q, t, c] for (q, t, c) in consultas_sql()]
    d.quadro("q-consultas", "Consultas SQL do projeto de Banco de Dados 1",
             ["Nº", "Objetivo", "Recursos de SQL"], linhas,
             "elaborado pelos autores a partir de docs/modelagem/sql/03_consultas.sql (2026).",
             larguras=[1.2, 8.6, 6.2], tamanho=8.5)
    d.p("A entrega da disciplina inclui ainda os slides do seminário e um roteiro de apresentação "
        "(docs/modelagem/bd1). O pull request 20 prepara o pacote de envio, com o documento e os quatro "
        "scripts, e registra o nome completo da professora, Letícia Souza Netto Brandi, na folha de rosto "
        "do documento.")

    # ------------------------------------------------------------------ 3.4
    d.h2("3.4 Programação Orientada a Objetos (BRAPROB)")
    d.h3("3.4.1 Decisões arquiteturais")
    d.p("O back-end é estruturado em quatro camadas, com responsabilidades distintas: schemas, que valida "
        "os dados de entrada e serializa as respostas; routes, que apenas traduz entre o protocolo HTTP e as "
        "chamadas de domínio; services, onde residem as regras de negócio que envolvem mais de um objeto, a "
        "sessão do banco e a auditoria; e models, com as entidades, seus métodos e a persistência. A "
        "separação entre rotas e serviços é a decisão arquitetural mais relevante do back-end: sem ela, as "
        "regras se distribuiriam pelas funções de tratamento das requisições, o que descaracterizaria a "
        "orientação a objetos e impediria testar as regras sem a camada HTTP.")
    d.p(f"O sistema adota o estilo cliente-servidor: o cliente é a aplicação React e o servidor é o "
        f"processo Flask, que se comunicam exclusivamente por HTTP com JSON, sob o prefixo /api; o navegador "
        f"não abre conexão com o banco de dados. O sistema foi publicado em 16/11/2026 (pull requests 9 e "
        f"10) em um único projeto da Vercel: o cliente é servido como site estático e a API como função "
        f"Python (api/index.py), no mesmo endereço, e o arquivo vercel.json encaminha os caminhos /api para "
        f"a função e os demais para o cliente, o que dispensa a liberação de origens cruzadas. O banco de "
        f"produção é PostgreSQL no Neon, conectado por variável de ambiente (Figura {R('f-arquitetura')}).")
    d.figura("f-arquitetura", "Arquitetura do sistema e ambiente de publicação",
             fig("diagrama-arquitetura.png"),
             "elaborado pelos autores a partir de vercel.json, api/index.py e docs/arquitetura.md (2026).")
    d.h3("3.4.2 Aplicação dos conceitos de orientação a objetos")
    d.p(f"Os conceitos exigidos pela disciplina — instância de objetos, métodos, encapsulamento, herança e "
        f"polimorfismo — foram aplicados no código do servidor da forma resumida no Quadro {R('q-poo')} e na "
        f"Figura {R('f-classes')}. O Apêndice I reproduz o trecho correspondente à hierarquia de usuários.")
    d.p("**Classes, instâncias e métodos.** Cada entidade do domínio é uma classe mapeada pelo SQLAlchemy "
        "em backend/app/models, e cada requisição trabalha com instâncias dessas classes. As regras ficam "
        "em métodos dos próprios objetos: Demanda.abrir cria a demanda já com o primeiro item de histórico; "
        "mudar_estado, anotar e reatribuir gravam o histórico sozinhos; Evolucao.retificar cria uma nova "
        "versão que aponta para a anterior; e Encaminhamento.registrar_desfecho grava o desfecho uma única "
        "vez. As classes de serviço, como DemandaService, coordenam essas operações com a sessão do banco e "
        "o registro de auditoria.")
    d.p("**Encapsulamento.** O hash da senha é guardado no atributo privado _senha_hash e só é manipulado "
        "por definir_senha, que exige no mínimo oito caracteres e aplica a função de hash, e por "
        "senha_confere, que compara sem expor o valor armazenado. Da mesma forma, o estado da demanda é "
        "validado no próprio atributo: qualquer atribuição fora das transições permitidas levanta erro de "
        "negócio, de modo que nenhuma parte do código consegue deixar a demanda em estado inválido.")
    d.p("**Herança.** A classe abstrata Usuario concentra identificação, autenticação e situação; dela "
        "derivam Direcao e a também abstrata Profissional, da qual derivam AssistenteSocial e "
        "EquipePedagogica. No banco, a hierarquia usa herança de tabela única, e o SQLAlchemy instancia a "
        "subclasse correta conforme a coluna perfil. A herança aparece ainda nos schemas de validação "
        "(FiltroAuditoriaSchema herda de FiltroPeriodo e de Paginacao), nas exceções de domínio e nas "
        "classes auxiliares SemExclusao e SomenteInsercao, aplicadas por herança múltipla às entidades que "
        "não podem ser apagadas ou alteradas.")
    d.p("**Polimorfismo.** Os métodos pode_ver_evolucao, pode_gerir_usuarios, pode_emitir_relatorio e "
        "pode_consultar_auditoria são declarados em Usuario e implementados de forma distinta em Direcao e "
        "em Profissional. As rotas perguntam ao objeto — por exemplo, pelo decorador "
        "exige_permissao(\"pode_gerir_usuarios\", ...) — e nunca comparam o texto do perfil; incluir um novo "
        "perfil exige apenas uma nova subclasse. A regra restritiva de acesso às evoluções está implementada "
        "em Profissional e desligada pelo atributo de classe acesso_restrito, em respeito à decisão da "
        "instituição; os testes verificam os dois comportamentos.")
    d.p("**Erros como exceções.** As violações são levantadas como exceções de domínio e convertidas em "
        "respostas HTTP por tratadores registrados na fábrica da aplicação: ErroDeNegocio em 400, "
        "NaoAutenticado em 401, PermissaoNegada em 403, NaoEncontrado em 404, DadoInvalido em 422 e "
        "MuitasTentativas em 429, sempre no formato {\"erro\": \"mensagem em português\"}.")
    d.quadro("q-poo", "Conceitos de orientação a objetos no código do servidor",
             ["Conceito", "Onde", "Exemplo"],
             [["Classe e instância", "app/models, app/services", "Demanda, Evolucao, Encaminhamento; "
               "DemandaService, AssistidoService"],
              ["Método", "app/models/demanda.py", "mudar_estado(novo, autor), anotar(texto, autor)"],
              ["Encapsulamento", "app/models/usuario.py, demanda.py", "_senha_hash com definir_senha e "
               "senha_confere; validação do atributo estado"],
              ["Herança", "app/models/usuario.py, imutavel.py; app/schemas", "Direcao(Usuario); "
               "SomenteInsercao(SemExclusao); FiltroAuditoriaSchema(FiltroPeriodo, Paginacao)"],
              ["Polimorfismo", "app/models/usuario.py; app/routes", "pode_ver_evolucao e permissões da "
               "direção, consultadas por exige_permissao"],
              ["Classe abstrata", "app/models/usuario.py", "Usuario e Profissional não geram linha própria"],
              ["Enumeração", "app/models/demanda.py, reuniao.py", "EstadoDemanda, Prioridade, Setor"]],
             "elaborado pelos autores a partir de backend/app (2026).", larguras=[3.2, 5.0, 7.8], tamanho=9)
    d.figura("f-classes", "Diagrama de classes: usuários e registros sem exclusão",
             fig("diagrama-classes.png"), "elaborado pelos autores a partir de backend/app/models (2026).")
    d.h3("3.4.3 Estado da implementação")
    d.p(f"Os quinze cartões de back-end planejados para os ciclos 4 e 5 (cartões 14 a 28 do quadro, dois "
        f"deles opcionais) foram implementados no pull request 12, sobre a estrutura integrada pelo pull "
        f"request 5. Na branch development, a API responde a 39 rotas, agrupadas em nove recursos, todas descritas no contrato "
        f"(docs/contrato-api.md) e cobertas por specs escritas antes do código (Quadro {R('q-specs')}).")
    d.quadro("q-specs", "Especificações de comportamento e recursos da API",
             ["Spec", "Recurso", "Principais operações", "Permissão", "Situação"],
             [["01 Acesso e papéis", "/api/auth, /api/usuarios", "login com token de 30 min e limite de "
               "tentativas; logout que revoga o token; cadastro, edição e desativação de usuários",
               "usuários: direção", "implementada"],
              ["02 Demanda e estados", "/api/demandas", "registrar; filtrar e buscar; painel; minhas demandas; "
               "mudar estado; anotar; trocar responsável; histórico", "todo perfil ativo",
               "implementada; período em aberto (A6)"],
              ["03 Pessoa assistida", "/api/assistidos", "cadastrar e editar o nome de tratamento; listar; "
               "ficha completa", "todo perfil ativo", "implementada; campos em aberto (A3)"],
              ["04 Reunião", "/api/reunioes", "registrar; listar por data; ficha com demandas; alterar",
               "todo perfil ativo", "implementada"],
              ["05 Auditoria", "/api/auditoria", "registro automático das operações com dado de assistido; "
               "consulta paginada com filtros", "consulta: direção", "implementada; retenção em aberto (A7)"],
              ["06 Evolução", "/api/assistidos/<id>/evolucoes, /api/evolucoes/<id>", "lançar; listar com "
               "filtros; consultar versões; retificar sem apagar", "pode_ver_evolucao",
               "implementada; autoria da retificação em aberto (A9)"],
              ["07 Encaminhamento", "/api/encaminhamentos", "registrar a partir de assistido ou demanda; "
               "pendentes; desfecho único", "todo perfil ativo", "implementada; destino em texto (A1)"],
              ["08 Relatório", "/api/relatorios", "demandas do período; acompanhamento do assistido; emissão "
               "auditada", "direção", "implementada; formato oficial depende da QA04"],
              ["09 Aviso de prazo", "campo avisos do login", "demandas vencidas ou perto do prazo, sem "
               "descrição", "usuário autenticado", "implementada; antecedência em aberto (A10)"]],
             "elaborado pelos autores a partir de docs/specs e docs/contrato-api.md (2026).",
             larguras=[2.6, 3.3, 5.2, 2.3, 2.6], tamanho=8.5)
    d.p(f"O ciclo de vida da demanda, núcleo do sistema, é controlado pela enumeração EstadoDemanda e por "
        f"uma tabela de transições permitidas (Figura {R('f-estados')}). Concluída e cancelada são estados "
        f"finais; a tentativa de transição não permitida é recusada com resposta 400, sem gravar histórico. "
        f"A interface oferece ao usuário apenas as transições válidas para o estado atual.")
    d.figura("f-estados", "Estados da demanda e transições aceitas pelo servidor",
             fig("diagrama-estados.png"),
             "elaborado pelos autores a partir de backend/app/models/demanda.py e da spec 02 (2026).",
             largura_cm=15.0)
    d.h3("3.4.4 Integração com o banco de dados")
    d.p("A integração usa o mapeamento objeto-relacional do SQLAlchemy, pela extensão Flask-SQLAlchemy, "
        "com o driver psycopg 3 para o PostgreSQL. O esquema não é criado pelo código da aplicação, e sim "
        "pelas migrações do Alembic, o que permite evoluir o banco sem recriá-lo. Há três ambientes: "
        "desenvolvimento, com PostgreSQL local em Docker Compose e carga de dados fictícios; testes, com "
        "SQLite em memória, de modo que a suíte não depende de serviço externo; e produção, com o "
        "PostgreSQL do Neon. A configuração de cada ambiente vem de variáveis de ambiente (backend/config.py).")
    d.p("Para que uma leitura auditada não gere uma consulta ao banco por linha retornada, as consultas "
        "carregam os relacionamentos de uma vez, e um teste verifica que o número de consultas não cresce "
        "com o número de linhas. As escritas que podem concorrer, como a mudança de estado e o registro "
        "de desfecho, bloqueiam a linha durante a operação (SELECT ... FOR UPDATE), e a retificação "
        "simultânea da mesma evolução é recusada com resposta 400.")
    d.h3("3.4.5 Publicação e primeiro acesso")
    d.p("O banco de produção foi publicado vazio, sem nenhum usuário, e a carga de demonstração recusa "
        "execução em produção. Assim, até 23/11/2026 não era possível entrar no sistema publicado. Para "
        "criar o primeiro acesso sem abrir uma rota pública de cadastro, o pull request 19, ainda em aberto, "
        "acrescenta o comando administrativo flask criar-primeira-direcao, que cria somente a primeira conta "
        "da direção e recusa a execução se já houver qualquer usuário, e um fluxo do GitHub Actions que o "
        "executa no banco de produção com a senha guardada como segredo. [[a preencher pela equipe: data em "
        "que a primeira conta da direção foi criada em produção, sem registrar e-mail nem senha neste "
        "relatório]]. As demais contas são criadas pela direção, na tela Usuários.")

    # ------------------------------------------------------------------ 3.5
    d.h2("3.5 Desenvolvimento Web Front End (BRADWFR)")
    d.h3("3.5.1 Decisões estruturais")
    d.p("A interface é desenvolvida com React, sob organização em que as páginas correspondem às rotas da "
        "aplicação e realizam a obtenção dos dados, ao passo que os componentes recebem os dados por "
        "propriedades e permanecem reutilizáveis. As páginas ficam em src/pages, agrupadas por módulo, e os "
        "componentes em src/components. A navegação usa o React Router, com rotas filhas de um layout base "
        "(RootLayout), e as rotas exclusivas da direção ficam sob um componente de proteção "
        "(SomenteDirecao).")
    d.p("Todo o acesso à API é centralizado no módulo src/api/cliente.js, construído com Axios: ele define "
        "o endereço base, envia o token guardado em sessionStorage, traduz as respostas de erro em mensagem "
        "para o usuário e reage à sessão encerrada. Em produção, o endereço base é vazio, porque cliente e "
        "API estão na mesma origem; em desenvolvimento, vem da variável pública VITE_API_URL, que contém "
        "apenas a origem do servidor. O código segue os recursos vistos nas aulas — componentes de função, "
        "useState, useEffect com função assíncrona, eventos com preventDefault, rotas filhas e Axios —, e os "
        "dois recursos que vão além delas, o interceptador de respostas do Axios e o useRef para abrir o "
        "diálogo nativo, ficam cada um em um único lugar, conforme registrado no README.")
    d.p("O pull request 21, aberto em 23/11/2026 e ainda sem revisão, propõe três mudanças nessa "
        "estrutura: o cliente de API passa a ser a classe ClienteApi, com o objeto Axios em campo privado e "
        "métodos de sessão, rascunho e requisição; as regras de exibição da demanda passam à classe Demanda "
        "(src/modelos/Demanda.js), cujos objetos são criados a partir do JSON da API e consultados pelos "
        "componentes; e o layout base encerra a sessão após 15 minutos sem interação, preservando o "
        "rascunho. As descrições desta seção referem-se à branch development em 23/11/2026; se o pull "
        "request 21 for integrado, [[a equipe atualiza esta seção e as linhas de RF02 e RNF05 do Quadro "
        "de requisitos]].")
    d.h3("3.5.2 Contrato de interface")
    d.p(f"O contrato da API (docs/contrato-api.md), proposto em 13/10/2026, passou a vigorar e foi "
        f"atualizado em 16/11/2026 com o estado real das rotas; ele constitui o Apêndice B. A regra de que o "
        f"contrato prevalece sobre o código foi mantida, e o cliente foi construído sobre ele. O "
        f"Quadro {R('q-contrato')} resume as convenções comuns a todas as rotas.")
    d.quadro("q-contrato", "Convenções do contrato da API",
             ["Item", "Valor"],
             [["Prefixo", "/api"],
              ["Corpo", "JSON, com campos em snake_case"],
              ["Datas", "ISO 8601, com fuso horário"],
              ["Autenticação", "Cabeçalho Authorization: Bearer <token>; token JWT com validade de 30 minutos, "
               "guardado pelo cliente em sessionStorage"],
              ["Formato de erro", "{\"erro\": \"mensagem em português\"}"],
              ["Códigos HTTP", "400 regra de negócio violada; 401 token ausente, inválido ou expirado; 403 "
               "perfil sem acesso; 404 recurso inexistente; 405 método inexistente, inclusive DELETE; 422 "
               "corpo ausente ou campo inválido; 429 excesso de tentativas de login"],
              ["Login", "Mensagem única \"E-mail ou senha inválidos.\", sem revelar se o e-mail existe"]],
             "elaborado pelos autores a partir de docs/contrato-api.md (2026).", larguras=[3.4, 12.6])
    d.h3("3.5.3 Telas implementadas")
    d.p(f"As telas de prioridade 1 foram implementadas no pull request 15 e as de prioridade 2 e 3 no pull "
        f"request 16, ambos integrados em 18/11/2026, com os textos e rótulos da especificação de telas. O "
        f"cliente tem 25 rotas, agrupadas nas telas do Quadro {R('q-telas')}. As Figuras {R('f-sis-entrar')} "
        f"a {R('f-sis-falha')} devem mostrar o sistema publicado.")
    d.quadro("q-telas", "Telas do cliente, rotas, perfis e recursos consumidos",
             ["Tela", "Rota", "Perfil", "Recurso da API", "PR"],
             [["Entrar", "/entrar", "todos", "/api/auth/login", "15"],
              ["Painel", "/", "todos", "/api/demandas/painel", "15"],
              ["Minhas demandas", "/minhas", "todos", "/api/demandas/minhas", "15"],
              ["Demandas: lista, busca e filtros", "/demandas", "todos", "/api/demandas", "15"],
              ["Registrar demanda", "/demandas/nova", "todos", "/api/demandas", "15"],
              ["Demanda: detalhe, estado, anotação, responsável", "/demandas/:id", "todos",
               "/api/demandas/<id>", "15"],
              ["Reuniões: lista, registro, ficha, edição", "/reunioes", "todos", "/api/reunioes", "16"],
              ["Assistidos: lista, cadastro, ficha, edição", "/assistidos", "todos", "/api/assistidos", "16"],
              ["Evoluções: lançar, versões, retificar", "/assistidos/:id/evolucoes/nova, /evolucoes/:id",
               "todos", "/api/.../evolucoes", "16"],
              ["Encaminhamentos: pendentes, registro, desfecho", "/encaminhamentos", "todos",
               "/api/encaminhamentos", "16"],
              ["Usuários", "/usuarios", "direção", "/api/usuarios", "16"],
              ["Relatórios", "/relatorios", "direção", "/api/relatorios", "16"],
              ["Auditoria", "/auditoria", "direção", "/api/auditoria", "16"]],
             "elaborado pelos autores a partir de frontend/src/App.jsx (2026).",
             larguras=[5.0, 4.2, 1.6, 4.2, 1.0], tamanho=9)
    d.h3("3.5.4 Componentes reutilizáveis")
    d.p(f"Os componentes compartilhados recebem os dados por propriedades e não fazem requisições, o que "
        f"permite reutilizá-los entre telas (Quadro {R('q-componentes')}).")
    d.quadro("q-componentes", "Componentes reutilizáveis do cliente",
             ["Componente", "Função", "Arquivos que o usam"],
             [["RootLayout", "Menu lateral, nome e perfil do usuário, botão Sair; menu recolhível no celular",
               "todas as telas internas"],
              ["SomenteDirecao", "Protege as rotas exclusivas da direção", "rotas da direção"],
              ["ErroConsulta", "Mensagem de erro com o botão Tentar de novo (role=\"alert\")", "18"],
              ["Carregando", "Texto de carregamento anunciado ao leitor de tela (role=\"status\")", "15"],
              ["CampoDemanda", "Rótulo, campo e mensagem de erro ligados por atributos de acessibilidade", "9"],
              ["AvisoSucesso", "Aviso de operação concluída, que permanece até a próxima ação", "6"],
              ["Confirmacao", "Diálogo nativo de confirmação, com foco preso e saída por Esc", "4"],
              ["ListaDemandas", "Lista de demandas com estado, prazo e marcação de vencida", "4"],
              ["CabecalhoDemandas", "Título e ação principal das telas de demandas", "3"],
              ["CartaoDemanda", "Cartão de demanda do painel", "2"],
              ["HistoricoDemanda", "Histórico numerado da demanda", "1"]],
             "elaborado pelos autores a partir de frontend/src/components (2026).",
             larguras=[3.6, 9.4, 3.0], tamanho=9)
    d.h3("3.5.5 Validações de formulário e requisições assíncronas")
    d.p("Os formulários validam os campos antes do envio. No registro de demanda, a função validarDemanda "
        "exige descrição, prioridade, responsável, prazo e reunião de origem e limita a categoria a 80 "
        "caracteres; havendo erro, o foco vai para o primeiro campo inválido e a mensagem fica ligada ao "
        "campo. Só depois da validação abre-se o diálogo de confirmação, o que atende ao limite de um "
        "formulário e uma confirmação (RNF12). O servidor valida novamente cada campo, e sua mensagem, já em "
        "português, é exibida como veio.")
    d.p("As requisições são assíncronas, com async e await dentro de useEffect, e cada tela trata os "
        "estados de carregamento, lista vazia e erro, este com o botão Tentar de novo. Para a conexão "
        "instável da instituição (RNF16), cada formulário guarda um rascunho em sessionStorage a cada campo "
        "alterado. Se o envio falha por falta de conexão, a tela informa: \"Não foi possível falar com o "
        "servidor. Seus dados continuam no formulário. Tente de novo.\". Se a sessão expira, o interceptador "
        "guarda a página atual, leva à tela Entrar e, quando a mesma conta entra de novo, devolve a pessoa à "
        "página com o rascunho; rascunhos de outra conta são descartados, e Sair apaga a sessão e os "
        "rascunhos da aba. Esse comportamento é coberto por um dos testes do cliente.")
    d.h3("3.5.6 Responsividade, acessibilidade e revisão visual")
    d.p("No computador, o menu fica fixo à esquerda; em telas de até cerca de 768 px, ele se recolhe atrás "
        "do botão Menu, fecha com Esc ou com a escolha de um item e devolve o foco ao botão, e as colunas do "
        "painel passam a seções empilhadas. A acessibilidade segue a especificação de telas: item de menu "
        "atual marcado também para leitores de tela, campos com rótulo e erro associado, diálogos nativos "
        "que prendem o foco, avisos anunciados ao leitor de tela, alvos de clique de pelo menos 44 px e "
        "contraste mínimo de 4,5:1.")
    d.p("O pull request 18, integrado em 23/11/2026, revisou o visual da interface para deixar a informação "
        "escrita em vez de codificada em ícones e cores: saíram os ícones do menu, o avatar, os selos "
        "coloridos e a biblioteca de ícones; o estado da demanda passou a ser escrito por extenso, o prazo "
        "vencido passou a ser indicado por \"(vencida)\" em vermelho, com a palavra sempre presente para que "
        "a cor não seja a única pista, e o histórico passou a ser apresentado como lista numerada. [[a preencher pela equipe: se "
        "a revisão respondeu a alguma observação recebida na EXPOEX]].")
    fonte_sis = "[[captura de tela do sistema publicado (sistema-demandas-crie.vercel.app), com dados fictícios, " \
                "elaborada pelos autores (data da captura)]]."
    d.figura_pendente("f-sis-entrar", "Sistema publicado: tela Entrar",
                      "tela Entrar do sistema publicado, sem campos preenchidos, largura 1280 px",
                      "entregas/extensao/prints/01-entrar.png", fonte_sis)
    d.figura_pendente("f-sis-painel", "Sistema publicado: painel da direção com aviso de prazo",
                      "Painel logado como direção, com o aviso de prazo aberto, os totais e as três colunas "
                      "por estado, com pelo menos uma demanda vencida; largura 1280 px",
                      "entregas/extensao/prints/02-painel-direcao.png", fonte_sis)
    d.figura_pendente("f-sis-painel-celular", "Sistema publicado: painel em tela de celular",
                      "Painel em largura 360 px, com o menu recolhido e o botão Menu visível",
                      "entregas/extensao/prints/03-painel-celular.png", fonte_sis)
    d.figura_pendente("f-sis-validacao", "Sistema publicado: validação do formulário de demanda",
                      "Registrar demanda após clicar em Registrar com campos obrigatórios vazios, mostrando as "
                      "mensagens junto aos campos; largura 1280 px",
                      "entregas/extensao/prints/04-registrar-demanda-validacao.png", fonte_sis)
    d.figura_pendente("f-sis-confirmacao", "Sistema publicado: confirmação do registro da demanda",
                      "diálogo de confirmação aberto sobre o formulário preenchido com dados fictícios; "
                      "largura 1280 px", "entregas/extensao/prints/05-confirmacao-demanda.png", fonte_sis)
    d.figura_pendente("f-sis-detalhe", "Sistema publicado: detalhe da demanda com histórico",
                      "detalhe de uma demanda com pelo menos uma mudança de estado e uma anotação no histórico "
                      "numerado; largura 1280 px", "entregas/extensao/prints/06-detalhe-demanda.png", fonte_sis)
    d.figura_pendente("f-sis-falha", "Sistema publicado: falha de conexão com dados preservados",
                      "formulário preenchido após falha de envio por falta de conexão (rede desligada nas "
                      "ferramentas do navegador), com a mensagem de que os dados continuam no formulário; "
                      "largura 1280 px", "entregas/extensao/prints/07-falha-conexao-rascunho.png", fonte_sis)
