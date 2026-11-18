import { useEffect, useState } from 'react'
import { Bell, Circle, CircleAlert, CircleDot, Clock3, Columns3 } from 'lucide-react'
import { Link } from 'react-router-dom'
import cliente, { lerSessao, mensagemDeErro } from '../api/cliente'
import CabecalhoDemandas from '../components/CabecalhoDemandas'
import CartaoDemanda from '../components/CartaoDemanda'
import ErroConsulta from '../components/ErroConsulta'
import { dataCurta, estados } from '../dominio'
import styles from './Painel.module.css'

const colunas = ['aberta', 'em_andamento', 'aguardando_terceiros']
const indicadores = [
  { chave: 'aberta', nome: 'Abertas', Icone: Circle },
  { chave: 'em_andamento', nome: 'Em andamento', Icone: CircleDot },
  { chave: 'aguardando_terceiros', nome: 'Aguardando terceiros', Icone: Clock3 },
  { chave: 'vencidas', nome: 'Vencidas', Icone: CircleAlert },
]

export default function Painel() {
  const [painel, setPainel] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const { avisos } = lerSessao()

  // Busca de novo quando a pessoa clica em "Tentar de novo" (tentativa muda).
  useEffect(() => {
    async function buscarPainel() {
      try {
        const resposta = await cliente.get('/api/demandas/painel')
        setPainel(resposta.data)
      } catch (falha) {
        setErro(mensagemDeErro(falha))
      }
    }
    buscarPainel()
  }, [tentativa])

  function tentarNovamente() {
    setErro('')
    setTentativa(tentativa + 1)
  }

  return (
    <>
      <CabecalhoDemandas titulo="Painel de demandas" />
      {erro && <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} />}
      {!painel && !erro && <p role="status">Carregando painel…</p>}
      {painel && (
        <dl className={styles.resumo} aria-label="Totais por estado e prazo">
          {indicadores.map(({ chave, nome, Icone }) => (
            <div key={chave} data-indicador={chave}>
              <dt><Icone size={17} aria-hidden="true" />{nome}</dt>
              <dd>{chave === 'vencidas' ? painel.vencidas : painel.totais[chave]}</dd>
            </div>
          ))}
        </dl>
      )}
      {avisos?.demandas.length > 0 && (
        <details className={styles.avisos}>
          <summary>
            <Bell size={18} aria-hidden="true" />
            <span>Você tem {avisos.vencidas} {avisos.vencidas === 1 ? 'demanda vencida' : 'demandas vencidas'} e {avisos.perto_do_prazo} perto do prazo</span>
          </summary>
          <ul>
            {avisos.demandas.map(demanda => (
              <li key={demanda.id}>
                <Link to={`/demandas/${demanda.id}`}>Demanda nº {demanda.id} · {dataCurta(demanda.prazo)} · {demanda.vencida ? 'Vencida' : 'Perto do prazo'}</Link>
              </li>
            ))}
          </ul>
        </details>
      )}
      {painel && (
        <section aria-labelledby="quadro-demandas">
          <div className={styles.cabecalhoQuadro}>
            <Columns3 size={20} aria-hidden="true" />
            <h2 id="quadro-demandas">Demandas por estado</h2>
            <span>{painel.total} no total</span>
          </div>
          <div className={styles.quadro}>
            {colunas.map(estado => (
              <section className={styles.coluna} key={estado} data-estado={estado} aria-label={estados[estado]}>
                <h3>{estados[estado]} <span>{painel.totais[estado]}</span></h3>
                {painel.por_estado[estado].length ? (
                  <ul>
                    {painel.por_estado[estado].map(demanda => <li key={demanda.id}><CartaoDemanda demanda={demanda} /></li>)}
                  </ul>
                ) : <p className={styles.vazia}>Nenhuma demanda neste estado.</p>}
              </section>
            ))}
          </div>
        </section>
      )}
    </>
  )
}
