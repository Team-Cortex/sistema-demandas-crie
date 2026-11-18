import { useEffect, useState } from 'react'
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
  const [reuniao, setReuniao] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)

  useEffect(() => {
    async function buscarReuniao() {
      try {
        const resposta = await cliente.get('/api/reunioes/' + id)
        setReuniao(resposta.data)
      } catch (falha) {
        setErro(mensagemDeErro(falha))
      }
    }
    buscarReuniao()
  }, [id, tentativa])

  function tentarNovamente() {
    setErro('')
    setTentativa(tentativa + 1)
  }

  return (
    <div className={styles.pagina}>
      <Link to="/reunioes" className="voltar">Voltar para reuniões</Link>
      <header className={styles.cabecalho}>
        <h1>{reuniao ? 'Reunião de ' + dataCurta(reuniao.data) : 'Reunião'}</h1>
        {reuniao && <Link to={'/reunioes/' + id + '/editar'} className="botao-secundario">Editar reunião</Link>}
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
              <Link className="botao-primario" to={'/demandas/nova?reuniao_id=' + id}>Registrar demanda desta reunião</Link>
            </div>
            {reuniao.demandas.length ? <ul className={styles.lista}>{reuniao.demandas.map(demanda =>
              <li key={demanda.id}><Link className={styles.linha} to={'/demandas/' + demanda.id}>
                <strong>{demanda.descricao}</strong><small>Estado: {estados[demanda.estado]}</small>
              </Link></li>)}</ul> : <p>Nenhuma demanda registrada nesta reunião.</p>}
          </section>
        </>}
    </div>
  )
}
