# Volere 18 a 27, Partes III, IV, VI, VII e VIII
TEMAS = [
    ['Q-01', 'Quais campos de identificação do assistido a instituição precisa (A3, QA07)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-02', 'Quais são as categorias de demanda (A2, QA06)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-03', 'Quais são as áreas de atuação das evoluções (QA06)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-04', 'Destino do encaminhamento: serviço cadastrado, profissional interno ou texto livre (A1)', 'Frentes de banco de dados e back-end, com a direção', 'Versão 2.0'],
    ['Q-05', 'Formato e campos do relatório impresso (QA04)', 'Direção do CRIE', 'Versão 2.0'],
    ['Q-06', 'Que data define o período: registro da demanda, reunião ou prazo (A6)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-07', 'Por quanto tempo guardar auditoria e registros, e como tratar pedido de eliminação de dados (A7, QA08)', 'Direção do CRIE (controladora)', 'Antes da implantação'],
    ['Q-08', 'Quem mantém o sistema e dá suporte depois de 26/11/2026', 'Equipe e direção do CRIE', '26/11/2026'],
    ['Q-09', 'Horário de uso e disponibilidade esperada', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-10', 'Quem pode retificar uma evolução (A9)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-11', 'Quantos dias antes do prazo a demanda conta como “perto do prazo” (A10; hoje, 3)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-12', 'A coordenação de setor precisa de perfil próprio (A4)', 'Direção do CRIE', 'Versão 2.0'],
    ['Q-13', 'Qual é o aplicativo de cadastro em uso e se ele exporta dados (QA03)', 'Direção do CRIE', 'Versão 2.0'],
    ['Q-14', 'Que termo a instituição usa para as pessoas atendidas (relatório v3)', 'Direção do CRIE', 'Antes da implantação'],
    ['Q-15', 'Expiração por inatividade em vez de 30 minutos fixos; token em sessionStorage ou em cookie HttpOnly (A5)', 'Frentes de back-end e front-end', '25/11/2026'],
    ['Q-16', 'Autorização por escrito para usar o logotipo do CRIE (docs/CREDITOS-UI.md)', 'Direção do CRIE', '25/11/2026'],
    ['Q-17', 'Criação da primeira conta da direção em produção (PR #19)', 'Frente de back-end', '25/11/2026'],
    ['Q-18', 'Quando, com quem e em que ambiente serão os 8 testes de usabilidade (D4, D6)', 'Frente de IHC e direção do CRIE', '25/11/2026'],
    ['Q-19', 'Texto completo das personas P2 e P3 (D3)', 'Frente de IHC', '25/11/2026'],
]

V19A = [
    'A equipe não fez avaliação formal de produtos prontos. Neste documento foram consideradas três alternativas:',
    'Planilha compartilhada: parecida com o que o CRIE já usa, mas não registra autor e hora de cada mudança, permite apagar linhas e não controla quem vê dados de saúde. Descartada.',
    'Aplicativo de cadastro já usado pela instituição: não foi identificado (Q-13) e, pelo que a direção informou, não trata de demandas.',
    'Ferramenta de quadro de tarefas, como o Trello usado pela própria equipe: organiza cartões, mas guarda os dados fora do controle da instituição, não tem auditoria de leitura e não tem os conceitos de reunião, assistido, evolução e encaminhamento. Descartada.',
]
V19B = 'No servidor: Flask, Flask-SQLAlchemy, Flask-Migrate (Alembic), Flask-JWT-Extended, Flask-Cors, marshmallow e o werkzeug.security para o hash das senhas. No cliente: React, React Router, Axios, Vite e o elemento <dialog> do próprio navegador para os diálogos de confirmação. Na interface: a fonte Archivo (SIL Open Font License) e o logotipo do CRIE do repositório site-crie (docs/CREDITOS-UI.md). Na publicação: Vercel e Neon, nos planos gratuitos.'
V19C = 'O painel em colunas por estado segue a mesma ideia do quadro Kanban que a equipe usa no Trello: cada coluna é uma situação, e o que está parado fica à vista. Não houve cópia de código nem de especificação de outro produto.'

V20 = {
    '20a': 'Os profissionais passam a registrar no computador logo depois da reunião, em vez de anotar em papel, e o responsável precisa atualizar o estado quando faz algo. A direção passa a acompanhar pelo painel. Toda consulta a dados de assistidos fica registrada, o que muda a relação com a informação: dá transparência, mas pode ser sentido como vigilância (20c).',
    '20b': 'O aplicativo de cadastro continua em uso, então a mesma pessoa pode estar cadastrada nos dois sistemas. O sistema não instala nada nos computadores da instituição.',
    '20c': 'Resistência à mudança de quem tem pouca familiaridade com tecnologia; trabalho dobrado no início, enquanto o papel e o sistema convivem; sessão de 30 minutos que vence no meio de um registro (o rascunho guardado na aba reduz o problema); sensação de vigilância por causa da auditoria das consultas.',
    '20d': 'Não há modo offline, e a internet do CRIE é instável. O plano gratuito pode ter limites de uso e tempo de resposta maior na primeira requisição depois de um período parado (a medir, CT-89). O limite de tentativas de login fica na memória de cada processo: com mais de uma instância na Vercel, cada uma conta as suas falhas (spec 01).',
    '20e': 'A auditoria cresce sem limite enquanto não houver política de retenção (Q-07). Mudanças na LGPD ou nas orientações para dados de saúde podem exigir ajustes. Se a direção decidir restringir o acesso, a regra restritiva já existe no código, mas falta a tela e a rota para vincular profissional e assistido (Volere 26). Um novo perfil, como a coordenação de setor, exige uma subclasse nova.',
}

V21A = 'Ciclo de vida iterativo e incremental com Kanban (I.3). Para cada funcionalidade: spec com regras, mensagens e testes; código e testes numa branch; pull request para a development com a descrição do que foi feito e do que não foi verificado; CI no PR (a partir do PR #19); integração por merge commit; promoção da development para a main, que publica na Vercel. Backlog, ciclos e cronograma estão na Parte VI.'

V21B = [
    ['Versão 0.1: estrutura (ciclos 1 a 3)', '22/10/2026', 'Servidor Flask estruturado, testes com pytest, PostgreSQL local em Docker; projeto React inicial', '—', 'RNF-020, RNF-021, RNF-022, RNF-024'],
    ['Versão 0.5: back-end completo e publicação (ciclo 5)', '17/11/2026 (PRs #9 a #13)', 'API Flask com as specs 01 a 09, migrações, Vercel e Neon', 'RF-001 a RF-036, RF-038 a RF-040', 'RNF-001 a RNF-005, RNF-008, RNF-019, RNF-023, RNF-025, RNF-034'],
    ['Versão 0.9: front-end e IHC (EXPOEX)', '18/11/2026 (PRs #14 a #18)', 'Telas React de prioridade 1 a 3; protótipo clicável; material de IHC', 'Telas de todos os RF acima; RF-037 (impressão pelo navegador)', 'RNF-011 a RNF-016, RNF-027, RNF-028, RNF-033, RNF-035'],
    ['Versão 1.0: entrega final', '26/11/2026', 'CI e criação da primeira direção (PR #19); correções dos testes de usabilidade', 'Correções', 'RNF-032; validação de RNF-011, RNF-029 e RNF-036'],
    ['Versão 2.0: futura', 'Sem data', 'Depende das questões abertas Q-01 a Q-07', 'RF-041; itens da Sala de Espera', 'A definir'],
]

V22A = [
    'Proposta da equipe, ainda não combinada com a instituição. Não há migração automática: as demandas antigas estão em papel e planilhas com dados reais, que não podem passar pelo repositório nem pelas mãos da equipe do projeto.',
    '1. Criar a conta da direção em produção pelo comando administrativo (PR #19) e, pela tela Usuários, as contas dos profissionais.',
    '2. Antes de qualquer dado real, entregar a orientação sobre a LGPD (RNF-009) e deixar documentada a rotina de cópia de segurança (RNF-010).',
    '3. Uso em paralelo: as demandas novas são registradas no sistema, e o papel continua como apoio por algumas semanas.',
    '4. As demandas antigas ainda em aberto são digitadas pela própria equipe do CRIE, não pela equipe do projeto.',
    '5. Quando a direção considerar o painel confiável, o papel deixa de ser usado para demandas novas. As datas dependem da direção.',
]
V22B = [
    ['Demandas em aberto', 'Papel e planilhas', 'Digitação pelos profissionais na tela Registrar demanda', 'A planilha pode não ter prazo e prioridade; toda demanda precisa de uma reunião de origem, então será preciso registrar a reunião correspondente ou decidir como tratar as antigas'],
    ['Profissionais', 'Sem cadastro no sistema', 'Cadastro pela direção na tela Usuários', 'Cada profissional precisa de um e-mail'],
    ['Assistidos', 'Papel e aplicativo de cadastro', 'Cadastro só com o nome de tratamento', 'Campos definitivos dependem de Q-01; possível duplicidade com o aplicativo de cadastro'],
    ['Reuniões passadas', 'Papel', 'Não serão migradas; registro a partir da implantação', 'Histórico anterior à implantação fica no papel'],
]

RISCOS = [
    ['R-01', 'Testes de usabilidade e validação com o CRIE não acontecerem antes da entrega', 'Alta', 'Alto', 'Protótipo offline e roteiro prontos; propor à direção uma sessão curta; registrar como pendência e fazer em 2027 se preciso', 'Inácio Fontes'],
    ['R-02', 'Questões abertas do CRIE sem resposta (Q-01 a Q-07)', 'Alta', 'Médio', 'Soluções provisórias nas specs; um único bloco de perguntas fechadas e numeradas', 'Vinícius Marrocos'],
    ['R-03', 'Exposição de dado pessoal sensível', 'Baixa', 'Alto', 'Só dados fictícios; auditoria; hash de senha; HTTPS; verificação de segredos no CI', 'Miguel Vaz de Souza'],
    ['R-04', 'Conhecimento do código concentrado em um integrante', 'Alta', 'Alto', 'README do back-end, estado do projeto e specs; revisão de PR por outro integrante; trabalho em par na manutenção', 'Vinícius Marrocos'],
    ['R-05', 'Modelo relacional atrasado bloqueando o back-end', 'Ocorreu no ciclo 3', 'Alto', 'O back-end adiantou estrutura, specs e contrato; os models seguiram as specs, com o script de BD1 como referência', 'Henry Claro'],
    ['R-06', 'Planos gratuitos da Vercel ou do Neon mudarem', 'Baixa', 'Médio', 'Publicação reproduzível (vercel.json e migrações); PostgreSQL padrão, que roda em outro provedor', 'Miguel Vaz de Souza'],
    ['R-07', 'Ninguém para manter o sistema depois do semestre', 'Alta', 'Alto', 'Documentação de instalação e do estado do projeto; definir um responsável com a direção (Q-08)', 'Equipe'],
    ['R-08', 'Internet instável no CRIE', 'Média', 'Médio', 'Rascunho guardado na aba; mensagem clara de falha de conexão', 'Gabriel Borba'],
    ['R-09', 'Produção sem conta da direção, sem acesso possível', 'Ocorreu', 'Alto', 'Comando administrativo e workflow que criam a primeira direção (PR #19)', 'Miguel Vaz de Souza'],
    ['R-10', 'Diferença entre o SQLite dos testes e o PostgreSQL de produção', 'Média', 'Médio', 'Migrações conferidas em SQL; acrescentar ao CI uma execução contra PostgreSQL', 'Miguel Vaz de Souza'],
]

CUSTOS = [
    ['Esforço estimado por pontos de caso de uso (136 UCP × 20 h)', '2.720 h', '50,00', '136.000,00'],
    ['Hospedagem do front-end e da API na Vercel (12 meses)', 'Plano gratuito', '0,00', '0,00'],
    ['Banco PostgreSQL no Neon (12 meses)', 'Plano gratuito', '0,00', '0,00'],
    ['Domínio próprio', 'Não usado (endereço vercel.app)', '0,00', '0,00'],
    ['Total estimado', '—', '—', '136.000,00 (referência); custo para o CRIE: R$ 0,00'],
]
CUSTOS_METODO = 'Método de estimativa utilizado: pontos de caso de uso (Karner, 1993), contados a partir dos casos de uso da seção 8b. Atores: Profissional e Direção, ambos complexos (interface gráfica), peso 3 cada, total 6. Casos de uso: 4 simples (UC-002, UC-012, UC-013, UC-014; peso 5), 8 médios (UC-001, UC-003, UC-004, UC-005, UC-008, UC-009, UC-010, UC-011; peso 10) e 2 complexos (UC-006 e UC-007; peso 15), total 130. Pontos não ajustados: 136. Para simplificar, os fatores técnico e ambiental foram fixados em 1,0, e foram usadas 20 horas por ponto, valor proposto por Karner. O valor-hora de R$ 50,00 é o do exemplo do modelo da disciplina e serve só para dimensionar quanto o sistema custaria se fosse contratado. O custo real para o CRIE é zero: o trabalho é de estudantes em projeto de extensão e a hospedagem usa planos gratuitos.'

V25A = [
    ['README.md e backend/README.md', 'Visão geral, instalação do zero, variáveis de ambiente e publicação', 'Quem mantém o sistema', 'Frente de back-end (existe)'],
    ['docs/specs, docs/contrato-api.md e docs/estado-do-projeto.md', 'Comportamento do servidor, rotas e mapa do sistema', 'Desenvolvedores', 'Frente de back-end (existe)'],
    ['Manual de uso (RNF-026)', 'Passo a passo das tarefas T1 a T7, com imagens de dados fictícios', 'Direção e profissionais do CRIE', 'A definir pela equipe (pendente)'],
    ['Orientação sobre a LGPD (RNF-009)', 'Responsabilidades da instituição como controladora', 'Direção do CRIE', 'A definir pela equipe (pendente)'],
    ['Procedimento de cópia de segurança (RNF-010)', 'Como copiar e restaurar o banco do Neon', 'Quem mantém o sistema', 'A definir pela equipe (pendente)'],
]
V25B = 'Proposta da equipe, ainda não agendada: uma sessão presencial no CRIE, conduzida pela equipe, com a direção e os profissionais, usando o roteiro de tarefas T1 a T7 do protótipo e do plano de testes, contas de teste e dados fictícios. A duração será definida depois dos testes de usabilidade, que mostram quanto apoio é preciso. Elaboração e condução: frentes de IHC e de front-end.'

SALA = [
    ['RF-041', 'Aviso por e-mail das demandas vencidas', 'Ficou fora das specs; exige serviço de envio e cuidado para não levar dado de saúde', '2.0'],
    ['—', 'Envio de avisos por WhatsApp (N-10)', 'A API oficial é paga e exige aprovação', 'Sem previsão'],
    ['—', 'Controle de estoque de materiais (N-16)', 'Outro domínio; a direção priorizou as demandas', 'Outro projeto'],
    ['—', 'Anexo de laudos e documentos', 'Exige controles de armazenamento de dado de saúde', 'Sem previsão'],
    ['—', 'Integração com o aplicativo de cadastro', 'Aplicativo não identificado (Q-13)', 'Depende de Q-13'],
    ['—', 'Funcionamento offline', 'Complexidade alta para o prazo', 'Sem previsão'],
    ['—', 'Cadastro de serviços da rede e retorno de acompanhamento (DER)', 'Depende de Q-04 (A1)', '2.0'],
    ['—', 'Relatório em PDF ou no formato pedido pela instituição', 'Depende de Q-05 (QA04)', '2.0'],
    ['—', 'Tela e rota para vincular profissional e assistido', 'Só necessária se a direção ligar a regra restritiva', 'Quando a direção pedir'],
    ['—', 'Troca de senha pelo próprio usuário e “esqueci a senha”', 'Fora da spec 01', '2.0'],
]

V27 = [
    'Renovar o token a cada ação, para que a expiração conte inatividade e não o tempo desde o login (Q-15). Segundo a equipe, isso está sendo feito no front-end em outro pull request, ainda não integrado.',
    'Guardar o token em cookie HttpOnly em vez de sessionStorage (A5).',
    'Guardar a contagem de falhas de login no banco, para valer em todas as instâncias.',
    'Exportar relatórios em PDF.',
    'Avisos dentro do sistema também fora do login, por exemplo no painel.',
    'Repetir o card sorting com dois ou três profissionais do CRIE, de forma aberta.',
    'Aviso por e-mail só com o número da demanda, sem conteúdo.',
]

# Parte III
III1 = [
    'Validar o fluxo de registro e acompanhamento com a equipe e, depois, com os profissionais do CRIE; servir de roteiro para os testes de usabilidade; orientar as telas do front-end.',
    'Média no Figma: tela do painel e telas iniciais, incompletas em 22/10/2026 (relatório v3, seção 3.2.3). Alta no protótipo clicável em HTML, navegável, com os três perfis e as tarefas T1 a T7. As telas do sistema React seguem a especificação tela a tela (docs/ihc/telas.md).',
    'Figma (fora do repositório); HTML, CSS e JavaScript num arquivo único que funciona sem internet; React no sistema.',
    'docs/ihc/prototipo/index.html no repositório (abrir no navegador). Link do Figma: não registrado no repositório (pendente). Sistema: https://sistema-demandas-crie.vercel.app',
    'Protótipo clicável de 18/11/2026 (PR #14), ainda com o visual anterior ao PR #18 (ícones e selos coloridos). Sem validação com usuários até 23/11/2026 (III.6).',
]
III2 = [
    'Texto #252331; texto secundário #615F6D; fundo #F7F8FA; superfície #FFFFFF; borda #DEDEE6; primária #8A21CE; primária escura (links e foco) #6B179F; fundo de destaque #F4EAFA; erro e alerta #9A3039 sobre #FFF2F1; sucesso #226749 (frontend/src/index.css). Contrastes calculados pela fórmula da WCAG: texto sobre fundo 14,5:1; texto secundário sobre branco 6,2:1; branco sobre a primária 6,6:1; link sobre branco 9,3:1; erro sobre branco 7,4:1; sucesso sobre branco 6,8:1.',
    'Archivo (SIL Open Font License), com Segoe UI e Arial como alternativas. Texto base de 16 px com entrelinha 1,5; título h1 de 28 px, h2 de 20 px e h3 de 16,8 px; pesos 400, 600 e 700; botões em 600.',
    'Botão primário (fundo primário e texto branco) e secundário (com borda), altura mínima de 44 px e raio de 6 px; campos sempre com rótulo e erro ligado ao campo; diálogo nativo do navegador, que prende o foco e fecha com Esc; aviso de sucesso no topo, que não some sozinho; estados “Carregando…”, vazio (com o que fazer) e erro (com “Tentar de novo”); menu lateral só com texto.',
    'Sem ícones no sistema (retirados no PR #18). Logotipo do CRIE na tela Entrar e no topo do menu; origem em docs/CREDITOS-UI.md e autorização por escrito pendente (Q-16). O protótipo clicável ainda usa ícones Lucide.',
    'Até cerca de 768 px de largura, o menu vira um painel recolhível aberto pelo botão Menu; as colunas do painel viram seções empilhadas e a tabela de demandas vira lista de cartões. Conferido em 360 px e 1280 px (PR #18).',
    'Contraste mínimo de 4,5:1 para texto (valores acima); foco visível com contorno de 3 px; Tab em ordem lógica; Esc fecha diálogos; rótulo em todo campo; alvos de 44 px; texto base de 16 px; estado e vencimento sempre escritos, sem depender só da cor; aria-current no item atual do menu.',
]

TELAS_INV = [
    ['T-01', 'Entrar', 'Identificar a pessoa', 'Todos', 'UC-001 / RF-001, RF-002, RNF-034'],
    ['T-02', 'Painel', 'Ver numa tela só o que está em aberto e vencido', 'Todos', 'UC-007, UC-002 / RF-030, RF-033, RF-039, RF-040'],
    ['T-03', 'Minhas demandas', 'Ver o que está com a própria pessoa', 'Todos', 'UC-007 / RF-034'],
    ['T-04', 'Demandas', 'Achar qualquer demanda, inclusive antiga', 'Todos', 'UC-007 / RF-031, RF-032, RNF-036'],
    ['T-05', 'Registrar demanda', 'Registrar em um formulário e uma confirmação', 'Todos', 'UC-005 / RF-010, RF-011, RNF-012, RNF-016'],
    ['T-06', 'Demanda (detalhe)', 'Ver e atualizar a demanda', 'Todos', 'UC-006, UC-007 / RF-012 a RF-017'],
    ['T-07', 'Reuniões', 'Listar as reuniões por data e setor', 'Todos', 'UC-004 / RF-007'],
    ['T-08', 'Registrar ou editar reunião', 'Registrar data, setor e participantes', 'Todos', 'UC-004 / RF-006, RF-009'],
    ['T-09', 'Reunião (ficha)', 'Ver as demandas que saíram da reunião', 'Todos', 'UC-004 / RF-008'],
    ['T-10', 'Assistidos', 'Listar e buscar pelo nome de tratamento', 'Todos', 'UC-008 / RF-019'],
    ['T-11', 'Cadastrar ou editar assistido', 'Cadastrar só o nome de tratamento', 'Todos', 'UC-008 / RF-018, RNF-008'],
    ['T-12', 'Ficha do assistido', 'Ver demandas, evoluções e encaminhamentos', 'Todos', 'UC-008 / RF-020, RF-023'],
    ['T-13', 'Lançar evolução', 'Registrar o acompanhamento', 'Todos', 'UC-009 / RF-021, RF-022'],
    ['T-14', 'Evolução (versões)', 'Retificar e ver as versões anteriores', 'Todos', 'UC-009 / RF-024, RF-026'],
    ['T-15', 'Encaminhamentos', 'Ver pendentes e registrar desfecho', 'Todos', 'UC-010 / RF-028, RF-029'],
    ['T-16', 'Registrar encaminhamento', 'Encaminhar a partir da demanda ou da ficha', 'Todos', 'UC-010 / RF-027'],
    ['T-17', 'Usuários', 'Cadastrar, editar e desativar contas', 'Direção', 'UC-003 / RF-004, RF-003'],
    ['T-18', 'Relatórios', 'Emitir e imprimir relatórios', 'Direção', 'UC-011 / RF-035 a RF-039'],
    ['T-19', 'Auditoria', 'Consultar quem fez o quê com dados de assistidos', 'Direção', 'UC-012 / RNF-003'],
]

TELAS_DESC = [
    dict(t='T-01', nome='Entrar', img='T-01.png',
         obj='Identificar a pessoa (RF-001).',
         el='Logotipo do CRIE; título “Sistema de Demandas”; campos E-mail e Senha; caixa “Mostrar senha”; botão Entrar; linha “Use o e-mail e a senha que a direção cadastrou.”',
         reg='E-mail e senha obrigatórios; o servidor bloqueia na sexta falha em 60 s (RNF-034).',
         msg='“Informe o e-mail.” / “Informe a senha.”; “E-mail ou senha inválidos.” (sem dizer qual); “Não foi possível falar com o servidor. Confira a internet e tente de novo.”; “Sua sessão terminou. Entre de novo.”',
         nav='Origem: endereço do sistema ou sessão encerrada / Destino: T-02, ou a tela em que a sessão terminou',
         req='RF-001, RF-002, RNF-002, RNF-005, RNF-014, RNF-034'),
    dict(t='T-02', nome='Painel', img='T-02.png',
         obj='Ver numa tela só o que está em aberto e o que está vencido (persona P1).',
         el='Aviso de prazo (se houver pendência), com um link por demanda; indicadores Em aberto, Vencidas e um por estado; três colunas (Aberta, Em andamento, Aguardando terceiros) com cartões de número, descrição, prioridade, responsável e prazo; botão Registrar demanda.',
         reg='Vencidas no topo de cada coluna, pela ordem do prazo; concluídas e canceladas fora; o aviso não mostra descrição (RN-14).',
         msg='“Nenhuma demanda em aberto. Quando a equipe registrar uma demanda, ela aparece aqui.”; “Nenhuma demanda neste estado.”',
         nav='Origem: T-01 / Destino: T-06 (cartão), T-05 (Registrar demanda) e itens do menu',
         req='RF-030, RF-033, RF-039, RF-040, RNF-028'),
    dict(t='T-04', nome='Demandas', img='T-04.png',
         obj='Achar qualquer demanda, inclusive antiga (cenário C2).',
         el='Busca “Procurar na descrição”; filtros Estado, Responsável, Categoria, Período e Assistido; Limpar filtros; tabela com Descrição, Estado, Responsável, Prazo e Prioridade (lista de cartões no celular); botão Registrar demanda.',
         reg='Sem filtro, mostra as não canceladas; com filtro, vale só o filtro (inclusive para achar cancelada); ordem pelo último movimento.',
         msg='“Nenhuma demanda encontrada com esses filtros. Tente tirar um filtro ou procurar outra palavra.”',
         nav='Origem: menu / Destino: T-06 e T-05',
         req='RF-031, RF-032, RF-033, RNF-036'),
    dict(t='T-05', nome='Registrar demanda', img='T-05.png',
         obj='Registrar a demanda em um formulário e uma confirmação (cenário C3).',
         el='Descrição; Prioridade (Baixa, Média, Alta); Responsável; Prazo; Reunião de origem (já com a mais recente); Assistido (opcional); Categoria (opcional, até 80 caracteres); botões Registrar demanda e Voltar; diálogo “Confirmar registro da demanda?” com o resumo.',
         reg='Obrigatórios: descrição, prioridade, responsável ativo, prazo e reunião; categoria até 80 caracteres; nada é apagado em falha de conexão.',
         msg='“Informe a descrição da demanda.”; “Escolha a prioridade.”; “Escolha o responsável.”; “Informe o prazo.”; “Escolha a reunião em que a demanda surgiu.”; “Demanda registrada com sucesso.”',
         nav='Origem: T-02, T-04 ou T-09 / Destino: T-06 depois de confirmar',
         req='RF-010, RF-011, RF-014, RNF-012, RNF-014, RNF-016, RNF-029'),
    dict(t='T-06', nome='Demanda (detalhe)', img='T-06.png',
         obj='Ver tudo de uma demanda e atualizar o andamento.',
         el='Descrição; estado, responsável, prazo, prioridade, reunião de origem, assistido, categoria, data de registro e último movimento; histórico numerado; campo Anotar; botões Mudar estado, Trocar responsável e Encaminhar.',
         reg='O diálogo Mudar estado mostra só as transições permitidas (RN-02) e some quando a demanda está encerrada; troca só para profissional ativo.',
         msg='“Esta demanda não pode mudar para esse estado.”; “Escreva o texto da anotação.”; “A demanda continua no histórico e pode ser encontrada pela busca.” (ao cancelar); “Esta demanda não existe ou o endereço está errado.”',
         nav='Origem: T-02, T-03, T-04, T-09 ou aviso de prazo / Destino: diálogos, T-09, T-12 e T-16',
         req='RF-012 a RF-017, RNF-019'),
    dict(t='T-09', nome='Reunião (ficha)', img='T-09.png',
         obj='Ver as demandas que saíram de uma reunião e o estado de cada uma.',
         el='Data, setor e participantes; lista das demandas da reunião com o estado; botões Editar reunião e Registrar demanda desta reunião.',
         reg='Editar a reunião não apaga as demandas ligadas a ela.',
         msg='“Reunião inexistente.” quando o endereço não existe.',
         nav='Origem: T-07 / Destino: T-06, T-08 e T-05 (com a reunião escolhida)',
         req='RF-006, RF-008, RF-009'),
    dict(t='T-12', nome='Ficha do assistido', img='T-12.png',
         obj='Ver tudo o que já foi feito por uma pessoa atendida (RF-020).',
         el='Nome de tratamento; seções Demandas, Evoluções e Encaminhamentos em ordem cronológica; botões Lançar evolução e Encaminhar.',
         reg='Só a versão vigente de cada evolução; toda abertura da ficha é auditada.',
         msg='“Você não tem acesso às evoluções deste assistido.” (com a regra restritiva ligada)',
         nav='Origem: T-10 ou link da demanda / Destino: T-13, T-14, T-16 e T-06',
         req='RF-005, RF-020, RF-023, RNF-003'),
    dict(t='T-13', nome='Lançar evolução', img='T-13.png',
         obj='Registrar o acompanhamento de um assistido.',
         el='Data (hoje por padrão); Área de atuação (até 80 caracteres); Descrição; botão Salvar. Autor e horário aparecem depois de salvar, vindos do servidor.',
         reg='Os três campos são obrigatórios; o corpo da requisição não escolhe autor nem horário; não existe a opção Excluir.',
         msg='“Informe a data da evolução.”; “Informe a área de atuação.”; “Escreva a descrição da evolução.”',
         nav='Origem: T-12 / Destino: T-12 depois de salvar',
         req='RF-021, RF-022, RF-026, RNF-003'),
    dict(t='T-15', nome='Encaminhamentos', img='T-15.png',
         obj='Ver o que a rede ainda não respondeu e registrar o desfecho.',
         el='Alternância Pendentes / Todos; lista do mais antigo para o mais novo, com destino, data, responsável e situação; ação Registrar desfecho.',
         reg='O desfecho é registrado uma única vez; registrar tira o encaminhamento da lista de pendentes.',
         msg='“O desfecho só pode ser registrado uma vez.” antes de confirmar; “Este encaminhamento já tem desfecho registrado.”',
         nav='Origem: menu / Destino: T-06 ou T-12 (vínculos)',
         req='RF-027, RF-028, RF-029'),
    dict(t='T-17', nome='Usuários', img='T-17.png',
         obj='Administrar as contas (só a direção).',
         el='Lista por nome com e-mail, perfil e situação; botões Cadastrar, Editar e Desativar; formulário com nome, e-mail, perfil e senha inicial.',
         reg='Senha com no mínimo 8 caracteres; e-mail único; desativar nunca exclui; a direção não vê o botão Desativar na própria linha.',
         msg='“Já existe um usuário com este e-mail.”; “A senha precisa ter no mínimo 8 caracteres.”; “A pessoa não consegue mais entrar. O histórico dela continua no sistema.”',
         nav='Origem: menu da direção / Destino: a própria tela',
         req='RF-003, RF-004, RNF-002'),
    dict(t='T-18', nome='Relatórios', img='T-18.png',
         obj='Emitir o relatório de demandas do período e o de acompanhamento do assistido (só a direção).',
         el='Escolha do relatório; De e Até (obrigatórios); filtros Estado, Categoria e Responsável ou o assistido; totais por estado e vencidas; lista; rodapé “Emitido por … em …”; botão Imprimir.',
         reg='Período obrigatório e coerente; toda emissão é auditada com o mesmo horário do rodapé.',
         msg='“Informe o período do relatório (de e ate).”; “Só a direção emite relatórios.”',
         nav='Origem: menu da direção / Destino: impressão do navegador',
         req='RF-035 a RF-039, RNF-003'),
    dict(t='T-19', nome='Auditoria', img='T-19.png',
         obj='Consultar quem criou, alterou, consultou ou emitiu relatório com dados de assistidos.',
         el='Tabela paginada com quando, quem, ação, recurso e assistido; filtros por autor, assistido, recurso, ação e período.',
         reg='Só leitura; 50 registros por página (máximo 200); do mais recente para o mais antigo.',
         msg='“Use datas no formato AAAA-MM-DD.”; “A data inicial não pode ser depois da final.”; “Só a direção consulta a auditoria.”',
         nav='Origem: menu da direção / Destino: a própria tela',
         req='RNF-003, RF-003'),
]

III6 = [
    ['01/10/2026', 'Equipe (frentes de interface e front-end)', 'Telas iniciais no Figma', 'Revisão interna das telas em conjunto (cartão “Apoiar a prototipação”); não é validação com usuário', 'Cartão reaberto; os demais itens ficaram para depois do protótipo', '—'],
    ['18/11/2026', 'Equipe (revisão interna)', 'Todas as telas do sistema', 'Excesso de elementos decorativos (ícones, selos coloridos, pílulas) que não acrescentavam informação', 'PR #18: estado e prazo por escrito, menu só com texto, sem ícones', 'RNF-028, RNF-015'],
    ['Pendente', '8 participantes (profissionais do CRIE ou voluntários, decisão D4)', 'T-01 a T-13 (tarefas T1 a T7)', 'Ainda não realizado', '—', 'RNF-011, RNF-013, RNF-029, RNF-036'],
]
III6_TEXTO = 'A validação dos protótipos com usuários não foi feita até 23/11/2026. O plano está pronto em docs/ihc/plano-de-testes.md: 8 sessões individuais de 25 a 30 minutos, de preferência presenciais no CRIE, com pensar em voz alta, um moderador e um anotador, tarefas T1 a T7 tiradas dos cenários, medição de tempo, passos, erros, conclusão e satisfação (questionário Q1 a Q8) e termo de participação. As planilhas modelo estão em docs/ihc e o relatório de usabilidade (docs/ihc/relatorio-de-usabilidade.md) está vazio de propósito, à espera dos resultados. Nenhum resultado, fala ou nota foi preenchido antes de os testes acontecerem. Esta é a principal pendência da equipe para a Parte III.'

# Parte IV
IV1 = [
    'Os requisitos foram agrupados como no Volere: funcionais (seção 9, RF-001 a RF-041, nos nove grupos de docs/requisitos.md: acesso, reuniões, demandas, assistidos, evoluções, encaminhamentos, consulta, relatórios e avisos), não funcionais (seções 10 a 17, RNF-001 a RNF-037) e restrições (seção 3, RS-01 a RS-06).',
    'A hierarquia vai da necessidade ao teste: necessidade (N, I.4e) → caso de uso (UC) → requisito (RF ou RNF) → regra de comportamento na spec → caso de teste (CT ou CB). Os requisitos amplos não foram quebrados em RF-xxx.y: o detalhe ficou nas specs 01 a 09, que fixam campos, mensagens e transições. Por exemplo, RF-012 vira a tabela de transições da spec 02 e os 25 pares testados em CT-28, CT-30, CB-01 e CB-02.',
    'Os valores numéricos dos critérios de ajuste que não vieram da instituição (por exemplo, 6 de 8 participantes ou média 4 no questionário) são metas propostas pela equipe neste documento e precisam ser confirmados com a direção.',
]

def lista_ids(prefixo, nums):
    return ', '.join(f'{prefixo}-{n:03d}' for n in nums)

IV2 = [
    ['Must have (obrigatório)', 'RF-001 a RF-008, RF-010 a RF-015, RF-017 a RF-023, RF-026, RF-027, RF-030, RF-031, RF-034, RF-035, RF-036; RNF-001 a RNF-012, RNF-019 a RNF-025, RNF-029, RNF-036', 'São os requisitos marcados como Essenciais em docs/requisitos.md e os critérios de aceitação 1 e 2. Sem eles o sistema não substitui o papel (não registra, não mostra o que venceu, não guarda o histórico) ou não pode receber dado real (sem senha protegida, auditoria, minimização e HTTPS). RNF-020 a RNF-025 são impostos pelas disciplinas e pela falta de orçamento.'],
    ['Should have (desejável)', 'RF-009, RF-016, RF-024, RF-025, RF-028, RF-029, RF-032, RF-033, RF-037, RF-038, RF-040; RNF-013 a RNF-018, RNF-026 a RNF-028, RNF-030 a RNF-035, RNF-037', 'Marcados como Importantes ou formalizados a partir de decisões da equipe. Agregam valor (editar, retificar, buscar, avisar, imprimir) ou qualidade, mas o sistema funciona sem eles por um tempo. Quase todos já foram implementados porque o servidor andou mais rápido que o previsto em novembro.'],
    ['Could have (poderia ter)', 'RF-039', 'Desejável em docs/requisitos.md: os indicadores consolidados ajudam a direção, mas o painel e as listas já mostram as informações.'],
    ['Won’t have (não terá nesta versão)', 'RF-041 e os itens da Sala de Espera (Volere 26)', 'Custo (WhatsApp), dependência de decisão da instituição (formato do relatório, destino do encaminhamento) ou complexidade incompatível com o prazo (offline, anexos).'],
]

IV3 = [
    'Conflito 1: visibilidade dos registros. A equipe propôs acesso restrito (cada profissional vê só quem acompanha), seguindo o princípio da necessidade da LGPD (RNF-001 na forma original e RF-005). A direção queria que todos os profissionais vissem tudo. Negociação: a equipe apresentou as duas alternativas em pergunta fechada; a direção, que responde pelos dados, escolheu o acesso aberto. Consenso: acesso aberto a toda conta ativa, com auditoria de todas as operações com dados de assistidos, inclusive leitura, como principal controle (RNF-003); a regra restritiva fica no código, desligada, para o caso de a direção mudar de ideia.',
    'Conflito 2: avisos por WhatsApp (N-10) e orçamento zero. A API oficial é paga e exige aprovação. Consenso: aviso dentro do sistema ao entrar (RF-040), sem dado de saúde; e-mail como desejável (RF-041, adiado).',
    'Conflito 3: duas necessidades e um semestre. A direção pediu também o controle de estoque (N-16). Consenso: a direção priorizou as demandas; estoque ficou como trabalho futuro.',
    'Conflito 4: dados do assistido e minimização. O cadastro precisa identificar a pessoa, e a LGPD pede o mínimo de dados. Consenso provisório: só o nome de tratamento até a instituição definir os campos (Q-01).',
]

# Parte VI
BACKLOG = [
    ['PB-01', 'Como profissional, quero entrar com e-mail e senha e ter a sessão encerrada ao sair ou depois de 30 minutos, para que ninguém use minha conta no computador compartilhado', 'RF-001, RF-002, RNF-002, RNF-005, RNF-034', 'Must', 'Card 14 (sem checklist registrado)', '5', 'Miguel Vaz de Souza'],
    ['PB-02', 'Como direção, quero que cada perfil veja só as funções permitidas, para proteger as funções administrativas', 'RF-003, RNF-001', 'Must', 'Card 15', '5', 'Miguel Vaz de Souza'],
    ['PB-03', 'Como direção, quero cadastrar, editar e desativar usuários, para controlar quem entra', 'RF-004', 'Must', 'Card 23', '5', 'Miguel Vaz de Souza'],
    ['PB-04', 'Como profissional, quero registrar a reunião do meu setor com os participantes, para ligar as demandas à origem', 'RF-006 a RF-009', 'Must', 'Card 18', '5', 'Miguel Vaz de Souza'],
    ['PB-05', 'Como profissional, quero registrar a demanda que saiu da reunião, com responsável e prazo, para que ela não seja esquecida', 'RF-010, RF-011', 'Must', 'Card 19', '5', 'Miguel Vaz de Souza'],
    ['PB-06', 'Como responsável, quero mudar o estado, anotar e trocar o responsável, com histórico, para registrar o andamento', 'RF-012 a RF-017, RNF-019', 'Must', 'Card 19', '5', 'Miguel Vaz de Souza'],
    ['PB-07', 'Como direção, quero ver num painel o que está em aberto e o que venceu, para cobrar quem precisa', 'RF-030, RF-033, RF-039, RNF-030', 'Must', 'Card 19', '5', 'Miguel Vaz de Souza'],
    ['PB-08', 'Como profissional, quero buscar e filtrar demandas antigas e ver as minhas, para retomar o histórico', 'RF-031, RF-032, RF-034', 'Must', 'Card 19', '5', 'Miguel Vaz de Souza'],
    ['PB-09', 'Como profissional, quero cadastrar o assistido e ver a ficha dele, para saber o que já foi feito', 'RF-018 a RF-020, RNF-008', 'Must', 'Card 20', '5', 'Miguel Vaz de Souza'],
    ['PB-10', 'Como profissional, quero lançar e retificar evoluções sem apagar, para manter o acompanhamento confiável', 'RF-005, RF-021 a RF-026, RNF-019', 'Must', 'Card 21 e card #54 (model)', '5', 'Miguel Vaz de Souza'],
    ['PB-11', 'Como profissional, quero registrar encaminhamentos e o desfecho, para acompanhar a rede', 'RF-027 a RF-029, RNF-019', 'Must', 'Card 22 e card #55 (model)', '5', 'Miguel Vaz de Souza'],
    ['PB-12', 'Como direção, quero emitir relatórios do período e do assistido, para acompanhar o trabalho', 'RF-035 a RF-039', 'Must', 'Card 24', '5', 'Miguel Vaz de Souza'],
    ['PB-13', 'Como direção, quero saber quem consultou ou alterou dados dos assistidos, para responder pelos dados', 'RNF-003, RF-038', 'Must', 'Card 17', '5', 'Miguel Vaz de Souza'],
    ['PB-14', 'Como profissional, quero ser avisado ao entrar das demandas vencidas ou perto do prazo', 'RF-040', 'Should', 'Card 25', '5', 'Miguel Vaz de Souza'],
    ['PB-15', 'Como equipe, quero erros sempre em português e no mesmo formato, para o cliente tratar todos igual', 'RNF-014, RNF-037', 'Should', 'Card 16', '5', 'Miguel Vaz de Souza'],
    ['PB-16', 'Como equipe, quero o servidor Flask em camadas, com testes automatizados e banco local', 'RNF-020, RNF-022, RNF-024', 'Must', '3 cartões: 6, 4 e 4 itens de checklist', '3', 'Miguel Vaz de Souza'],
    ['PB-17', 'Como equipe, quero o contrato da API definido antes das telas, para as frentes trabalharem em paralelo', 'RNF-023, RNF-037', 'Must', '5 itens (4 concluídos em 22/10)', '3 e 4', 'Miguel Vaz de Souza'],
    ['PB-18', 'Como equipe, quero o minimundo, o DER e o modelo relacional, para estruturar os dados', 'RNF-022', 'Must', 'Cartões de 3, 7 e 10 itens', '2 a 5', 'Henry Claro'],
    ['PB-19', 'Como equipe, quero os scripts SQL de criação, carga e consultas de demonstração', 'RNF-022', 'Should', 'Sem checklist registrado (PR #8)', '5', 'Henry Claro (frente de banco de dados)'],
    ['PB-20', 'Como equipe de interface, quero personas, cenários, arquitetura da informação e fluxos, para basear as telas no usuário', 'RNF-011, RNF-013', 'Must', 'Cartões de 5, 6 e 4 itens', '3 a 5', 'Inácio Fontes'],
    ['PB-21', 'Como equipe, quero um protótipo navegável para os testes de usabilidade', 'RNF-011, RNF-012', 'Must', 'Cartão do Figma (2 itens) e protótipo clicável (PR #14)', '3 a 5', 'Inácio Fontes e Gabriel Borba'],
    ['PB-22', 'Como profissional, quero as telas de entrar, painel e demandas no navegador', 'RF-001, RF-010 a RF-017, RF-030 a RF-034, RNF-012, RNF-016, RNF-021', 'Must', 'Cartões de 4, 5 e 4 itens (PR #15)', '5', 'Gabriel Borba (frente de front-end)'],
    ['PB-23', 'Como profissional e direção, quero as telas de reuniões, assistidos, evoluções, encaminhamentos, usuários, relatórios e auditoria', 'RF-004, RF-006 a RF-009, RF-018 a RF-029, RF-035 a RF-038', 'Must', 'Sem checklist registrado (PR #16)', '5', 'Gabriel Borba (frente de front-end)'],
    ['PB-24', 'Como equipe, quero publicar o sistema com HTTPS e sem custo', 'RNF-004, RNF-025', 'Must', 'Sem checklist registrado (PRs #9 e #10)', '5', 'Miguel Vaz de Souza'],
    ['PB-25', 'Como equipe, quero os testes rodando em todo PR', 'RNF-024, RNF-032', 'Should', 'Sem checklist registrado (PR #19)', '5', 'Miguel Vaz de Souza'],
    ['PB-26', 'Como equipe de interface, quero aplicar os 8 testes de usabilidade e relatar os resultados', 'RNF-011, RNF-013, RNF-029, RNF-031, RNF-036', 'Must', 'Plano pronto (PR #14); execução pendente', '5', 'Inácio Fontes'],
    ['PB-27', 'Como direção, quero receber por e-mail o aviso de demanda vencida', 'RF-041', 'Won’t', '—', '—', '—'],
    ['PB-28', 'Como direção, quero receber a orientação sobre a LGPD, o procedimento de cópia de segurança e o manual de uso, para operar o sistema com dados reais', 'RNF-009, RNF-010, RNF-026', 'Must', 'Não registrado no quadro (pendente)', '5', 'A definir pela equipe'],
    ['PB-29', 'Como profissional, quero uma interface com a identidade do CRIE, sóbria, acessível e que funcione no celular', 'RNF-015, RNF-027, RNF-028, RNF-033, RNF-035', 'Should', 'Sem checklist registrado (PR #18)', '5', 'Gabriel Borba (frente de front-end)'],
    ['PB-30', 'Como equipe, quero garantir que nenhum dado real ou segredo entre no repositório', 'RNF-006, RNF-007', 'Must', 'Verificação de segredos (ciclo 3) e carga fictícia (PR #12)', '3 e 5', 'Miguel Vaz de Souza'],
    ['PB-31', 'Como direção, quero respostas rápidas mesmo com dez pessoas usando ao mesmo tempo', 'RNF-017, RNF-018', 'Should', 'Medição pendente', '5', 'Miguel Vaz de Souza'],
]
BACKLOG_NOTA = 'A equipe não estimou em pontos de história. O tamanho de cada cartão foi controlado pelo número de itens do checklist no Trello, mostrado na coluna Estimativa quando está registrado no relatório v3. Os cards 14 a 28 do back-end são os do PR #12. O responsável é o dono da frente (divisão de papéis); a autoria dos pull requests está em VI.6 e no Anexo C.'

CICLOS = [
    ['1', 'Até 03/09/2026 (ET1)', 'Contato com o CRIE, levantamento, requisitos 1.0 e 2.0, quadro Kanban', 'Requisitos (sem PB de código)', 'Sim', 'A escuta corrigiu três hipóteses; perguntas fechadas e numeradas funcionam melhor (relatório v1)'],
    ['2', '04/09 a 01/10/2026 (ET2)', 'Minimundo, DER, persona P1, estrutura do React, backlog', 'PB-18, PB-20 e PB-22 (em parte)', 'Parcial', 'O modelo relacional não fechou e virou o gargalo; os PRs 1 a 3 só foram integrados em 13/10 (relatório v3)'],
    ['3', '02/10 a 22/10/2026 (ET3)', 'Servidor Flask, testes, specs 01 a 04, contrato da API, personas', 'PB-16, PB-17, PB-20', 'Parcial', 'Colunas de teste do quadro não foram usadas; cartões de código foram direto para Concluído. Correção: o cartão só fecha depois da revisão do PR (relatório v3, seção 3.1.5)'],
    ['4', '23/10 a 05/11/2026 (ET4)', 'API e telas integradas; testes de usabilidade em andamento (planejado)', 'PB-01 a PB-15', 'Parcial (PR #5 integrado em 05/11; a API veio no ciclo 5)', 'Retrospectiva não registrada'],
    ['5', '06/11 a 26/11/2026 (EXPOEX em 18/11, ET5 em 26/11)', 'API completa, publicação, telas, material de IHC, CI', 'PB-01 a PB-15, PB-19, PB-21 a PB-25', 'Parcial (testes de usabilidade e aceitação pendentes)', 'Retrospectiva não registrada. Pelo histórico, 156 dos 179 commits sem merge são de novembro'],
]

CRONOGRAMA = [
    ['Especificação aprovada pelo cliente', '01/10/2026 (ET2)', 'Sem aprovação formal; decisões da direção registradas entre agosto e setembro de 2026', 'Parte II validada'],
    ['Protótipo navegável', '22/10/2026 (ET3)', '18/11/2026 (protótipo clicável, PR #14); validação pendente', 'Telas principais prontas'],
    ['Sistema publicado', '05/11/2026 (ET4)', '17/11/2026 (PR #10; API completa no PR #13)', 'Endereço https respondendo'],
    ['Versão testada', '05/11/2026 (ET4)', '23/11/2026 (CI do PR #19: 587 aprovados)', 'Casos Must executados'],
    ['Entrega final', '25/11/2026 (ES) e 26/11/2026 (ET5)', 'A registrar', 'Documento, sistema e apresentação'],
]

VI4 = [
    'O andamento foi acompanhado no quadro Kanban “Equipe Cortex” no Trello, com as colunas Backlog, A Fazer, Fazendo, Esperando Teste, Testando e Concluído, etiquetas por frente (Banco de Dados, UI/UX, Backend, Frontend e Comunidade Externa) e checklist em cada cartão. O progresso foi medido pela proporção de itens concluídos: 40 de 92 itens no fim do 3º ciclo (relatório v3, seção 4.3). A cada versão do relatório, a equipe revisou o quadro, registrou as movimentações e apontou inconsistências entre cartões e decisões (relatório v3, Quadros 9, 10 e 12). Não foi usado gráfico de burndown.',
    'No GitHub, cada pull request descreve o que entra, como foi verificado e o que ficou em aberto; docs/estado-do-projeto.md mantém o mapa do sistema; e, a partir do PR #19, o CI mostra em cada PR se os testes passaram. Os riscos foram acompanhados no relatório (seção 4.4) e estão em Volere 23.',
    'Ponto fraco: o estado do quadro depois de 22/10/2026 não está registrado no repositório, e as capturas mais recentes são as do relatório v3. Anexar uma captura atual do quadro é pendência da equipe (VIII.6).',
]

FERRAMENTAS = [
    'Não padronizado; o repositório não registra o editor usado por cada integrante',
    'Git e GitHub (organização Team-Cortex): monorepo, uma branch por funcionalidade, PR para a development, main como produção',
    'Trello, quadro “Equipe Cortex”: Kanban com checklists e etiquetas por frente',
    'draw.io (DER_CRIE_v2.drawio); SVG gerado para os diagramas deste documento (entregas/engenharia-de-software/diagramas)',
    'Figma (telas iniciais) e protótipo clicável em HTML (docs/ihc/prototipo)',
    'pytest com o test client do Flask e SQLite em memória (back-end); node:test (front-end)',
    'pip (requirements.txt), npm (package-lock.json), Vite, Docker Compose (PostgreSQL local), Alembic (Flask-Migrate)',
    'GitHub Actions, workflow “Testes” (PR #19, em revisão); Vercel publica a cada merge na main',
    'ESLint no front-end (sem erro no CI de 23/11/2026); verificação de segredos (backend/scripts/check-segredo.mjs). O back-end não tem linter configurado; SonarQube não foi usado',
]

VI6 = [
    'https://github.com/Team-Cortex/sistema-demandas-crie (organização criada para a equipe, para que todos tenham o mesmo controle do repositório depois do semestre)',
    'main = produção (a Vercel publica a cada merge); development = integração; uma branch por funcionalidade ou frente (henry/modelagem, feature/estrutura-inicial-react, miguel/estrutura-servidor, miguel/cards-backend, ihc/documentos, front/base-telas-prioridade-1, front/telas-prioridade-2, front/visual-sem-enfeite, ci/testes-e-primeira-direcao), integradas por pull request com merge commit, que preserva os commits.',
    'Conventional Commits em português, no formato tipo(escopo): efeito, um commit por ação. Exemplos reais: “feat(acesso): cria a primeira direção por comando administrativo”, “fix(servidor): converte a URL do banco para o driver psycopg 3”, “docs(ihc): alinha telas e cenários ao visual sem selos”. Contagem dos 179 commits sem merge da development: 81 feat, 43 docs, 20 fix, 9 chore, 8 test, 7 refactor, 4 style e 7 iniciais fora do padrão.',
    '19 pull requests até 23/11/2026 (18 integrados e 1 aberto, o #19). Na development, 194 commits entre 27/08 e 23/11/2026. Commits por autor (git shortlog, pelo e-mail): Miguel Vaz de Souza 187, Vinícius Marrocos 3, Gabriel Borba 1, Henry Claro 1 e 2 da conta de automação openbotgit; Inácio Fontes não tem commits. PRs abertos: 14 pela conta miguelvzs, 1 por HenryClaro (#1), 1 por Gabriel-Ribeiro-Borba (#2), 1 por fmvini (#3) e 2 pela conta de automação (#10 e #13). Nenhum PR tem revisão formal aprovada no GitHub. Lista completa no Anexo C.',
]

# Parte VII
VII1 = [
    ['Funcionalidade', 'Alta', 'RF-001 a RF-040', 'Percentual de casos de teste aprovados (100% dos automatizados no CI de 23/11/2026); critérios de aceitação 1 a 7 com a direção (pendente)'],
    ['Confiabilidade', 'Alta', 'RNF-010, RNF-016, RNF-019, RNF-003', 'Nenhuma exclusão possível (CT-50, CT-91, CB-06, CB-07); restauração de cópia testada (pendente); erros 5xx em produção (não medido)'],
    ['Usabilidade', 'Alta', 'RNF-011 a RNF-015, RNF-029, RNF-036', 'Taxa de conclusão sem ajuda, tempo da tarefa T2 e notas Q1 a Q8 nos 8 testes (pendente)'],
    ['Eficiência de desempenho', 'Média', 'RNF-017, RNF-018', 'Tempo de resposta até 3 s com 10 usuários (não medido); número de consultas SQL constante (CB-19)'],
    ['Manutenibilidade', 'Alta', 'RNF-020 a RNF-024, RNF-026, RNF-037', 'Camadas separadas; specs antes do código; 587 testes; README de instalação; lint sem erro'],
    ['Portabilidade', 'Média', 'RNF-031, RNF-033, RNF-025, RS-05', 'Funciona em 360 px e 1280 px (CT-100); só navegador; publicação reproduzível em outro provedor'],
    ['Segurança', 'Alta', 'RNF-001 a RNF-010, RNF-034', 'Testes de 401 e 403, hash, auditoria e limite de tentativas; HTTPS em produção (CT-77); nenhum dado real fora da instituição'],
    ['Compatibilidade', 'Baixa', 'RNF-023, RNF-037', 'Sem integração com outros sistemas nesta versão; contrato da API documentado e conferido (CT-93)'],
]
VII2 = [
    ['1. Segurança', 'O sistema guarda dados de saúde de pessoas com deficiência, muitas menores de idade, e o acesso é aberto a todo profissional', 'Exposição de dados sensíveis, quebra da LGPD e perda da confiança das famílias e da instituição'],
    ['2. Usabilidade', 'Os profissionais têm pouca familiaridade com tecnologia e a direção pediu um sistema “bem simples”', 'O sistema é abandonado e o papel continua, ou o registro fica incompleto e o painel deixa de ser confiável'],
    ['3. Confiabilidade', 'O valor do sistema é o histórico: o que foi feito, por quem e quando', 'Demanda ou evolução perdida, histórico alterado sem rastro; o problema das demandas esquecidas volta'],
]
VII3 = [
    ['Sim', 'Ver Parte V: 587 testes automatizados no back-end e 4 no front-end, executados no CI; verificação manual no navegador (PR #18)', 'Desenvolvimento (outubro e novembro de 2026)'],
    ['Parcial', 'Todo código entrou por pull request com descrição do que foi verificado e do que ficou de fora; specs revisadas antes do código (“se a spec divergir do código, a spec vence”). Porém nenhum PR tem revisão formal aprovada por outro integrante no GitHub', 'A cada PR'],
    ['Sim', 'Conventional Commits em português; ESLint; specs com mensagens e testes; contrato da API; README de instalação; guia de interface em docs/ihc/telas.md', 'Todo o projeto'],
    ['Sim', 'Ver VI.6: Git com branches por funcionalidade, merge commit, migrações Alembic versionadas, package-lock.json, variáveis de ambiente fora do repositório, publicação automática pela main', 'Todo o projeto'],
    ['Parcial', 'ESLint no front-end sem erro no CI de 23/11/2026; verificação de segredos no CI (213 arquivos, nenhum achado). No back-end não há linter nem ferramenta de análise de vulnerabilidades; SonarQube não foi usado', 'Desenvolvimento e CI'],
]
VII4 = [
    '1. A spec da funcionalidade existe e lista os testes que a provam (relatório v3, seção 3.1.1).',
    '2. O código segue a spec; se divergir, a spec vence e o código é corrigido.',
    '3. Os testes da spec passam e o CI do PR fica verde: back-end, front-end, lint, build e verificação de segredos (a partir do PR #19).',
    '4. docs/contrato-api.md e docs/estado-do-projeto.md são atualizados no mesmo PR quando uma rota ou um fato muda.',
    '5. O PR descreve o que foi verificado e o que ficou de fora e é revisado por outro integrante antes do merge (regra do relatório v3, ainda sem revisão registrada no GitHub).',
    '6. A integração é feita por merge commit na development; a main só recebe o que já está na development.',
    '7. Só dados fictícios no código, nos testes e nas telas.',
    '8. A matriz de rastreabilidade (IV.4) é atualizada.',
]

# Parte VIII
VIII1 = [
    'Foi entregue o que o projeto prometia no lado do servidor e da interface: a API cobre as specs 01 a 09 (acesso, demandas, assistidos, reuniões, auditoria, evoluções, encaminhamentos, relatórios e aviso de prazo), com 587 testes aprovados no CI; o front-end React tem todas as telas, de entrar à auditoria; o material de IHC (personas, cenários, arquitetura da informação, fluxos, telas, plano de testes e protótipo clicável) está no repositório; e o sistema está publicado com HTTPS, sem custo. As salvaguardas de dados que a equipe propôs estão no código: senha só como hash, auditoria inclusive de leitura, cadastro mínimo do assistido, nenhuma exclusão e só dados fictícios.',
    'Não foi entregue o que depende de pessoas fora da equipe: os 8 testes de usabilidade, a validação com a direção pelos critérios de aceitação, as respostas às questões abertas (Q-01 a Q-07) e a orientação sobre a LGPD. Também faltam o manual de uso, o procedimento de cópia de segurança, a primeira conta da direção em produção (PR #19), a expiração por inatividade (Q-15) e o aviso por e-mail (RF-041, adiado).',
    'Próximos passos: integrar o PR #19 e criar a conta da direção; aplicar os testes de usabilidade e corrigir o que aparecer; levar à direção o bloco de perguntas fechadas das questões abertas; escrever o manual, a orientação sobre a LGPD e a rotina de cópia; e combinar com o CRIE quem mantém o sistema depois do semestre (Q-08).',
]
VIII2 = [
    'Escutar antes de propor. A primeira ideia da equipe estava errada em três pontos estruturais, e só a escuta continuada mostrou isso. Num próximo projeto, a equipe começaria com uma observação ou entrevista do fluxo real antes de modelar.',
    'A pergunta define a resposta. Perguntas abertas tiveram respostas genéricas; alternativas fechadas e numeradas tiveram respostas imediatas.',
    'Escrever o critério de ajuste junto com o requisito. A versão 2.0 dos requisitos não tinha critérios, e só neste documento cada requisito ganhou um. Com o critério desde o início, os testes teriam saído direto dos requisitos.',
    'Dependência entre frentes custa caro. O modelo relacional atrasou e travou o back-end. Adiantar a estrutura, as specs e o contrato reduziu o dano.',
    'A revisão precisa acompanhar a produção. Pull requests ficaram dias sem integração e nenhum teve revisão formal registrada. Faríamos revisões curtas e frequentes, em dupla, desde setembro.',
    'O trabalho ficou concentrado no fim e em poucas pessoas: 156 dos 179 commits são de novembro, quase todos de uma conta. Distribuir o código mais cedo diminui o risco de o sistema depender de uma pessoa só.',
    'Validação com usuários tem que entrar no calendário no começo. Os testes de usabilidade dependiam da agenda do CRIE e ficaram para o fim, que é a pior hora para descobrir problemas.',
]
VIII3 = [
    ['Vinícius Marrocos', 'Gerente de projeto e analista de requisitos: documento de requisitos, plano de projeto, divisão de papéis, quadro Kanban e planejamento de V&V', 'Partes I, II, IV e VII', '3 commits (31/08/2026, documentos de papéis); PR #3 (conta fmvini); cartões de escopo e formulário de interesse no Trello'],
    ['Henry Claro', 'Analista de banco de dados: minimundo, DER conceitual e modelagem; frente de Banco de Dados 1', 'Volere 7', 'PR #1 (henry/modelagem, 1 commit); cartões do minimundo (3 de 3) e do DER (7 de 7) no Trello'],
    ['Inácio Fontes', 'Analista de interface: personas (concluídas em 08/10/2026), telas iniciais no Figma e frente de IHC (os documentos de docs/ihc se identificam como “Frente de IHC”)', 'Parte III; Volere 2e, 10 e 11', 'Cartão das personas (5 de 5) e anexos do protótipo no Trello; sem commits no repositório; documentos de IHC integrados pelo PR #14 (conta miguelvzs)'],
    ['Miguel Vaz de Souza', 'Desenvolvedor back-end: specs 01 a 09, models, rotas, auditoria e testes; publicação na Vercel e no Neon; CI; integração do front-end e do material de IHC no repositório', 'Volere 12 a 15; Partes V e VI', '187 commits; PRs #4 a #9, #11, #12 e #14 a #19'],
    ['Gabriel Borba', 'Desenvolvedor front-end: estrutura inicial do projeto React (Vite, páginas, componentes, cliente de API e rotas); apoio à prototipação', 'Parte III (telas); Volere 13 e 14', 'PR #2 (1 commit); cartão “Montar a estrutura inicial do projeto React” (4 de 4)'],
]
VIII3_NOTA = 'Esta tabela foi montada com o que está registrado no repositório, no GitHub e nos relatórios. Trabalho feito fora do repositório (contato com o CRIE, Figma, Trello, banner da EXPOEX, redação dos relatórios) não aparece em commits. Cada integrante deve revisar a própria linha antes da entrega (pendência em VIII.6).'

REFERENCIAS_EXTRA = [
    'ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. ABNT NBR ISO/IEC 25010: engenharia de sistemas e software: requisitos e avaliação da qualidade de sistemas e software (SQuaRE): modelos de qualidade de sistemas e software. Rio de Janeiro: ABNT, 2011.',
    'BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018.',
    'EQUIPE CORTEX. Relatório de projeto: versões 1 a 3. Bragança Paulista: IFSP, 2026. Disponível em: https://github.com/Team-Cortex/sistema-demandas-crie/tree/main/docs/relatorios. Acesso em: 23 nov. 2026.',
    'EQUIPE CORTEX. Sistema de Demandas do CRIE: repositório do projeto. GitHub, 2026. Disponível em: https://github.com/Team-Cortex/sistema-demandas-crie. Acesso em: 23 nov. 2026.',
    'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO. Documento de especificação de projeto integrado de extensão: BRAEXT2. Bragança Paulista: IFSP, 2026.',
    'INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. ISO 9241-210: ergonomics of human-system interaction: part 210: human-centred design for interactive systems. Geneva: ISO, 2019.',
    'KARNER, Gustav. Resource estimation for Objectory projects. Stockholm: Objective Systems SF AB, 1993.',
    'ROSENFELD, Louis; MORVILLE, Peter; ARANGO, Jorge. Information architecture: for the web and beyond. 4. ed. Sebastopol: O’Reilly, 2015.',
    'W3C. Web Content Accessibility Guidelines (WCAG) 2.2. 2023. Disponível em: https://www.w3.org/TR/WCAG22/. Acesso em: 23 nov. 2026.',
]

ANEXOS = [
    'Formulário de levantamento respondido pela direção e registro das interações: Anexos B e C do relatório v3 (docs/relatorios/Relatorio_de_Projeto_v3.pdf), não reproduzidos aqui',
    'Protótipo clicável em docs/ihc/prototipo/index.html; capturas das telas em tamanho original em entregas/engenharia-de-software/telas',
    'Lista de pull requests no Quadro C.1, abaixo; capturas do quadro Kanban nas Figuras 2 e 3 do relatório v3; execução do CI em https://github.com/Team-Cortex/sistema-demandas-crie/actions/runs/45199075617',
    'Diagramas de contexto, casos de uso e navegação em entregas/engenharia-de-software/diagramas (SVG e PNG); DER em docs/modelagem/DER_CRIE_v2.png',
    'Não se aplica a este projeto, porque não houve reuniões presenciais com o CRIE: a interação foi por mensagens e áudios, resumida no relatório v3, seção 2. As reuniões da equipe não tiveram ata registrada',
]

PRS = [
    ['#1', 'HenryClaro', 'Minimundo e DER conceitual', '13/10/2026'],
    ['#2', 'Gabriel-Ribeiro-Borba', 'Estrutura inicial do projeto React', '13/10/2026'],
    ['#3', 'fmvini', 'Minimundo e DER conceitual (development para main)', '13/10/2026'],
    ['#4', 'miguelvzs', 'Atualização da development a partir da main', '13/10/2026'],
    ['#5', 'miguelvzs', 'Estrutura inicial do servidor Flask e specs do back-end', '05/11/2026'],
    ['#6', 'miguelvzs', 'Relatórios de projeto v1 a v3', '22/10/2026'],
    ['#7', 'miguelvzs', 'Relatórios na main', '22/10/2026'],
    ['#8', 'miguelvzs', 'BD1: modelo relacional, scripts, 17 consultas e seminário', '17/11/2026'],
    ['#9', 'miguelvzs', 'Deploy na Vercel com banco no Neon', '17/11/2026'],
    ['#10', 'openbotgit (automação)', 'Development para a main e publicação em produção', '17/11/2026'],
    ['#11', 'miguelvzs', 'BD1: documento no padrão ABNT', '17/11/2026'],
    ['#12', 'miguelvzs', 'Cards do back-end: autenticação, perfis, auditoria e API completa', '17/11/2026'],
    ['#13', 'openbotgit (automação)', 'Cards do back-end e documento de BD1 na main', '17/11/2026'],
    ['#14', 'miguelvzs', 'IHC: cenários, arquitetura da informação, fluxos, telas e plano de testes', '18/11/2026'],
    ['#15', 'miguelvzs', 'Front-end: cliente da API, layout base e telas de prioridade 1', '18/11/2026'],
    ['#16', 'miguelvzs', 'Front-end: telas de prioridade 2 e 3', '18/11/2026'],
    ['#17', 'miguelvzs', 'Front-end e material de IHC em produção', '18/11/2026'],
    ['#18', 'miguelvzs', 'Interface sem ícones e selos decorativos', '23/11/2026'],
    ['#19', 'miguelvzs', 'CI de testes e criação da primeira direção em produção', 'Aberto em 23/11/2026'],
]

CHECKLIST = [
    '☐ Parcial: falta o prontuário de cada integrante na capa',
    '☑ Sim (I.3)',
    '☑ Sim, com as evidências nos anexos do relatório v3 (Anexo A)',
    '☑ Sim: seções 1 a 27 preenchidas; as que não se aplicam estão justificadas',
    '☑ Sim: Figuras 1 a 4',
    '☑ Sim: cada RF e RNF tem critério de ajuste; metas propostas pela equipe a confirmar com a direção',
    '☑ Sim: 49 cartões (28 RF e 21 RNF Must)',
    '☐ Parcial: protótipos inseridos e ligados aos requisitos; validação com usuários pendente (III.6)',
    '☑ Sim (IV.2 e IV.4)',
    '☐ Parcial: casos automatizados executados no CI de 23/11/2026; 13 casos manuais pendentes (usabilidade, aceitação, desempenho, cópia de segurança, orientação sobre a LGPD)',
    '☑ Sim (VI.1, VI.2 e VI.6); falta anexar captura atual do quadro Trello',
    '☑ Sim (Parte VII)',
    '☑ Sim: sumário atualizado na geração do arquivo e blocos “Conteúdo” removidos',
]
