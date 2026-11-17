"""Demanda pela API. Spec 02, card #19, RF10 a RF17 e RF30 a RF34.

A máquina de estados e o histórico imutável moram no model (Demanda);
aqui ficam a busca dos vínculos, a tradução de erro e o commit.
"""

from sqlalchemy.orm import joinedload, selectinload

from app.errors import DadoInvalido, NaoEncontrado
from app.extensions import db
from app.fuso import fim_do_dia, inicio_do_dia
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
    def _com_vinculos(consulta):
        """Carrega histórico e responsável junto: a lista não faz uma consulta por linha."""
        from app.models import Demanda, HistoricoDemanda

        return consulta.options(
            selectinload(Demanda.historico).joinedload(HistoricoDemanda.autor),
            joinedload(Demanda.responsavel),
        )

    @staticmethod
    def listar(estado=None, responsavel_id=None, assistido_id=None, reuniao_id=None, categoria=None,
               periodo_inicio=None, periodo_fim=None, q=None):
        """Filtros combináveis; sem filtro nenhum, deixa as canceladas de fora.

        Ordem: último movimento (item de histórico mais recente) primeiro.
        """
        from app.models import Demanda, EstadoDemanda, HistoricoDemanda

        consulta = db.select(Demanda)
        if estado:
            consulta = consulta.where(Demanda.estado.in_([EstadoDemanda(e) for e in estado]))
        if responsavel_id is not None:
            consulta = consulta.where(Demanda.responsavel_id == responsavel_id)
        if assistido_id is not None:
            consulta = consulta.where(Demanda.assistido_id == assistido_id)
        if reuniao_id is not None:
            consulta = consulta.where(Demanda.reuniao_id == reuniao_id)
        if categoria:
            consulta = consulta.where(db.func.lower(Demanda.categoria) == categoria.strip().lower())
        if periodo_inicio is not None:
            consulta = consulta.where(Demanda.criado_em >= inicio_do_dia(periodo_inicio))
        if periodo_fim is not None:
            consulta = consulta.where(Demanda.criado_em < fim_do_dia(periodo_fim))
        if q:
            consulta = consulta.where(Demanda.descricao.icontains(q.strip(), autoescape=True))
        sem_filtro = not any(
            v not in (None, "", [])
            for v in (estado, responsavel_id, assistido_id, reuniao_id, categoria, periodo_inicio, periodo_fim, q)
        )
        if sem_filtro:
            consulta = consulta.where(Demanda.estado != EstadoDemanda.CANCELADA)

        ultimo = (
            db.select(db.func.max(HistoricoDemanda.ocorrido_em))
            .where(HistoricoDemanda.demanda_id == Demanda.id)
            .correlate(Demanda)
            .scalar_subquery()
        )
        consulta = consulta.order_by(db.func.coalesce(ultimo, Demanda.criado_em).desc(), Demanda.id.desc())
        return db.session.scalars(DemandaService._com_vinculos(consulta)).unique().all()

    @staticmethod
    def mudar_estado(demanda_id, estado, autor):
        """Transição recusada → 400 pelo model, sem gravar histórico."""
        demanda = DemandaService.obter(demanda_id)
        demanda.mudar_estado(estado, autor)
        db.session.commit()
        return demanda

    @staticmethod
    def anotar(demanda_id, texto, autor):
        """Anotação vira item de histórico; o estado não muda (RF15)."""
        demanda = DemandaService.obter(demanda_id)
        try:
            item = demanda.anotar(texto, autor)
        except ValueError as erro:
            raise DadoInvalido(str(erro)) from None
        db.session.commit()
        return item

    @staticmethod
    def reatribuir(demanda_id, responsavel_id, autor):
        """Inexistente ou inativo → 404 pelo model; a troca vai para o histórico (RF16)."""
        from app.models import Usuario

        demanda = DemandaService.obter(demanda_id)
        demanda.reatribuir(db.session.get(Usuario, responsavel_id), autor)
        db.session.commit()
        return demanda

    @staticmethod
    def obter(demanda_id):
        from app.models import Demanda

        demanda = db.session.get(Demanda, demanda_id)
        if demanda is None:
            raise NaoEncontrado(INEXISTENTE)
        return demanda
