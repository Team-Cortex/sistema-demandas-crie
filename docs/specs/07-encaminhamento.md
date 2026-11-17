# Spec 07 — Encaminhamento à rede

**Status:** fechada para implementação no servidor, com o destino em texto enquanto A1 estiver aberta. O model já existe (card #55).
**Origem:** RF27 a RF29, RNF03, proposta do `contrato-api.md` de 13/10/2026.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido. Encaminhamento ligado a assistido é dado sensível: passa por `pode_ver_evolucao(assistido)`, e quem não pode → 403, `{"erro": "Você não tem acesso aos dados deste assistido."}`. Nas listas, o que a pessoa não pode ver simplesmente não aparece. Cada operação grava auditoria (spec 05).

Cada encaminhamento sai com: `id`, `assistido_id`, `demanda_id`, `destino`, `data`, `responsavel_id`, `responsavel_nome`, `observacao`, `pendente`, `desfecho`, `desfecho_autor_id`, `desfecho_em`, `criado_em`.

### POST `/api/encaminhamentos`

Corpo: `assistido_id` e/ou `demanda_id`, `destino`, `data`, `observacao` (opcional). O responsável sai do token.

1. Nem `assistido_id` nem `demanda_id` → 422, `{"erro": "Informe o assistido ou a demanda do encaminhamento."}`.
2. Assistido ou demanda inexistente → 422, `{"erro": "Assistido inexistente."}` ou `{"erro": "Demanda inexistente."}`.
3. Os dois informados, e a demanda é de outro assistido → 422, `{"erro": "A demanda informada é de outro assistido."}`.
4. Vindo só da demanda, herda o assistido dela (encaminhar a demanda de alguém encaminha a pessoa).
5. Sem permissão sobre o assistido → 403.
6. `destino` vazio ou acima de 200 → 422, `{"erro": "Informe o destino do encaminhamento."}`; `data` ausente → 422, `{"erro": "Informe a data do encaminhamento."}`. Desfecho no corpo → 422 (campo não aceito): o desfecho vem depois.
7. Resposta 201: o encaminhamento, pendente.

### GET `/api/encaminhamentos` e GET `/api/encaminhamentos/pendentes`

Lista do mais antigo para o mais novo, por `data`. Filtros opcionais: `assistido_id`, `demanda_id`, `responsavel_id` e `pendentes=true` (só os sem desfecho, RF29). `/pendentes` é o mesmo que `pendentes=true` (o card pediu a rota; o contrato, o parâmetro).

### GET `/api/encaminhamentos/<id>`

O encaminhamento. Inexistente → 404, `{"erro": "Encaminhamento inexistente."}`.

### PATCH `/api/encaminhamentos/<id>/desfecho` e PATCH `/api/encaminhamentos/<id>`

Corpo: `{"desfecho": "..."}` (RF28). Grava o texto, o autor do token e o momento, uma única vez.

1. Texto vazio → 422, `{"erro": "Escreva o desfecho do encaminhamento."}`.
2. Já tem desfecho → 400, `{"erro": "Este encaminhamento já tem desfecho registrado."}`.
3. Resposta 200: o encaminhamento com o desfecho.

Não existe `DELETE`; a sessão e o trigger do banco também recusam.

## 2. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A1 | Destino: serviço cadastrado, profissional interno ou texto livre | texto livre de até 200 caracteres |

## 3. Testes que provam esta spec

- Encaminhar pela demanda herda o assistido; sem assistido nem demanda dá 422.
- A lista de pendentes deixa de fora o que já tem desfecho.
- O desfecho grava autor e momento e não aceita segundo desfecho.
- `DELETE` dá 405.
- Com a regra restritiva ligada, quem não acompanha o assistido recebe 403 e não vê o encaminhamento na lista.

## 4. O que não entra

Cadastro de serviços da rede, retorno de acompanhamento, notificação ao destino e exclusão.
