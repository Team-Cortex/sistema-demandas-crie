import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import cliente from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataCurta, setores } from '../../dominio'
import styles from './Reunioes.module.css'

export default function Reunioes() {
  // O setor escolhido fica no rascunho para voltar depois que a sessão é renovada.
  const [setor, setSetor] = useState(cliente.lerRascunho('setor-reunioes') || '')
  const [reunioes, setReunioes] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)

  useEffect(() => {
    async function buscarReunioes() {
      try {
        const resposta = await cliente.get('/api/reunioes', { params: setor ? { setor } : {} })
        setReunioes(resposta.data)
      } catch (falha) {
        setErro(cliente.mensagemDeErro(falha))
      }
    }
    buscarReunioes()
  }, [setor, tentativa])

  function filtrarSetor(evento) {
    setReunioes(null)
    setErro('')
    setSetor(evento.target.value)
    cliente.guardarRascunho('setor-reunioes', evento.target.value)
  }

  function tentarNovamente() {
    setErro('')
    setTentativa(tentativa + 1)
  }

  return (
    <div className={styles.pagina}>
      <header className={styles.cabecalho}>
        <h1>Reuniões</h1>
        <Link to="/reunioes/nova" className="botao-primario">Registrar reunião</Link>
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
                  <strong>{dataCurta(reuniao.data)}, {setores[reuniao.setor]}</strong>
                  <small>Participantes: {reuniao.participantes.map(pessoa => pessoa.nome).join(', ')}</small>
                </Link>
              </li>
            ))}
          </ul>}
      </section>
    </div>
  )
}
