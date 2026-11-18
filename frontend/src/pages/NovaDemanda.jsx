import { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { ArrowLeft, ClipboardList } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../api/cliente'
import CampoDemanda from '../components/CampoDemanda'
import Confirmacao from '../components/Confirmacao'
import { prioridades, setores, dataCurta } from '../dominio'
import { validarDemanda } from './regrasDemanda'
import styles from './NovaDemanda.module.css'

const vazio = {
  descricao: '', prioridade: '', responsavel_id: '', prazo: '',
  reuniao_id: null, assistido_id: '', categoria: '',
}

export default function NovaDemanda() {
  const navegar = useNavigate()
  const [parametros] = useSearchParams()
  const reuniaoDeOrigem = parametros.get('reuniao_id')
  const chave = reuniaoDeOrigem ? 'nova-demanda-reuniao-' + reuniaoDeOrigem : 'nova-demanda'
  const [rascunho, definirRascunho] = useState(() => ({ ...vazio, ...lerRascunho(chave) }))
  const [opcoes, definirOpcoes] = useState(null)
  const [erroListas, definirErroListas] = useState('')
  const [tentativa, definirTentativa] = useState(0)
  const [erros, definirErros] = useState({})
  const [erroServidor, definirErroServidor] = useState('')
  const [confirmando, definirConfirmando] = useState(false)
  const [enviando, definirEnviando] = useState(false)

  useEffect(() => {
    let ativo = true
    async function listarOpcoes() {
      try {
        const [usuarios, reunioes, assistidos] = await Promise.all([
          cliente.get('/api/usuarios', { params: { ativo: true } }),
          cliente.get('/api/reunioes'), cliente.get('/api/assistidos'),
        ])
        if (ativo) definirOpcoes({ usuarios: usuarios.data, reunioes: reunioes.data, assistidos: assistidos.data })
      } catch (erro) {
        if (ativo) definirErroListas(mensagemDeErro(erro))
      }
    }
    listarOpcoes()
    return () => { ativo = false }
  }, [tentativa])

  const campos = {
    ...rascunho,
    reuniao_id: rascunho.reuniao_id ?? reuniaoDeOrigem ?? String(opcoes?.reunioes[0]?.id ?? ''),
  }

  function tentarNovamente() {
    definirErroListas('')
    definirTentativa(tentativa + 1)
  }

  function preencherCampo(evento) {
    const { name, value } = evento.target
    const valores = { ...rascunho, [name]: value }
    if (opcoes && valores.reuniao_id === null) valores.reuniao_id = campos.reuniao_id
    definirRascunho(valores)
    guardarRascunho(chave, valores)
    definirErros({ ...erros, [name]: '' })
    definirErroServidor('')
  }

  function atributos(nome, obrigatorio = true) {
    return {
      id: nome, name: nome, required: obrigatorio,
      value: campos[nome], onChange: preencherCampo,
      'aria-invalid': Boolean(erros[nome]),
      'aria-describedby': erros[nome] ? nome + '-erro' : undefined,
    }
  }

  function revisarDemanda(evento) {
    evento.preventDefault()
    const invalidos = validarDemanda(campos, opcoes)
    definirErros(invalidos)
    const primeiro = Object.keys(invalidos)[0]
    if (primeiro) {
      evento.currentTarget.elements.namedItem(primeiro).focus()
      return
    }
    definirConfirmando(true)
  }

  function voltarAoFormulario() {
    definirConfirmando(false)
  }

  async function salvarDemanda() {
    definirConfirmando(false)
    definirEnviando(true)
    definirErroServidor('')
    try {
      const { data } = await cliente.post('/api/demandas', {
        descricao: campos.descricao.trim(), prioridade: campos.prioridade,
        responsavel_id: Number(campos.responsavel_id), prazo: campos.prazo,
        reuniao_id: Number(campos.reuniao_id),
        assistido_id: campos.assistido_id ? Number(campos.assistido_id) : null,
        categoria: campos.categoria.trim() || null,
      })
      apagarRascunho(chave)
      navegar('/demandas/' + data.id, { replace: true, state: { mensagem: 'Demanda registrada com sucesso.' } })
    } catch (erro) {
      definirErroServidor(mensagemDeErro(erro))
      definirEnviando(false)
    }
  }

  const semResponsavel = opcoes && !opcoes.usuarios.length
  const semReuniao = opcoes && !opcoes.reunioes.length
  const responsavel = opcoes?.usuarios.find(item => item.id === Number(campos.responsavel_id))
  const reuniao = opcoes?.reunioes.find(item => item.id === Number(campos.reuniao_id))

  return (
    <div className={styles.pagina}>
      <Link to="/demandas" className={styles.voltar}><ArrowLeft size={17} aria-hidden="true" />Demandas</Link>
      <h1>Registrar demanda</h1>
      <form onSubmit={revisarDemanda} noValidate className={styles.ficha}>
        <header className={styles.cabecalho}><ClipboardList size={21} aria-hidden="true" /><h2>Dados da demanda</h2></header>
        {erroListas ? <div role="alert" className="aviso-erro">{erroListas} <button type="button" className="botao botao-secundario" onClick={tentarNovamente}>Tentar de novo</button></div> :
          !opcoes && <p role="status">Carregando responsáveis, reuniões e assistidos…</p>}
        <fieldset disabled={enviando} className={styles.campos}>
          <div className={styles.inteira}>
            <CampoDemanda nome="descricao" rotulo="Descrição" erro={erros.descricao}>
              <textarea {...atributos('descricao')} rows="4" />
            </CampoDemanda>
          </div>
          <CampoDemanda nome="prioridade" rotulo="Prioridade" erro={erros.prioridade}>
            <select {...atributos('prioridade')}>
              <option value="">Selecione a prioridade</option>
              {Object.entries(prioridades).map(([valor, nome]) => <option key={valor} value={valor}>{nome}</option>)}
            </select>
          </CampoDemanda>
          <CampoDemanda nome="prazo" rotulo="Prazo" erro={erros.prazo}>
            <input {...atributos('prazo')} type="date" />
          </CampoDemanda>
          <CampoDemanda nome="responsavel_id" rotulo="Responsável" erro={erros.responsavel_id}>
            <select {...atributos('responsavel_id')} disabled={!opcoes || semResponsavel}>
              <option value="">{semResponsavel ? 'Nenhum responsável ativo' : 'Selecione o responsável'}</option>
              {opcoes?.usuarios.map(item => <option key={item.id} value={item.id}>{item.nome}</option>)}
            </select>
          </CampoDemanda>
          <CampoDemanda nome="reuniao_id" rotulo="Reunião de origem" erro={erros.reuniao_id}>
            <select {...atributos('reuniao_id')} disabled={!opcoes || semReuniao}>
              <option value="">{semReuniao ? 'Nenhuma reunião cadastrada' : 'Selecione a reunião'}</option>
              {opcoes?.reunioes.map(item => <option key={item.id} value={item.id}>Reunião de {dataCurta(item.data)} — {setores[item.setor]}</option>)}
            </select>
          </CampoDemanda>
          <CampoDemanda nome="assistido_id" rotulo="Assistido (opcional)" erro={erros.assistido_id}>
            <select {...atributos('assistido_id', false)} disabled={!opcoes}>
              <option value="">{opcoes && !opcoes.assistidos.length ? 'Nenhum assistido cadastrado' : 'Sem assistido vinculado'}</option>
              {opcoes?.assistidos.map(item => <option key={item.id} value={item.id}>{item.nome_tratamento}</option>)}
            </select>
          </CampoDemanda>
          <CampoDemanda nome="categoria" rotulo="Categoria (opcional)" erro={erros.categoria}>
            <input {...atributos('categoria', false)} type="text" maxLength={80} />
          </CampoDemanda>
        </fieldset>
        {semResponsavel && <p role="status">Para registrar uma demanda, é preciso ter um responsável ativo. Consulte a direção.</p>}
        {semReuniao && <p role="status">Antes, registre a reunião em que a demanda surgiu. <Link className="botao-secundario" to="/reunioes/nova">Registrar reunião</Link></p>}
        {erroServidor && <p role="alert" className="aviso-erro">{erroServidor}</p>}
        <footer className={styles.acoes}>
          <button type="submit" className="botao botao-primario" disabled={enviando || !opcoes || semReuniao || semResponsavel}>{enviando ? 'Registrando…' : 'Registrar demanda'}</button>
        </footer>
      </form>
      {confirmando && <Confirmacao titulo="Confirmar registro da demanda?" acao="Confirmar registro" aoVoltar={voltarAoFormulario} aoConfirmar={salvarDemanda}>
        <p className={styles.descricao}>{campos.descricao}</p>
        <dl className={styles.resumo}>
          <dt>Responsável</dt><dd>{responsavel.nome}</dd>
          <dt>Prazo</dt><dd>{dataCurta(campos.prazo)}</dd>
          <dt>Prioridade</dt><dd>{prioridades[campos.prioridade]}</dd>
          <dt>Reunião de origem</dt><dd>{dataCurta(reuniao.data)} — {setores[reuniao.setor]}</dd>
          {campos.assistido_id && <><dt>Assistido</dt><dd>{opcoes.assistidos.find(item => item.id === Number(campos.assistido_id)).nome_tratamento}</dd></>}
          {campos.categoria.trim() && <><dt>Categoria</dt><dd>{campos.categoria}</dd></>}
        </dl>
      </Confirmacao>}
    </div>
  )
}
