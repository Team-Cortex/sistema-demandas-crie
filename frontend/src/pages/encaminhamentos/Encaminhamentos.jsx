import { useEffect, useState } from 'react'
import { Link, useLocation, useSearchParams } from 'react-router-dom'
import cliente, { mensagemDeErro } from '../../api/cliente'
import { dataCurta, dataHora } from '../../dominio'
import Carregando from '../../components/Carregando'
import AvisoSucesso from '../../components/AvisoSucesso'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Encaminhamentos.module.css'

export default function Encaminhamentos() {
  const { state } = useLocation()
  const [parametros] = useSearchParams()
  const todos = parametros.get('lista') === 'todos'
  const [resultado, setResultado] = useState(null)
  const [tentativa, setTentativa] = useState(0)
  const dados = resultado?.todos === todos ? resultado : null

  useEffect(() => {
    const controle = new AbortController()
    cliente.get('/api/encaminhamentos' + (todos ? '' : '/pendentes'), { signal: controle.signal })
      .then(({ data }) => setResultado({ todos, itens: data }))
      .catch(erro => { if (!controle.signal.aborted) setResultado({ todos, erro: mensagemDeErro(erro) }) })
    return () => controle.abort()
  }, [todos, tentativa])

  function tentarNovamente() {
    setResultado(null)
    setTentativa(tentativa + 1)
  }

  return (
    <div className={styles.pagina}>
      <h1>Encaminhamentos</h1>
      <AvisoSucesso>{state?.mensagem}</AvisoSucesso>
      <nav className={styles.abas} aria-label="Listas de encaminhamentos">
        <Link to="/encaminhamentos" aria-current={!todos ? 'page' : undefined}>Pendentes</Link>
        <Link to="?lista=todos" aria-current={todos ? 'page' : undefined}>Todos</Link>
      </nav>
      {!dados ? <Carregando /> : dados.erro ? <ErroConsulta mensagem={dados.erro} tentarNovamente={tentarNovamente} />
        : !dados.itens.length ? <p className={styles.ficha}>{todos ? 'Nenhum encaminhamento registrado. Abra a demanda ou a ficha do assistido para encaminhar.' : 'Nenhum encaminhamento pendente. Consulte Todos para ver os desfechos registrados.'}</p>
        : <ul className={styles.lista}>{dados.itens.map(item =>
          <li key={item.id} className={styles.ficha}>
            <div className={styles.topo}><h2>{item.destino}</h2><span className={styles.situacao}>{item.pendente ? 'Pendente' : 'Com desfecho'}</span></div>
            <p>{dataCurta(item.data)} · {item.responsavel_nome}</p>
            <div className={styles.vinculos}>
              {item.demanda_id && <Link to={'/demandas/' + item.demanda_id}>Demanda nº {item.demanda_id}</Link>}
              {item.assistido_id && <Link to={'/assistidos/' + item.assistido_id}>Assistido nº {item.assistido_id}</Link>}
            </div>
            {item.observacao && <p className={styles.texto}><strong>Observação</strong>{item.observacao}</p>}
            {item.pendente
              ? <Link className="botao-secundario" to={'/encaminhamentos/' + item.id + '/desfecho'}>Registrar desfecho</Link>
              : <p className={styles.texto}><strong>Desfecho · {dataHora(item.desfecho_em)}</strong>{item.desfecho}</p>}
          </li>)}</ul>}
    </div>
  )
}
