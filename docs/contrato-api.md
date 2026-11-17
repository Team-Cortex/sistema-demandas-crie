# Contrato da API

**Status:** proposta — frente de back-end, 13/10/2026.  
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
| 422 | Corpo ausente ou campo inválido |
| 429 | Muitas tentativas de login |

A mensagem de login é sempre **E-mail ou senha inválidos.** O servidor não revela se o e-mail existe.

---

## 2. O que já responde

| Método | Caminho | Auth | Resposta |
| --- | --- | --- | --- |
| GET | `/api/saude` | não | `{"ok": true, "status": "ok"}` ou `"degradado"` |
| GET | `/api/teste` | não | `Hello World` |
| POST | `/api/auth/login` | não | 200 `token`, `perfil`, `usuario` (`id`, `nome`, `perfil`); 401 credencial recusada; 422 corpo incompleto; 429 na sexta falha em 60 s do mesmo IP e e-mail |
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
| GET | `/api/demandas/<id>` | sim | a demanda com `vencida`, `ultimo_movimento` e `historico`; 404 inexistente |
| PATCH | `/api/demandas/<id>/estado` | sim | corpo `estado`; 200 a demanda com o histórico novo; 400 transição recusada, sem gravar; 422 sem `estado`. Sem `DELETE` |
| POST | `/api/demandas/<id>/anotacoes` | sim | corpo `texto`; 201 o item de histórico `anotacao`; o estado não muda; 422 texto vazio |
| PATCH | `/api/demandas/<id>/responsavel` | sim | corpo `responsavel_id`; 200 a demanda, com a troca anotada no histórico; 404 responsável inexistente ou inativo |
| GET | `/api/demandas/<id>/historico` | sim | itens `tipo`, `texto`, `estado_anterior`, `estado_novo`, `autor_id`, `autor_nome`, `ocorrido_em`, em ordem cronológica |
| GET | `/api/auditoria` | direção | `itens`, `total`, `pagina`, `por_pagina`; filtros `autor_id`, `assistido_id`, `recurso`, `acao`, `de`, `ate` (spec 05) |

`/api/saude` não inclui host do banco, versão de schema, stack nem mensagem interna. Detalhe de falha fica no log do servidor, com id de correlação, status e duração. O log não leva senha, token, e-mail nem corpo da requisição.

---

## 3. Recursos das primeiras specs

O comportamento está nas specs. Este quadro é o índice.

| Spec | Recurso | Situação |
| --- | --- | --- |
| [`01-acesso-e-papeis.md`](specs/01-acesso-e-papeis.md) | `/api/auth`, `/api/usuarios` | em implementação; o que já responde está no §2 |
| [`02-demanda-e-estados.md`](specs/02-demanda-e-estados.md) | `/api/demandas` | especificado; espera o modelo relacional para persistir |
| [`03-assistido.md`](specs/03-assistido.md) | `/api/assistidos` | especificado; campos de identificação em aberto |
| [`04-reuniao.md`](specs/04-reuniao.md) | `/api/reunioes` | especificado |
| abaixo | `/api/assistidos/<id>/evolucoes`, `/api/evolucoes/<id>` | proposta; sem rota |
| abaixo | `/api/encaminhamentos` | proposta; sem rota. Destino do encaminhamento continua A1 |
| abaixo | `/api/relatorios/demandas`, `/api/relatorios/assistidos/<id>` | proposta; sem rota |

Serviço da rede, retorno de acompanhamento e notificação continuam fora.

### Evoluções

Token obrigatório. Profissional ativo ou direção. Sem `DELETE`.

| Método | Caminho | Parâmetros | Resposta |
| --- | --- | --- | --- |
| POST | `/api/assistidos/<assistido_id>/evolucoes` | corpo: `data`, `area_atuacao`, `descricao`. Autor sai do token | 201 `id`, `assistido_id`, `data`, `autor_id`, `area_atuacao`, `descricao`, `ocorrido_em` |
| GET | `/api/assistidos/<assistido_id>/evolucoes` | query opcional: `de`, `ate`, `area_atuacao` | lista em ordem cronológica |
| PATCH | `/api/evolucoes/<id>` | corpo: `data`, `area_atuacao`, `descricao` | retifica e preserva a versão anterior, com autor e momento da alteração |

### Encaminhamentos

Token obrigatório. Sem `DELETE`. Enquanto A1 estiver aberta, `destino` é texto.

| Método | Caminho | Parâmetros | Resposta |
| --- | --- | --- | --- |
| POST | `/api/encaminhamentos` | corpo: `assistido_id` ou `demanda_id`, `destino`, `data`, `observacao`. Responsável sai do token | 201 `id`, `assistido_id`, `demanda_id`, `destino`, `data`, `responsavel_id`, `observacao`, `desfecho` |
| GET | `/api/encaminhamentos` | query opcional: `pendentes=true` | lista. Com `pendentes=true`, só os sem desfecho |
| PATCH | `/api/encaminhamentos/<id>` | corpo: `desfecho` | o registro com o desfecho |

### Relatórios

Só a direção. A resposta inclui `emissao` com `autor_id` e `ocorrido_em`.

| Método | Caminho | Parâmetros | Resposta |
| --- | --- | --- | --- |
| GET | `/api/relatorios/demandas` | query: `de`, `ate`; opcionais `estado`, `categoria`, `responsavel_id` | `emissao` e `itens` do período |
| GET | `/api/relatorios/assistidos/<assistido_id>` | query: `de`, `ate` | `emissao`, `evolucoes` e `encaminhamentos` do período |

---

## 4. O que o cliente faz

Quando o React passar a chamar a API, um único módulo concentra a URL base, o header `Authorization`, o tratamento de `{"erro": "..."}` e o descarte do token quando a resposta for 401. Nenhuma tela chama a API por fora desse módulo. O endereço base vem de variável de ambiente pública só com a origem (`http://localhost:5000` em desenvolvimento). Segredo nenhum usa prefixo `VITE_`. Esse módulo é da frente de front-end e ainda não está neste repositório.

---

## 5. Decisões abertas

| # | Decisão | Hoje, enquanto não fecha | Quem decide | O que espera |
| --- | --- | --- | --- | --- |
| A1 | Destino de um encaminhamento: serviço cadastrado, profissional interno ou texto livre | não há rota de encaminhamento | Henry, com o back-end | spec e model de encaminhamento |
| A2 | Lista de categorias de demanda | o campo é opcional e, se vier, é texto de até 80 caracteres, sem catálogo | direção do CRIE | validação por lista fechada |
| A3 | Campos de identificação do assistido | o servidor não grava atributo além de nome de tratamento fictício | direção do CRIE | model `Assistido` |
| A4 | Perfil "coordenação de setor" como classe própria | não existe classe; o acesso aberto cobre o uso descrito no relatório v2 | equipe, se a instituição distinguir o perfil | subclasse e papel novo |
| A5 | Trocar JWT em `sessionStorage` por cookie `HttpOnly` | permanece o JWT de 30 minutos já publicado na arquitetura | back-end e front-end, juntos | o cliente HTTP |
