import { useEffect, useState } from 'react'
import cliente from '../api/cliente'
import Carregando from '../components/Carregando'
import CabecalhoDemandas from '../components/CabecalhoDemandas'
import ErroConsulta from '../components/ErroConsulta'
import ListaDemandas from '../components/ListaDemandas'
import Demanda from '../modelos/Demanda'
import { estados } from '../dominio'
import styles from './Demandas.module.css'

const filtrosVazios = { q: '', estado: '', responsavel_id: '', categoria: '', periodo_inicio: '', periodo_fim: '', assistido_id: '' }

// Só os filtros preenchidos vão para a API.
function preenchidos(filtros) {
  const parametros = {}
  for (const campo in filtros) {
    if (filtros[campo].trim()) parametros[campo] = filtros[campo].trim()
  }
  return parametros
}

export default function Demandas() {
  // Os filtros ficam no rascunho para voltarem depois que a sessão é renovada.
  const [filtros, setFiltros] = useState(cliente.lerRascunho('filtros-demandas') || filtrosVazios)
  const [consulta, setConsulta] = useState(preenchidos(filtros))
  const [demandas, setDemandas] = useState(null)
  const [erro, setErro] = useState('')
  const [opcoes, setOpcoes] = useState(null)
  const [erroOpcoes, setErroOpcoes] = useState('')
  const [tentativaOpcoes, setTentativaOpcoes] = useState(0)
  const [erroPeriodo, setErroPeriodo] = useState('')
  const [maisFiltros, setMaisFiltros] = useState(
    Boolean(filtros.responsavel_id || filtros.categoria || filtros.periodo_inicio || filtros.periodo_fim || filtros.assistido_id))

  useEffect(() => {
    async function buscarOpcoes() {
      try {
        const usuarios = await cliente.get('/api/usuarios')
        const assistidos = await cliente.get('/api/assistidos')
        setOpcoes({ usuarios: usuarios.data, assistidos: assistidos.data })
      } catch (falha) {
        setErroOpcoes(cliente.mensagemDeErro(falha))
      }
    }
    buscarOpcoes()
  }, [tentativaOpcoes])

  // Busca de novo sempre que a consulta muda (Buscar, Limpar ou Tentar de novo).
  useEffect(() => {
    async function buscarDemandas() {
      try {
        const resposta = await cliente.get('/api/demandas', { params: consulta })
        setDemandas(resposta.data.map(dados => new Demanda(dados)))
      } catch (falha) {
        setErro(cliente.mensagemDeErro(falha))
      }
    }
    buscarDemandas()
  }, [consulta])

  function alterarFiltro(evento) {
    setFiltros({ ...filtros, [evento.target.name]: evento.target.value })
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
    cliente.guardarRascunho('filtros-demandas', filtros)
    consultar(preenchidos(filtros))
  }

  function limparFiltros() {
    setFiltros(filtrosVazios)
    cliente.apagarRascunho('filtros-demandas')
    setErroPeriodo('')
    consultar({})
  }

  // Um objeto novo, mesmo igual, faz o useEffect buscar de novo.
  function tentarNovamente() {
    consultar({ ...consulta })
  }

  function tentarOpcoes() {
    setErroOpcoes('')
    setTentativaOpcoes(tentativaOpcoes + 1)
  }

  function alternarFiltros() {
    setMaisFiltros(!maisFiltros)
  }

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
            {maisFiltros ? 'Menos filtros' : 'Mais filtros'}
          </button>
        </div>
        <div id="mais-filtros" hidden={!maisFiltros}>
          {!opcoes && !erroOpcoes && <Carregando>Carregando responsáveis e assistidos…</Carregando>}
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
          <button type="submit" className="botao botao-primario">Buscar</button>
          {Object.values(filtros).some(Boolean) || Object.keys(consulta).length > 0
            ? <button type="button" className={styles.limpar} onClick={limparFiltros}>Limpar filtros</button>
            : null}
        </div>
      </form>
      {erro && <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} />}
      {!erro && !demandas && <Carregando>Carregando demandas…</Carregando>}
      {demandas && (
        <section>
          <h2 className={styles.tituloResultados}>Resultado da busca ({demandas.length})</h2>
          <ListaDemandas demandas={demandas} titulo="Resultado da busca" mensagemVazia="Nenhuma demanda encontrada. Tente outra busca ou altere os filtros." />
        </section>
      )}
    </>
  )
}
