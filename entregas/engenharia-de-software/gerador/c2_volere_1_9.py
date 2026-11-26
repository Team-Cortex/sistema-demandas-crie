# Volere 1 a 9
V1A = [
    'O CRIE foi fundado em 1991 em Extrema (MG) por cidadãos da cidade, diante da falta de atendimento especializado a pessoas com deficiência. Filiou-se à Federação das APAEs em 2005 e, em 2016, obteve autorização para o seu Centro de Atendimento Educacional Especializado e o Certificado de Entidade Beneficente de Assistência Social. Atende pessoas com deficiência e suas famílias com atendimento educacional especializado, saúde, assistência social, oficinas e programas para famílias.',
    'O fato que motivou o projeto: nas reuniões semanais de cada setor, a equipe discute casos que não consegue resolver sozinha, define as ações (encaminhar à psicóloga, convocar a família, verificar o referenciamento no CRAS), escolhe um responsável pela articulação e, no fim, registra o desfecho. Tudo isso fica em papel.',
    'Com o produto pronto, a equipe registra a demanda logo depois da reunião, atualiza o andamento e anota o que fez, registra os encaminhamentos à rede e o retorno, lança evoluções na ficha da pessoa atendida e, ao entrar, vê o que está vencido. A direção acompanha tudo pelo painel, emite relatórios e confere na auditoria quem consultou os dados.',
]

V1B = [
    ['Nenhuma demanda esquecida', 'Providências de garantia de direitos não ficam paradas sem que alguém perceba', 'Todas as demandas vencidas aparecem no painel, numa única tela (critério de aceitação 3). A direção acompanha o número de vencidas semana a semana; o valor de referência será o do primeiro mês de uso, porque o papel não permite medir hoje.'],
    ['Retomar o histórico rapidamente', 'Resposta à família e à rede sem procurar em papéis', 'Localizar uma demanda antiga e ler o histórico completo em menos de 1 minuto (critério de aceitação 2; tarefa T2 do teste de usabilidade).'],
    ['Proteger os dados das pessoas atendidas', 'Cumprir a LGPD e manter a confiança das famílias', '100% das operações com dados de assistidos auditadas com autor, data e hora; nenhum dado real fora da instituição; nenhuma conta inativa ou sem login acessa evoluções (critério de aceitação 6).'],
    ['Operar sem custo', 'A instituição não tem orçamento para o sistema', 'Custo mensal de hospedagem e banco: R$ 0,00.'],
]

V2A = 'CRIE, Centro de Integração Especial (APAE de Extrema-MG), representado pela diretora da instituição, interlocutora da equipe desde o primeiro contato. A direção respondeu ao levantamento, tomou as decisões de escopo (prioridade das demandas sobre o estoque; acesso aberto com auditoria) e tem a palavra final na aceitação. A parceria foi formalizada pelo Formulário de Manifestação de Interesse em Participação em Projeto de Extensão do IFSP, assinado pela direção (relatório v3, seção 2.5).'

V2B = 'Cliente e consumidor são a mesma organização: a direção do CRIE decide adotar o sistema. Não há compra; o sistema é entregue sem custo, como projeto de extensão do IFSP.'

V2C = [
    ['Profissionais do CRIE (assistente social, equipe pedagógica, saúde, serviço de convivência)', 'Rotina das reuniões e do acompanhamento; termos usados no dia a dia', 'Alto (são os usuários)', 'Alta'],
    ['Pessoas atendidas e suas famílias', 'Titulares dos dados, muitas menores de idade; não usam o sistema', 'Indireto', 'Alta (LGPD)'],
    ['Rede de serviços públicos (CRAS, CAPSi, UBS, escolas, conselhos)', 'Destino dos encaminhamentos e origem dos retornos', 'Baixo', 'Baixa'],
    ['Prefeitura de Extrema', 'Recebe o relatório de atendimento feito por cada profissional (fora do escopo)', 'Nenhum', 'Baixa'],
    ['Professores do IFSP (Prof. Luiz Gustavo Diniz de Oliveira Véras, orientador da extensão; Profa. Marina, Engenharia de Software; professores de IHC, BD1, POO e Front End)', 'Critérios de avaliação e tecnologias obrigatórias', 'Médio', 'Alta (definem as restrições de solução)'],
    ['Equipe Cortex', 'Constrói e mantém o sistema até o fim do semestre', 'Alto', 'Média'],
    ['Público e avaliadores da Mostra de Extensão (EXPOEX, 18/11/2026)', 'Veem o sistema só com dados fictícios', 'Baixo', 'Baixa'],
]

V2D = [
    ['Direção', 'Acompanhar todas as demandas, cadastrar usuários, emitir relatórios, consultar a auditoria', 'Mestre (conduz as reuniões dos três setores)', 'Maior que a dos profissionais, segundo o relatório v3 (seção 3.2.2); nível não medido', 'Quer ver tudo numa tela só; decide o acesso aos dados'],
    ['Assistente social', 'Registrar e atualizar demandas, evoluções e encaminhamentos', 'Experiente: executa o trabalho hoje', 'Iniciante: baixa familiaridade, informada pela direção', 'Computador compartilhado, logo depois da reunião ou entre atendimentos'],
    ['Equipe pedagógica', 'Registrar e atualizar demandas e evoluções', 'Experiente: executa o trabalho hoje', 'Iniciante: baixa familiaridade, informada pela direção', 'Mesmo contexto da assistente social'],
]

V2E = [
    ['P1: Júlia Costa (fictícia), diretora do CRIE; idade não registrada', 'Centralizar a gestão das demandas numa tela só, para decidir com agilidade; ver de imediato as demandas em aberto com prazo vencido', 'Perde tempo procurando o histórico de demandas antigas; o papel espalha a informação', 'Painel único com vencidas em destaque (RF-030, RF-033); busca e histórico (RF-031, RF-017)'],
    ['P2: assistente social (nome e dados a transcrever do cartão no Trello, decisão D3)', 'Registrar e atualizar demandas, evoluções e encaminhamentos', 'Baixa familiaridade com tecnologia (relatório v3); demais frustrações a transcrever', 'Registro em um formulário e uma confirmação (RNF-012); linguagem do CRIE (RNF-013)'],
    ['P3: equipe pedagógica (nome e dados a transcrever do cartão no Trello, decisão D3)', 'Registrar e atualizar demandas e evoluções', 'Baixa familiaridade com tecnologia (relatório v3); demais frustrações a transcrever', 'Ver só o que é seu (RF-034); aviso de prazo ao entrar (RF-040)'],
]

V2F = [
    ['Profissionais (assistente social e equipe pedagógica)', 'Chave', 'Fazem o registro do dia a dia; se acharem difícil, o papel continua (RNF-011, critério de aceitação 1)'],
    ['Direção', 'Chave', 'É a cliente, acompanha tudo e decide a aceitação; prevalece nas regras de acesso aos dados'],
    ['Coordenação de setor', 'Secundária', 'Não tem perfil próprio; usa o sistema como profissional até a instituição definir permissões (A4)'],
]

V2G = [
    'Direção: participou do levantamento por formulário, mensagens e áudios entre agosto e setembro de 2026 e tomou as decisões de escopo. Disponibilidade em horário comercial, com preferência por mensagens.',
    'Profissionais: previstos nos 8 testes de usabilidade (docs/ihc/plano-de-testes.md), sessões individuais de 25 a 30 minutos, de preferência presenciais no CRIE. Até 23/11/2026 os testes não aconteceram; a data e os participantes dependem da instituição (decisão D4).',
    'Validação final com a direção, pelos critérios de aceitação de docs/requisitos.md (seção 8): pendente.',
]

V2H = 'Durante o semestre, a própria equipe mantém o sistema: Miguel Vaz de Souza (servidor, banco e publicação) e Gabriel Borba (interface). O CRIE não tem equipe de TI, e depois de 26/11/2026 ninguém está designado (questão Q-08). Quem assumir precisa de: backend/README.md (instalação do zero e variáveis de ambiente), docs/estado-do-projeto.md (mapa do sistema), as specs e o contrato da API, acesso à Vercel e ao Neon, e o comando que cria a primeira conta da direção (PR #19, em revisão).'

V3A = [
    ['RS-01', 'Back-end em Python com Flask, orientado a objetos (RNF-020)', 'Exigência da disciplina de POO (BRAPROB)', 'Servidor em backend/app com classes de domínio e herança de Usuario (Direcao, Profissional, AssistenteSocial, EquipePedagogica); conferido pelos testes de test_usuario.py'],
    ['RS-02', 'Front-end em React, com componentes reutilizáveis (RNF-021)', 'Exigência da disciplina BRADWFR', 'frontend/package.json com React 19; telas em src/pages e componentes em src/components; build sem erro no CI'],
    ['RS-03', 'Banco relacional (RNF-022): PostgreSQL em desenvolvimento e produção', 'Exigência da disciplina BRABCD1', 'Schema criado pelas migrações Alembic, que batem com os models (test_migracoes.py)'],
    ['RS-04', 'Hospedagem sem custo, com HTTPS (RNF-025 e RNF-004)', 'Sem orçamento na instituição e na equipe', 'Produção na Vercel (plano gratuito) com banco no Neon; custo mensal de R$ 0,00'],
    ['RS-05', 'Uso por navegador, sem instalar nada nos computadores do CRIE', 'Computadores compartilhados da instituição', 'Acesso pelo endereço https://sistema-demandas-crie.vercel.app em navegador atual'],
    ['RS-06', 'Só dados fictícios em repositório, testes, protótipos e apresentações (RNF-006 e RNF-007)', 'Dados de saúde de pessoas com deficiência, muitas menores de idade', 'Verificação de segredos no CI sem achados (213 arquivos em 23/11/2026); carga de demonstração só com nomes marcados como fictícios (test_seed.py)'],
]

V3B = 'Computadores de mesa da instituição, compartilhados entre profissionais e usados nas dependências do CRIE, com internet de estabilidade intermitente (informado pela direção). O número de computadores e o sistema operacional não foram levantados (plano de projeto, seção 6.3). O sistema roda na nuvem: o front-end é publicado como site estático e a API Flask como função Python na Vercel; o banco PostgreSQL fica no Neon. O navegador só acessa o endereço publicado.'

V3C = 'Não se aplica a este projeto, porque a única aplicação existente no CRIE, o aplicativo de cadastro de usuários, ficou fora do escopo: ele não foi identificado (QA03) e não há interface de integração conhecida. O sistema não troca dados com outros sistemas.'

V3D = 'PostgreSQL (exigido pela restrição RS-03), Flask 3, Flask-SQLAlchemy, Flask-Migrate (Alembic), Flask-JWT-Extended, Flask-Cors, marshmallow, python-dotenv, psycopg 3 e pytest no servidor (backend/requirements.txt); React 19, React Router 7, Axios, Vite e ESLint no cliente (README.md). Todos gratuitos e de código aberto; as licenças das bibliotecas da interface estão no README.'

V3E = 'Sala de trabalho do CRIE, em computador compartilhado, logo depois das reuniões de setor ou entre atendimentos. A internet instável pode derrubar o envio de um formulário (RNF-016). O profissional pode ser interrompido e deixar a tela aberta; por isso a sessão expira em 30 minutos e o token some quando a aba fecha (RNF-005).'

V3F = [
    ['ET1: relatório v1, quadro Kanban', '03/09/2026', 'Calendário da disciplina de extensão (BRAEXT2)'],
    ['ET2: requisitos, DER, personas', '01/10/2026', 'Calendário BRAEXT2'],
    ['Documentação parcial Volere', '18/10/2026', 'Tarefa da disciplina de Engenharia de Software'],
    ['ET3: servidor estruturado e protótipo', '22/10/2026', 'Calendário BRAEXT2'],
    ['ET4: API e telas integradas', '05/11/2026', 'Calendário BRAEXT2'],
    ['Mostra de Extensão (EXPOEX)', '18/11/2026', 'Calendário BRAEXT2'],
    ['Trabalho final e apresentação de Engenharia de Software', '25/11/2026', 'Fim do semestre letivo'],
    ['ET5: entrega final do sistema', '26/11/2026', 'Calendário BRAEXT2'],
]

V3G = 'R$ 0,00. Nem a instituição nem a equipe têm orçamento (docs/requisitos.md, seção 2.4). Por isso a solução usa só serviços gratuitos (Vercel, Neon, GitHub, Trello) e o envio por WhatsApp foi descartado, porque exige a API oficial paga.'

GLOSSARIO = [
    ['Assistido (pessoa atendida)', 'Pessoa com deficiência atendida pelo CRIE. No sistema, só o nome de tratamento é registrado.'],
    ['Nome de tratamento', 'Nome pelo qual a pessoa é chamada no CRIE. No repositório e nas demonstrações, sempre fictício.'],
    ['Demanda (de articulação)', 'Situação levantada em reunião que a equipe não resolve sozinha e que exige providência, em geral com a rede pública.'],
    ['Reunião de setor', 'Encontro semanal de um dos três setores (pedagógico, saúde, serviço de convivência) em que as demandas nascem.'],
    ['Estado da demanda', 'Aberta, Em andamento, Aguardando terceiros, Concluída ou Cancelada (spec 02).'],
    ['Histórico da demanda', 'Lista, só de inserção, das mudanças de estado, anotações e trocas de responsável, com autor, data e hora.'],
    ['Anotação', 'Texto de acompanhamento gravado no histórico sem mudar o estado.'],
    ['Vencida', 'Demanda com prazo anterior a hoje (fuso do CRIE) que não está concluída nem cancelada.'],
    ['Perto do prazo', 'Demanda em aberto com prazo entre hoje e hoje mais 3 dias (configurável, A10).'],
    ['Evolução', 'Registro do acompanhamento de um assistido feito por um profissional (data, área de atuação, descrição).'],
    ['Retificação', 'Correção de uma evolução que cria uma versão nova e mantém a anterior intacta.'],
    ['Encaminhamento', 'Direcionamento de um assistido ou de uma demanda a um serviço da rede ou setor.'],
    ['Desfecho', 'Resultado de um encaminhamento, registrado uma única vez.'],
    ['Rede de serviços', 'Serviços públicos acionados: CRAS, CAPSi, UBS, escolas, conselhos.'],
    ['CRAS / CAPSi / UBS', 'Centro de Referência de Assistência Social / Centro de Atenção Psicossocial Infantojuvenil / Unidade Básica de Saúde.'],
    ['Painel', 'Tela inicial com as demandas em aberto por estado, totais e vencidas.'],
    ['Auditoria', 'Registro, só de inserção, de quem criou, alterou, consultou ou emitiu relatório com dados de assistidos, e quando.'],
    ['Direção / Profissional', 'Perfis do sistema. Profissional inclui assistente social e equipe pedagógica.'],
    ['Dado pessoal sensível', 'Dado sobre saúde, entre outros, que a LGPD protege com salvaguardas específicas.'],
    ['Controlador', 'Na LGPD, quem decide sobre o tratamento dos dados; aqui, o CRIE.'],
    ['APAE / CRIE', 'Associação de Pais e Amigos dos Excepcionais / Centro de Integração Especial, a instituição parceira.'],
    ['LGPD', 'Lei Geral de Proteção de Dados Pessoais, Lei nº 13.709/2018.'],
    ['Spec', 'Especificação curta de comportamento do servidor (docs/specs), escrita antes do código; se divergir do código, a spec vale.'],
    ['API / JWT', 'Interface HTTP entre o React e o Flask / token assinado que identifica a sessão por 30 minutos.'],
    ['PR / CI', 'Pull request no GitHub / integração contínua: os testes que rodam automaticamente em cada PR.'],
    ['RF / RNF / RS / RN', 'Requisito funcional / requisito não funcional / restrição de solução / regra de negócio.'],
    ['MoSCoW', 'Priorização em Must, Should, Could e Won’t have.'],
    ['Critério de ajuste', 'Medida objetiva que permite testar se o requisito foi atendido.'],
]

V5A = [
    'O CRIE foi fundado em 1991, filiou-se às APAEs em 2005 e tem Certificado de Entidade Beneficente de Assistência Social desde 2016.',
    'Há três reuniões semanais de equipe, uma por setor: pedagógico, saúde e serviço de convivência.',
    'A instituição estima cerca de seis usuários simultâneos.',
    'Parte expressiva das pessoas atendidas é menor de idade.',
    'A internet do CRIE tem estabilidade intermitente.',
    'O relatório enviado à Prefeitura não tem modelo padronizado, é feito por cada profissional e resume atendimentos; não trata das demandas de articulação.',
    'Algumas demandas se repetem ao longo do tempo, e a família ou a rede pede informações sobre o que já foi feito.',
    'O acompanhamento de casos encaminhados continua em reunião mensal de rede.',
    'Hoje as demandas ficam em papel e planilhas.',
]

RN = [
    ['RN-01', 'Toda demanda nasce no estado Aberta', 'Spec 02'],
    ['RN-02', 'Transições permitidas: Aberta para Em andamento ou Cancelada; Em andamento para Aguardando terceiros, Concluída ou Cancelada; Aguardando terceiros para Em andamento ou Cancelada. Concluída e Cancelada não mudam mais', 'Spec 02 (decisão da frente de back-end em 13/10/2026, a confirmar pela instituição)'],
    ['RN-03', 'Nada é excluído: demanda, histórico, evolução, encaminhamento, reunião, usuário e auditoria. Cancelar ou desativar é mudança de estado', 'Restrição (d) do relatório v3, seção 3.1.3; specs 01 a 07'],
    ['RN-04', 'Toda mudança de estado, anotação e troca de responsável grava autor, data e hora', 'RF-014; spec 02'],
    ['RN-05', 'Demanda vencida: prazo anterior a hoje, no fuso do CRIE, e não concluída nem cancelada', 'Spec 02'],
    ['RN-06', 'Perto do prazo: prazo entre hoje e hoje mais 3 dias, valor configurável', 'Spec 09 (decisão A10)'],
    ['RN-07', 'Toda reunião pertence a um setor: pedagógico, saúde ou serviço de convivência', 'Relatórios v2 e v3; spec 04'],
    ['RN-08', 'Toda demanda tem reunião de origem, responsável ativo, prioridade (baixa, média ou alta) e prazo', 'Spec 02'],
    ['RN-09', 'O assistido é cadastrado só com o nome de tratamento enquanto a instituição não definir os campos', 'Spec 03 (decisão A3); princípio da minimização da LGPD'],
    ['RN-10', 'Evolução não se edita: retificar cria versão nova e preserva a anterior; só a versão vigente pode ser retificada', 'Spec 06'],
    ['RN-11', 'Encaminhamento é ligado a assistido, a demanda ou aos dois; vindo da demanda, herda o assistido dela; o desfecho é registrado uma única vez', 'Spec 07'],
    ['RN-12', 'Acesso aberto: todo profissional ativo vê demandas, assistidos, evoluções e encaminhamentos; a auditoria registra quem consultou', 'Decisão da direção (relatórios v2 e v3)'],
    ['RN-13', 'Só a direção cadastra, edita e desativa usuários, emite relatórios e consulta a auditoria; a direção não desativa a própria conta', 'Specs 01, 05 e 08'],
    ['RN-14', 'Avisos não levam dado de saúde nem descrição: só número, prazo e estado da demanda', 'docs/requisitos.md, seção 3.9; spec 09'],
    ['RN-15', 'O login é bloqueado na sexta falha em 60 segundos para o mesmo IP e e-mail', 'Spec 01'],
]

V5C = [
    ['A instituição disponibiliza profissionais para validar o protótipo e participar dos testes de usabilidade', 'Os critérios de aceitação 1, 2 e 7 ficam sem verificação com usuários reais'],
    ['O aplicativo de cadastro continua em uso, sem integração', 'Cadastro duplicado de pessoas'],
    ['A instituição, como controladora, define as regras de acesso e a política de retenção', 'A orientação RNF-009 não tem efeito e a auditoria cresce sem limite (A7)'],
    ['Os computadores do CRIE têm navegador atual', 'A interface pode não funcionar'],
    ['As transições de estado da spec 02 correspondem ao fluxo real das reuniões', 'Retrabalho na máquina de estados e nos testes'],
    ['A internet, mesmo instável, permite usar um sistema online', 'Seria preciso modo offline, que está fora do escopo'],
    ['Os planos gratuitos da Vercel e do Neon continuam disponíveis', 'Custo mensal ou migração de hospedagem'],
]

V6A = [
    'Depois de cada reunião de setor, as demandas ficam anotadas em papel e, em parte, em planilhas. Não há controle central do andamento: para saber o que já foi feito, é preciso procurar nas anotações de quem participou. O responsável pela articulação faz os contatos com a rede (CRAS, saúde, escola) e o retorno também fica em anotações.',
    'Problemas relatados pela direção: tempo perdido para retomar demandas antigas; demandas esquecidas, porque nada avisa que estão paradas; dificuldade de responder à família ou à rede quando uma demanda se repete. Além disso, sem registro de quem consultou o quê, não há como cumprir as salvaguardas da LGPD para dados de saúde.',
]

EVENTOS = [
    ['E-01', 'Reunião de setor acontece (semanal)', 'Data, setor, participantes e casos discutidos', 'Reunião registrada e demandas abertas com responsável e prazo'],
    ['E-02', 'Profissional toma uma providência ou recebe resposta', 'Demanda, novo estado ou anotação', 'Histórico atualizado com autor, data e hora'],
    ['E-03', 'Família ou rede pergunta o que já foi feito; demanda se repete', 'Trecho da descrição ou nome de tratamento', 'Histórico da demanda e ficha do assistido'],
    ['E-04', 'Profissional faz atendimento ou oficina com o assistido', 'Assistido, data, área de atuação e descrição', 'Evolução registrada na ficha'],
    ['E-05', 'Caso precisa ser encaminhado à rede', 'Demanda ou assistido, destino e data', 'Encaminhamento pendente'],
    ['E-06', 'Serviço da rede dá retorno', 'Encaminhamento e texto do desfecho', 'Encaminhamento com desfecho, fora da lista de pendentes'],
    ['E-07', 'Profissional entra no sistema e há prazo vencido ou próximo (temporal)', 'Data atual e demandas do responsável', 'Aviso de prazo sem dado de saúde'],
    ['E-08', 'Fim de um período, por exemplo o mês (temporal)', 'Período e filtros', 'Relatório de demandas ou de acompanhamento, com emissão auditada'],
    ['E-09', 'Profissional entra ou sai da equipe', 'Nome, e-mail e perfil', 'Conta criada ou desativada'],
    ['E-10', 'Direção quer saber quem consultou dados de um assistido', 'Assistido e período', 'Registros de auditoria'],
]

ESPEC_EVENTOS = [
    ['E-01 – Reunião de setor acontece', 'Data, setor, participantes e, para cada caso, descrição, prioridade, responsável, prazo e, se houver, o assistido',
     ['1. A reunião do setor acontece e define as ações de cada caso.', '2. Um participante registra a reunião no sistema: data, setor e participantes (UC-004).', '3. Para cada caso, registra a demanda a partir da ficha da reunião, que já traz a reunião escolhida (UC-005), e confirma o resumo.', '4. O sistema grava a demanda como Aberta e o primeiro item do histórico com autor, data e hora.', '5. A ficha da reunião passa a listar as demandas com o estado de cada uma; o painel e a lista Minhas demandas do responsável também.'],
     'Reunião registrada; demandas abertas visíveis no painel e para o responsável'],
    ['E-06 – Serviço da rede dá retorno', 'Encaminhamento pendente e texto do retorno',
     ['1. O responsável recebe o retorno da rede (por ligação, ofício ou visita, fora do sistema).', '2. Abre Encaminhamentos, que mostra os pendentes do mais antigo para o mais novo (UC-010).', '3. Escolhe o encaminhamento e registra o desfecho; a tela avisa que o desfecho só pode ser registrado uma vez.', '4. O sistema grava o texto, o autor e o momento e registra a auditoria “registrar_desfecho”.', '5. Se for o caso, o responsável abre a demanda ligada e muda o estado (UC-006).'],
     'Encaminhamento com desfecho, fora da lista de pendentes; auditoria registrada'],
    ['E-07 – Hora de verificar prazos (ao entrar)', 'Login do profissional e data atual no fuso do CRIE',
     ['1. O profissional entra no sistema (UC-001).', '2. O sistema separa as demandas em aberto em que ele é o responsável.', '3. Marca como vencidas as de prazo anterior a hoje e como perto do prazo as de prazo entre hoje e hoje mais 3 dias.', '4. Devolve só número, prazo e estado de cada uma, sem descrição nem assistido.', '5. O painel mostra o aviso com um link por demanda (UC-002).'],
     'Aviso de prazo no painel; nenhum dado de saúde exposto'],
]

V7_NOTA = 'O DER conceitual (versão 2, frente de Banco de Dados) inclui as entidades Ação, Serviço da rede e Retorno de acompanhamento, que não foram implementadas nesta versão: o destino do encaminhamento continua em texto (decisão A1) e o retorno é registrado como desfecho (Volere 26). O modelo implementado tem 11 tabelas, criadas pelas migrações de backend/migrations e conferidas pelo teste test_migracoes.py: usuario, assistido, assistido_profissional, reuniao, reuniao_participante, demanda, historico_demanda, evolucao, encaminhamento, auditoria e token_revogado. Os scripts SQL de Banco de Dados 1 estão em docs/modelagem/sql.'

DICIONARIO = [
    ['Usuario', 'id', 'Inteiro', 'Sim', 'Chave primária'],
    ['Usuario', 'nome', 'Texto', 'Sim', 'Não pode ser vazio'],
    ['Usuario', 'email', 'Texto', 'Sim', 'Único; comparado sem maiúsculas e sem espaços nas pontas'],
    ['Usuario', 'senha (hash)', 'Texto', 'Sim', 'Só o hash (werkzeug); senha com no mínimo 8 caracteres; nunca volta em resposta'],
    ['Usuario', 'perfil', 'direcao, assistente_social ou equipe_pedagogica', 'Sim', 'Define a classe (herança em tabela única)'],
    ['Usuario', 'ativo', 'Booleano', 'Sim', 'Desativar substitui a exclusão'],
    ['Assistido', 'nome_tratamento', 'Texto, até 120', 'Sim', 'Único campo aceito enquanto A3 estiver aberta'],
    ['Assistido', 'ativo, criado_em', 'Booleano; data e hora', 'Sim', 'Sem exclusão'],
    ['AssistidoProfissional', 'assistido_id, usuario_id, data_inicio', 'Chaves estrangeiras; data', 'Sim', 'Quem acompanha quem; usado só pela regra restritiva desligada'],
    ['Reuniao', 'data', 'Data AAAA-MM-DD', 'Sim', '—'],
    ['Reuniao', 'setor', 'pedagogico, saude ou convivencia', 'Sim', 'Outro valor é recusado'],
    ['ReuniaoParticipante', 'reuniao_id, usuario_id', 'Chaves estrangeiras', 'Sim', 'Participante repetido vira uma linha só'],
    ['Demanda', 'descricao', 'Texto', 'Sim', 'Não pode ser vazio'],
    ['Demanda', 'categoria', 'Texto, até 80', 'Não', 'Sem catálogo (A2)'],
    ['Demanda', 'prioridade', 'baixa, media ou alta', 'Sim', '—'],
    ['Demanda', 'prazo', 'Data', 'Sim', 'Base do cálculo de vencida'],
    ['Demanda', 'estado', 'aberta, em_andamento, aguardando_terceiros, concluida, cancelada', 'Sim', 'Nasce aberta; transições da RN-02; CHECK no banco'],
    ['Demanda', 'responsavel_id, reuniao_id', 'Chaves estrangeiras', 'Sim', 'Responsável ativo; reunião existente'],
    ['Demanda', 'assistido_id', 'Chave estrangeira', 'Não', 'A resposta da API traz só o id'],
    ['HistoricoDemanda', 'tipo', 'estado ou anotacao', 'Sim', 'Só inserção (sessão e trigger)'],
    ['HistoricoDemanda', 'estado_anterior, estado_novo, texto', 'Texto', 'Conforme o tipo', '—'],
    ['HistoricoDemanda', 'autor_id, ocorrido_em', 'Chave estrangeira; data e hora do servidor', 'Sim', 'Autor sai do token'],
    ['Evolucao', 'data, area_atuacao, descricao', 'Data; texto até 80; texto', 'Sim', 'Área sem catálogo (QA06)'],
    ['Evolucao', 'profissional_id, autor_id, ocorrido_em', 'Chaves estrangeiras; data e hora do servidor', 'Sim', 'Saem do token e do relógio do servidor'],
    ['Evolucao', 'retifica_id', 'Chave estrangeira para a versão anterior', 'Não', 'Única: uma versão só pode ser retificada uma vez'],
    ['Encaminhamento', 'assistido_id, demanda_id', 'Chaves estrangeiras', 'Pelo menos um', 'CHECK no banco; vindo da demanda herda o assistido'],
    ['Encaminhamento', 'destino, data, responsavel_id', 'Texto até 200; data; chave estrangeira', 'Sim', 'Destino em texto livre (A1)'],
    ['Encaminhamento', 'observacao', 'Texto', 'Não', '—'],
    ['Encaminhamento', 'desfecho, desfecho_autor_id, desfecho_em', 'Texto; chave estrangeira; data e hora', 'Não (os três juntos)', 'Registrado uma única vez'],
    ['Auditoria', 'autor_id, acao, recurso, recurso_id, assistido_id', 'Chaves e listas fechadas', 'autor, acao e recurso sim', 'Ações: criar, alterar, consultar, listar, retificar, registrar_desfecho, emitir'],
    ['Auditoria', 'detalhe', 'Texto até 200', 'Não', 'Filtros e período; nunca texto de evolução nem nome de assistido'],
    ['Auditoria', 'ocorrido_em', 'Data e hora do servidor', 'Sim', 'Só inserção (sessão e trigger)'],
    ['TokenRevogado', 'jti, expira_em', 'Texto; data e hora', 'Sim', 'Token encerrado no logout até a expiração original'],
]

V8A_FARA = 'Registro de reuniões por setor e das demandas de cada reunião; controle de estado com histórico que não se apaga; anotações e troca de responsável; painel com o que está em aberto e vencido; Minhas demandas; busca e filtros; cadastro de assistidos só com o nome de tratamento e ficha com demandas, evoluções e encaminhamentos; evoluções com retificação que preserva a versão anterior; encaminhamentos com desfecho; aviso de prazo ao entrar; relatórios do período e do assistido (só a direção, com impressão pelo navegador); auditoria das operações com dados de assistidos; gestão de usuários pela direção.'
V8A_NAO = 'Controle de estoque de materiais; anexo de laudos e documentos; integração com o aplicativo de cadastro em uso; funcionamento offline; envio por WhatsApp; notificação por e-mail (RF-041, adiada); relatório no formato da Prefeitura; cadastro de serviços da rede e retorno de acompanhamento; exclusão definitiva de registros; troca de senha pelo próprio usuário, “esqueci a senha” e autocadastro.'

UCS = [
    ['UC-001', 'Entrar no sistema', 'Profissional, Direção', 'E-07', 'RF-001, RF-002, RF-003'],
    ['UC-002', 'Ver aviso de prazo', 'Profissional, Direção', 'E-07', 'RF-040, RF-033'],
    ['UC-003', 'Gerir usuários', 'Direção', 'E-09', 'RF-003, RF-004'],
    ['UC-004', 'Registrar reunião de setor', 'Profissional', 'E-01', 'RF-006, RF-007, RF-008, RF-009'],
    ['UC-005', 'Registrar demanda', 'Profissional', 'E-01', 'RF-010, RF-011, RF-012, RF-014'],
    ['UC-006', 'Atualizar andamento da demanda', 'Profissional', 'E-02', 'RF-012, RF-013, RF-014, RF-015, RF-016'],
    ['UC-007', 'Consultar demandas e histórico', 'Profissional', 'E-03', 'RF-017, RF-030, RF-031, RF-032, RF-033, RF-034, RF-039'],
    ['UC-008', 'Cadastrar e consultar assistido', 'Profissional', 'E-03', 'RF-018, RF-019, RF-020'],
    ['UC-009', 'Lançar e retificar evolução', 'Profissional', 'E-04', 'RF-005, RF-021 a RF-026'],
    ['UC-010', 'Registrar encaminhamento e desfecho', 'Profissional', 'E-05, E-06', 'RF-027, RF-028, RF-029'],
    ['UC-011', 'Emitir relatório', 'Direção', 'E-08', 'RF-035, RF-036, RF-037, RF-038, RF-039'],
    ['UC-012', 'Consultar auditoria', 'Direção', 'E-10', 'RNF-003'],
    ['UC-013', 'Registrar auditoria (incluído)', 'Sistema', '—', 'RNF-003, RF-038'],
    ['UC-014', 'Gravar histórico da demanda (incluído)', 'Sistema', '—', 'RF-014, RF-017'],
]

UC_DETALHE = [
    {
        'id': 'UC-001 – Entrar no sistema',
        'objetivo': 'Identificar a pessoa, abrir o painel e encerrar a sessão ao sair.',
        'ator': 'Profissional ou Direção',
        'secundarios': 'Nenhum',
        'prioridade': 'Alta',
        'pre': 'Conta cadastrada pela direção e ativa.',
        'fluxo': ['1. O ator abre o endereço do sistema.', '2. O sistema mostra a tela Entrar, com E-mail e Senha.', '3. O ator informa os dados e aciona Entrar.', '4. O sistema confere a senha pelo hash, emite um token de 30 minutos e mostra o Painel.', '5. Se houver demanda do ator vencida ou perto do prazo, o painel mostra o aviso (UC-002).', '6. Ao terminar, o ator aciona Sair; o sistema revoga o token e apaga a sessão e os rascunhos da aba.'],
        'alt': ['4a. A sessão anterior terminou por tempo: o sistema mostra “Sua sessão terminou. Entre de novo.” e, depois do login, volta para a tela em que o ator estava.'],
        'exc': ['E1. E-mail inexistente, senha errada ou conta desativada: “E-mail ou senha inválidos.”, sem dizer qual (401).', 'E2. Sexta falha em 60 segundos do mesmo IP e e-mail: a mesma mensagem e bloqueio temporário (429).', 'E3. Campo vazio: “Informe o e-mail.” ou “Informe a senha.”', 'E4. Servidor sem resposta: “Não foi possível falar com o servidor. Confira a internet e tente de novo.”'],
        'pos': 'Sucesso: sessão aberta por até 30 minutos, com o menu do perfil. Falha: nenhuma sessão aberta.',
        'req': 'RF-001, RF-002, RF-003, RF-040, RNF-002, RNF-005, RNF-034',
    },
    {
        'id': 'UC-005 – Registrar demanda',
        'objetivo': 'Registrar, logo depois da reunião, uma demanda com responsável e prazo, para que ela não seja esquecida.',
        'ator': 'Profissional (assistente social ou equipe pedagógica) ou Direção',
        'secundarios': 'Responsável escolhido, que passa a ver a demanda em Minhas demandas',
        'prioridade': 'Alta',
        'pre': 'Usuário autenticado com conta ativa; reunião de origem registrada (UC-004); responsável com conta ativa.',
        'fluxo': ['1. O ator escolhe Registrar demanda no Painel, em Demandas ou na ficha da reunião.', '2. O sistema mostra um único formulário, com a reunião mais recente já escolhida.', '3. O ator informa descrição, prioridade, responsável e prazo e, se quiser, assistido e categoria.', '4. O ator aciona Registrar demanda.', '5. O sistema mostra o diálogo “Confirmar registro da demanda?” com o resumo.', '6. O ator confirma.', '7. O sistema grava a demanda como Aberta, grava o primeiro item do histórico com autor, data e hora (UC-014) e abre a ficha da demanda com o aviso de sucesso.'],
        'alt': ['2a. Não há reunião cadastrada: o sistema mostra “Antes, registre a reunião em que a demanda surgiu.” com link para UC-004.', '2b. O ator veio da ficha da reunião: o formulário já vem com essa reunião.', '6a. O ator escolhe Voltar: o diálogo fecha e o formulário mantém o que foi preenchido.'],
        'exc': ['E1. Campo obrigatório vazio ou inválido: a mensagem aparece junto do campo (por exemplo, “Informe a descrição da demanda.”) e nada é gravado (422).', 'E2. Falha de conexão: aviso no topo do formulário, sem apagar os dados (RNF-016).', 'E3. Sessão vencida (401): o rascunho fica guardado na aba e volta depois de entrar de novo com a mesma conta.'],
        'pos': 'Sucesso: demanda Aberta no painel e em Minhas demandas do responsável, com histórico. Falha: nada é gravado.',
        'req': 'RF-010, RF-011, RF-012, RF-014, RNF-012, RNF-014, RNF-016',
    },
    {
        'id': 'UC-006 – Atualizar andamento da demanda',
        'objetivo': 'Registrar o que foi feito numa demanda: mudar o estado, anotar ou trocar o responsável.',
        'ator': 'Profissional ou Direção',
        'secundarios': 'Novo responsável, na troca',
        'prioridade': 'Alta',
        'pre': 'Usuário autenticado; demanda existente.',
        'fluxo': ['1. O ator abre a demanda pelo Painel, por Minhas demandas, por Demandas ou pelo aviso de prazo.', '2. O sistema mostra os dados, o histórico em ordem cronológica e as ações.', '3. O ator escolhe Mudar estado.', '4. O sistema abre o diálogo só com os estados permitidos a partir do atual.', '5. O ator escolhe o novo estado e confirma.', '6. O sistema grava o estado e um item de histórico com estado anterior, novo, autor, data e hora (UC-014) e atualiza a ficha.'],
        'alt': ['3a. Anotar: o ator escreve o texto e salva; o sistema grava um item do tipo anotação sem mudar o estado.', '3b. Trocar responsável: o ator escolhe um profissional ativo e confirma; o histórico registra a troca e quem a fez.', '3c. Encaminhar: segue para UC-010 com a demanda já vinculada.', '5a. Estado Cancelada: o diálogo avisa que a demanda continua no histórico e pode ser encontrada pela busca.'],
        'exc': ['E1. Transição não permitida, por exemplo de Concluída para Aberta: “Esta demanda não pode mudar para esse estado.”, sem gravar histórico (400).', 'E2. Anotação vazia: “Escreva o texto da anotação.” (422).', 'E3. Responsável inativo ou inexistente: “Responsável inexistente ou inativo.” (404).'],
        'pos': 'Sucesso: estado, anotação ou responsável gravado e um item a mais no histórico. Falha: nada muda.',
        'req': 'RF-012, RF-013, RF-014, RF-015, RF-016, RF-017',
    },
    {
        'id': 'UC-009 – Lançar e retificar evolução',
        'objetivo': 'Registrar o acompanhamento de um assistido e corrigir sem apagar.',
        'ator': 'Profissional ou Direção',
        'secundarios': 'Nenhum',
        'prioridade': 'Alta',
        'pre': 'Usuário autenticado; assistido cadastrado; acesso às evoluções (no acesso aberto, toda conta ativa).',
        'fluxo': ['1. O ator abre Assistidos e a ficha do assistido.', '2. Aciona Lançar evolução.', '3. Informa a data (hoje por padrão), a área de atuação e a descrição.', '4. Salva.', '5. O sistema grava a evolução com autor, profissional e momento do servidor, registra a auditoria (UC-013) e mostra a evolução na ficha em ordem cronológica.'],
        'alt': ['1a. O ator filtra as evoluções por período e por área (RF-025).', '4a. Retificar: na versão vigente, o ator aciona Retificar, altera os campos e salva; o sistema cria uma versão nova que aponta a anterior, mantém a anterior intacta e registra a auditoria “retificar”.'],
        'exc': ['E1. Campo vazio: “Informe a data da evolução.”, “Informe a área de atuação.” ou “Escreva a descrição da evolução.” (422).', 'E2. Retificar versão antiga: “Só a versão vigente da evolução pode ser retificada.” (400).', 'E3. Com a regra restritiva ligada, quem não acompanha o assistido recebe “Você não tem acesso às evoluções deste assistido.” (403) e nada é gravado.', 'E4. Tentativa de excluir: a tela não tem essa opção e a API responde 405.'],
        'pos': 'Sucesso: evolução vigente na ficha e versões anteriores consultáveis. Falha: nada é gravado.',
        'req': 'RF-005, RF-021, RF-022, RF-023, RF-024, RF-025, RF-026, RNF-003',
    },
    {
        'id': 'UC-011 – Emitir relatório',
        'objetivo': 'Obter as demandas de um período ou o acompanhamento de um assistido, com registro de quem emitiu.',
        'ator': 'Direção',
        'secundarios': 'Nenhum',
        'prioridade': 'Alta',
        'pre': 'Conta da direção ativa.',
        'fluxo': ['1. A direção abre Relatórios.', '2. Escolhe Demandas do período, informa De e Até e, se quiser, estado, categoria e responsável.', '3. Aciona Emitir.', '4. O sistema lista as demandas registradas no período, com totais por estado e vencidas e o rodapé “Emitido por … em …”, e grava a auditoria “emitir” com o mesmo momento (UC-013).', '5. A direção aciona Imprimir e o navegador imprime.'],
        'alt': ['2a. Acompanhamento do assistido: a direção escolhe o assistido e o período; o sistema mostra as evoluções vigentes e os encaminhamentos do período.'],
        'exc': ['E1. Sem De ou Até, ou De depois de Até: “Informe o período do relatório (de e ate).” (422).', 'E2. Perfil profissional: “Só a direção emite relatórios.” (403); o item nem aparece no menu.', 'E3. Assistido inexistente: 404, sem auditoria.'],
        'pos': 'Sucesso: relatório na tela, emissão auditada. Falha: nada é registrado.',
        'req': 'RF-035, RF-036, RF-037, RF-038, RF-039, RNF-003',
    },
]
