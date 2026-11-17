"""Evolução do assistido pela API. Spec 06, cards #15, #17 e #21, RF21 a RF26.

Toda operação passa por pode_ver_evolucao e grava auditoria. Não há
exclusão: corrigir é retificar, que cria versão nova.
"""

from app.errors import DadoInvalido, NaoEncontrado
from app.extensions import db
from app.schemas import descrever_filtros
from app.services.acesso import exigir_acesso_ao_assistido
from app.services.assistido import AssistidoService
from app.services.auditoria import AuditoriaService

INEXISTENTE = "Evolução inexistente."


class EvolucaoService:
    @staticmethod
    def lancar(assistido_id, dados, autor):
        from app.models import Evolucao

        assistido = AssistidoService.obter(assistido_id)
        exigir_acesso_ao_assistido(autor, assistido)
        try:
            evolucao = Evolucao.lancar(autor, assistido=assistido, **dados)
        except ValueError as erro:
            raise DadoInvalido(str(erro)) from None
        db.session.add(evolucao)
        db.session.flush()
        AuditoriaService.registrar(autor, "criar", "evolucao", evolucao.id, assistido.id)
        db.session.commit()
        return evolucao

    @staticmethod
    def listar(assistido_id, autor, de=None, ate=None, area_atuacao=None):
        """Vigentes, em ordem cronológica (RF23), com filtros (RF25)."""
        from app.models import Evolucao

        assistido = AssistidoService.obter(assistido_id)
        exigir_acesso_ao_assistido(autor, assistido)
        evolucoes = Evolucao.do_assistido(assistido.id, de=de, ate=ate, area_atuacao=area_atuacao)
        filtros = {"de": de, "ate": ate, "area_atuacao": area_atuacao}
        AuditoriaService.registrar_leitura(
            autor, "listar", "evolucao", assistido_id=assistido.id, detalhe=descrever_filtros(filtros)
        )
        return evolucoes

    @staticmethod
    def obter(evolucao_id):
        from app.models import Evolucao

        evolucao = db.session.get(Evolucao, evolucao_id)
        if evolucao is None:
            raise NaoEncontrado(INEXISTENTE)
        return evolucao

    @staticmethod
    def consultar(evolucao_id, autor):
        evolucao = EvolucaoService.obter(evolucao_id)
        exigir_acesso_ao_assistido(autor, evolucao.assistido)
        AuditoriaService.registrar_leitura(autor, "consultar", "evolucao", evolucao.id, evolucao.assistido_id)
        return evolucao

    @staticmethod
    def retificar(evolucao_id, dados, autor):
        """Versão nova com autor e momento; a anterior fica intacta (RF24)."""
        evolucao = EvolucaoService.obter(evolucao_id)
        exigir_acesso_ao_assistido(autor, evolucao.assistido)
        try:
            nova = evolucao.retificar(autor, **dados)
        except ValueError as erro:
            raise DadoInvalido(str(erro)) from None
        db.session.add(nova)
        db.session.flush()
        AuditoriaService.registrar(
            autor, "retificar", "evolucao", nova.id, nova.assistido_id, detalhe=f"retifica {evolucao.id}"
        )
        db.session.commit()
        return nova
