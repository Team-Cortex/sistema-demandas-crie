import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import { dataCurta } from '../../dominio'
import CampoDemanda from '../../components/CampoDemanda'
import Confirmacao from '../../components/Confirmacao'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Encaminhamentos.module.css'

export default function RegistrarDesfecho() {
  const { id } = useParams()
  const navegar = useNavigate()
  const caminho = '/api/encaminhamentos/' + id
  const chave = 'desfecho:' + id
  const [item, setItem] = useState(null)
  const [texto, setTexto] = useState(lerRascunho(chave)?.texto || '')
  const [erroCarga, setErroCarga] = useState('')
  const [erroCampo, setErroCampo] = useState('')
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [confirmando, setConfirmando] = useState(false)
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    async function buscarEncaminhamento() {
      try {
        const resposta = await cliente.get(caminho)
        setItem(resposta.data)
      } catch (falha) {
        setErroCarga(mensagemDeErro(falha))
      }
    }
    buscarEncaminhamento()
  }, [caminho, tentativa])

  function tentarNovamente() {
    setErroCarga('')
    setItem(null)
    setTentativa(tentativa + 1)
  }

  function alterarTexto(evento) {
    setTexto(evento.target.value)
    guardarRascunho(chave, { texto: evento.target.value })
    setErroCampo('')
    setErro('')
  }

  function revisarDesfecho(evento) {
    evento.preventDefault()
    if (!texto.trim()) {
      setErroCampo('Escreva o desfecho do encaminhamento.')
      evento.currentTarget.elements.desfecho.focus()
    } else {
      setConfirmando(true)
    }
  }

  function voltar() {
    setConfirmando(false)
  }

  async function registrar() {
    setConfirmando(false)
    setEnviando(true)
    setErro('')
    try {
      await cliente.patch(caminho + '/desfecho', { desfecho: texto.trim() })
      apagarRascunho(chave)
      navegar('/encaminhamentos?lista=todos', { replace: true, state: { mensagem: 'Desfecho registrado.' } })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
      // 400: o desfecho já foi registrado; recarrega para mostrar o que ficou gravado.
      if (falha.response?.status === 400) tentarNovamente()
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className={styles.formulario}>
      <Link className="voltar" to="/encaminhamentos">Voltar para encaminhamentos</Link>
      <h1>Registrar desfecho</h1>
      {erro && <p className="aviso-erro" role="alert">{erro}</p>}
      {erroCarga ? <ErroConsulta mensagem={erroCarga} tentarNovamente={tentarNovamente} /> : !item ? <Carregando /> :
        <form onSubmit={revisarDesfecho} noValidate>
          <fieldset disabled={enviando}>
            <h2>{item.destino}</h2><p>Em {dataCurta(item.data)}, por {item.responsavel_nome}</p>
            {item.pendente ? <>
              <CampoDemanda nome="desfecho" rotulo="Desfecho" erro={erroCampo}>
                <textarea id="desfecho" name="desfecho" required rows={4} value={texto} onChange={alterarTexto} aria-invalid={Boolean(erroCampo)} aria-describedby={erroCampo ? 'desfecho-erro aviso-desfecho' : 'aviso-desfecho'} />
              </CampoDemanda>
              <p className={styles.aviso} id="aviso-desfecho">O desfecho só pode ser registrado uma vez.</p>
              <div className={styles.acoes}><button type="submit" className="botao-primario">{enviando ? 'Registrando…' : 'Registrar desfecho'}</button></div>
            </> : <p className={styles.texto}><strong>Desfecho registrado</strong>{item.desfecho}</p>}
          </fieldset>
        </form>}
      {confirmando && <Confirmacao titulo="Confirmar o desfecho?" acao="Confirmar desfecho" aoVoltar={voltar} aoConfirmar={registrar}>
        <p className={styles.texto}>{texto}</p><p>O desfecho só pode ser registrado uma vez.</p>
      </Confirmacao>}
    </div>
  )
}
