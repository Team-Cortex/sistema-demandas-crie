import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
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
  const [usuarios, setUsuarios] = useState(null)
  const [erroCarga, setErroCarga] = useState('')
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [escolhido, setEscolhido] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [sucesso, setSucesso] = useState(state?.mensagem)

  useEffect(() => {
    async function buscarUsuarios() {
      try {
        const resposta = await cliente.get('/api/usuarios')
        setUsuarios(resposta.data)
      } catch (falha) {
        setErroCarga(mensagemDeErro(falha))
      }
    }
    buscarUsuarios()
  }, [tentativa])

  function tentarNovamente() {
    setErroCarga('')
    setTentativa(tentativa + 1)
  }

  function revisarDesativacao(evento) {
    setEscolhido(usuarios.find(item => String(item.id) === evento.currentTarget.value))
    setErro('')
    setSucesso('')
  }

  function voltar() {
    setEscolhido(null)
  }

  async function desativar() {
    setEscolhido(null)
    setEnviando(true)
    try {
      const resposta = await cliente.patch('/api/usuarios/' + escolhido.id + '/desativar')
      setUsuarios(usuarios.map(item => item.id === resposta.data.id ? resposta.data : item))
      setSucesso('Conta de ' + resposta.data.nome + ' desativada.')
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className={styles.pagina}>
      <header className={styles.cabecalho}>
        <h1>Usuários</h1>
        <Link to="/usuarios/novo" className="botao-primario">Cadastrar usuário</Link>
      </header>
      <AvisoSucesso>{sucesso}</AvisoSucesso>
      {erro && <p className="aviso-erro" role="alert">{erro}</p>}
      {erroCarga ? <ErroConsulta mensagem={erroCarga} tentarNovamente={tentarNovamente} /> : !usuarios ? <Carregando /> :
        usuarios.length === 0 ? <p>Nenhum usuário encontrado. Use Cadastrar usuário para registrar uma conta.</p> :
          <ul className={styles.lista}>{usuarios.map(item =>
            <li key={item.id}>
              <div className={styles.pessoa}><h2>{item.nome}</h2><p>{item.email}</p></div>
              <p>{perfis[item.perfil]}</p>
              <p className={item.ativo ? undefined : styles.inativo}>{item.ativo ? 'Ativo' : 'Desativado'}</p>
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
