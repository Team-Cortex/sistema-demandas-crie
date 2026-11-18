import { useEffect, useRef } from 'react'
import styles from './Confirmacao.module.css'

export default function Confirmacao({ titulo, children, acao, aoVoltar, aoConfirmar }) {
  const referencia = useRef(null)

  useEffect(() => {
    const dialogo = referencia.current
    dialogo.showModal()
    return () => dialogo.close()
  }, [])

  function voltar() {
    referencia.current.close()
    aoVoltar()
  }

  function fecharComEscape(evento) {
    evento.preventDefault()
    voltar()
  }

  function confirmar() {
    referencia.current.close()
    aoConfirmar()
  }

  return (
    <dialog ref={referencia} className={styles.dialogo} aria-labelledby="titulo-confirmacao" onCancel={fecharComEscape}>
      <h2 id="titulo-confirmacao">{titulo}</h2>
      {children}
      <div className={styles.acoes}>
        <button type="button" className="botao botao-secundario" onClick={voltar}>Voltar</button>
        <button type="button" className="botao botao-primario" onClick={confirmar}>{acao}</button>
      </div>
    </dialog>
  )
}
