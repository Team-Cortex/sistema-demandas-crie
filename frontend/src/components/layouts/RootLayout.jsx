import { useEffect, useRef, useState } from 'react'
import { Link, Navigate, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { CalendarDays, ClipboardList, FolderOpen, LayoutDashboard, LogOut, Menu, UserRound, X } from 'lucide-react'
import cliente, { apagarSessao, expiraEm, expirarSessao, lerSessao } from '../../api/cliente'
import { perfis } from '../../dominio'
import { FileText } from 'lucide-react'
import { Send } from 'lucide-react'
import { ContactRound } from 'lucide-react'
import { CalendarRange } from 'lucide-react'
import classes from './RootLayout.module.css'

const navegacao = [
  { rota: '/', texto: 'Painel', icone: LayoutDashboard },
  { rota: '/minhas', texto: 'Minhas demandas', icone: ClipboardList },
  { rota: '/demandas', texto: 'Demandas', icone: FolderOpen },
  { rota: '/reunioes', texto: 'Reuniões', icone: CalendarRange },
  { rota: '/assistidos', texto: 'Assistidos', icone: ContactRound },
  { rota: '/encaminhamentos', texto: 'Encaminhamentos', icone: Send },
  { rota: '/relatorios', texto: 'Relatórios', icone: FileText, direcao: true },
]

const formatoData = new Intl.DateTimeFormat('pt-BR', {
  day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'America/Sao_Paulo',
})

export default function RootLayout() {
  const { usuario, token } = lerSessao()
  const { pathname, search } = useLocation()
  const navegar = useNavigate()
  const [menuAberto, definirMenuAberto] = useState(false)
  const [saindo, definirSaindo] = useState(false)
  const botaoMenu = useRef(null)
  const painelMenu = useRef(null)
  const conteudo = useRef(null)
  const paginaAnterior = useRef(pathname)

  useEffect(() => {
    if (paginaAnterior.current !== pathname) conteudo.current?.focus()
    paginaAnterior.current = pathname
  }, [pathname])

  useEffect(() => {
    if (!token) return
    const temporizador = window.setTimeout(expirarSessao, Math.max(0, expiraEm() - Date.now()))
    return () => window.clearTimeout(temporizador)
  }, [token])

  useEffect(() => {
    if (!menuAberto) return
    function fecharComEscape(evento) {
      if (evento.key === 'Escape') {
        definirMenuAberto(false)
        botaoMenu.current?.focus()
      }
    }
    window.addEventListener('keydown', fecharComEscape)
    function fecharFora(evento) {
      if (!painelMenu.current?.contains(evento.target)) definirMenuAberto(false)
    }
    document.addEventListener('pointerdown', fecharFora)
    return () => {
      window.removeEventListener('keydown', fecharComEscape)
      document.removeEventListener('pointerdown', fecharFora)
    }
  }, [menuAberto])

  async function sair() {
    definirSaindo(true)
    let aviso = ''
    try {
      await cliente.post('/api/auth/logout', null, { timeout: 8000 })
    } catch (erro) {
      if (erro.response?.status !== 401) {
        aviso = 'Você saiu deste navegador. O servidor não confirmou o encerramento da sessão.'
      }
    } finally {
      apagarSessao()
      navegar('/entrar', { replace: true, state: { aviso } })
    }
  }

  function alternarMenu() { definirMenuAberto(!menuAberto) }
  function fecharMenu() { definirMenuAberto(false) }
  function classeDoLink({ isActive }) {
    return isActive ? classes.ativo : undefined
  }

  if (!token || !usuario) return <Navigate to="/entrar" replace state={{ destino: pathname + search }} />

  return (
    <div className={classes.layout}>
      <a className={classes.pular} href="#conteudo">Ir para o conteúdo</a>
      <aside className={classes.lateral} ref={painelMenu}>
        <div className={classes.cabecalhoMenu}>
          <Link to="/" className={classes.marca} onClick={fecharMenu} aria-label="CRIE — ir para o painel">
            <img src="/crie-logo-oficial.png" alt="CRIE" width="107" height="50" />
          </Link>
          <button type="button" className={classes.menu} aria-expanded={menuAberto}
            aria-controls="navegacao" ref={botaoMenu} onClick={alternarMenu}>
            {menuAberto ? <X size={19} aria-hidden="true" /> : <Menu size={19} aria-hidden="true" />} Menu
          </button>
        </div>
        <div id="navegacao" className={menuAberto ? classes.navegacaoAberta : classes.navegacao}>
          <nav aria-label="Navegação principal">
            {navegacao.filter(item => !item.direcao || usuario.perfil === 'direcao').map(({ rota, texto, icone: Icone }) => (
              <NavLink key={rota} to={rota} end={rota === '/'} className={classeDoLink} onClick={fecharMenu}>
                <Icone size={20} strokeWidth={1.8} aria-hidden="true" /> {texto}
              </NavLink>
            ))}
          </nav>
        </div>
      </aside>
      <div className={classes.area}>
        <header className={classes.topo}>
          <div className={classes.usuario}>
            <span className={classes.avatar}><UserRound size={21} aria-hidden="true" /></span>
            <div><strong>Olá, {usuario.nome.trim().split(/\s+/)[0]}</strong><span>{perfis[usuario.perfil]}</span></div>
          </div>
          <div className={classes.fimTopo}>
            <div className={classes.data}><CalendarDays size={17} aria-hidden="true" />{formatoData.format(new Date())}</div>
            <button className={classes.sair} type="button" onClick={sair} disabled={saindo}>
              <LogOut size={19} aria-hidden="true" />{saindo ? 'Saindo…' : 'Sair'}
            </button>
          </div>
        </header>
        <main className={classes.conteudo} ref={conteudo} id="conteudo" tabIndex={-1}>
          <Outlet key={pathname} />
        </main>
      </div>
    </div>
  )
}
