import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import cliente from '../../api/cliente'
import { hojeCrie } from '../../dominio'
import CampoDemanda from '../../components/CampoDemanda'
import styles from './Encaminhamentos.module.css'

export default function RegistrarEncaminhamento() {
  const navegar = useNavigate()
  // Vindo da demanda ou da ficha do assistido ("Encaminhar"), o endereço traz o id de origem.
  const [parametros] = useSearchParams()
  const demanda = parametros.get('demanda_id')
  const assistido = parametros.get('assistido_id')
  const origem = demanda ? '/demandas/' + demanda : '/assistidos/' + assistido
  const chave = 'encaminhar:' + origem
  const [campos, setCampos] = useState(cliente.lerRascunho(chave) || { destino: '', data: hojeCrie(), observacao: '' })
  const [erros, setErros] = useState({})
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  function alterarCampo(evento) {
    const { name, value } = evento.target
    const valores = { ...campos, [name]: value }
    setCampos(valores)
    cliente.guardarRascunho(chave, valores)
    setErros({ ...erros, [name]: '' })
    setErro('')
  }

  async function registrar(evento) {
    evento.preventDefault()
    const falhas = {}
    if (!campos.destino.trim()) falhas.destino = 'Informe o destino.'
    if (!campos.data) falhas.data = 'Informe a data do encaminhamento.'
    setErros(falhas)
    const primeiro = Object.keys(falhas)[0]
    if (primeiro) {
      evento.currentTarget.elements[primeiro].focus()
      return
    }
    setEnviando(true)
    setErro('')
    try {
      const dados = { destino: campos.destino.trim(), data: campos.data, observacao: campos.observacao.trim() }
      if (demanda) dados.demanda_id = Number(demanda)
      if (assistido) dados.assistido_id = Number(assistido)
      await cliente.post('/api/encaminhamentos', dados)
      cliente.apagarRascunho(chave)
      navegar('/encaminhamentos', { replace: true, state: { mensagem: 'Encaminhamento registrado.' } })
    } catch (falha) {
      setErro(cliente.mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  if (!demanda && !assistido) {
    return <div className={styles.pagina}><h1>Registrar encaminhamento</h1><p>Abra a demanda ou a ficha do assistido que deseja encaminhar.</p><div className={styles.acoes}><Link className="botao-secundario" to="/demandas">Demandas</Link><Link className="botao-secundario" to="/assistidos">Assistidos</Link></div></div>
  }
  return (
    <form className={styles.formulario} onSubmit={registrar} noValidate>
      <Link className="voltar" to={origem}>{demanda ? 'Voltar para a demanda nº ' + demanda : 'Voltar para o assistido nº ' + assistido}</Link>
      <h1>Registrar encaminhamento</h1>
      <fieldset disabled={enviando}>
        <CampoDemanda nome="destino" rotulo="Destino" erro={erros.destino}>
          <input id="destino" name="destino" required maxLength={200} value={campos.destino} onChange={alterarCampo} aria-invalid={Boolean(erros.destino)} aria-describedby={erros.destino ? 'destino-erro' : undefined} />
        </CampoDemanda>
        <CampoDemanda nome="data" rotulo="Data" erro={erros.data}>
          <input id="data" name="data" type="date" required value={campos.data} onChange={alterarCampo} aria-invalid={Boolean(erros.data)} aria-describedby={erros.data ? 'data-erro' : undefined} />
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
