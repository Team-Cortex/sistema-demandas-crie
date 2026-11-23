import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import cliente from '../../api/cliente'
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
    async function buscarFicha() {
      try {
        const resposta = await cliente.get('/api/assistidos/' + id + '/ficha')
        setFicha(resposta.data)
      } catch (falha) {
        setErro(cliente.mensagemDeErro(falha))
      }
    }
    buscarFicha()
  }, [id, tentativa])

  function tentarNovamente() {
    setErro('')
    setTentativa(tentativa + 1)
  }

  return (
    <div className={styles.pagina}>
      <Link className="voltar" to="/assistidos">Voltar para assistidos</Link>
      <div className={styles.cabecalho}><h1>{ficha ? ficha.assistido.nome_tratamento : 'Ficha do assistido'}</h1>
        {ficha && <Link className="botao-secundario" to={'/assistidos/' + id + '/editar'}>Editar nome</Link>}
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
            <strong>{item.destino}</strong><p>Em {dataCurta(item.data)}, por {item.responsavel_nome}</p>
            {item.pendente ? <Link className={styles.link} to={'/encaminhamentos/' + item.id + '/desfecho'}>Registrar desfecho</Link> :
              <p className={styles.texto}>Desfecho: {item.desfecho}</p>}
          </li>)}</ul> : <p>Nenhum encaminhamento registrado para este assistido.</p>}
        </section>
      </>}
    </div>
  )
}
