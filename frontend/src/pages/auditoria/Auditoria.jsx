import { useEffect, useState } from 'react'
import cliente from '../../api/cliente'
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
  // Filtros e página ficam no rascunho para voltarem depois que a sessão é renovada.
  const [filtros, setFiltros] = useState(cliente.lerRascunho('auditoria-filtros') || filtrosVazios)
  const [consulta, setConsulta] = useState(cliente.lerRascunho('auditoria-consulta') || { pagina: 1 })
  const [dados, setDados] = useState(null)
  const [erro, setErro] = useState('')
  const [erroPeriodo, setErroPeriodo] = useState('')
  const [usuarios, setUsuarios] = useState(null)
  const [erroUsuarios, setErroUsuarios] = useState('')
  const [tentativa, setTentativa] = useState(0)

  useEffect(() => {
    async function buscarUsuarios() {
      try {
        const resposta = await cliente.get('/api/usuarios')
        setUsuarios(resposta.data)
      } catch (falha) {
        setErroUsuarios(cliente.mensagemDeErro(falha))
      }
    }
    buscarUsuarios()
  }, [tentativa])

  // Busca de novo sempre que a consulta muda (filtros, página ou Tentar de novo).
  useEffect(() => {
    async function buscarRegistros() {
      try {
        const resposta = await cliente.get('/api/auditoria', { params: { ...consulta, por_pagina: 20 } })
        setDados(resposta.data)
      } catch (falha) {
        setErro(cliente.mensagemDeErro(falha))
      }
    }
    buscarRegistros()
  }, [consulta])

  function consultar(parametros) {
    setErro('')
    setDados(null)
    setConsulta(parametros)
    cliente.guardarRascunho('auditoria-consulta', parametros)
  }

  function alterarFiltro(evento) {
    const novos = { ...filtros, [evento.target.name]: evento.target.value }
    setFiltros(novos)
    setErroPeriodo('')
    cliente.guardarRascunho('auditoria-filtros', novos)
  }

  function filtrar(evento) {
    evento.preventDefault()
    if (filtros.de && filtros.ate && filtros.ate < filtros.de) {
      setErroPeriodo('Escolha uma data final igual ou posterior à inicial.')
      evento.currentTarget.elements.ate.focus()
      return
    }
    const parametros = { pagina: 1 }
    for (const [nome, valor] of Object.entries(filtros)) {
      if (valor) parametros[nome] = valor
    }
    consultar(parametros)
  }

  function limparFiltros() {
    cliente.apagarRascunho('auditoria-filtros')
    setFiltros(filtrosVazios)
    setErroPeriodo('')
    consultar({ pagina: 1 })
  }

  // Um objeto novo, mesmo igual, faz o useEffect buscar de novo.
  function tentarNovamente() {
    consultar({ ...consulta })
  }

  function carregarUsuarios() {
    setErroUsuarios('')
    setTentativa(tentativa + 1)
  }

  // A página vem da consulta, não dos dados: durante a busca os dados ficam vazios.
  function paginaAnterior() {
    consultar({ ...consulta, pagina: consulta.pagina - 1 })
  }

  function proximaPagina() {
    consultar({ ...consulta, pagina: consulta.pagina + 1 })
  }
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
            <input name="assistido_id" type="number" min="1" value={filtros.assistido_id} onChange={alterarFiltro} />
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
            aria-invalid={Boolean(erroPeriodo)} aria-describedby={erroPeriodo ? 'erro-ate' : undefined} />
            {erroPeriodo && <span className={styles.erroCampo} id="erro-ate">{erroPeriodo}</span>}
          </label>
        </div>
        {!usuarios && (erroUsuarios ? <ErroConsulta mensagem={erroUsuarios} tentarNovamente={carregarUsuarios} /> : <Carregando>Carregando autores…</Carregando>)}
        <div className={styles.acoes}>
          <button className="botao-primario">Aplicar filtros</button>
          <button className="botao-secundario" type="button" onClick={limparFiltros}>Limpar filtros</button>
        </div>
      </form>
      {erro ? <ErroConsulta mensagem={erro} tentarNovamente={tentarNovamente} /> :
        !dados ? <Carregando>Carregando registros…</Carregando> :
        !dados.total ? <p className={styles.painel} role="status">Nenhum registro encontrado. Tente outro período ou limpe os filtros.</p> :
        <section className={styles.painel} aria-label="Registros de auditoria">
          <h2>Registros de auditoria ({dados.total})</h2>
          <table className={styles.tabela} aria-label="Registros de auditoria">
            <thead><tr>{colunas.map(titulo => <th key={titulo} scope="col">{titulo}</th>)}</tr></thead>
            <tbody>{dados.itens.map(item => (
              <tr key={item.id}>
                <td data-rotulo="Quando"><time dateTime={item.ocorrido_em}>{dataHora(item.ocorrido_em)}</time></td>
                <td data-rotulo="Quem">{item.autor_nome}</td>
                <td data-rotulo="Ação">{acoes[item.acao] || item.acao}</td>
                <td data-rotulo="Recurso">{recursos[item.recurso] || item.recurso}{item.recurso_id && ' nº ' + item.recurso_id}</td>
                <td data-rotulo="Assistido">{item.assistido_id ? 'Assistido nº ' + item.assistido_id : 'Sem vínculo'}</td>
              </tr>
            ))}</tbody>
          </table>
          <nav className={styles.paginacao} aria-label="Paginação da auditoria">
            <button className="botao-secundario" type="button" disabled={dados.pagina <= 1} onClick={paginaAnterior}>Anterior</button>
            <span aria-live="polite">Página {dados.pagina} de {totalPaginas}</span>
            <button className="botao-secundario" type="button" disabled={dados.pagina >= totalPaginas} onClick={proximaPagina}>Próxima</button>
          </nav>
        </section>}
    </div>
  )
}
