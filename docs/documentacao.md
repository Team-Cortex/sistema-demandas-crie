# Documentação no mesmo commit

Acordo da frente de back-end, irmão de [`commits.md`](commits.md). Vale para Miguel e para o agente neste ambiente.

A atualização no mesmo commit é viável aqui porque o agente acompanha a mudança. Não é regra do time e não se espera que as outras frentes mantenham Markdown em tempo real.

## 1. A regra

**O commit nosso que muda o servidor, o contrato ou o mapa leva junto o texto nosso que essa mudança torna falso.**

[`estado-do-projeto.md`](estado-do-projeto.md) é o mapa. Ele é atualizado por nós quando o commit muda algo que o mapa afirma: o que o servidor responde, a estrutura que descrevemos, uma decisão que fechamos, o que ainda está só especificado. Commit que não muda nenhum desses fatos não mexe no mapa.

Documento de outra frente (requisitos, plano, modelagem, telas) não entra neste acordo. Se a nossa mudança o deixar desalinhado, avisamos o dono. Não reescrevemos o arquivo dele para "acompanhar o commit".

## 2. O que mudou e onde atualizar

| Mudou, por nós | Atualizamos |
| --- | --- |
| O que está no ar, a estrutura que o mapa descreve, uma decisão nossa que saiu de aberta | [`estado-do-projeto.md`](estado-do-projeto.md) |
| Rota, corpo, código de erro, autenticação | [`contrato-api.md`](contrato-api.md) e a spec em [`specs/`](specs/) |
| Regra de negócio do servidor | A spec correspondente |
| Como subir o servidor | [`../backend/README.md`](../backend/README.md) e o `.env.example` |

## 3. O que esta regra não muda

- Spec ou decisão nova nossa nasce num commit `docs` próprio, antes do código que a cumpre.
- O Markdown entra no commit porque descreve aquela ação. Texto sem relação vai num commit `docs` separado.
- Refatoração sem mudança de comportamento não reescreve o mapa.
- Nada a descrever, nada a mudar.
