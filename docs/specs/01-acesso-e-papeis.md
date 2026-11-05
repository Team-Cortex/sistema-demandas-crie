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
4. Se a conta não existir, estiver inativa ou a senha não conferir → 401, `{"erro": "E-mail ou senha inválidos."}`.
5. Emite JWT com `sub` = id, `perfil` e expiração em 30 minutos. Resposta 200: `{"token": "...", "perfil": "direcao"}`.

### POST `/api/auth/logout`

Exige Bearer válido. Grava o `jti` do token até a expiração original. Uso posterior desse token → 401. Sem token → 401.

### POST `/api/usuarios`

Só o perfil `direcao`. Corpo: `email`, `senha`, `nome`, `perfil`.

1. Outro perfil → 403, `{"erro": "Você não pode cadastrar usuários."}`.
2. E-mail já usado por conta ativa ou inativa → 400, `{"erro": "Já existe um usuário com este e-mail."}`.
3. Senha com menos de 8 caracteres → 422, `{"erro": "A senha precisa ter no mínimo 8 caracteres."}`.
4. `perfil` fora de `direcao`, `assistente_social`, `equipe_pedagogica` → 422.
5. Grava o hash da senha. A senha em claro não volta em resposta nenhuma.

### PATCH `/api/usuarios/<id>`

Só `direcao`. Pode alterar `nome`, `perfil` e `ativo`. Não apaga a linha. `ativo: false` impede login novo e invalida a sessão no próximo uso do token.

Não há autocadastro. Quem cria a primeira conta `direcao` é o comando de semente, abaixo.

---

## 2. Papéis

Herança prevista: `Usuario` → `Direcao` e `Profissional`; `Profissional` → `AssistenteSocial` e `EquipePedagogica`. Tabela única, coluna `perfil`.

`pode_ver_evolucao` existe em cada subclasse. Nesta versão, direção e profissional ativo retornam verdadeiro para qualquer assistido. A implementação restritiva (só quem acompanha aquele assistido) permanece no código, desligada, porque a direção do CRIE escolheu acesso aberto no relatório v2. A rota chama o método e não inspeciona o nome da classe.

Toda rota que não seja `POST /api/auth/login` e `GET /api/saude` exige token válido e conta ativa. Esconder botão no cliente não conta como permissão.

---

## 3. Semente

Quando o script de criação do Henry existir, o comando `python seed.py` (a partir de `backend/`) garante um usuário `direcao` fictício. Rodar de novo não duplica. Nome, e-mail e senha vêm do ambiente local, nunca de valor gravado no repositório. O comando recusa rodar se `FLASK_ENV=production`.

---

## 4. Testes que provam esta spec

- Login certo devolve token; login errado, e-mail inexistente e senha vazia devolvem a mesma mensagem.
- A sexta falha em 60 segundos devolve 429 com essa mesma mensagem.
- Rota de dado sem token devolve 401.
- `assistente_social` em `POST /api/usuarios` devolve 403.
- Usuário inativo não recebe token.
- Logout impede reutilizar o token.

---

## 5. O que não entra

Autocadastro, MFA, OAuth, "esqueci a senha", convite por e-mail e troca de senha pelo próprio usuário.
