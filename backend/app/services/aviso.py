"""Aviso de prazo no login. Spec 09, card #25, RF40.

Só indica que há pendência: nada de descrição, categoria ou assistido,
porque a descrição da demanda pode citar a saúde da pessoa atendida.
"""

from datetime import timedelta

from app.extensions import db
from app.fuso import hoje
from app.services.demanda import EM_ABERTO


class AvisoService:
    @staticmethod
    def de_prazo(usuario, dias_de_antecedencia, dia=None):
        from app.models import Demanda

        dia = dia or hoje()
        limite = dia + timedelta(days=dias_de_antecedencia)
        demandas = db.session.scalars(
            db.select(Demanda)
            .where(
                Demanda.responsavel_id == usuario.id,
                Demanda.estado.in_(EM_ABERTO),
                Demanda.prazo <= limite,
            )
            .order_by(Demanda.prazo, Demanda.id)
        ).all()
        itens = [
            {
                "id": demanda.id,
                "prazo": demanda.prazo.isoformat(),
                "estado": demanda.estado.value,
                "vencida": demanda.vencida_em(dia),
            }
            for demanda in demandas
        ]
        vencidas = sum(1 for item in itens if item["vencida"])
        return {
            "vencidas": vencidas,
            "perto_do_prazo": len(itens) - vencidas,
            "dias_de_antecedencia": dias_de_antecedencia,
            "demandas": itens,
        }
