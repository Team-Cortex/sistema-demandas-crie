# Servidor — arquitetura cliente-servidor

Este diretório é o **servidor**. O **cliente** é o React em `frontend/`. Os dois processos se falam por HTTP em `/api`. O cliente não importa este pacote e não conecta no PostgreSQL.

Dentro do servidor a requisição atravessa quatro camadas, nesta ordem:

1. `app/schemas/` valida e serializa (marshmallow).
2. `app/routes/` traduz HTTP em chamada de domínio; `routes/sessao.py` exige o token e verifica o perfil.
3. `app/services/` aplica a regra de negócio e grava a auditoria.
4. `app/models/` persiste e guarda as regras que não podem ser contornadas (transição de estado, imutabilidade do histórico, da evolução e da auditoria, senha só em hash).

O contrato está em [`docs/contrato-api.md`](../docs/contrato-api.md); o que já responde, rota por rota, está no §2 dele. As specs em [`docs/specs/`](../docs/specs/) vencem o código quando divergirem.

---

## Instalação do zero

### Pré-requisitos

| Ferramenta | Para quê | Obrigatória? |
| --- | --- | --- |
| Python 3.12 | o servidor | sim |
| Git | clonar | sim |
| Docker (Docker Desktop no Windows) | o PostgreSQL local do `docker-compose.yml` | para rodar o servidor; os testes não precisam |
| Node 18 ou mais novo | `scripts/check-segredo.mjs` | só para a verificação de segredo |

### Passo a passo

Os comandos abaixo são do bash (Linux, macOS ou Git Bash). No PowerShell, a ativação do ambiente é `.venv\Scripts\Activate.ps1` e a cópia é `Copy-Item .env.example .env`.

```bash
# 1. Código
git clone https://github.com/Team-Cortex/sistema-demandas-crie.git
cd sistema-demandas-crie

# 2. Banco local (na raiz do repositório)
docker compose up -d

# 3. Ambiente Python, só para este projeto
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 4. Configuração local
cp .env.example .env
```

5. Abra o `.env` e preencha (o arquivo não vai para o Git):
   - `DATABASE_URL`: no exemplo, troque `USUARIO` e `SENHA` pelos do `docker-compose.yml` (os dois são `crie`) e `host` por `localhost`. Esses valores só valem na sua máquina.
   - `SECRET_KEY` e `JWT_SECRET_KEY`: textos aleatórios seus. Para gerar: `python -c "import secrets; print(secrets.token_hex(32))"`.
   - `SEED_DIRECAO_SENHA` e `SEED_SENHA_PADRAO`: senhas suas, de pelo menos 8 caracteres, para a carga fictícia.

```bash
# 6. Tabelas
flask db upgrade

# 7. Dados fictícios (opcional, recomendado)
python seed.py

# 8. Servidor em http://127.0.0.1:5000
flask run
```

`flask run` usa `backend/.flaskenv`. Para conferir: `http://127.0.0.1:5000/api/saude` responde `{"ok": true, "status": "ok"}`.

### Primeira chamada autenticada

Com a carga fictícia, a direção entra com o e-mail `SEED_DIRECAO_EMAIL` e a senha `SEED_DIRECAO_SENHA` do `.env`:

```bash
curl -s -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "direcao@exemplo.test", "senha": "<SEED_DIRECAO_SENHA>"}'
# → {"token": "...", "perfil": "direcao", "usuario": {...}, "avisos": {...}}

curl -s http://127.0.0.1:5000/api/demandas/painel -H "Authorization: Bearer <token>"
```

O token vale 30 minutos. `POST /api/auth/logout` encerra antes.

---

## Variáveis de ambiente

| Variável | Uso | Padrão |
| --- | --- | --- |
| `FLASK_ENV` | `development`, `testing` ou `production`. Em `production`, faltar `SECRET_KEY`, `JWT_SECRET_KEY` ou `DATABASE_URL` impede o servidor de subir | `development` |
| `DATABASE_URL` | PostgreSQL; `postgres://` e `postgresql://` viram `postgresql+psycopg://` sozinhos (`config.url_do_banco`) | vazio: sobe sem banco, só `/api/saude` |
| `SECRET_KEY`, `JWT_SECRET_KEY` | assinatura do Flask e do JWT | só em desenvolvimento há um valor local |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | validade do token | `30` |
| `CORS_ORIGINS` | origens do front-end separadas por vírgula; `*` não abre nada | `http://localhost:5173` em desenvolvimento, vazio em produção |
| `AVISO_DIAS_ANTES_DO_PRAZO` | dias que contam como "perto do prazo" no aviso do login (spec 09) | `3` |
| `SEED_*` | carga fictícia (`python seed.py`) | sem padrão para as senhas |

Front-end e API na mesma origem (como na Vercel) não precisam de CORS.

---

## Migrações

O schema do banco é versionado em `migrations/` (Flask-Migrate / Alembic).

| Revisão | O que cria |
| --- | --- |
| `b0f13416410c` | modelo de domínio, tipos enum e triggers que recusam alterar histórico e evolução e excluir demanda e encaminhamento |
| `3df29fd96f0b` | `token_revogado`, para o logout |
| `3f00c11df825` | `auditoria`, somente inserção (trigger recusa UPDATE e DELETE) |

Depois de mudar um model:

```bash
flask db migrate -m "descrição curta"
# revise o arquivo gerado em migrations/versions/
flask db upgrade
```

`flask db downgrade` desfaz a última migração. O teste `tests/test_migracoes.py` falha se um model mudar sem migração.

---

## Dados fictícios (seed)

### Primeiro acesso sem carga de demonstração

Num banco já migrado e **sem nenhum usuário**, o comando administrativo cria somente a primeira direção:

```bash
cd backend
flask criar-primeira-direcao --nome "Direção Fictícia" --email "direcao@exemplo.test"
```

O nome e o e-mail acima servem para validação fictícia. No ambiente publicado, confirme a identidade com o responsável. A senha é solicitada duas vezes em prompt oculto; não a coloque em argumentos, commits ou relatórios. O comando usa as mesmas validações e o hash do cadastro pela API.

Se já houver qualquer usuário, inclusive inativo, o comando recusa sem alterar nada. Não cria tabelas nem dados de assistidos, reuniões ou demandas. As próximas contas são criadas pela direção em `POST /api/usuarios`. O `seed.py` abaixo continua proibido em produção.

Antes de operar o banco publicado, confira o projeto e o ambiente selecionados, as migrações e a liberação operacional. Não copie credenciais de produção para o `.env` de desenvolvimento. Roteiro e limites da validação: [`docs/validacao-primeiro-acesso.md`](../docs/validacao-primeiro-acesso.md).

### Carga fictícia de desenvolvimento

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

---

## Testes

```bash
pytest
node scripts/check-segredo.mjs
```

A suíte usa SQLite em memória, criado e descartado a cada teste: **não precisa de Docker nem de PostgreSQL**. Os testes de rota (`tests/test_*_api.py`) usam a fixture `api` do `tests/conftest.py`, com uma pessoa fictícia de cada perfil e uma inativa; cada requisição abre o próprio contexto, como no servidor. A diferença conhecida: no SQLite, maiúscula acentuada não casa sem diferenciar maiúscula (área "SAÚDE" × "saúde"); no PostgreSQL casa.

A suíte inteira leva alguns minutos porque cada hash de senha custa cerca de 0,3 s. Para rodar em paralelo na sua máquina, `pip install pytest-xdist` e `pytest -n auto` (o plugin não está no `requirements.txt`).

O banco local do Compose usa usuário, senha e base `crie`. Isso vale só na máquina de desenvolvimento. Produção lê variável de ambiente e não reaproveita esse valor.

---

## Onde fica cada coisa

| Recurso | Rota | Serviço | Schema | Spec |
| --- | --- | --- | --- | --- |
| Login, logout, sessão, perfil | `routes/auth.py`, `routes/sessao.py` | `services/acesso.py` | `schemas/acesso.py` | 01 |
| Usuários | `routes/usuarios.py` | `services/usuario.py` | `schemas/acesso.py` | 01 |
| Demandas, painel, minhas | `routes/demandas.py` | `services/demanda.py` | `schemas/demanda.py` | 02 |
| Assistidos e ficha | `routes/assistidos.py` | `services/assistido.py` | `schemas/assistido.py` | 03 |
| Reuniões | `routes/reunioes.py` | `services/reuniao.py` | `schemas/reuniao.py` | 04 |
| Auditoria | `routes/auditoria.py` | `services/auditoria.py` | `schemas/auditoria.py` | 05 |
| Evoluções | `routes/evolucoes.py` | `services/evolucao.py` | `schemas/evolucao.py` | 06 |
| Encaminhamentos | `routes/encaminhamentos.py` | `services/encaminhamento.py` | `schemas/encaminhamento.py` | 07 |
| Relatórios | `routes/relatorios.py` | `services/relatorio.py` | `schemas/relatorio.py` | 08 |
| Aviso de prazo no login | `routes/auth.py` | `services/aviso.py` | — | 09 |

Erros: `app/errors.py` (formato `{"erro": "..."}`). Data e fuso do CRIE: `app/fuso.py`.

---

## Publicação

A Vercel serve a API pelo `api/index.py` da raiz, que chama `create_app()`. Dependência nova de produção entra **nos dois** arquivos: `backend/requirements.txt` e `requirements.txt` da raiz (a Vercel não aceita `-r`).

A publicação não roda migração. Depois de subir código com migração nova, rode `flask db upgrade` com o `DATABASE_URL` do banco publicado; sem a tabela `token_revogado`, toda rota com token responde 500.

---

## Problemas comuns

| Sintoma | Causa provável |
| --- | --- |
| `ModuleNotFoundError: psycopg2` | `DATABASE_URL` com driver errado; use a URL do provedor como veio, o `config.py` converte |
| `RuntimeError: Produção sem variável` | `FLASK_ENV=production` sem `SECRET_KEY`, `JWT_SECRET_KEY` ou `DATABASE_URL` |
| Front-end em outra porta bloqueado pelo navegador | origem fora de `CORS_ORIGINS` |
| 401 `Sessão encerrada` logo depois de entrar | conta desativada, ou token usado depois do logout |
| 429 no login | seis falhas em 60 s do mesmo IP e e-mail; espere um minuto |
