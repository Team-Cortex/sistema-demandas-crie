import { Printer } from 'lucide-react'
import { dataCurta, dataHora, estados } from '../../dominio'
import ListaDemandas from '../../components/ListaDemandas'
import styles from './Relatorios.module.css'

export default function ResultadoRelatorio({ relatorio, usuarios }) {
  const { emissao, periodo, totais, assistido, filtros } = relatorio
  const responsavel = usuarios.find(pessoa => pessoa.id === filtros?.responsavel_id)
  function imprimir() { window.print() }
  return (
    <section className={styles.resultado} aria-labelledby="titulo-relatorio">
      <header>
        <div>
          <h2 id="titulo-relatorio">{assistido ? 'Acompanhamento de ' + assistido.nome_tratamento : 'Demandas do período'}</h2>
          <p>De {dataCurta(periodo.de)} a {dataCurta(periodo.ate)}</p>
          {filtros?.estado?.length > 0 && <p>Estado: {filtros.estado.map(chave => estados[chave]).join(', ')}</p>}
          {filtros?.categoria && <p>Categoria: {filtros.categoria}</p>}
          {responsavel && <p>Responsável: {responsavel.nome}</p>}
        </div>
        <button className="botao-secundario" onClick={imprimir}><Printer size={18} aria-hidden="true" />Imprimir</button>
      </header>
      {totais && <>
        <dl className={styles.totais}>
          <div><dt>Total</dt><dd>{totais.total}</dd></div>
          {Object.entries(estados).map(([chave, nome]) => <div key={chave}><dt>{nome}</dt><dd>{totais.por_estado[chave]}</dd></div>)}
          <div><dt>Vencidas</dt><dd>{totais.vencidas}</dd></div>
        </dl>
        <ListaDemandas titulo="Demandas do período" demandas={relatorio.itens} mensagemVazia="Nenhuma demanda encontrada para os filtros deste período." />
      </>}
      {assistido && <>
        <h3>Evoluções</h3>
        {relatorio.evolucoes.length ? <ol>{relatorio.evolucoes.map(item => <li key={item.id}>
          <strong>{dataCurta(item.data)} · {item.area_atuacao}</strong>
          <p>{item.descricao}</p><small>{item.autor_nome}</small>
        </li>)}</ol> : <p>Nenhuma evolução no período.</p>}
        <h3>Encaminhamentos</h3>
        {relatorio.encaminhamentos.length ? <ol>{relatorio.encaminhamentos.map(item => <li key={item.id}>
          <strong>{dataCurta(item.data)} · {item.destino}</strong>
          <p>{item.observacao}</p><p>{item.pendente ? 'Pendente' : 'Desfecho registrado'}</p>
          {item.desfecho && <p>{item.desfecho}</p>}
        </li>)}</ol> : <p>Nenhum encaminhamento no período.</p>}
      </>}
      <footer>Emitido por {emissao.autor_nome} em {dataHora(emissao.ocorrido_em)}</footer>
    </section>
  )
}
