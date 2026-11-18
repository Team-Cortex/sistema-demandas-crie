import test from 'node:test'
import assert from 'node:assert/strict'
import { transicoes, validarDemanda } from '../src/pages/regrasDemanda.js'

const campos = {
  descricao: 'Verificar a vaga fictícia', prioridade: 'baixa', responsavel_id: '2',
  prazo: '2024-02-29', reuniao_id: '4', assistido_id: '', categoria: '',
}

test('aceita demanda sem assistido ou categoria e prazo no passado', () => {
  assert.deepEqual(validarDemanda(campos), {})
})

test('indica os campos obrigatórios vazios e a categoria longa', () => {
  const erros = validarDemanda({
    descricao: ' ', prioridade: '', responsavel_id: '', prazo: '',
    reuniao_id: '', assistido_id: '', categoria: 'a'.repeat(81),
  })
  assert.deepEqual(Object.keys(erros).sort(), ['categoria', 'descricao', 'prazo', 'prioridade', 'responsavel_id', 'reuniao_id'])
})

test('cancelamento e conclusão encerram as transições', () => {
  assert.deepEqual(transicoes.cancelada, [])
  assert.deepEqual(transicoes.concluida, [])
  assert.deepEqual(transicoes.aberta, ['em_andamento', 'cancelada'])
  assert.deepEqual(transicoes.em_andamento, ['aguardando_terceiros', 'concluida', 'cancelada'])
  assert.deepEqual(transicoes.aguardando_terceiros, ['em_andamento', 'cancelada'])
})
