import { Link } from 'react-router-dom'
import styles from './CartaoDemanda.module.css'

// `demanda` é um objeto da classe Demanda (src/modelos/Demanda.js).
export default function CartaoDemanda({ demanda, mostrarEstado = false }) {
  return (
    <Link to={`/demandas/${demanda.id}`} className={styles.cartao}>
      <span className={styles.numero}>
        Demanda nº {demanda.id}{mostrarEstado && `, ${demanda.rotuloEstado().toLocaleLowerCase('pt-BR')}`}
      </span>
      <strong>{demanda.descricao}</strong>
      <span>Prioridade {demanda.rotuloPrioridade().toLocaleLowerCase('pt-BR')}</span>
      <span>Responsável: {demanda.responsavel_nome}</span>
      <span>
        Prazo: {demanda.prazoFormatado()}
        {demanda.estaVencida() && <strong className={styles.vencida}> (vencida)</strong>}
      </span>
    </Link>
  )
}
