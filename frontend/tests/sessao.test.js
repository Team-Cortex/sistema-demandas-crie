import assert from 'node:assert/strict'
import test from 'node:test'

class Armazenamento {
  getItem(chave) { return this[chave] ?? null }
  setItem(chave, valor) { this[chave] = String(valor) }
  removeItem(chave) { delete this[chave] }
  clear() { for (const chave of Object.keys(this)) delete this[chave] }
}
const storage = new Armazenamento()
Object.defineProperty(globalThis, 'sessionStorage', { configurable: true, value: storage })
const { default: cliente } = await import('../src/api/cliente.js')

// O Axios é privado na classe (#http). Para ver o cabeçalho, a requisição usa um adapter que devolve o que receberia.
async function cabecalhoEnviado() {
  const resposta = await cliente.get('/api/qualquer', {
    adapter: async (config) => ({ data: config.headers.Authorization, status: 200, statusText: 'OK', headers: {}, config }),
  })
  return resposta.data
}

test('rascunho volta para a mesma conta, some para outra conta e sair apaga tudo', async () => {
  cliente.guardarSessao({ usuario: { id: 1 }, token: 'teste' })
  assert.equal(await cabecalhoEnviado(), 'Bearer teste')
  cliente.guardarRascunho('nova', { descricao: 'Exemplo fictício' })

  cliente.esquecerSessao() // é o que acontece no 401 e por inatividade
  assert.equal(await cabecalhoEnviado(), undefined)
  cliente.guardarSessao({ usuario: { id: 1 }, token: 'nova-sessao' })
  assert.equal(cliente.lerRascunho('nova').descricao, 'Exemplo fictício')

  cliente.guardarSessao({ usuario: { id: 2 }, token: 'outra-conta' })
  assert.equal(cliente.lerRascunho('nova'), null)
  assert.ok(!Object.keys(storage).some(chave => chave.startsWith('crie:rascunho:1:')))

  cliente.guardarRascunho('nova', { descricao: 'Outro exemplo' })
  cliente.apagarSessao()
  assert.deepEqual(Object.keys(storage), [])
  assert.equal(cliente.lerSessao().token, undefined)
  assert.equal(await cabecalhoEnviado(), undefined)
})

test('mensagemDeErro usa o texto do servidor e diferencia consulta de envio sem internet', () => {
  assert.equal(cliente.mensagemDeErro({ response: { status: 400, data: { erro: 'Informe o prazo.' } } }), 'Informe o prazo.')
  assert.equal(cliente.mensagemDeErro({ response: { status: 403, data: {} } }), 'Seu perfil não tem acesso a esta operação.')
  assert.match(cliente.mensagemDeErro({ config: { method: 'get' } }), /Confira a internet/)
  assert.match(cliente.mensagemDeErro({ config: { method: 'post' } }), /Seus dados continuam no formulário/)
})
