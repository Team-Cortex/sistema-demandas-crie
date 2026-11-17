"""Cadastro mínimo do assistido e auditoria de leitura. Spec 03, cards #17 e #20.

Toda leitura e toda escrita passam pela auditoria (spec 05).
"""

from app.errors import NaoEncontrado
from app.extensions import db
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
