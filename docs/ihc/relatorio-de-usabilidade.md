# Relatório de usabilidade

Frente de IHC. Estrutura do relatório pedida no documento do projeto integrado (BRAEXT2 §4.2, item 4): perfil dos voluntários, tabelas e gráficos das medições, lista detalhada dos problemas com sugestão de correção.

> **Situação: testes ainda não executados.** Todas as tabelas abaixo estão vazias de propósito. Nenhum número, fala ou resultado é preenchido antes de os testes acontecerem com participantes reais (`plano-de-testes.md`). Quando a equipe trouxer as planilhas anonimizadas, os números entram aqui e os gráficos são gerados a partir delas.

---

## 1. Como os testes foram feitos

| Item | Preencher |
| --- | --- |
| Datas das sessões | |
| Local / formato | presencial no CRIE / remoto |
| Ambiente do sistema | preview da Vercel / computador da equipe com API local |
| Versão testada (commit) | |
| Moderador(es) e anotador(es) | |
| Sessões realizadas | __ de 8 |
| Tarefas aplicadas | T1 a T__ |

Desvios em relação ao plano: *(preencher; por exemplo, sessão interrompida, tarefa pulada, participante de fora do perfil)*

## 2. Perfil dos voluntários

| Participante | Faixa etária | Função | Tempo na função | Uso de computador | Familiaridade (1–5) |
| --- | --- | --- | --- | --- | --- |
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |
| P4 | | | | | |
| P5 | | | | | |
| P6 | | | | | |
| P7 | | | | | |
| P8 | | | | | |

Resumo: *(quantos do CRIE, quantos voluntários de fora; distribuição de idade e de uso de computador)*

## 3. Resultados por tarefa

### 3.1 Desempenho e precisão

| Tarefa | Conclusão (sim / com ajuda / não) | Tempo médio (s) | Tempo mediano (s) | Passos médios | Passos mínimos | Eficiência (mín ÷ médio) | Erros médios | Facilidade média (1–5) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 Ver vencidas | | | | | 0 | — | | |
| T2 Achar demanda antiga | | | | | 3 | | | |
| T3 Registrar demanda | | | | | 7 | | | |
| T4 Atualizar e anotar | | | | | 7 | | | |
| T5 Concluir e sair | | | | | 9 | | | |
| T6 Trocar responsável | | | | | 4 | | | |
| T7 Lançar evolução | | | | | 7 | | | |

Critérios de aceitação ligados (`requisitos.md` §8): T3 sem ajuda (critério 1); T2 em menos de 60 s (critério 2); T1 numa tela só (critério 3); T7 (critério 4).

### 3.2 Gráficos

Gerados a partir da planilha consolidada, com os mesmos números das tabelas:
1. **Taxa de conclusão por tarefa** — barras empilhadas (sim / com ajuda / não).
2. **Tempo por tarefa** — pontos de cada participante com a mediana marcada, e a linha do tempo-limite.
3. **Passos medidos × passos mínimos** — barras lado a lado por tarefa.
4. **Questionário Q1 a Q8** — barras divergentes (1–2, 3, 4–5).

*(inserir as imagens aqui; guardar em `docs/ihc/graficos/`)*

## 4. Resposta emocional

| Afirmação | Média | 1–2 (discorda) | 3 | 4–5 (concorda) |
| --- | --- | --- | --- | --- |
| Q1 Fácil entender cada tela | | | | |
| Q2 Palavras do trabalho | | | | |
| Q3 Registraria sozinha(o) | | | | |
| Q4 Sabia o que fazer no erro | | | | |
| Q5 Confiança de que ficou guardado | | | | |
| Q6 Claro o que está atrasado | | | | |
| Q7 Usaria no lugar do papel | | | | |
| Q8 Satisfação geral | | | | |

Comentários abertos (anonimizados, só P1 a P8): *(transcrever o que foi dito, sem editar o sentido)*

## 5. Problemas encontrados

Gravidade conforme `plano-de-testes.md` §6 (4 impeditivo, 3 grave, 2 moderado, 1 cosmético). Um problema por linha, mesmo que vários participantes tenham tido.

| # | Problema | Tela | Tarefa | Participantes | Gravidade | Sugestão de correção | Corrigido em (PR) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U1 | | | | | | | |

## 6. Conclusão

*(o que funcionou, o que foi corrigido, o que ficou para depois e por quê; resposta ao critério de aceitação 7: "a equipe da instituição avaliar a interface como compreensível")*
