# POO no back-end

Onde estão os conceitos de Programação Orientada a Objetos no servidor Flask (`backend/`), com arquivo e linha, ligados às aulas de POO:

- **Aula 14:** classe, `__init__`, `self`, encapsulamento com `_` e `__`, herança, `super()` e polimorfismo.
- **Aula 15:** banco de dados com SQLite3.

O enunciado de POO pede uma aplicação Python orientada a objetos, com Flask, integrada ao SQLite3 e com pelo menos 4 tabelas. A seção 7 mostra como cada item é atendido. O lado do React está em [`front-orientacao-a-objetos.md`](front-orientacao-a-objetos.md); o resumo da arquitetura está em [`arquitetura.md`](arquitetura.md) §5.

Os caminhos abaixo partem de `backend/`. As linhas são as do código na data deste documento; se o arquivo mudar, procure pelo nome da classe ou do método.

---

## 1. Classes e objetos

Cada entidade do CRIE é uma **classe** em `app/models/`. Cada linha do banco vira um **objeto** dessa classe quando o SQLAlchemy a carrega.

| Classe | Arquivo e linha | Tabela |
| --- | --- | --- |
| `Usuario` e subclasses | `app/models/usuario.py` 19 | `usuario` |
| `Assistido`, `AssistidoProfissional` | `app/models/assistido.py` 29 e 14 | `assistido`, `assistido_profissional` |
| `Reuniao` | `app/models/reuniao.py` 25 | `reuniao`, `reuniao_participante` |
| `Demanda` | `app/models/demanda.py` 60 | `demanda` |
| `HistoricoDemanda` | `app/models/historico.py` 22 | `historico_demanda` |
| `Evolucao` | `app/models/evolucao.py` 18 | `evolucao` |
| `Encaminhamento` | `app/models/encaminhamento.py` 16 | `encaminhamento` |
| `RegistroAuditoria` | `app/models/auditoria.py` 20 | `auditoria` |
| `TokenRevogado` | `app/models/sessao.py` 11 | `token_revogado` |

**Objetos sendo criados e usados:**

- `app/services/usuario.py` 80 e 81: `classe = CLASSE_POR_PERFIL[dados["perfil"]]` escolhe a classe; `usuario = classe(nome=..., email=..., senha=...)` cria o objeto.
- `app/services/demanda.py` 36: `Demanda.abrir(autor, ...)` devolve um objeto `Demanda` já com o primeiro item de histórico; a linha 48 grava com `db.session.add(demanda)`.
- `app/services/demanda.py` 108: `demanda.mudar_estado(estado, autor)` chama um método do objeto carregado do banco.
- `app/extensions.py` 5: `db = SQLAlchemy()` também é um objeto, compartilhado pela aplicação inteira.

## 2. `__init__` e `self`

Vários models escrevem o próprio `__init__` para validar os dados antes de o objeto existir, e depois chamam o `__init__` da classe-mãe com `super()`:

- `app/models/usuario.py` 37 a 43: normaliza o e-mail, chama `super().__init__(**campos)` (linha 41) e, se veio senha, chama `self.definir_senha(senha)`.
- `app/models/demanda.py` 99 a 111: recusa descrição vazia e categoria acima de 80 caracteres; `super().__init__(**campos)` na linha 111.
- `app/models/evolucao.py` 129 a 142, `app/models/encaminhamento.py` 88 a 107, `app/models/assistido.py` 82 a 84 e `app/models/auditoria.py` 40 a 52: mesmo desenho.
- `app/services/acesso.py` 36 a 41: `LimiteDeTentativas.__init__(self, maximo=5, janela=60, ...)` guarda o estado do objeto em `self.maximo`, `self.janela`, `self._falhas`.

O `self` aparece em todo método de instância: `self.estado`, `self.historico.append(...)` (`app/models/demanda.py` 141 a 167).

## 3. Encapsulamento

O código usa o `_` da Aula 14 (convenção: "não mexa por fora"). O `__` (troca de nome do Python) **não** aparece no back-end; no front-end, o campo privado `#http` cumpre esse papel.

- **Senha (RNF02).** `app/models/usuario.py` 29: `_senha_hash` só é escrito por `definir_senha` (linha 45, que exige 8 caracteres e grava o hash) e só é lido por `senha_confere` (linha 50). Nenhuma rota devolve o hash.
- **Estado da demanda.** `app/models/demanda.py` 113 a 126: o `@validates("estado")` roda toda vez que alguém atribui `demanda.estado = ...` e recusa a transição inválida com `ErroDeNegocio`. Não dá para pular a regra da spec 02 mudando o atributo por fora.
- **Métodos internos.** `_registrar_estado` (`app/models/demanda.py` 153) só é chamado pelos métodos da própria classe (`abrir` e `mudar_estado`).
- **Estado interno de um serviço.** `app/services/acesso.py` 39 a 41 e 73 a 85: `_relogio`, `_falhas`, `_trava`, `_anotar` e `_esquecer_antigas` são internos do `LimiteDeTentativas`; por fora, só `bloqueado`, `reservar`, `registrar_falha` e `limpar`.
- **Propriedades.** `@property` expõe um valor calculado como se fosse atributo, sem deixar alterar: `Demanda.encerrada` e `Demanda.ultimo_movimento` (`app/models/demanda.py` 198 e 206), `Evolucao.vigente` (`app/models/evolucao.py` 55), `Encaminhamento.pendente` (`app/models/encaminhamento.py` 49).

## 4. Herança e `super()`

**Perfis de usuário** (`app/models/usuario.py`):

```
Usuario (abstrata, linha 19)
├── Direcao (linha 74)
└── Profissional (abstrata, linha 92)
    ├── AssistenteSocial (linha 121)
    └── EquipePedagogica (linha 125)
```

As subclasses herdam nome, e-mail, ativo, `definir_senha` e `senha_confere`. As linhas 32 a 35 ligam a herança ao banco: todos os perfis ficam na tabela `usuario`, e a coluna `perfil` diz qual classe o SQLAlchemy cria ao carregar a linha (herança de tabela única). `Usuario` e `Profissional` são abstratas (`"polymorphic_abstract": True`): nunca viram objeto sozinhas.

**Exceções do domínio** (`app/errors.py`): `ErroDeNegocio` (linha 20), `PermissaoNegada` (26), `NaoEncontrado` (32), `DadoInvalido` (38), `NaoAutenticado` (46) e `MuitasTentativas` (54) herdam de `Exception`. Cada uma guarda `self.mensagem` e chama `super().__init__(mensagem)` (linhas 23, 29, 35, 43, 51 e 59). `RegistroImutavel` (`app/models/imutavel.py` 17) herda de `ErroDeNegocio`. `SeedRecusado` (`seed.py` 23) herda de `RuntimeError`.

**Mixins e herança múltipla** (`app/models/imutavel.py`):

- `SemExclusao` (linha 21): a linha nunca é apagada. Usada por `Demanda(SemExclusao, db.Model)` e `Encaminhamento(SemExclusao, db.Model)`.
- `SomenteInsercao(SemExclusao)` (linha 28): nem apagada nem alterada. Usada por `HistoricoDemanda`, `Evolucao` e `RegistroAuditoria`.
- A classe herda ao mesmo tempo o comportamento do mixin e o mapeamento do `db.Model`. As enumerações também usam herança múltipla: `class EstadoDemanda(str, enum.Enum)` (`app/models/demanda.py` 25).

**Herança em outros pontos:**

- **Schemas** (`app/schemas/__init__.py`): `Entrada(Schema)` (linha 17) recusa campo desconhecido; `Filtro(Schema)` (26) ignora. `FiltroPeriodo(Filtro)` (49) acrescenta `de` e `ate`. `FiltroAuditoriaSchema(FiltroPeriodo, Paginacao)` (`app/schemas/auditoria.py` 9) junta período e paginação. `DemandaComHistoricoSchema(DemandaSchema)` (`app/schemas/demanda.py` 146) acrescenta o histórico.
- **Configuração** (`config.py`): `Config` (linha 31) tem o que é comum; `DevelopmentConfig`, `TestingConfig` e `ProductionConfig` (linhas 47, 54 e 69) herdam e mudam só o banco, as chaves e o CORS.

## 5. Polimorfismo

**O mesmo método, uma resposta por perfil.** `Usuario` declara `pode_ver_evolucao`, `pode_gerir_usuarios`, `pode_emitir_relatorio` e `pode_consultar_auditoria` sem implementar (`app/models/usuario.py` 55 a 68, `raise NotImplementedError`). `Direcao` (linhas 79 a 89) responde `True` a todos quando ativa. `Profissional` (linhas 104 a 118) responde `False` aos três da direção, e `pode_ver_evolucao` segue a regra do acesso aberto escolhida pela direção do CRIE.

**Quem chama não olha a classe:**

- `app/services/acesso.py` 25: `if not usuario.pode_ver_evolucao(assistido): raise PermissaoNegada(...)`.
- `app/routes/sessao.py` 104: `getattr(usuario_atual(), permissao)()`. O decorador `exige_permissao("pode_gerir_usuarios", ...)` (usado, por exemplo, em `app/routes/usuarios.py` 35) chama o método pelo nome e cada objeto responde do seu jeito.

Para acrescentar um perfil, basta uma subclasse nova com esses métodos; nenhuma rota muda.

**Outros exemplos:**

- O tratador de `ErroDeNegocio` (`app/errors.py` 95) também atende `RegistroImutavel`, porque ela é uma `ErroDeNegocio`.
- `app/models/imutavel.py` 50 a 57: antes de gravar, `isinstance(objeto, SemExclusao)` e `isinstance(objeto, SomenteInsercao)` decidem o que recusar. A mensagem usa `objeto.nome_registro`, que cada classe define ("A demanda", "A evolução"...).
- `__repr__` é sobrescrito em cada model (por exemplo, `app/models/evolucao.py` 144, que de propósito não mostra a descrição, por ser dado sensível).

## 6. Métodos de classe e métodos estáticos

- **`@classmethod`:** um método que recebe a classe (`cls`) e cria ou busca objetos. `Demanda.abrir` (`app/models/demanda.py` 134), `Evolucao.lancar` e `Evolucao.do_assistido` (`app/models/evolucao.py` 118 e 59), `Encaminhamento.pendentes` (`app/models/encaminhamento.py` 53), `TokenRevogado.revogado` (`app/models/sessao.py` 17).
- **`@staticmethod`:** os serviços (`DemandaService` em `app/services/demanda.py` 19, `UsuarioService`, `AcessoService` e os demais) agrupam as operações de cada recurso em métodos estáticos. Eles não guardam estado; a classe serve para organizar. A exceção é o `LimiteDeTentativas`, que é um objeto de verdade, com estado: um por aplicação, criado em `app/services/acesso.py` 92.

## 7. Banco de dados (Aula 15) e o enunciado de POO

| Exigência | Como o projeto atende |
| --- | --- |
| Python orientado a objetos | seções 1 a 6 |
| Flask | `app/__init__.py` 29: `create_app` monta a aplicação; uma rota por recurso em `app/routes/` |
| SQLite3 | com `DATABASE_URL=sqlite:///crie_local.db`, o SQLAlchemy usa o módulo `sqlite3` do Python por baixo. As migrações criam as tabelas e as travas também em SQLite (`migrations/versions/`, com ramos para `sqlite` e `postgresql`). Passo a passo no [`README.md`](../README.md), seção "Rodar com SQLite3" |
| Mínimo de 4 tabelas | 11 tabelas: `usuario`, `assistido`, `assistido_profissional`, `reuniao`, `reuniao_participante`, `demanda`, `historico_demanda`, `evolucao`, `encaminhamento`, `token_revogado`, `auditoria` (a lista está em `tests/test_migracoes.py` 13 a 25) |

**Onde o `sqlite3` da Aula 15 aparece direto:** `tests/test_migracoes.py` abre o arquivo do banco com `sqlite3.connect(caminho)` e roda SQL com `execute`: lista as tabelas em `sqlite_master` (linhas 60 a 62) e prova que a trava recusa `DELETE` e `UPDATE` no histórico mesmo por SQL escrito à mão (linhas 103 a 128).

**Do objeto para a tabela.** A aplicação não escreve SQL: cada classe do model é uma tabela, cada atributo `db.Column` é uma coluna e cada objeto é uma linha. `db.session.add(objeto)` e `db.session.commit()` fazem o `INSERT` e o `COMMIT` que, na Aula 15, eram escritos com `cursor.execute(...)` e `conexao.commit()`.

**Produção.** O sistema publicado na Vercel usa PostgreSQL (Neon). O mesmo código roda nos dois bancos porque o endereço vem de `DATABASE_URL` (`config.py` 17 a 28). A suíte de testes roda em SQLite em memória (`config.py` 60).
