import assert from 'node:assert/strict'
import test from 'node:test'

test('rascunho volta para a mesma conta, some para outra conta e sair apaga tudo', async () => {
  class Armazenamento {
    getItem(chave) { return this[chave] ?? null }
    setItem(chave, valor) { this[chave] = String(valor) }
    removeItem(chave) { delete this[chave] }
    clear() { for (const chave of Object.keys(this)) delete this[chave] }
  }
  const storage = new Armazenamento()
  Object.defineProperty(globalThis, 'sessionStorage', { configurable: true, value: storage })
  const { default: cliente, guardarSessao, apagarSessao, lerSessao,
    guardarRascunho, lerRascunho } = await import('../src/api/cliente.js')

  guardarSessao({ usuario: { id: 1 }, token: 'teste' })
  assert.equal(cliente.defaults.headers.common.Authorization, 'Bearer teste')
  guardarRascunho('nova', { descricao: 'Exemplo fictício' })

  storage.removeItem('crie:sessao') // é o que o interceptador faz no 401
  guardarSessao({ usuario: { id: 1 }, token: 'nova-sessao' })
  assert.equal(lerRascunho('nova').descricao, 'Exemplo fictício')

  guardarSessao({ usuario: { id: 2 }, token: 'outra-conta' })
  assert.equal(lerRascunho('nova'), null)
  assert.ok(!Object.keys(storage).some(chave => chave.startsWith('crie:rascunho:1:')))

  guardarRascunho('nova', { descricao: 'Outro exemplo' })
  apagarSessao()
  assert.deepEqual(Object.keys(storage), [])
  assert.equal(lerSessao().token, undefined)
  assert.equal(cliente.defaults.headers.common.Authorization, undefined)
})
