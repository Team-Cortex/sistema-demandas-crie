"""Reunião por setor e participantes. Spec 04, card #18, RF06 a RF09."""

from app.errors import DadoInvalido, NaoEncontrado
from app.extensions import db
from app.schemas.reuniao import INFORME_PARTICIPANTES

INEXISTENTE = "Reunião inexistente."


class ReuniaoService:
    @staticmethod
    def _participantes(ids):
        """Usuários ativos com esses ids. Faltou um → 422 (spec 04)."""
        from app.models import Usuario

        unicos = set(ids)
        encontrados = db.session.scalars(
            db.select(Usuario).where(Usuario.id.in_(unicos), Usuario.ativo.is_(True))
        ).all()
        if not unicos or len(encontrados) != len(unicos):
            raise DadoInvalido(INFORME_PARTICIPANTES)
        return encontrados

    @staticmethod
    def registrar(dados):
        from app.models import Reuniao, Setor

        reuniao = Reuniao(
            data=dados["data"],
            setor=Setor(dados["setor"]),
            participantes=ReuniaoService._participantes(dados["participante_ids"]),
        )
        db.session.add(reuniao)
        db.session.commit()
        return reuniao

    @staticmethod
    def listar(setor=None):
        from app.models import Reuniao, Setor

        consulta = db.select(Reuniao)
        if setor:
            consulta = consulta.where(Reuniao.setor == Setor(setor))
        return db.session.scalars(consulta.order_by(Reuniao.data.desc(), Reuniao.id.desc())).all()

    @staticmethod
    def obter(reuniao_id):
        from app.models import Reuniao

        reuniao = db.session.get(Reuniao, reuniao_id)
        if reuniao is None:
            raise NaoEncontrado(INEXISTENTE)
        return reuniao

    @staticmethod
    def alterar(reuniao_id, dados):
        """Muda data, setor e participantes. As demandas da reunião ficam."""
        from app.models import Setor

        reuniao = ReuniaoService.obter(reuniao_id)
        if "participante_ids" in dados:
            reuniao.participantes = ReuniaoService._participantes(dados["participante_ids"])
        if "data" in dados:
            reuniao.data = dados["data"]
        if "setor" in dados:
            reuniao.setor = Setor(dados["setor"])
        db.session.commit()
        return reuniao
