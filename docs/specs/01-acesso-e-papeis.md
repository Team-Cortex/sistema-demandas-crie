# Spec 01 — Acesso e papéis

**Status:** fechada para implementação no servidor.  
**Depende de:** tabela de usuário no modelo relacional (Henry) para persistir. O comportamento abaixo já vale.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

### POST `/api/auth/login`

Corpo: `{"email": "...", "senha": "..."}`.

Ordem das regras:

1. Corpo ausente ou campo vazio → 422, `{"erro": "Informe e-mail e senha."}`.
2. Conta as falhas recentes daquele par IP + e-mail. Na sexta falha em 60 segundos → 429, `{"erro": "E-mail ou senha inválidos."}`.
3. Busca o usuário pelo e-mail. Se não existir, compara a senha com um hash fixo de mentira, no mesmo custo do hash real.
4. Se a conta não existir, estiver inativa ou a senha não conferir → 401, `{"erro": "E-mail ou senha inválidos."}`. A conta inativa também passa pela comparação de senha, para responder no mesmo tempo.
5. Emite JWT com `sub` = id (em texto, exigência do PyJWT), `perfil` e expiração em 30 minutos. Resposta 200: `{"token": "...", "perfil": "direcao", "usuario": {"id": 1, "nome": "...", "perfil": "direcao"}, "avisos": {...}}`. O formato de `avisos` (demandas vencidas ou perto do prazo, sem dado de saúde) está na [spec 09](09-aviso-de-prazo.md). O e-mail que deu certo zera a contagem de falhas do par IP + e-mail.

A contagem de falhas fica na memória do processo do servidor: reiniciar zera, e com mais de um processo cada um conta o seu. Basta para um processo só; mais que isso depende do deploy.

### POST `/api/auth/logout`

Exige Bearer válido. Grava o `jti` do token na tabela `token_revogado` até a expiração original. Resposta 200: `{"ok": true}`. Uso posterior desse token → 401. Sem token → 401. Registros já expirados saem da tabela no logout seguinte.

### Sessão: 401

Toda rota protegida responde 401 no formato único:

| Situação | Mensagem |
| --- | --- |
| Sem `Authorization` | `Entre no sistema para continuar.` |
| Token malformado ou com assinatura errada | `Sessão inválida. Entre de novo.` |
| Token vencido (30 minutos) | `Sessão expirada. Entre de novo.` |
| Token de logout, ou conta desativada ou inexistente | `Sessão encerrada. Entre de novo.` |

O perfil e o `ativo` são lidos do banco a cada requisição, não do token. Mudar o perfil vale na requisição seguinte; desativar encerra a sessão na requisição seguinte.

### POST `/api/usuarios`

Só o perfil `direcao`. Corpo: `email`, `senha`, `nome`, `perfil`.

1. Outro perfil → 403, `{"erro": "Você não pode cadastrar usuários."}`.
2. Campo fora dos quatro → 422, `{"erro": "Campo não aceito: confira o formulário."}`. Nome vazio → 422, `{"erro": "Informe o nome."}`. E-mail sem formato de e-mail → 422, `{"erro": "Informe um e-mail válido."}`.
3. E-mail já usado por conta ativa ou inativa → 400, `{"erro": "Já existe um usuário com este e-mail."}`. A comparação ignora maiúsculas e espaços nas pontas.
4. Senha com menos de 8 caracteres → 422, `{"erro": "A senha precisa ter no mínimo 8 caracteres."}`.
5. `perfil` fora de `direcao`, `assistente_social`, `equipe_pedagogica` → 422, `{"erro": "Escolha um perfil válido."}`.
6. Grava o hash da senha. A senha em claro não volta em resposta nenhuma. Resposta 201: `id`, `nome`, `email`, `perfil`, `ativo`, `criado_em`.

### GET `/api/usuarios` e GET `/api/usuarios/<id>`

Qualquer conta ativa: o cliente precisa da lista para escolher responsável e participantes. Filtros opcionais: `ativo` (`true`/`false`) e `perfil`. Ordem por nome. Cada item: `id`, `nome`, `perfil`, `ativo`; o `email` só vem quando quem pede é a direção. Inexistente → 404, `{"erro": "Usuário inexistente."}`.

### PATCH `/api/usuarios/<id>` (PUT aceito, mesmo efeito)

Só `direcao`; outro perfil → 403, `{"erro": "Você não pode alterar usuários."}`. Pode alterar `nome`, `perfil` e `ativo`, um ou mais. Outro campo → 422. Não apaga a linha. `ativo: false` impede login novo e invalida a sessão no próximo uso do token. O card pediu `PUT`; a rota aceita os dois verbos com o comportamento de PATCH (só muda o que veio).

A direção não altera o próprio `perfil` nem o próprio `ativo` → 400, `{"erro": "Você não pode alterar o próprio perfil nem desativar a própria conta."}`. Assim sempre resta ao menos a direção que está operando.

### PATCH `/api/usuarios/<id>/desativar`

Só `direcao`. Marca `ativo: false` e devolve o usuário. Desativar quem já está inativo devolve 200 sem mudar nada. A própria conta → 400, mesma mensagem acima. Não existe `DELETE`.

Não há autocadastro. A primeira conta `direcao` é criada pelo comando administrativo do §3.1; a semente do §3 continua exclusiva de desenvolvimento.

---

## 2. Papéis

Herança prevista: `Usuario` → `Direcao` e `Profissional`; `Profissional` → `AssistenteSocial` e `EquipePedagogica`. Tabela única, coluna `perfil`.

`pode_ver_evolucao` existe em cada subclasse. Nesta versão, direção e profissional ativo retornam verdadeiro para qualquer assistido. A implementação restritiva (só quem acompanha aquele assistido) permanece no código, desligada, porque a direção do CRIE escolheu acesso aberto no relatório v2. A rota chama o método e não inspeciona o nome da classe.

As permissões só da direção seguem o mesmo desenho: `pode_gerir_usuarios`, `pode_emitir_relatorio` e `pode_consultar_auditoria` respondem verdadeiro na `Direcao` ativa e falso no `Profissional`. A rota declara a permissão com o decorador `exige_permissao("pode_gerir_usuarios", "mensagem do 403")` e não compara o texto do perfil.

Toda rota que não seja `POST /api/auth/login`, `GET /api/saude` e `GET /api/teste` (o Hello World de fumaça) exige token válido e conta ativa. A verificação fica no blueprint, antes de qualquer rota dele: rota nova já nasce protegida. Esconder botão no cliente não conta como permissão.

---

## 3. Semente

Quando o script de criação do Henry existir, o comando `python seed.py` (a partir de `backend/`) garante um usuário `direcao` fictício. Rodar de novo não duplica. Nome, e-mail e senha vêm do ambiente local, nunca de valor gravado no repositório. O comando recusa rodar se `FLASK_ENV=production`.

---

### 3.1 Primeira direção no banco publicado

Solicitado em 17/11/2026 para viabilizar o primeiro acesso na fase atual, ainda sem interface integrada. `flask criar-primeira-direcao --nome "..." --email "..."` cria **somente uma direção ativa** num banco sem usuários. Não carrega demonstração, não cria tabelas e não altera contas existentes. O `seed.py` continua recusando produção.

Regras, na ordem:

1. Sem banco configurado, recusa com mensagem legível.
2. Nome, e-mail e senha seguem a validação do cadastro HTTP. O perfil é sempre `direcao`; senha recebida em prompt oculto, com confirmação, nunca por argumento de linha de comando.
3. No PostgreSQL, bloqueia a tabela `usuario` na mesma transação da consulta e criação, impedindo dois primeiros cadastros simultâneos.
4. Qualquer usuário existente, mesmo profissional ou inativo, impede o comando. Repetir não muda senha, perfil ou ativação.
5. Reutiliza o cadastro do servidor e seu hash de senha. Confirma apenas o id criado; falha do banco desfaz a transação e não imprime SQL, credenciais ou detalhes de conexão.

Não existe endpoint de bootstrap nem senha padrão. As próximas contas são cadastradas pela direção em `POST /api/usuarios`.

A identidade da primeira direção no ambiente publicado permanece **aberta** até confirmação do responsável. Na validação isolada, usam-se somente nome fictício e e-mail `@exemplo.test`. A criação e a validação autenticada no ambiente de produção dependem da liberação operacional desse ambiente; o roteiro e as evidências ficam em `docs/validacao-primeiro-acesso.md`.

## 4. Testes que provam esta spec

- Login certo devolve token; login errado, e-mail inexistente e senha vazia devolvem a mesma mensagem.
- A sexta falha em 60 segundos devolve 429 com essa mesma mensagem.
- Rota de dado sem token devolve 401.
- Token expirado devolve 401 com `Sessão expirada. Entre de novo.`
- `assistente_social` em `POST /api/usuarios` devolve 403.
- Usuário inativo não recebe token.
- Logout impede reutilizar o token.
- Desativar não apaga a linha e derruba a sessão aberta do desativado.
- A direção não desativa a própria conta.
- O comando cria só uma direção, permite login e acesso protegido, e o logout invalida o token.
- O comando recusa qualquer usuário prévio, entrada inválida e falha do banco, sem revelar senha ou detalhes internos.

---

## 5. O que não entra

Autocadastro, MFA, OAuth, "esqueci a senha", convite por e-mail e troca de senha pelo próprio usuário.
