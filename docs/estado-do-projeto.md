# Estado do projeto

Mapa geral do sistema, para quem abre o repositório sem a conversa anterior. Atualizado em 16/11/2026.

Quem mantém este arquivo é a frente de back-end. A atualização acompanha os commits dessa frente quando um fato daqui muda. Não é diário de commits e não é obrigação das outras frentes manterem este texto em tempo real.

---

## 1. O que é

Sistema web para registrar, acompanhar e consultar as **demandas de articulação de rede** do CRIE — Centro de Integração Especial / APAE de Extrema. São situações que a equipe não resolve internamente e que exigem a rede pública (assistência social, saúde, educação).

Há três reuniões semanais, uma por setor: pedagógico, saúde e serviço de convivência. O histórico é consultável e não se apaga. Dados no repositório e na demonstração são fictícios. Parte das pessoas atendidas é menor de idade.

A direção optou por visibilidade aberta a todo profissional cadastrado. A auditoria (autor, data e hora, inclusive na consulta) é o controle. A alternativa restritiva permanece prevista no código, desligada.

Parceiro: CRIE. Curso: ADS, IFSP Câmpus Bragança Paulista, BRAEXT2, orientação do Prof. Luiz Gustavo Diniz de Oliveira Véras. Entrega final: 26/11/2026. A ET3, em que o back-end começa a responder, é 22/10/2026.

O relato acadêmico da versão 2 (02/10/2026) é a referência de escopo quando divergir dos Markdown de agosto.

## 2. Como está desenhado

Cliente-servidor. O navegador não fala com o PostgreSQL.

| Parte | Onde | Quem preenche |
| --- | --- | --- |
| Cliente React | `frontend/` | os arquivos do Gabriel, apenas movidos da raiz para esta pasta |
| Servidor Flask | `backend/` | Miguel Vaz |
| Camadas do servidor | `schemas/`, `routes/`, `services/`, `models/` | back-end; um arquivo por recurso das specs |
| Banco | PostgreSQL via `docker-compose.yml`; scripts em `docs/modelagem/sql/` | Henry Claro |
| Requisitos e plano | `docs/requisitos.md`, `docs/plano-de-projeto.md` | Vinícius Marrocos |
| Interface | Figma, fora deste repositório | Inácio Fontes |

Contrato HTTP: [`contrato-api.md`](contrato-api.md). Comportamento do servidor: [`specs/`](specs/).

## 3. O que responde hoje

A lista rota por rota está no §2 do [`contrato-api.md`](contrato-api.md), atualizada no mesmo commit de cada rota nova. Em resumo, o servidor responde:

| Recurso | Spec | O que faz |
| --- | --- | --- |
| Sessão | 01, 09 | login com JWT de 30 minutos, limite de tentativas (429), logout que revoga o token, aviso de prazo no login sem dado de saúde |
| Usuários | 01 | a direção cadastra, edita e desativa (nunca exclui); todos listam para escolher responsável |
| Reuniões | 04 | registrar, listar por data, ficha com as demandas e o estado, alterar |
| Demandas | 02 | abrir, filtrar e buscar, histórico, mudar estado, anotar, trocar responsável, painel por estado, minhas demandas |
| Assistidos | 03 | cadastro só com nome de tratamento, lista, consulta e ficha completa |
| Evoluções | 06 | lançar, listar com filtros, consultar versões, retificar sem apagar |
| Encaminhamentos | 07 | registrar ligado a assistido ou demanda, pendentes, desfecho uma vez |
| Relatórios | 08 | demandas do período e acompanhamento do assistido, só a direção |
| Auditoria | 05 | toda operação com dado de assistido grava autor, ação e momento, inclusive leitura; a direção consulta |

Toda rota de dado exige token de conta ativa. Permissão só da direção sai de métodos polimórficos (`pode_gerir_usuarios`, `pode_emitir_relatorio`, `pode_consultar_auditoria`), como `pode_ver_evolucao`. Nenhum recurso tem `DELETE`.

## 3.1 Models no servidor

Entidades SQLAlchemy em `backend/app/models/`, testadas contra SQLite em memória. O schema sai de `backend/migrations/` (`flask db upgrade`); a migração inicial `b0f13416410c` cria as tabelas do domínio e, no banco, recusa UPDATE/DELETE em `historico_demanda` e `evolucao` e DELETE em `demanda` e `encaminhamento` (trigger); `3df29fd96f0b` cria `token_revogado` e `3f00c11df825` cria `auditoria`, que recusa UPDATE e DELETE. O script relacional do Henry continua sendo a referência do banco; se divergir, o model e a migração se ajustam.

| Model | Tabela | Situação |
| --- | --- | --- |
| `Usuario` → `Direcao`, `Profissional` → `AssistenteSocial`, `EquipePedagogica` (abstratas: `Usuario`, `Profissional`) | `usuario`, herança de tabela única por `perfil` | nome, e-mail único, ativo, perfil, criado_em; senha só como hash, via `definir_senha` e `senha_confere`; `pode_ver_evolucao` por perfil, acesso aberto com a regra restritiva desligada (`Profissional.acesso_restrito`) |
| `Assistido` | `assistido` | só `nome_tratamento` enquanto A3 estiver aberta; ativo, criado_em; ficha com `demandas`, `evolucoes` e `encaminhamentos` em ordem cronológica, sem cascade de exclusão |
| `AssistidoProfissional` | `assistido_profissional` | quem acompanha quem, com `data_inicio`; alimenta a regra restritiva desligada |
| `Reuniao` | `reuniao`, `reuniao_participante` | data, setor fechado em `pedagogico`, `saude`, `convivencia` e participantes; `demandas` originadas nela, com o estado atual |
| `Demanda` | `demanda` | descrição, categoria opcional até 80 (A2), prioridade `baixa`/`media`/`alta`, responsável, prazo, reunião de origem, assistido opcional; estado fechado em `EstadoDemanda`, nasce `aberta`; transições da spec 02 validadas no próprio atributo; `Demanda.abrir(autor, ...)` e `mudar_estado(novo, autor)` gravam o histórico sozinhos, recusa vira 400 e não grava nada; `anotar(texto, autor)` grava anotação sem mudar o estado; `reatribuir(novo, autor)` recusa responsável inexistente ou inativo com 404 e anota a troca no histórico |
| `HistoricoDemanda` | `historico_demanda` | ligado à demanda; autor, tipo `estado`/`anotacao`, estado anterior e novo, texto, `ocorrido_em`; lido em ordem cronológica; somente inserção: a sessão recusa alterar e excluir (`app/models/imutavel.py`), e a demanda também não admite exclusão |
| `Evolucao` | `evolucao` | assistido, profissional, data, área de atuação (texto até 80 enquanto QA06 não fecha) e descrição; `Evolucao.lancar(autor, ...)` grava autor e `ocorrido_em` pelo servidor; `retificar(autor, ...)` cria versão nova apontando a anterior (`retifica_id`), que fica intacta; somente inserção, sem exclusão; `Evolucao.do_assistido(id, de, ate, area_atuacao)` lista as vigentes em ordem cronológica (no SQLite de teste, maiúscula acentuada na área não casa; no PostgreSQL casa) |
| `RegistroAuditoria` | `auditoria` | autor, ação, recurso, `recurso_id`, assistido, detalhe curto e `ocorrido_em` do servidor (spec 05, migração `3f00c11df825`); somente inserção pela sessão e por trigger que recusa UPDATE e DELETE |
| `TokenRevogado` | `token_revogado` | `jti` do token encerrado por logout, até a expiração original (migração `3df29fd96f0b`); linha vencida sai no logout seguinte |
| `Encaminhamento` | `encaminhamento` | destino em texto (A1 aberta), data, responsável, observação opcional; ligado a assistido, a demanda ou aos dois, nunca a nenhum (CHECK); vindo da demanda, herda o assistido dela; `registrar_desfecho(texto, autor)` grava desfecho, autor e momento uma única vez; `Encaminhamento.pendentes(responsavel_id, assistido_id)` lista os sem desfecho, do mais antigo; sem exclusão |

## 4. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A1 | Destino do encaminhamento | destino em texto livre de até 200 caracteres |
| A2 | Categorias de demanda | campo opcional, texto de até 80 caracteres, sem catálogo |
| A3 | Campos do assistido | o servidor só aceita `nome_tratamento` |
| A4 | Perfil coordenação de setor | não há classe própria |
| A5 | Trocar JWT em `sessionStorage` por cookie | permanece o JWT de 30 minutos |
| A6 | Data do "período" no filtro e no relatório de demandas | data de registro da demanda |
| A7 | Retenção da auditoria | nada sai da tabela |
| A8 | Onde fica a auditoria | tabela `auditoria` no mesmo banco (spec 05); a equipe confirma |
| A9 | Quem retifica evolução | quem pode ver a evolução |
| A10 | Antecedência do aviso de prazo | 3 dias, configurável |

Fora das specs atuais: serviço da rede, retorno de acompanhamento, notificação por e-mail (RF41) e exportação de relatório para impressão (RF37, espera a QA04).

## 5. Como rodar

Está no [`README.md`](../README.md); a instalação do servidor do zero está em [`backend/README.md`](../backend/README.md). Servidor em `backend/` (`flask run`, porta 5000). Cliente em `frontend/` (`npm run dev`, porta 5173). Banco local com `docker compose up -d`.
