import { Link } from 'react-router-dom'
import CartaoDemanda from './CartaoDemanda'
import styles from './ListaDemandas.module.css'

// `demandas` é uma lista de objetos da classe Demanda (src/modelos/Demanda.js).
export default function ListaDemandas({ demandas, titulo, mensagemVazia }) {
  if (!demandas.length) return <p className={styles.vazia} role="status">{mensagemVazia}</p>
  return (
    <>
      <table className={styles.tabela} aria-label={titulo}>
        <thead>
          <tr>{['Demanda', 'Estado', 'Responsável', 'Prioridade', 'Prazo'].map(campo => <th key={campo} scope="col">{campo}</th>)}</tr>
        </thead>
        <tbody>
          {demandas.map(demanda => (
            <tr key={demanda.id}>
              <th scope="row">
                <Link to={`/demandas/${demanda.id}`}>
                  <small>nº {demanda.id}</small> {demanda.descricao}
                </Link>
              </th>
              <td>{demanda.rotuloEstado()}</td>
              <td>{demanda.responsavel_nome}</td>
              <td>{demanda.rotuloPrioridade()}</td>
              <td>
                <time dateTime={demanda.prazo}>{demanda.prazoFormatado()}</time>
                {demanda.estaVencida() && <strong className={styles.vencida}>Vencida</strong>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <ul className={styles.cartoes} aria-label={titulo}>
        {demandas.map(demanda => <li key={demanda.id}><CartaoDemanda demanda={demanda} mostrarEstado /></li>)}
      </ul>
    </>
  )
}
