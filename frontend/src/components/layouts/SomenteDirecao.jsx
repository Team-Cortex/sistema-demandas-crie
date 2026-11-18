import { Link, Outlet, useLocation } from 'react-router-dom'
import { lerSessao } from '../../api/cliente'

const permissoes = {
  usuarios: 'Só a direção gerencia usuários.',
  relatorios: 'Só a direção emite relatórios.',
  auditoria: 'Só a direção consulta a auditoria.',
}

export default function SomenteDirecao() {
  const { pathname } = useLocation()
  if (lerSessao().usuario?.perfil === 'direcao') return <Outlet />
  return (
    <section>
      <h1>Acesso restrito</h1>
      <p role="alert" className="aviso-erro">{permissoes[pathname.split('/')[1]]}</p>
      <Link className="botao-secundario" to="/">Voltar ao painel</Link>
    </section>
  )
}
