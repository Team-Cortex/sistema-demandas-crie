# Textos do documento de BD1: universo de discurso, explicação de cada consulta
# e ligação de cada consulta com os requisitos e os cards do back-end.

EQUIPE = ['Gabriel Ribeiro de Borba', 'Henry Claro Maruca', 'Inácio Fontes Bueno',
          'Miguel Vaz de Souza', 'Vinícius Fatichi Marrocos']

UNIVERSO = [
    'O CRIE (Centro de Integração Especial, ligado à APAE de Extrema/MG) atende pessoas com deficiência e organiza seus atendimentos em três setores: pedagógico, saúde e serviço de convivência. Cada setor realiza uma reunião semanal de equipe, na qual são discutidas as situações dos assistidos que não puderam ser resolvidas só com os recursos internos da instituição. De cada reunião registram-se a data, o setor que a realizou e o momento do registro.',
    'Nas reuniões são levantadas <b>demandas de articulação</b>: situações que exigem providências com profissionais da instituição, famílias ou serviços da rede pública (CRAS, unidades de saúde, escolas, Conselho Tutelar). Cada demanda nasce em uma única reunião, e uma reunião pode originar várias demandas ou nenhuma. De cada demanda registram-se a descrição, a categoria, a prioridade (baixa, média ou alta), o prazo, o estado e os momentos de criação e da última atualização. O estado assume apenas os valores aberta, em andamento, aguardando terceiros, concluída ou cancelada; toda demanda nasce aberta, e as concluídas ou canceladas são consideradas encerradas. Cada demanda tem um único profissional responsável e pode se referir a no máximo um assistido, ou a nenhum, nos casos institucionais.',
    'Os profissionais e a direção acessam o sistema como <b>usuários</b>. De cada usuário registram-se o nome, o e-mail (único), a senha, guardada apenas na forma de hash, o perfil (direção, assistente social ou equipe pedagógica), se está ativo e a data de cadastro. Usuários não são excluídos, apenas desativados, para preservar a autoria dos registros antigos.',
    'Dos <b>assistidos</b> registram-se apenas o nome de tratamento, a situação (ativo ou não) e a data de cadastro, seguindo o princípio da minimização de dados da LGPD. Um assistido pode ser acompanhado por vários profissionais, e cada profissional pode acompanhar vários assistidos; desse vínculo registra-se a data de início.',
    'Por fim, os profissionais registram <b>evoluções</b>: anotações sobre o acompanhamento de um assistido, com data, área de atuação, descrição e o momento do lançamento. Cada evolução pertence a um único assistido e a um único profissional. Uma evolução nunca é apagada nem alterada: para corrigi-la, lança-se uma nova versão que aponta para a versão corrigida. Cada versão pode ser retificada no máximo uma vez, o que forma uma cadeia de versões.',
    'Todos os dados usados nesta entrega são fictícios, como exige o minimundo do projeto.',
]

RECORTE = ('O DER do sistema completo (versão 2.0 da equipe) tem 13 entidades. Como a especificação de Banco de Dados I pede de quatro a seis tabelas, este trabalho implementa o recorte central do sistema em seis tabelas: cinco entidades (<b>usuário, assistido, reunião, demanda e evolução</b>) e a tabela associativa do relacionamento N:N acompanha (<b>assistido_profissional</b>). '
           'Duas entidades do DER completo viraram atributos neste recorte: Setor (coluna setor de reuniao, com os três setores) e Categoria de Demanda (coluna categoria de demanda). Ficaram fora as outras seis: Serviço da Rede, Encaminhamento, Ação, Retorno de Acompanhamento, Histórico de Demanda e Registro de Auditoria, além do relacionamento N:N participa (participantes da reunião). Os nomes de tabelas e colunas são os mesmos do back-end do sistema (Flask/SQLAlchemy), para que o banco desta disciplina e o do servidor contem a mesma história.')

RELACIONAMENTOS = [
    ('origina', 'Reunião, Demanda', '1:N', 'Reunião (0,N) e Demanda (1,1)', 'FK reuniao_id em demanda'),
    ('é responsável por', 'Usuário, Demanda', '1:N', 'Usuário (0,N) e Demanda (1,1)', 'FK responsavel_id em demanda'),
    ('refere-se a', 'Assistido, Demanda', '1:N (opcional)', 'Assistido (0,N) e Demanda (0,1)', 'FK assistido_id em demanda, aceita NULL'),
    ('acompanha', 'Usuário, Assistido', 'N:N', 'Usuário (0,N) e Assistido (0,N)', 'tabela associativa assistido_profissional, com data_inicio'),
    ('possui', 'Assistido, Evolução', '1:N', 'Assistido (0,N) e Evolução (1,1)', 'FK assistido_id em evolucao'),
    ('escreve', 'Usuário, Evolução', '1:N', 'Usuário (0,N) e Evolução (1,1)', 'FK profissional_id em evolucao'),
    ('retifica', 'Evolução, Evolução', '1:1', 'Evolução (0,1) e Evolução (0,1)', 'FK retifica_id em evolucao com UNIQUE (autorrelacionamento)'),
]

DESCRICOES = {
    'usuario.id': 'Identificador do usuário', 'usuario.nome': 'Nome completo', 'usuario.email': 'E-mail de acesso, único',
    'usuario.senha_hash': 'Senha cifrada (hash), nunca em texto', 'usuario.perfil': 'Direção, assistente social ou equipe pedagógica',
    'usuario.ativo': 'Falso quando desativado', 'usuario.criado_em': 'Data e hora do cadastro',
    'assistido.id': 'Identificador do assistido', 'assistido.nome_tratamento': 'Nome pelo qual é tratado (fictício)',
    'assistido.ativo': 'Falso quando o atendimento encerra', 'assistido.criado_em': 'Data e hora do cadastro',
    'assistido_profissional.assistido_id': 'Assistido acompanhado', 'assistido_profissional.profissional_id': 'Profissional que acompanha',
    'assistido_profissional.data_inicio': 'Início do acompanhamento',
    'reuniao.id': 'Identificador da reunião', 'reuniao.data': 'Dia da reunião', 'reuniao.setor': 'Setor que realizou a reunião',
    'reuniao.criado_em': 'Data e hora do registro',
    'demanda.id': 'Identificador da demanda', 'demanda.descricao': 'Situação que exige articulação', 'demanda.categoria': 'Classificação em texto curto',
    'demanda.prioridade': 'Baixa, média ou alta', 'demanda.prazo': 'Data limite prevista', 'demanda.estado': 'Situação atual (domínio fechado)',
    'demanda.responsavel_id': 'Profissional responsável', 'demanda.reuniao_id': 'Reunião de origem', 'demanda.assistido_id': 'Assistido, quando houver',
    'demanda.criado_em': 'Abertura da demanda', 'demanda.atualizado_em': 'Última alteração; nas encerradas, o encerramento',
    'evolucao.id': 'Identificador da evolução', 'evolucao.assistido_id': 'Assistido da anotação', 'evolucao.profissional_id': 'Profissional autor',
    'evolucao.data': 'Dia do atendimento', 'evolucao.area_atuacao': 'Área (pedagógica, saúde...)', 'evolucao.descricao': 'Texto da anotação',
    'evolucao.ocorrido_em': 'Momento do lançamento', 'evolucao.retifica_id': 'Versão que esta evolução corrige',
}

# Explicação do processamento (ordem lógica de execução) e ligação com o sistema.
CONSULTAS = {
    'Q01': ('O banco lê a tabela <i>demanda</i> (FROM) e, no WHERE, testa cada linha: o padrão <code>%CRAS%</code> aceita qualquer texto antes e depois da palavra. Com OR, basta uma das duas condições ser verdadeira. O SELECT escolhe as colunas e o ORDER BY ordena pelo prazo, do menor para o maior.',
            'Busca textual na descrição das demandas (RF32), rota <code>GET /api/demandas?busca=</code>, card 19 do back-end.'),
    'Q02': ('FROM <i>reuniao</i>; o WHERE mantém só as linhas cujo setor está na lista do IN <b>e</b> cuja data está entre 01/10 e 31/10 (o BETWEEN inclui os dois extremos). O DATE_FORMAT só muda a exibição para dd/mm/aaaa, sem alterar o dado.',
            'Consulta de reuniões ordenadas por data, com filtro de período (RF07), rota <code>GET /api/reunioes</code>, card 18.'),
    'Q03': ('O WHERE descarta as demandas encerradas (NOT IN) e as de prazo futuro. Para cada linha que sobra, o SELECT calcula <code>DATEDIFF(CURDATE(), prazo)</code>, a diferença em dias entre hoje e o prazo. O ORDER BY usa o apelido do cálculo, em ordem decrescente.',
            'Destaque das demandas com prazo vencido no painel (RF30 e RF33), rota <code>GET /api/demandas/painel</code>, card 19.'),
    'Q04': ('Com a data do seminário, CURDATE() é 30/11/2026 e <code>ADDDATE(CURDATE(), INTERVAL 7 DAY)</code> é 07/12/2026. O BETWEEN mantém os prazos dentro dessa janela, só das demandas não encerradas, e o DATEDIFF mostra quantos dias faltam.',
            'Aviso, ao entrar no sistema, das demandas com prazo próximo do vencimento (RF40), card 25.'),
    'Q05': ('Cada INNER JOIN liga a demanda à linha correspondente da outra tabela pela chave estrangeira. Como é INNER, uma demanda sem assistido (assistido_id NULL) não encontra par e fica de fora. Depois da junção, o WHERE filtra a prioridade alta e o ORDER BY ordena pela data da reunião.',
            'Listagem de demandas com responsável, reunião e assistido (RF10, RF11 e RF31), rota <code>GET /api/demandas</code>, card 19.'),
    'Q06': ('O LEFT JOIN mantém <b>todos</b> os assistidos, mesmo sem demanda; nesses casos, as colunas de <i>demanda</i> vêm NULL. O WHERE <code>d.id IS NULL</code> mantém exatamente essas linhas "sem par", e <code>ativo = TRUE</code> exclui os desligados.',
            'Apoio à ficha do assistido (RF20): mostra quem está cadastrado e ainda não teve nenhuma demanda. Rota <code>GET /api/assistidos</code>, card 20.'),
    'Q07': ('A condição de estado está no ON, e não no WHERE: assim o filtro é aplicado na junção, e o profissional que só tem demandas encerradas continua na lista com NULL. O GROUP BY cria um grupo por usuário e <code>COUNT(d.id)</code> conta apenas valores não nulos, então quem não tem nada aparece com 0. Se a condição estivesse no WHERE, essas pessoas sumiriam do resultado.',
            'Demandas sob responsabilidade de cada usuário (RF34) e indicadores para a direção (RF39), rota <code>GET /api/demandas/minhas</code>, cards 19 e 24.'),
    'Q08': ('O WHERE deixa só as concluídas; o GROUP BY separa por prioridade; em cada grupo são calculados COUNT, AVG, MIN e MAX da diferença em dias entre abertura e conclusão. O HAVING filtra os <b>grupos</b> depois do cálculo: a prioridade alta, com média de 23,2 dias, sai do resultado. O WHERE não poderia fazer isso, porque roda antes do agrupamento e não enxerga o AVG. O ROUND deixa a média com uma casa decimal.',
            'Indicadores consolidados de demandas (RF39), card 24 (relatórios e indicadores).'),
    'Q09': ('A junção traz o setor da reunião para cada demanda. O GROUP BY usa duas colunas, então cada combinação setor e estado vira um grupo. A subconsulta <code>(SELECT COUNT(*) FROM demanda)</code> roda uma vez e devolve o total (29); o percentual é a quantidade do grupo vezes 100, dividida por esse total, arredondada.',
            'Painel com as demandas organizadas por estado (RF30) e indicadores por setor (RF39), cards 19 e 24.'),
    'Q10': ('YEAR() e MONTH() extraem partes da data de criação, e o GROUP BY usa essas partes, formando um grupo por mês. COUNT(*) conta as demandas do mês e <code>COUNT(DISTINCT categoria)</code> conta quantas categorias diferentes apareceram nele.',
            'Relatório de demandas por período (RF35), rota <code>GET /api/relatorios/demandas</code>, card 24.'),
    'Q11': ('A subconsulta roda primeiro e devolve <b>um único valor</b>: a menor data de criação entre as demandas em aberto. A consulta de fora compara cada linha com esse valor usando =, junta o responsável e calcula há quantos dias a demanda está aberta.',
            'Prioridade de cobrança no painel de demandas em aberto (RF30 e RF33), card 19.'),
    'Q12': ('A subconsulta do WHERE calcula uma vez a média de dias para concluir (24,9) e a consulta de fora mantém as concluídas acima dela. A subconsulta do SELECT repete a média só para exibi-la ao lado, como referência.',
            'Indicadores de desempenho no atendimento das demandas (RF39), card 24.'),
    'Q13': ('A subconsulta devolve uma <b>lista</b> com todos os profissionais que acompanham alguém. O NOT IN mantém os usuários que não estão nessa lista; o WHERE ainda exige usuário ativo e perfil diferente de direção.',
            'Gestão de usuários e distribuição de acompanhamentos pela direção (RF04), card 23.'),
    'Q14': ('A junção passa pela tabela associativa: usuário, depois assistido_profissional, depois assistido. O WHERE ignora assistidos desligados; o GROUP BY agrupa por profissional. COUNT conta os assistidos, AVG dos dias dividido por 30 dá a média em meses (ROUND), e FLOOR do maior tempo dividido por 365 dá os anos completos.',
            'Vínculo de acompanhamento entre profissionais e assistidos (RF20 e RF05), usado no controle de acesso às evoluções, cards 15 e 20.'),
    'Q15': ('É uma <b>autojunção</b>: a tabela <i>evolucao</i> aparece duas vezes, com os apelidos <i>original</i> e <i>nova</i>. O ON <code>nova.retifica_id = original.id</code> forma pares "versão corrigida e versão que a corrige". A cadeia 5, 16 e 17 gera duas linhas, porque a 16 corrige a 5 e a 17 corrige a 16.',
            'Retificação de evolução preservando a versão anterior (RF24 e RF26), rota <code>PATCH /api/evolucoes/&lt;id&gt;</code>, card 21.'),
    'Q16': ('A subconsulta lista as evoluções que já foram retificadas; o NOT IN as descarta, porque foram substituídas por uma versão nova. Depois, a junção com assistido, o GROUP BY por assistido e o MAX(data) dão a última evolução vigente de cada um. O HAVING mantém só os grupos cuja última evolução tem mais de 20 dias.',
            'Evoluções vigentes de cada assistido em ordem cronológica (RF23), rota <code>GET /api/assistidos/&lt;id&gt;/evolucoes</code>, card 21.'),
    'Q17': ('O RIGHT JOIN mantém todas as linhas da tabela da <b>direita</b> (reuniao), mesmo as que não casam com nenhuma demanda. Nesses casos as colunas de demanda vêm NULL e <code>COUNT(d.id)</code> resulta 0. Escrever <code>reuniao LEFT JOIN demanda</code> daria o mesmo resultado.',
            'Ficha da reunião com as demandas nela levantadas (RF07 e RF08), rota <code>GET /api/reunioes/&lt;id&gt;</code>, card 18.'),
}

NORMALIZACAO = [
    '<b>1FN:</b> todos os atributos são atômicos e não há grupos repetidos. Os vários profissionais de um assistido não ficam numa lista dentro de ASSISTIDO: viram linhas da tabela associativa ASSISTIDO_PROFISSIONAL.',
    '<b>2FN:</b> a única chave primária composta é a de ASSISTIDO_PROFISSIONAL (assistido_id, profissional_id), e seu único atributo, data_inicio, depende da chave inteira: é a data em que <i>aquele</i> profissional começou a acompanhar <i>aquele</i> assistido. Nas demais tabelas a chave é simples, então não há dependência parcial.',
    '<b>3FN:</b> não há dependência transitiva. O setor da demanda não é guardado em DEMANDA, porque é determinado pela reunião (reuniao_id determina setor); ele é obtido pela junção, como na consulta Q09. Nome e perfil do responsável ficam só em USUARIO. Não há campos calculados: dias de atraso, idade do acompanhamento e médias são calculados nas consultas.',
]
