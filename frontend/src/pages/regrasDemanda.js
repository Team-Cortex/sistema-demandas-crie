export const transicoes = {
  aberta: ['em_andamento', 'cancelada'],
  em_andamento: ['aguardando_terceiros', 'concluida', 'cancelada'],
  aguardando_terceiros: ['em_andamento', 'cancelada'],
  concluida: [],
  cancelada: [],
}

function contemId(lista, valor) {
  return lista.some(item => item.id === Number(valor))
}

export function validarDemanda(campos, opcoes) {
  const erros = {}
  if (!campos.descricao.trim()) erros.descricao = 'Informe a descrição da demanda.'
  if (!['baixa', 'media', 'alta'].includes(campos.prioridade)) erros.prioridade = 'Escolha a prioridade.'
  if (!contemId(opcoes.usuarios, campos.responsavel_id)) erros.responsavel_id = 'Escolha um responsável ativo.'
  const data = new Date(campos.prazo + 'T12:00:00Z')
  if (!/^\d{4}-\d{2}-\d{2}$/.test(campos.prazo) || campos.prazo.startsWith('0000') ||
      Number.isNaN(data.getTime()) || data.toISOString().slice(0, 10) !== campos.prazo) {
    erros.prazo = 'Informe uma data válida para o prazo.'
  }
  if (!contemId(opcoes.reunioes, campos.reuniao_id)) erros.reuniao_id = 'Escolha uma reunião de origem.'
  if (campos.assistido_id && !contemId(opcoes.assistidos, campos.assistido_id)) erros.assistido_id = 'Escolha um assistido da lista.'
  if ([...campos.categoria].length > 80) erros.categoria = 'A categoria aceita até 80 caracteres.'
  return erros
}
