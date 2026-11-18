import axios from 'axios'

// Sem VITE_API_URL, a API fica no mesmo endereço do front (Vercel). O "?." deixa os testes rodarem fora do Vite.
const cliente = axios.create({ baseURL: import.meta.env?.VITE_API_URL || '', timeout: 20000 })

export function lerSessao() {
  return JSON.parse(sessionStorage.getItem('crie:sessao')) || {}
}

export function guardarSessao(sessao) {
  // Rascunho deixado por outra conta neste navegador não fica para quem entrou agora.
  for (const chave of Object.keys(sessionStorage)) {
    if (chave.startsWith('crie:rascunho:') && !chave.startsWith(`crie:rascunho:${sessao.usuario.id}:`)) {
      sessionStorage.removeItem(chave)
    }
  }
  sessionStorage.setItem('crie:sessao', JSON.stringify(sessao))
  cliente.defaults.headers.common.Authorization = 'Bearer ' + sessao.token
}

export function apagarSessao() {
  sessionStorage.clear()
  delete cliente.defaults.headers.common.Authorization
}

// O rascunho guarda o que foi digitado: se a sessão vencer ou a internet cair, nada se perde (RNF16).
function chaveRascunho(nome) {
  return `crie:rascunho:${lerSessao().usuario?.id}:${nome}`
}

export function lerRascunho(nome) {
  return JSON.parse(sessionStorage.getItem(chaveRascunho(nome)))
}

export function guardarRascunho(nome, dados) {
  sessionStorage.setItem(chaveRascunho(nome), JSON.stringify(dados))
}

export function apagarRascunho(nome) {
  sessionStorage.removeItem(chaveRascunho(nome))
}

export function mensagemDeErro(erro) {
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

const { token } = lerSessao()
if (token) cliente.defaults.headers.common.Authorization = 'Bearer ' + token

// Extraclasse: o interceptador trata a sessão vencida (401) num lugar só, em vez de em cada tela.
// Login e logout ficam de fora: lá o 401 é senha errada ou sessão já encerrada.
cliente.interceptors.response.use(undefined, (erro) => {
  if (erro.response?.status === 401 && !erro.config.url.startsWith('/api/auth/')) {
    sessionStorage.setItem('crie:retorno', window.location.pathname + window.location.search)
    sessionStorage.removeItem('crie:sessao')
    window.location.replace('/entrar')
  }
  return Promise.reject(erro)
})

export default cliente
