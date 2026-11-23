# sistema-demandas-crie

Sistema web para registro e acompanhamento das demandas levantadas nas reuniões de equipe do **CRIE — Centro de Integração Especial / APAE de Extrema**.

Projeto de extensão curricularizada do curso de Tecnologia em Análise e Desenvolvimento de Sistemas do **IFSP — Câmpus Bragança Paulista**, disciplina Extensão como Metodologia de Ensino 2 (BRAEXT2), sob orientação do Prof. Luiz Gustavo Diniz de Oliveira Véras.

**Sistema publicado:** [https://sistema-demandas-crie.vercel.app](https://sistema-demandas-crie.vercel.app) (interface React e API Flask no mesmo endereço; a API responde em `/api`).

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
| Front-end | React (Vite), JavaScript |
| Back-end | Python + Flask (orientado a objetos) |
| Banco de dados | PostgreSQL em produção (Neon); SQLite3 para rodar localmente sem Docker e nos testes |
| Comunicação | API REST com JSON |
| Migrações | Alembic (Flask-Migrate) |

---

## Estrutura do repositório

```
sistema-demandas-crie/
├── docs/                 documentação compartilhada
├── backend/              servidor Flask
├── frontend/             cliente React
├── api/index.py          entrada da API na Vercel
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
| [`docs/contrato-api.md`](docs/contrato-api.md) | Contrato HTTP entre o React e o Flask |
| [`docs/specs/`](docs/specs/) | Comportamento do servidor, na ordem de implementação |
| [`docs/estado-do-projeto.md`](docs/estado-do-projeto.md) | Mapa geral do que o sistema é hoje |
| [`docs/poo-no-backend.md`](docs/poo-no-backend.md) | POO: onde estão classe, objeto, encapsulamento, herança, polimorfismo e o banco no servidor |
| [`docs/front-orientacao-a-objetos.md`](docs/front-orientacao-a-objetos.md) | Front End: as classes `ClienteApi` e `Demanda` no React |
| [`docs/ihc/`](docs/ihc/) | IHC: personas, cenários de uso, arquitetura da informação, fluxos, telas, protótipo clicável, plano de testes e relatório de usabilidade |
| [`docs/modelagem/bd1/`](docs/modelagem/bd1/) | Banco de Dados 1: documento ABNT, DER, slides e guia do seminário; scripts SQL em [`docs/modelagem/sql/`](docs/modelagem/sql/) |
| [`docs/relatorios/`](docs/relatorios/) | Relatórios de projeto de Extensão (v1 a v3) |
| [`docs/CREDITOS-UI.md`](docs/CREDITOS-UI.md) | Origem e licença do logotipo e da fonte da interface |
| [`entregas/`](entregas/) | Exigências oficiais e checklist de entrega por disciplina (pasta trazida pelo PR #20; o link funciona depois do merge dele) |

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

O servidor é o Flask em `backend/`. O cliente é o React em `frontend/`. Detalhe do servidor em [`backend/README.md`](backend/README.md).

Pré-requisitos: Python 3.12, Node.js 22.13 ou superior (LTS) e Git. O Docker só é necessário para o PostgreSQL local; sem ele, use o SQLite3 (seção seguinte).

### Servidor com PostgreSQL (Docker)

```bash
# Subir o banco de dados
docker compose up -d

# Servidor
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env        # preencher os valores (ver backend/README.md)
flask db upgrade            # cria as tabelas
python seed.py              # opcional: dados fictícios de demonstração
flask run                   # http://127.0.0.1:5000
```

### Rodar com SQLite3

A disciplina de Programação Orientada a Objetos pede a aplicação integrada ao **SQLite3**. O mesmo código roda em SQLite3 e em PostgreSQL: o banco é escolhido pela variável `DATABASE_URL`. O sistema publicado usa PostgreSQL (Neon); a suíte de testes do servidor usa SQLite3 em memória.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env        # Windows (PowerShell): Copy-Item .env.example .env
```

No `.env`, troque a linha do banco e escolha as senhas da carga fictícia (pelo menos 8 caracteres):

```
DATABASE_URL=sqlite:///crie_local.db
SEED_DIRECAO_SENHA=<uma senha sua>
SEED_SENHA_PADRAO=<outra senha sua>
```

```bash
flask db upgrade            # cria as 11 tabelas no arquivo SQLite
python seed.py              # dados fictícios de demonstração
flask run                   # http://127.0.0.1:5000
```

O Flask-SQLAlchemy guarda o arquivo `crie_local.db` na pasta `backend/instance/`, que o Git ignora. Para conferir as tabelas, abra o arquivo com o módulo `sqlite3` do Python ou com o DB Browser for SQLite. Para recomeçar do zero, apague o arquivo e rode `flask db upgrade` e `python seed.py` de novo.

### Front-end

Com a API local em execução, abra outro terminal na raiz do repositório e instale as versões registradas no lockfile.

```bash
cd frontend
npm ci
npm run dev                 # http://localhost:5173
```

Em desenvolvimento, `frontend/.env.development` define `VITE_API_URL=http://localhost:5000`. A variável contém apenas a origem pública da API; a API deve permitir a origem do front em `CORS_ORIGINS` (o padrão de desenvolvimento já permite `http://localhost:5173`). No build de produção a variável fica vazia e o front usa a mesma origem da interface. As rotas da API já incluem `/api`.

Para verificar o cliente, execute dentro de `frontend/`:

```bash
npm run lint
node --test
npm run build
```

Os testes do servidor rodam com `pytest` dentro de `backend/` (detalhes em [`backend/README.md`](backend/README.md)).

---

## Como usar

### Contas fictícias para uso local

Depois de `python seed.py`, entre em http://localhost:5173 com uma destas contas. As senhas são as que você escolheu no `.env`:

| Perfil | Nome fictício | E-mail | Senha |
| --- | --- | --- | --- |
| Direção | Direção Fictícia | `direcao@exemplo.test` (o `SEED_DIRECAO_EMAIL` do `.env`) | `SEED_DIRECAO_SENHA` |
| Assistente social | Bruna Fictícia | `assistente.social@exemplo.test` | `SEED_SENHA_PADRAO` |
| Equipe pedagógica | Carlos Fictício | `pedagogico@exemplo.test` | `SEED_SENHA_PADRAO` |

A carga traz dois assistidos, uma reunião por setor, demandas em todos os estados (duas já vencidas), evoluções e encaminhamentos, todos fictícios. No sistema publicado não há contas de demonstração: as contas são cadastradas pela direção.

### O que cada perfil faz

| Perfil | Pode |
| --- | --- |
| Direção | tudo o que os outros perfis fazem, mais cadastrar, editar e desativar usuários, emitir relatórios e consultar a auditoria |
| Assistente social | registrar e atualizar demandas, reuniões, assistidos, evoluções e encaminhamentos |
| Equipe pedagógica | o mesmo que a assistente social |

Os itens **Usuários**, **Relatórios** e **Auditoria** só aparecem no menu da direção. Nenhum registro é excluído: uma demanda que não vai adiante muda para **Cancelada**, e uma evolução corrigida é **retificada**, com a versão anterior guardada.

### Principais fluxos

1. **Entrar.** Informe e-mail e senha. Se você tiver demandas vencidas ou perto do prazo, o **Painel** mostra o aviso logo no topo, com o link de cada uma.
2. **Acompanhar.** O **Painel** mostra os totais e as demandas em aberto por estado (Aberta, Em andamento, Aguardando terceiros), com "(vencida)" escrito ao lado do prazo. **Minhas demandas** lista só as suas, do prazo mais antigo para o mais novo.
3. **Registrar uma reunião.** Em **Reuniões**, escolha a data, o setor e os participantes. Na ficha da reunião, **Registrar demanda desta reunião** já abre o formulário com ela escolhida.
4. **Registrar uma demanda.** **Registrar demanda** abre um único formulário (descrição, prioridade, prazo, responsável, reunião de origem e, se quiser, assistido e categoria). Confira o resumo e confirme.
5. **Atualizar uma demanda.** Na ficha, escolha **Mudar estado** (só aparecem as mudanças permitidas, com confirmação), **Anotar** ou **Trocar responsável**. Tudo entra no histórico, com autor, data e hora. **Encaminhar** registra um encaminhamento para a rede.
6. **Encontrar uma demanda antiga.** Em **Demandas**, procure por uma palavra da descrição e use **Mais filtros** (estado, responsável, categoria, período, assistido).
7. **Assistidos e evoluções.** Em **Assistidos**, cadastre só o nome de tratamento. A ficha reúne as demandas, as evoluções e os encaminhamentos da pessoa. Nela fica **Lançar evolução**; ao abrir uma evolução, **Retificar** cria uma versão nova e guarda a anterior.
8. **Encaminhamentos.** A tela abre nos pendentes; **Registrar desfecho** grava o resultado uma única vez.
9. **Direção.** Em **Usuários**, cadastre e desative contas. Em **Relatórios**, emita o relatório do período ou do assistido e imprima pelo navegador. Em **Auditoria**, consulte quem fez o quê e quando.

### Sessão e dados preenchidos

- **Sair** encerra a sessão e apaga o que estava em rascunho nesta aba.
- Depois de **15 minutos sem uso**, a sessão é encerrada sozinha, porque o computador é compartilhado (RF02, RNF05). O token também vence em 30 minutos.
- Se a sessão terminar ou a internet cair no meio de um formulário, o que foi digitado continua guardado: ao entrar de novo com a mesma conta, o formulário volta preenchido (RNF16).

---

## Bibliotecas

### Interface (`frontend/package.json`)

| Biblioteca | Versão instalada | Licença | Uso |
| --- | --- | --- | --- |
| react, react-dom | 19.3.0 | MIT | Componentes funcionais, estado, efeitos e renderização no navegador |
| react-router-dom | 7.18.5 | MIT | Rotas filhas do layout, navegação, parâmetros da ficha e página de erro |
| axios | 1.21.1 | MIT | Requisições HTTP, dentro da classe `ClienteApi` |

O código segue as aulas de React: componentes de função, `useState` e `useEffect` com uma função `async` de busca, eventos com `preventDefault`, rotas filhas e Axios. A orientação a objetos aparece em duas classes, explicadas em [`docs/front-orientacao-a-objetos.md`](docs/front-orientacao-a-objetos.md):

- **`ClienteApi`** (`src/api/cliente.js`): o objeto `cliente`, usado por todas as páginas, guarda o endereço da API, o token, os rascunhos e as mensagens de erro;
- **`Demanda`** (`src/modelos/Demanda.js`): cada demanda da API vira um objeto com `rotuloEstado()`, `prazoFormatado()`, `estaVencida()` e `proximosEstados()`.

Dois recursos ficam fora das aulas, cada um em um só lugar:

- o **interceptador de respostas do Axios**, dentro do `ClienteApi`, trata o 401 das rotas protegidas. Quando a sessão vence, o sistema lembra a página. O rascunho guardado na aba volta para a mesma conta depois de entrar;
- o **`useRef`**, em `src/components/Confirmacao.jsx`, abre o `<dialog>` nativo com `showModal()`, que prende o foco no diálogo e volta com Esc.

A API valida o token e as permissões a cada requisição.

### Ferramentas de desenvolvimento da interface

| Pacote | Versão instalada | Licença | Uso |
| --- | --- | --- | --- |
| vite, @vitejs/plugin-react | 8.3.2, 6.1.1 | MIT | Servidor local, atualização durante a edição e build do JSX |
| eslint, @eslint/js, globals | 10.11.0, 10.0.1, 17.13.0 | MIT | Análise estática e reconhecimento das APIs do navegador |
| eslint-plugin-react-hooks, eslint-plugin-react-refresh | 7.1.1, 0.5.7 | MIT | Verificação dos hooks e das exportações de componentes |

O projeto é JavaScript puro (sem TypeScript) e não usa o React Compiler: o Vite só transforma o JSX, como nas aulas. A fonte Archivo é servida pelo próprio site (`frontend/public/fonts`, licença OFL). As origens do logotipo e da tipografia estão nos [créditos da interface](docs/CREDITOS-UI.md).

### Servidor (`backend/requirements.txt`)

| Biblioteca | Versões aceitas | Licença | Uso |
| --- | --- | --- | --- |
| Flask | 3.x | BSD-3-Clause | Aplicação web, rotas (blueprints) e respostas JSON |
| Flask-SQLAlchemy | 3.1 ou superior, < 4 | BSD-3-Clause | ORM: cada classe do model é uma tabela (SQLite3 ou PostgreSQL) |
| Flask-Migrate | 4.x | MIT | Migrações do banco com Alembic (`flask db upgrade`) |
| Flask-JWT-Extended | 4.6 ou superior, < 5 | MIT | Login com token JWT de 30 minutos e logout |
| Flask-Cors | 4.0 ou superior, < 6 | MIT | Libera só as origens do front listadas em `CORS_ORIGINS` |
| marshmallow | 3.21 ou superior, < 4 | MIT | Validação da entrada e formato da saída (schemas) |
| python-dotenv | 1.x | BSD-3-Clause | Lê o `.env` local |
| psycopg[binary] | 3.2 ou superior, < 4 | LGPL-3.0 | Driver do PostgreSQL (produção e Docker) |
| pytest | 8.x | MIT | Testes automatizados do servidor |

O SQLite3 não precisa de instalação: o módulo `sqlite3` já vem com o Python.

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
