import { useEffect, useState } from 'react'
import { CalendarDays, ChevronRight, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import cliente, { mensagemDeErro, lerRascunho, guardarRascunho } from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataCurta, setores } from '../../dominio'
import styles from './Reunioes.module.css'

export default function Reunioes() {
  const [setor, definirSetor] = useState(() => lerRascunho('setor-reunioes') || '')
  const [reunioes, definirReunioes] = useState(null)
  const [erro, definirErro] = useState('')
  const [tentativa, definirTentativa] = useState(0)

  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/reunioes', { params: setor ? { setor } : {}, signal: controlador.signal })
      .then(({ data }) => definirReunioes(data))
      .catch(falha => { if (!controlador.signal.aborted) definirErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [setor, tentativa])

  function filtrarSetor(evento) {
    definirReunioes(null)
    definirErro('')
    definirSetor(evento.target.value)
    guardarRascunho('setor-reunioes', evento.target.value)
  }

  function tentarNovamente() {
    definirErro('')
    definirTentativa(tentativa + 1)
  }

  return (
    <div className={styles.pagina}>
      <header className={styles.cabecalho}>
        <h1>Reuniões</h1>
        <Link to="/reunioes/nova" className="botao-primario"><Plus aria-hidden="true" size={18} />Registrar reunião</Link>
      </header>
      <section className={styles.painel} aria-label="Lista de reuniões">
        <div className={styles.filtro}>
          <label htmlFor="setor">Setor</label>
          <select id="setor" value={setor} onChange={filtrarSetor}>
            <option value="">Todos os setores</option>
            {Object.entries(setores).map(([valor, nome]) => <option key={valor} value={valor}>{nome}</option>)}
          </select>
        </div>
        {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> :
          !reunioes ? <Carregando>Carregando reuniões…</Carregando> :
          !reunioes.length ? <p role="status">{setor ? 'Nenhuma reunião neste setor. Escolha outro setor ou registre uma reunião.' : 'Nenhuma reunião registrada. Use Registrar reunião para começar.'}</p> :
          <ul className={styles.lista}>
            {reunioes.map(reuniao => (
              <li key={reuniao.id}>
                <Link to={'/reunioes/' + reuniao.id} className={styles.linha}>
                  <span className={styles.icone}><CalendarDays size={20} aria-hidden="true" /></span>
                  <span><strong>{dataCurta(reuniao.data)} · {setores[reuniao.setor]}</strong><small>Participantes: {reuniao.participantes.map(pessoa => pessoa.nome).join(', ')}</small></span>
                  <ChevronRight size={18} aria-hidden="true" />
                </Link>
              </li>
            ))}
          </ul>}
      </section>
    </div>
  )
}
