import { Link, isRouteErrorResponse, useRouteError } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { lerSessao } from '../api/cliente'
import classes from './ErrorPage.module.css'

export default function ErrorPage() {
  const erro = useRouteError()
  const sessao = lerSessao()
  const inexistente = isRouteErrorResponse(erro) && erro.status === 404
  return (
    <main className={classes.tela}>
      <section className={classes.cartao}>
        <img src="/crie-logo-oficial.png" alt="CRIE" width="107" height="50" />
        <h1>{inexistente ? 'Página não encontrada' : 'Não foi possível abrir esta página'}</h1>
        <p>{inexistente ? 'Confira o endereço ou use o botão abaixo para continuar.' : 'Volte ao sistema e tente abrir a página novamente.'}</p>
        <Link className="botao-primario" to={sessao.token ? '/' : '/entrar'}>
          <ArrowLeft size={18} aria-hidden="true" />{sessao.token ? 'Voltar ao painel' : 'Ir para entrar'}
        </Link>
      </section>
    </main>
  )
}
