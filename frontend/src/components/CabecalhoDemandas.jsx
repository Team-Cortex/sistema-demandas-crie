import { Link } from 'react-router-dom'
import styles from './CabecalhoDemandas.module.css'

export default function CabecalhoDemandas({ titulo, children }) {
  return (
    <header className={styles.cabecalho}>
      <div>
        <h1>{titulo}</h1>
        {children && <p>{children}</p>}
      </div>
      <Link to="/demandas/nova" className="botao botao-primario">Registrar demanda</Link>
    </header>
  )
}
