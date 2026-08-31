# Divisão de Papéis — Projeto Integrado de Extensão (BRAEXT2)

**Projeto:** Sistemas em Ação — Desenvolvimento de Soluções Digitais para Demandas Comunitárias
**Parceiro externo:** CRIE / APAE de Extrema (contato: Agnes, diretora)
**Equipe:** Inácio Fontes, Henry Claro, Gabriel Borba, Miguel Vaz, Vinicius Marrocos
**Entrega final:** 26/11/2026

---

## 1. Como este documento deve ser lido

Cada pessoa é **dona** de uma frente, não executora exclusiva dela. Ser dono significa: garantir que a entrega saia, cobrar quem precisa contribuir, revisar antes de ir para o professor e responder pela frente na apresentação.

Duas consequências práticas:

- **Todo mundo programa no final.** A partir de outubro, quando o desenvolvimento concentra, quem estiver com a frente mais leve migra para código. Ninguém termina o semestre sem ter contribuído com o sistema.
- **A carga não é simultânea.** Engenharia de Software, IHC e Banco de Dados pesam de agosto a outubro. Back-end e front-end pesam de outubro a novembro. Quem ficar com uma frente tardia precisa estar no relatório e nos testes até lá — não parado.

---

## 2. Atribuições

### Vinícius Marrocos — Gerente de Projeto e Analista de Requisitos
**Disciplina:** Engenharia de Software (BRAENSO)

**Responsabilidades**

- Manter o board Kanban no Trello atualizado, com colunas Backlog / A Fazer / Em Andamento / Em Revisão / Concluído e as cores por disciplina definidas pelo professor
- Adicionar o professor como membro do board e garantir que ele esteja atualizado **antes de cada apresentação** — isso é critério de nota explícito
- Produzir o documento de requisitos, separando requisitos funcionais de não funcionais
- Organizar o repositório Git: estrutura, padrão de commits, branches
- Planejar verificação, validação e testes de software
- Escrever a seção de Engenharia de Software e a discussão sobre qualidade de software

**Quando pesa:** setembro e outubro — e de forma contínua até o fim.

**Perfil ideal:** a pessoa mais organizada e mais insistente do grupo, não necessariamente a mais técnica. Nas entregas 1 e 2, o relatório e o Kanban valem 10,0 de 10,0 pontos: nessa fase, esta frente *é* a nota da equipe.

---

### Henry Claro — Analista de Banco de Dados
**Disciplina:** Banco de Dados 1 (BRABCD1)

**Responsabilidades**

- Escrever a especificação do minimundo a partir do que for levantado com o CRIE
- Produzir o Diagrama Entidade-Relacionamento (modelagem conceitual)
- Produzir o modelo relacional com tabelas, atributos e restrições
- Escrever os scripts SQL de criação (`CREATE TABLE`) e carga inicial (`INSERT`)
- Escrever as consultas de demonstração (`SELECT`, `INSERT`, `UPDATE`, `DELETE`)
- Escrever a seção de banco de dados do relatório

**Quando pesa:** setembro e outubro. Depois disso, migra para o back-end — é a transição mais natural do grupo.

**Prazo crítico:** o modelo relacional precisa estar fechado até **01/10**, não até 22/10. O back-end não começa antes disso.

**Perfil ideal:** quem tiver mais familiaridade com SQL e com pensar em estrutura de dados.

---

### Inácio Fontes — Analista de Interface e Experiência do Usuário
**Disciplina:** Interface Humano-Computador (BRAINHC)

**Responsabilidades**

- Elaborar personas e cenários a partir do contato com o CRIE
- Construir protótipo interativo de média ou alta fidelidade no Figma, com navegação entre telas
- Planejar os testes de usabilidade: metodologia (remoto ou presencial), perfil demográfico dos participantes, tarefas baseadas nos cenários
- Executar os testes medindo desempenho (tempo e número de passos), precisão (taxa de erros) e resposta emocional (satisfação e confiança)
- Produzir o relatório de usabilidade com tabelas, gráficos e lista de problemas encontrados com sugestões de correção
- Conduzir o banner e a apresentação da EXPOEX

**Quando pesa:** setembro a outubro (protótipo e testes), depois novembro (banner).

**Atenção — esta é a frente de maior peso na nota.** A Mostra de Extensão vale 35% da média final, mais que a entrega final do sistema (20%). Quem assumir precisa estar disposto a apresentar em público.

**Perfil ideal:** quem tiver sensibilidade visual e desenvoltura para falar com pessoas — tanto com o pessoal do CRIE quanto na mostra.

---

### Miguel Vaz de Souza — Desenvolvedor Back-end
**Disciplina:** Programação Orientada a Objetos (BRAPROB) — Python e Flask

**Responsabilidades**

- Modelar as classes do sistema aplicando encapsulamento, herança e polimorfismo — a disciplina cobra esses conceitos explicitamente, não basta código que funcione
- Desenvolver a API web em Flask
- Integrar o back-end ao banco de dados
- Definir e documentar, junto ao front-end, o contrato da API (endpoints, parâmetros, formato de resposta)
- Escrever a seção de POO do relatório

**Quando pesa:** outubro e novembro. Antes disso, contribui com requisitos e com a modelagem junto ao Banco de Dados.

**Depende de:** modelo relacional fechado. Sem tabelas definidas não há como escrever os models.

**Perfil ideal:** quem já programou em Python, ou quem estiver disposto a estudar a fundo — esta frente não se improvisa em três semanas.

---

### Gabriel Borba — Desenvolvedor Front-end
**Disciplina:** Desenvolvimento Web Front End (BRADWFR) — React

**Responsabilidades**

- Construir a interface em React, organizada em componentes reutilizáveis
- Implementar funcionalidades dinâmicas em JavaScript: validação de formulários e requisições assíncronas ao back-end
- Garantir responsividade e acessibilidade
- Definir e documentar, junto ao back-end, o contrato da API
- Escrever a seção de front-end do relatório

**Quando pesa:** outubro e novembro. Antes disso, contribui com o protótipo no Figma junto ao IHC — o protótipo vira a referência direta das telas.

**Depende de:** protótipo validado (IHC) e API disponível (back-end).

**Perfil ideal:** quem tiver mais facilidade com JavaScript. Vale considerar colocar as duas pessoas mais fortes tecnicamente nas frentes D e E: são as duas pontas do contrato da API, e é ali que a integração costuma quebrar.

---

## 3. Responsabilidades compartilhadas

Estas não pertencem a uma frente e precisam de nome definido:

| Responsabilidade | Por quê |
| --- | --- |
| **Compilador do relatório** | Cinco pessoas escrevendo seções soltas produzem um documento com cinco vozes e formatação quebrada. Uma pessoa consolida em ABNT antes de cada entrega. Não escreve tudo — padroniza. |
| **Contato com o CRIE** | Precisa ser alguém com disponibilidade em horário comercial, já que a instituição responde durante o dia. O canal com a Agnes já está aberto, mas não deve depender de uma única pessoa. |
| **Registro de evidências** | Prints de conversas, fotos de visitas, documentos assinados. Vão para os anexos do relatório e comprovam o contato com a comunidade externa. Alguém precisa arquivar isso desde já. |

---

## 4. Dependências entre as frentes

A ordem importa. Quem atrasa trava o próximo:

1. **Contato com o CRIE** → define o problema real
2. **Requisitos (Vinícius)** → transformam o problema em especificação
3. **Minimundo e DER (Henry)** → estruturam os dados
4. **Personas e protótipo (Inácio)** → definem as telas
5. **Modelo relacional fechado (Henry)** → libera o back-end
6. **API (Miguel)** → libera a integração do front-end
7. **Testes de usabilidade (Inácio)** → validam com o público-alvo

O gargalo mais provável do semestre é o passo 5. Se o modelo relacional escorregar para o fim de outubro, back-end e front-end ficam espremidos em três semanas.

---

## 5. Calendário e quem lidera cada entrega

| Entrega | Data | Peso | Quem lidera |
| --- | --- | --- | --- |
| ET1 | 03/09 | 5% | Vinícius + contato com o CRIE |
| ET2 | 01/10 | 10% | Vinícius + B + C |
| ET3 | 22/10 | 10% | Henry + D |
| ET4 | 05/11 | 15% | Miguel + E |
| EXPOEX | 18/11 | 35% | Inácio (banner) — mas **todos** apresentam |
| ET5 | 26/11 | 20% | Todos |
| Simulado ENADE | — | 5% | Individual |

**Fórmula da média final:**
`MF = ET1×0,05 + ET2×0,10 + ET3×0,10 + ET4×0,15 + ME×0,35 + ET5×0,20 + EN×0,05`

---

## 6. Combinados sugeridos

- Board no Trello criado e com o professor adicionado **antes de 03/09**
- Contrato da API definido em setembro, no papel, antes de existir código
- Ciclos de duas semanas, com o board atualizado antes de cada apresentação
- Toda decisão tomada com o CRIE registrada por escrito e compartilhada com o grupo
- Nenhum dado real de usuários ou famílias do CRIE em repositório, planilha ou protótipo — apenas dados fictícios. São dados pessoais sensíveis e a maior parte envolve menores de idade
