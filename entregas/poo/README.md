# Programação Orientada a Objetos: projeto semestral

**Profa. Ana Paula Müller Giancoli.**
- **Envio:** até 01/12/2026, 23:59.
- **Valor:** 9,0 (Parte I 7,5 + Parte II 1,5). A média é (ENADE + Prova + Seminário + Projeto + NETACAD1 + NETACAD2) / 4 + Pesquisa.
- **Fonte:** tarefa "Entrega PROJETO SEMESTRAL: Entrega em EQUIPES [01-12-2026]" (Moodle de POO).

## O que o enunciado pede

| Exigência | Situação | Onde |
|---|---|---|
| "aplicação python sob o paradigma da orientação a objetos" | ok | Classes de modelo, serviço, esquema e erro em `backend/app/`. O mapa dos conceitos (classe, objeto, encapsulamento, herança, polimorfismo) fica em `docs/poo-no-backend.md`, no PR de ajustes finais |
| "FLASK ou a FAST API" | ok | Flask 3, em `backend/app/__init__.py` |
| "integrado ao banco de dados SQLite3" | atenção | O back-end roda em SQLite3: os 587 testes usam SQLite, e o desenvolvimento local aceita `DATABASE_URL=sqlite:///crie_local.db`. A produção na Vercel usa PostgreSQL (Neon), porque a Vercel não guarda arquivo de banco entre execuções. **Confirmar com a professora se isso é aceito**; na apresentação, mostrar a API rodando com SQLite3 |
| "no mínimo 4 tabelas relacionais" | ok | 3 migrações em `backend/migrations/versions/`; o DER fica em `docs/modelagem/` |
| README.md "com as instruções de instalação e execução", "Indicar as bibliotecas", "Indicar as instruções de como utilizá-la" | parcial | `README.md` e `backend/README.md`. O PR de ajustes finais acrescenta "Como usar" e "Rodar com SQLite3" |
| "Publicar na plataforma Vercel.com" | ok | https://sistema-demandas-crie.vercel.app (a API fica em `/api`; saúde em `/api/saude`) |
| Código zipado da API | a gerar | Comando abaixo |
| Apresentação (1,5): até 20 min, todos apresentam, front + back + dados no banco, divisão de tarefas, trecho de código | a preparar | Precisa da primeira direção em produção (PR #19) ou da API local com SQLite3 e o `seed.py` |

## Gerar o .zip da API (a partir da raiz, no commit entregue)

```bash
git archive --format=zip -o entregas/poo/API_CRIE_Equipe_Cortex.zip HEAD backend api requirements.txt vercel.json README.md
```

## Pendências da equipe
- [ ] Perguntar à professora: a produção em PostgreSQL é aceita, mostrando o SQLite3 localmente?
- [ ] Ensaio: cada integrante explica uma classe do back-end usando `docs/poo-no-backend.md`.
- [ ] Gerar o .zip no commit final e enviar no Moodle.
