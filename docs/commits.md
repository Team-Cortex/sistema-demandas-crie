# Commits unitários

Acordo da frente de back-end: Miguel e o agente neste ambiente. Não é regra das outras frentes. Quem produz em outro ritmo commita do jeito que a equipe já combina.

Se um commit nosso e este arquivo divergirem, este arquivo vence e o próximo commit nosso volta à regra.

O mapa do sistema está em [`estado-do-projeto.md`](estado-do-projeto.md). Quando um commit nosso tornar falso algo que esse mapa afirma, a correção entra no mesmo commit ([`documentacao.md`](documentacao.md)). Isso também é acordo nosso, não obrigação do time.

---

## 1. A regra

**Cada ação nossa tem um commit próprio.** Ação é uma mudança com um propósito só, que pode ser lida, revisada e revertida sozinha.

| É uma ação | Exemplo de título |
| --- | --- |
| Um documento ou uma decisão | `docs(contrato): registra o formato de erro da API` |
| A superfície de uma pasta, sem regra nova | `chore(servidor): reserva os módulos das specs 01 a 04` |
| Uma rota com o teste que a prova | `feat(acesso): autentica por e-mail e senha` |
| Uma correção | `fix(demanda): recusa reabrir demanda concluída` |
| Um teste ou uma guarda | `test(saude): exige resposta mínima em /api/saude` |
| Uma dependência | `chore(deps): adiciona Flask-JWT-Extended` |
| Uma refatoração sem mudança de comportamento | `refactor(servidor): extrai o registro de erros` |

## 2. O que não entra junto

- Duas specs ou duas rotas no mesmo commit.
- Documento sem relação com a ação. O documento nosso que a ação torna falso vai junto.
- Refatoração e comportamento novo.
- Formatação em massa e mudança de lógica.
- Correção de revisão misturada com a feature: a correção é o commit seguinte.
- Título com "e", "ajustes gerais" ou "wip". Se o título precisa de "e", são dois commits.

## 3. Cada commit fica de pé sozinho

O que já existe continua executável em todo commit nosso, não só no último. A ordem respeita a dependência: contrato ou spec, depois o código que os cumpre, teste no mesmo commit da rota quando o teste é a prova daquela rota.

## 4. Mensagem

```
<tipo>(<escopo>): <efeito, em português, no presente>

<por quê, em uma a três linhas; cite a spec quando houver>
```

- `tipo`: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.
- `escopo`: `acesso`, `demanda`, `assistido`, `reuniao`, `servidor`, `contrato`, `docs`, `deps`.
- O título diz o efeito, não o nome do arquivo.
- Sem trailer de ferramenta. Nenhum `Co-Authored-By` de agente, nenhum "Generated with". O autor é a pessoa.

Commits nossos saem da conta **miguelvzs**. Se o `gh` estiver em outra conta, o passo anterior é `gh auth switch`.

## 5. Como montar

1. Ver o que mudou e corrigir o Markdown nosso que ficou falso.
2. Adicionar por caminho. Não usar `git add -A` quando houver mais de uma ação pendente.
3. Conferir o que está no índice: só os arquivos daquela ação.
4. Commitar. Repetir para a próxima ação.

## 6. Histórico

Commit que já está no GitHub não se reescreve. A regra vale do próximo commit nosso em diante.

No pull request desta frente, o merge que preserva os commits unitários é o que mantém o histórico legível. Squash junta tudo num commit só.
