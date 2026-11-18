import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataCurta, dataHora } from '../../dominio'
import styles from '../assistidos/Assistidos.module.css'

const vazio = { de: '', ate: '', area_atuacao: '' }

export default function EvolucoesAssistido({ assistidoId, iniciais }) {
  const chave = 'filtros-evolucoes-' + assistidoId
  const [campos, setCampos] = useState(() => lerRascunho(chave)?.campos || vazio)
  const [consulta, setConsulta] = useState(() => lerRascunho(chave)?.consulta || null)
  const [resultados, setResultados] = useState(null)
  const [erro, setErro] = useState('')
  const [erroPeriodo, setErroPeriodo] = useState('')
  const evolucoes = consulta ? resultados : iniciais

  useEffect(() => {
    if (!consulta) return
    const controlador = new AbortController()
    cliente.get('/api/assistidos/' + assistidoId + '/evolucoes', { params: consulta, signal: controlador.signal })
      .then(({ data }) => setResultados(data))
      .catch(falha => { if (!controlador.signal.aborted) setErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [consulta, assistidoId])

  function preencher(evento) {
    const atual = { ...campos, [evento.target.name]: evento.target.value }
    setCampos(atual)
    guardarRascunho(chave, { campos: atual, consulta })
    setErroPeriodo('')
  }

  function filtrar(evento) {
    evento.preventDefault()
    if (campos.de && campos.ate && campos.ate < campos.de) {
      setErroPeriodo('Informe uma data final igual ou posterior à inicial.')
      evento.currentTarget.elements.ate.focus()
      return
    }
    const params = Object.fromEntries(Object.entries(campos).filter(([, valor]) => valor.trim()))
    if (params.area_atuacao) params.area_atuacao = params.area_atuacao.trim()
    const aplicados = Object.keys(params).length ? params : null
    setErro('')
    setResultados(null)
    setConsulta(aplicados)
    guardarRascunho(chave, { campos, consulta: aplicados })
  }

  function limpar() {
    apagarRascunho(chave)
    setConsulta(null)
    setCampos(vazio)
    setErroPeriodo('')
    setErro('')
  }

  function tentarNovamente() { setErro(''); setConsulta({ ...consulta }) }

  return (
    <section className={styles.painel}>
      <div className={styles.cabecalho}><h2>Evoluções</h2>
        <Link className="botao-primario" to={'/assistidos/' + assistidoId + '/evolucoes/nova'}>Lançar evolução</Link>
      </div>
      <form className={styles.pesquisa} onSubmit={filtrar}>
        <label>De<input name="de" type="date" value={campos.de} onChange={preencher} /></label>
        <label>Até<input name="ate" type="date" value={campos.ate} onChange={preencher} aria-invalid={Boolean(erroPeriodo)} aria-describedby={erroPeriodo ? 'erro-periodo' : undefined} /></label>
        <label>Área de atuação<input name="area_atuacao" value={campos.area_atuacao} onChange={preencher} maxLength={80} /></label>
        <button className="botao-secundario">Filtrar evoluções</button>
        {(consulta || Object.values(campos).some(Boolean)) && <button type="button" className="botao-secundario" onClick={limpar}>Limpar filtros</button>}
        {erroPeriodo && <p role="alert" className={styles.erro} id="erro-periodo">{erroPeriodo}</p>}
      </form>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> : !evolucoes ? <Carregando /> :
        evolucoes.length ? <ul className={styles.lista}>{evolucoes.map(item => <li key={item.id}>
          <Link className={styles.link} to={'/evolucoes/' + item.id}>{dataCurta(item.data)} — {item.area_atuacao}</Link>
          <p className={styles.texto}>{item.descricao}</p>
          <p className={styles.secundario}>{item.autor_nome} · {dataHora(item.ocorrido_em)}</p>
        </li>)}</ul> : <p>{consulta ? 'Nenhuma evolução encontrada com esses filtros. Tente ampliar o período ou limpar os filtros.' : 'Nenhuma evolução lançada para este assistido.'}</p>}
    </section>
  )
}
