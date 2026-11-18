import { CheckCircle2 } from 'lucide-react'
import styles from './AvisoSucesso.module.css'

export default function AvisoSucesso({ children }) {
  if (!children) return null
  return <p role="status" className={styles.aviso}><CheckCircle2 size={19} aria-hidden="true" />{children}</p>
}
