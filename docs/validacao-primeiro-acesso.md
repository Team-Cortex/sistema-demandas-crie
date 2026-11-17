# Primeiro acesso da direção — 17/11/2026

## Escopo e fase

O back-end tem as rotas de domínio, mas o React ainda só tem as páginas iniciais. A validação desta entrega é pela CLI administrativa e pela API Flask, com dados fictícios em banco isolado. Não equivale à aceitação da interface nem ao início do uso com dados reais.

Contrato: [spec 01 §3.1](specs/01-acesso-e-papeis.md). Se algo aqui conflitar com o código atual, este arquivo vence e o código muda.

O comando `flask criar-primeira-direcao --nome "..." --email "..."` cria apenas a primeira direção ativa. Reusa validação e hash existentes, recusa qualquer usuário prévio e não carrega o seed. No PostgreSQL, mantém um bloqueio da tabela de usuários na transação para impedir dois primeiros cadastros simultâneos. Não precisa de migração ou deploy da API para executar a ferramenta administrativa a partir deste código.

## Decisões e pré-requisitos publicados

| Item | Estado |
| --- | --- |
| Criar o primeiro acesso | solicitado pelo responsável nesta entrega |
| Identidade da primeira direção publicada | aberta; exemplo fictício não é identidade de produção aprovada |
| Acesso administrativo à Vercel/Neon nesta máquina | indisponível: a CLI 65.17.0 informou `No existing credentials found` na consulta ao projeto vinculado |
| Liberação para alterar o banco de produção | pendente da regra de operação §2 da metodologia, que exige a mensagem isolada `EU AUTORIZO` |
| Configuração da aplicação publicada | consultar depois da autenticação; não alterada por esta entrega |

Projeto vinculado em `.vercel/project.json`: `sistema-demandas-crie`, organização `team_WwZFnyRlgNhjvoccnjPpGEY0`, projeto `prj_7cDNgD9LclvhAfSm46BVFVsoswlv`. A CLI não foi autenticada automaticamente e a tentativa de fluxo de login foi encerrada.

O PR #13 informa banco Neon em `3f00c11df825` e nenhum usuário. Isso é registro anterior, não uma leitura atual do banco. Confirmar novamente antes do cadastro.

## Validação reproduzível

Na raiz do repositório, com as dependências do servidor instaladas:

```powershell
.\backend\.venv\Scripts\python.exe -m pytest backend/tests/test_cli.py -q
.\backend\.venv\Scripts\python.exe -m pytest backend/tests -q
node backend/scripts/check-segredo.mjs
```

Os testes criam e descartam SQLite em memória. A senha desses testes é exclusivamente fictícia e não deve ser usada no ambiente publicado.

| Passo do teste integrado | Resultado esperado |
| --- | --- |
| CLI em banco vazio | uma direção ativa, senha em hash, nenhuma carga de domínio |
| Consulta de usuários sem token | 401 |
| Login da direção | 200, perfil `direcao` e token |
| Usuários e painel com token | 200; uma conta e painel vazio |
| Criar reunião e demanda fictícias | 201; demanda nasce `aberta` |
| Alterar para `em_andamento` e `concluida` | 200; três estados preservados no histórico com autor |
| Painel após concluir | 200, sem demanda pendente |
| Logout e reutilização do token | logout 200; consulta seguinte 401 |

As recusas cobrem contas prévias de todos os perfis, ativas e inativas; repetição sem troca de senha; nome/e-mail/senha inválidos; confirmação de senha divergente ou cancelada; falta de banco e falha SQL com rollback e sem revelar detalhes internos.

## Evidências desta execução

- Testes novos do comando e do fluxo integrado: **17 aprovados**.
- Testes existentes de acesso, modelo de usuário, seed e saúde: **72 aprovados**.
- Suíte completa: **587 aprovados em 100,13 s**, com 39 avisos em modelos e migrações existentes, fora dos arquivos desta mudança.
- Verificação de segredo: aprovada; nenhum segredo acrescentado.
- Revisão independente da implementação: sem achados acionáveis.
- Consultas HTTPS ao endereço publicado `https://sistema-demandas-crie.vercel.app`: `/` respondeu **200**, `/api/saude` respondeu **200** com `{"ok":true,"status":"ok"}` e `/api/usuarios` sem token respondeu **401** com `Entre no sistema para continuar.`.

## Próxima validação no ambiente publicado

1. Autenticar deliberadamente a CLI da Vercel e confirmar o projeto vinculado com `vercel project inspect --non-interactive`.
2. Confirmar a identidade da direção, a liberação operacional e o ambiente exato. Conferir `FLASK_ENV=production`, presença das chaves e migrações sem imprimir valores sensíveis.
3. Usar acesso administrativo ao banco e injeção temporária de variáveis no processo, sem salvar segredos no repositório. Executar apenas o comando da primeira direção, sem `seed.py`.
4. Guardar a senha no gerenciador de senhas do responsável; não registrá-la em saída de ferramenta, histórico, issue, PR ou neste relatório.
5. Pela URL publicada, validar login → usuários/painel → logout → token recusado. Não criar assistidos, reuniões ou demandas de teste em produção: esses registros mantêm histórico e não admitem exclusão pela API.

## Limites

Não houve criação de conta nem login autenticado no banco publicado nesta execução. A suíte SQLite não prova a exclusão mútua do bloqueio PostgreSQL nem as variáveis do ambiente publicado. A interface ainda não oferece o fluxo autenticado.
