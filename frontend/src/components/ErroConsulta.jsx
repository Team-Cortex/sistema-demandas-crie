export default function ErroConsulta({ mensagem, tentarNovamente }) {
  return (
    <div className="aviso-erro" role="alert">
      <p>{mensagem}</p>
      <button type="button" className="botao botao-secundario" onClick={tentarNovamente}>
        Tentar de novo
      </button>
    </div>
  )
}
