import { useState } from 'react'
import { Link, Navigate, Outlet, useLocation, useNavigate } from 'react-router-dom'
import {
  CalendarDays, CalendarRange, ClipboardList, ContactRound, FileText, FolderOpen, History,
  LayoutDashboard, LogOut, Menu, Send, UserRound, UsersRound, X,
} from 'lucide-react'
import cliente, { apagarSessao, lerSessao } from '../../api/cliente'
import { dataCurta, hojeCrie, perfis } from '../../dominio'
import classes from './RootLayout.module.css'

const navegacao = [
  { rota: '/', texto: 'Painel', icone: LayoutDashboard },
  { rota: '/minhas', texto: 'Minhas demandas', icone: ClipboardList },
  { rota: '/demandas', texto: 'Demandas', icone: FolderOpen },
  { rota: '/reunioes', texto: 'Reuniões', icone: CalendarRange },
  { rota: '/assistidos', texto: 'Assistidos', icone: ContactRound },
  { rota: '/encaminhamentos', texto: 'Encaminhamentos', icone: Send },
  { rota: '/usuarios', texto: 'Usuários', icone: UsersRound, direcao: true },
  { rota: '/relatorios', texto: 'Relatórios', icone: FileText, direcao: true },
  { rota: '/auditoria', texto: 'Auditoria', icone: History, direcao: true },
]

export default function RootLayout() {
  const { usuario, token } = lerSessao()
  const { pathname, search } = useLocation()
  const navegar = useNavigate()
  const [menuAberto, setMenuAberto] = useState(false)
  const [saindo, setSaindo] = useState(false)
  // As telas de evolução ficam dentro de Assistidos no menu.
  const secao = pathname.split('/')[1]
  const rotaAtual = secao === 'evolucoes' ? '/assistidos' : '/' + secao

  async function sair() {
    setSaindo(true)
    let aviso = ''
    try {
      await cliente.post('/api/auth/logout', null, { timeout: 8000 })
    } catch (erro) {
      if (erro.response?.status !== 401) {
        aviso = 'Você saiu deste navegador. O servidor não confirmou o encerramento da sessão.'
      }
    }
    apagarSessao()
    navegar('/entrar', { replace: true, state: { aviso } })
  }

  function alternarMenu() {
    setMenuAberto(!menuAberto)
  }

  function fecharMenu() {
    setMenuAberto(false)
  }

  function fecharComEsc(evento) {
    if (menuAberto && evento.key === 'Escape') {
      setMenuAberto(false)
      document.getElementById('botao-menu').focus()
    }
  }

  if (!token) return <Navigate to="/entrar" replace state={{ destino: pathname + search }} />

  return (
    <div className={classes.layout}>
      <a className={classes.pular} href="#conteudo">Ir para o conteúdo</a>
      <aside className={classes.lateral} onKeyDown={fecharComEsc}>
        <div className={classes.cabecalhoMenu}>
          <Link to="/" className={classes.marca} onClick={fecharMenu} aria-label="CRIE — ir para o painel">
            <img src="/crie-logo-oficial.png" alt="CRIE" width="107" height="50" />
          </Link>
          <button type="button" id="botao-menu" className={classes.menu} aria-expanded={menuAberto}
            aria-controls="navegacao" onClick={alternarMenu}>
            {menuAberto ? <X size={19} aria-hidden="true" /> : <Menu size={19} aria-hidden="true" />} Menu
          </button>
        </div>
        <div id="navegacao" className={menuAberto ? classes.navegacaoAberta : classes.navegacao}>
          <nav aria-label="Navegação principal">
            {navegacao.filter(item => !item.direcao || usuario.perfil === 'direcao').map(({ rota, texto, icone: Icone }) => (
              <Link key={rota} to={rota} className={rotaAtual === rota ? classes.ativo : undefined}
                aria-current={rotaAtual === rota ? 'page' : undefined} onClick={fecharMenu}>
                <Icone size={20} strokeWidth={1.8} aria-hidden="true" /> {texto}
              </Link>
            ))}
          </nav>
        </div>
      </aside>
      <div className={classes.area}>
        <header className={classes.topo}>
          <div className={classes.usuario}>
            <span className={classes.avatar}><UserRound size={21} aria-hidden="true" /></span>
            <div><strong>Olá, {usuario.nome.split(' ')[0]}</strong><span>{perfis[usuario.perfil]}</span></div>
          </div>
          <div className={classes.fimTopo}>
            <div className={classes.data}><CalendarDays size={17} aria-hidden="true" />{dataCurta(hojeCrie())}</div>
            <button className={classes.sair} type="button" onClick={sair} disabled={saindo}>
              <LogOut size={19} aria-hidden="true" />{saindo ? 'Saindo…' : 'Sair'}
            </button>
          </div>
        </header>
        <main className={classes.conteudo} id="conteudo" tabIndex={-1}>
          {/* A chave faz cada endereço abrir a tela do zero, sem estado da tela anterior. */}
          <Outlet key={pathname + search} />
        </main>
      </div>
    </div>
  )
}
