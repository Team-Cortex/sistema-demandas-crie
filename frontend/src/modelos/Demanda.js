// Com a extensão .js, o node --test também encontra o arquivo.
import { dataCurta, estados, prioridades } from '../dominio.js'

// Mudanças de estado que a API aceita (spec 02). Concluída e cancelada não mudam mais.
const transicoes = {
  aberta: ['em_andamento', 'cancelada'],
  em_andamento: ['aguardando_terceiros', 'concluida', 'cancelada'],
  aguardando_terceiros: ['em_andamento', 'cancelada'],
  concluida: [],
  cancelada: [],
}

// Classe de domínio: cada demanda que chega da API vira um objeto que sabe se apresentar.
// É a mesma ideia da classe Demanda do back-end (backend/app/models/demanda.py).
export default class Demanda {
  constructor(dados) {
    // Copia os campos do JSON (id, descricao, estado, prazo, vencida...) para o objeto,
    // como o self.campo = valor do __init__ em Python.
    Object.assign(this, dados)
  }

  // Quem calcula o vencimento é o servidor, no fuso do CRIE; a tela não refaz a conta.
  estaVencida() {
    return this.vencida === true
  }

  rotuloEstado() {
    return estados[this.estado]
  }

  rotuloPrioridade() {
    return prioridades[this.prioridade]
  }

  prazoFormatado() {
    return dataCurta(this.prazo)
  }

  proximosEstados() {
    return transicoes[this.estado]
  }

  // Método estático: valida o formulário antes de a demanda existir, então pertence à classe, não a um objeto.
  // Mensagens da especificação de telas (docs/ihc/telas.md, Registrar demanda).
  static validar(campos) {
    const erros = {}
    if (!campos.descricao.trim()) erros.descricao = 'Informe a descrição da demanda.'
    if (!campos.prioridade) erros.prioridade = 'Escolha a prioridade.'
    if (!campos.responsavel_id) erros.responsavel_id = 'Escolha o responsável.'
    if (!campos.prazo) erros.prazo = 'Informe o prazo.'
    if (!campos.reuniao_id) erros.reuniao_id = 'Escolha a reunião em que a demanda surgiu.'
    if (campos.categoria.length > 80) erros.categoria = 'A categoria aceita até 80 caracteres.'
    return erros
  }
}
