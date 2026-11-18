import axios from 'axios'

const cliente = axios.create({ baseURL: import.meta.env?.VITE_API_URL || '', timeout: 20000 })
const chaveSessao = 'crie:sessao'
const prefixoRascunho = 'crie:rascunho:'

export function lerSessao() {
  return JSON.parse(sessionStorage.getItem(chaveSessao)) || { token: null, usuario: null, avisos: null }
}

function limparRascunhos() {
  for (const chave of Object.keys(sessionStorage)) {
    if (chave.startsWith(prefixoRascunho)) sessionStorage.removeItem(chave)
  }
}

export function guardarSessao({ token, usuario, avisos }) {
  const anterior = sessionStorage.getItem('crie:retornoUsuario')
  if (anterior && anterior !== String(usuario.id)) limparRascunhos()
  sessionStorage.setItem(chaveSessao, JSON.stringify({ token, usuario, avisos }))
  cliente.defaults.headers.common.Authorization = `Bearer ${token}`
}

function limparCredenciais() {
  sessionStorage.removeItem(chaveSessao)
  delete cliente.defaults.headers.common.Authorization
}

export function apagarSessao() {
  limparCredenciais()
  limparRascunhos()
  sessionStorage.removeItem('crie:retorno')
  sessionStorage.removeItem('crie:retornoUsuario')
}

export function expiraEm() {
  const { token } = lerSessao()
  if (!token) return 0
  try {
    const carga = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    return Number(JSON.parse(atob(carga)).exp) * 1000 || 0
  } catch {
    return 0
  }
}

export function expirarSessao() {
  const { usuario } = lerSessao()
  if (!usuario) return
  sessionStorage.setItem('crie:retornoUsuario', String(usuario.id))
  sessionStorage.setItem('crie:retorno', window.location.pathname + window.location.search)
  limparCredenciais()
  window.location.replace('/entrar')
}

function chaveRascunho(chave) {
  return prefixoRascunho + lerSessao().usuario?.id + ':' + chave
}

export function lerRascunho(chave) {
  return JSON.parse(sessionStorage.getItem(chaveRascunho(chave)))
}

export function guardarRascunho(chave, dados) {
  if (lerSessao().usuario) sessionStorage.setItem(chaveRascunho(chave), JSON.stringify(dados))
}

export function apagarRascunho(chave) {
  sessionStorage.removeItem(chaveRascunho(chave))
}

export function mensagemDeErro(erro) {
  if (!erro.response) {
    // Só envio (POST, PATCH) vem de formulário; numa consulta (GET) não há dado digitado a preservar.
    return erro.config?.method === 'get'
      ? 'Não foi possível falar com o servidor. Confira a internet e tente de novo.'
      : 'Não foi possível falar com o servidor. Seus dados continuam no formulário. Tente de novo.'
  }
  if (erro.response.status === 401 && erro.config?.url !== '/api/auth/login') return 'Sua sessão terminou. Entre de novo.'
  return erro.response.data?.erro || (erro.response.status === 403
    ? 'Seu perfil não tem acesso a esta operação.'
    : 'Não foi possível concluir a solicitação. Tente de novo.')
}

const { token } = lerSessao()
if (token) cliente.defaults.headers.common.Authorization = `Bearer ${token}`

cliente.interceptors.response.use(undefined, (erro) => {
  // Uma resposta atrasada de outra sessão não deve encerrar a sessão atual.
  const enviado = erro.config?.headers?.Authorization
  if (erro.response?.status === 401 && enviado && enviado === cliente.defaults.headers.common.Authorization &&
      !['/api/auth/login', '/api/auth/logout'].includes(erro.config.url)) expirarSessao()
  return Promise.reject(erro)
})

export default cliente
