import { useEffect, useState } from 'react'
import { ArrowLeft, ChevronRight, Pencil, Plus } from 'lucide-react'
import { Link, useLocation, useParams } from 'react-router-dom'
import cliente, { mensagemDeErro } from '../../api/cliente'
import AvisoSucesso from '../../components/AvisoSucesso'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataCurta, estados, setores } from '../../dominio'
import styles from './Reunioes.module.css'

export default function FichaReuniao() {
  const { id } = useParams()
  const { state } = useLocation()
  const [reuniao, definirReuniao] = useState(null)
  const [erro, definirErro] = useState('')
  const [tentativa, definirTentativa] = useState(0)

  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/reunioes/' + id, { signal: controlador.signal })
      .then(({ data }) => definirReuniao(data))
      .catch(falha => { if (!controlador.signal.aborted) definirErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [id, tentativa])

  function tentarNovamente() {
    definirErro('')
    definirTentativa(tentativa + 1)
  }

  return (
    <div className={styles.pagina}>
      <Link to="/reunioes" className={styles.voltar}><ArrowLeft size={17} aria-hidden="true" />Reuniões</Link>
      <header className={styles.cabecalho}>
        <h1>{reuniao ? 'Reunião de ' + dataCurta(reuniao.data) : 'Reunião'}</h1>
        {reuniao && <Link to={'/reunioes/' + id + '/editar'} className="botao-secundario"><Pencil size={16} aria-hidden="true" />Editar reunião</Link>}
      </header>
      <AvisoSucesso>{state?.mensagem}</AvisoSucesso>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> :
        !reuniao ? <Carregando>Carregando reunião…</Carregando> :
        <>
          <dl className={styles.dados}>
            <div><dt>Setor</dt><dd>{setores[reuniao.setor]}</dd></div>
            <div><dt>Participantes</dt><dd>{reuniao.participantes.map(pessoa => pessoa.nome).join(', ')}</dd></div>
          </dl>
          <section className={styles.painel}>
            <div className={styles.cabecalho}>
              <h2>Demandas da reunião</h2>
              <Link className="botao-primario" to={'/demandas/nova?reuniao_id=' + id}><Plus size={18} aria-hidden="true" />Registrar demanda desta reunião</Link>
            </div>
            {reuniao.demandas.length ? <ul className={styles.lista}>{reuniao.demandas.map(demanda =>
              <li key={demanda.id}><Link className={styles.linha} to={'/demandas/' + demanda.id}>
                <span><strong>{demanda.descricao}</strong><span className={styles.estado} data-estado={demanda.estado}>{estados[demanda.estado]}</span></span>
                <ChevronRight size={18} aria-hidden="true" />
              </Link></li>)}</ul> : <p>Nenhuma demanda registrada nesta reunião.</p>}
          </section>
        </>}
    </div>
  )
}
