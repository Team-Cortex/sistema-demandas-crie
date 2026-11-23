import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import CampoDemanda from '../../components/CampoDemanda'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Assistidos.module.css'

export default function FormAssistido() {
  const { id } = useParams()
  const navegar = useNavigate()
  const chave = 'assistido-' + (id || 'novo')
  // null = ainda não digitou; aí vale o nome já gravado (na edição).
  const [nome, setNome] = useState(lerRascunho(chave)?.nome_tratamento ?? null)
  const [assistido, setAssistido] = useState(null)
  const [erroConsulta, setErroConsulta] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [erro, setErro] = useState('')
  const [erroNome, setErroNome] = useState('')
  const [salvando, setSalvando] = useState(false)
  const valor = nome ?? assistido?.nome_tratamento ?? ''
  const titulo = id ? 'Editar nome de tratamento' : 'Cadastrar assistido'
  const voltar = id ? '/assistidos/' + id : '/assistidos'

  useEffect(() => {
    async function buscarAssistido() {
      try {
        const resposta = await cliente.get('/api/assistidos/' + id)
        setAssistido(resposta.data)
      } catch (falha) {
        setErroConsulta(mensagemDeErro(falha))
      }
    }
    if (id) buscarAssistido()
  }, [id, tentativa])

  function tentarNovamente() {
    setErroConsulta('')
    setTentativa(tentativa + 1)
  }

  function preencherNome(evento) {
    setNome(evento.target.value)
    guardarRascunho(chave, { nome_tratamento: evento.target.value })
    setErroNome('')
    setErro('')
  }

  async function salvarAssistido(evento) {
    evento.preventDefault()
    const nome_tratamento = valor.trim()
    if (!nome_tratamento) {
      setErroNome('Informe o nome de tratamento.')
      evento.currentTarget.elements.nome_tratamento.focus()
      return
    }
    setSalvando(true)
    setErro('')
    try {
      const resposta = id ? await cliente.patch('/api/assistidos/' + id, { nome_tratamento }) :
        await cliente.post('/api/assistidos', { nome_tratamento })
      apagarRascunho(chave)
      navegar('/assistidos/' + resposta.data.id, { replace: true, state: { mensagem: id ? 'Nome de tratamento atualizado.' : 'Assistido cadastrado.' } })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
      setSalvando(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <Link className="voltar" to={voltar}>{id ? 'Voltar para a ficha do assistido' : 'Voltar para assistidos'}</Link>
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
