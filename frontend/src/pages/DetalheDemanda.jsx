import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { ArrowLeft, AlertCircle, CheckCircle2 } from 'lucide-react'
import cliente, { guardarRascunho, lerRascunho, mensagemDeErro } from '../api/cliente'
import { estados, prioridades, dataCurta, dataHora } from '../dominio'
import Confirmacao from '../components/Confirmacao'
import HistoricoDemanda from '../components/HistoricoDemanda'
import CampoDemanda from '../components/CampoDemanda'
import { transicoes } from './regrasDemanda'
import styles from './DetalheDemanda.module.css'

const acoes = { estado: 'Mudar estado', texto: 'Anotar', responsavel_id: 'Trocar responsável' }
const inicial = { acao: 'estado', estado: '', texto: '', responsavel_id: '' }

export default function DetalheDemanda() {
  const { id } = useParams()
  const local = useLocation()
  const chave = 'demanda-' + id
  const caminho = '/api/demandas/' + id
  const [rascunho, definirRascunho] = useState(() => ({ ...inicial, ...lerRascunho(chave) }))
  const [demanda, definirDemanda] = useState(null)
  const [erroFicha, definirErroFicha] = useState('')
  const [usuarios, definirUsuarios] = useState(null)
  const [erroUsuarios, definirErroUsuarios] = useState('')
  const [tentativa, definirTentativa] = useState(0)
  const [confirmando, definirConfirmando] = useState(false)
  const [enviando, definirEnviando] = useState(false)
  const [erroCampo, definirErroCampo] = useState('')
  const [erroServidor, definirErroServidor] = useState('')
  const [sucesso, definirSucesso] = useState(local.state?.mensagem || '')

  useEffect(() => {
    let ativo = true
    cliente.get(caminho).then(({ data }) => {
      if (ativo) definirDemanda(data)
    }).catch(erro => {
      if (ativo) definirErroFicha(mensagemDeErro(erro))
    })
    return () => { ativo = false }
  }, [caminho, tentativa])

  useEffect(() => {
    let ativo = true
    cliente.get('/api/usuarios', { params: { ativo: true } }).then(({ data }) => {
      if (ativo) definirUsuarios(data)
    }).catch(erro => {
      if (ativo) definirErroUsuarios(mensagemDeErro(erro))
    })
    return () => { ativo = false }
  }, [tentativa])

  function tentarNovamente() {
    definirErroFicha('')
    definirErroUsuarios('')
    definirTentativa(tentativa + 1)
  }

  const proximos = demanda ? transicoes[demanda.estado] : []
  const acao = rascunho.acao === 'estado' && !proximos.length ? 'texto' : rascunho.acao
  const outrosUsuarios = usuarios?.filter(item => item.id !== demanda?.responsavel_id)

  function guardar(valores) {
    definirRascunho(valores)
    guardarRascunho(chave, valores)
    definirErroCampo('')
    definirErroServidor('')
  }

  function escolherAcao(evento) {
    guardar({ ...rascunho, acao: evento.currentTarget.value })
    definirSucesso('')
  }

  function preencherCampo(evento) {
    guardar({ ...rascunho, [acao]: evento.target.value })
    definirSucesso('')
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
      definirErroCampo(mensagem)
      evento.currentTarget.elements.namedItem(acao).focus()
    } else if (acao === 'estado') {
      definirConfirmando(true)
    } else {
      salvarAlteracao()
    }
  }

  function voltarAoFormulario() {
    definirConfirmando(false)
  }

  async function salvarAlteracao() {
    definirConfirmando(false)
    definirEnviando(true)
    definirErroServidor('')
    definirSucesso('')
    try {
      if (acao === 'estado') {
        const { data } = await cliente.patch(caminho + '/estado', { estado: rascunho.estado })
        definirDemanda(data)
        definirSucesso('Estado atualizado.')
      } else if (acao === 'texto') {
        const { data } = await cliente.post(caminho + '/anotacoes', { texto: rascunho.texto.trim() })
        definirDemanda({ ...demanda, historico: [...demanda.historico, data], ultimo_movimento: data.ocorrido_em })
        definirSucesso('Anotação registrada no histórico.')
      } else {
        const { data } = await cliente.patch(caminho + '/responsavel', { responsavel_id: Number(rascunho.responsavel_id) })
        definirDemanda(data)
        definirSucesso('Responsável atualizado.')
      }
      guardar({ ...rascunho, [acao]: '' })
    } catch (erro) {
      definirErroServidor(mensagemDeErro(erro))
    } finally {
      definirEnviando(false)
    }
  }

  const atributos = {
    id: acao, name: acao, value: rascunho[acao], onChange: preencherCampo, required: true,
    'aria-invalid': Boolean(erroCampo), 'aria-describedby': erroCampo ? acao + '-erro' : undefined,
  }

  return (
    <div className={styles.pagina}>
      <Link className={styles.voltar} to="/demandas"><ArrowLeft size={17} aria-hidden="true" />Demandas</Link>
      <h1>Demanda #{id}</h1>
      {sucesso && <p className={styles.sucesso} role="status"><CheckCircle2 size={19} aria-hidden="true" />{sucesso}</p>}
      {erroFicha ? <div className="aviso-erro" role="alert">{erroFicha} <button className="botao botao-secundario" onClick={tentarNovamente}>Tentar de novo</button></div> :
        !demanda && <p role="status">Carregando demanda…</p>}
      {demanda && <>
        <section className={styles.ficha} aria-label="Dados da demanda">
          <div className={styles.estados}><span>{estados[demanda.estado]}</span>
            {demanda.vencida && <strong><AlertCircle size={16} aria-hidden="true" />Vencida</strong>}
          </div>
          <p className={styles.descricao}>{demanda.descricao}</p>
          <dl className={styles.dados}>
            <div><dt>Responsável</dt><dd>{demanda.responsavel_nome}</dd></div>
            <div><dt>Prazo</dt><dd>{dataCurta(demanda.prazo)}</dd></div>
            <div><dt>Prioridade</dt><dd>{prioridades[demanda.prioridade]}</dd></div>
            <div><dt>Reunião de origem</dt><dd><Link to={'/reunioes/' + demanda.reuniao_id}>Reunião #{demanda.reuniao_id}</Link></dd></div>
            <div><dt>Assistido</dt><dd>{demanda.assistido_id ? <Link to={'/assistidos/' + demanda.assistido_id}>Assistido #{demanda.assistido_id}</Link> : 'Sem vínculo'}</dd></div>
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
          <p>A demanda #{id} passará de <strong>{estados[demanda.estado]}</strong> para <strong>{estados[rascunho.estado]}</strong>.</p>
          {['concluida', 'cancelada'].includes(rascunho.estado) && <p>Esse estado encerra a demanda.</p>}
        </Confirmacao>}
      </>}
    </div>
  )
}
