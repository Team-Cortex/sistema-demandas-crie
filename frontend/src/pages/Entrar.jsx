import { useState } from 'react'
import { ArrowRight, Eye, EyeOff } from 'lucide-react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import cliente, { guardarSessao, lerSessao, mensagemDeErro } from '../api/cliente'
import classes from './Entrar.module.css'

function destinoInterno(caminho) {
  if (!caminho?.startsWith('/') || caminho.startsWith('//')) return '/'
  const url = new URL(caminho, window.location.origin)
  return url.origin === window.location.origin ? url.pathname + url.search : '/'
}

export default function Entrar() {
  const navegar = useNavigate()
  const { state } = useLocation()
  const [jaEstavaAutenticado] = useState(() => Boolean(lerSessao().token))
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [visivel, setVisivel] = useState(false)
  const [erros, setErros] = useState({})
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)
  const retorno = sessionStorage.getItem('crie:retorno')
  const aviso = retorno ? 'Sua sessão terminou. Entre de novo.' : state?.aviso

  function atualizarEmail(evento) {
    setEmail(evento.target.value)
    setErros({ ...erros, email: '' })
    setErro('')
  }

  function atualizarSenha(evento) {
    setSenha(evento.target.value)
    setErros({ ...erros, senha: '' })
    setErro('')
  }

  function alternarSenha() { setVisivel(!visivel) }

  async function entrar(evento) {
    evento.preventDefault()
    if (enviando) return
    const campos = evento.currentTarget.elements
    const falhas = {}
    if (!email.trim() || campos.email.validity.typeMismatch) falhas.email = 'Informe um e-mail válido.'
    if (!senha) falhas.senha = 'Informe a senha.'
    setErros(falhas)
    setErro('')
    if (Object.keys(falhas).length) {
      campos[Object.keys(falhas)[0]].focus()
      return
    }
    setEnviando(true)
    try {
      const { data } = await cliente.post('/api/auth/login', { email: email.trim(), senha })
      const mesmaPessoa = sessionStorage.getItem('crie:retornoUsuario') === String(data.usuario.id)
      const caminho = retorno ? (mesmaPessoa ? retorno : '/') : state?.destino
      guardarSessao(data)
      sessionStorage.removeItem('crie:retorno')
      sessionStorage.removeItem('crie:retornoUsuario')
      navegar(destinoInterno(caminho), { replace: true })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  if (jaEstavaAutenticado) return <Navigate to="/" replace />

  return (
    <main className={classes.tela}>
      <section className={classes.cartao} aria-labelledby="titulo-login">
        <img className={classes.marca} src="/crie-logo-oficial.png" alt="CRIE" width="128" height="60" />
        <h1 id="titulo-login">Entrar no sistema</h1>
        <p className={classes.instrucao}>Use o e-mail e a senha cadastrados no CRIE.</p>
        {aviso && <p className={classes.aviso} role="status">{aviso}</p>}
        <form className={classes.formulario} onSubmit={entrar} noValidate>
          <div className={classes.campo}>
            <label htmlFor="email">E-mail</label>
            <input id="email" name="email" type="email" value={email} onChange={atualizarEmail}
              autoComplete="username" autoCapitalize="none" required aria-invalid={Boolean(erros.email)}
              aria-describedby={erros.email ? 'erro-email' : undefined} />
            {erros.email && <span id="erro-email" className={classes.erroCampo}>{erros.email}</span>}
          </div>
          <div className={classes.campo}>
            <label htmlFor="senha">Senha</label>
            <div className={classes.senha}>
              <input id="senha" name="senha" type={visivel ? 'text' : 'password'} value={senha} onChange={atualizarSenha}
                autoComplete="current-password" required aria-invalid={Boolean(erros.senha)}
                aria-describedby={erros.senha ? 'erro-senha' : undefined} />
              <button type="button" onClick={alternarSenha} aria-label={visivel ? 'Ocultar senha' : 'Mostrar senha'}>
                {visivel ? <EyeOff size={19} aria-hidden="true" /> : <Eye size={19} aria-hidden="true" />}
              </button>
            </div>
            {erros.senha && <span id="erro-senha" className={classes.erroCampo}>{erros.senha}</span>}
          </div>
          {erro && <p className="aviso-erro" role="alert">{erro}</p>}
          <button type="submit" className="botao-primario" disabled={enviando}>
            {enviando ? 'Entrando…' : 'Entrar'}<ArrowRight size={18} aria-hidden="true" />
          </button>
        </form>
      </section>
    </main>
  )
}
