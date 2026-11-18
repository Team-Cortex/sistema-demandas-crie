import styles from './AvisoSucesso.module.css'

export default function AvisoSucesso({ children }) {
  if (!children) return null
  return <p role="status" className={styles.aviso}>{children}</p>
}
