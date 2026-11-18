# Cenários de uso

Frente de IHC. Cartão "Escrever cenários de uso a partir das personas" (backlog no relatório v3, §3.2.4).

Persona + **cenário de uso** (Aula 04): a persona diz *quem*; o cenário conta *em que situação, com que objetivo e por quais passos* ela usa o sistema. Cada cenário daqui vira uma ou mais tarefas do teste de usabilidade (`plano-de-testes.md`, coluna "Tarefa").

Correções do relatório v3 (Quadro 12) já aplicadas:
- **Não há cenário de relatório para a Prefeitura**: o requisito saiu do escopo. No lugar dele entrou o cenário C2, consultar o que já foi feito quando uma demanda se repete.
- **Acesso aberto**: todo profissional ativo vê todas as demandas e os assistidos (decisão da direção no relatório v2). A auditoria registra quem consultou. Nenhum cenário supõe tela escondida por setor.

Todos os nomes de pessoas atendidas e de profissionais são **fictícios** e iguais aos da carga de demonstração (`backend/seed.py`): Bruna Fictícia (assistente social), Carlos Fictício (equipe pedagógica), Assistido Fictício A e B.

---

## Quadro-resumo

| # | Persona | Objetivo | Requisitos | Tarefa de teste |
| --- | --- | --- | --- | --- |
| C1 | P1 Direção | Começar o dia vendo o que está atrasado e cobrar quem precisa | RF30, RF33, RF16 | T1, T6 |
| C2 | P1 Direção | Achar o que já foi feito numa demanda que voltou a aparecer | RF31, RF32, RF17 | T2 |
| C3 | P2 Assistente social | Registrar a demanda que saiu da reunião de saúde | RF10, RF11, RNF12, RNF16 | T3 |
| C4 | P2 Assistente social | Atualizar o andamento e registrar o encaminhamento à rede | RF13, RF15, RF27 | T4 |
| C5 | P3 Equipe pedagógica | Entrar, ver o aviso de prazo e concluir a própria demanda | RF40, RF34, RF13 | T5 |
| C6 | P3 Equipe pedagógica | Lançar a evolução de um assistido depois da oficina | RF21, RF20 | T7 |

---

## C1 — Júlia começa a semana pelo painel

**Quem:** Júlia Costa, diretora (P1).
**Contexto:** segunda-feira de manhã, antes da reunião do setor de saúde. Computador da sala da direção; a internet às vezes cai.
**Objetivo:** saber, sem procurar em papel, quais demandas estão atrasadas e quem é responsável por elas.

**Passo a passo:**
1. Abre o sistema e entra com e-mail e senha.
2. Cai direto no **Painel**. No topo, vê o total de demandas em aberto e quantas estão **vencidas**.
3. Nas colunas Aberta, Em andamento e Aguardando terceiros, as vencidas aparecem primeiro, com o selo "Vencida".
4. Vê que "Agendar avaliação fonoaudiológica na rede municipal" está vencida e com Bruna Fictícia, que está de férias.
5. Abre a demanda, escolhe **Trocar responsável**, seleciona outro profissional e confirma.
6. O histórico mostra a troca, com o nome dela e o horário.

**O que o cenário exige da interface:** painel como tela inicial; vencida marcada com texto, não só cor; troca de responsável a dois cliques do painel; histórico visível na mesma tela.

## C2 — A demanda que se repete

**Quem:** Júlia Costa (P1).
**Contexto:** na reunião do setor de convivência, alguém lembra que "já pedimos material adaptado para a turma da tarde no mês passado". Ninguém lembra o que aconteceu.
**Objetivo:** encontrar a demanda antiga e ler o histórico em menos de um minuto (critério de aceitação 2, `requisitos.md` §8).

**Passo a passo:**
1. No menu, abre **Demandas**.
2. Escreve "material adaptado" na busca.
3. A lista mostra a demanda, com estado e responsável. Se ela já tiver sido concluída ou cancelada, a busca a encontra do mesmo jeito.
4. Abre a demanda e lê o histórico: quem mudou o estado, quando, e as anotações.
5. Decide, com a equipe, se registra uma demanda nova ou se reabre o assunto numa anotação.

**O que o cenário exige:** busca por trecho da descrição; filtros visíveis mas opcionais; histórico em ordem cronológica, legível por quem não estava na reunião anterior.

## C3 — Bruna registra a demanda logo depois da reunião

**Quem:** Bruna Fictícia, assistente social (P2), com pouca familiaridade com tecnologia.
**Contexto:** acabou a reunião do setor de saúde. Bruna tem as anotações em papel e dez minutos antes do próximo atendimento.
**Objetivo:** registrar a demanda "Solicitar ao CAPSi vaga para avaliação" sem pedir ajuda.

**Passo a passo:**
1. No painel, clica em **Registrar demanda**.
2. Preenche a descrição, escolhe a prioridade Alta, o responsável (ela mesma), o prazo e, se quiser, o assistido. A reunião de hoje já vem escolhida.
3. Clica em **Registrar demanda**.
4. Vê a confirmação "Demanda registrada" e a página da demanda nova, com o estado Aberta.

**Variação (internet instável, RNF16):** no passo 3 a conexão cai. O sistema avisa "Não foi possível falar com o servidor. Seus dados continuam no formulário. Tente de novo." O que ela escreveu continua lá; ela clica de novo quando a internet volta.

**O que o cenário exige:** um formulário e uma confirmação (RNF12); reunião de origem pré-selecionada; erro junto do campo dizendo como corrigir; nada se perde quando a conexão falha.

## C4 — Bruna atualiza o andamento e encaminha à rede

**Quem:** Bruna Fictícia (P2).
**Contexto:** ligou para o CRAS sobre a atualização do cadastro de uma família. O CRAS pediu um documento e vai responder em uma semana.
**Objetivo:** deixar registrado que a demanda depende do CRAS e o que foi feito.

**Passo a passo:**
1. Abre **Minhas demandas** e escolhe "Solicitar ao CRAS a atualização do cadastro da família".
2. Em **Mudar estado**, só aparecem as mudanças possíveis. Escolhe **Aguardando terceiros** e confirma.
3. Em **Anotar**, escreve "Liguei para o CRAS; pediram comprovante de endereço" e salva.
4. Em **Encaminhamentos**, registra o encaminhamento ao "CRAS Centro" com a data de hoje.

**O que o cenário exige:** só oferecer transições válidas; confirmação antes de mudar o estado; anotação sem mudar o estado; encaminhamento a partir da própria demanda.

## C5 — Carlos entra e vê que tem prazo chegando

**Quem:** Carlos Fictício, equipe pedagógica (P3), com pouca familiaridade com tecnologia.
**Contexto:** começo do turno, computador compartilhado da sala dos professores.
**Objetivo:** saber se tem alguma coisa atrasada e fechar o que já resolveu.

**Passo a passo:**
1. Entra no sistema.
2. Logo no painel, vê o aviso: "Você tem 1 demanda vencida e 1 perto do prazo", com o link de cada uma. O aviso não mostra a descrição (pode citar a saúde do assistido, spec 09).
3. Abre a que está perto do prazo: "Pedir material adaptado para a turma da tarde". O material chegou ontem.
4. Muda o estado para **Concluída** (passando por Em andamento, se ainda estiver Aberta) e confirma.
5. Clica em **Sair** antes de deixar o computador.

**O que o cenário exige:** aviso de prazo no login (RF40) sem dado sensível; caminho curto do aviso até a demanda; botão Sair sempre visível (computador compartilhado, RF02).

## C6 — Carlos lança a evolução depois da oficina

**Quem:** Carlos Fictício (P3).
**Contexto:** terminou a oficina de música; quer registrar como foi a participação do Assistido Fictício A.
**Objetivo:** lançar a evolução e conferir que ela aparece na ficha.

**Passo a passo:**
1. No menu, abre **Assistidos** e busca "Fictício A".
2. Abre a ficha e escolhe **Lançar evolução**.
3. Preenche a data, a área de atuação ("Pedagógica") e a descrição. Salva.
4. A evolução aparece na ficha, em ordem cronológica, com o nome dele e o horário.
5. Percebe um erro de digitação e usa **Retificar**: a versão anterior continua guardada, e a nova passa a valer.

**O que o cenário exige:** ficha do assistido como lugar de evolução; retificar em vez de apagar (RF24, RF26); 403 explicado em português se a regra restritiva for ligada um dia.
