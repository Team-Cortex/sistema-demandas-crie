import styles from './CampoDemanda.module.css'

export default function CampoDemanda({ nome, rotulo, erro, children }) {
  return (
    <div className={styles.campo}>
      <label htmlFor={nome}>{rotulo}</label>
      {children}
      {erro && <span id={nome + '-erro'} className={styles.erro}>{erro}</span>}
    </div>
  )
}
