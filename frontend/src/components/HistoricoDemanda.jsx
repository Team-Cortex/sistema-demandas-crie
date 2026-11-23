import { estados, dataHora } from '../dominio'
import styles from './HistoricoDemanda.module.css'

export default function HistoricoDemanda({ historico }) {
  return (
    <section className={styles.secao} aria-labelledby="historico">
      <h2 id="historico">Histórico</h2>
      {!historico.length ? <p>Nenhum movimento registrado.</p> :
        <ol className={styles.lista}>
          {historico.map(item => (
            <li key={item.id}>
              <strong>{item.tipo === 'anotacao' ? 'Anotação' : item.estado_anterior ? 'Mudança de estado' : 'Abertura da demanda'}</strong>
              <p>{item.tipo === 'anotacao' ? item.texto : item.estado_anterior ?
                `De ${estados[item.estado_anterior]} para ${estados[item.estado_novo]}` : estados[item.estado_novo]}</p>
              <small>{item.autor_nome}, <time dateTime={item.ocorrido_em}>{dataHora(item.ocorrido_em)}</time></small>
            </li>
          ))}
        </ol>}
    </section>
  )
}
