# Spec 08 — Relatórios

**Status:** fechada para a primeira versão, em JSON. O formato de impressão e os campos exigidos pela Prefeitura esperam a QA04.
**Origem:** RF35, RF36, RF38, RF39, RNF03, proposta do `contrato-api.md` de 13/10/2026.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Só a direção (`pode_emitir_relatorio`); outro perfil → 403, `{"erro": "Só a direção emite relatórios."}`. O período é obrigatório: sem `de` ou sem `ate` → 422, `{"erro": "Informe o período do relatório (de e ate)."}`; `de` depois de `ate` → 422. Datas `AAAA-MM-DD`, inclusivas, no fuso do CRIE.

Toda emissão grava auditoria `emitir` (spec 05) e a resposta traz `emissao`: `autor_id`, `autor_nome` e `ocorrido_em`, o mesmo momento gravado na auditoria (RF38).

### GET `/api/relatorios/demandas`

Demandas registradas no período (decisão A6, spec 02), com filtros opcionais `estado` (um ou vários separados por vírgula), `categoria` e `responsavel_id` (RF35). Canceladas entram, a não ser que o filtro de estado as tire.

```json
{
  "emissao": {"autor_id": 1, "autor_nome": "...", "ocorrido_em": "2026-11-16T10:00:00-03:00"},
  "periodo": {"de": "2026-10-01", "ate": "2026-10-31"},
  "filtros": {"estado": ["aberta"], "categoria": null, "responsavel_id": null},
  "totais": {
    "total": 12,
    "por_estado": {"aberta": 3, "em_andamento": 4, "aguardando_terceiros": 1, "concluida": 3, "cancelada": 1},
    "vencidas": 2
  },
  "itens": [ ... demandas no formato da spec 02, por último movimento ... ]
}
```

`totais` são os indicadores do período (RF39): abertas por estado, concluídas e vencidas hoje.

### GET `/api/relatorios/assistidos/<assistido_id>`

Acompanhamento de um assistido no período (RF36): `emissao`, `periodo`, `assistido` (`id`, `nome_tratamento`), `evolucoes` vigentes com `data` no período (spec 06) e `encaminhamentos` com `data` no período (spec 07), em ordem cronológica. Assistido inexistente → 404, sem auditoria.

## 2. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| QA04 | Formato e campos do relatório entregue à Prefeitura; exportação para impressão (RF37) | JSON; o cliente monta a tela de impressão |
| A6 | Data que define o período da demanda | data de registro (spec 02) |

## 3. Testes que provam esta spec

- Profissional recebe 403; sem período, 422.
- O relatório de demandas traz só as do período, com os totais por estado e as vencidas.
- O relatório do assistido traz evoluções vigentes e encaminhamentos do período.
- Cada emissão grava `emitir` na auditoria, com o mesmo momento da resposta.

## 4. O que não entra

PDF, planilha, envio por e-mail, agendamento e relatório de auditoria.
