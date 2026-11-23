import test from 'node:test'
import assert from 'node:assert/strict'
import Demanda from '../src/modelos/Demanda.js'

const campos = {
  descricao: 'Verificar a vaga fictícia', prioridade: 'baixa', responsavel_id: '2',
  prazo: '2024-02-29', reuniao_id: '4', assistido_id: '', categoria: '',
}

test('aceita demanda sem assistido ou categoria e prazo no passado', () => {
  assert.deepEqual(Demanda.validar(campos), {})
})

test('indica os campos obrigatórios vazios e a categoria longa', () => {
  const erros = Demanda.validar({
    descricao: ' ', prioridade: '', responsavel_id: '', prazo: '',
    reuniao_id: '', assistido_id: '', categoria: 'a'.repeat(81),
  })
  assert.deepEqual(Object.keys(erros).sort(), ['categoria', 'descricao', 'prazo', 'prioridade', 'responsavel_id', 'reuniao_id'])
})

test('cancelamento e conclusão encerram as transições', () => {
  const proximos = estado => new Demanda({ estado }).proximosEstados()
  assert.deepEqual(proximos('cancelada'), [])
  assert.deepEqual(proximos('concluida'), [])
  assert.deepEqual(proximos('aberta'), ['em_andamento', 'cancelada'])
  assert.deepEqual(proximos('em_andamento'), ['aguardando_terceiros', 'concluida', 'cancelada'])
  assert.deepEqual(proximos('aguardando_terceiros'), ['em_andamento', 'cancelada'])
})

test('o objeto mostra estado, prioridade e prazo como a tela escreve', () => {
  const demanda = new Demanda({ id: 7, estado: 'aguardando_terceiros', prioridade: 'media', prazo: '2026-11-14', vencida: true })
  assert.equal(demanda.id, 7)
  assert.equal(demanda.rotuloEstado(), 'Aguardando terceiros')
  assert.equal(demanda.rotuloPrioridade(), 'Média')
  assert.equal(demanda.prazoFormatado(), '14/11/2026')
  assert.equal(demanda.estaVencida(), true)
  assert.equal(new Demanda({ prazo: '2026-11-14', vencida: false }).estaVencida(), false)
})
