# Servidor — arquitetura cliente-servidor

Este diretório é o **servidor**. O **cliente** é o React em `frontend/`. Os dois processos se falam por HTTP em `/api`. O cliente não importa este pacote e não conecta no PostgreSQL.

As pastas `routes/`, `schemas/`, `services/` e `models/` já têm um arquivo por recurso das specs 01 a 04. Cada arquivo marca o lugar. A rota ainda não está registrada: quem implementa é a frente de back-end, depois do modelo relacional.

Dentro do servidor a requisição atravessa quatro camadas, nesta ordem:

1. `app/schemas/` valida e serializa.
2. `app/routes/` traduz HTTP em chamada de domínio.
3. `app/services/` aplica a regra de negócio.
4. `app/models/` persiste. As entidades de domínio entram quando o modelo relacional fechar.

O contrato está em [`docs/contrato-api.md`](../docs/contrato-api.md). As specs em `docs/specs/` vencem o código quando divergirem.

Nesta etapa o processo sobe e responde `GET /api/saude` e `GET /api/teste` (`Hello World`). Login, demanda, assistido e reunião estão especificados e ainda não têm rota: a persistência espera o script de tabelas do banco.

## Subir localmente

```bash
docker compose up -d
cd backend
cp .env.example .env
pip install -r requirements.txt
flask run
```

`flask run` usa `backend/.flaskenv`. Saúde: `http://127.0.0.1:5000/api/saude`.

```bash
pytest
node scripts/check-segredo.mjs
```

O banco local do Compose usa usuário, senha e base `crie`. Isso vale só na máquina de desenvolvimento. Produção lê variável de ambiente e não reaproveita esse valor.
