import { useEffect, useState } from 'react'
import cliente from '../../api/cliente'
import { estados } from '../../dominio'
import ErroConsulta from '../../components/ErroConsulta'
import Carregando from '../../components/Carregando'
import CampoDemanda from '../../components/CampoDemanda'
import ResultadoRelatorio from './ResultadoRelatorio'
import styles from './Relatorios.module.css'

const inicial = { tipo: 'demandas', de: '', ate: '', estado: '', categoria: '', responsavel_id: '', assistido_id: '' }

export default function Relatorios() {
  const [campos, setCampos] = useState({ ...inicial, ...cliente.lerRascunho('relatorios') })
  const [opcoes, setOpcoes] = useState(null)
  const [erroOpcoes, setErroOpcoes] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [relatorio, setRelatorio] = useState(null)
  const [erro, setErro] = useState('')
  const [errosCampos, setErrosCampos] = useState({})
  const [emitindo, setEmitindo] = useState(false)

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
  }, [tentativa])

  function repetirConsulta() {
    setErroOpcoes('')
    setTentativa(tentativa + 1)
  }

  function alterarCampo(evento) {
    const valores = { ...campos, [evento.target.name]: evento.target.value }
    setCampos(valores)
    cliente.guardarRascunho('relatorios', valores)
    setErro('')
    setErrosCampos({})
    setRelatorio(null)
  }

  async function emitirRelatorio(evento) {
    evento.preventDefault()
    const falhas = {}
    if (!campos.de) falhas.de = 'Informe a data inicial.'
    if (!campos.ate) falhas.ate = 'Informe a data final.'
    else if (campos.ate < campos.de) falhas.ate = 'Escolha uma data final igual ou posterior à inicial.'
    if (campos.tipo === 'assistido' && !campos.assistido_id) falhas.assistido_id = 'Selecione um assistido.'
    setErrosCampos(falhas)
    const primeiro = Object.keys(falhas)[0]
    if (primeiro) {
      evento.currentTarget.elements[primeiro].focus()
      return
    }
    setErro('')
    setRelatorio(null)
    setEmitindo(true)
    const params = { de: campos.de, ate: campos.ate }
    let caminho = '/api/relatorios/demandas'
    if (campos.tipo === 'demandas') {
      for (const nome of ['estado', 'categoria', 'responsavel_id']) {
        if (campos[nome].trim()) params[nome] = campos[nome].trim()
      }
    } else {
      caminho = '/api/relatorios/assistidos/' + campos.assistido_id
    }
    try {
      const resposta = await cliente.get(caminho, { params })
      setRelatorio(resposta.data)
    } catch (falha) {
      setErro(cliente.mensagemDeErro(falha))
    } finally {
      setEmitindo(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <h1>Relatórios</h1>
      <form onSubmit={emitirRelatorio} className={styles.formulario} noValidate>
        <fieldset disabled={emitindo}>
          <legend>Emitir relatório</legend>
          <label className={styles.inteira}>Tipo de relatório
            <select name="tipo" value={campos.tipo} onChange={alterarCampo}>
              <option value="demandas">Demandas do período</option>
              <option value="assistido">Acompanhamento do assistido</option>
            </select>
          </label>
          {[['de', 'De'], ['ate', 'Até']].map(([nome, rotulo]) => (
            <CampoDemanda key={nome} nome={nome} rotulo={rotulo} erro={errosCampos[nome]}>
              <input id={nome} type="date" required name={nome} value={campos[nome]} onChange={alterarCampo}
                aria-invalid={Boolean(errosCampos[nome])} aria-describedby={errosCampos[nome] ? nome + '-erro' : undefined} />
            </CampoDemanda>
          ))}
          {campos.tipo === 'demandas' ? <>
            <label>Estado<select name="estado" value={campos.estado} onChange={alterarCampo}>
              <option value="">Todos os estados</option>
              {Object.entries(estados).map(([valor, nome]) => <option key={valor} value={valor}>{nome}</option>)}
            </select></label>
            <label>Categoria<input name="categoria" maxLength={80} value={campos.categoria} onChange={alterarCampo} /></label>
            <label className={styles.inteira}>Responsável
              <select name="responsavel_id" value={campos.responsavel_id} onChange={alterarCampo} disabled={!opcoes}>
                <option value="">Todos os responsáveis</option>
                {opcoes?.usuarios.map(pessoa => <option key={pessoa.id} value={pessoa.id}>{pessoa.nome}</option>)}
              </select>
            </label>
          </> : <div className={styles.inteira}><CampoDemanda nome="assistido_id" rotulo="Assistido" erro={errosCampos.assistido_id}>
            <select id="assistido_id" name="assistido_id" required value={campos.assistido_id} onChange={alterarCampo} disabled={!opcoes}
              aria-invalid={Boolean(errosCampos.assistido_id)} aria-describedby={errosCampos.assistido_id ? 'assistido_id-erro' : undefined}>
              <option value="">Selecione o assistido</option>
              {opcoes?.assistidos.map(pessoa => <option key={pessoa.id} value={pessoa.id}>{pessoa.nome_tratamento}</option>)}
            </select>
          </CampoDemanda></div>}
        </fieldset>
        {erroOpcoes ? <ErroConsulta mensagem={erroOpcoes} tentarNovamente={repetirConsulta} /> :
          !opcoes && <Carregando>Carregando opções do relatório…</Carregando>}
        {campos.tipo === 'assistido' && opcoes?.assistidos.length === 0 && <p role="status">Nenhum assistido cadastrado.</p>}
        {erro && <p role="alert" className="aviso-erro">{erro}</p>}
        <button className="botao-primario" disabled={emitindo || !opcoes || (campos.tipo === 'assistido' && !opcoes.assistidos.length)}>
          {emitindo ? 'Emitindo…' : erro ? 'Tentar de novo' : 'Emitir relatório'}
        </button>
      </form>
      {emitindo && <Carregando>Preparando o relatório…</Carregando>}
      {relatorio && <ResultadoRelatorio relatorio={relatorio} usuarios={opcoes.usuarios} />}
    </div>
  )
}
