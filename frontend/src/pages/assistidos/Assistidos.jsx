import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight, Plus, Search } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Assistidos.module.css'

export default function Assistidos() {
  // A busca fica no rascunho para voltar depois que a sessão é renovada.
  const [busca, setBusca] = useState(lerRascunho('busca-assistidos') || '')
  const [consulta, setConsulta] = useState(busca.trim() ? { busca: busca.trim() } : {})
  const [assistidos, setAssistidos] = useState(null)
  const [erro, setErro] = useState('')

  // Busca de novo sempre que a consulta muda (Buscar, Limpar ou Tentar de novo).
  useEffect(() => {
    async function buscarAssistidos() {
      try {
        const resposta = await cliente.get('/api/assistidos', { params: consulta })
        setAssistidos(resposta.data)
      } catch (falha) {
        setErro(mensagemDeErro(falha))
      }
    }
    buscarAssistidos()
  }, [consulta])

  function consultar(texto) {
    setErro('')
    setAssistidos(null)
    setConsulta(texto ? { busca: texto } : {})
  }

  function buscar(evento) {
    evento.preventDefault()
    guardarRascunho('busca-assistidos', busca)
    consultar(busca.trim())
  }

  function limpar() {
    apagarRascunho('busca-assistidos')
    setBusca('')
    consultar('')
  }

  // Um objeto novo, mesmo igual, faz o useEffect buscar de novo.
  function tentarNovamente() {
    consultar(consulta.busca)
  }

  function preencherBusca(evento) {
    setBusca(evento.target.value)
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
