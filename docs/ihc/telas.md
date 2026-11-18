# Especificação tela a tela

Frente de IHC, para o protótipo no Figma (decisão D2 em aberto: quem monta) e para o front-end React contarem a mesma história. Rotas da API conforme `docs/contrato-api.md` §2; regras de campo conforme as specs.

Cada tela tem: objetivo, quem vê, conteúdo, componentes, ação principal, estados e textos. Os textos são os que aparecem na tela, já na linguagem do CRIE ([`arquitetura-da-informacao.md`](arquitetura-da-informacao.md) §4.3).

---

## 0. Regras para todas as telas

**Layout base** (todas, menos Entrar):
- Menu lateral à esquerda, com o logo do CRIE no topo, os itens na ordem do sitemap e o item atual marcado (cor + barra + `aria-current="page"`).
- No topo do conteúdo: saudação "Olá, *primeiro nome*", o perfil por extenso e o botão **Sair**.
- No celular (até ~768 px): o menu vira um painel recolhível aberto pelo botão **Menu**; Esc e clique fora fecham.
- Título `h1` da página igual ao rótulo do menu.

**Estados** que toda tela com dados tem:

| Estado | O que aparece |
| --- | --- |
| Carregando | Esqueleto (blocos cinza com o formato do conteúdo) e texto para leitor de tela "Carregando..." |
| Vazio | Frase que explica e diz o que fazer, com a ação principal quando fizer sentido |
| Erro | A mensagem do servidor (já em português) ou a de conexão, e o botão **Tentar de novo** |
| Sucesso (depois de salvar) | Aviso curto no topo, "Demanda registrada.", que some sozinho e é anunciado ao leitor de tela |

**Selo de estado** (texto + cor, nunca só cor):

| Estado | Rótulo | Cor de apoio |
| --- | --- | --- |
| `aberta` | Aberta | azul |
| `em_andamento` | Em andamento | roxo (cor de destaque) |
| `aguardando_terceiros` | Aguardando terceiros | âmbar |
| `concluida` | Concluída | verde |
| `cancelada` | Cancelada | cinza |
| `vencida: true` | **Vencida** (selo extra, ao lado do estado) | vermelho |

**Prioridade:** Baixa, Média, Alta (texto; Alta com marcador visual).
**Datas:** `dd/mm/aaaa`; data e hora no histórico `dd/mm/aaaa às hh:mm`.
**Acessibilidade:** contraste ≥ 4,5:1; foco visível; Tab em ordem lógica; Esc fecha diálogos; todo campo com rótulo; erro ligado ao campo; alvos de clique ≥ 44 px; texto base 16 px.

---

## 1. Entrar — `/entrar`

- **Objetivo:** identificar a pessoa (RF01).
- **Quem vê:** todos, sem sessão.
- **Conteúdo:** logo do CRIE, título "Sistema de Demandas", campos **E-mail** e **Senha**, botão **Entrar**. Linha discreta: "Use o e-mail e a senha que a direção cadastrou."
- **Erros:**
  - Campo vazio: junto do campo, "Informe o e-mail." / "Informe a senha."
  - 401 e 429: "E-mail ou senha inválidos." (o servidor não diz qual).
  - Sem resposta: "Não foi possível falar com o servidor. Confira a internet e tente de novo."
  - Vindo de sessão encerrada: aviso no topo "Sua sessão terminou. Entre de novo."
- **Depois de entrar:** vai para o Painel, ou de volta para a tela em que estava quando a sessão terminou.

## 2. Painel — `/`

- **Objetivo:** ver numa tela só o que está em aberto e o que está vencido (RF30, RF33, RF39; persona P1).
- **Quem vê:** todos.
- **API:** `GET /api/demandas/painel`.
- **Conteúdo, de cima para baixo:**
  1. **Aviso de prazo** (RF40), só se o login trouxe pendências: "Você tem **2 demandas vencidas** e **1 perto do prazo**." e um link por demanda ("Demanda nº 7 — prazo 14/11/2026 — Vencida"). Sem descrição (spec 09). Botão **Fechar aviso**.
  2. **Indicadores**: Em aberto (total), Vencidas, e um por estado (Aberta, Em andamento, Aguardando terceiros). Números grandes com rótulo; o de Vencidas em destaque quando > 0.
  3. **Três colunas** por estado. Cada cartão: descrição (até 2 linhas), responsável, prazo, prioridade, selo Vencida quando for o caso. Vencidas no topo (o servidor já ordena pelo prazo).
- **Ação principal:** **Registrar demanda**.
- **Vazio:** "Nenhuma demanda em aberto. Quando a equipe registrar uma demanda, ela aparece aqui." Por coluna: "Nenhuma demanda neste estado."
- **No celular:** as colunas viram seções empilhadas.

## 3. Minhas demandas — `/minhas`

- **Objetivo:** o que está com a própria pessoa (RF34).
- **API:** `GET /api/demandas/minhas`.
- **Conteúdo:** lista de cartões, do prazo mais antigo; mesmo cartão do painel, com o estado.
- **Vazio:** "Você não tem demandas em aberto."

## 4. Demandas — `/demandas`

- **Objetivo:** achar qualquer demanda, inclusive antiga (RF31, RF32; cenário C2).
- **API:** `GET /api/demandas` com os filtros; listas auxiliares `GET /api/usuarios?ativo=true` e `GET /api/assistidos`.
- **Conteúdo:**
  - Busca **Procurar na descrição** sempre visível.
  - Filtros: Estado, Responsável, Categoria, Período (de / até), Assistido. No celular, atrás de **Mais filtros**.
  - **Limpar filtros** quando algum estiver ativo.
  - Tabela (`table`) no computador: Descrição, Estado, Responsável, Prazo, Prioridade. Cada linha leva ao detalhe.
  - No celular, a tabela vira lista de cartões.
- **Ação principal:** **Registrar demanda**.
- **Vazio com filtro:** "Nenhuma demanda encontrada com esses filtros. Tente tirar um filtro ou procurar outra palavra."

## 5. Registrar demanda — `/demandas/nova`

- **Objetivo:** registrar em **um formulário e uma confirmação** (RF10, RF11, RNF12; cenário C3).
- **API:** `POST /api/demandas`; listas `GET /api/usuarios?ativo=true`, `GET /api/reunioes`, `GET /api/assistidos`.
- **Campos, na ordem:**

| Rótulo | Tipo | Obrigatório | Regra e mensagem |
| --- | --- | --- | --- |
| Descrição | texto longo | sim | "Informe a descrição da demanda." |
| Prioridade | 3 opções lado a lado (Baixa, Média, Alta) | sim | "Escolha a prioridade." |
| Responsável | lista | sim | "Escolha o responsável." |
| Prazo | data | sim | "Informe o prazo." |
| Reunião de origem | lista "Reunião de dd/mm/aaaa — Setor", **já com a mais recente** | sim | "Escolha a reunião em que a demanda surgiu." |
| Assistido | lista por nome de tratamento | não | — |
| Categoria | texto curto, até 80 | não | "A categoria aceita até 80 caracteres." |

- **Ação principal:** **Registrar demanda**. Secundária: **Voltar** (sem salvar).
- **Confirmação:** vai para o detalhe da demanda nova com "Demanda registrada."
- **Falha de conexão:** aviso no topo do formulário; nada é apagado (RNF16).
- **Sem reunião cadastrada:** "Antes, registre a reunião em que a demanda surgiu." com link **Registrar reunião**.

## 6. Demanda (detalhe) — `/demandas/:id`

- **Objetivo:** ver tudo de uma demanda e atualizar (RF12 a RF17).
- **API:** `GET /api/demandas/<id>`; `PATCH .../estado`; `POST .../anotacoes`; `PATCH .../responsavel`.
- **Conteúdo:**
  - Cabeçalho: descrição (título), selo de estado, selo Vencida, prioridade.
  - Dados: responsável, prazo, reunião de origem (link), assistido (link, se houver), categoria, registrada em.
  - **Histórico** em linha do tempo, do mais antigo para o mais novo: "Bruna Fictícia mudou de Aberta para Em andamento — 18/11/2026 às 14:30"; anotações com o texto.
  - Campo **Anotar** com botão **Salvar anotação**.
- **Ações:** **Mudar estado** (principal; some quando concluída ou cancelada), **Trocar responsável**, **Encaminhar**.
- **Diálogo Mudar estado:** título "Mudar o estado da demanda"; só as opções válidas (spec 02); texto de apoio quando a opção é Cancelada: "A demanda continua no histórico e pode ser encontrada pela busca."; botões **Confirmar** e **Voltar**. Esc fecha. Foco vai para o diálogo ao abrir e volta ao botão ao fechar.
- **Diálogo Trocar responsável:** lista de profissionais ativos; **Confirmar** e **Voltar**.
- **404:** "Esta demanda não existe ou o endereço está errado." e link para Demandas.

## 7. Reuniões — `/reunioes` (prioridade 2)

- **Lista** por data decrescente: data, setor, participantes. Filtro por setor. Ação principal **Registrar reunião**.
- **Registrar / editar:** Data (hoje por padrão), Setor (Pedagógico, Saúde, Serviço de convivência), Participantes (caixas de seleção dos profissionais ativos).
- **Ficha** `/reunioes/:id`: dados da reunião e as demandas que surgiram nela, cada uma com o estado (RF08), e o botão **Registrar demanda desta reunião** (abre o formulário com a reunião já escolhida).

## 8. Assistidos — `/assistidos` (prioridade 2)

- **Lista** alfabética com busca pelo nome de tratamento. Ação principal **Cadastrar assistido**.
- **Cadastrar / editar:** só **Nome de tratamento** (decisão A3, minimização da LGPD). Texto de apoio: "Use o nome pelo qual a pessoa é chamada no CRIE. Não registre documentos nem dados de saúde aqui."
- **Ficha** `/assistidos/:id` (RF20): abas ou seções Demandas, Evoluções, Encaminhamentos, em ordem cronológica. Ações **Lançar evolução** e **Encaminhar**. 403: "Você não tem acesso às evoluções deste assistido."

## 9. Evoluções (dentro da ficha, prioridade 2)

- **Lançar:** Data (hoje), Área de atuação (texto até 80, QA06 em aberto), Descrição. Autor e horário saem do servidor e aparecem depois de salvar.
- **Lista:** filtros por período e área (RF25).
- **Versões** `/evolucoes/:id`: versão vigente e as anteriores, com autor e horário de cada uma. Ação **Retificar** só na vigente: "A versão atual fica guardada no histórico." Nunca "Excluir" (RF26).

## 10. Encaminhamentos — `/encaminhamentos` (prioridade 2)

- Abre em **Pendentes** (RF29), do mais antigo. Alternância Pendentes / Todos.
- **Registrar** (vindo da demanda ou da ficha): Destino (texto até 200, A1 em aberto), Data, Observação.
- **Registrar desfecho:** texto; aviso "O desfecho só pode ser registrado uma vez." antes de confirmar.

## 11. Usuários — `/usuarios` (só direção, prioridade 3)

- Lista por nome: nome, e-mail, perfil, situação (Ativo / Desativado).
- Cadastrar: nome, e-mail, perfil, senha inicial (mínimo 8). Editar: nome e perfil.
- **Desativar** (nunca excluir), com confirmação: "A pessoa não consegue mais entrar. O histórico dela continua no sistema." A direção não vê o botão na própria linha.

## 12. Relatórios — `/relatorios` (só direção, prioridade 3)

- **Demandas do período:** De, Até (obrigatórios), filtros Estado, Categoria, Responsável; totais por estado e vencidas; lista. Rodapé com "Emitido por *nome* em dd/mm/aaaa às hh:mm" (RF38).
- **Acompanhamento do assistido:** assistido, De, Até; evoluções e encaminhamentos do período.
- Botão **Imprimir** usa a impressão do navegador (RF37 depende da QA04).

## 13. Auditoria — `/auditoria` (só direção, prioridade 3)

- Tabela paginada: quando, quem, ação, recurso, assistido. Filtros: autor, assistido, recurso, ação, período.
- Só leitura.
