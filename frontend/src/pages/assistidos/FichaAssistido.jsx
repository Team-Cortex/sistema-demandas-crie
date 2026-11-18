import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { ArrowLeft, Pencil } from 'lucide-react'
import cliente, { mensagemDeErro } from '../../api/cliente'
import { dataCurta } from '../../dominio'
import AvisoSucesso from '../../components/AvisoSucesso'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import ListaDemandas from '../../components/ListaDemandas'
import EvolucoesAssistido from '../evolucoes/EvolucoesAssistido'
import styles from './Assistidos.module.css'

export default function FichaAssistido() {
  const { id } = useParams()
  const { state } = useLocation()
  const [ficha, setFicha] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/assistidos/' + id + '/ficha', { signal: controlador.signal }).then(({ data }) => setFicha(data))
      .catch(falha => { if (!controlador.signal.aborted) setErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [id, tentativa])
  function tentarNovamente() { setErro(''); setTentativa(tentativa + 1) }

  return (
    <div className={styles.pagina}>
      <Link className={styles.voltar} to="/assistidos"><ArrowLeft size={17} aria-hidden="true" />Assistidos</Link>
      <div className={styles.cabecalho}><h1>{ficha ? ficha.assistido.nome_tratamento : 'Ficha do assistido'}</h1>
        {ficha && <Link className="botao-secundario" to={'/assistidos/' + id + '/editar'}><Pencil size={16} aria-hidden="true" />Editar nome</Link>}
      </div>
      <AvisoSucesso>{state?.mensagem}</AvisoSucesso>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> : !ficha ? <Carregando /> : <>
        {ficha.profissionais.length > 0 && <p>Profissionais que acompanham: {ficha.profissionais.map(item => item.nome).join(', ')}</p>}
        <section className={styles.painel}>
          <h2>Demandas</h2>
          <ListaDemandas demandas={ficha.demandas} titulo="Demandas do assistido" mensagemVazia="Nenhuma demanda vinculada a este assistido." />
        </section>
        <EvolucoesAssistido assistidoId={id} iniciais={ficha.evolucoes} />
        <section className={styles.painel}>
          <div className={styles.cabecalho}><h2>Encaminhamentos</h2>
            <Link className="botao-secundario" to={'/encaminhamentos/novo?assistido_id=' + id}>Encaminhar</Link>
          </div>
          {ficha.encaminhamentos.length ? <ul className={styles.lista}>{ficha.encaminhamentos.map(item => <li key={item.id}>
            <strong>{item.destino}</strong><p>{dataCurta(item.data)} · {item.responsavel_nome}</p>
            {item.pendente ? <Link className={styles.link} to={'/encaminhamentos/' + item.id + '/desfecho'}>Registrar desfecho</Link> :
              <p className={styles.texto}>Desfecho: {item.desfecho}</p>}
          </li>)}</ul> : <p>Nenhum encaminhamento registrado para este assistido.</p>}
        </section>
      </>}
    </div>
  )
}
