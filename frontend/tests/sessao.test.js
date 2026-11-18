import assert from 'node:assert/strict'
import test from 'node:test'

test('expirar permite retomar o rascunho só com a mesma conta e sair o descarta', async () => {
  class Armazenamento {
    getItem(chave) { return this[chave] ?? null }
    setItem(chave, valor) { this[chave] = String(valor) }
    removeItem(chave) { delete this[chave] }
  }
  const storage = new Armazenamento()
  Object.defineProperty(globalThis, 'sessionStorage', { configurable: true, value: storage })
  let destino
  globalThis.window = { location: {
    pathname: '/demandas/nova', search: '', replace(rota) { destino = rota },
  } }
  const { default: cliente, guardarSessao, expirarSessao, apagarSessao, lerSessao,
    guardarRascunho, lerRascunho } = await import('../src/api/cliente.js')
  const usuario = { id: 1 }
  guardarSessao({ usuario, token: 'teste' })
  guardarRascunho('nova', { descricao: 'Exemplo fictício' })
  expirarSessao()
  assert.equal(destino, '/entrar')
  assert.equal(storage.getItem('crie:retorno'), '/demandas/nova')
  assert.equal(lerSessao().token, null)
  assert.equal(cliente.defaults.headers.common.Authorization, undefined)
  guardarSessao({ usuario, token: 'nova-sessao' })
  assert.equal(lerRascunho('nova').descricao, 'Exemplo fictício')
  expirarSessao()
  guardarSessao({ usuario: { id: 2 }, token: 'outra-conta' })
  assert.equal(lerRascunho('nova'), null)
  assert.ok(!Object.keys(storage).some(chave => chave.startsWith('crie:rascunho:')))
  guardarRascunho('nova', { descricao: 'Outro exemplo' })
  apagarSessao()
  assert.deepEqual(Object.keys(storage), [])
})
