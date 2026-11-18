import { useEffect, useState } from 'react'
import { ArrowLeft } from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import CampoDemanda from '../../components/CampoDemanda'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { hojeCrie, setores } from '../../dominio'
import styles from './Reunioes.module.css'

export default function FormularioReuniao() {
  const { id } = useParams()
  const navegar = useNavigate()
  const chave = 'reuniao-' + (id || 'nova')
  const voltar = id ? '/reunioes/' + id : '/reunioes'
  const [rascunho, setRascunho] = useState(() => lerRascunho(chave) || {})
  const [opcoes, setOpcoes] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [erros, setErros] = useState({})
  const [erroServidor, setErroServidor] = useState('')
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    const controlador = new AbortController()
    const config = { signal: controlador.signal }
    Promise.all([cliente.get('/api/usuarios', { ...config, params: { ativo: true } }), id ? cliente.get('/api/reunioes/' + id, config) : null])
      .then(([usuarios, ficha]) => setOpcoes({ usuarios: usuarios.data, reuniao: ficha?.data }))
      .catch(falha => { if (!controlador.signal.aborted) setErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [id, tentativa])

  const reuniao = opcoes?.reuniao
  const data = rascunho.data ?? reuniao?.data ?? hojeCrie()
  const setor = rascunho.setor ?? reuniao?.setor ?? ''
  const presentes = reuniao?.participantes || []
  const participanteIds = rascunho.participante_ids ?? presentes.map(pessoa => pessoa.id)
  const inativos = presentes.filter(pessoa => !opcoes.usuarios.some(usuario => usuario.id === pessoa.id))

  function tentarNovamente() {
    setErro('')
    setTentativa(tentativa + 1)
  }

  function guardar(campo, valor) {
    const atualizado = { ...rascunho, [campo]: valor }
    setRascunho(atualizado)
    guardarRascunho(chave, atualizado)
    setErros({ ...erros, [campo]: '' })
    setErroServidor('')
  }

  function preencherCampo(evento) { guardar(evento.target.name, evento.target.value) }
  function alterarPresenca(evento) {
    const participante = Number(evento.target.value)
    const ativos = participanteIds.filter(valor => opcoes.usuarios.some(usuario => usuario.id === valor))
    guardar('participante_ids', evento.target.checked ? [...ativos, participante] : ativos.filter(valor => valor !== participante))
  }

  async function salvarReuniao(evento) {
    evento.preventDefault()
    const invalidos = {}
    if (!/^\d{4}-\d{2}-\d{2}$/.test(data) || data.startsWith('0000')) invalidos.data = 'Informe a data da reunião.'
    if (!setores[setor]) invalidos.setor = 'Informe o setor da reunião.'
    const corpo = id ? { ...rascunho } : { data, setor }
    if (!id || rascunho.participante_ids) {
      corpo.participante_ids = participanteIds
      if (!participanteIds.length || participanteIds.some(valor => !opcoes.usuarios.some(usuario => usuario.id === valor))) {
        invalidos.participante_ids = 'Escolha pelo menos um participante ativo.'
      }
    }
    setErros(invalidos)
    if (Object.keys(invalidos).length) {
      evento.currentTarget.querySelector('[name="' + Object.keys(invalidos)[0] + '"]')?.focus()
      return
    }
    setEnviando(true)
    setErroServidor('')
    try {
      const resposta = id ? await cliente.patch('/api/reunioes/' + id, corpo) : await cliente.post('/api/reunioes', corpo)
      apagarRascunho(chave)
      navegar('/reunioes/' + resposta.data.id, { replace: true, state: { mensagem: id ? 'Reunião atualizada.' : 'Reunião registrada.' } })
    } catch (falha) {
      setErroServidor(mensagemDeErro(falha))
      setEnviando(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <Link to={voltar} className={styles.voltar}><ArrowLeft size={17} aria-hidden="true" />{id ? 'Reunião' : 'Reuniões'}</Link>
      <h1>{id ? 'Editar reunião' : 'Registrar reunião'}</h1>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> :
        !opcoes ? <Carregando>Carregando dados da reunião…</Carregando> :
        <form className={styles.formulario} onSubmit={salvarReuniao} noValidate>
          <fieldset className={styles.campos} disabled={enviando}>
            <CampoDemanda nome="data" rotulo="Data" erro={erros.data}>
              <input type="date" id="data" name="data" required value={data} onChange={preencherCampo} aria-invalid={!!erros.data} aria-describedby={erros.data ? 'data-erro' : undefined} />
            </CampoDemanda>
            <CampoDemanda nome="setor" rotulo="Setor" erro={erros.setor}>
              <select id="setor" name="setor" required value={setor} onChange={preencherCampo} aria-invalid={!!erros.setor} aria-describedby={erros.setor ? 'setor-erro' : undefined}>
                <option value="">Selecione o setor</option>{Object.entries(setores).map(([valor, nome]) => <option key={valor} value={valor}>{nome}</option>)}
              </select>
            </CampoDemanda>
            <fieldset className={styles.presencas} aria-describedby={erros.participante_ids ? 'presenca-erro' : undefined}>
              <legend>Participantes</legend>
              {opcoes.usuarios.map(usuario => <label key={usuario.id}>
                <input type="checkbox" name="participante_ids" value={usuario.id} checked={participanteIds.includes(usuario.id)} onChange={alterarPresenca}
                  aria-invalid={!!erros.participante_ids} aria-describedby={erros.participante_ids ? 'presenca-erro' : undefined} /> {usuario.nome}
              </label>)}
              {!opcoes.usuarios.length && <p>Nenhum participante ativo disponível. Consulte a direção.</p>}
              {inativos.length > 0 && <p>Participantes desativados no registro original: {inativos.map(pessoa => pessoa.nome).join(', ')}. Alterar a seleção de participantes substitui a lista original.</p>}
              {erros.participante_ids && <span id="presenca-erro" className={styles.erroCampo}>{erros.participante_ids}</span>}
            </fieldset>
          </fieldset>
          {erroServidor && <p role="alert" className="aviso-erro">{erroServidor}</p>}
          <div className={styles.acoes}><button className="botao-primario" disabled={enviando || (id ? !Object.keys(rascunho).length : !opcoes.usuarios.length)}>{enviando ? 'Salvando…' : id ? 'Salvar alterações' : 'Registrar reunião'}</button></div>
        </form>}
    </div>
  )
}
