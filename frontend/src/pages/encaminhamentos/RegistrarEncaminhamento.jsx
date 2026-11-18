import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import { hojeCrie } from '../../dominio'
import CampoDemanda from '../../components/CampoDemanda'
import styles from './Encaminhamentos.module.css'

export default function RegistrarEncaminhamento() {
  const navegar = useNavigate()
  const [parametros] = useSearchParams()
  const demanda = parametros.get('demanda_id')
  const assistido = parametros.get('assistido_id')
  const origem = demanda ? '/demandas/' + demanda : '/assistidos/' + assistido
  const chave = 'encaminhar:' + origem
  const [campos, setCampos] = useState(() => lerRascunho(chave) || { destino: '', data: hojeCrie(), observacao: '' })
  const [erros, setErros] = useState({})
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  function alterarCampo(evento) {
    const { name, value } = evento.target
    const valores = { ...campos, [name]: value }
    setCampos(valores)
    guardarRascunho(chave, valores)
    setErros({ ...erros, [name]: '' })
    setErro('')
  }

  async function registrar(evento) {
    evento.preventDefault()
    const falhas = {}
    if (!campos.destino.trim() || campos.destino.trim().length > 200) falhas.destino = 'Informe o destino em até 200 caracteres.'
    if (!campos.data || !evento.currentTarget.elements.data.validity.valid) falhas.data = 'Informe a data do encaminhamento.'
    setErros(falhas)
    if (Object.keys(falhas).length) {
      evento.currentTarget.elements[Object.keys(falhas)[0]].focus()
      return
    }
    setEnviando(true)
    setErro('')
    try {
      const dados = { destino: campos.destino.trim(), data: campos.data, observacao: campos.observacao.trim() }
      if (demanda) dados.demanda_id = Number(demanda)
      if (assistido) dados.assistido_id = Number(assistido)
      await cliente.post('/api/encaminhamentos', dados)
      apagarRascunho(chave)
      navegar('/encaminhamentos', { replace: true, state: { mensagem: 'Encaminhamento registrado.' } })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  if ((!demanda && !assistido) || [demanda, assistido].some(id => id !== null && !/^[1-9]\d*$/.test(id))) {
    return <div className={styles.pagina}><h1>Registrar encaminhamento</h1><p>Abra a demanda ou a ficha do assistido que deseja encaminhar.</p><div className={styles.acoes}><Link className="botao-secundario" to="/demandas">Demandas</Link><Link className="botao-secundario" to="/assistidos">Assistidos</Link></div></div>
  }
  return (
    <form className={styles.formulario} onSubmit={registrar} noValidate>
      <Link className={styles.voltar} to={origem}><ArrowLeft size={17} aria-hidden="true" />{demanda ? 'Demanda #' + demanda : 'Assistido #' + assistido}</Link>
      <h1>Registrar encaminhamento</h1>
      <fieldset disabled={enviando}>
        <CampoDemanda nome="destino" rotulo="Destino" erro={erros.destino}>
          <input id="destino" name="destino" required maxLength={200} value={campos.destino} onChange={alterarCampo} aria-invalid={!!erros.destino} aria-describedby={erros.destino ? 'destino-erro' : undefined} />
        </CampoDemanda>
        <CampoDemanda nome="data" rotulo="Data" erro={erros.data}>
          <input id="data" name="data" type="date" required value={campos.data} onChange={alterarCampo} aria-invalid={!!erros.data} aria-describedby={erros.data ? 'data-erro' : undefined} />
        </CampoDemanda>
        <CampoDemanda nome="observacao" rotulo="Observação (opcional)">
          <textarea id="observacao" name="observacao" rows={4} value={campos.observacao} onChange={alterarCampo} />
        </CampoDemanda>
        {erro && <p className="aviso-erro" role="alert">{erro}</p>}
        <div className={styles.acoes}><button className="botao-primario" type="submit">{enviando ? 'Registrando…' : 'Registrar encaminhamento'}</button></div>
      </fieldset>
    </form>
  )
}
