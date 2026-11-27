# Notas do apresentador (tecla N): o que falar, conceitos da matéria e respostas prontas.
# Base: aulas de BD1 (Aula 02 Modelagem, 03 Transformação, 04 SQL, 05 Manipulação, 06 Agregação,
# 07 Ligação de tabelas, 08 Datas, 09 Normalização), os scripts 01 a 04 e o GUIA_APRESENTACAO.md.
import html

e = html.escape

# ------------------------------------------------------------------ conceitos (chave = rótulo do recurso no slide)
CONCEITOS = {
    'LIKE com %': 'Compara texto com um padrão. % vale qualquer sequência de caracteres (inclusive nenhuma) e _ vale exatamente um. \'%CRAS%\' acha CRAS em qualquer posição da descrição.',
    'OR': 'Basta uma das condições ser verdadeira. Se misturar com AND, use parênteses: o AND tem prioridade sobre o OR.',
    'ORDER BY': 'Ordena o resultado. ASC (o padrão) vai do menor para o maior; DESC, ao contrário. É a última etapa, por isso aceita os apelidos criados no SELECT.',
    'ORDER BY DESC': 'Ordena do maior para o menor. Aqui usa o apelido do SELECT, o que só funciona porque o ORDER BY roda depois do SELECT.',
    'IN': "Testa se o valor está numa lista. setor IN ('pedagogico', 'saude') é o mesmo que setor = 'pedagogico' OR setor = 'saude'.",
    'BETWEEN com datas': "Intervalo fechado: inclui os dois extremos. Com coluna DATE, BETWEEN '2026-10-01' AND '2026-10-31' pega o mês inteiro.",
    'BETWEEN': 'Intervalo fechado: inclui os dois extremos (o valor pode ser igual ao início ou ao fim).',
    'DATE_FORMAT': 'Só muda a exibição da data: %d dia, %m mês, %Y ano com 4 dígitos, %H hora, %i minutos. O valor guardado continua sendo data.',
    'CURDATE': 'A data de hoje, sem hora. No seminário os números saem com a data de 30/11/2026 (SET TIMESTAMP no início do 03).',
    'DATEDIFF': 'DATEDIFF(a, b) devolve quantos dias vão de b até a (a menos b), ignorando as horas. Dá positivo quando a é depois de b.',
    'ADDDATE + INTERVAL': 'Soma um intervalo a uma data: ADDDATE(CURDATE(), INTERVAL 7 DAY) é daqui a 7 dias, e o mês vira sozinho. DATE_ADD faz o mesmo.',
    'NOT IN': 'Verdadeiro quando o valor não está na lista. Cuidado: se a lista tiver um NULL, o NOT IN nunca dá verdadeiro.',
    'INNER JOIN de 4 tabelas': 'Cada INNER JOIN liga mais uma tabela pela condição do ON (chave estrangeira = chave primária). Linha sem par em qualquer uma delas sai do resultado.',
    'INNER JOIN': 'Junta as linhas das duas tabelas quando a condição do ON é verdadeira. Linha sem par sai do resultado.',
    'JOIN': 'JOIN sozinho é o mesmo que INNER JOIN: só ficam as linhas que têm par na outra tabela.',
    'apelidos (AS)': 'Nome curto para tabela (demanda d) ou para coluna (u.nome AS responsavel). Nas tabelas, tira a ambiguidade quando várias têm a coluna id.',
    'LEFT JOIN': 'Mantém todas as linhas da tabela da esquerda. Quando não há par na direita, as colunas da direita vêm NULL.',
    'LEFT JOIN com condição no ON': 'A condição extra fica no ON para escolher quais demandas entram no par sem eliminar o profissional. No WHERE, ela apagaria quem ficou sem par.',
    'IS NULL': 'Testa ausência de valor. NULL não é igual a nada, nem a outro NULL: "= NULL" nunca é verdadeiro, por isso existe IS NULL.',
    'COUNT(coluna)': 'COUNT(*) conta linhas; COUNT(coluna) conta só os valores que não são NULL. Depois de um LEFT JOIN, só o COUNT(coluna) dá 0 para quem não tem par.',
    'GROUP BY': 'Junta as linhas que têm o mesmo valor nas colunas indicadas e aplica as funções de agregação (COUNT, AVG, MIN, MAX, SUM) a cada grupo.',
    'GROUP BY com 2 colunas': 'Um grupo para cada combinação diferente das duas colunas: aqui, cada par (setor, estado).',
    'HAVING': 'Filtra grupos, depois do GROUP BY, por isso pode usar AVG, COUNT e MAX. O WHERE filtra linhas antes do agrupamento e não enxerga essas funções.',
    'AVG': 'Média dos valores do grupo (ignora NULL).',
    'ROUND': 'Arredonda: ROUND(x, 1) deixa uma casa decimal.',
    'MIN': 'Menor valor do grupo.',
    'MAX': 'Maior valor do grupo. Com datas, MAX é a mais recente.',
    'FLOOR': 'Arredonda para baixo: FLOOR(1,9) dá 1. Serve para contar anos completos.',
    'YEAR': 'Extrai o ano de uma data.',
    'MONTH': 'Extrai o mês (1 a 12) de uma data.',
    'COUNT(DISTINCT)': 'Conta valores diferentes, sem repetir. Também ignora NULL: categoria vazia não entra na conta.',
    'subconsulta no SELECT': 'Um SELECT dentro de outro. Esta devolve um único número (o total de demandas) e não depende da linha de fora, então o banco calcula uma vez só.',
    'subconsulta com MIN': 'A subconsulta devolve um único valor (a menor data de criação entre as abertas), que a consulta de fora compara com =.',
    'subconsulta com AVG': 'A subconsulta devolve um único valor, a média geral, que é calculada uma vez e usada para comparar cada linha.',
    'subconsulta que devolve lista': 'A subconsulta devolve uma coluna com vários valores; o NOT IN testa se o id está fora dessa lista.',
    'NOT IN com subconsulta': 'Descarta os ids que aparecem na lista devolvida pela subconsulta. A lista não pode ter NULL, por isso o IS NOT NULL dentro dela.',
    'JOIN pela associativa': 'Para atravessar um N:N, passa-se pela tabela associativa: usuario liga em assistido_profissional, que liga em assistido.',
    'autojunção': 'A mesma tabela entra duas vezes com apelidos diferentes (original e nova). É assim que se consulta um autorrelacionamento.',
    'RIGHT JOIN': 'O espelho do LEFT JOIN: mantém todas as linhas da tabela da direita. A JOIN B à direita é o mesmo que B LEFT JOIN A.',
}

# ------------------------------------------------------------------ extras por consulta
CONSULTA = {
    'q01': {
        'fala': 'Procuramos CRAS ou Conselho Tutelar dentro da descrição. O % do LIKE aceita qualquer texto antes e depois; com OR, basta aparecer um dos dois. A ordem é pelo prazo, da mais urgente para a menos urgente.',
        'perguntas': [('O LIKE diferencia maiúscula e acento?', 'Não neste banco: a collation utf8mb4_0900_ai_ci é ci (não diferencia maiúsculas) e ai (não diferencia acentos).')],
    },
    'q02': {
        'fala': 'O IN testa se o setor está na lista; o BETWEEN pega de 01/10 a 31/10, incluindo os dois dias; o DATE_FORMAT só muda como a data aparece, para o formato brasileiro.',
        'perguntas': [('E se a coluna fosse DATETIME?', "Aí '2026-10-31' valeria 31/10 à meia-noite e o resto do dia ficaria de fora. Como data é DATE, o mês vem inteiro.")],
    },
    'q03': {
        'fala': 'O WHERE tira as encerradas e fica só com prazo antes de hoje. O DATEDIFF(CURDATE(), prazo) dá o atraso em dias. A ordem é pelo apelido dias_de_atraso, da mais atrasada para a menos.',
        'atencao': ['O apelido dias_de_atraso funciona no ORDER BY (etapa 6) porque ele vem depois do SELECT (etapa 5). No WHERE (etapa 2) ele ainda não existe, por isso o filtro usa prazo < CURDATE().'],
    },
    'q04': {
        'fala': 'A janela vai de hoje até hoje mais 7 dias: ADDDATE(CURDATE(), INTERVAL 7 DAY). É o aviso que o painel mostra ao entrar. O DATEDIFF mostra quantos dias faltam.',
        'perguntas': [('Por que não CURDATE() + 7?', 'Porque em conta numérica CURDATE() vira o número 20261130, e somar 7 dá 20261137, que não é data. Com INTERVAL o banco soma dias de verdade e vira o mês.')],
    },
    'q05': {
        'fala': 'Quatro tabelas ligadas pelas chaves estrangeiras: demanda com reunião, com usuário (responsável) e com assistido. O INNER JOIN descarta a demanda sem assistido, porque assistido_id NULL não casa com nenhum id.',
        'perguntas': [('E para ver também as demandas sem assistido?', 'Troca o último INNER JOIN por LEFT JOIN: elas aparecem com assistido em NULL.')],
    },
    'q06': {
        'fala': 'O LEFT JOIN mantém todos os assistidos. Quem não tem demanda fica com as colunas de demanda em NULL, e o WHERE d.id IS NULL fica só com esses.',
        'perguntas': [('Dava para fazer sem JOIN?', 'Sim: a.id NOT IN (SELECT assistido_id FROM demanda WHERE assistido_id IS NOT NULL). O IS NOT NULL é obrigatório, porque assistido_id aceita NULL e um NULL na lista estragaria o NOT IN.')],
    },
    'q07': {
        'fala': 'O filtro de estado está no ON, não no WHERE: assim o profissional sem demanda aberta continua na lista. COUNT(d.id) não conta NULL e dá 0 para ele.',
        'atencao': ['O GROUP BY tem u.id, u.nome e u.perfil, e não só o id: o MySQL 8 usa ONLY_FULL_GROUP_BY, e toda coluna do SELECT fora de função de agregação precisa estar no agrupamento (ou depender da chave).'],
        'perguntas': [('O que aconteceria com o filtro no WHERE?', 'Para quem não tem demanda, d.estado é NULL; o WHERE descartaria essas linhas e os profissionais com zero sumiriam.')],
    },
    'q08': {
        'fala': 'O WHERE pega só as concluídas; o GROUP BY separa por prioridade; o HAVING fica com os grupos de média acima de 24 dias. A prioridade alta tem média 23,2 e sai.',
        'atencao': ['A data de conclusão usada é atualizado_em, que muda sozinha a cada UPDATE. Se uma concluída fosse editada depois, a medida mudaria; por isso o script 04 só reatribui demandas em aberto. No sistema completo, o histórico da demanda (fora do recorte) guarda a data exata.'],
        'perguntas': [('Por que não WHERE AVG(...) > 24?', 'Porque o WHERE roda antes do GROUP BY, quando ainda não existe média de grupo. Filtro sobre agregação é sempre HAVING.')],
    },
    'q09': {
        'fala': 'O GROUP BY usa duas colunas: um grupo para cada par setor e estado. O setor vem da reunião pela junção (é a 3FN na prática). A subconsulta devolve o total de demandas, 29, e cada grupo vira percentual desse total.',
        'atencao': ['No MySQL a barra / não faz divisão inteira: COUNT(*) * 100 / 29 já dá decimal. Divisão inteira seria DIV. O ROUND só deixa uma casa.'],
    },
    'q10': {
        'fala': 'YEAR e MONTH tiram o ano e o mês de criado_em; o GROUP BY forma um grupo por mês. COUNT(*) conta as demandas do mês e COUNT(DISTINCT categoria) conta quantas categorias diferentes apareceram.',
    },
    'q11': {
        'fala': 'A subconsulta devolve um único valor: a menor data de criação entre as demandas abertas. A consulta de fora pega a demanda com essa data, junta o responsável e calcula há quantos dias ela está aberta.',
        'atencao': ['Se duas demandas tivessem exatamente a mesma data, as duas apareceriam. A subconsulta não usa nada da consulta de fora (não é correlacionada), então roda uma vez só.'],
    },
    'q12': {
        'fala': 'A subconsulta calcula a média de dias das concluídas, 24,9, uma vez só; ficam as concluídas que levaram mais do que isso. A mesma subconsulta aparece no SELECT só para mostrar a média ao lado.',
    },
    'q13': {
        'fala': 'A subconsulta devolve a lista de profissionais que já acompanham alguém; o NOT IN fica com quem está fora dela. A direção fica de fora com perfil <> \'direcao\': a consulta procura profissionais para receber novos acompanhamentos.',
        'atencao': ['Aqui o NOT IN é seguro: profissional_id faz parte da chave primária de assistido_profissional e nunca é NULL. Compare com a Q16.'],
    },
    'q14': {
        'fala': 'Para atravessar o N:N passamos pela tabela associativa. Para cada profissional: quantos assistidos acompanha, a média de tempo em meses (dias divididos por 30) e quantos anos completos tem o vínculo mais antigo (FLOOR).',
        'atencao': ['Dividir por 30 é uma aproximação de mês. TIMESTAMPDIFF(MONTH, data_inicio, CURDATE()) contaria meses de calendário completos.'],
    },
    'q15': {
        'fala': 'Autojunção: a tabela evolucao entra duas vezes, como original e como nova, ligadas por nova.retifica_id = original.id. Cada linha mostra o texto antigo ao lado da correção e quantos dias depois ela foi feita.',
        'atencao': ['É o 1:1 aparecendo no resultado: como retifica_id é UNIQUE, cada versão aparece corrigida no máximo uma vez.'],
    },
    'q16': {
        'fala': 'Só contam as evoluções vigentes: o NOT IN descarta as versões que já foram substituídas. Depois agrupamos por assistido e o HAVING fica com quem tem a última evolução há mais de 20 dias.',
        'atencao': ['O IS NOT NULL dentro da subconsulta é obrigatório. Quase todas as evoluções têm retifica_id NULL; se um NULL entrar na lista, "x NOT IN (..., NULL)" dá desconhecido para todo x e a consulta volta vazia. É a lógica de três valores do SQL: verdadeiro, falso e desconhecido.'],
    },
    'q17': {
        'fala': 'O RIGHT JOIN mantém todas as reuniões, mesmo as que não originaram demanda. COUNT(d.id) dá 0 para elas, porque não conta NULL.',
        'perguntas': [('RIGHT JOIN é obrigatório aqui?', 'Não: reuniao LEFT JOIN demanda dá o mesmo resultado. Usamos o RIGHT para mostrar o comando.')],
    },
}

def acao(chave):
    if 'JOIN' in chave:
        return 'liga as linhas pela condição do ON'
    return {'FROM': 'lê a tabela', 'WHERE': 'mantém só as linhas em que a condição é verdadeira',
            'GROUP BY': 'forma um grupo para cada valor diferente de', 'HAVING': 'mantém só os grupos em que',
            'SELECT': 'calcula as colunas do resultado', 'ORDER BY': 'ordena por'}[chave]

# ------------------------------------------------------------------ notas dos outros slides
FN_DEF = [
    ('Normalização (Aula 09)', 'Processo de organizar os dados para reduzir redundância, evitar anomalias de inserção, atualização e exclusão e garantir integridade lógica.'),
    ('Dependência funcional', 'A depende funcionalmente de B quando cada valor de B determina um único valor de A. Ex.: reuniao.id determina setor.'),
    ('1FN', 'Para cada chave primária, uma única informação em cada atributo: nada de grupo repetitivo (multivalorado). Lista vira linhas de outra tabela.'),
    ('2FN', 'Estar na 1FN e não ter atributo com dependência parcial: quando a chave é composta, todo atributo precisa depender da chave inteira, não só de uma parte.'),
    ('3FN', 'Estar na 2FN e não ter dependência transitiva: nenhum atributo pode depender de outro atributo que não é chave (não pode haver um intermediário entre a chave e o atributo). Também não se guarda atributo calculado.'),
]

OUTROS = {
    'capa': {
        'fala': 'Boa noite. Somos a equipe Cortex. Nosso projeto interdisciplinar é com o CRIE, o Centro de Integração Especial de Extrema (MG). Em 20 minutos vamos mostrar o banco das demandas de articulação: como modelamos, como criamos e populamos e as 17 consultas. Cada integrante se apresenta ao começar a sua parte.',
        'conceitos': [('Projeto interdisciplinar', 'O mesmo CRIE é o projeto de Extensão, de Engenharia de Software e do sistema; em BD1 implementamos o núcleo do banco dele.')],
    },
    'roteiro': {
        'fala': 'São cinco partes: abertura com o CRIE e o recorte; modelagem e scripts; as 17 consultas; manutenção dos dados e o sistema; perguntas. Na parte das consultas, todos falam: cada integrante explica o processamento de 3 ou 4 consultas, como o enunciado pede.',
    },
    'crie': {
        'fala': 'O CRIE atende pessoas com deficiência e se organiza em três setores. Cada setor faz uma reunião semanal; ali aparecem as demandas de articulação: situações que não se resolvem só com os recursos internos e pedem providências com famílias, profissionais ou a rede pública (CRAS, saúde, escola, Conselho Tutelar). O banco precisa garantir três coisas: de onde a demanda veio, em que pé ela está e o histórico.',
        'conceitos': [('Universo de discurso (minimundo)', 'A descrição em texto da parte do mundo real que o banco representa: quem são os envolvidos, o que se registra e quais regras valem. É dele que saem entidades, atributos e restrições.')],
    },
    'regras': {
        'fala': 'Cada regra do minimundo virou uma restrição que o próprio MySQL garante. Não depende de quem digita: se alguém tentar quebrar a regra, o banco recusa.',
        'conceitos': [('NOT NULL', 'O campo é obrigatório.'), ('DEFAULT', 'Valor usado quando o INSERT não informa a coluna.'),
                      ('UNIQUE', 'Não deixa repetir o valor na tabela (dois usuários com o mesmo e-mail).'),
                      ('Chave estrangeira e integridade referencial (Aula 03)', 'A FK é um atributo cujo valor corresponde à chave primária de outra tabela. Integridade referencial: quando a FK tem valor, ele aponta para uma linha que existe.'),
                      ('ENUM', 'Domínio fechado: só os valores listados. No MySQL 8, com o modo estrito ligado (o padrão), um valor fora da lista dá erro.')],
    },
    'recorte': {
        'fala': 'O DER do sistema (versão 2.0) tem 13 entidades. O enunciado pede de 4 a 6 tabelas, então implementamos o núcleo: 5 entidades (usuário, assistido, reunião, demanda, evolução) e a tabela associativa do N:N acompanha. Setor e Categoria viraram colunas. As outras 6 ficaram fora.',
        'conceitos': [('A conta', '13 entidades = 5 que viraram tabelas + 2 que viraram colunas (Setor e Categoria) + 6 fora. A sexta tabela, assistido_profissional, vem do relacionamento N:N, não de uma entidade.')],
        'perguntas': [('Por que só 6 tabelas?', 'O enunciado de BD1 pede de 4 a 6. Serviço da Rede, Encaminhamento, Ação, Retorno, Histórico e Auditoria continuam no sistema, fora desta entrega.'),
                      ('Por que Setor virou coluna?', 'No recorte, o setor só precisa de três valores fixos, então virou ENUM em reuniao. No sistema completo ele é tabela, com nome e situação.')],
    },
    'der': {
        'fala': 'Leia pelos verbos: a reunião origina demandas; o usuário responde por demandas e acompanha assistidos; o assistido possui evoluções, que o usuário escreve; e uma evolução retifica outra. O quadro no canto explica como ler os pares, como na Aula 02.',
        'conceitos': [('Entidade', 'Retângulo: algo sobre o que guardamos dados (REUNIÃO, DEMANDA).'), ('Relacionamento', 'Losango: a associação entre entidades, nomeada por um verbo.'),
                      ('Cardinalidade (mín, máx), Aula 02', 'Notação de Elmasri, a mesma da Figura 7.15 da Aula 02: o par junto a cada entidade diz de quantas ocorrências do relacionamento cada ocorrência dela participa. Em origina, DEMANDA (1,1): cada demanda nasce em exatamente uma reunião; REUNIÃO (0,N): uma reunião origina nenhuma, uma ou várias demandas.'),
                      ('E o 1:N?', 'Os máximos dão o tipo: DEMANDA participa no máximo 1 vez e REUNIÃO até N vezes, então é 1:N, com a FK no lado da demanda.'),
                      ('Atributo de relacionamento', 'data_inicio pertence ao "acompanha": é a data em que aquele profissional começou com aquele assistido. No banco, vira coluna da tabela associativa.'),
                      ('Autorrelacionamento', 'A entidade se relaciona com ela mesma: EVOLUÇÃO retifica EVOLUÇÃO, com os papéis versão corrigida e nova versão.')],
        'perguntas': [('Onde estão os atributos?', 'Na notação textual e no dicionário, nos próximos slides, e no DER completo do documento.')],
    },
    'rel': {
        'fala': 'Mapeamos cada relacionamento com as regras da Aula 03: 1:N vira chave estrangeira no lado N; N:N vira tabela associativa com chave primária composta; o 1:1 ficou como chave estrangeira com UNIQUE.',
        'conceitos': [('1:N (Aula 03)', 'Adiciona a FK na tabela do lado N: reuniao_id fica em demanda.'),
                      ('1:N opcional', 'Quando o lado 1 é opcional, a FK aceita NULL: assistido_id em demanda (demanda institucional não tem assistido).'),
                      ('N:N (Aula 03)', 'Cria uma tabela associativa com as duas FKs, que juntas formam a chave primária composta; pode ter atributos próprios (data_inicio).'),
                      ('1:1 (Aula 03)', 'Junta as tabelas ou adiciona uma FK. Aqui é autorrelacionamento, então é FK para a própria tabela, e o UNIQUE garante o máximo 1.')],
        'perguntas': [('Onde está o 1:1?', 'Evolução retifica evolução. Sem o UNIQUE em retifica_id, uma versão poderia ser corrigida várias vezes e seria 1:N.')],
    },
    'notacao': {
        'fala': 'A notação textual é o modelo relacional escrito: o nome da tabela e as colunas entre parênteses. Sublinhado é chave primária; em itálico, chave estrangeira. Na AssistidoProfissional as duas FKs são, juntas, a chave primária.',
        'conceitos': [('Chave primária (PK)', 'Identifica cada linha; não repete e não é nula.'), ('Chave composta', 'PK formada por mais de uma coluna: o par (assistido_id, profissional_id) não se repete.'),
                      ('Chave estrangeira (FK)', 'Coluna que aponta para a PK de outra tabela (ou da mesma, como retifica_id).')],
    },
    'fn': {
        'fala': 'As tabelas estão na terceira forma normal. Primeira: nenhum campo guarda lista. Segunda: na única chave composta, data_inicio depende das duas colunas juntas. Terceira: o setor da demanda não é copiado na demanda, vem da reunião pela junção.',
        'conceitos': FN_DEF,
        'atencao': ['Exemplos de como seria errado: 1FN quebrada seria uma coluna profissionais com "Ana, Bruno" dentro de assistido. 2FN quebrada seria o nome do profissional dentro de assistido_profissional (depende só de profissional_id, parte da chave). 3FN quebrada seria setor dentro de demanda (depende de reuniao_id, que não é a chave da demanda).'],
        'perguntas': [('As tabelas estão normalizadas?', 'Sim, em 3FN: sem grupos repetidos, sem dependência parcial e sem transitiva. Dias de atraso e médias são calculados nas consultas, não guardados.')],
    },
    'dic': {
        'fala': 'Estas são as seis tabelas como o script 01 cria. O enunciado pede tipos numérico, texto e data: INT e BOOLEAN; VARCHAR, TEXT e ENUM; DATE e DATETIME. PK, FK e UQ marcam as chaves; NULL marca o que é opcional.',
        'conceitos': [('VARCHAR(n) e TEXT', 'VARCHAR guarda texto até n caracteres; TEXT, texto longo (a descrição).'),
                      ('DATE e DATETIME', 'DATE só a data (prazo); DATETIME data e hora (criado_em).'), ('BOOLEAN', 'No MySQL vira TINYINT(1): TRUE é 1 e FALSE é 0.'),
                      ('AUTO_INCREMENT', 'O banco gera o próximo id sozinho.'),
                      ('Detalhes', 'email é VARCHAR(254), o tamanho máximo de um e-mail; senha_hash guarda o SHA2 de 256 bits (64 caracteres).')],
    },
    's01': {
        'fala': 'O script 01 roda do zero: apaga o banco se existir, cria de novo e cria as tabelas, cada uma depois das tabelas que ela referencia. No fim, o ALTER TABLE acrescenta a FK da evolução para ela mesma e o UNIQUE que faz o 1:1.',
        'conceitos': [('DDL', 'Comandos que definem a estrutura: CREATE, ALTER, DROP (Aula 04).'),
                      ('utf8mb4', 'UTF-8 completo, para acentos. O antigo utf8 do MySQL guarda só até 3 bytes por caractere.'),
                      ('ON UPDATE CASCADE', 'Se a PK referenciada mudar, a FK acompanha. Na associativa também há ON DELETE CASCADE: o vínculo some junto com a ponta.')],
        'perguntas': [('Por que a FK do 1:1 foi criada com ALTER TABLE?', 'O enunciado pede scripts com create, drop e alter; e a FK aponta para a própria tabela, então criamos a tabela e depois acrescentamos a restrição. Também daria para declarar dentro do CREATE TABLE.')],
    },
    's02': {
        'fala': 'O script 02 insere 103 registros fictícios. A ordem respeita as chaves estrangeiras: cada tabela entra depois das que ela referencia (usuário, assistido, vínculo, reunião, demanda e evolução). Os dados foram montados para toda consulta ter resultado: os 5 estados, as 3 prioridades e prazos vencidos, próximos e futuros.',
        'conceitos': [('DML', 'Comandos que mexem nos dados: INSERT, UPDATE, DELETE (Aula 05).'), ('SHA2', 'A senha entra como SHA2(texto, 256): nenhuma senha fica legível no banco.')],
    },
    'mapa': {
        'fala': 'Visão geral das 17 consultas. Cada coluna é um recurso; o quadrado diz que a consulta usa. O enunciado pede no mínimo 12 diferentes, com datas ou cálculo, junção e GROUP BY. A cor da linha é a do bloco de quem apresenta: cada integrante explica 3 ou 4.',
    },
    'ordem': {
        'fala': 'Esta é a frase que serve para qualquer consulta: primeiro o FROM e os JOIN montam as linhas (etapa 1); o WHERE filtra linha a linha (2); o GROUP BY junta em grupos (3); o HAVING filtra os grupos (4); o SELECT calcula as colunas (5); e o ORDER BY ordena (6).',
        'atencao': ['Consequência que vale citar: o apelido criado no SELECT funciona no ORDER BY (que vem depois), mas não no WHERE (que vem antes).'],
        'conceitos': [('Ordem lógica', 'É a ordem em que o resultado é definido, não a ordem em que se escreve. O otimizador pode executar de outro jeito, mas o resultado é sempre o desta ordem.')],
    },
    's04': {
        'fala': 'O script 04 faz a manutenção do dia a dia sem perder histórico: insere sem informar o estado (o DEFAULT faz nascer aberta), muda estado, reatribui responsável, desativa usuário em vez de apagar e remove um vínculo lançado por engano. Por fim, mostra que o banco recusa apagar uma reunião que tem demandas.',
        'conceitos': [('Erro 1451', 'A FK de demanda para reunião não tem ON DELETE CASCADE: apagar a reunião deixaria demandas órfãs, então o MySQL recusa.'),
                      ('ON UPDATE CURRENT_TIMESTAMP', 'atualizado_em muda sozinho a cada UPDATE na linha.'),
                      ('UPDATE sem WHERE', 'Altera todas as linhas da tabela. Por isso todo UPDATE e DELETE do script tem WHERE.')],
        'perguntas': [('Por que não apagar o usuário?', 'Para não perder a autoria das demandas e evoluções antigas: ele é desativado (ativo = FALSE).')],
    },
    'sistema': {
        'fala': 'O banco desta disciplina usa os mesmos nomes de tabelas e colunas do back-end em Flask. As consultas não são só exercício: Q03 e Q11 são o painel de vencidas, Q04 é o aviso de prazo ao entrar, Q07 é minhas demandas, Q15 e Q16 são a retificação de evolução, e Q08, Q09, Q10 e Q12 são os relatórios da direção.',
        'conceitos': [('ORM', 'No back-end, o SQLAlchemy gera o SQL a partir das classes Python; as tabelas por trás são estas.')],
        'atencao': ['A tela é do protótipo do sistema, com dados fictícios.'],
    },
    'criterios': {
        'fala': 'Para fechar: cada critério do enunciado e onde está no deck. A entrega no Moodle é o PDF no padrão ABNT e os quatro scripts .sql comentados, num .zip que cada integrante envia.',
    },
    'fim': {
        'fala': 'Obrigado. Abrimos para perguntas.',
        'perguntas': [
            ('Diferença entre WHERE e HAVING?', 'WHERE filtra linhas antes do agrupamento; HAVING filtra grupos depois, por isso pode usar AVG e COUNT (Q08 e Q16).'),
            ('Diferença entre INNER e LEFT JOIN?', 'INNER só traz o que casa nas duas tabelas; LEFT traz tudo da esquerda e completa com NULL (Q05 e Q06).'),
            ('COUNT(*) ou COUNT(coluna)?', 'COUNT(*) conta linhas; COUNT(coluna) ignora NULL. Com LEFT JOIN, só o segundo dá zero para quem não tem nada (Q07 e Q17).'),
            ('Por que ENUM no estado?', 'O estado é um domínio fechado: o banco recusa qualquer valor fora da lista.'),
            ('Por que o assistido só tem nome de tratamento?', 'Minimização de dados da LGPD: guardamos só o necessário. Todos os dados são fictícios.'),
            ('Como sabem o tempo para concluir?', 'DATEDIFF(atualizado_em, criado_em): na demanda concluída, atualizado_em é o dia do encerramento.'),
            ('Como rodar ao vivo?', "MySQL Workbench: 01, 02 e a consulta pedida do 03. Para os mesmos números, antes SET TIMESTAMP = UNIX_TIMESTAMP('2026-11-30 19:00:00')."),
        ],
    },
}


def _bloco(titulo, corpo):
    return f'<section class="n-bloco"><h4>{titulo}</h4>{corpo}</section>'


def _lista_def(pares):
    return '<dl>' + ''.join(f'<dt>{e(a)}</dt><dd>{e(b)}</dd>' for a, b in pares) + '</dl>'


def _lista(itens):
    return '<ul>' + ''.join(f'<li>{e(i)}</li>' for i in itens) + '</ul>'


def montar(ident, parte, extra=None):
    """HTML das notas de um slide. extra: dados da consulta (enunciado, passos, resultado, chips)."""
    esq, dir_ = [], []
    if extra:  # slide de consulta
        c = CONSULTA[ident]
        esq.append(_bloco('A pergunta', f'<p>{e(extra["enunciado"])}</p>'))
        esq.append(_bloco('O que falar', f'<p>{e(c["fala"])}</p>'))
        passos = ''.join(f'<li><b>{n}. {e(k)}</b> {e(acao(k))}: <code>{e(t)}</code></li>' for n, k, t in extra['passos'])
        esq.append(_bloco('Passo a passo, na ordem em que o banco processa', f'<ol class="passos">{passos}</ol>'))
        esq.append(_bloco('O resultado', f'<p>{e(extra["resultado"])}</p>'))
        dir_.append(_bloco('Conceitos', _lista_def([(ch, CONCEITOS[ch]) for ch in extra['chips']])))
        if c.get('atencao'):
            dir_.append(_bloco('Detalhe técnico', _lista(c['atencao'])))
        if c.get('perguntas'):
            dir_.append(_bloco('Se perguntarem', _lista_def(c['perguntas'])))
    elif ident.startswith('parte'):
        esq.append(_bloco('O que falar', f'<p>Passagem. Quem apresenta a parte {parte} diz o nome e o que vai mostrar: {e(extra_parte(parte))}.</p>'))
    else:
        o = OUTROS[ident]
        esq.append(_bloco('O que falar', f'<p>{e(o["fala"])}</p>'))
        if o.get('atencao'):
            esq.append(_bloco('Detalhe técnico', _lista(o['atencao'])))
        if o.get('conceitos'):
            dir_.append(_bloco('Conceitos', _lista_def(o['conceitos'])))
        if o.get('perguntas'):
            dir_.append(_bloco('Se perguntarem', _lista_def(o['perguntas'])))
    return f'<div class="n-esq">{"".join(esq)}</div><div class="n-dir">{"".join(dir_)}</div>'


_PARTES_TXT = {}


def extra_parte(n):
    return _PARTES_TXT.get(n, '')


def texto_puro(html_):
    """Para conferir travessões nas notas."""
    import re
    return html.unescape(re.sub(r'<[^>]+>', ' ', html_))
