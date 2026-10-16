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
├── docs/                 documentação compartilhada
├── backend/              servidor Flask
├── frontend/             cliente React
└── docker-compose.yml    PostgreSQL local
```

---

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [`docs/plano-de-projeto.md`](docs/plano-de-projeto.md) | Escopo, cronograma, dependências e como cada frente se desenvolve ao longo do semestre |
| [`docs/requisitos.md`](docs/requisitos.md) | Requisitos funcionais e não funcionais, rastreabilidade e critérios de aceitação |
| [`docs/divisao-de-papeis.md`](docs/divisao-de-papeis.md) | Atribuições detalhadas de cada integrante |
| [`docs/arquitetura.md`](docs/arquitetura.md) | Cliente-servidor, camadas do servidor e decisões já tomadas |
| [`docs/contrato-api.md`](docs/contrato-api.md) | Proposta de contrato HTTP entre o React e o Flask |
| [`docs/specs/`](docs/specs/) | Comportamento do servidor, na ordem de implementação |
| [`docs/estado-do-projeto.md`](docs/estado-do-projeto.md) | Mapa geral do que o sistema é hoje, mantido pela frente de back-end |
| [`docs/commits.md`](docs/commits.md) | Como a frente de back-end separa cada mudança num commit |
| [`docs/documentacao.md`](docs/documentacao.md) | Quando a frente de back-end atualiza o mapa no mesmo commit |

---

## Equipe

| Integrante | Função | Disciplina |
| --- | --- | --- |
| Vinícius Marrocos | Gerente de Projeto e Analista de Requisitos | Engenharia de Software (BRAENSO) |
| Henry Claro | Analista de Banco de Dados | Banco de Dados 1 (BRABCD1) |
| Inácio Fontes | Analista de Interface e Experiência do Usuário | Interface Humano-Computador (BRAINHC) |
| Miguel Vaz | Desenvolvedor Back-end | Programação Orientada a Objetos (BRAPROB) |
| Gabriel Borba | Desenvolvedor Front-end | Desenvolvimento Web Front End (BRADWFR) |

---

## Como rodar localmente

O servidor é o Flask em `backend/`. O cliente é o React em `frontend/`, com os mesmos arquivos que estavam na raiz. Detalhe do servidor em [`backend/README.md`](backend/README.md).

```bash
# Subir o banco de dados
docker compose up -d

# Servidor
cd backend
cp .env.example .env        # preencher os valores
pip install -r requirements.txt
flask run

# Cliente
cd frontend
npm install
npm run dev
```

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
