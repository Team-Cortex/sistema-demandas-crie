// Mudanças de estado que a API aceita (contrato da API, seção de demandas).
export const transicoes = {
  aberta: ['em_andamento', 'cancelada'],
  em_andamento: ['aguardando_terceiros', 'concluida', 'cancelada'],
  aguardando_terceiros: ['em_andamento', 'cancelada'],
  concluida: [],
  cancelada: [],
}

// Mensagens da especificação de telas (docs/ihc/telas.md, Registrar demanda).
export function validarDemanda(campos) {
  const erros = {}
  if (!campos.descricao.trim()) erros.descricao = 'Informe a descrição da demanda.'
  if (!campos.prioridade) erros.prioridade = 'Escolha a prioridade.'
  if (!campos.responsavel_id) erros.responsavel_id = 'Escolha o responsável.'
  if (!campos.prazo) erros.prazo = 'Informe o prazo.'
  if (!campos.reuniao_id) erros.reuniao_id = 'Escolha a reunião em que a demanda surgiu.'
  if (campos.categoria.length > 80) erros.categoria = 'A categoria aceita até 80 caracteres.'
  return erros
}
