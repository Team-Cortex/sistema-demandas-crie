# Plano de testes de usabilidade

Frente de IHC. Atende o documento do projeto integrado (BRAEXT2 §4.2: planejamento, execução e relatório de usabilidade) e o compromisso publicado no relatório da equipe, objetivo "d": **validar a interface por meio de 8 testes de usabilidade**.

Fundamento (Aula 03): Design Centrado no Usuário, ciclo da ISO 9241-210 — entender o contexto, especificar requisitos, produzir soluções, **avaliar o design**. "O teste não é uma etapa, é uma cultura": os problemas encontrados voltam como correção no sistema, com o PR anotado no relatório.

**Pendências que este plano não decide** (seção 9 do briefing):
- **D4:** quando e com quem serão os 8 testes (profissionais do CRIE ou voluntários). O plano serve aos dois casos (§3).
- **D6:** em que ambiente. O banco de produção não tem usuários; até haver decisão, os testes rodam no **preview da Vercel** ou num computador da equipe com a API local e a carga fictícia (`backend/seed.py`). O [protótipo clicável](prototipo/LEIA-ME.md) roda sem internet e já traz T1 a T7; serve ao menos para o teste-piloto e o ensaio do moderador. Usá-lo nas sessões também faz parte de D6.

---

## 1. Objetivos

1. Verificar se profissionais com pouca familiaridade com tecnologia conseguem, **sem ajuda**, realizar as tarefas principais (RNF11, critério de aceitação 1).
2. Medir **desempenho** (tempo e número de passos), **precisão** (erros e conclusão) e **resposta emocional** (satisfação e confiança).
3. Encontrar problemas de interface, classificá-los por gravidade e corrigi-los antes da entrega.

## 2. Metodologia

| Item | Decisão |
| --- | --- |
| Formato | **Presencial no CRIE** (recomendado: mesmo ambiente, computador e internet de uso real). Alternativa: **remoto**, com compartilhamento de tela |
| Técnica | Teste com tarefas e **pensar em voz alta** (a pessoa fala o que está pensando enquanto usa) |
| Moderação | 1 moderador (lê o roteiro e as tarefas, não ajuda) e 1 anotador (tempo, passos, erros, falas) |
| Duração | 25 a 30 minutos por sessão |
| Sessões | **8**, individuais |
| Dados | **Só fictícios** (RNF06, RNF07). Cada participante usa uma conta de teste `@exemplo.test`. Nenhum dado real de assistido é digitado, nem para "testar de verdade" |
| Gravação | Só da tela e só com autorização no termo (§9). Sem gravar rosto. Se não houver autorização, só anotação |

### Ferramentas de comunicação

| Situação | Ferramenta |
| --- | --- |
| Presencial | Computador do CRIE com navegador; cronômetro do celular do anotador; planilha (§10) impressa ou no notebook do anotador |
| Remoto | Google Meet (gratuito, roda no navegador sem instalar), com compartilhamento de tela do participante; o moderador envia o link do sistema pelo chat da chamada |
| Agendamento | WhatsApp com a direção do CRIE (contato da equipe) |
| Questionário | Papel (presencial) ou Google Forms (remoto), com as perguntas do §8 |

## 3. Participantes

**Perfil demográfico a registrar** (sem nome; cada participante vira P1 a P8):

| Campo | Opções |
| --- | --- |
| Faixa etária | 18–29, 30–39, 40–49, 50–59, 60+ |
| Função | Direção, assistente social, equipe pedagógica, saúde, convivência, outra |
| Tempo na função | menos de 1 ano, 1–5, mais de 5 |
| Uso de computador | todo dia, algumas vezes por semana, raramente |
| Familiaridade com sistemas de cadastro | autodeclarada de 1 (nenhuma) a 5 (muita) |
| Usa óculos ou outro recurso para ler a tela | sim / não |

**Composição desejada:**

| Caso | Composição das 8 sessões |
| --- | --- |
| A — profissionais do CRIE (preferido) | 1 da direção, 3 do serviço social ou saúde, 3 da equipe pedagógica, 1 de outra função. Pelo menos metade com uso de computador "raramente" ou "algumas vezes por semana" |
| B — voluntários de fora | Adultos que **não** são da área de TI, de preferência que trabalhem com atendimento ao público, educação ou saúde, e pelo menos metade com 40 anos ou mais. Registrar no relatório que não são os usuários reais (limita a validade) |

Não participam: integrantes da equipe e colegas de ADS (conhecem o sistema ou a tecnologia demais).

## 4. Tarefas

Tiradas dos cenários (`cenarios-de-uso.md`). Passos mínimos conforme `fluxos.md`. Tempo-limite: se passar dele, o moderador encerra a tarefa e anota "não concluída".

| # | Tarefa (como o moderador lê) | Cenário | Passos mínimos | Tempo-limite | Conclusão = |
| --- | --- | --- | --- | --- | --- |
| T1 | "Você chegou para trabalhar. Descubra quantas demandas estão vencidas e qual delas está vencida há mais tempo." | C1 | 0 (está no painel) | 1 min | Diz o número certo e aponta a demanda |
| T2 | "Na reunião, alguém lembrou de um pedido de material adaptado para a turma da tarde. Descubra o que já foi feito." | C2 | 3 | 1 min | Abre a demanda certa e lê o histórico |
| T3 | "A reunião de saúde acabou. Registre esta demanda: *Solicitar ao CAPSi vaga para avaliação*, prioridade alta, responsável você, prazo daqui a 7 dias." | C3 | 7 | 3 min | Demanda gravada com os dados certos |
| T4 | "Você ligou para o CRAS e agora está esperando a resposta. Atualize a demanda do cadastro da família e anote o que fez." | C4 | 7 (F3 + F4) | 3 min | Estado Aguardando terceiros e anotação gravada |
| T5 | "O material adaptado chegou. Marque a demanda como resolvida e saia do sistema." | C5 | 9 (2×F3 + F9) | 3 min | Estado Concluída e sessão encerrada |
| T6 | "Bruna saiu de férias. Passe a demanda vencida dela para outra pessoa." | C1 | 4 | 2 min | Responsável trocado |
| T7 | "Registre como foi a oficina de música do Assistido Fictício A." | C6 | 7 | 3 min | Evolução gravada e visível na ficha |

Ordem: T1 → T7. T7 só entra quando a tela de evoluções estiver pronta; até lá, a sessão tem T1 a T6.

**Preparação do ambiente antes de cada sessão:** rodar a carga fictícia num banco limpo (ou restaurar o banco de teste), para todo participante encontrar os mesmos dados. Conferir que existe a demanda "Pedir material adaptado para a turma da tarde" (T2, T5), "Solicitar ao CRAS a atualização do cadastro da família" em andamento (T4) e uma demanda vencida de Bruna Fictícia (T1, T6). Conferido em 18/11/2026 na carga atual: a demanda do CRAS começa **Aberta**, e Aberta não passa direto para Aguardando terceiros. Antes de cada sessão, passe-a para Em andamento (ou ajuste a carga). O material adaptado começa Aberta, como T5 prevê. O protótipo já começa com o CRAS em andamento.

## 5. Métricas por tarefa

| Dimensão (BRAEXT2 §4.2) | Métrica | Como medir |
| --- | --- | --- |
| Desempenho | **Tempo** (segundos) | Do fim da leitura da tarefa até a pessoa dizer "terminei" ou o tempo-limite |
| Desempenho | **Número de passos** | Cliques, escolhas e campos preenchidos (mesma regra do `fluxos.md`) |
| Precisão | **Erros** | Clique em lugar que não leva à tarefa, campo preenchido errado, mensagem de erro recebida, voltar atrás |
| Precisão | **Conclusão** | Sim / Sim com ajuda / Não |
| Resposta emocional | **Facilidade da tarefa** | Logo após cada tarefa: "De 1 (muito difícil) a 5 (muito fácil), como foi?" |
| Resposta emocional | **Satisfação e confiança** | Questionário final (§8) |

Indicadores consolidados para o relatório: taxa de conclusão por tarefa, tempo médio e mediano, passos médios ÷ passos mínimos (eficiência), erros médios, média das notas.

## 6. Classificação de gravidade dos problemas

| Nível | Quando |
| --- | --- |
| 4 — Impeditivo | A pessoa não conclui a tarefa |
| 3 — Grave | Conclui, mas com erro, ajuda ou muito mais passos que o mínimo |
| 2 — Moderado | Hesita, volta atrás, comenta que ficou confusa |
| 1 — Cosmético | Comenta algo de aparência ou texto, sem atrapalhar |

## 7. Roteiro do moderador

**Antes (5 min)**
1. Agradecer. "Vamos testar o sistema, não você. Se algo for difícil, a falha é do sistema, e é isso que queremos descobrir." (Don Norman, Aula 03.)
2. Explicar que todos os dados são inventados.
3. Ler e entregar o termo (§9). Só seguir com a assinatura ou o aceite.
4. Preencher o perfil (§3) com a pessoa.
5. Pedir para pensar em voz alta: "Fale o que está procurando e o que espera que aconteça."

**Durante (15–20 min)**
6. Entrar com a conta de teste (o moderador informa e-mail e senha em papel). O tempo de T1 começa com o painel aberto.
7. Ler cada tarefa em voz alta e deixar o papel com o texto na mesa.
8. **Não ajudar.** Se pedirem ajuda: "O que você tentaria?" Se travar por mais de 1 minuto ou passar do tempo-limite, encerrar a tarefa com gentileza e seguir.
9. Depois de cada tarefa: a pergunta de facilidade (1 a 5).

**Depois (5 min)**
10. Questionário final (§8).
11. Perguntas abertas: "O que foi mais fácil?", "O que foi mais difícil?", "Usaria isso no lugar do papel? Por quê?"
12. Agradecer. Clicar em **Sair** e restaurar os dados para a próxima sessão.

## 8. Questionário de satisfação e confiança

Escala de 1 (discordo totalmente) a 5 (concordo totalmente).

| # | Afirmação |
| --- | --- |
| Q1 | Foi fácil entender o que cada tela mostra. |
| Q2 | Os nomes dos botões e menus são as palavras que eu uso no trabalho. |
| Q3 | Eu conseguiria registrar uma demanda sozinha(o), sem ajuda. |
| Q4 | Eu sabia o que fazer quando apareceu uma mensagem de erro. |
| Q5 | Eu me senti segura(o) de que o que registrei ficou guardado. |
| Q6 | Ficou claro quais demandas estão atrasadas. |
| Q7 | Eu usaria este sistema no lugar do papel e da planilha. |
| Q8 | De modo geral, fiquei satisfeita(o) com o sistema. |

Q5 mede **confiança**; Q8 mede **satisfação** geral; Q1 a Q4 e Q6 dizem onde está o problema quando a nota cai.

## 9. Termo de participação voluntária

> **Termo de participação voluntária — teste de usabilidade**
>
> Projeto de extensão "Sistema de Demandas do CRIE", curso de Tecnologia em Análise e Desenvolvimento de Sistemas, IFSP Câmpus Bragança Paulista.
>
> Você está sendo convidada(o) a usar uma versão de teste de um sistema e dar sua opinião. O objetivo é avaliar o **sistema**, e não você.
>
> - A participação é **voluntária**. Você pode parar a qualquer momento, sem precisar explicar o motivo.
> - O teste dura cerca de 30 minutos.
> - Todos os dados que aparecem no sistema são **inventados**. Não digite nenhum dado real de pessoas atendidas.
> - Anotamos tempo, cliques, erros e o que você comentar. **Seu nome não aparece** em nenhum relatório: você será identificada(o) como "Participante 1", "Participante 2" etc.
> - Gravação da tela: ( ) autorizo ( ) não autorizo. Se autorizada, a gravação mostra só a tela, é usada apenas pela equipe para conferir as anotações e é apagada depois da entrega do relatório.
> - Não há pagamento nem custo.
>
> Dúvidas: equipe do projeto, pelo contato da direção do CRIE.
>
> Declaro que li e aceito participar.
>
> Nome: ______________________ Assinatura: ______________________ Data: ___/___/______

O termo assinado fica com a equipe, fora do repositório (tem nome real).

## 10. Planilha modelo

Arquivo: [`planilha-resultados-modelo.csv`](planilha-resultados-modelo.csv) (abre no Excel, no LibreOffice ou no Google Planilhas). Uma linha por participante e tarefa. Colunas:

`participante, sessao_data, formato, tarefa, tempo_s, passos, passos_minimos, erros, conclusao, nota_facilidade, observacoes`

Questionário final e perfil têm modelos próprios: [`questionario-modelo.csv`](questionario-modelo.csv) e [`perfil-participantes-modelo.csv`](perfil-participantes-modelo.csv). No Google Planilhas, viram três abas do mesmo arquivo.

**Os dados brutos não entram no repositório se tiverem nome ou qualquer informação que identifique alguém.** Só a planilha já anonimizada (P1 a P8).
