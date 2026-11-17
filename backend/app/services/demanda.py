"""Demanda pela API. Spec 02, card #19, RF10 a RF17 e RF30 a RF34.

A máquina de estados e o histórico imutável moram no model (Demanda);
aqui ficam a busca dos vínculos, a tradução de erro e o commit.
"""

from app.errors import DadoInvalido, NaoEncontrado
from app.extensions import db
from app.schemas.demanda import ASSISTIDO_INEXISTENTE, INFORME_REUNIAO, INFORME_RESPONSAVEL

INEXISTENTE = "Demanda inexistente."


class DemandaService:
    @staticmethod
    def abrir(dados, autor):
        from app.models import Assistido, Demanda, Prioridade, Reuniao, Usuario

        responsavel = db.session.get(Usuario, dados["responsavel_id"])
        if responsavel is None or not responsavel.ativo:
            raise DadoInvalido(INFORME_RESPONSAVEL)
        reuniao = db.session.get(Reuniao, dados["reuniao_id"])
        if reuniao is None:
            raise DadoInvalido(INFORME_REUNIAO)
        assistido = None
        if dados.get("assistido_id") is not None:
            assistido = db.session.get(Assistido, dados["assistido_id"])
            if assistido is None:
                raise DadoInvalido(ASSISTIDO_INEXISTENTE)
        try:
            demanda = Demanda.abrir(
                autor,
                descricao=dados["descricao"],
                categoria=dados.get("categoria"),
                prioridade=Prioridade(dados["prioridade"]),
                prazo=dados["prazo"],
                responsavel=responsavel,
                reuniao=reuniao,
                assistido=assistido,
            )
        except ValueError as erro:
            raise DadoInvalido(str(erro)) from None
        db.session.add(demanda)
        db.session.commit()
        return demanda

    @staticmethod
    def obter(demanda_id):
        from app.models import Demanda

        demanda = db.session.get(Demanda, demanda_id)
        if demanda is None:
            raise NaoEncontrado(INEXISTENTE)
        return demanda
