import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { UserPlus } from 'lucide-react'
import cliente, { lerSessao, mensagemDeErro } from '../../api/cliente'
import { perfis } from '../../dominio'
import Carregando from '../../components/Carregando'
import AvisoSucesso from '../../components/AvisoSucesso'
import Confirmacao from '../../components/Confirmacao'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Usuarios.module.css'

export default function Usuarios() {
  const { state } = useLocation()
  const meuId = lerSessao().usuario.id
  const [usuarios, definirUsuarios] = useState(null)
  const [erroCarga, definirErroCarga] = useState('')
  const [erro, definirErro] = useState('')
  const [tentativa, definirTentativa] = useState(0)
  const [escolhido, definirEscolhido] = useState(null)
  const [enviando, definirEnviando] = useState(false)
  const [sucesso, definirSucesso] = useState(state?.mensagem)

  useEffect(() => {
    const controle = new AbortController()
    cliente.get('/api/usuarios', { signal: controle.signal }).then(({ data }) => definirUsuarios(data))
      .catch(falha => { if (!controle.signal.aborted) definirErroCarga(mensagemDeErro(falha)) })
    return () => controle.abort()
  }, [tentativa])

  function tentarNovamente() {
    definirErroCarga('')
    definirTentativa(tentativa + 1)
  }

  function revisarDesativacao(evento) {
    definirEscolhido(usuarios.find(item => String(item.id) === evento.currentTarget.value))
    definirErro('')
    definirSucesso('')
  }

  function voltar() { definirEscolhido(null) }

  async function desativar() {
    definirEscolhido(null)
    definirEnviando(true)
    try {
      const { data } = await cliente.patch('/api/usuarios/' + escolhido.id + '/desativar')
      definirUsuarios(usuarios.map(item => item.id === data.id ? data : item))
      definirSucesso('Conta de ' + data.nome + ' desativada.')
    } catch (falha) {
      definirErro(mensagemDeErro(falha))
    } finally {
      definirEnviando(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <header className={styles.cabecalho}>
        <h1>Usuários</h1>
        <Link to="/usuarios/novo" className="botao-primario"><UserPlus size={18} aria-hidden="true" />Cadastrar usuário</Link>
      </header>
      <AvisoSucesso>{sucesso}</AvisoSucesso>
      {erro && <p className="aviso-erro" role="alert">{erro}</p>}
      {erroCarga ? <ErroConsulta mensagem={erroCarga} tentarNovamente={tentarNovamente} /> : !usuarios ? <Carregando /> :
        usuarios.length === 0 ? <p>Nenhum usuário encontrado. Use Cadastrar usuário para registrar uma conta.</p> :
          <ul className={styles.lista}>{usuarios.map(item =>
            <li key={item.id}>
              <div className={styles.pessoa}><h2>{item.nome}</h2><p>{item.email}</p></div>
              <p>{perfis[item.perfil]}</p>
              <span className={item.ativo ? styles.ativo : styles.inativo}>{item.ativo ? 'Ativo' : 'Desativado'}</span>
              <div className={styles.acoes}>
                <Link className="botao-secundario" to={'/usuarios/' + item.id + '/editar'} aria-label={'Editar ' + item.nome}>Editar</Link>
                {item.id !== meuId && item.ativo && <button className="botao-secundario" type="button" value={item.id} onClick={revisarDesativacao} disabled={enviando} aria-label={'Desativar ' + item.nome}>Desativar</button>}
              </div>
            </li>)}</ul>}
      {escolhido && <Confirmacao titulo={'Desativar ' + escolhido.nome + '?'} acao="Desativar usuário" aoVoltar={voltar} aoConfirmar={desativar}>
        <p>A pessoa não consegue mais entrar. O histórico dela continua no sistema.</p>
      </Confirmacao>}
    </div>
  )
}
