"""Seções 4 a 7, referências, anexos e apêndices."""
import os

WT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # raiz do repositório
PEND = "[[a preencher]]"


def secao4(d, R):
    d.h1("4 GESTÃO DO PROJETO")
    d.h2("4.1 Metodologia e quadro Kanban")
    d.p("Adotou-se o método Kanban para a gestão das atividades, conforme sugerido na especificação da "
        "unidade curricular e no material de apoio do Serviço Brasileiro de Apoio às Micro e Pequenas "
        "Empresas ([2023]). O quadro, denominado Equipe Cortex, "
        "encontra-se hospedado na ferramenta Trello, no endereço trello.com/b/XgMRYAKo/equipe-cortex, e o "
        "docente responsável pela unidade curricular foi incluído como membro do quadro. Cada cartão contém "
        "lista de verificação com os critérios de conclusão da tarefa, anexos com os artefatos produzidos e "
        "comentários da equipe, e o progresso de cada tarefa é medido pela proporção de itens concluídos.")
    d.p("A especificação da unidade curricular orienta que o quadro seja categorizado por disciplina, com as "
        "cores azul para BRAINHC, laranja para BRABCD1, roxo para BRAPROB, verde para BRADWFR e amarelo para "
        "BRAENSO, que o fluxo inclua as colunas Backlog, A Fazer, Em Andamento, Em Revisão e Concluído, e que "
        "o quadro seja atualizado antes de cada apresentação (INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E "
        "TECNOLOGIA DE SÃO PAULO, 2026). Na versão 3, o quadro usava as colunas Backlog, A Fazer, Fazendo, "
        "Esperando Teste, Testando e Concluído, e etiquetas por frente (Banco de Dados, UI/UX, Backend, "
        "Frontend e Comunidade Externa). [[a preencher pela equipe: colunas, etiquetas e membros do quadro "
        "em 26/11/2026, e se seguem o padrão da especificação]].")
    fonte_k = "[[captura de tela do quadro no Trello, elaborada pelos autores (26/11/2026)]]."
    d.figura_pendente("f-kanban-1", "Quadro Kanban ao final do 5º ciclo (vista 1)",
                      "quadro do Trello atualizado em 26/11/2026, colunas Backlog, A Fazer e Em Andamento, com "
                      "as etiquetas coloridas por disciplina visíveis; largura 1280 px ou mais",
                      "entregas/extensao/prints/17-kanban-vista-1.png", fonte_k)
    d.figura_pendente("f-kanban-2", "Quadro Kanban ao final do 5º ciclo (vista 2)",
                      "mesmo quadro, colunas Em Revisão e Concluído; largura 1280 px ou mais",
                      "entregas/extensao/prints/18-kanban-vista-2.png", fonte_k)
    d.figura_pendente("f-kanban-3", "Etiquetas por disciplina e membros do quadro",
                      "menu de etiquetas com as cinco cores por disciplina e lista de membros com o professor "
                      "de BRAEXT2; largura 1280 px", "entregas/extensao/prints/19-kanban-etiquetas-membros.png",
                      fonte_k)
    d.h2("4.2 Divisão de responsabilidades")
    d.quadro("q-equipe", "Atribuições da equipe",
             ["Integrante", "Atribuição", "Disciplina"],
             [["Vinícius Marrocos", "Gerente de Projeto e Analista de Requisitos", "Engenharia de Software "
               "(BRAENSO)"],
              ["Henry Claro", "Analista de Banco de Dados", "Banco de Dados 1 (BRABCD1)"],
              ["Inácio Fontes", "Analista de Interface e Experiência do Usuário", "Interface Humano-Computador "
               "(BRAINHC)"],
              ["Miguel Vaz de Souza", "Desenvolvedor Back-end", "Programação Orientada a Objetos (BRAPROB)"],
              ["Gabriel Borba", "Desenvolvedor Front-end", "Desenvolvimento Web Front End (BRADWFR)"]],
             "elaborado pelos autores (2026).", larguras=[3.8, 6.4, 5.8])
    d.p("Cada integrante responde pela sua frente, o que compreende a produção dos artefatos "
        "correspondentes, a redação da respectiva seção deste relatório e a apresentação dos resultados. "
        "Conforme previsto, as atividades de implementação concentraram-se na segunda metade do semestre. "
        "[[a preencher pela equipe: participação de cada integrante nos ciclos 4 e 5, inclusive a "
        "condução dos testes de usabilidade, o banner e a atualização do quadro]].")
    d.h2("4.3 Situação do quadro ao final do 5º ciclo")
    d.p(f"O Quadro {R('q-board')} deve consolidar as tarefas do quadro em 26/11/2026, como foi feito na "
        f"versão 3. [[a preencher pela equipe a partir do Trello: total de tarefas por coluna e itens de "
        f"verificação atendidos, no formato \"__ de __ itens\"]].")
    d.quadro("q-board", "Tarefas do quadro Kanban ao final do 5º ciclo (26/11/2026)",
             ["Tarefa", "Disciplina", "Coluna", "Checklist"],
             [[PEND, PEND, PEND, PEND], [PEND, PEND, PEND, PEND], [PEND, PEND, PEND, PEND]],
             "[[elaborado pelos autores a partir do quadro no Trello (26/11/2026)]].",
             larguras=[8.4, 2.6, 2.8, 2.2])
    d.h2("4.4 Evolução desde a versão 3")
    d.p("Entre 22/10 e 23/11/2026, o trabalho registrado no repositório concentrou-se em quatro momentos: "
        "em 04/11, a criação do modelo de domínio e da migração inicial do banco; em 05/11, a integração do "
        "pull request 5, com a estrutura do servidor e as primeiras specs; em 16 e 17/11, o projeto de BD1, "
        "a publicação na Vercel e a API completa; e em 18/11, os artefatos de IHC e a interface em React, "
        "seguidos, em 23/11, da revisão visual e da integração contínua. O Quadro "
        f"{R('q-plano')} compara, item por item, o planejamento registrado na versão 3 (Quadro 13 daquela "
        "versão) com a situação em 23/11/2026.")
    C, P, N = "Concluído", "Parcial", "Pendente"
    linhas = [
        ["BRAENSO", "Enviar à instituição o bloco de perguntas sobre as questões em aberto",
         "[[a preencher pela equipe]]", "Decisões A2, A3, A6, A7, A9 e A10 ainda abertas no repositório"],
        ["BRAENSO", "Atualizar o documento de requisitos com as respostas e as decisões das specs", P,
         "Decisões registradas nas specs e no contrato; docs/requisitos.md não revisado"],
        ["BRAENSO", "Revisar e integrar o PR 5; condicionar a conclusão dos cartões de código à revisão", P,
         "PR 5 integrado em 05/11; revisões não registradas no GitHub; CI no PR 19"],
        ["BRAENSO", "Conduzir a validação junto à instituição e verificar os critérios de aceitação", N,
         "Seção 6"],
        ["BRABCD1", "Concluir o modelo relacional e decidir o destino do encaminhamento", P,
         "Modelo implementado (migração de 04/11); destino segue como texto (A1)"],
        ["BRABCD1", "Modelar auditoria e imutabilidade do histórico", C, "Tabelas e gatilhos (seção 3.3.4)"],
        ["BRABCD1", "Aplicar restrições de proteção de dados sensíveis ao modelo", C,
         "Hash de senha, minimização, sem exclusão"],
        ["BRABCD1", "Elaborar scripts de criação das tabelas e carga com dados fictícios", C,
         "Scripts 01 e 02 (PR 8); seed.py do sistema"],
        ["BRABCD1", "Elaborar consultas de seleção, inserção, atualização e remoção", C,
         "Scripts 03 (17 consultas) e 04"],
        ["BRAINHC", "Concluir o protótipo no Figma e compartilhar o link", "[[a preencher pela equipe]]",
         "Protótipo clicável em HTML no repositório (PR 14)"],
        ["BRAINHC", "Escrever cenários de uso a partir das personas", C, "C1 a C6 (PR 14)"],
        ["BRAINHC", "Mapear a arquitetura da informação e o fluxo de navegação", C,
         "Arquitetura da informação e fluxos F1 a F9 (PR 14); card sorting simulado"],
        ["BRAINHC", "Planejar e executar os testes de usabilidade e redigir o relatório", P,
         "Plano e modelos prontos; sessões não realizadas"],
        ["BRAPROB", "Validar o contrato da API com a equipe", C,
         "Contrato em vigor desde 16/11 e usado pelo cliente"],
        ["BRAPROB", "Implementar as specs 01 a 04 com os testes correspondentes", C, "PR 12"],
        ["BRAPROB", "Especificar e implementar evoluções, encaminhamentos e relatórios", C,
         "Specs 06 a 08 (PR 12)"],
        ["BRAPROB", "Implementar a consulta ao histórico da pessoa assistida e a auditoria", C,
         "Ficha do assistido e spec 05 (PR 12)"],
        ["BRADWFR", "Concluir o apoio à prototipação com foco em componentes",
         "[[a preencher pela equipe]]", "—"],
        ["BRADWFR", "Criar o cliente de API centralizado", C, "src/api/cliente.js (PR 15)"],
        ["BRADWFR", "Tela de login e controle de sessão", C,
         "PR 15; encerramento por inatividade no PR 21 (aberto)"],
        ["BRADWFR", "Layout base, navegação e proteção de rotas por perfil", C, "PRs 15 e 16"],
        ["BRADWFR", "Implementar as telas, as validações e a integração com a API", C,
         "PRs 15, 16 e 18"]]
    d.quadro("q-plano", "Planejamento da versão 3 e situação em 23/11/2026",
             ["Disciplina", "Atividade planejada na versão 3", "Situação", "Evidência"], linhas,
             "elaborado pelos autores a partir do relatório v3 e do repositório (2026).",
             larguras=[2.2, 6.6, 2.4, 4.8], tamanho=8.5)
    nc = sum(1 for l in linhas if l[2] == C)
    np_ = sum(1 for l in linhas if l[2] == P)
    nn = sum(1 for l in linhas if l[2] == N)
    na = len(linhas) - nc - np_ - nn
    d.p(f"Dos {len(linhas)} itens planejados, {nc} foram concluídos, {np_} foram atendidos em parte, {nn} "
        f"permanece pendente e {na} dependem de informação da equipe. Os itens de código foram concluídos; "
        f"os atrasos concentram-se nas atividades que dependem de pessoas de fora da equipe — a instituição "
        f"e os participantes dos testes — e na revisão entre integrantes.")
    d.h2("4.5 Decisões em aberto e riscos")
    d.p(f"As decisões que dependem da instituição ou da equipe foram mantidas como abertas, com uma solução "
        f"provisória explícita, de modo que o desenvolvimento prosseguisse sem tomar como definitivo o que "
        f"ainda não foi decidido (Quadro {R('q-decisoes')}).")
    d.quadro("q-decisoes", "Decisões em aberto e soluções provisórias",
             ["Nº", "Decisão", "Solução provisória", "Quem decide"],
             [["A1", "Destino do encaminhamento: serviço cadastrado, profissional interno ou texto livre",
               "Texto livre de até 200 caracteres", "Banco de Dados, com o back-end"],
              ["A2", "Lista de categorias de demanda", "Campo opcional de até 80 caracteres, sem catálogo",
               "Direção do CRIE"],
              ["A3", "Campos de identificação da pessoa assistida", "Apenas o nome de tratamento",
               "Direção do CRIE"],
              ["A4", "Perfil de coordenação de setor como classe própria", "Sem classe própria; o acesso aberto "
               "cobre o uso descrito", "Equipe, se a instituição distinguir o perfil"],
              ["A5", "Token em sessionStorage ou em cookie HttpOnly", "Token JWT de 30 minutos em "
               "sessionStorage", "Back-end e front-end"],
              ["A6", "Data considerada no período do filtro e do relatório de demandas", "Data de registro da "
               "demanda", "Direção do CRIE, com o back-end"],
              ["A7", "Prazo de retenção da auditoria", "Nenhum registro é removido", "Direção do CRIE"],
              ["A8", "Local de armazenamento da auditoria", "Tabela no mesmo PostgreSQL, somente inserção",
               "Equipe"],
              ["A9", "Quem pode retificar evolução", "Quem pode ver a evolução; autor e momento gravados",
               "Direção do CRIE"],
              ["A10", "Antecedência do aviso de prazo", "3 dias, configurável", "Direção do CRIE"]],
             "elaborado pelos autores a partir de docs/contrato-api.md (2026).",
             larguras=[1.2, 6.0, 5.4, 3.4], tamanho=9)
    d.p(f"O Quadro {R('q-riscos')} reúne os riscos e pendências que afetam a entrega final.")
    d.quadro("q-riscos", "Riscos e pendências na entrega final",
             ["Risco ou pendência", "Efeito", "Medida"],
             [["Pull requests 19, 20 e 21 abertos às vésperas da entrega", "Sistema publicado sem o "
               "primeiro acesso, sem a sessão por inatividade e sem a integração contínua", "Revisar e "
               "integrar antes de 26/11/2026 e levar a development para a main"],
              ["Banco de produção sem nenhum usuário", "Não é possível entrar no sistema publicado nem "
               "demonstrá-lo", "Integrar o PR 19 e executar a criação da primeira conta da direção antes de "
               "26/11/2026"],
              ["Testes de usabilidade não realizados", "Validação com o público-alvo e relatório de "
               "usabilidade sem dados", "Aplicar o plano com oito participantes e preencher a seção 6.3"],
              ["Quadro Kanban fora do padrão da especificação", "Critério de atualização do projeto",
               "Ajustar colunas, etiquetas por disciplina e membros, e atualizar antes da apresentação"],
              ["Migrações no banco publicado", "As rotas autenticadas dependem da tabela token_revogado",
               "[[confirmar pela equipe que as três migrações foram aplicadas no Neon]]"],
              ["Revisão não registrada e commits concentrados em uma conta", "Rastreabilidade da "
               "participação de cada integrante", "Registrar revisões nos pull requests e a contribuição "
               "de cada integrante (seção 4.2)"],
              ["Limite de tentativas de login guardado em memória", "Proteção mais fraca com várias "
               "instâncias na Vercel", "Armazenamento compartilhado do contador (trabalho futuro)"],
              ["Decisões da instituição em aberto", "Campos e categorias provisórios", "Bloco único de "
               "perguntas fechadas e numeradas"]],
             "elaborado pelos autores (2026).", larguras=[4.6, 5.0, 6.4], tamanho=9)
    d.h2("4.6 Alterações após a EXPOEX")
    d.p("**Feedback recebido na EXPOEX:** [[a preencher pela equipe]].")
    d.p("Depois da Mostra de Extensão, realizada em 18/11/2026, foram registradas no repositório as "
        "seguintes alterações:")
    d.alineas([
        "a) pull request 18, integrado em 23/11/2026: revisão visual da interface, com texto no lugar de "
        "ícones, selos e enfeites (seção 3.5.6);",
        "b) pull request 19, aberto em 23/11/2026: integração contínua dos testes e procedimento para criar "
        "a primeira conta da direção em produção (seções 3.1.5 e 3.4.5);",
        "c) pull request 20, aberto em 23/11/2026: pasta de entregas com as exigências oficiais de cada "
        "disciplina, listas de verificação e pacote de envio de BD1;",
        "d) pull request 21, aberto em 23/11/2026 e aguardando revisão: classes ClienteApi e Demanda no "
        "cliente, encerramento da sessão por inatividade, aviso de prazo aberto no topo do painel e "
        "documentação dos conceitos de POO (seção 3.5.1);",
        "e) esta versão do relatório, que incorpora a evolução do período e a estrutura da validação."])
    d.p("**Relação entre cada observação recebida e a alteração correspondente:** [[a preencher pela "
        "equipe; se uma observação não gerou alteração, registrar o motivo]].")


def secao5(d, R):
    d.h1("5 RESULTADOS DO SISTEMA DESENVOLVIDO")
    d.h2("5.1 Visão geral")
    d.p(f"O sistema está publicado no endereço https://sistema-demandas-crie.vercel.app, com o cliente "
        f"React e a API Flask no mesmo endereço e o banco PostgreSQL no Neon (Figura {R('f-arquitetura')}). "
        f"Em 23/11/2026, a interface carregou, a rota de saúde da API respondeu normalmente e as rotas de "
        f"dados recusaram acesso sem autenticação, como previsto. O acesso às telas internas depende da "
        f"criação da primeira conta da direção (seção 3.4.5).")
    d.p("O sistema atende três perfis. A direção usa todas as funções, inclusive o cadastro de usuários, os "
        "relatórios e a consulta à auditoria. O assistente social e a equipe pedagógica registram e "
        "acompanham demandas, reuniões, pessoas assistidas, evoluções e encaminhamentos; por decisão da "
        "instituição, veem todos os registros, e cada consulta a dado de pessoa assistida fica registrada "
        "na auditoria.")
    d.h2("5.2 Funcionalidades por módulo")
    d.p("**Acesso e sessão.** A pessoa entra com e-mail e senha; a mensagem de erro é sempre a mesma, para "
        "não revelar se o e-mail existe, e a sexta tentativa errada em 60 segundos é bloqueada "
        "temporariamente. A sessão dura 30 minutos, termina ao fechar a aba ou ao clicar em Sair, quando o "
        "token é revogado no servidor. Ao entrar, a pessoa recebe o aviso das demandas sob sua "
        "responsabilidade vencidas ou perto do prazo, sem descrição nem dado de saúde.")
    d.p(f"**Painel e minhas demandas.** O painel mostra, em uma única tela, o total em aberto, o total de "
        f"vencidas e as demandas em três colunas — Aberta, Em andamento e Aguardando terceiros —, da mais "
        f"antiga para a mais recente pelo prazo (Figura {R('f-sis-painel')}). Minhas demandas lista apenas as "
        f"do usuário autenticado.")
    d.p(f"**Demandas.** A lista permite buscar trecho da descrição e filtrar por estado, responsável, "
        f"categoria, período e pessoa assistida (Figura {R('f-sis-busca')}). O registro usa um formulário e "
        f"uma confirmação. No detalhe, é possível mudar o estado, apenas para as transições permitidas, "
        f"anotar e trocar o responsável, e cada ação entra no histórico com autor, data e hora.")
    d.p(f"**Reuniões.** Cada reunião registra data, setor e participantes; a ficha mostra as demandas "
        f"nascidas nela e o estado de cada uma, e dela se registra uma nova demanda já vinculada "
        f"(Figura {R('f-sis-reuniao')}).")
    d.p(f"**Pessoas assistidas e evoluções.** A pessoa assistida é cadastrada pelo nome de tratamento. Sua "
        f"ficha reúne demandas, evoluções e encaminhamentos em ordem cronológica, o que responde à "
        f"necessidade de consultar o que já foi feito quando uma demanda se repete "
        f"(Figura {R('f-sis-ficha')}). A evolução pode ser filtrada por período e área e retificada sem apagar "
        f"a versão anterior (Figura {R('f-sis-versoes')}).")
    d.p(f"**Encaminhamentos.** O encaminhamento é registrado a partir da demanda ou da ficha da pessoa "
        f"assistida; a lista abre nos pendentes, e o desfecho é registrado uma única vez, com confirmação "
        f"(Figura {R('f-sis-encaminhamentos')}).")
    d.p(f"**Funções da direção.** A direção cadastra, edita e desativa usuários, sem excluí-los "
        f"(Figura {R('f-sis-usuarios')}); emite o relatório de demandas do período e o de acompanhamento de "
        f"uma pessoa assistida, com identificação de quem emitiu e impressão pelo navegador "
        f"(Figura {R('f-sis-relatorio')}); e consulta a auditoria, com filtros e paginação "
        f"(Figura {R('f-sis-auditoria')}).")
    fonte_sis = "[[captura de tela do sistema publicado, com dados fictícios, elaborada pelos autores (data)]]."
    d.figura_pendente("f-sis-busca", "Sistema publicado: lista de demandas com busca e filtros",
                      "Demandas com o texto \"material adaptado\" na busca e um filtro de estado aplicado, "
                      "mostrando o resultado; largura 1280 px", "entregas/extensao/prints/08-demandas-busca.png",
                      fonte_sis)
    d.figura_pendente("f-sis-reuniao", "Sistema publicado: ficha da reunião",
                      "ficha de uma reunião do setor de saúde com participantes e demandas; largura 1280 px",
                      "entregas/extensao/prints/09-ficha-reuniao.png", fonte_sis)
    d.figura_pendente("f-sis-ficha", "Sistema publicado: ficha da pessoa assistida",
                      "ficha do Assistido Fictício A com demandas, evoluções e encaminhamentos; largura 1280 px",
                      "entregas/extensao/prints/10-ficha-assistido.png", fonte_sis)
    d.figura_pendente("f-sis-versoes", "Sistema publicado: versões de uma evolução retificada",
                      "tela de versões de uma evolução já retificada, mostrando a versão vigente e a anterior; "
                      "largura 1280 px", "entregas/extensao/prints/11-versoes-evolucao.png", fonte_sis)
    d.figura_pendente("f-sis-encaminhamentos", "Sistema publicado: encaminhamentos pendentes",
                      "Encaminhamentos aberta nos pendentes, com pelo menos dois itens; largura 1280 px",
                      "entregas/extensao/prints/12-encaminhamentos-pendentes.png", fonte_sis)
    d.figura_pendente("f-sis-usuarios", "Sistema publicado: gestão de usuários pela direção",
                      "Usuários logado como direção, com a lista de contas fictícias e uma desativada; "
                      "largura 1280 px", "entregas/extensao/prints/15-usuarios.png", fonte_sis)
    d.figura_pendente("f-sis-relatorio", "Sistema publicado: relatório de demandas do período",
                      "Relatórios logado como direção, com o relatório de demandas de um período emitido, "
                      "totais e \"Emitido por\"; largura 1280 px",
                      "entregas/extensao/prints/13-relatorio-periodo.png", fonte_sis)
    d.figura_pendente("f-sis-auditoria", "Sistema publicado: consulta à auditoria",
                      "Auditoria logado como direção, com filtros e a primeira página de registros; largura "
                      "1280 px", "entregas/extensao/prints/14-auditoria.png", fonte_sis)
    d.figura_pendente("f-sis-detalhe-celular", "Sistema publicado: detalhe da demanda em tela de celular",
                      "detalhe de uma demanda em largura 360 px, com as ações empilhadas",
                      "entregas/extensao/prints/16-detalhe-celular.png", fonte_sis)
    d.h2("5.3 Atendimento aos requisitos")
    d.p(f"O Quadro {R('q-rf')} relaciona os requisitos funcionais à implementação, com a numeração de "
        f"docs/requisitos.md, e o Quadro {R('q-rnf')} faz o mesmo para os não funcionais. \"Atendido\" "
        f"indica que a funcionalidade existe na API e na interface e é coberta por testes automatizados; a "
        f"validação com usuários é tratada na seção 6.")
    A, AP, NA = "Atendido", "Atendido em parte", "Não atendido"
    d.quadro("q-rf", "Requisitos funcionais e situação na versão final",
             ["Requisitos", "Situação", "Evidência ou observação"],
             [["RF01 autenticação", A, "Login por e-mail e senha"],
              ["RF02 encerramento da sessão", AP, "Sair revoga o token; a sessão expira 30 minutos após o "
               "login e ao fechar a aba; o encerramento por inatividade está no PR 21, ainda aberto"],
              ["RF03 restrição por perfil", A, "Funções da direção com resposta 403 para os demais perfis e "
               "fora do menu deles"],
              ["RF04 gestão de usuários pela direção", A, "Cadastrar, editar e desativar"],
              ["RF05 acesso às evoluções", A, "Acesso aberto por decisão da instituição; regra restritiva "
               "implementada e desligada; consultas auditadas"],
              ["RF06 a RF09 reuniões", A, "Registro, lista por data, ficha com demandas e edição"],
              ["RF10 a RF17 demandas", A, "Registro, estados, transições, histórico automático, anotações, "
               "troca de responsável; categoria sem catálogo (A2)"],
              ["RF18 cadastro de assistidos", AP, "Apenas o nome de tratamento, até a instituição definir os "
               "campos (A3)"],
              ["RF19 e RF20 consulta, edição e ficha do assistido", A, "Ficha com demandas, evoluções e "
               "encaminhamentos"],
              ["RF21 a RF26 evoluções", A, "Lançamento, autoria automática, ordem cronológica, retificação "
               "com versões, filtros, sem exclusão"],
              ["RF27 a RF29 encaminhamentos", A, "Registro, desfecho único e pendentes; destino em texto (A1)"],
              ["RF30 a RF34 consulta e acompanhamento", A, "Painel, filtros, busca, marcação de vencida e "
               "minhas demandas"],
              ["RF35, RF36 e RF38 relatórios", A, "Demandas do período e acompanhamento do assistido; "
               "emissão auditada"],
              ["RF37 exportação para impressão", AP, "Impressão pelo navegador; formato oficial depende da "
               "QA04"],
              ["RF39 indicadores do período", A, "Totais por estado e vencidas no relatório do período"],
              ["RF40 aviso de prazo", A, "Aviso no login (spec 09)"],
              ["RF41 notificação por e-mail", NA, "Desejável; fora das specs desta versão"]],
             "elaborado pelos autores a partir de docs/requisitos.md, docs/specs e do código (2026).",
             larguras=[5.0, 2.8, 8.2], tamanho=9)
    d.quadro("q-rnf", "Requisitos não funcionais e situação na versão final",
             ["Requisitos", "Situação", "Evidência ou observação"],
             [["RNF01 acesso por necessidade", AP, "Acesso aberto por decisão da instituição, com auditoria "
               "como controle"],
              ["RNF02 senha criptografada", A, "Somente hash, por métodos encapsulados"],
              ["RNF03 auditoria", A, "Criação, alteração, consulta e emissão de relatório com dado de "
               "assistido"],
              ["RNF04 HTTPS", A, "Sistema servido por HTTPS na Vercel"],
              ["RNF05 encerramento de sessão inativa", AP, "Token de 30 minutos em sessionStorage; "
               "encerramento após 15 minutos sem interação proposto no PR 21"],
              ["RNF06 e RNF07 dados fictícios", A, "Carga fictícia, verificação de segredos, protótipo e "
               "telas com dados fictícios"],
              ["RNF08 minimização", A, "Apenas nome de tratamento"],
              ["RNF09 orientação à instituição como controladora", NA, "Documento ainda não produzido"],
              ["RNF10 cópia de segurança", NA, "Rotina não documentada nesta versão"],
              ["RNF11 a RNF15 usabilidade", AP, "Implementados conforme a especificação de telas; dependem "
               "dos testes de usabilidade para validação"],
              ["RNF16 preservação do formulário", A, "Rascunho por conta de usuário, coberto por teste"],
              ["RNF17 e RNF18 desempenho e uso simultâneo", "Não verificado", "Não houve medição"],
              ["RNF19 sem exclusão definitiva", A, "Sem DELETE na API; ORM e gatilhos"],
              ["RNF20 a RNF24 tecnologias e versionamento", A, "Flask orientado a objetos, React, PostgreSQL, "
               "contrato documentado, Git"],
              ["RNF25 hospedagem sem custo com HTTPS", AP, "Publicado na Vercel com banco no Neon; [[a equipe "
               "confirma o plano gratuito e a transferência à instituição]]"],
              ["RNF26 documentação de instalação e manual de uso", AP, "README com instalação; manual de uso "
               "para a instituição não produzido"]],
             "elaborado pelos autores a partir de docs/requisitos.md e do código (2026).",
             larguras=[5.0, 2.8, 8.2], tamanho=9)
    d.h2("5.4 Aplicação das disciplinas na solução final")
    d.quadro("q-disciplinas", "Contribuição de cada disciplina para o sistema",
             ["Disciplina", "Artefatos", "Onde aparece no sistema"],
             [["BRAENSO", "Requisitos, specs, contrato da API, controle de versão, testes e integração "
               "contínua", "Comportamento de cada rota e tela; rastreabilidade da seção 5.3"],
              ["BRAINHC", "Personas, cenários, arquitetura da informação, fluxos, especificação de telas, "
               "protótipo e plano de testes", "Menu, rótulos, uma ação principal por tela, estados e "
               "mensagens, tarefas de teste"],
              ["BRABCD1", "Minimundo, DER, modelo relacional, scripts e consultas", "Tabelas, enumerações, "
               "restrições e gatilhos do PostgreSQL"],
              ["BRAPROB", "Classes do domínio, serviços, permissões polimórficas e API Flask", "Regras de "
               "estado, histórico, auditoria e permissões"],
              ["BRADWFR", "Cliente React, cliente de API, componentes e validações", "Todas as telas "
               "publicadas"]],
             "elaborado pelos autores (2026).", larguras=[2.4, 7.0, 6.6], tamanho=9)


def secao6(d, R):
    d.h1("6 VALIDAÇÃO")
    d.p("Esta seção demonstra em que medida o sistema atende aos objetivos e às necessidades da "
        "instituição parceira. Ela reúne a verificação automatizada, a verificação dos critérios de "
        "aceitação e a avaliação de usabilidade com o público-alvo.")
    d.h2("6.1 Verificação automatizada")
    d.p(f"A verificação automatizada, descrita na seção 3.1.5 e resumida na Tabela {R('t-testes')}, "
        f"comprova que as regras especificadas estão implementadas: em 23/11/2026, 587 testes do servidor "
        f"foram aprovados na execução do GitHub Actions sobre o pull request 19 (os 570 da branch development e 17 do novo comando); "
        f"no cliente, os quatro testes, o lint e o build foram aprovados. Esses testes verificam o "
        f"comportamento previsto nas specs, mas não substituem a validação com quem vai usar o sistema.")
    d.h2("6.2 Critérios de aceitação")
    d.p(f"Os critérios de aceitação do documento de requisitos estabelecem quando o sistema será "
        f"considerado adequado às necessidades da instituição. O Quadro {R('q-aceitacao')} indica, para cada "
        f"um, como o sistema o atende e como será verificado.")
    d.quadro("q-aceitacao", "Critérios de aceitação e forma de verificação",
             ["Critério", "Como o sistema atende", "Verificação", "Resultado"],
             [["1. Registrar demanda sem auxílio", "Formulário único com confirmação", "T3 concluída sem "
               "ajuda", "[[a preencher após as sessões]]"],
              ["2. Localizar demanda e histórico em menos de um minuto", "Busca na descrição e histórico no "
               "detalhe", "T2 em menos de 60 s", "[[a preencher após as sessões]]"],
              ["3. Identificar, em tela única, as demandas vencidas", "Painel com total de vencidas e marcação "
               "\"(vencida)\"", "T1", "[[a preencher após as sessões]]"],
              ["4. Registrar evolução e consultá-la na ficha", "Lançar evolução a partir da ficha", "T7",
               "[[a preencher após as sessões]]"],
              ["5. Emitir os dois relatórios", "Tela Relatórios da direção", "Demonstração à direção do CRIE",
               "[[a preencher pela equipe]]"],
              ["6. Profissional não autorizado sem acesso às evoluções", "Regra restritiva implementada e "
               "desligada por decisão da instituição", "Testes automatizados com a regra ligada",
               "Verificado nos testes; não se aplica à configuração adotada pela instituição"],
              ["7. Interface avaliada como compreensível", "Especificação de telas e rótulos da instituição",
               "Questionário Q1 a Q8", "[[a preencher após as sessões]]"]],
             "elaborado pelos autores a partir de docs/requisitos.md, seção 8 (2026).",
             larguras=[4.2, 4.6, 3.6, 3.6], tamanho=9)
    d.h2("6.3 Avaliação de usabilidade")
    d.p("A avaliação segue o plano de testes da frente de Interface, fundamentado no ciclo de design "
        "centrado no usuário da ISO 9241-210 (INTERNATIONAL ORGANIZATION FOR STANDARDIZATION, 2019), e mede "
        "as dimensões pedidas pela especificação: desempenho (tempo e número de passos), precisão (erros e "
        "conclusão) e resposta emocional (satisfação e confiança). As sessões ainda não foram realizadas; "
        "por isso, as tabelas de resultados desta seção estão vazias, e nenhum valor foi estimado. "
        "**Resultados a preencher após as sessões.**")
    d.h3("6.3.1 Método")
    d.quadro("q-metodo", "Método da avaliação de usabilidade",
             ["Item", "Decisão"],
             [["Formato", "Presencial no CRIE, no computador e na internet de uso real; alternativa remota com "
               "compartilhamento de tela"],
              ["Técnica", "Teste com tarefas e pensar em voz alta"],
              ["Moderação", "Um moderador, que lê o roteiro e não ajuda, e um anotador, que registra tempo, "
               "passos, erros e falas"],
              ["Sessões", "Oito sessões individuais de 25 a 30 minutos"],
              ["Dados", "Somente fictícios, com contas de teste do domínio exemplo.test"],
              ["Gravação", "Apenas da tela e apenas com autorização no termo; sem gravar rosto"],
              ["Ferramentas", "Navegador, cronômetro e planilha; remoto: Google Meet; questionário em papel ou "
               "Google Forms"],
              ["Ambiente", "[[a preencher: sistema publicado, prévia da Vercel, computador da equipe com a "
               "carga fictícia ou protótipo clicável; versão (commit) testada]]"],
              ["Datas e local", "[[a preencher após as sessões]]"]],
             "elaborado pelos autores a partir de docs/ihc/plano-de-testes.md (2026).",
             larguras=[3.2, 12.8], tamanho=9)
    d.h3("6.3.2 Participantes")
    d.p("Estão previstos oito participantes, identificados apenas como P1 a P8. A composição preferida é "
        "de profissionais do CRIE — um da direção, três do serviço social ou da saúde, três da equipe "
        "pedagógica e um de outra função —, com ao menos metade usando computador raramente ou algumas vezes "
        "por semana. Na falta deles, a alternativa são voluntários adultos de fora da área de tecnologia, de "
        "preferência que trabalhem com atendimento ao público, educação ou saúde, com ao menos metade com 40 "
        "anos ou mais; nesse caso, o relatório deve registrar que não são os usuários reais. Integrantes da "
        "equipe e colegas do curso não participam. Cada participante assina o termo de participação "
        "voluntária (Apêndice H), que fica com a equipe, fora do repositório, por conter nome real.")
    d.quadro("q-perfil", "Perfil dos participantes",
             ["Participante", "Faixa etária", "Função", "Tempo na função", "Uso de computador",
              "Familiaridade (1 a 5)"],
             [[f"P{i}", "", "", "", "", ""] for i in range(1, 9)],
             "[[elaborado pelos autores a partir da planilha anonimizada (data)]]. Resultados a preencher após "
             "as sessões.", larguras=[2.2, 2.4, 3.4, 2.6, 2.8, 2.6], tamanho=9)
    d.h3("6.3.3 Tarefas")
    d.p(f"As sete tarefas derivam dos cenários de uso; os passos mínimos vêm dos fluxos da seção 3.2.5 e "
        f"servem de referência para a eficiência (Quadro {R('q-tarefas')}). Antes de cada sessão, o banco "
        f"de teste é restaurado para que todos os participantes encontrem os mesmos dados.")
    d.quadro("q-tarefas", "Tarefas do teste de usabilidade",
             ["Nº", "Tarefa, como o moderador lê", "Passos mínimos", "Tempo-limite", "Conclusão"],
             [["T1", "Você chegou para trabalhar. Descubra quantas demandas estão vencidas e qual delas está "
               "vencida há mais tempo.", "0", "1 min", "Diz o número certo e aponta a demanda"],
              ["T2", "Na reunião, alguém lembrou de um pedido de material adaptado para a turma da tarde. "
               "Descubra o que já foi feito.", "3", "1 min", "Abre a demanda certa e lê o histórico"],
              ["T3", "A reunião de saúde acabou. Registre esta demanda: Solicitar ao CAPSi vaga para "
               "avaliação, prioridade alta, responsável você, prazo daqui a 7 dias.", "7", "3 min",
               "Demanda gravada com os dados certos"],
              ["T4", "Você ligou para o CRAS e agora está esperando a resposta. Atualize a demanda do "
               "cadastro da família e anote o que fez.", "7", "3 min", "Estado Aguardando terceiros e "
               "anotação gravada"],
              ["T5", "O material adaptado chegou. Marque a demanda como resolvida e saia do sistema.", "9",
               "3 min", "Estado Concluída e sessão encerrada"],
              ["T6", "Bruna saiu de férias. Passe a demanda vencida dela para outra pessoa.", "4", "2 min",
               "Responsável trocado"],
              ["T7", "Registre como foi a oficina de música do Assistido Fictício A.", "7", "3 min",
               "Evolução gravada e visível na ficha"]],
             "elaborado pelos autores a partir de docs/ihc/plano-de-testes.md (2026).",
             larguras=[1.0, 7.6, 1.8, 1.8, 3.8], tamanho=9)
    d.h3("6.3.4 Métricas")
    d.quadro("q-metricas", "Métricas da avaliação de usabilidade",
             ["Dimensão", "Métrica", "Como medir"],
             [["Desempenho", "Tempo, em segundos", "Do fim da leitura da tarefa até a pessoa dizer "
               "\"terminei\" ou atingir o tempo-limite"],
              ["Desempenho", "Número de passos", "Cliques, escolhas e campos preenchidos, com a regra dos "
               "fluxos"],
              ["Precisão", "Erros", "Clique que não leva à tarefa, campo preenchido errado, mensagem de erro "
               "recebida, volta atrás"],
              ["Precisão", "Conclusão", "Sim, sim com ajuda ou não"],
              ["Resposta emocional", "Facilidade da tarefa", "Nota de 1 (muito difícil) a 5 (muito fácil) "
               "após cada tarefa"],
              ["Resposta emocional", "Satisfação e confiança", "Questionário final Q1 a Q8, de 1 (discordo "
               "totalmente) a 5 (concordo totalmente)"]],
             "elaborado pelos autores a partir de docs/ihc/plano-de-testes.md (2026).",
             larguras=[3.2, 3.8, 9.0], tamanho=9)
    d.p("Os indicadores consolidados por tarefa serão a taxa de conclusão, o tempo médio e mediano, a "
        "eficiência (passos mínimos divididos pelos passos médios), os erros médios e a média das notas de "
        "facilidade. Os problemas encontrados serão classificados em quatro níveis de gravidade: 4, "
        "impeditivo (a pessoa não conclui); 3, grave (conclui com erro, ajuda ou muito mais passos que o "
        "mínimo); 2, moderado (hesita ou volta atrás); e 1, cosmético.")
    d.h3("6.3.5 Resultados")
    d.p("**Resultados a preencher após as sessões.** [[a preencher pela equipe: sessões realizadas (__ de "
        "8), tarefas aplicadas e desvios em relação ao plano]].")
    d.tabela("t-desempenho", "Desempenho e precisão por tarefa",
             ["Tarefa", "Conclusão (sim / com ajuda / não)", "Tempo médio (s)", "Tempo mediano (s)",
              "Passos médios", "Passos mínimos", "Eficiência", "Erros médios", "Facilidade média (1 a 5)"],
             [["T1", "", "", "", "", "0", "—", "", ""],
              ["T2", "", "", "", "", "3", "", "", ""],
              ["T3", "", "", "", "", "7", "", "", ""],
              ["T4", "", "", "", "", "7", "", "", ""],
              ["T5", "", "", "", "", "9", "", "", ""],
              ["T6", "", "", "", "", "4", "", "", ""],
              ["T7", "", "", "", "", "7", "", "", ""]],
             "[[elaborado pelos autores a partir da planilha anonimizada (data)]]. Resultados a preencher após "
             "as sessões.", larguras=[1.3, 2.6, 1.6, 1.7, 1.6, 1.6, 1.8, 1.6, 2.2], tamanho=8.5)
    d.figura_pendente("f-graficos", "Conclusão e tempo por tarefa no teste de usabilidade",
                      "gráficos gerados da planilha consolidada: barras empilhadas de conclusão por tarefa e "
                      "tempos de cada participante com a mediana e o tempo-limite; largura 1280 px",
                      "entregas/extensao/prints/21-graficos-usabilidade.png",
                      "[[elaborado pelos autores a partir da planilha anonimizada (data)]].")
    d.tabela("t-emocional", "Respostas ao questionário de satisfação e confiança",
             ["Afirmação", "Média", "1 a 2 (discorda)", "3", "4 a 5 (concorda)"],
             [["Q1 Foi fácil entender o que cada tela mostra.", "", "", "", ""],
              ["Q2 Os nomes dos botões e menus são as palavras que uso no trabalho.", "", "", "", ""],
              ["Q3 Eu conseguiria registrar uma demanda sozinha(o), sem ajuda.", "", "", "", ""],
              ["Q4 Eu sabia o que fazer quando apareceu uma mensagem de erro.", "", "", "", ""],
              ["Q5 Eu me senti segura(o) de que o que registrei ficou guardado.", "", "", "", ""],
              ["Q6 Ficou claro quais demandas estão atrasadas.", "", "", "", ""],
              ["Q7 Eu usaria este sistema no lugar do papel e da planilha.", "", "", "", ""],
              ["Q8 De modo geral, fiquei satisfeita(o) com o sistema.", "", "", "", ""]],
             "[[elaborado pelos autores a partir dos questionários anonimizados (data)]]. Resultados a "
             "preencher após as sessões.", larguras=[8.4, 1.6, 2.2, 1.4, 2.4], tamanho=9)
    d.p("A afirmação Q5 mede a confiança e a Q8, a satisfação geral; as demais indicam onde está o problema "
        "quando a nota cai. **Comentários dos participantes:** [[transcrever, anonimizados como P1 a P8, "
        "sem alterar o sentido]].")
    d.h3("6.3.6 Problemas encontrados e correções")
    d.quadro("q-problemas", "Problemas de usabilidade e sugestões de correção",
             ["Nº", "Problema", "Tela", "Tarefa", "Participantes", "Gravidade", "Sugestão de correção",
              "Corrigido em"],
             [["U1", "", "", "", "", "", "", ""], ["U2", "", "", "", "", "", "", ""],
              ["U3", "", "", "", "", "", "", ""]],
             "[[elaborado pelos autores (data)]]. Resultados a preencher após as sessões.",
             larguras=[1.0, 3.4, 1.8, 1.4, 2.0, 1.8, 3.0, 1.6], tamanho=8.5)
    d.h2("6.4 Retorno da instituição parceira")
    d.p("[[a preencher pela equipe: retorno da direção do CRIE sobre o sistema publicado e sobre os "
        "resultados dos testes, com data e canal; se não houver retorno até a entrega, registrar que a "
        "validação com a instituição fica pendente]].")


def secao7(d, R):
    d.h1("7 CONCLUSÃO")
    d.p("O projeto partiu da escuta da instituição parceira, e seu primeiro resultado foi a constatação de "
        "que a concepção inicial da equipe divergia da realidade institucional em três aspectos "
        "estruturais. As etapas seguintes converteram esse entendimento em artefatos — requisitos, "
        "minimundo, DER, personas e especificações de comportamento — e, nos dois últimos ciclos, em um "
        "sistema implementado e publicado.")
    d.p("Ao final, o sistema permite registrar as demandas que saem das três reuniões semanais, acompanhar "
        "seu andamento até o desfecho, identificar em uma única tela as que estão vencidas e consultar, na "
        "ficha de cada pessoa assistida, tudo o que já foi feito — as três consequências do registro em "
        "papel relatadas pela direção. A API em Flask aplica os conceitos de orientação a objetos a "
        "problemas concretos do domínio, como as permissões por perfil e a impossibilidade de apagar o "
        "histórico; o banco de dados garante as mesmas regras por restrições e gatilhos; a interface em "
        "React segue a especificação produzida pela frente de Interface; e 570 testes automatizados "
        "verificam o comportamento especificado.")
    d.p("Os principais desafios foram o atraso do modelo relacional, que bloqueou a implementação até o "
        "início de novembro e concentrou o desenvolvimento nas três últimas semanas; a disponibilidade "
        "limitada da instituição para responder às decisões em aberto; e a etapa de validação com usuários, "
        "que até o fechamento desta versão não havia sido realizada. No processo, a revisão de código entre "
        "integrantes não ficou registrada, e as contribuições no repositório concentraram-se em uma conta.")
    d.p("Como lições aprendidas, a equipe destaca que a formulação das perguntas determina a qualidade das "
        "respostas no levantamento de requisitos; que escrever o comportamento antes do código permitiu "
        "trabalhar em paralelo e reduziu retrabalho; que registrar as decisões em aberto com uma solução "
        "provisória explícita evita tomar suposição por decisão; e que a validação com o público-alvo "
        "precisa ser agendada cedo, porque depende de pessoas de fora da equipe.")
    d.p("Como trabalhos futuros, ficam: a execução e o registro dos testes de usabilidade, com as correções "
        "que deles resultarem; a orientação formal à instituição sobre suas responsabilidades como "
        "controladora dos dados e a rotina de cópia de segurança; o manual de uso; o cadastro dos serviços "
        "da rede e o retorno de acompanhamento dos encaminhamentos; o aviso por e-mail; o armazenamento "
        "compartilhado do limite de tentativas de login; e, fora do escopo atual, o controle de estoque de "
        "materiais, a outra necessidade levantada pela instituição.")
    d.p("[[a completar pela equipe após os testes de usabilidade e o retorno da instituição: síntese dos "
        "resultados da validação e resposta ao critério de aceitação 7]].")


REFERENCIAS = [
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: informação e documentação: referências: "
    "elaboração. Rio de Janeiro: ABNT, 2018.",
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6024**: informação e documentação: numeração "
    "progressiva das seções de um documento: apresentação. Rio de Janeiro: ABNT, 2012a.",
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6027**: informação e documentação: sumário: "
    "apresentação. Rio de Janeiro: ABNT, 2012b.",
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 10520**: informação e documentação: citações em "
    "documentos: apresentação. Rio de Janeiro: ABNT, 2023.",
    "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 14724**: informação e documentação: trabalhos "
    "acadêmicos: apresentação. Rio de Janeiro: ABNT, 2011.",
    "BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). "
    "**Diário Oficial da União**: Brasília, DF, 2018a.",
    "BRASIL. Ministério da Educação. Conselho Nacional de Educação. Resolução nº 7, de 18 de dezembro de "
    "2018. Estabelece as Diretrizes para a Extensão na Educação Superior Brasileira. **Diário Oficial da "
    "União**: Brasília, DF, 2018b.",
    "EQUIPE CORTEX. **Projeto interdisciplinar de Banco de Dados I**: Sistema de Gestão de Demandas de "
    "Articulação do CRIE/APAE de Extrema-MG. Bragança Paulista: IFSP, 2026a.",
    "EQUIPE CORTEX. **sistema-demandas-crie**: repositório do Sistema de Gestão de Demandas de "
    "Articulação. GitHub, 2026b. Disponível em: https://github.com/Team-Cortex/sistema-demandas-crie. "
    "Acesso em: 23 nov. 2026.",
    "HEUSER, Carlos Alberto. **Projeto de banco de dados**. 3. ed. Porto Alegre: Sagra Luzzatto, 2000.",
    "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO. **Documento de Especificação de "
    "Projeto Integrado de Extensão**: BRAEXT2. Bragança Paulista: IFSP, 2026.",
    "INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO 9241-210**: ergonomics of human-system "
    "interaction: part 210: human-centred design for interactive systems. Geneva: ISO, 2019.",
    "INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO/IEC 25010**: systems and software engineering: "
    "systems and software Quality Requirements and Evaluation (SQuaRE): system and software quality "
    "models. Geneva: ISO, 2011.",
    "ROSENFELD, Louis; MORVILLE, Peter; ARANGO, Jorge. **Information architecture**: for the web and "
    "beyond. 4. ed. Sebastopol: O'Reilly Media, 2015.",
    "SERVIÇO BRASILEIRO DE APOIO ÀS MICRO E PEQUENAS EMPRESAS. **O método Kanban**: uma metodologia ágil "
    "para aumentar a produtividade e reduzir desperdícios. [S. l.]: Sebrae, [2023]. E-book.",
    "W3C. **Web Content Accessibility Guidelines (WCAG) 2.2**. [S. l.]: W3C, 2023. Disponível em: "
    "https://www.w3.org/TR/WCAG22/. Acesso em: 23 nov. 2026.",
]

TRECHO_USUARIO = '''class Usuario(db.Model):
    __tablename__ = "usuario"
    # ... colunas id, nome, email, ativo, perfil, criado_em
    # Encapsulamento: o hash só é lido e escrito por definir_senha e senha_confere.
    _senha_hash = db.Column("senha_hash", db.String(255), nullable=False)
    # Herança de tabela única: `perfil` escolhe a subclasse ao carregar a linha.
    __mapper_args__ = {
        "polymorphic_on": perfil,
        "polymorphic_abstract": True,
    }

    def definir_senha(self, senha):
        if not isinstance(senha, str) or len(senha) < SENHA_MINIMA:
            raise ValueError(f"A senha precisa ter no mínimo {SENHA_MINIMA} caracteres.")
        self._senha_hash = generate_password_hash(senha)

    def senha_confere(self, senha):
        if not self._senha_hash or not isinstance(senha, str):
            return False
        return check_password_hash(self._senha_hash, senha)

    def pode_ver_evolucao(self, assistido):
        """Polimorfismo: cada perfil responde. A rota não olha a classe."""
        raise NotImplementedError

    # ... pode_gerir_usuarios, pode_emitir_relatorio e pode_consultar_auditoria


class Direcao(Usuario):
    """Direção da instituição. Cadastra usuários e emite relatórios."""

    __mapper_args__ = {"polymorphic_identity": "direcao"}

    def pode_ver_evolucao(self, assistido):
        return bool(self.ativo)

    # ... demais permissões: return bool(self.ativo)


class Profissional(Usuario):
    """O que é comum a quem atende assistidos. Não vira linha sozinha."""

    __mapper_args__ = {"polymorphic_abstract": True}

    # A direção do CRIE escolheu acesso aberto (relatório v2, spec 01).
    # A regra restritiva continua aqui, desligada.
    acesso_restrito = False

    def acompanha(self, assistido):
        return self in getattr(assistido, "profissionais", ())

    def pode_ver_evolucao(self, assistido):
        if not self.ativo:
            return False
        if self.acesso_restrito:
            return self.acompanha(assistido)
        return True

    # ... demais permissões: return False


class AssistenteSocial(Profissional):
    __mapper_args__ = {"polymorphic_identity": "assistente_social"}


class EquipePedagogica(Profissional):
    __mapper_args__ = {"polymorphic_identity": "equipe_pedagogica"}
'''


def _consulta(numero):
    txt = open(os.path.join(WT, "docs", "modelagem", "sql", "03_consultas.sql"), encoding="utf-8").read()
    ini = txt.find(f"{numero}.")
    ini = txt.rfind("/*", 0, ini)
    fim = txt.find(";", ini) + 1
    return txt[ini:fim].strip()


def finais(d, R):
    d.titulo_sem_numero("REFERÊNCIAS")
    d.doc.paragraphs[-1].paragraph_format.page_break_before = True
    for ref in REFERENCIAS:
        d.referencia(ref)
    d.titulo_sem_numero("ANEXOS")
    d.doc.paragraphs[-1].paragraph_format.page_break_before = True
    d.p("Os anexos reúnem documentos produzidos no contato com a comunidade externa. Termos de participação "
        "nos testes, por conterem nomes reais, ficam sob guarda da equipe e não são reproduzidos.",
        recuo=False)
    d.alineas([
        "ANEXO A — Formulário de Manifestação de Interesse em Participação em Projeto de Extensão, assinado "
        "pela direção do CRIE.",
        "ANEXO B — Formulário de Levantamento de Requisitos respondido pela direção da instituição.",
        "ANEXO C — Registro das interações com a instituição parceira.",
        "ANEXO D — [[Registro escrito do retorno recebido na EXPOEX, se houver]]."])
    d.titulo_sem_numero("APÊNDICES")
    d.doc.paragraphs[-1].paragraph_format.page_break_before = True
    d.p("Os apêndices A a H são documentos elaborados pela equipe e mantidos no repositório; o Apêndice I "
        "reproduz trechos de código citados no texto.", recuo=False)
    d.alineas([
        "APÊNDICE A — Documento de Requisitos de Software, versão 4.0.",
        "APÊNDICE B — Contrato da API, em vigor, atualizado em 16/11/2026 (docs/contrato-api.md).",
        "APÊNDICE C — Documento de arquitetura do sistema (docs/arquitetura.md).",
        "APÊNDICE D — Especificação do minimundo e Diagrama Entidade-Relacionamento (docs/modelagem).",
        "APÊNDICE E — Personas, cenários de uso, arquitetura da informação, fluxos, especificação de telas e "
        "protótipo clicável (docs/ihc).",
        "APÊNDICE F — Especificações de comportamento do servidor, specs 01 a 09 (docs/specs).",
        "APÊNDICE G — Documento de Banco de Dados 1 e scripts SQL (docs/modelagem/bd1 e docs/modelagem/sql).",
        "APÊNDICE H — Plano de testes de usabilidade, termo de participação voluntária e modelos de planilha "
        "(docs/ihc).",
        "APÊNDICE I — Trechos de código."])
    d.titulo_sem_numero("APÊNDICE I — TRECHOS DE CÓDIGO")
    d.doc.paragraphs[-1].paragraph_format.page_break_before = True
    d.codigo("Código da hierarquia de usuários (trecho)", TRECHO_USUARIO,
             "backend/app/models/usuario.py, com omissões indicadas por reticências (EQUIPE CORTEX, 2026b).",
             rotulo="q-codigo-usuario")
    d.codigo("Consulta Q03 do projeto de Banco de Dados 1", _consulta("Q03"),
             "docs/modelagem/sql/03_consultas.sql (EQUIPE CORTEX, 2026b).", rotulo="q-codigo-q03")
    d.codigo("Consulta Q09 do projeto de Banco de Dados 1", _consulta("Q09"),
             "docs/modelagem/sql/03_consultas.sql (EQUIPE CORTEX, 2026b).", rotulo="q-codigo-q09")
