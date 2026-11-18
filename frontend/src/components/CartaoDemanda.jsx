import { Link } from 'react-router-dom'
import { dataCurta, estados, prioridades } from '../dominio'
import styles from './CartaoDemanda.module.css'

export default function CartaoDemanda({ demanda, mostrarEstado = false }) {
  return (
    <Link to={`/demandas/${demanda.id}`} className={styles.cartao}>
      <span className={styles.numero}>
        Demanda nº {demanda.id}{mostrarEstado && `, ${estados[demanda.estado].toLocaleLowerCase('pt-BR')}`}
      </span>
      <strong>{demanda.descricao}</strong>
      <span>Prioridade {prioridades[demanda.prioridade].toLocaleLowerCase('pt-BR')}</span>
      <span>Responsável: {demanda.responsavel_nome}</span>
      <span>
        Prazo: {dataCurta(demanda.prazo)}
        {demanda.vencida && <strong className={styles.vencida}> (vencida)</strong>}
      </span>
    </Link>
  )
}
