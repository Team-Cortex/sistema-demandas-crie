# Capa, controle do documento, organização e Parte I
SISTEMA = 'Sistema de Demandas do CRIE'
VERSAO = '0.9'
DATA = '23/11/2026'

CAPA = {
    'instituicao': 'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO\nCÂMPUS BRAGANÇA PAULISTA',
    'curso': 'Tecnologia em Análise e Desenvolvimento de Sistemas, 2º semestre de 2026',
    'sistema': 'SISTEMA DE DEMANDAS DO CRIE',
    'equipe_rotulo': 'Equipe Cortex:',
    'equipe': [
        ['a informar', 'Gabriel Borba'],
        ['a informar', 'Henry Claro'],
        ['a informar', 'Inácio Fontes'],
        ['a informar', 'Miguel Vaz de Souza'],
        ['a informar', 'Vinícius Marrocos'],
    ],
    'cidade': 'Bragança Paulista',
    'mes': 'Novembro de 2026',
}

CONTROLE = [
    'Sistema de Demandas do CRIE (gestão das demandas de articulação de rede)',
    'CRIE, Centro de Integração Especial (APAE de Extrema-MG), representado pela direção',
    VERSAO,
    DATA,
    'Em revisão. Falta a equipe concluir as pendências marcadas em VIII.6.',
    'https://github.com/Team-Cortex/sistema-demandas-crie',
    'Trello, quadro “Equipe Cortex”: https://trello.com/b/XgMRYAKo/equipe-cortex',
]

HISTORICO = [
    ['23/11/2026', '0.1', 'Criação do documento a partir do modelo e consolidação do conteúdo do repositório: requisitos, specs 01 a 09, material de IHC, testes e histórico do GitHub', 'Equipe Cortex'],
    ['23/11/2026', '0.9', 'Resultados do CI de 23/11/2026 (PR #19) e verificação de HTTPS em produção', 'Equipe Cortex'],
    ['25/11/2026 (previsto)', '1.0', 'Versão final para entrega, depois das pendências listadas em VIII.6', 'Equipe Cortex'],
]

PAPEIS = [
    ['Vinícius Marrocos', 'Gerente de Projeto e Analista de Requisitos', 'Partes I, II (seções 1 a 9 e 18 a 27), IV e VII'],
    ['Henry Claro', 'Analista de Banco de Dados', 'Volere 7 (modelo de dados) e apoio às seções 12 a 15'],
    ['Inácio Fontes', 'Analista de Interface e Experiência do Usuário', 'Parte III, Volere 2e, 10 e 11, plano de testes de usabilidade'],
    ['Miguel Vaz de Souza', 'Desenvolvedor Back-end', 'Volere 12 a 15, Partes V e VI'],
    ['Gabriel Borba', 'Desenvolvedor Front-end', 'Parte III (telas do sistema), Volere 13 e 14'],
]

ORGANIZACAO_INTRO = [
    'Este documento reúne, no modelo Volere adotado na disciplina, a especificação e os artefatos do Sistema de Demandas do CRIE produzidos pela Equipe Cortex no 2º semestre de 2026. A fonte é o repositório do projeto: cada afirmação aponta o arquivo de origem (por exemplo, docs/requisitos.md) ou o pull request (PR) do GitHub. O que não tem evidência no repositório aparece como pendente, e não como concluído.',
    'Convenção de identificadores: RF-001 a RF-041 correspondem, um a um, a RF01 a RF41 de docs/requisitos.md (versão 2.0). RNF-001 a RNF-026 correspondem a RNF01 a RNF26 do mesmo documento. RNF-027 a RNF-037 foram formalizados neste documento a partir de decisões já registradas no repositório, com a fonte indicada em cada um. Os demais prefixos são: N (necessidade), RS (restrição), RN (regra de negócio), E (evento), UC (caso de uso), T (tela), Q (questão aberta), R (risco), CT (caso de teste de caixa preta), CB (caso de teste de caixa branca), BUG (defeito) e PB (item do backlog). As letras A1 a A10, D3, D4, D6 e QA01 a QA08 são as decisões abertas com esses nomes nas specs e nos documentos de IHC.',
]

MAPA_ENTREGAS_COL4 = [
    'Relatórios de projeto v1 a v3 (docs/relatorios); formulário de levantamento respondido pela direção do CRIE',
    'Documento de requisitos v2.0 (docs/requisitos.md); specs 01 a 09 (docs/specs); minimundo e DER (docs/modelagem)',
    'Material de IHC (docs/ihc): personas, cenários, arquitetura da informação, fluxos, telas e protótipo clicável',
    'Prioridades e rastreabilidade de docs/requisitos.md (seções 3 e 7)',
    'Testes automatizados (backend/tests e frontend/tests); plano de testes de usabilidade (docs/ihc/plano-de-testes.md)',
    'Repositório no GitHub (Team-Cortex) e quadro Kanban no Trello',
    'Regras de qualidade das specs, do contrato da API e do CI (PR #19)',
    '–',
]

I1 = [
    'Este documento especifica os requisitos do Sistema de Demandas do CRIE e reúne os artefatos produzidos ao longo do semestre: elicitação, especificação no modelo Volere, protótipos, priorização, rastreabilidade, verificação e validação, gerenciamento e qualidade. É o trabalho final da disciplina de Engenharia de Software (BRAENSO) e junta, numa única especificação, o que hoje está espalhado pelo repositório.',
    'Leitores: a professora da disciplina, que avalia o trabalho; a direção do CRIE, que é a cliente e decide se o sistema atende à instituição; e a própria equipe, que usa o documento para saber o que falta implementar e validar. Quem mantiver o sistema depois do semestre encontra aqui as decisões tomadas e as que continuam abertas (Volere 18).',
]

I2 = [
    'O Sistema de Demandas do CRIE é uma aplicação web para registrar, acompanhar e consultar as demandas de articulação de rede levantadas nas reuniões semanais de equipe do CRIE, Centro de Integração Especial, organização sem fins lucrativos de Extrema (MG) filiada à Federação das APAEs, que atende pessoas com deficiência e suas famílias. Demanda de articulação é uma situação que a equipe não resolve com recursos internos e que exige a rede de serviços públicos: assistência social, saúde e educação.',
    'Hoje essas demandas ficam em papel e planilhas, sem controle de andamento. A direção relatou três consequências: perde-se tempo para retomar demandas antigas, algumas demandas são esquecidas e ficam sem conclusão, e é difícil saber o que já foi feito quando uma demanda se repete. O sistema centraliza o registro desde a reunião até o desfecho, mostra numa única tela o que está atrasado, guarda o histórico sem permitir exclusão e registra quem consultou os dados das pessoas atendidas.',
]

I2_TABELA = [
    'Aplicação web com dados pessoais sensíveis: cliente React e API REST em Python com Flask, banco PostgreSQL',
    'Web, em navegador de computador da instituição (o layout também funciona em telas estreitas)',
    'Direção e profissionais do CRIE (assistente social e equipe pedagógica), cerca de seis usuários simultâneos',
    'Novo. Substitui o registro em papel e planilhas; não substitui o aplicativo de cadastro que a instituição já usa',
]

I3 = [
    'Processo iterativo e incremental com Kanban (quadro no Trello), em cinco ciclos ligados às entregas da disciplina de extensão: 03/09, 01/10, 22/10, 05/11 e 18 a 26/11/2026. A partir do 3º ciclo, cada funcionalidade passou a ter uma especificação de comportamento (spec) escrita antes do código, com os testes que a provam.',
    'Os requisitos vieram de uma interlocutora externa com pouca disponibilidade e mudaram conforme a equipe entendeu o domínio: três hipóteses estruturais estavam erradas (I.4f). Em cascata, com requisitos congelados no início, o sistema teria uma reunião única, trataria a demanda como tarefa interna e restringiria o acesso, o contrário do que a instituição informou. Scrum foi descartado porque a equipe tem cinco estudantes com dedicação parcial, cada um ligado a uma disciplina diferente, sem horário comum para cerimônias diárias. O Kanban, sugerido pela disciplina de extensão, mostra o que está parado sem exigir papéis fixos. Os ciclos seguiram as datas de entrega porque cada entrega pedia uma nova versão do relatório.',
]

I3A = [
    ['Especificação', 'Formulário de levantamento respondido pela direção, rodadas de perguntas por mensagem e áudio, documento de requisitos (docs/requisitos.md) e specs 01 a 09 escritas antes do código', 'Partes I, II e III'],
    ['Desenvolvimento', 'Monorepo no GitHub com backend (Flask), frontend (React) e docs; uma branch por funcionalidade, integrada por pull request na development; a main publica na Vercel', 'Parte VI'],
    ['Validação', 'Testes automatizados (pytest e node --test) no CI do GitHub Actions; revisão das decisões com a direção por mensagem; 8 testes de usabilidade planejados e ainda não executados', 'Parte V'],
    ['Evolução', 'Decisões abertas A1 a A10 registradas nas specs; itens adiados: e-mail, impressão formatada, integração com o aplicativo de cadastro, estoque', 'Volere 18 e 26'],
]

I3B = [
    'Não se aplica a este projeto, porque a equipe usou Kanban, sem papel de Product Owner. Quem prioriza é a direção do CRIE; Vinícius Marrocos, gerente de projeto, transforma as prioridades em cartões.',
    'Não se aplica a este projeto, porque não houve Scrum Master. O acompanhamento do quadro ficou com o gerente de projeto, Vinícius Marrocos.',
    'Gabriel Borba (front-end), Henry Claro (banco de dados), Inácio Fontes (interface), Miguel Vaz de Souza (back-end) e Vinícius Marrocos (requisitos e gestão)',
    'Não se aplica a este projeto, porque não houve sprints. Os ciclos duraram de duas a quatro semanas, conforme as datas de entrega (VI.2).',
    'Não se aplica a este projeto, porque não houve cerimônias formais. Equivalentes registrados: revisão do quadro e do backlog a cada versão do relatório (relatório v3, seções 4.3 a 4.5) e integração de cada entrega de código por pull request, com a descrição do que mudou e do que não foi verificado.',
]

I4A = [
    ['Contato inicial por mensagem eletrônica, sem apresentar solução pronta', 'Diretora do CRIE', 'Agosto de 2026', 'Relatório v3, seção 2.1'],
    ['Formulário estruturado em dez seções', 'Direção do CRIE', 'Agosto de 2026', 'Formulário respondido (Anexo B do relatório v3); docs/requisitos.md, seção 1.4'],
    ['Perguntas complementares em blocos temáticos, com alternativas fechadas (mensagens e áudios)', 'Diretora do CRIE', 'Agosto de 2026, antes da ET1 (03/09/2026)', 'Relatório v1, seção 2.3; relatório v3, seção 2.3 e Quadro 2'],
    ['Descrição do fluxo de uma reunião de setor (áudio)', 'Diretora do CRIE', 'Agosto de 2026', 'Relatório v3, seção 2.4'],
    ['Análise de documentos: LGPD e especificação do projeto integrado (BRAEXT2)', 'Equipe', 'Agosto de 2026', 'docs/requisitos.md, seção 4.1'],
    ['Personas e cenários de uso', 'Frente de IHC', 'Personas em 08/10/2026; cenários em 18/11/2026 (PR #14)', 'docs/ihc/personas.md; docs/ihc/cenarios-de-uso.md'],
    ['Card sorting simulado pela equipe (não feito com usuários)', 'Frente de IHC', 'Novembro de 2026 (PR #14)', 'docs/ihc/arquitetura-da-informacao.md, seção 2'],
]

I4A_JUSTIFICATIVA = 'Justificativa da escolha das técnicas: a direção pediu para conversar por mensagens e áudios, formato que cabe na rotina dela; entrevista presencial e observação da reunião não couberam no calendário. O formulário deu o panorama (objetivo, situação atual, usuários, funcionalidades, sigilo, ambiente, ferramentas, prioridades, prazos e critério de sucesso). As perguntas fechadas resolveram as ambiguidades: a primeira versão, aberta, da pergunta sobre visibilidade teve resposta genérica; reformulada com alternativas numeradas, teve resposta imediata. Personas e cenários transformaram o perfil informado pela direção em requisitos de usabilidade verificáveis.'

I4B = [
    'Dar “agilidade e organização às demandas”, nas palavras da direção: nenhuma demanda esquecida, histórico consultável quando o caso volta e visão única do que está em aberto, sem custo para a instituição.',
    'Direção: perde tempo para achar o histórico de demandas antigas e não vê numa tela só o que está atrasado. Profissionais: anotam em papel e planilha, sem saber o que está com cada um; quando a família ou a rede pergunta o que já foi feito, precisam procurar em vários lugares. Nada avisa que uma demanda está parada.',
    'Entrega em novembro de 2026; orçamento zero (só hospedagem e ferramentas gratuitas); Python com Flask, banco relacional e React, definidos pelas disciplinas; uso em navegador nos computadores do CRIE; dados de saúde de pessoas com deficiência, muitas menores de idade (LGPD); só dados fictícios fora da instituição.',
]

I4C = [
    'A direção decide e é a interlocutora da equipe. Os setores atendem as pessoas e as famílias: atendimento educacional especializado, saúde, assistência social, oficinas e programas para famílias. As demandas nascem em três reuniões semanais, uma por setor: pedagógico, saúde e serviço de convivência. Existe coordenação de setor, mas a instituição não definiu permissões próprias para ela (decisão A4).',
    'Assistência a pessoas com deficiência no terceiro setor, com articulação da rede pública: CRAS, CAPSi, UBS, escolas e conselhos. Os termos estão no Volere 4.',
    'Papel e planilhas para as demandas, sem controle de andamento nem histórico. Um aplicativo de cadastro de usuários já em uso, ainda não identificado (QA03), que continua funcionando sem integração. O relatório enviado à Prefeitura é feito por cada profissional, sem modelo padronizado.',
]

I4D = [
    'A diretora do CRIE (formulário, perguntas complementares e áudios). Os demais profissionais ainda não foram ouvidos diretamente; isso está previsto nos testes de usabilidade (2g).',
    '1. Não esquecer demandas: ver numa tela só o que está em aberto e o que venceu. 2. Retomar o histórico quando uma demanda se repete. 3. Proteger os dados das pessoas atendidas. Os dois primeiros vêm das consequências relatadas pela direção; o terceiro foi proposto pela equipe depois que a direção informou que o sistema trataria dados de saúde e disse desconhecer as exigências legais.',
    'Uma instituição (CRIE, Extrema-MG), uso interno nas dependências, três setores e cinco módulos: demandas, reuniões, assistidos (com evoluções e encaminhamentos), relatórios e auditoria, e usuários. Ficam fora: estoque de materiais, laudos digitalizados, integração com o aplicativo de cadastro, uso offline e envio por WhatsApp (Volere 8a).',
]

NECESSIDADES = [
    ['N-01', 'Retomar demandas anteriores sem perder tempo', 'Direção / formulário', 'Cliente'],
    ['N-02', 'Evitar demandas esquecidas: algo que mostre o que está parado', 'Direção / formulário', 'Cliente'],
    ['N-03', 'Centralizar o registro que hoje está em papel e planilhas', 'Direção / formulário', 'Organizacional'],
    ['N-04', 'Saber o que já foi feito quando a demanda se repete (pedido da família ou da rede)', 'Direção / áudio', 'Cliente'],
    ['N-05', 'Guardar os dados das pessoas atendidas', 'Direção / formulário', 'Domínio'],
    ['N-06', 'Registrar as evoluções do acompanhamento', 'Direção / formulário (incluído na versão 2.0 dos requisitos)', 'Cliente'],
    ['N-07', 'Registrar os encaminhamentos à rede e o retorno', 'Direção / formulário e áudio', 'Domínio'],
    ['N-08', 'Três reuniões semanais por setor, com responsável pela articulação', 'Direção / áudio', 'Organizacional'],
    ['N-09', 'Relatórios para uso interno (o relatório da Prefeitura saiu do escopo depois do esclarecimento)', 'Direção / formulário e áudio', 'Cliente'],
    ['N-10', 'Avisos aos profissionais, de preferência por aplicativo de mensagens', 'Direção / formulário', 'Cliente'],
    ['N-11', 'Sistema “bem simples”: profissionais com pouca familiaridade com tecnologia', 'Direção / formulário', 'Cliente'],
    ['N-12', 'Uso só nas dependências, em computador compartilhado, com internet instável', 'Direção / formulário', 'Domínio'],
    ['N-13', 'Dados de saúde; a instituição desconhece as exigências legais', 'Direção / formulário', 'Organizacional'],
    ['N-14', 'Todos os profissionais cadastrados veem os registros', 'Direção / pergunta fechada com duas alternativas', 'Organizacional'],
    ['N-15', 'Cerca de seis usuários simultâneos', 'Direção / formulário', 'Domínio'],
    ['N-16', 'Controle de entrada e saída de materiais de consumo (segunda necessidade, menos prioritária)', 'Direção / formulário', 'Cliente'],
    ['N-17', 'Sucesso medido por “agilidade e organização das demandas”', 'Direção / formulário', 'Cliente'],
]

I4F = [
    'A maior dificuldade foi descobrir que a hipótese inicial da equipe estava errada em três pontos, o que só apareceu com a escuta continuada (relatório v3, Quadro 2): a equipe imaginava uma reunião semanal, e são três, uma por setor; imaginava a demanda como tarefa interna, e ela é uma situação que exige a rede pública; imaginava acesso restrito por profissional, e a direção escolheu acesso aberto a todos os cadastrados. Cada correção mudou o modelo: entrou o setor na reunião, o encaminhamento virou peça central e o controle de acesso foi refeito.',
    'Outras dificuldades: a disponibilidade da interlocutora, que responde em horário comercial e por mensagens; perguntas abertas que geraram respostas genéricas, resolvidas com alternativas fechadas e numeradas; e o relatório da Prefeitura, tratado como requisito essencial até a direção esclarecer que ele não tem modelo, é feito por cada profissional e não trata das demandas de articulação. O requisito saiu do escopo.',
    'Consenso: as decisões de escopo foram tomadas pela direção, que é a responsável pelos dados (acesso aberto; prioridade das demandas sobre o estoque). Para o acesso aberto, a equipe propôs e a direção aceitou a auditoria de todas as operações com dados de assistidos, inclusive leitura, como principal controle (IV.3).',
    'Ponto de atenção para a revisão da equipe: o relatório v3 cita uma versão 4.0 do documento de requisitos, com 50 requisitos funcionais e 28 não funcionais, que não está no repositório. Este documento parte da versão 2.0 versionada (docs/requisitos.md) e incorpora as decisões das specs. É preciso conferir se algum requisito da versão 4.0 ficou de fora (pendência em VIII.6).',
]
