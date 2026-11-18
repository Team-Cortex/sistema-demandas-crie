import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import CampoDemanda from '../../components/CampoDemanda'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Assistidos.module.css'

export default function FormAssistido() {
  const { id } = useParams()
  const navegar = useNavigate()
  const chave = 'assistido-' + (id || 'novo')
  const [nome, definirNome] = useState(() => lerRascunho(chave)?.nome_tratamento ?? null)
  const [assistido, definirAssistido] = useState(null)
  const [erroConsulta, definirErroConsulta] = useState('')
  const [tentativa, definirTentativa] = useState(0)
  const [erro, definirErro] = useState('')
  const [erroNome, definirErroNome] = useState('')
  const [salvando, definirSalvando] = useState(false)
  const valor = nome ?? assistido?.nome_tratamento ?? ''
  const titulo = id ? 'Editar nome de tratamento' : 'Cadastrar assistido'
  const voltar = id ? '/assistidos/' + id : '/assistidos'

  useEffect(() => {
    if (!id) return
    const controlador = new AbortController()
    cliente.get('/api/assistidos/' + id, { signal: controlador.signal }).then(({ data }) => definirAssistido(data))
      .catch(falha => { if (!controlador.signal.aborted) definirErroConsulta(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [id, tentativa])

  function tentarNovamente() { definirErroConsulta(''); definirTentativa(tentativa + 1) }

  function preencherNome(evento) {
    definirNome(evento.target.value)
    guardarRascunho(chave, { nome_tratamento: evento.target.value })
    definirErroNome('')
    definirErro('')
  }

  async function salvarAssistido(evento) {
    evento.preventDefault()
    const nome_tratamento = valor.trim()
    if (!nome_tratamento || [...nome_tratamento].length > 120) {
      definirErroNome(!nome_tratamento ? 'Informe o nome de tratamento.' : 'Use até 120 caracteres.')
      evento.currentTarget.elements.nome_tratamento.focus()
      return
    }
    definirSalvando(true)
    definirErro('')
    try {
      const { data } = id ? await cliente.patch('/api/assistidos/' + id, { nome_tratamento }) :
        await cliente.post('/api/assistidos', { nome_tratamento })
      apagarRascunho(chave)
      navegar('/assistidos/' + data.id, { replace: true, state: { mensagem: id ? 'Nome de tratamento atualizado.' : 'Assistido cadastrado.' } })
    } catch (falha) {
      definirErro(mensagemDeErro(falha))
      definirSalvando(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <Link className={styles.voltar} to={voltar}><ArrowLeft size={17} aria-hidden="true" />{id ? 'Ficha do assistido' : 'Assistidos'}</Link>
      <h1>{titulo}</h1>
      {erroConsulta ? <ErroConsulta mensagem={erroConsulta} tentarNovamente={tentarNovamente} /> : id && !assistido ? <Carregando /> :
        <form noValidate className={styles.formulario} onSubmit={salvarAssistido}>
          <fieldset className={styles.campos} disabled={salvando}>
            <CampoDemanda nome="nome_tratamento" rotulo="Nome de tratamento" erro={erroNome}>
              <input id="nome_tratamento" name="nome_tratamento" value={valor} onChange={preencherNome} required maxLength={120}
                aria-describedby={erroNome ? 'apoio-nome nome_tratamento-erro' : 'apoio-nome'} aria-invalid={Boolean(erroNome)} />
              <p id="apoio-nome" className={styles.secundario}>Use o nome pelo qual a pessoa é chamada no CRIE. Não registre documentos nem dados de saúde aqui.</p>
            </CampoDemanda>
            {erro && <p role="alert" className="aviso-erro">{erro}</p>}
            <div className={styles.acoes}><button className="botao-primario">{salvando ? 'Salvando…' : id ? 'Salvar alterações' : titulo}</button></div>
          </fieldset>
        </form>}
    </div>
  )
}
