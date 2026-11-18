import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import CampoDemanda from '../../components/CampoDemanda'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { hojeCrie } from '../../dominio'
import styles from '../assistidos/Assistidos.module.css'

export default function FormEvolucao() {
  const { id, assistidoId } = useParams()
  const navegar = useNavigate()
  const chave = id ? 'retificar-evolucao-' + id : 'lancar-evolucao-' + assistidoId
  const [rascunho, setRascunho] = useState(() => lerRascunho(chave))
  const [origem, setOrigem] = useState(null)
  const [tentativa, setTentativa] = useState(0)
  const [erroConsulta, setErroConsulta] = useState('')
  const [erros, setErros] = useState({})
  const [erroServidor, setErroServidor] = useState('')
  const [salvando, setSalvando] = useState(false)

  useEffect(() => {
    const controlador = new AbortController()
    const caminho = id ? '/api/evolucoes/' + id : '/api/assistidos/' + assistidoId + '/ficha'
    cliente.get(caminho, { signal: controlador.signal }).then(({ data }) => setOrigem(data))
      .catch(falha => { if (!controlador.signal.aborted) setErroConsulta(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [id, assistidoId, tentativa])

  const campos = rascunho ?? {
    data: origem?.data ?? hojeCrie(), area_atuacao: origem?.area_atuacao ?? '', descricao: origem?.descricao ?? '',
  }
  function tentarNovamente() { setErroConsulta(''); setTentativa(tentativa + 1) }
  function preencher(evento) {
    const { name, value } = evento.target
    const atual = { ...campos, [name]: value }
    setRascunho(atual)
    guardarRascunho(chave, atual)
    setErros({ ...erros, [name]: '' })
    setErroServidor('')
  }
  function atributos(nome) {
    return {
      name: nome, id: nome, value: campos[nome], required: true, onChange: preencher,
      'aria-invalid': Boolean(erros[nome]), 'aria-describedby': erros[nome] ? nome + '-erro' : undefined,
    }
  }

  async function salvar(evento) {
    evento.preventDefault()
    const invalidos = {}
    if (!evento.currentTarget.elements.data.validity.valid) invalidos.data = 'Informe a data da evolução.'
    if (!campos.area_atuacao.trim()) invalidos.area_atuacao = 'Informe a área de atuação.'
    else if ([...campos.area_atuacao].length > 80) invalidos.area_atuacao = 'A área de atuação aceita até 80 caracteres.'
    if (!campos.descricao.trim()) invalidos.descricao = 'Escreva a descrição da evolução.'
    setErros(invalidos)
    const primeiro = Object.keys(invalidos)[0]
    if (primeiro) {
      evento.currentTarget.elements[primeiro].focus()
      return
    }
    const valores = { data: campos.data, area_atuacao: campos.area_atuacao.trim(), descricao: campos.descricao.trim() }
    const mudancas = id && Object.fromEntries(Object.entries(valores).filter(([nome, valor]) => valor !== origem[nome]))
    if (id && !Object.keys(mudancas).length) {
      setErroServidor('Informe o que muda na retificação.')
      return
    }
    setErroServidor('')
    setSalvando(true)
    try {
      const { data } = id ? await cliente.patch('/api/evolucoes/' + id, mudancas) :
        await cliente.post('/api/assistidos/' + assistidoId + '/evolucoes', valores)
      apagarRascunho(chave)
      navegar('/evolucoes/' + data.id, { replace: true, state: { mensagem: id ? 'Evolução retificada.' : 'Evolução lançada.' } })
    } catch (falha) {
      setErroServidor(mensagemDeErro(falha))
      setSalvando(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <Link className={styles.voltar} to={id ? '/evolucoes/' + id : '/assistidos/' + assistidoId}><ArrowLeft size={17} aria-hidden="true" />{id ? 'Versões da evolução' : 'Ficha do assistido'}</Link>
      <h1>{id ? 'Retificar evolução' : 'Lançar evolução'}</h1>
      {erroConsulta ? <ErroConsulta mensagem={erroConsulta} tentarNovamente={tentarNovamente} /> : !origem ? <Carregando /> :
        id && !origem.vigente ? <p className={styles.painel}>Esta versão já foi retificada. <Link className={styles.link} to={'/evolucoes/' + origem.retificada_por_id}>Ver versão seguinte</Link></p> :
          <form className={styles.formulario} onSubmit={salvar} noValidate>
            {id ? <p>A versão atual fica guardada no histórico.</p> : <p>Assistido: <strong>{origem.assistido.nome_tratamento}</strong></p>}
            <fieldset className={styles.campos} disabled={salvando}>
              <CampoDemanda nome="data" rotulo="Data" erro={erros.data}><input {...atributos('data')} type="date" min="0001-01-01" max="9999-12-31" /></CampoDemanda>
              <CampoDemanda nome="area_atuacao" rotulo="Área de atuação" erro={erros.area_atuacao}><input {...atributos('area_atuacao')} maxLength={80} /></CampoDemanda>
              <CampoDemanda nome="descricao" rotulo="Descrição" erro={erros.descricao}><textarea {...atributos('descricao')} rows="5" /></CampoDemanda>
              {erroServidor && <p role="alert" className="aviso-erro">{erroServidor}</p>}
              <div className={styles.acoes}><button className="botao-primario">{salvando ? 'Salvando…' : id ? 'Retificar' : 'Lançar evolução'}</button></div>
            </fieldset>
          </form>}
    </div>
  )
}
