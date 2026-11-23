import axios from 'axios'

// Classe: junta num lugar só o endereço da API, o token, os rascunhos e as mensagens de erro.
// As páginas usam o objeto criado no fim do arquivo: cliente.get(...), cliente.mensagemDeErro(...).
class ClienteApi {
  // Encapsulamento: o # deixa o Axios privado. Fora da classe, só os métodos abaixo chegam nele.
  #http

  constructor(baseURL) {
    this.#http = axios.create({ baseURL, timeout: 20000 })
    const { token } = this.lerSessao()
    if (token) this.#http.defaults.headers.common.Authorization = 'Bearer ' + token

    // Extraclasse: o interceptador trata a sessão vencida (401) num lugar só, em vez de em cada tela.
    // Login e logout ficam de fora: lá o 401 é senha errada ou sessão já encerrada.
    this.#http.interceptors.response.use(undefined, (erro) => {
      if (erro.response?.status === 401 && !erro.config.url.startsWith('/api/auth/')) {
        sessionStorage.setItem('crie:retorno', window.location.pathname + window.location.search)
        this.esquecerSessao()
        window.location.replace('/entrar')
      }
      return Promise.reject(erro)
    })
  }

  get(url, opcoes) {
    return this.#http.get(url, opcoes)
  }

  post(url, dados, opcoes) {
    return this.#http.post(url, dados, opcoes)
  }

  patch(url, dados, opcoes) {
    return this.#http.patch(url, dados, opcoes)
  }

  lerSessao() {
    return JSON.parse(sessionStorage.getItem('crie:sessao')) || {}
  }

  guardarSessao(sessao) {
    // Rascunho deixado por outra conta neste navegador não fica para quem entrou agora.
    for (const chave of Object.keys(sessionStorage)) {
      if (chave.startsWith('crie:rascunho:') && !chave.startsWith(`crie:rascunho:${sessao.usuario.id}:`)) {
        sessionStorage.removeItem(chave)
      }
    }
    sessionStorage.setItem('crie:sessao', JSON.stringify(sessao))
    this.#http.defaults.headers.common.Authorization = 'Bearer ' + sessao.token
  }

  // Sair pelo menu: apaga a sessão e também os rascunhos da aba.
  apagarSessao() {
    sessionStorage.clear()
    delete this.#http.defaults.headers.common.Authorization
  }

  // Sessão vencida (401) ou encerrada por inatividade: o rascunho fica para quem entrar de novo com a mesma conta.
  esquecerSessao() {
    sessionStorage.removeItem('crie:sessao')
    delete this.#http.defaults.headers.common.Authorization
  }

  // O rascunho guarda o que foi digitado: se a sessão vencer ou a internet cair, nada se perde (RNF16).
  #chaveRascunho(nome) {
    return `crie:rascunho:${this.lerSessao().usuario?.id}:${nome}`
  }

  lerRascunho(nome) {
    return JSON.parse(sessionStorage.getItem(this.#chaveRascunho(nome)))
  }

  guardarRascunho(nome, dados) {
    sessionStorage.setItem(this.#chaveRascunho(nome), JSON.stringify(dados))
  }

  apagarRascunho(nome) {
    sessionStorage.removeItem(this.#chaveRascunho(nome))
  }

  mensagemDeErro(erro) {
    if (!erro.response) {
      // Só envio (POST, PATCH) vem de formulário; numa consulta (GET) não há dado digitado a preservar.
      return erro.config?.method === 'get'
        ? 'Não foi possível falar com o servidor. Confira a internet e tente de novo.'
        : 'Não foi possível falar com o servidor. Seus dados continuam no formulário. Tente de novo.'
    }
    if (erro.response.data?.erro) return erro.response.data.erro
    if (erro.response.status === 403) return 'Seu perfil não tem acesso a esta operação.'
    return 'Não foi possível concluir a solicitação. Tente de novo.'
  }
}

// Objeto: a única instância da classe, usada por todas as páginas.
// Sem VITE_API_URL, a API fica no mesmo endereço do front (Vercel). O "?." deixa os testes rodarem fora do Vite.
const cliente = new ClienteApi(import.meta.env?.VITE_API_URL || '')

export default cliente
