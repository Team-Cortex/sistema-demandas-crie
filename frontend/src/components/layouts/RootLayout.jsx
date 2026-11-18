import { useState } from 'react'
import { Link, Navigate, Outlet, useLocation, useNavigate } from 'react-router-dom'
import cliente, { apagarSessao, lerSessao } from '../../api/cliente'
import { perfis } from '../../dominio'
import styles from './RootLayout.module.css'

const navegacao = [
  { rota: '/', texto: 'Painel' },
  { rota: '/minhas', texto: 'Minhas demandas' },
  { rota: '/demandas', texto: 'Demandas' },
  { rota: '/reunioes', texto: 'Reuniões' },
  { rota: '/assistidos', texto: 'Assistidos' },
  { rota: '/encaminhamentos', texto: 'Encaminhamentos' },
  { rota: '/usuarios', texto: 'Usuários', direcao: true },
  { rota: '/relatorios', texto: 'Relatórios', direcao: true },
  { rota: '/auditoria', texto: 'Auditoria', direcao: true },
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
    <div className={styles.layout}>
      <a className={styles.pular} href="#conteudo">Ir para o conteúdo</a>
      <aside className={styles.lateral} onKeyDown={fecharComEsc}>
        <div className={styles.cabecalhoMenu}>
          <Link to="/" className={styles.marca} onClick={fecharMenu} aria-label="CRIE, ir para o painel">
            <img src="/crie-logo-oficial.png" alt="CRIE" width="107" height="50" />
          </Link>
          <button type="button" id="botao-menu" className={styles.menu} aria-expanded={menuAberto}
            aria-controls="navegacao" onClick={alternarMenu}>
            {menuAberto ? 'Fechar menu' : 'Menu'}
          </button>
        </div>
        <nav id="navegacao" className={menuAberto ? styles.navegacaoAberta : styles.navegacao} aria-label="Navegação principal">
          {navegacao.filter(item => !item.direcao || usuario.perfil === 'direcao').map(({ rota, texto }) => (
            <Link key={rota} to={rota} className={rotaAtual === rota ? styles.ativo : undefined}
              aria-current={rotaAtual === rota ? 'page' : undefined} onClick={fecharMenu}>
              {texto}
            </Link>
          ))}
        </nav>
      </aside>
      <div className={styles.area}>
        <header className={styles.topo}>
          <p className={styles.usuario}>{usuario.nome} <span>({perfis[usuario.perfil]})</span></p>
          <button className="botao botao-secundario" type="button" onClick={sair} disabled={saindo}>
            {saindo ? 'Saindo…' : 'Sair'}
          </button>
        </header>
        <main className={styles.conteudo} id="conteudo" tabIndex={-1}>
          {/* A chave faz cada endereço abrir a tela do zero, sem estado da tela anterior. */}
          <Outlet key={pathname + search} />
        </main>
      </div>
    </div>
  )
}
