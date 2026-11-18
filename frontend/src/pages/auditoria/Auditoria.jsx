import { useEffect, useState } from 'react'
import { ChevronLeft, ChevronRight, ListFilter } from 'lucide-react'
import cliente, { apagarRascunho, guardarRascunho, lerRascunho, mensagemDeErro } from '../../api/cliente'
import Carregando from '../../components/Carregando'
import ErroConsulta from '../../components/ErroConsulta'
import { dataHora } from '../../dominio'
import styles from './Auditoria.module.css'

const filtrosVazios = { autor_id: '', assistido_id: '', recurso: '', acao: '', de: '', ate: '' }
const acoes = {
  criar: 'Cadastro', alterar: 'Alteração', consultar: 'Consulta', listar: 'Listagem',
  retificar: 'Retificação', registrar_desfecho: 'Registro de desfecho', emitir: 'Emissão',
}
const recursos = {
  assistido: 'Assistido', evolucao: 'Evolução', encaminhamento: 'Encaminhamento',
  relatorio_demandas: 'Relatório de demandas', relatorio_assistido: 'Relatório do assistido',
}
const colunas = ['Quando', 'Quem', 'Ação', 'Recurso', 'Assistido']

export default function Auditoria() {
  const [filtros, definirFiltros] = useState(() => lerRascunho('auditoria-filtros') || filtrosVazios)
  const [consulta, definirConsulta] = useState(() => lerRascunho('auditoria-consulta') || { pagina: 1 })
  const [dados, definirDados] = useState(null)
  const [erro, definirErro] = useState('')
  const [erroCampo, definirErroCampo] = useState({})
  const [usuarios, definirUsuarios] = useState(null)
  const [erroUsuarios, definirErroUsuarios] = useState('')
  const [tentativa, definirTentativa] = useState(0)

  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/usuarios', { signal: controlador.signal })
      .then(({ data }) => definirUsuarios(data))
      .catch(falha => { if (!controlador.signal.aborted) definirErroUsuarios(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [tentativa])

  useEffect(() => {
    const controlador = new AbortController()
    cliente.get('/api/auditoria', { params: { ...consulta, por_pagina: 20 }, signal: controlador.signal })
      .then(({ data }) => definirDados(data))
      .catch(falha => { if (!controlador.signal.aborted) definirErro(mensagemDeErro(falha)) })
    return () => controlador.abort()
  }, [consulta])

  function consultar(parametros) {
    definirErro('')
    definirDados(null)
    definirConsulta(parametros)
    guardarRascunho('auditoria-consulta', parametros)
  }

  function alterarFiltro(evento) {
    const novos = { ...filtros, [evento.target.name]: evento.target.value }
    definirFiltros(novos)
    definirErroCampo({})
    guardarRascunho('auditoria-filtros', novos)
  }

  function filtrar(evento) {
    evento.preventDefault()
    const erros = {}
    if (filtros.assistido_id && !/^[1-9]\d*$/.test(filtros.assistido_id)) erros.assistido_id = 'Informe o número do assistido.'
    if (filtros.ate && filtros.de > filtros.ate) erros.ate = 'A data inicial não pode ser depois da final.'
    definirErroCampo(erros)
    if (Object.keys(erros).length) {
      evento.currentTarget.elements.namedItem(Object.keys(erros)[0]).focus()
      return
    }
    const parametros = { pagina: 1 }
    for (const [nome, valor] of Object.entries(filtros)) {
      if (valor) parametros[nome] = valor
    }
    consultar(parametros)
  }

  function limparFiltros() {
    apagarRascunho('auditoria-filtros')
    definirFiltros(filtrosVazios)
    definirErroCampo({})
    consultar({ pagina: 1 })
  }

  function tentarNovamente() { consultar({ ...consulta }) }
  function carregarUsuarios() {
    definirErroUsuarios('')
    definirTentativa(tentativa + 1)
  }
  function paginaAnterior() { consultar({ ...consulta, pagina: dados.pagina - 1 }) }
  function proximaPagina() { consultar({ ...consulta, pagina: dados.pagina + 1 }) }
  const totalPaginas = dados ? Math.ceil(dados.total / dados.por_pagina) : 0

  return (
    <div className={styles.pagina}>
      <h1>Auditoria</h1>
      <form onSubmit={filtrar} className={styles.painel} noValidate aria-label="Filtros da auditoria">
        <div className={styles.campos}>
          <label>Autor
            <select name="autor_id" value={filtros.autor_id} onChange={alterarFiltro} disabled={!usuarios}>
              <option value="">Todos os autores</option>
              {usuarios?.map(usuario => <option value={usuario.id} key={usuario.id}>{usuario.nome}</option>)}
            </select>
          </label>
          <label>Assistido (número)
            <input name="assistido_id" inputMode="numeric" value={filtros.assistido_id} onChange={alterarFiltro}
              aria-invalid={!!erroCampo.assistido_id} aria-describedby={erroCampo.assistido_id ? 'erro-assistido' : undefined} />
            {erroCampo.assistido_id && <span id="erro-assistido" className={styles.erroCampo}>{erroCampo.assistido_id}</span>}
          </label>
          <label>Recurso
            <select name="recurso" value={filtros.recurso} onChange={alterarFiltro}>
              <option value="">Todos os recursos</option>
              {Object.entries(recursos).map(([valor, texto]) => <option key={valor} value={valor}>{texto}</option>)}
            </select>
          </label>
          <label>Ação
            <select name="acao" value={filtros.acao} onChange={alterarFiltro}>
              <option value="">Todas as ações</option>
              {Object.entries(acoes).map(([valor, texto]) => <option key={valor} value={valor}>{texto}</option>)}
            </select>
          </label>
          <label>De<input name="de" type="date" value={filtros.de} onChange={alterarFiltro} /></label>
          <label>Até<input name="ate" type="date" value={filtros.ate} onChange={alterarFiltro}
            aria-invalid={!!erroCampo.ate} aria-describedby={erroCampo.ate ? 'erro-ate' : undefined} />
            {erroCampo.ate && <span className={styles.erroCampo} id="erro-ate">{erroCampo.ate}</span>}
          </label>
        </div>
        {!usuarios && (erroUsuarios ? <ErroConsulta mensagem={erroUsuarios} tentarNovamente={carregarUsuarios} /> : <Carregando>Carregando autores…</Carregando>)}
        <div className={styles.acoes}>
          <button className="botao-primario"><ListFilter size={17} aria-hidden="true" />Aplicar filtros</button>
          <button className="botao-secundario" type="button" onClick={limparFiltros}>Limpar filtros</button>
        </div>
      </form>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> :
        !dados ? <Carregando>Carregando registros…</Carregando> :
        !dados.total ? <p className={styles.painel} role="status">Nenhum registro encontrado. Tente outro período ou limpe os filtros.</p> :
        <section className={styles.painel} aria-label="Registros de auditoria">
          <h2>Registros de auditoria <small>{dados.total}</small></h2>
          <table className={styles.tabela} aria-label="Registros de auditoria">
            <thead><tr>{colunas.map(titulo => <th key={titulo} scope="col">{titulo}</th>)}</tr></thead>
            <tbody>{dados.itens.map(item => (
              <tr key={item.id}>
                <td data-rotulo="Quando"><time dateTime={item.ocorrido_em}>{dataHora(item.ocorrido_em)}</time></td>
                <td data-rotulo="Quem">{item.autor_nome}</td>
                <td data-rotulo="Ação">{acoes[item.acao] || item.acao}</td>
                <td data-rotulo="Recurso">{recursos[item.recurso] || item.recurso}{item.recurso_id && ' #' + item.recurso_id}</td>
                <td data-rotulo="Assistido">{item.assistido_id ? '#' + item.assistido_id : 'Sem vínculo'}</td>
              </tr>
            ))}</tbody>
          </table>
          <nav className={styles.paginacao} aria-label="Paginação da auditoria">
            <button className="botao-secundario" type="button" disabled={dados.pagina <= 1} onClick={paginaAnterior}><ChevronLeft size={16} aria-hidden="true" />Anterior</button>
            <span aria-live="polite">Página {dados.pagina} de {totalPaginas}</span>
            <button className="botao-secundario" type="button" disabled={dados.pagina >= totalPaginas} onClick={proximaPagina}>Próxima<ChevronRight size={16} aria-hidden="true" /></button>
          </nav>
        </section>}
    </div>
  )
}
