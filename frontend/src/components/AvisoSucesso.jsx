import { useEffect, useState } from 'react'
import { CheckCircle2 } from 'lucide-react'
import styles from './AvisoSucesso.module.css'

export default function AvisoSucesso({ children }) {
  const [visivel, definirVisivel] = useState(true)
  useEffect(() => {
    definirVisivel(true)
    if (!children) return
    const tempo = window.setTimeout(() => definirVisivel(false), 7000)
    return () => window.clearTimeout(tempo)
  }, [children])
  if (!children || !visivel) return null
  return <p role="status" className={styles.aviso}><CheckCircle2 size={19} aria-hidden="true" />{children}</p>
}
