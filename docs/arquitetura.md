# Arquitetura do Sistema

Sistema de Gestão de Demandas — CRIE / APAE de Extrema
Projeto de extensão BRAEXT2 · ADS · IFSP Câmpus Bragança Paulista

---

## 1. Visão geral

O sistema segue arquitetura **cliente-servidor com API REST**: uma aplicação React no navegador consome uma API em Flask, que persiste os dados em PostgreSQL.

```
┌──────────────────┐        HTTP/JSON        ┌──────────────────┐        SQL        ┌──────────────┐
│                  │  ────────────────────▶  │                  │  ──────────────▶  │              │
│  React (Vite)    │                         │  Flask (API)     │                   │  PostgreSQL  │
│  navegador       │  ◀────────────────────  │  Python          │  ◀──────────────  │              │
└──────────────────┘      Bearer token       └──────────────────┘                   └──────────────┘
     BRADWFR                                       BRAPROB                              BRABCD1
```

As três camadas correspondem às disciplinas do módulo, o que torna a separação não apenas técnica mas também organizacional: cada frente é dona de uma camada e das suas interfaces com as vizinhas.

**Por que essa arquitetura.** A separação entre front-end e back-end permite que Vinícius e Miguel trabalhem em paralelo a partir do contrato da API, sem que um bloqueie o outro. É também o modelo mais comum no mercado, o que dá ao projeto valor além da disciplina.

---

## 2. Estrutura de diretórios

```
sistema-demandas-crie/
├── README.md                    visão geral e instruções de execução
├── LICENSE                      MIT
├── .gitignore
├── docker-compose.yml           PostgreSQL local
│
├── docs/                        documentação do projeto
│   ├── plano-de-projeto.md      escopo, cronograma, atribuições
│   ├── requisitos.md            requisitos funcionais e não funcionais
│   ├── divisao-de-papeis.md     detalhamento por integrante
│   ├── arquitetura.md           este documento
│   ├── contrato-api.md          endpoints, formatos, códigos de erro
│   └── modelagem/               DER, modelo relacional, scripts SQL
│
├── backend/                     API — BRAPROB
│   ├── .env.example
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── run.py                   ponto de entrada
│   ├── config.py                configuração por ambiente
│   ├── seed.py                  carga inicial com dados fictícios
│   ├── app/
│   │   ├── __init__.py          factory create_app()
│   │   ├── extensions.py        instâncias de db, jwt, cors, migrate
│   │   ├── models/              entidades de domínio
│   │   ├── services/            regras de negócio
│   │   ├── routes/              endpoints HTTP
│   │   └── schemas/             validação e serialização
│   └── tests/
│
└── frontend/                    interface — BRADWFR
    ├── .env.example
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx             ponto de entrada
        ├── App.jsx              rotas
        ├── api/                 cliente HTTP
        ├── components/          componentes reutilizáveis
        ├── pages/               telas
        └── styles/              estilos globais
```

**Monorepo, e não dois repositórios.** Para uma equipe de cinco pessoas em um semestre, dois repositórios criariam problemas de sincronização de versão sem trazer benefício. Front e back evoluem juntos e são entregues juntos.

---

## 3. Camadas do back-end

O back-end tem quatro camadas, e a ordem em que uma requisição as atravessa é sempre a mesma:

```
requisição HTTP
      │
      ▼
┌─────────────┐   valida o formato de entrada e serializa a saída
│  schemas/   │   (marshmallow)
└─────────────┘
      │
      ▼
┌─────────────┐   traduz HTTP em chamadas de domínio: lê parâmetros,
│  routes/    │   verifica autenticação, devolve status e JSON
└─────────────┘
      │
      ▼
┌─────────────┐   regras de negócio: o que pode acontecer, em que ordem,
│  services/  │   sob quais condições
└─────────────┘
      │
      ▼
┌─────────────┐   entidades, relacionamentos e persistência
│  models/    │   (SQLAlchemy)
└─────────────┘
      │
      ▼
  PostgreSQL
```

### Por que a camada de serviços existe

É a decisão de arquitetura mais importante do back-end. Sem ela, a lógica de negócio acaba dentro das funções de rota, e o resultado é um conjunto de scripts com decorador em cima — não um sistema orientado a objetos.

Comparando:

```python
# Sem camada de serviço: regra misturada com HTTP.
@bp.patch("/<int:id>/estado")
def mudar_estado(id):
    demanda = Demanda.query.get_or_404(id)
    novo = request.json["estado"]
    if demanda.estado == "concluida" and novo == "aberta":
        return jsonify({"erro": "..."}), 400
    demanda.estado = novo
    db.session.commit()
    return jsonify(...)

# Com camada de serviço: a rota só traduz HTTP.
@bp.patch("/<int:id>/estado")
def mudar_estado(id):
    demanda = Demanda.query.get_or_404(id)
    dados = MudancaEstadoSchema().load(request.get_json())
    DemandaService.alterar_estado(demanda, dados["estado"], usuario_atual())
    return jsonify(demanda_schema.dump(demanda))
```

A segunda versão permite testar a regra sem subir servidor HTTP — é exatamente isso que `tests/test_demanda_service.py` faz.

---

## 4. Modelo de domínio

```
                    ┌───────────┐
                    │  Usuario  │  (abstrata na prática)
                    └─────┬─────┘
                          │ herança
          ┌───────────────┼────────────────┐
          ▼               ▼                │
    ┌──────────┐   ┌──────────────┐        │
    │ Direcao  │   │ Profissional │        │
    └──────────┘   └──────┬───────┘        │
                          │                │
              ┌───────────┴──────────┐     │
              ▼                      ▼     │
    ┌───────────────────┐  ┌─────────────────────┐
    │ AssistenteSocial  │  │  EquipePedagogica   │
    └───────────────────┘  └─────────────────────┘
```

```
  Reuniao ──────< Demanda >────── Assistido
                    │  │              │
                    │  │              ├──< Evolucao
                    │  └──────────────┼──< Encaminhamento
                    │                 │
                    └──< HistoricoDemanda
```

| Entidade | Papel |
| --- | --- |
| `Usuario` e subclasses | Quem acessa o sistema. O perfil determina as permissões. |
| `Assistido` | Pessoa atendida. Identificação mínima (RNF08). |
| `Reuniao` | Encontro semanal onde as demandas nascem. |
| `Demanda` | Núcleo do sistema: o que precisa ser feito, por quem, até quando. |
| `HistoricoDemanda` | Registro imutável de cada mudança e anotação (RF14, RF17). |
| `Evolucao` | Acompanhamento do assistido. Dado sensível, acesso restrito. |
| `Encaminhamento` | Direcionamento a outro serviço, com desfecho. |

Duas tabelas associativas resolvem os relacionamentos muitos-para-muitos: `assistido_profissional` (quem acompanha quem) e `reuniao_participante` (quem esteve na reunião).

### Herança no banco

A hierarquia de usuários usa **herança de tabela única**: todos os perfis compartilham a tabela `usuario`, e a coluna `tipo` identifica a subclasse. O SQLAlchemy instancia a classe correta automaticamente ao carregar o registro.

A alternativa seria uma tabela por subclasse, mais normalizada porém com junções em toda consulta. Como os perfis não têm atributos próprios — apenas comportamento diferente — a tabela única é a escolha adequada aqui.

---

## 5. Como os conceitos de POO aparecem

A disciplina de Programação Orientada a Objetos cobra encapsulamento, herança e polimorfismo. Eles não foram adicionados para cumprir a ementa; resolvem problemas concretos do sistema.

**Encapsulamento — `models/usuario.py`**

A senha nunca é acessível diretamente. O atributo `_senha_hash` só é manipulado por `definir_senha`, que valida o tamanho mínimo e aplica o hash, e por `senha_confere`, que compara sem expor o valor armazenado. Isso é o que garante o RNF02.

**Herança — `models/usuario.py`**

Cada perfil estende `Usuario` e herda identificação, autenticação e estado de ativação. `AssistenteSocial` e `EquipePedagogica` estendem `Profissional`, que concentra o que é comum a quem atende assistidos.

**Polimorfismo — `models/usuario.py` e `routes/assistidos.py`**

O método `pode_ver_evolucao` tem implementação distinta em cada perfil: a direção sempre pode; o profissional só pode se acompanhar aquele assistido. A rota que protege o acesso não sabe nem precisa saber com qual perfil está lidando:

```python
if not usuario.pode_ver_evolucao(assistido):
    raise PermissaoNegada("Você não tem acesso às evoluções deste assistido.")
```

Acrescentar um perfil novo no futuro não exige alterar nenhuma rota — apenas criar a subclasse e sobrescrever o método. É a vantagem prática do polimorfismo, e vale explicá-la assim na apresentação.

---

## 6. Autenticação e autorização

O fluxo usa **JWT** (JSON Web Token):

1. O usuário envia e-mail e senha em `POST /api/auth/login`
2. A API valida e devolve um token assinado, com validade de 30 minutos
3. O front guarda o token em `sessionStorage` e o envia no cabeçalho `Authorization` de cada requisição
4. Rotas protegidas com `@jwt_required()` recusam requisições sem token válido

**Por que `sessionStorage` e não `localStorage`:** o token é descartado quando a aba fecha. Como o sistema roda em computadores compartilhados dentro da instituição, isso reduz o risco de a sessão de um profissional continuar aberta para o próximo que sentar na máquina. Combina com o RNF05, que exige encerramento de sessões inativas.

**Autenticação é diferente de autorização.** O token responde "quem é você"; os métodos polimórficos de `Usuario` respondem "o que você pode ver". As duas verificações são independentes e ambas necessárias.

---

## 7. Front-end

```
main.jsx  →  App.jsx (rotas)  →  pages/  →  components/
                                    │
                                    ▼
                                 api/cliente.js  →  API
```

**Todo acesso à API passa por `api/cliente.js`.** Nenhuma tela chama `fetch` diretamente. Isso concentra num único arquivo o endereço base, o envio do token, o tratamento de erro e a reação à sessão expirada — se o contrato mudar, muda-se um arquivo.

**`pages/` e `components/`:** páginas correspondem a rotas e buscam dados; componentes são reutilizáveis e recebem tudo por props. Um componente que busca dados sozinho deixa de ser reutilizável.

Os estilos atuais são mínimos e provisórios. O visual definitivo virá do protótipo em Figma produzido na disciplina de IHC.

---

## 8. Tratamento de erros

Erros de domínio são exceções, capturadas por handlers registrados na factory:

| Exceção | HTTP | Quando |
| --- | --- | --- |
| `ErroDeNegocio` | 400 | Regra violada: transição de estado inválida, descrição vazia |
| `PermissaoNegada` | 403 | Perfil sem acesso ao recurso |
| `ValidationError` | 422 | Campos ausentes ou mal formatados |
| — | 401 | Token ausente, inválido ou expirado |
| — | 404 | Recurso inexistente |

Toda resposta de erro tem o mesmo formato: `{"erro": "mensagem legível"}`. As mensagens são escritas para quem usa o sistema, não para quem o desenvolve — a de login não revela se o e-mail existe, o que evita descobrir usuários por tentativa.

---

## 9. Decisões de arquitetura e seus motivos

| Decisão | Motivo | Alternativa descartada |
| --- | --- | --- |
| Monorepo | Front e back evoluem e são entregues juntos; equipe pequena | Dois repositórios |
| Camada de serviços separada | Mantém o domínio testável e o código orientado a objetos | Lógica dentro das rotas |
| Herança de tabela única | Perfis diferem em comportamento, não em atributos | Uma tabela por subclasse |
| JWT com expiração curta | Computadores compartilhados na instituição | Sessão em cookie sem expiração |
| PostgreSQL | Exigência de banco relacional; hospedagem gratuita disponível; valor de mercado | SQLite, mais simples porém menos representativo |
| Estados como enumeração | Impede estado inválido no banco | Campo de texto livre |
| Histórico imutável | RF17 e RNF19: nada é apagado, apenas acrescentado | Sobrescrever o registro |
| Migrações com Alembic | Alterações de schema propagadas sem recriar o banco | `db.create_all()` a cada mudança |

---

## 10. Restrições que a arquitetura precisa respeitar

Estas não são preferências, e sim requisitos formais do projeto:

- **Dados fictícios apenas.** Em desenvolvimento, testes, protótipos e na apresentação da EXPOEX. Nenhum dado real do CRIE em repositório ou ambiente de desenvolvimento (RNF06, RNF07).
- **Senhas com hash.** Nunca em texto legível (RNF02).
- **Auditoria.** Criação, alteração e emissão de relatório envolvendo dados de assistidos registram autor, data e hora (RNF03).
- **Sem exclusão definitiva.** Demandas, evoluções e encaminhamentos são cancelados ou substituídos, nunca apagados (RNF19).
- **HTTPS em produção** (RNF04).
- **Tolerância a falha de conexão.** A internet da instituição é intermitente; o formulário preserva o que foi preenchido quando a requisição falha (RNF16).

---

## 11. O que ainda pode mudar

A arquitetura acompanha as questões em aberto com a instituição:

| Questão | Impacto na arquitetura |
| --- | --- |
| QA01 — quem enxerga o quê | Altera `Profissional.pode_ver_evolucao`. Hoje está na alternativa mais restritiva. |
| QA02 — o que é "evolução" | Se for o andamento da demanda, o modelo `Evolucao` deixa de existir e o `HistoricoDemanda` absorve a função. |
| QA04 — formato dos relatórios | Pode exigir uma camada de geração de documento. |
| QA07 — campos do assistido | Altera o modelo `Assistido`. |

Enquanto essas respostas não chegam, o que está implementado é hipótese fundamentada, não decisão fechada.
