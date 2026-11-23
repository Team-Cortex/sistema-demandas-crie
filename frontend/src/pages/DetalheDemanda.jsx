import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import cliente from '../api/cliente'
import { estados, setores, dataCurta, dataHora } from '../dominio'
import AvisoSucesso from '../components/AvisoSucesso'
import Confirmacao from '../components/Confirmacao'
import HistoricoDemanda from '../components/HistoricoDemanda'
import CampoDemanda from '../components/CampoDemanda'
import Demanda from '../modelos/Demanda'
import styles from './DetalheDemanda.module.css'

const acoes = { estado: 'Mudar estado', texto: 'Anotar', responsavel_id: 'Trocar responsável' }
const inicial = { acao: 'estado', estado: '', texto: '', responsavel_id: '' }

export default function DetalheDemanda() {
  const { id } = useParams()
  const local = useLocation()
  const chave = 'demanda-' + id
  const caminho = '/api/demandas/' + id
  const [rascunho, setRascunho] = useState({ ...inicial, ...cliente.lerRascunho(chave) })
  const [demanda, setDemanda] = useState(null)
  const [reuniao, setReuniao] = useState(null)
  const [assistido, setAssistido] = useState(null)
  const [erroFicha, setErroFicha] = useState('')
  const [usuarios, setUsuarios] = useState(null)
  const [erroUsuarios, setErroUsuarios] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [confirmando, setConfirmando] = useState(false)
  const [enviando, setEnviando] = useState(false)
  const [erroCampo, setErroCampo] = useState('')
  const [erroServidor, setErroServidor] = useState('')
  const [sucesso, setSucesso] = useState(local.state?.mensagem || '')

  useEffect(() => {
    async function buscarDemanda() {
      try {
        const resposta = await cliente.get(caminho)
        setDemanda(new Demanda(resposta.data))
      } catch (falha) {
        setErroFicha(cliente.mensagemDeErro(falha))
      }
    }
    buscarDemanda()
  }, [caminho, tentativa])

  // A demanda só traz os ids; data, setor e nome vêm das fichas. Se a consulta falhar, fica o número.
  const reuniaoId = demanda?.reuniao_id
  const assistidoId = demanda?.assistido_id
  useEffect(() => {
    async function buscarReuniao() {
      try {
        const resposta = await cliente.get('/api/reunioes/' + reuniaoId)
        setReuniao(resposta.data)
      } catch {
        setReuniao(null)
      }
    }
    if (reuniaoId) buscarReuniao()
  }, [reuniaoId])

  useEffect(() => {
    async function buscarAssistido() {
      try {
        const resposta = await cliente.get('/api/assistidos/' + assistidoId)
        setAssistido(resposta.data)
      } catch {
        setAssistido(null)
      }
    }
    if (assistidoId) buscarAssistido()
  }, [assistidoId])

  useEffect(() => {
    async function buscarUsuarios() {
      try {
        const resposta = await cliente.get('/api/usuarios', { params: { ativo: true } })
        setUsuarios(resposta.data)
      } catch (falha) {
        setErroUsuarios(cliente.mensagemDeErro(falha))
      }
    }
    buscarUsuarios()
  }, [tentativa])

  function tentarNovamente() {
    setErroFicha('')
    setErroUsuarios('')
    setTentativa(tentativa + 1)
  }

  const proximos = demanda ? demanda.proximosEstados() : []
  const acao = rascunho.acao === 'estado' && !proximos.length ? 'texto' : rascunho.acao
  const outrosUsuarios = usuarios?.filter(item => item.id !== demanda?.responsavel_id)

  function guardar(valores) {
    setRascunho(valores)
    cliente.guardarRascunho(chave, valores)
    setErroCampo('')
    setErroServidor('')
  }

  function escolherAcao(evento) {
    guardar({ ...rascunho, acao: evento.currentTarget.value })
    setSucesso('')
  }

  function preencherCampo(evento) {
    guardar({ ...rascunho, [acao]: evento.target.value })
    setSucesso('')
  }

  function revisarAlteracao(evento) {
    evento.preventDefault()
    let mensagem = ''
    if (acao === 'texto' && !rascunho.texto.trim()) mensagem = 'Escreva o texto da anotação.'
    if (acao === 'estado' && !proximos.includes(rascunho.estado)) mensagem = 'Escolha o novo estado.'
    if (acao === 'responsavel_id' && !outrosUsuarios?.some(item => item.id === Number(rascunho.responsavel_id))) {
      mensagem = 'Escolha um novo responsável ativo.'
    }
    if (mensagem) {
      setErroCampo(mensagem)
      evento.currentTarget.elements[acao].focus()
    } else if (acao === 'estado') {
      setConfirmando(true)
    } else {
      salvarAlteracao()
    }
  }

  function voltarAoFormulario() {
    setConfirmando(false)
  }

  async function salvarAlteracao() {
    setConfirmando(false)
    setEnviando(true)
    setErroServidor('')
    setSucesso('')
    try {
      if (acao === 'estado') {
        const resposta = await cliente.patch(caminho + '/estado', { estado: rascunho.estado })
        setDemanda(new Demanda(resposta.data))
        setSucesso('Estado atualizado.')
      } else if (acao === 'texto') {
        // A API devolve só a anotação nova; ela entra no fim do histórico já carregado.
        const resposta = await cliente.post(caminho + '/anotacoes', { texto: rascunho.texto.trim() })
        setDemanda(new Demanda({ ...demanda, historico: [...demanda.historico, resposta.data], ultimo_movimento: resposta.data.ocorrido_em }))
        setSucesso('Anotação registrada no histórico.')
      } else {
        const resposta = await cliente.patch(caminho + '/responsavel', { responsavel_id: Number(rascunho.responsavel_id) })
        setDemanda(new Demanda(resposta.data))
        setSucesso('Responsável atualizado.')
      }
      guardar({ ...rascunho, [acao]: '' })
    } catch (falha) {
      setErroServidor(cliente.mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  const atributos = {
    id: acao, name: acao, value: rascunho[acao], onChange: preencherCampo, required: true,
    'aria-invalid': Boolean(erroCampo), 'aria-describedby': erroCampo ? acao + '-erro' : undefined,
  }

  return (
    <div className={styles.pagina}>
      <Link className="voltar" to="/demandas">Voltar para demandas</Link>
      <h1>Demanda nº {id}</h1>
      <AvisoSucesso>{sucesso}</AvisoSucesso>
      {erroFicha ? <div className="aviso-erro" role="alert">{erroFicha} <button className="botao botao-secundario" onClick={tentarNovamente}>Tentar de novo</button></div> :
        !demanda && <p role="status">Carregando demanda…</p>}
      {demanda && <>
        <section className={styles.ficha} aria-label="Dados da demanda">
          <p className={styles.descricao}>{demanda.descricao}</p>
          <dl className={styles.dados}>
            <div><dt>Estado</dt><dd>{demanda.rotuloEstado()}</dd></div>
            <div><dt>Responsável</dt><dd>{demanda.responsavel_nome}</dd></div>
            <div><dt>Prazo</dt><dd>
              {demanda.prazoFormatado()}{demanda.estaVencida() && <strong className={styles.vencida}> (vencida)</strong>}
            </dd></div>
            <div><dt>Prioridade</dt><dd>{demanda.rotuloPrioridade()}</dd></div>
            <div><dt>Reunião de origem</dt><dd>
              <Link to={'/reunioes/' + reuniaoId}>
                {reuniao ? `${dataCurta(reuniao.data)}, ${setores[reuniao.setor]}` : `Reunião nº ${reuniaoId}`}
              </Link>
            </dd></div>
            <div><dt>Assistido</dt><dd>
              {assistidoId ? (
                <Link to={'/assistidos/' + assistidoId}>
                  {assistido ? assistido.nome_tratamento : `Assistido nº ${assistidoId}`}
                </Link>
              ) : 'Sem vínculo'}
            </dd></div>
            <div><dt>Categoria</dt><dd>{demanda.categoria || 'Sem categoria'}</dd></div>
            <div><dt>Registro</dt><dd>{dataHora(demanda.criado_em)}</dd></div>
            <div><dt>Último movimento</dt><dd>{dataHora(demanda.ultimo_movimento)}</dd></div>
          </dl>
        </section>
        <section className={styles.ficha} aria-labelledby="atualizar">
          <h2 id="atualizar">Atualizar demanda</h2>
          <div className={styles.acoes} role="group" aria-label="Tipo de atualização">
            {Object.entries(acoes).filter(([valor]) => valor !== 'estado' || proximos.length > 0).map(([valor, nome]) =>
              <button key={valor} type="button" value={valor} aria-pressed={acao === valor} onClick={escolherAcao} disabled={enviando}>{nome}</button>)}
            <Link className="botao-secundario" to={'/encaminhamentos/novo?demanda_id=' + id}>Encaminhar</Link>
          </div>
          <form noValidate onSubmit={revisarAlteracao}>
            <fieldset className={styles.edicao} disabled={enviando}>
              {acao === 'estado' && <CampoDemanda nome={acao} rotulo="Novo estado" erro={erroCampo}>
                <select {...atributos}><option value="">Selecione o novo estado</option>
                  {proximos.map(valor => <option key={valor} value={valor}>{estados[valor]}</option>)}
                </select>
              </CampoDemanda>}
              {acao === 'texto' && <CampoDemanda nome={acao} rotulo="Anotação" erro={erroCampo}><textarea {...atributos} rows="3" /></CampoDemanda>}
              {acao === 'responsavel_id' && <>
                {erroUsuarios ? <div className="aviso-erro" role="alert">{erroUsuarios} <button type="button" className="botao botao-secundario" onClick={tentarNovamente}>Tentar de novo</button></div> :
                  !usuarios && <p role="status">Carregando responsáveis…</p>}
                <CampoDemanda nome={acao} rotulo="Novo responsável" erro={erroCampo}>
                  <select {...atributos} disabled={!outrosUsuarios?.length}><option value="">{usuarios && !outrosUsuarios.length ? 'Nenhum outro responsável ativo' : 'Selecione o novo responsável'}</option>
                    {outrosUsuarios?.map(item => <option key={item.id} value={item.id}>{item.nome}</option>)}
                  </select>
                </CampoDemanda>
              </>}
              {erroServidor && <p role="alert" className="aviso-erro">{erroServidor}</p>}
              <button type="submit" className="botao botao-primario" disabled={acao === 'responsavel_id' && !outrosUsuarios?.length}>
                {enviando ? 'Salvando…' : acao === 'texto' ? 'Salvar anotação' : acao === 'estado' ? 'Alterar estado' : 'Salvar responsável'}
              </button>
            </fieldset>
          </form>
        </section>
        <HistoricoDemanda historico={demanda.historico} />
        {confirmando && <Confirmacao titulo="Confirmar mudança de estado?" acao="Confirmar mudança" aoVoltar={voltarAoFormulario} aoConfirmar={salvarAlteracao}>
          <p>A demanda nº {id} passará de <strong>{demanda.rotuloEstado()}</strong> para <strong>{estados[rascunho.estado]}</strong>.</p>
          {['concluida', 'cancelada'].includes(rascunho.estado) && <p>Esse estado encerra a demanda.</p>}
        </Confirmacao>}
      </>}
    </div>
  )
}
