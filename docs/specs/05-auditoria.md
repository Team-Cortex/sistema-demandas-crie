# Spec 05 — Auditoria

**Status:** fechada para implementação no servidor. Armazenamento decidido pela frente de back-end em 16/11/2026, a confirmar pela equipe. Retenção em aberto (A7).
**Origem:** RNF03, RF38, regra RN13 do minimundo (autor, data e hora, inclusive na consulta) e a escolha da direção do CRIE por acesso aberto com auditoria como controle (relatório v2).

Se esta spec divergir do código, a spec vence.

---

## 1. Onde fica

Tabela `auditoria`, no mesmo PostgreSQL do sistema.

| Coluna | Conteúdo |
| --- | --- |
| `id` | sequencial |
| `autor_id` | usuário do token; obrigatório |
| `acao` | `criar`, `alterar`, `consultar`, `listar`, `retificar`, `registrar_desfecho`, `emitir` |
| `recurso` | `assistido`, `evolucao`, `encaminhamento`, `relatorio_demandas`, `relatorio_assistido` |
| `recurso_id` | id do registro tocado; vazio em lista e relatório de demandas |
| `assistido_id` | assistido envolvido, quando há um |
| `detalhe` | até 200 caracteres: filtros e período usados. Nunca texto de evolução, de encaminhamento ou nome de assistido |
| `ocorrido_em` | momento do servidor, em UTC no banco e com -03:00 na API |

Somente inserção, em duas camadas: a sessão do ORM recusa alterar e excluir (`SomenteInsercao`, a mesma guarda do histórico da demanda), e a migração cria trigger que recusa `UPDATE` e `DELETE` para quem escrever SQL direto. Não existe rota de alterar nem de apagar.

Alternativa descartada: arquivo de log. Arquivo de log gira, é apagado pelo sistema operacional e não se consulta por assistido ou por autor sem ferramenta extra. A tabela fica na mesma cópia de segurança do resto (RNF10).

## 2. O que gera registro

Toda operação que envolve dado de assistido, inclusive leitura.

| Operação | `acao` | `recurso` | `recurso_id` | `assistido_id` |
| --- | --- | --- | --- | --- |
| POST `/api/assistidos` | `criar` | `assistido` | o novo | o novo |
| PATCH/PUT `/api/assistidos/<id>` | `alterar` | `assistido` | id | id |
| GET `/api/assistidos` | `listar` | `assistido` | — | — |
| GET `/api/assistidos/<id>` | `consultar` | `assistido` | id | id |
| GET `/api/assistidos/<id>/ficha` | `consultar` | `assistido` | id | id (`detalhe`: `ficha`) |
| POST `/api/assistidos/<id>/evolucoes` | `criar` | `evolucao` | a nova | assistido |
| GET `/api/assistidos/<id>/evolucoes` | `listar` | `evolucao` | — | assistido (`detalhe`: filtros) |
| GET `/api/evolucoes/<id>` | `consultar` | `evolucao` | id | assistido |
| PATCH `/api/evolucoes/<id>` | `retificar` | `evolucao` | a versão nova | assistido (`detalhe`: `retifica <id anterior>`) |
| POST `/api/encaminhamentos` | `criar` | `encaminhamento` | o novo | assistido, se houver |
| PATCH `/api/encaminhamentos/<id>/desfecho` | `registrar_desfecho` | `encaminhamento` | id | assistido, se houver |
| GET `/api/encaminhamentos` e `/pendentes` | `listar` | `encaminhamento` | — | o do filtro, se houver |
| GET `/api/encaminhamentos/<id>` | `consultar` | `encaminhamento` | id | assistido, se houver |
| GET `/api/relatorios/demandas` | `emitir` | `relatorio_demandas` | — | — (`detalhe`: período e filtros) |
| GET `/api/relatorios/assistidos/<id>` | `emitir` | `relatorio_assistido` | — | id (`detalhe`: período) |

Regras:

1. Escrita: o registro entra na mesma transação da operação. Se a operação falha, não fica registro; se o registro falha, a operação não grava.
2. Leitura: o registro é gravado antes de a resposta sair. Se não gravar, a resposta é 500 e o dado não sai. Sem registro, sem leitura.
3. Pedido recusado (401, 403, 404, 422) não gera registro: nada foi lido nem gravado.
4. Demanda não gera registro: a resposta da demanda só traz o `assistido_id`, nunca dado do assistido (spec 02). Se a equipe quiser auditar demanda ligada a assistido, entra como linha nova da tabela acima.

## 3. Consulta

### GET `/api/auditoria`

Só a direção (`pode_consultar_auditoria`); outro perfil → 403, `{"erro": "Só a direção consulta a auditoria."}`.

Filtros opcionais: `autor_id`, `assistido_id`, `recurso`, `acao`, `de` e `ate` (datas `AAAA-MM-DD`, inclusivas, no fuso do CRIE), `pagina` (desde 1) e `por_pagina` (padrão 50, máximo 200). Data inválida → 422, `{"erro": "Use datas no formato AAAA-MM-DD."}`; `de` depois de `ate` → 422, `{"erro": "A data inicial não pode ser depois da final."}`.

Resposta 200: `{"itens": [...], "total": 123, "pagina": 1, "por_pagina": 50}`, do mais recente para o mais antigo. Cada item: `id`, `autor_id`, `autor_nome`, `acao`, `recurso`, `recurso_id`, `assistido_id`, `detalhe`, `ocorrido_em`.

A consulta à auditoria não gera registro: ela não mostra dado de assistido, só ids e nomes de profissionais.

## 4. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A7 | Por quanto tempo a auditoria é guardada (LGPD; RNF09 fala em política de retenção da instituição) | nada sai da tabela |
| A8 | Armazenamento em tabela do próprio banco (§1) | vale o §1; a equipe confirma na revisão |

## 5. Testes que provam esta spec

- O registro recusa alteração e exclusão pela sessão e por SQL (trigger).
- Criar assistido grava `criar` com autor e momento; consultar a ficha grava `consultar`.
- Pedido sem token não grava registro de leitura.
- Retificar evolução grava `retificar` apontando a versão nova.
- Emitir relatório grava `emitir`.
- Profissional em GET `/api/auditoria` recebe 403; a direção filtra por assistido e por período.

## 6. O que não entra

Auditoria de login e logout, de consulta à própria auditoria, de demanda e de reunião; exportação da auditoria; alerta automático de acesso suspeito.
