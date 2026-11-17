# Spec 09 — Aviso de prazo no login

**Status:** fechada para a notificação interna. O número de dias que conta como "perto do prazo" é decisão aberta (A10).
**Origem:** RF40 e a observação sobre notificações em `requisitos.md` §3.9: nenhuma notificação leva dado de saúde nem conteúdo de evolução; só indica que há pendência.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

O login certo (spec 01) devolve, além de `token`, `perfil` e `usuario`, o campo `avisos` com as demandas sob a responsabilidade de quem entrou que estão vencidas ou perto do prazo:

```json
"avisos": {
  "vencidas": 1,
  "perto_do_prazo": 1,
  "dias_de_antecedencia": 3,
  "demandas": [
    {"id": 7, "prazo": "2026-11-14", "estado": "em_andamento", "vencida": true},
    {"id": 9, "prazo": "2026-11-18", "estado": "aberta", "vencida": false}
  ]
}
```

Regras:

1. Entram só as demandas em que a pessoa é a responsável e que não estão concluídas nem canceladas.
2. Vencida: prazo antes de hoje (fuso do CRIE). Perto do prazo: prazo entre hoje e hoje + `dias_de_antecedencia`, inclusive.
3. Ordem: do prazo mais antigo para o mais novo.
4. Cada item leva só `id`, `prazo`, `estado` e `vencida`. Não leva descrição, categoria, assistido nem texto de histórico: a descrição da demanda pode citar saúde da pessoa atendida. Para ver o conteúdo, o cliente abre a demanda (rota com token, spec 02).
5. Sem pendência: `{"vencidas": 0, "perto_do_prazo": 0, "dias_de_antecedencia": 3, "demandas": []}`.
6. `dias_de_antecedencia` vem de `AVISO_DIAS_ANTES_DO_PRAZO` na configuração (padrão 3).

## 2. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A10 | Quantos dias antes do prazo a demanda conta como "perto do prazo" | 3 dias, configurável |

## 3. Testes que provam esta spec

- O login devolve as vencidas e as perto do prazo de quem entrou, sem as de outra pessoa e sem as encerradas.
- Nenhum item tem descrição, categoria ou assistido.
- Sem pendência, a lista vem vazia com as contagens em zero.

## 4. O que não entra

E-mail (RF41), WhatsApp, aviso em tela fora do login e aviso de encaminhamento pendente.
