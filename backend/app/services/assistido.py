"""Cadastro mínimo do assistido e auditoria de leitura. Spec 03, cards #17 e #20.

Toda leitura e toda escrita passam pela auditoria (spec 05).
"""

from sqlalchemy.orm import joinedload, selectinload

from app.errors import NaoEncontrado
from app.extensions import db
from app.schemas import descrever_filtros
from app.services.acesso import exigir_acesso_ao_assistido
from app.services.auditoria import AuditoriaService

INEXISTENTE = "Assistido inexistente."


class AssistidoService:
    @staticmethod
    def obter(assistido_id):
        """Sem auditoria: uso interno das outras operações."""
        from app.models import Assistido

        assistido = db.session.get(Assistido, assistido_id)
        if assistido is None:
            raise NaoEncontrado(INEXISTENTE)
        return assistido

    @staticmethod
    def listar(autor, busca=None):
        """Em ordem alfabética. A auditoria guarda que houve busca, não o texto."""
        from app.models import Assistido

        consulta = db.select(Assistido)
        if busca and busca.strip():
            consulta = consulta.where(Assistido.nome_tratamento.icontains(busca.strip(), autoescape=True))
        assistidos = db.session.scalars(consulta.order_by(Assistido.nome_tratamento, Assistido.id)).all()
        AuditoriaService.registrar_leitura(
            autor, "listar", "assistido", detalhe=descrever_filtros({"busca": busca}, ocultar=("busca",))
        )
        return assistidos

    @staticmethod
    def consultar(assistido_id, autor):
        assistido = AssistidoService.obter(assistido_id)
        AuditoriaService.registrar_leitura(autor, "consultar", "assistido", assistido.id, assistido.id)
        return assistido

    @staticmethod
    def _com_a_ficha_carregada(assistido_id):
        """O assistido com as quatro listas da ficha, sem uma consulta por linha."""
        from app.models import Assistido, AssistidoProfissional, Demanda, Encaminhamento, Evolucao

        consulta = (
            db.select(Assistido)
            .where(Assistido.id == assistido_id)
            .options(
                selectinload(Assistido.acompanhamentos).joinedload(AssistidoProfissional.profissional),
                selectinload(Assistido.demandas).options(
                    joinedload(Demanda.responsavel), selectinload(Demanda.historico)
                ),
                selectinload(Assistido.evolucoes).options(*Evolucao.carregar_junto()),
                selectinload(Assistido.encaminhamentos).joinedload(Encaminhamento.responsavel),
            )
        )
        assistido = db.session.scalars(consulta).first()
        if assistido is None:
            raise NaoEncontrado(INEXISTENTE)
        return assistido

    @staticmethod
    def ficha(assistido_id, autor):
        """Ficha completa (RF20). Traz evolução, então passa por pode_ver_evolucao."""
        assistido = AssistidoService._com_a_ficha_carregada(assistido_id)
        exigir_acesso_ao_assistido(autor, assistido)
        AuditoriaService.registrar_leitura(
            autor, "consultar", "assistido", assistido.id, assistido.id, detalhe="ficha"
        )
        return assistido

    @staticmethod
    def cadastrar(dados, autor):
        from app.models import Assistido

        assistido = Assistido(nome_tratamento=dados["nome_tratamento"].strip())
        db.session.add(assistido)
        db.session.flush()
        AuditoriaService.registrar(autor, "criar", "assistido", assistido.id, assistido.id)
        db.session.commit()
        return assistido

    @staticmethod
    def alterar(assistido_id, dados, autor):
        assistido = AssistidoService.obter(assistido_id)
        assistido.nome_tratamento = dados["nome_tratamento"].strip()
        AuditoriaService.registrar(autor, "alterar", "assistido", assistido.id, assistido.id)
        db.session.commit()
        return assistido
