# Contrato da API

**Status:** em vigor no servidor — frente de back-end, proposta em 13/10/2026, atualizada com o estado real das rotas em 16/11/2026.  
**Quem confirma do outro lado:** Gabriel Borba, no cliente React.  
Se este arquivo divergir do código do servidor, o arquivo vence e o código muda.

O estilo é **cliente-servidor**. O cliente é a aplicação React em `frontend/`. O servidor é o processo Flask em `backend/`. Os dois só se falam por HTTP com JSON, no prefixo `/api`. O navegador não abre conexão com o PostgreSQL.

---

## 1. Combinações fixas

| Item | Valor |
| --- | --- |
| Prefixo | `/api` |
| Corpo | JSON, campos em snake_case |
| Datas | ISO 8601, com fuso (`2026-10-13T14:30:00-03:00`) |
| Autenticação | `Authorization: Bearer <token>` |
| Token | JWT, validade de 30 minutos |
| Onde o cliente guarda o token | `sessionStorage` (decisão já publicada em `docs/arquitetura.md`) |
| Erro | `{"erro": "mensagem em português"}` |
| CORS | lista explícita em `CORS_ORIGINS`. `*` não abre origem nenhuma |

Códigos:

| HTTP | Quando |
| --- | --- |
| 400 | Regra de negócio violada |
| 401 | Token ausente, inválido ou expirado; credencial recusada |
| 403 | Perfil sem acesso à operação |
| 404 | Recurso inexistente |
| 405 | Método que a rota não tem, inclusive `DELETE`: nenhum recurso é excluído |
| 422 | Corpo ausente, campo inválido ou campo não aceito; a mensagem é a do primeiro campo recusado |
| 429 | Muitas tentativas de login |

A mensagem de login é sempre **E-mail ou senha inválidos.** O servidor não revela se o e-mail existe.

---

## 2. O que já responde

| Método | Caminho | Auth | Resposta |
| --- | --- | --- | --- |
| GET | `/api/saude` | não | `{"ok": true, "status": "ok"}` ou `"degradado"` |
| POST | `/api/auth/login` | não | 200 `token`, `perfil`, `usuario` (`id`, `nome`, `perfil`), `avisos` (demandas vencidas ou perto do prazo, só `id`, `prazo`, `estado`, `vencida`; spec 09); 401 credencial recusada; 422 corpo incompleto; 429 na sexta falha em 60 s do mesmo IP e e-mail |
| POST | `/api/auth/logout` | sim | 200 `{"ok": true}`; o token deixa de valer (401 no uso seguinte) |
| POST | `/api/usuarios` | direção | 201 `id`, `nome`, `email`, `perfil`, `ativo`, `criado_em`; 400 e-mail repetido; 403 outro perfil; 422 campo inválido |
| GET | `/api/usuarios` | sim | lista por nome; filtros `ativo`, `perfil`; `email` só para a direção |
| GET | `/api/usuarios/<id>` | sim | o usuário; 404 inexistente |
| PATCH ou PUT | `/api/usuarios/<id>` | direção | corpo com `nome`, `perfil` e/ou `ativo`; 200 o usuário; 400 se a direção mexe no próprio perfil ou se desativa |
| PATCH | `/api/usuarios/<id>/desativar` | direção | 200 o usuário com `ativo: false`; a sessão aberta dele cai; 400 na própria conta. Sem `DELETE` |
| POST | `/api/reunioes` | sim | corpo `data`, `setor`, `participante_ids`; 201 a reunião com `participantes` e `demandas: []`; 422 setor, data ou participante inválido |
| GET | `/api/reunioes` | sim | lista por data decrescente; filtro `setor`; cada item `id`, `data`, `setor`, `participantes`, `criado_em` |
| GET | `/api/reunioes/<id>` | sim | a reunião mais `demandas` (`id`, `descricao`, `estado`); 404 inexistente |
| PATCH ou PUT | `/api/reunioes/<id>` | sim | `data`, `setor` e/ou `participante_ids`, mesmas regras do POST; demandas ligadas ficam. Sem `DELETE` |
| POST | `/api/demandas` | sim | 201 a demanda nascida `aberta`, com `historico`; 422 com a mensagem do campo (spec 02) |
| GET | `/api/demandas` | sim | lista por último movimento; filtros `estado` (vírgula para vários), `responsavel_id`, `categoria`, `periodo_inicio`, `periodo_fim`, `assistido_id`, `reuniao_id`, `q` ou `busca`; sem filtro, sem as canceladas |
| GET | `/api/demandas/painel` | sim | `por_estado` (`aberta`, `em_andamento`, `aguardando_terceiros`, cada uma do prazo mais antigo), `totais`, `total`, `vencidas` |
| GET | `/api/demandas/minhas` | sim | as do usuário do token, não encerradas, do prazo mais antigo, com `vencida`; filtro `estado` |
| GET | `/api/demandas/<id>` | sim | a demanda com `vencida`, `ultimo_movimento` e `historico`; 404 inexistente |
| PATCH | `/api/demandas/<id>/estado` | sim | corpo `estado`; 200 a demanda com o histórico novo; 400 transição recusada, sem gravar; 422 sem `estado`. Sem `DELETE` |
| POST | `/api/demandas/<id>/anotacoes` | sim | corpo `texto`; 201 o item de histórico `anotacao`; o estado não muda; 422 texto vazio |
| PATCH | `/api/demandas/<id>/responsavel` | sim | corpo `responsavel_id`; 200 a demanda, com a troca anotada no histórico; 404 responsável inexistente ou inativo |
| GET | `/api/demandas/<id>/historico` | sim | itens `tipo`, `texto`, `estado_anterior`, `estado_novo`, `autor_id`, `autor_nome`, `ocorrido_em`, em ordem cronológica |
| POST | `/api/assistidos` | sim | corpo só `nome_tratamento` (A3); 201 o assistido com `demandas`, `evolucoes`, `encaminhamentos` (ids); 422 dado não autorizado; audita `criar` |
| GET | `/api/assistidos` | sim | `id`, `nome_tratamento` em ordem alfabética; filtro `busca`; audita `listar` sem guardar o texto buscado |
| GET | `/api/assistidos/<id>` | sim | o assistido com os ids de `demandas`, `evolucoes` (vigentes) e `encaminhamentos`; 404 inexistente; audita `consultar` |
| GET | `/api/assistidos/<id>/ficha` | `pode_ver_evolucao` | `assistido`, `profissionais`, `demandas`, `evolucoes` vigentes e `encaminhamentos`, em ordem cronológica; 403 sem acesso; audita `consultar` (`ficha`) |
| PATCH ou PUT | `/api/assistidos/<id>` | sim | só `nome_tratamento`; 200; audita `alterar`. Sem `DELETE` |
| POST | `/api/assistidos/<id>/evolucoes` | `pode_ver_evolucao` | corpo `data`, `area_atuacao`, `descricao`; autor, profissional e momento saem do token e do servidor; 201; audita `criar` (spec 06) |
| GET | `/api/assistidos/<id>/evolucoes` | `pode_ver_evolucao` | vigentes em ordem cronológica; filtros `de`, `ate`, `area_atuacao`; audita `listar` |
| GET | `/api/evolucoes/<id>` | `pode_ver_evolucao` | a evolução com `versoes_anteriores` e `retificada_por_id`; audita `consultar` |
| PATCH | `/api/evolucoes/<id>` | `pode_ver_evolucao` | retifica: 201 a versão nova, a anterior fica intacta; 400 se não for a vigente; audita `retificar`. Sem `DELETE` |
| POST | `/api/encaminhamentos` | sim; `pode_ver_evolucao` se tiver assistido | corpo `assistido_id` e/ou `demanda_id`, `destino`, `data`, `observacao`; responsável do token; 201; audita `criar` (spec 07) |
| GET | `/api/encaminhamentos` | sim | por data, do mais antigo; filtros `pendentes=true`, `assistido_id`, `demanda_id`, `responsavel_id`; só o que a pessoa pode ver; audita `listar` |
| GET | `/api/encaminhamentos/pendentes` | sim | o mesmo que `pendentes=true` |
| GET | `/api/encaminhamentos/<id>` | sim; `pode_ver_evolucao` se tiver assistido | o encaminhamento; 404 inexistente; audita `consultar`. Sem `DELETE` |
| PATCH | `/api/encaminhamentos/<id>/desfecho` ou `/api/encaminhamentos/<id>` | sim; `pode_ver_evolucao` se tiver assistido | corpo só `desfecho`; 200 com autor e momento do desfecho; 400 se já tinha; audita `registrar_desfecho` |
| GET | `/api/relatorios/demandas` | direção | `de` e `ate` obrigatórios; filtros `estado`, `categoria`, `responsavel_id`; `emissao`, `periodo`, `filtros`, `totais`, `itens`; audita `emitir` (spec 08) |
| GET | `/api/relatorios/assistidos/<id>` | direção | `de` e `ate` obrigatórios; `emissao`, `periodo`, `assistido`, `evolucoes` vigentes e `encaminhamentos` do período; audita `emitir` |
| GET | `/api/auditoria` | direção | `itens`, `total`, `pagina`, `por_pagina`; filtros `autor_id`, `assistido_id`, `recurso`, `acao`, `de`, `ate` (spec 05) |

`/api/saude` não inclui host do banco, versão de schema, stack nem mensagem interna. Detalhe de falha fica no log do servidor, com id de correlação, status e duração. O log não leva senha, token, e-mail nem corpo da requisição.

---

## 3. Índice das specs

O comportamento detalhado (ordem das regras, mensagens, testes que provam) está nas specs. Este quadro é o índice; o §2 lista o que responde hoje.

| Spec | Recurso | Situação |
| --- | --- | --- |
| [`01-acesso-e-papeis.md`](specs/01-acesso-e-papeis.md) | `/api/auth`, `/api/usuarios` | implementado |
| [`02-demanda-e-estados.md`](specs/02-demanda-e-estados.md) | `/api/demandas` | implementado; período do filtro em aberto (A6) |
| [`03-assistido.md`](specs/03-assistido.md) | `/api/assistidos` | implementado; campos de identificação em aberto (A3) |
| [`04-reuniao.md`](specs/04-reuniao.md) | `/api/reunioes` | implementado |
| [`05-auditoria.md`](specs/05-auditoria.md) | `/api/auditoria` e o registro das operações com assistido | implementado; retenção em aberto (A7) |
| [`06-evolucao.md`](specs/06-evolucao.md) | `/api/assistidos/<id>/evolucoes`, `/api/evolucoes/<id>` | implementado; quem retifica em aberto (A9) |
| [`07-encaminhamento.md`](specs/07-encaminhamento.md) | `/api/encaminhamentos` | implementado; destino em texto enquanto A1 estiver aberta |
| [`08-relatorio.md`](specs/08-relatorio.md) | `/api/relatorios` | implementado em JSON; formato de impressão espera a QA04 |
| [`09-aviso-de-prazo.md`](specs/09-aviso-de-prazo.md) | campo `avisos` do login | implementado; antecedência em aberto (A10) |

Onde o card e a spec usaram nomes diferentes, o servidor aceita os dois: `PUT` e `PATCH` em usuários, reuniões e assistidos; `q` e `busca` na lista de demandas; `PATCH /<id>` e `PATCH /<id>/desfecho` no encaminhamento; `pendentes=true` e `/pendentes`.

Serviço da rede, retorno de acompanhamento, e-mail (RF41) e exportação para impressão (RF37) continuam fora.

### Controle de acesso

| Coluna "Auth" do §2 | Significa |
| --- | --- |
| não | rota pública |
| sim | token válido de conta ativa; qualquer perfil |
| direção | token válido e permissão só da direção (`pode_gerir_usuarios`, `pode_emitir_relatorio`, `pode_consultar_auditoria`); outro perfil → 403 |
| `pode_ver_evolucao` | token válido e acesso ao assistido; com o acesso aberto de hoje, todo perfil ativo passa; com a regra restritiva ligada, só quem acompanha e a direção |

---

## 4. O que o cliente faz

Quando o React passar a chamar a API, um único módulo concentra a URL base, o header `Authorization`, o tratamento de `{"erro": "..."}` e o descarte do token quando a resposta for 401. Nenhuma tela chama a API por fora desse módulo. O endereço base vem de variável de ambiente pública só com a origem (`http://localhost:5000` em desenvolvimento). Segredo nenhum usa prefixo `VITE_`. Esse módulo é da frente de front-end e ainda não está neste repositório.

---

## 5. Decisões abertas

| # | Decisão | Hoje, enquanto não fecha | Quem decide | O que espera |
| --- | --- | --- | --- | --- |
| A1 | Destino de um encaminhamento: serviço cadastrado, profissional interno ou texto livre | `destino` é texto livre de até 200 caracteres | Henry, com o back-end | model e spec 07 |
| A2 | Lista de categorias de demanda | o campo é opcional e, se vier, é texto de até 80 caracteres, sem catálogo | direção do CRIE | validação por lista fechada |
| A3 | Campos de identificação do assistido | o servidor não grava atributo além de nome de tratamento fictício | direção do CRIE | model `Assistido` |
| A4 | Perfil "coordenação de setor" como classe própria | não existe classe; o acesso aberto cobre o uso descrito no relatório v2 | equipe, se a instituição distinguir o perfil | subclasse e papel novo |
| A5 | Trocar JWT em `sessionStorage` por cookie `HttpOnly` | permanece o JWT de 30 minutos já publicado na arquitetura | back-end e front-end, juntos | o cliente HTTP |
| A6 | A que data o "período" do filtro e do relatório de demandas se refere | data de registro da demanda, no fuso do CRIE | direção do CRIE, com o back-end | spec 02 e spec 08 |
| A7 | Por quanto tempo a auditoria é guardada | nada sai da tabela `auditoria` | direção do CRIE (controladora dos dados, RNF09) | spec 05 |
| A8 | Onde fica a auditoria | tabela `auditoria` no mesmo PostgreSQL, somente inserção por ORM e trigger | equipe, na revisão do card #17 | spec 05 §1 |
| A9 | Quem pode retificar evolução | quem pode ver a evolução; autor e momento ficam gravados | direção do CRIE | spec 06 |
| A10 | Quantos dias antes do prazo a demanda conta como "perto" no aviso do login | 3, em `AVISO_DIAS_ANTES_DO_PRAZO` | direção do CRIE | spec 09 |
