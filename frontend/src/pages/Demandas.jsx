import { useEffect, useState } from 'react'
import { ListFilter, Search } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../api/cliente'
import CabecalhoDemandas from '../components/CabecalhoDemandas'
import ErroConsulta from '../components/ErroConsulta'
import ListaDemandas from '../components/ListaDemandas'
import { estados } from '../dominio'
import styles from './Demandas.module.css'

const filtrosVazios = { q: '', estado: '', responsavel_id: '', categoria: '', periodo_inicio: '', periodo_fim: '', assistido_id: '' }

export default function Demandas() {
  const [filtros, setFiltros] = useState(() => lerRascunho('filtros-demandas') || filtrosVazios)
  const [consulta, setConsulta] = useState(() => lerRascunho('filtros-aplicados') || {})
  const [demandas, setDemandas] = useState(null)
  const [erro, setErro] = useState('')
  const [opcoes, setOpcoes] = useState(null)
  const [erroOpcoes, setErroOpcoes] = useState('')
  const [tentativaOpcoes, setTentativaOpcoes] = useState(0)
  const [erroPeriodo, setErroPeriodo] = useState('')
  const [maisFiltros, setMaisFiltros] = useState(() =>
    Boolean(filtros.responsavel_id || filtros.categoria || filtros.periodo_inicio || filtros.periodo_fim || filtros.assistido_id))

  useEffect(() => {
    const controlador = new AbortController()
    Promise.all([
      cliente.get('/api/usuarios', { signal: controlador.signal }),
      cliente.get('/api/assistidos', { signal: controlador.signal }),
    ])
      .then(([usuarios, assistidos]) => setOpcoes({ usuarios: usuarios.data, assistidos: assistidos.data }))
      .catch(falha => { if (!controlador.signal.aborted) setErroOpcoes(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [tentativaOpcoes])

  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/demandas', { params: consulta, signal: controlador.signal })
      .then(resposta => setDemandas(resposta.data))
      .catch(falha => { if (!controlador.signal.aborted) setErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [consulta])

  function alterarFiltro(evento) {
    const novosFiltros = { ...filtros, [evento.target.name]: evento.target.value }
    setFiltros(novosFiltros)
    guardarRascunho('filtros-demandas', novosFiltros)
    setErroPeriodo('')
  }

  function consultar(parametros) {
    setErro('')
    setDemandas(null)
    setConsulta(parametros)
  }

  function aplicarFiltros(evento) {
    evento.preventDefault()
    if (filtros.periodo_inicio && filtros.periodo_fim && filtros.periodo_fim < filtros.periodo_inicio) {
      setMaisFiltros(true)
      setErroPeriodo('Escolha uma data final igual ou posterior à inicial.')
      return
    }
    const parametros = {}
    for (const [campo, valor] of Object.entries(filtros)) {
      if (valor.trim()) parametros[campo] = valor.trim()
    }
    guardarRascunho('filtros-aplicados', parametros)
    consultar(parametros)
  }

  function limparFiltros() {
    setFiltros(filtrosVazios)
    apagarRascunho('filtros-demandas')
    apagarRascunho('filtros-aplicados')
    setErroPeriodo('')
    consultar({})
  }

  function tentarNovamente() { consultar({ ...consulta }) }
  function tentarOpcoes() {
    setErroOpcoes('')
    setTentativaOpcoes(tentativaOpcoes + 1)
  }
  function alternarFiltros() { setMaisFiltros(!maisFiltros) }

  return (
    <>
      <CabecalhoDemandas titulo="Demandas" />
      <form className={styles.filtros} onSubmit={aplicarFiltros} aria-label="Buscar e filtrar demandas">
        <div className={styles.linhaBusca}>
          <label htmlFor="busca-demanda">Buscar na descrição
            <input id="busca-demanda" name="q" type="search" value={filtros.q} onChange={alterarFiltro} />
          </label>
          <label htmlFor="filtro-estado">Estado
            <select id="filtro-estado" name="estado" value={filtros.estado} onChange={alterarFiltro}>
              <option value="">Qualquer estado</option>
              {Object.entries(estados).map(([valor, texto]) => <option key={valor} value={valor}>{texto}</option>)}
            </select>
          </label>
          <button type="button" className="botao botao-secundario" onClick={alternarFiltros} aria-controls="mais-filtros" aria-expanded={maisFiltros}>
            <ListFilter size={17} aria-hidden="true" /> Mais filtros
          </button>
        </div>
        <div id="mais-filtros" hidden={!maisFiltros}>
          {!opcoes && !erroOpcoes && <p role="status">Carregando responsáveis e assistidos…</p>}
          {erroOpcoes && <ErroConsulta mensagem={erroOpcoes} tentarNovamente={tentarOpcoes} />}
          <div className={styles.campos}>
            <label htmlFor="filtro-responsavel">Responsável
              <select disabled={!opcoes} name="responsavel_id" id="filtro-responsavel" value={filtros.responsavel_id} onChange={alterarFiltro}>
                <option value="">Qualquer responsável</option>
                {opcoes?.usuarios.map(usuario => <option key={usuario.id} value={usuario.id}>{usuario.nome}</option>)}
              </select>
            </label>
            <label htmlFor="filtro-assistido">Assistido
              <select disabled={!opcoes} name="assistido_id" id="filtro-assistido" value={filtros.assistido_id} onChange={alterarFiltro}>
                <option value="">Qualquer assistido</option>
                {opcoes?.assistidos.map(assistido => <option key={assistido.id} value={assistido.id}>{assistido.nome_tratamento}</option>)}
              </select>
            </label>
            <label htmlFor="filtro-categoria">Categoria
              <input name="categoria" id="filtro-categoria" value={filtros.categoria} onChange={alterarFiltro} maxLength={80} />
            </label>
            <label htmlFor="filtro-inicio">Registrada de
              <input name="periodo_inicio" id="filtro-inicio" type="date" value={filtros.periodo_inicio} onChange={alterarFiltro} />
            </label>
            <label htmlFor="filtro-fim">Registrada até
              <input name="periodo_fim" id="filtro-fim" type="date" value={filtros.periodo_fim} onChange={alterarFiltro} aria-invalid={!!erroPeriodo} aria-describedby={erroPeriodo ? 'erro-periodo' : undefined} />
            </label>
          </div>
          {erroPeriodo && <p id="erro-periodo" className="aviso-erro" role="alert">{erroPeriodo}</p>}
        </div>
        <div className={styles.acoes}>
          <button type="submit" className="botao botao-secundario"><Search size={17} aria-hidden="true" /> Buscar</button>
          {Object.values(filtros).some(Boolean) || Object.keys(consulta).length > 0
            ? <button type="button" className={styles.limpar} onClick={limparFiltros}>Limpar filtros</button>
            : null}
        </div>
      </form>
      {erro && <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} />}
      {!erro && !demandas && <p role="status">Carregando demandas…</p>}
      {demandas && (
        <section>
          <h2 className={styles.tituloResultados}>Resultado da busca <span>{demandas.length}</span></h2>
          <ListaDemandas demandas={demandas} titulo="Resultado da busca" mensagemVazia="Nenhuma demanda encontrada. Tente outra busca ou altere os filtros." />
        </section>
      )}
    </>
  )
}
