import { useEffect, useState } from 'react'
import { ArrowRight, Eye, EyeOff } from 'lucide-react'
import { useLocation, useNavigate } from 'react-router-dom'
import cliente, { guardarSessao, mensagemDeErro } from '../api/cliente'
import classes from './Entrar.module.css'

// Acesso rápido de demonstração: só aparece quando a API diz que está ligado (DEMO_ACESSO_RAPIDO).
const PERFIS_DEMO = {
  direcao: 'Direção',
  assistente_social: 'Assistente social',
  equipe_pedagogica: 'Equipe pedagógica',
}

export default function Entrar() {
  const navegar = useNavigate()
  const { state } = useLocation()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [senhaVisivel, setSenhaVisivel] = useState(false)
  const [erros, setErros] = useState({})
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [perfisDemo, setPerfisDemo] = useState([])
  // Página de onde a sessão vencida saiu (o cliente guarda no 401).
  const retorno = sessionStorage.getItem('crie:retorno')
  const aviso = retorno ? 'Sua sessão terminou. Entre de novo.' : state?.aviso

  useEffect(() => {
    let ativo = true
    cliente.get('/api/demo')
      .then((resposta) => { if (ativo) setPerfisDemo(resposta.data.perfis || []) })
      .catch(() => {})
    return () => { ativo = false }
  }, [])

  async function entrarComoDemo(perfil) {
    setErro('')
    setEnviando(true)
    try {
      const resposta = await cliente.post('/api/demo/entrar', { perfil })
      guardarSessao(resposta.data)
      sessionStorage.removeItem('crie:retorno')
      navegar('/', { replace: true })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

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
      guardarSessao(resposta.data)
      sessionStorage.removeItem('crie:retorno')
      navegar(retorno || state?.destino || '/', { replace: true })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

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
              <input id="senha" name="senha" type={senhaVisivel ? 'text' : 'password'} value={senha} onChange={atualizarSenha}
                autoComplete="current-password" required aria-invalid={Boolean(erros.senha)}
                aria-describedby={erros.senha ? 'erro-senha' : undefined} />
              <button type="button" onClick={alternarSenha} aria-label={senhaVisivel ? 'Ocultar senha' : 'Mostrar senha'}>
                {senhaVisivel ? <EyeOff size={19} aria-hidden="true" /> : <Eye size={19} aria-hidden="true" />}
              </button>
            </div>
            {erros.senha && <span id="erro-senha" className={classes.erroCampo}>{erros.senha}</span>}
          </div>
          {erro && <p className="aviso-erro" role="alert">{erro}</p>}
          <button type="submit" className="botao-primario" disabled={enviando}>
            {enviando ? 'Entrando…' : 'Entrar'}<ArrowRight size={18} aria-hidden="true" />
          </button>
        </form>
        {perfisDemo.length > 0 && (
          <section className={classes.demo} aria-labelledby="titulo-demo">
            <h2 id="titulo-demo">Acesso rápido para demonstração</h2>
            <p>Entra com um usuário fictício de cada perfil. Todos os dados são fictícios.</p>
            <div className={classes.demoBotoes}>
              {perfisDemo.filter((perfil) => PERFIS_DEMO[perfil]).map((perfil) => (
                <button key={perfil} type="button" className="botao-secundario" disabled={enviando}
                  onClick={() => entrarComoDemo(perfil)}>
                  Entrar como {PERFIS_DEMO[perfil]}
                </button>
              ))}
            </div>
          </section>
        )}
      </section>
    </main>
  )
}
