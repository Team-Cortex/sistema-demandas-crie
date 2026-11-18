import test from 'node:test'
import assert from 'node:assert/strict'
import { transicoes, validarDemanda } from '../src/pages/regrasDemanda.js'

const opcoes = { usuarios: [{ id: 2 }], reunioes: [{ id: 4 }], assistidos: [] }
const campos = {
  descricao: 'Verificar a vaga fictícia', prioridade: 'baixa', responsavel_id: '2',
  prazo: '2024-02-29', reuniao_id: '4', assistido_id: '', categoria: '',
}

test('aceita demanda sem assistido ou categoria e prazo no passado', () => {
  assert.deepEqual(validarDemanda(campos, opcoes), {})
})

test('indica os campos inválidos, inclusive seleções antigas do rascunho', () => {
  const erros = validarDemanda({
    descricao: ' ', prioridade: 'urgente', responsavel_id: '7', prazo: '2026-02-29',
    reuniao_id: '', assistido_id: '9', categoria: 'a'.repeat(81),
  }, opcoes)
  assert.deepEqual(Object.keys(erros).sort(), Object.keys(campos).sort())
})

test('cancelamento e conclusão encerram as transições', () => {
  assert.deepEqual(transicoes.cancelada, [])
  assert.deepEqual(transicoes.concluida, [])
  assert.deepEqual(transicoes.aberta, ['em_andamento', 'cancelada'])
  assert.deepEqual(transicoes.em_andamento, ['aguardando_terceiros', 'concluida', 'cancelada'])
  assert.deepEqual(transicoes.aguardando_terceiros, ['em_andamento', 'cancelada'])
})
