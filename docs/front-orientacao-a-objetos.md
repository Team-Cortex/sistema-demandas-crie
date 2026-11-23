# Orientação a objetos no front-end

O enunciado de Front End pede uma "aplicação REACT JS sob o paradigma de Orientação a Objetos" que consome a API Flask feita em POO. Este documento mostra onde a orientação a objetos aparece no código do `frontend/` e como ela conversa com o que foi visto em Programação Orientada a Objetos (Aula 14, em Python).

**A escolha:** os componentes continuam **funções**, como nas Aulas 03 a 09 de Front End (componente funcional, props, `useState`, `useEffect`). A orientação a objetos entra onde ela resolve um problema real do front:

1. **`ClienteApi`** (`frontend/src/api/cliente.js`): o objeto que conversa com a API.
2. **`Demanda`** (`frontend/src/modelos/Demanda.js`): cada demanda que chega da API vira um objeto que sabe se apresentar na tela.

O back-end tem a sua parte em [`poo-no-backend.md`](poo-no-backend.md).

---

## 1. Resumo: conceito, onde está, como é em Python

| Conceito (Aula 14) | No front (JavaScript) | Onde | Em Python seria |
| --- | --- | --- | --- |
| Classe | `class ClienteApi { ... }` e `class Demanda { ... }` | `src/api/cliente.js` linha 5; `src/modelos/Demanda.js` linha 15 | `class Demanda:` |
| Construtor | `constructor(baseURL)` e `constructor(dados)` | `cliente.js` linha 9; `Demanda.js` linha 16 | `def __init__(self, ...)` |
| `self` | `this` (`this.#http`, `this.estado`) | os dois arquivos | `self` |
| Objeto (instância) | `new ClienteApi(...)` e `new Demanda(dados)` | `cliente.js` linha 97; páginas (seção 3) | `Demanda(...)` |
| Atributo | `this.id`, `this.prazo`, `this.estado`... copiados do JSON | `Demanda.js` linha 19 | `self.prazo = prazo` |
| Método | `cliente.get(...)`, `demanda.rotuloEstado()` | os dois arquivos | `def rotulo_estado(self):` |
| Encapsulamento (privado) | campo `#http` e método `#chaveRascunho` | `cliente.js` linhas 7 e 66 | `self.__http` (o `__` da Aula 14) |
| Método estático | `static validar(campos)` | `Demanda.js` linha 45 | `@staticmethod` |

---

## 2. `ClienteApi`: o objeto que fala com a API

Arquivo: `frontend/src/api/cliente.js`.

**Por que uma classe.** Toda tela precisa das mesmas coisas: o endereço da API, o token de quem entrou, o tratamento da sessão vencida, os rascunhos (RNF16) e uma mensagem de erro em português (RNF14). A classe junta esses dados e as operações sobre eles num lugar só. As páginas não sabem como isso é feito; só chamam os métodos.

**Construtor (linha 9).** Recebe a `baseURL`, cria o Axios com `axios.create` (como o `src/services/api.js` da Aula 09 de Front End), recoloca o token se a aba já tinha sessão e registra o interceptador do 401.

**Encapsulamento (linhas 7 e 66).** O Axios fica no campo privado `#http`. Fora da classe, escrever `cliente.#http` é erro de sintaxe: ninguém troca o token ou o endereço por fora. É a mesma ideia do `__` da Aula 14 em Python (no JavaScript, o `#` é privado de verdade, não só por convenção). O método `#chaveRascunho` também é privado: só a classe sabe como a chave do rascunho é montada.

**Métodos.**

| Método | O que faz |
| --- | --- |
| `get`, `post`, `patch` | fazem a requisição pelo Axios privado; as páginas escrevem `await cliente.get('/api/demandas')`, igual à aula |
| `lerSessao`, `guardarSessao` | leem e gravam a sessão no `sessionStorage` e põem o token no cabeçalho `Authorization` |
| `apagarSessao` | botão **Sair**: apaga a sessão e os rascunhos |
| `esquecerSessao` | sessão vencida (401) ou 15 minutos sem uso: tira só a sessão; o rascunho volta para a mesma conta |
| `lerRascunho`, `guardarRascunho`, `apagarRascunho` | guardam o que foi digitado, para nada se perder se a internet cair (RNF16) |
| `mensagemDeErro` | devolve o texto do servidor (`{"erro": "..."}`) ou uma mensagem de conexão |

**O objeto (linha 97).** `const cliente = new ClienteApi(import.meta.env?.VITE_API_URL || '')`. É criado uma vez e exportado; todas as páginas importam esse mesmo objeto:

```js
import cliente from '../api/cliente'

const resposta = await cliente.get('/api/demandas/minhas')
setErro(cliente.mensagemDeErro(falha))
```

**`this` dentro do interceptador (linha 16).** A função do interceptador é uma *arrow function*; por isso o `this` dentro dela continua sendo o objeto `ClienteApi`, e ela consegue chamar `this.esquecerSessao()` (linha 19). O interceptador é extraclasse em Front End (está anotado no código e no README).

---

## 3. `Demanda`: a classe de domínio

Arquivo: `frontend/src/modelos/Demanda.js`. É o mesmo conceito da classe `Demanda` do back-end (`backend/app/models/demanda.py`), do lado da tela.

**Construtor (linha 16).** Recebe o JSON que veio da API e copia os campos para o objeto com `Object.assign(this, dados)`. É o equivalente ao `self.prazo = prazo` do `__init__`: depois disso, `demanda.id`, `demanda.descricao` e `demanda.prazo` existem no objeto.

**Métodos.**

| Método | Devolve | Antes era |
| --- | --- | --- |
| `estaVencida()` | `true` quando o servidor marcou a demanda como vencida | `demanda.vencida` espalhado nas telas |
| `rotuloEstado()` | "Em andamento", "Aguardando terceiros"... | `estados[demanda.estado]` |
| `rotuloPrioridade()` | "Baixa", "Média", "Alta" | `prioridades[demanda.prioridade]` |
| `prazoFormatado()` | `dd/mm/aaaa` | `dataCurta(demanda.prazo)` |
| `proximosEstados()` | os estados para onde ela pode ir (spec 02) | `transicoes[demanda.estado]` em `pages/regrasDemanda.js` |
| `static validar(campos)` | os erros do formulário de registro | `validarDemanda(campos)` em `pages/regrasDemanda.js` |

`estaVencida()` não refaz a conta da data: quem decide é o servidor, no fuso do CRIE (`Demanda.vencida_em` no back-end). Se um dia a regra mudar, só o método muda; as telas continuam chamando `demanda.estaVencida()`. Isso também é encapsulamento: a tela não precisa saber de onde vem a informação.

`validar` é **estático** porque valida o formulário antes de a demanda existir: pertence à classe, não a um objeto. Chama-se `Demanda.validar(campos)` (`pages/NovaDemanda.jsx` linha 73), como um `@staticmethod` do Python.

**Onde os objetos são criados (`new Demanda`).** A página recebe o JSON e transforma cada item em objeto com `map` (Aula 06):

| Arquivo | Linha | Trecho |
| --- | --- | --- |
| `pages/MinhasDemandas.jsx` | 19 | `setDemandas(resposta.data.map(dados => new Demanda(dados)))` |
| `pages/Demandas.jsx` | 53 | idem, com os filtros |
| `pages/DetalheDemanda.jsx` | 39, 143, 148, 152 | a demanda da ficha e a versão nova depois de cada alteração |
| `pages/Painel.jsx` | 27 e 102 | os itens do aviso de prazo e os cartões de cada coluna |
| `pages/assistidos/FichaAssistido.jsx` | 24 | as demandas do assistido |
| `pages/reunioes/FichaReuniao.jsx` | 22 | as demandas da reunião |

**Onde os métodos são usados.** Os componentes recebem o objeto por props e chamam os métodos: `components/CartaoDemanda.jsx` (linhas 9 a 16), `components/ListaDemandas.jsx` (linhas 22 a 27), a ficha em `pages/DetalheDemanda.jsx` (linhas 92 e 179 a 184) e o aviso do painel (`pages/Painel.jsx` linha 70).

Um cuidado: ao acrescentar uma anotação, a ficha monta a demanda nova com `new Demanda({ ...demanda, historico: [...] })` (linha 148). Só o `{ ...demanda }` geraria um objeto comum, sem os métodos.

---

## 4. O que não usamos no front, e por quê

- **Herança e polimorfismo:** nenhuma das duas classes estende outra. O front não tem tipos diferentes de demanda nem de cliente; criar uma hierarquia só para mostrar o conceito seria abstração sem motivo. Herança e polimorfismo aparecem no back-end, onde resolvem problema real: os perfis de usuário (ver [`poo-no-backend.md`](poo-no-backend.md)).
  - No teste `frontend/tests/sessao.test.js`, a classe `Armazenamento` imita o `sessionStorage` com os mesmos métodos (`getItem`, `setItem`, `removeItem`, `clear`). O `ClienteApi` usa um ou outro sem perceber a diferença: é a ideia do polimorfismo (objetos diferentes respondendo à mesma mensagem), usada só no teste.
- **Componentes de classe** (`class Painel extends React.Component`): não foram dados nas aulas de Front End e a documentação atual do React recomenda funções com hooks. Os componentes continuam funções.

---

## 5. Como explicar na apresentação (1 minuto)

1. Abra `src/api/cliente.js`: "Aqui está a classe `ClienteApi`. O construtor recebe o endereço da API. O Axios fica no campo privado `#http`, então nenhuma tela mexe nele direto: é encapsulamento, como o `__` do Python."
2. Desça até a linha 97: "Este é o objeto, criado com `new`. Todas as páginas usam ele: `cliente.get(...)`, `cliente.mensagemDeErro(...)`."
3. Abra `src/modelos/Demanda.js`: "Cada demanda que chega da API vira um objeto `Demanda`. Em vez de cada tela traduzir o estado e formatar a data, o objeto sabe: `rotuloEstado()`, `prazoFormatado()`, `estaVencida()`."
4. Abra `components/CartaoDemanda.jsx`: "O componente recebe o objeto por props e chama os métodos."

---

## 6. Testes

Rodam com `node --test` dentro de `frontend/`:

- `tests/Demanda.test.js`: cria objetos `Demanda` e confere os métodos e a validação.
- `tests/sessao.test.js`: confere a sessão, os rascunhos e o `mensagemDeErro` do objeto `cliente`. Como o Axios é privado, o teste lê o cabeçalho enviado por um `adapter` passado na própria requisição, sem abrir o encapsulamento.
