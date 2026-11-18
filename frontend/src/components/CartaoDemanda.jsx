import { CalendarDays, ChevronRight, UserRound } from 'lucide-react'
import { Link } from 'react-router-dom'
import { dataCurta, estados, prioridades } from '../dominio'
import styles from './CartaoDemanda.module.css'

export default function CartaoDemanda({ demanda, mostrarEstado = false }) {
  return (
    <Link to={`/demandas/${demanda.id}`} className={styles.cartao}>
      <span className={styles.linha}>
        <span className={styles.numero}>Demanda #{demanda.id}</span>
        <ChevronRight aria-hidden="true" size={16} />
      </span>
      <strong className={styles.descricao}>{demanda.descricao}</strong>
      <span className={styles.etiquetas}>
        <span className={styles.prioridade} data-nivel={demanda.prioridade}>
          Prioridade {prioridades[demanda.prioridade].toLocaleLowerCase('pt-BR')}
        </span>
        {mostrarEstado && <span className={styles.estado}>{estados[demanda.estado]}</span>}
      </span>
      <span className={styles.rodape}>
        <span className={styles.dado}><UserRound aria-hidden="true" size={15} /> {demanda.responsavel_nome}</span>
        <span className={styles.dado}>
          <CalendarDays aria-hidden="true" size={15} /> {dataCurta(demanda.prazo)}
          {demanda.vencida && <strong className={styles.vencida}>Vencida</strong>}
        </span>
      </span>
    </Link>
  )
}
