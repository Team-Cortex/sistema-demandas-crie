import styles from './Carregando.module.css'

export default function Carregando({ children = 'Carregando…' }) {
  return (
    <div role="status" className={styles.bloco}>
      <span>{children}</span>
      <div aria-hidden="true" /><div aria-hidden="true" />
    </div>
  )
}
