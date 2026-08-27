# sistema-demandas-crie

Sistema web para registro e acompanhamento das demandas levantadas nas reuniões de equipe do **CRIE — Centro de Integração Especial / APAE de Extrema**.

Projeto de extensão curricularizada do curso de Tecnologia em Análise e Desenvolvimento de Sistemas do **IFSP — Câmpus Bragança Paulista**, disciplina Extensão como Metodologia de Ensino 2 (BRAEXT2), sob orientação do Prof. Luiz Gustavo Diniz de Oliveira Véras.

---

## Aviso sobre dados

**Este repositório contém exclusivamente dados fictícios.**

O sistema foi projetado para tratar dados de pessoas atendidas por uma instituição de assistência a pessoas com deficiência, parte delas menores de idade. Nenhum dado real de assistidos ou de suas famílias é versionado, utilizado em desenvolvimento, exibido em protótipos ou apresentado publicamente. Ver requisitos RNF06 e RNF07 em [`docs/requisitos.md`](docs/requisitos.md).

---

## O problema

A equipe do CRIE realiza reuniões semanais em que levanta demandas: providências que precisam ser tomadas por um ou mais profissionais. Hoje essas demandas são anotadas em papel e planilhas, sem controle centralizado. Isso gera perda de tempo ao retomar demandas antigas e demandas esquecidas que ficam sem conclusão.

O sistema centraliza esse registro, torna o andamento visível e preserva o histórico de forma consultável.

---

## Stack

| Camada | Tecnologia |
| --- | --- |
| Front-end | React |
| Back-end | Python + Flask (orientado a objetos) |
| Banco de dados | PostgreSQL |
| Comunicação | API REST |
| Migrações | Alembic |

---

## Estrutura do repositório

```
sistema-demandas-crie/
├── docs/          documentação do projeto
├── backend/       API em Flask
├── frontend/      interface em React
└── docker-compose.yml
```

---

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [`docs/plano-de-projeto.md`](docs/plano-de-projeto.md) | Escopo, cronograma, dependências e como cada frente se desenvolve ao longo do semestre |
| [`docs/requisitos.md`](docs/requisitos.md) | Requisitos funcionais e não funcionais, rastreabilidade e critérios de aceitação |
| [`docs/divisao-de-papeis.md`](docs/divisao-de-papeis.md) | Atribuições detalhadas de cada integrante |

---

## Equipe

| Integrante | Função | Disciplina |
| --- | --- | --- |
| Inácio Fontes | Gerente de Projeto e Analista de Requisitos | Engenharia de Software (BRAENSO) |
| Henry Claro | Analista de Banco de Dados | Banco de Dados 1 (BRABCD1) |
| Gabriel Borba | Analista de Interface e Experiência do Usuário | Interface Humano-Computador (BRAINHC) |
| Miguel Vaz de Souza | Desenvolvedor Back-end | Programação Orientada a Objetos (BRAPROB) |
| Vinícius Marrocos | Desenvolvedor Front-end | Desenvolvimento Web Front End (BRADWFR) |

---

## Como rodar localmente

*Instruções serão adicionadas conforme o desenvolvimento avança.*

```bash
# Subir o banco de dados
docker compose up -d

# Back-end
cd backend
cp .env.example .env        # preencher os valores
pip install -r requirements.txt
flask run

# Front-end
cd frontend
cp .env.example .env
npm install
npm run dev
```

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
