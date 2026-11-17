# Servidor — arquitetura cliente-servidor

Este diretório é o **servidor**. O **cliente** é o React em `frontend/`. Os dois processos se falam por HTTP em `/api`. O cliente não importa este pacote e não conecta no PostgreSQL.

As pastas `routes/`, `schemas/` e `services/` já têm um arquivo por recurso das specs 01 a 04. Cada arquivo marca o lugar; as rotas ainda não estão registradas. Os models de domínio já existem em `app/models/` (mapa em [`docs/estado-do-projeto.md`](../docs/estado-do-projeto.md)).

Dentro do servidor a requisição atravessa quatro camadas, nesta ordem:

1. `app/schemas/` valida e serializa.
2. `app/routes/` traduz HTTP em chamada de domínio.
3. `app/services/` aplica a regra de negócio.
4. `app/models/` persiste e guarda as regras que não podem ser contornadas (transição de estado, imutabilidade do histórico, senha só em hash).

O contrato está em [`docs/contrato-api.md`](../docs/contrato-api.md). As specs em `docs/specs/` vencem o código quando divergirem.

Nesta etapa o processo sobe e responde `GET /api/saude` e `GET /api/teste` (`Hello World`). Login, demanda, assistido e reunião estão especificados e ainda não têm rota.

## Subir localmente

```bash
docker compose up -d
cd backend
cp .env.example .env
pip install -r requirements.txt
flask db upgrade
flask run
```

`flask run` usa `backend/.flaskenv`. Saúde: `http://127.0.0.1:5000/api/saude`.

## Migrações

O schema do banco é versionado em `migrations/` (Flask-Migrate / Alembic). Depois de mudar um model:

```bash
flask db migrate -m "descrição curta"
# revise o arquivo gerado em migrations/versions/
flask db upgrade
```

`flask db downgrade` desfaz a última migração.

## Dados fictícios (seed)

Para desenvolvimento e demonstração. **Nunca com dado real do CRIE.**

1. No `.env`, preencha `SEED_DIRECAO_SENHA` e `SEED_SENHA_PADRAO` com senhas suas, de pelo menos 8 caracteres. Nome e e-mail da direção já vêm no `.env.example`.
2. Com o banco migrado (`flask db upgrade`), rode a partir de `backend/`:

```bash
python seed.py
```

O que entra:

| Tipo | Conteúdo |
| --- | --- |
| Usuários | uma direção (do `.env`), uma assistente social e um profissional da equipe pedagógica, todos `@exemplo.test` |
| Assistidos | dois, com nome de tratamento fictício e profissionais vinculados |
| Reuniões | uma por setor (pedagógico, saúde, convivência), com participantes |
| Demandas | uma em cada estado, duas vencidas ainda abertas, com anotações e uma troca de responsável no histórico |
| Evoluções | uma simples e uma retificada |
| Encaminhamentos | pendentes e um com desfecho |

Os profissionais entram com a senha de `SEED_SENHA_PADRAO`. Rodar de novo não duplica nada. Com `FLASK_ENV=production` o comando recusa e sai com erro.

## Testes

```bash
pytest
node scripts/check-segredo.mjs
```

O banco local do Compose usa usuário, senha e base `crie`. Isso vale só na máquina de desenvolvimento. Produção lê variável de ambiente e não reaproveita esse valor.
