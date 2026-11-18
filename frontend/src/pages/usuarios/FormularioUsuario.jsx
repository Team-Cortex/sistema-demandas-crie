import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import cliente, { apagarRascunho, guardarRascunho, guardarSessao, lerRascunho, lerSessao, mensagemDeErro } from '../../api/cliente'
import { perfis } from '../../dominio'
import Carregando from '../../components/Carregando'
import CampoDemanda from '../../components/CampoDemanda'
import ErroConsulta from '../../components/ErroConsulta'
import styles from './Usuarios.module.css'

export default function FormularioUsuario() {
  const { id } = useParams()
  const navegar = useNavigate()
  const chave = 'usuario:' + (id || 'novo')
  const minhaConta = id === String(lerSessao().usuario.id)
  const [original, setOriginal] = useState(null)
  const [rascunho, setRascunho] = useState(lerRascunho(chave) || {})
  const [senha, setSenha] = useState('')
  const [erros, setErros] = useState({})
  const [erroCarga, setErroCarga] = useState('')
  const [erro, setErro] = useState('')
  const [tentativa, setTentativa] = useState(0)
  const [enviando, setEnviando] = useState(false)
  // O que foi digitado (rascunho) vale mais que o que veio da API.
  const campos = { nome: '', email: '', perfil: '', ...original, ...rascunho }

  useEffect(() => {
    async function buscarUsuario() {
      try {
        const resposta = await cliente.get('/api/usuarios/' + id)
        setOriginal(resposta.data)
      } catch (falha) {
        setErroCarga(mensagemDeErro(falha))
      }
    }
    if (id) buscarUsuario()
  }, [id, tentativa])

  function tentarNovamente() {
    setErroCarga('')
    setTentativa(tentativa + 1)
  }

  function alterarCampo(evento) {
    const { name, value } = evento.target
    if (name === 'senha') setSenha(value)
    else {
      const valores = { ...rascunho, [name]: value }
      setRascunho(valores)
      guardarRascunho(chave, valores)
    }
    setErros({ ...erros, [name]: '' })
    setErro('')
  }

  function atributos(nome) {
    return {
      id: nome, name: nome, value: nome === 'senha' ? senha : campos[nome], required: true, onChange: alterarCampo,
      'aria-invalid': Boolean(erros[nome]), 'aria-describedby': erros[nome] ? nome + '-erro' : undefined,
    }
  }

  async function salvarUsuario(evento) {
    evento.preventDefault()
    const falhas = {}
    if (!campos.nome.trim()) falhas.nome = 'Informe o nome.'
    if (!id && !campos.email.includes('@')) falhas.email = 'Informe um e-mail válido.'
    if (!campos.perfil) falhas.perfil = 'Escolha o perfil.'
    if (!id && senha.length < 8) falhas.senha = 'A senha precisa ter no mínimo 8 caracteres.'
    setErros(falhas)
    if (Object.keys(falhas).length) {
      evento.currentTarget.elements[Object.keys(falhas)[0]].focus()
      return
    }
    setErro('')
    setEnviando(true)
    try {
      const dados = { nome: campos.nome.trim() }
      if (!minhaConta) dados.perfil = campos.perfil
      if (id) {
        const resposta = await cliente.patch('/api/usuarios/' + id, dados)
        // O topo da tela lê o nome da sessão; sem isso, ele ficaria com o nome antigo.
        if (minhaConta) {
          const sessao = lerSessao()
          guardarSessao({ ...sessao, usuario: { ...sessao.usuario, nome: resposta.data.nome } })
        }
      } else {
        await cliente.post('/api/usuarios', { ...dados, email: campos.email.trim(), senha })
      }
      apagarRascunho(chave)
      navegar('/usuarios', { replace: true, state: { mensagem: id ? 'Usuário atualizado.' : 'Usuário cadastrado.' } })
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className={styles.formulario}>
      <Link className="voltar" to="/usuarios">Voltar para usuários</Link>
      <h1>{id ? 'Editar usuário' : 'Cadastrar usuário'}</h1>
      {erroCarga ? <ErroConsulta mensagem={erroCarga} tentarNovamente={tentarNovamente} /> : id && !original ? <Carregando /> :
        <form onSubmit={salvarUsuario} noValidate>
          <fieldset disabled={enviando}>
            <CampoDemanda nome="nome" rotulo="Nome" erro={erros.nome}><input {...atributos('nome')} maxLength={120} /></CampoDemanda>
            {!id && <CampoDemanda nome="email" rotulo="E-mail" erro={erros.email}><input {...atributos('email')} type="email" maxLength={254} autoComplete="off" /></CampoDemanda>}
            <CampoDemanda nome="perfil" rotulo="Perfil" erro={erros.perfil}>
              <select {...atributos('perfil')} disabled={minhaConta}>
                <option value="">Selecione o perfil</option>
                {Object.entries(perfis).map(([valor, rotulo]) => <option key={valor} value={valor}>{rotulo}</option>)}
              </select>
            </CampoDemanda>
            {!id && <CampoDemanda nome="senha" rotulo="Senha inicial (mínimo de 8 caracteres)" erro={erros.senha}><input {...atributos('senha')} type="password" minLength={8} autoComplete="new-password" /></CampoDemanda>}
            {erro && <p className="aviso-erro" role="alert">{erro}</p>}
            <div className={styles.acoes}><button className="botao-primario" type="submit">{enviando ? 'Salvando…' : id ? 'Salvar alterações' : 'Cadastrar usuário'}</button></div>
          </fieldset>
        </form>}
    </div>
  )
}
