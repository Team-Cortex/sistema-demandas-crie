import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import cliente from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataCurta, dataHora } from '../../dominio'
import styles from '../assistidos/Assistidos.module.css'

const vazio = { de: '', ate: '', area_atuacao: '' }

// Só os filtros preenchidos vão para a API; sem nenhum, vale a lista que veio com a ficha.
function preenchidos(campos) {
  const parametros = {}
  for (const nome in campos) {
    if (campos[nome].trim()) parametros[nome] = campos[nome].trim()
  }
  return Object.keys(parametros).length ? parametros : null
}

export default function EvolucoesAssistido({ assistidoId, iniciais }) {
  // Os filtros aplicados ficam no rascunho para voltarem depois que a sessão é renovada.
  const chave = 'evolucoes-' + assistidoId
  const [campos, setCampos] = useState(cliente.lerRascunho(chave) || vazio)
  const [consulta, setConsulta] = useState(preenchidos(campos))
  const [resultados, setResultados] = useState(null)
  const [erro, setErro] = useState('')
  const [erroPeriodo, setErroPeriodo] = useState('')
  const evolucoes = consulta ? resultados : iniciais

  useEffect(() => {
    async function buscarEvolucoes() {
      try {
        const resposta = await cliente.get('/api/assistidos/' + assistidoId + '/evolucoes', { params: consulta })
        setResultados(resposta.data)
      } catch (falha) {
        setErro(cliente.mensagemDeErro(falha))
      }
    }
    if (consulta) buscarEvolucoes()
  }, [consulta, assistidoId])

  function preencher(evento) {
    setCampos({ ...campos, [evento.target.name]: evento.target.value })
    setErroPeriodo('')
  }

  function filtrar(evento) {
    evento.preventDefault()
    if (campos.de && campos.ate && campos.ate < campos.de) {
      setErroPeriodo('Informe uma data final igual ou posterior à inicial.')
      evento.currentTarget.elements.ate.focus()
      return
    }
    setErro('')
    setResultados(null)
    setConsulta(preenchidos(campos))
    cliente.guardarRascunho(chave, campos)
  }

  function limpar() {
    cliente.apagarRascunho(chave)
    setConsulta(null)
    setCampos(vazio)
    setErroPeriodo('')
    setErro('')
  }

  // Um objeto novo, mesmo igual, faz o useEffect buscar de novo.
  function tentarNovamente() {
    setErro('')
    setConsulta({ ...consulta })
  }

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
          <Link className={styles.link} to={'/evolucoes/' + item.id}>{dataCurta(item.data)}, {item.area_atuacao}</Link>
          <p className={styles.texto}>{item.descricao}</p>
          <p className={styles.secundario}>Registrada por {item.autor_nome} em {dataHora(item.ocorrido_em)}</p>
        </li>)}</ul> : <p>{consulta ? 'Nenhuma evolução encontrada com esses filtros. Tente ampliar o período ou limpar os filtros.' : 'Nenhuma evolução lançada para este assistido.'}</p>}
    </section>
  )
}
