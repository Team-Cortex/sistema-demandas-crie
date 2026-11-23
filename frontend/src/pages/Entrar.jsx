import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import cliente from '../api/cliente'
import styles from './Entrar.module.css'

export default function Entrar() {
  const navegar = useNavigate()
  const { state } = useLocation()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [senhaVisivel, setSenhaVisivel] = useState(false)
  const [erros, setErros] = useState({})
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)
  // Página de onde a sessão vencida saiu (o cliente guarda no 401).
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

  function alternarSenha() {
    setSenhaVisivel(!senhaVisivel)
  }

  async function entrar(evento) {
    evento.preventDefault()
    const falhas = {}
    if (!email.includes('@')) falhas.email = 'Informe um e-mail válido.'
    if (!senha) falhas.senha = 'Informe a senha.'
    setErros(falhas)
    setErro('')
    if (falhas.email || falhas.senha) {
      evento.currentTarget.elements[falhas.email ? 'email' : 'senha'].focus()
      return
    }
    setEnviando(true)
    try {
      const resposta = await cliente.post('/api/auth/login', { email: email.trim(), senha })
      cliente.guardarSessao(resposta.data)
      sessionStorage.removeItem('crie:retorno')
      navegar(retorno || state?.destino || '/', { replace: true })
    } catch (falha) {
      setErro(cliente.mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <main className={styles.tela}>
      <section className={styles.cartao} aria-labelledby="titulo-login">
        <img className={styles.marca} src="/crie-logo-oficial.png" alt="CRIE" width="128" height="60" />
        <h1 id="titulo-login">Entrar no sistema</h1>
        <p className={styles.instrucao}>Use o e-mail e a senha cadastrados no CRIE.</p>
        {aviso && <p className={styles.aviso} role="status">{aviso}</p>}
        <form className={styles.formulario} onSubmit={entrar} noValidate>
          <div className={styles.campo}>
            <label htmlFor="email">E-mail</label>
            <input id="email" name="email" type="email" value={email} onChange={atualizarEmail}
              autoComplete="username" autoCapitalize="none" required aria-invalid={Boolean(erros.email)}
              aria-describedby={erros.email ? 'erro-email' : undefined} />
            {erros.email && <span id="erro-email" className={styles.erroCampo}>{erros.email}</span>}
          </div>
          <div className={styles.campo}>
            <label htmlFor="senha">Senha</label>
            <input id="senha" name="senha" type={senhaVisivel ? 'text' : 'password'} value={senha} onChange={atualizarSenha}
              autoComplete="current-password" required aria-invalid={Boolean(erros.senha)}
              aria-describedby={erros.senha ? 'erro-senha' : undefined} />
            {erros.senha && <span id="erro-senha" className={styles.erroCampo}>{erros.senha}</span>}
            <label className={styles.mostrar}>
              <input type="checkbox" checked={senhaVisivel} onChange={alternarSenha} /> Mostrar senha
            </label>
          </div>
          {erro && <p className="aviso-erro" role="alert">{erro}</p>}
          <button type="submit" className="botao-primario" disabled={enviando}>
            {enviando ? 'Entrando…' : 'Entrar'}
          </button>
        </form>
      </section>
    </main>
  )
}
