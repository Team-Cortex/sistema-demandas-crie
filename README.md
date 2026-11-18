# sistema-demandas-crie

Sistema web para registro e acompanhamento das demandas levantadas nas reuniões de equipe do **CRIE — Centro de Integração Especial / APAE de Extrema**.

Projeto de extensão curricularizada do curso de Tecnologia em Análise e Desenvolvimento de Sistemas do **IFSP — Câmpus Bragança Paulista**, disciplina Extensão como Metodologia de Ensino 2 (BRAEXT2), sob orientação do Prof. Luiz Gustavo Diniz de Oliveira Véras.

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
| Front-end | React |
| Back-end | Python + Flask (orientado a objetos) |
| Banco de dados | PostgreSQL |
| Comunicação | API REST |
| Migrações | Alembic |

---

## Estrutura do repositório

```
sistema-demandas-crie/
├── docs/                 documentação compartilhada
├── backend/              servidor Flask
├── frontend/             cliente React
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
| [`docs/contrato-api.md`](docs/contrato-api.md) | Proposta de contrato HTTP entre o React e o Flask |
| [`docs/specs/`](docs/specs/) | Comportamento do servidor, na ordem de implementação |
| [`docs/estado-do-projeto.md`](docs/estado-do-projeto.md) | Mapa geral do que o sistema é hoje, mantido pela frente de back-end |

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

O servidor é o Flask em `backend/`. O cliente é o React em `frontend/`, com os mesmos arquivos que estavam na raiz. Detalhe do servidor em [`backend/README.md`](backend/README.md).

```bash
# Subir o banco de dados
docker compose up -d

# Servidor
cd backend
cp .env.example .env        # preencher os valores
pip install -r requirements.txt
flask db upgrade            # cria as tabelas
python seed.py              # opcional: dados fictícios de demonstração
flask run
```

### Front-end de demandas

Com a API local em execução, abra outro terminal na raiz do repositório. Use Node.js 22.13 ou superior em uma versão LTS compatível e instale as versões registradas no lockfile.

```bash
cd frontend
npm ci
npm run dev
```

Abra [o sistema local](http://localhost:5173) e entre com uma conta da carga fictícia do servidor. A API deve permitir essa origem em `CORS_ORIGINS`. Em desenvolvimento, `frontend/.env.development` define `VITE_API_URL=http://localhost:5000`. A variável contém apenas a origem pública da API. No build de produção, omita-a para usar a mesma origem da interface. As rotas da API já incluem `/api`.

O painel reúne os totais e as demandas em aberto. Em **Demandas**, use a descrição e os filtros para localizar um registro. **Registrar demanda** abre um único formulário com confirmação. Na ficha é possível mudar o estado, anotar e trocar o responsável. O prazo de cada aviso e a indicação de vencimento vêm do servidor.

Em **Reuniões**, a equipe registra os participantes e abre uma demanda vinculada ao encontro. **Assistidos** reúne as demandas, evoluções e encaminhamentos de cada pessoa pelo nome de tratamento. Retificar uma evolução preserva a versão anterior. Para encaminhar, abra a demanda ou a ficha do assistido. Em **Encaminhamentos**, consulte as pendências e registre o desfecho.

A direção também acessa **Usuários**, **Relatórios** e **Auditoria**. Os relatórios do período e do assistido podem ser impressos pelo navegador com a identificação de quem os emitiu. A auditoria permite consultar e filtrar os registros em páginas.

Para verificar o cliente, execute os comandos abaixo dentro de `frontend/`.

```bash
npm run lint
node --test
npm run build
```

#### Bibliotecas da interface

| Biblioteca | Versão instalada | Licença | Uso |
| --- | --- | --- | --- |
| react, react-dom | 19.3.0 | MIT | Componentes funcionais, estado, efeitos e renderização no navegador |
| react-router-dom | 7.18.5 | MIT | Rotas filhas do layout, navegação, parâmetros da ficha e página de erro |
| axios | 1.21.1 | MIT | Cliente HTTP único, cabeçalho de autenticação e tratamento das respostas |
| lucide-react | 1.75.0 | ISC e MIT (ícones derivados de Feather) | Ícones de navegação, estados e ações com rótulo |

O código segue as aulas de React: componentes de função, `useState` e `useEffect` com uma função `async` de busca, eventos com `preventDefault`, rotas filhas e Axios. Dois recursos ficam fora delas, cada um em um só lugar:

- o **interceptador de respostas do Axios**, em `src/api/cliente.js`, trata o 401 das rotas protegidas. Quando a sessão vence, o sistema lembra a página. O rascunho guardado na aba volta para a mesma conta depois de entrar;
- o **`useRef`**, em `src/components/Confirmacao.jsx`, abre o `<dialog>` nativo com `showModal()`, que prende o foco no diálogo e volta com Esc.

Sair pelo menu apaga a sessão e os rascunhos da aba. A API valida o token e as permissões a cada requisição.

#### Ferramentas de desenvolvimento

| Pacote | Versão instalada | Licença | Uso |
| --- | --- | --- | --- |
| vite, @vitejs/plugin-react | 8.3.2, 6.1.1 | MIT | Servidor local, atualização durante a edição e build |
| @babel/core, @rolldown/plugin-babel, babel-plugin-react-compiler | 7.29.7, 0.2.4, 1.0.0 | MIT | Compilação dos componentes no Vite com React Compiler |
| eslint, @eslint/js, globals | 10.11.0, 10.0.1, 17.13.0 | MIT | Análise estática e reconhecimento das APIs do navegador |
| eslint-plugin-react-hooks, eslint-plugin-react-refresh | 7.1.1, 0.5.7 | MIT | Verificação dos hooks e das exportações de componentes |
| @types/react, @types/react-dom | 19.3.0, 19.3.0 | MIT | Definições do ambiente React para apoio do editor ao JSX |

As origens do logotipo, da tipografia e dos ícones estão nos [créditos da interface](docs/CREDITOS-UI.md).

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
