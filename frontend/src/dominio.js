export const estados = {
  aberta: 'Aberta',
  em_andamento: 'Em andamento',
  aguardando_terceiros: 'Aguardando terceiros',
  concluida: 'Concluída',
  cancelada: 'Cancelada',
}

export const prioridades = { baixa: 'Baixa', media: 'Média', alta: 'Alta' }
export const setores = { pedagogico: 'Pedagógico', saude: 'Saúde', convivencia: 'Serviço de convivência' }
export const perfis = { direcao: 'Direção', assistente_social: 'Assistente social', equipe_pedagogica: 'Equipe pedagógica' }

export function dataCurta(iso) {
  return iso.slice(0, 10).split('-').reverse().join('/')
}

const horarioCrie = new Intl.DateTimeFormat('pt-BR', {
  timeZone: 'America/Sao_Paulo', dateStyle: 'short', timeStyle: 'short',
})

export function dataHora(iso) {
  return horarioCrie.format(new Date(iso)).replace(',', '')
}
