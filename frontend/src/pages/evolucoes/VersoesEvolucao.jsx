import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import cliente, { mensagemDeErro } from '../../api/cliente'
import AvisoSucesso from '../../components/AvisoSucesso'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataCurta, dataHora } from '../../dominio'
import styles from '../assistidos/Assistidos.module.css'

export default function VersoesEvolucao() {
  const { id } = useParams()
  const { state } = useLocation()
  const [evolucao, setEvolucao] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/evolucoes/' + id, { signal: controlador.signal }).then(({ data }) => setEvolucao(data))
      .catch(falha => { if (!controlador.signal.aborted) setErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [id, tentativa])
  function tentarNovamente() { setErro(''); setTentativa(tentativa + 1) }

  return (
    <div className={styles.pagina}>
      <Link className={styles.voltar} to={evolucao ? '/assistidos/' + evolucao.assistido_id : '/assistidos'}><ArrowLeft size={17} aria-hidden="true" />{evolucao ? 'Ficha do assistido' : 'Assistidos'}</Link>
      <header className={styles.cabecalho}><h1>Versões da evolução</h1>
        {evolucao?.vigente && <Link className="botao-primario" to={'/evolucoes/' + id + '/retificar'}>Retificar</Link>}
      </header>
      <AvisoSucesso>{state?.mensagem}</AvisoSucesso>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> : !evolucao ? <Carregando /> : <>
        {evolucao.retificada_por_id && <Link className={styles.link} to={'/evolucoes/' + evolucao.retificada_por_id}>Ver versão seguinte</Link>}
        {[evolucao, ...evolucao.versoes_anteriores].map(item => <article key={item.id} className={styles.painel}>
          <h2>{item.vigente ? 'Versão vigente' : 'Versão anterior'}</h2>
          <p><strong>{item.area_atuacao}</strong> · {dataCurta(item.data)}</p>
          <p className={styles.texto}>{item.descricao}</p>
          <p className={styles.secundario}>Registrada por {item.autor_nome} em {dataHora(item.ocorrido_em)}</p>
        </article>)}
        {!evolucao.versoes_anteriores.length && <p className={styles.secundario}>Esta é a versão original.</p>}
      </>}
    </div>
  )
}
