import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight, Plus, Search } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Assistidos.module.css'

export default function Assistidos() {
  const chave = 'busca-assistidos'
  const [busca, definirBusca] = useState(() => lerRascunho(chave)?.busca || '')
  const [consulta, definirConsulta] = useState(() => lerRascunho(chave)?.consulta || {})
  const [assistidos, definirAssistidos] = useState(null)
  const [erro, definirErro] = useState('')

  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/assistidos', { params: consulta, signal: controlador.signal })
      .then(({ data }) => definirAssistidos(data))
      .catch(falha => { if (!controlador.signal.aborted) definirErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [consulta])

  function consultar(texto) {
    definirErro('')
    definirAssistidos(null)
    definirConsulta(texto ? { busca: texto } : {})
  }

  function buscar(evento) {
    evento.preventDefault()
    const texto = busca.trim()
    guardarRascunho(chave, { busca, consulta: texto ? { busca: texto } : {} })
    consultar(texto)
  }

  function limpar() {
    apagarRascunho(chave)
    definirBusca('')
    consultar('')
  }

  function tentarNovamente() { consultar(consulta.busca) }
  function preencherBusca(evento) {
    definirBusca(evento.target.value)
    guardarRascunho(chave, { busca: evento.target.value, consulta })
  }

  return (
    <div className={styles.pagina}>
      <header className={styles.cabecalho}><h1>Assistidos</h1>
        <Link className="botao-primario" to="/assistidos/novo"><Plus size={18} aria-hidden="true" />Cadastrar assistido</Link>
      </header>
      <form className={styles.painel} onSubmit={buscar}>
        <div className={styles.pesquisa}>
          <label>Buscar pelo nome de tratamento<input type="search" value={busca} onChange={preencherBusca} /></label>
          <button className="botao-secundario"><Search size={18} aria-hidden="true" />Buscar</button>
          {(busca || consulta.busca) && <button type="button" className="botao-secundario" onClick={limpar}>Limpar busca</button>}
        </div>
      </form>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> : !assistidos ? <Carregando /> :
        <section className={styles.painel} aria-label="Lista de assistidos">
          {!assistidos.length ? <p>{consulta.busca ? 'Nenhum assistido encontrado. Tente outro nome de tratamento.' : 'Nenhum assistido cadastrado. Use Cadastrar assistido para começar.'}</p> :
            <ul className={styles.lista}>{assistidos.map(item => <li key={item.id}>
              <Link to={'/assistidos/' + item.id} className={styles.linhaNome}>{item.nome_tratamento}<ChevronRight size={18} aria-hidden="true" /></Link>
            </li>)}</ul>}
        </section>}
    </div>
  )
}
