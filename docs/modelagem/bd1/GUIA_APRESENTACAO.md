# Seminário de Banco de Dados I: roteiro de 20 minutos

Seminário em 30/11/2026. Entrega no Moodle até 29/11/2026, 23:59: **cada integrante sobe o mesmo .zip com o próprio login**.

Critério que mais pesa na fala: o enunciado diz que "os estudantes deverão explicar o processamento das consultas". Cada um precisa saber explicar as próprias consultas sem ler.

## Divisão sugerida (a equipe ajusta)

| Tempo | Quem | Slides | Conteúdo |
|---|---|---|---|
| 0:00 a 2:00 | Vinícius | 1 a 5 | Capa, roteiro, o CRIE e o problema, regras que viram restrições, recorte de 6 tabelas |
| 2:00 a 5:30 | Henry | 6 a 13 | DER, os 7 relacionamentos, notação textual, 3FN, dicionário, scripts 01 e 02 |
| 5:30 a 9:30 | Inácio | 14 a 21 | Mapa das 17 consultas, ordem de processamento, Q01 a Q05 (seleção, datas, INNER JOIN) |
| 9:30 a 13:30 | Gabriel | 22 a 28 | Q06 a Q11 (LEFT JOIN, GROUP BY, HAVING, subconsulta) |
| 13:30 a 18:30 | Miguel | 29 a 38 | Q12 a Q17, script 04 (manutenção), do banco ao sistema, critérios do enunciado |
| 18:30 a 20:00 | Todos | 39 | Perguntas |

Os slides 6, 14, 22 e 29 são de passagem: mostram a parte e o tempo do bloco. Os slides não trazem nomes (nem da equipe nem da professora): cada um se apresenta ao começar a sua parte.

## Como usar o deck

- Abrir `deck/index.html` no navegador. Funciona sem internet: fontes, logos e imagem estão dentro do arquivo.
- **F** tela cheia · **seta direita, espaço ou clique** avança · **seta esquerda** volta · **Home/End** primeiro e último · **N** mostra as notas de quem fala (o enunciado completo de cada consulta e a explicação).
- Em cada consulta, o número colorido ao lado de cada cláusula é a etapa em que o MySQL a processa (1 FROM, 2 JOIN, 3 WHERE, 4 GROUP BY, 5 HAVING, 6 SELECT, 7 ORDER BY). É a deixa para a fala.
- Reserva: `deck/Seminario_BD1_Equipe_Cortex.pdf`, com os mesmos 39 slides.

Se a professora pedir para rodar ao vivo: abrir o MySQL Workbench, executar `01`, `02` e depois a consulta pedida do `03`. As consultas com `CURDATE()` dão números diferentes conforme o dia; para reproduzir os do documento, rodar antes `SET TIMESTAMP = UNIX_TIMESTAMP('2026-11-30 19:00:00');`.

## A frase que serve para qualquer consulta

"O banco processa nesta ordem: primeiro FROM e os JOIN, que montam as linhas; depois o WHERE filtra linha a linha; o GROUP BY junta em grupos; o HAVING filtra os grupos; o SELECT calcula as colunas; e o ORDER BY ordena."

## Falas por consulta (curtas, para decorar a ideia, não o texto)

- **Q01** LIKE com `%` aceita qualquer texto antes e depois. OR: basta uma condição.
- **Q02** IN testa uma lista; BETWEEN inclui os dois extremos; DATE_FORMAT só muda a exibição.
- **Q03** WHERE tira encerradas e prazos futuros; DATEDIFF(hoje, prazo) dá o atraso; ordena pelo apelido.
- **Q04** Janela de hoje até `ADDDATE(CURDATE(), INTERVAL 7 DAY)`.
- **Q05** Quatro tabelas pelas FKs. O INNER descarta a demanda sem assistido, porque NULL não casa.
- **Q06** LEFT JOIN mantém todos os assistidos; `IS NULL` acha quem não tem demanda.
- **Q07** Filtro no ON, não no WHERE, para não perder quem tem zero. `COUNT(d.id)` não conta NULL.
- **Q08** HAVING filtra grupos depois do AVG; o WHERE não enxerga o AVG. A prioridade alta (23,2) sai.
- **Q09** GROUP BY com duas colunas; a subconsulta devolve o total (29) para o percentual.
- **Q10** YEAR e MONTH formam um grupo por mês; `COUNT(DISTINCT categoria)`.
- **Q11** A subconsulta devolve um valor (MIN), comparado com `=`.
- **Q12** A subconsulta calcula a média (24,9) uma vez; ficam as concluídas acima dela.
- **Q13** A subconsulta devolve uma lista; NOT IN mantém quem não está nela.
- **Q14** Passa pela tabela associativa do N:N; AVG/30 em meses com ROUND; FLOOR para anos completos.
- **Q15** Autojunção: a mesma tabela duas vezes (`original` e `nova`), ligadas por `retifica_id`. É o 1:1.
- **Q16** NOT IN descarta as versões já substituídas; HAVING sobre `MAX(data)`.
- **Q17** RIGHT JOIN mantém todas as reuniões; as sem demanda contam 0.

## Parte do Miguel: o banco dentro do sistema

"O banco desta disciplina usa os mesmos nomes de tabelas e colunas do back-end em Flask. As consultas não são só exercício: Q03 e Q11 são o painel de vencidas, Q04 é o aviso de prazo próximo no login, Q07 é a tela 'minhas demandas', Q15 e Q16 são a retificação de evolução, e Q08, Q09, Q10 e Q12 são os indicadores dos relatórios da direção."

## Perguntas prováveis da professora

| Pergunta | Resposta curta |
|---|---|
| Onde está o 1:1? | Evolução retifica evolução. `retifica_id` é FK para a própria tabela, com UNIQUE: cada versão só pode ser corrigida uma vez. Sem o UNIQUE seria 1:N. |
| E o N:N? | Profissional acompanha assistido. Virou a tabela `assistido_profissional`, com PK composta e o atributo `data_inicio`. |
| Por que a FK do 1:1 foi criada com ALTER TABLE? | Porque ela aponta para a própria tabela: criamos a tabela e depois acrescentamos a restrição, como na Aula 04. |
| Por que só 6 tabelas, se o DER da equipe tem 12 entidades? | O enunciado de BD1 pede de 4 a 6. Implementamos o recorte central; encaminhamento, histórico e auditoria ficaram fora. |
| Por que ENUM no estado? | O estado é um domínio fechado (regra do minimundo): o banco recusa qualquer valor fora da lista. |
| Diferença entre WHERE e HAVING? | WHERE filtra linhas antes do agrupamento; HAVING filtra grupos depois, por isso pode usar AVG e COUNT. (Q08 e Q16) |
| Diferença entre INNER e LEFT JOIN? | INNER só traz o que casa nas duas tabelas; LEFT traz tudo da esquerda e completa com NULL. (Q05 e Q06) |
| COUNT(*) ou COUNT(coluna)? | COUNT(*) conta linhas; COUNT(coluna) ignora NULL. Com LEFT JOIN, só o segundo dá zero para quem não tem nada. (Q07 e Q17) |
| As tabelas estão normalizadas? | Sim, em 3FN: sem grupos repetidos, sem dependência parcial (a única PK composta só tem `data_inicio`, que depende das duas colunas) e sem transitiva (o setor da demanda vem da reunião, não é copiado). |
| Por que não dá para apagar uma reunião? | A FK de demanda para reunião não tem CASCADE: o banco recusa (erro 1451) para não deixar demanda órfã. |
| Por que a senha é um hash? | Regra de proteção de dados: nenhuma senha fica legível. Na carga usamos `SHA2(..., 256)`. |
| Por que o assistido só tem nome de tratamento? | Minimização de dados da LGPD: guardamos só o necessário. Todos os dados são fictícios. |
| Como sabe o tempo para concluir? | `atualizado_em` guarda a última alteração; na demanda concluída, é o dia do encerramento. DATEDIFF(atualizado_em, criado_em). |

## Antes do seminário (checklist)

- [ ] Cada integrante leu o documento e treinou as próprias consultas.
- [ ] Rodar os quatro scripts no MySQL Workbench de quem vai apresentar.
- [ ] Ensaiar com cronômetro: 20 minutos.
- [ ] Os cinco enviaram o .zip no Moodle até 29/11, 23:59.
