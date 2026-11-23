import { useEffect, useState } from 'react'
import cliente from '../api/cliente'
import CabecalhoDemandas from '../components/CabecalhoDemandas'
import ErroConsulta from '../components/ErroConsulta'
import ListaDemandas from '../components/ListaDemandas'
import Demanda from '../modelos/Demanda'

export default function MinhasDemandas() {
  const [demandas, setDemandas] = useState(null)
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)

  useEffect(() => {
    async function buscarDemandas() {
      try {
        const resposta = await cliente.get('/api/demandas/minhas')
        // Cada item do JSON vira um objeto Demanda, com os métodos que a lista usa.
        setDemandas(resposta.data.map(dados => new Demanda(dados)))
      } catch (falha) {
        setErro(cliente.mensagemDeErro(falha))
      }
    }
    buscarDemandas()
  }, [tentativa])

  function tentarNovamente() {
    setErro('')
    setTentativa(tentativa + 1)
  }

  return (
    <>
      <CabecalhoDemandas titulo="Minhas demandas">Demandas em aberto sob sua responsabilidade, por ordem de prazo.</CabecalhoDemandas>
      {erro && <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} />}
      {!erro && !demandas && <p role="status">Carregando suas demandas…</p>}
      {demandas && <ListaDemandas demandas={demandas} titulo="Minhas demandas" mensagemVazia="Você não tem demandas em aberto." />}
    </>
  )
}
