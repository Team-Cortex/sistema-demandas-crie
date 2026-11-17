"""Encaminhamento à rede pela API. Spec 07, cards #15, #17 e #22, RF27 a RF29.

Encaminhamento ligado a assistido passa por pode_ver_evolucao; nas listas,
o que a pessoa não pode ver não aparece. Toda operação grava auditoria.
"""

from app.errors import DadoInvalido, NaoEncontrado
from app.extensions import db
from app.schemas import descrever_filtros
from app.schemas.encaminhamento import ASSISTIDO_INEXISTENTE, DEMANDA_INEXISTENTE
from app.services.acesso import exigir_acesso_ao_assistido
from app.services.auditoria import AuditoriaService

INEXISTENTE = "Encaminhamento inexistente."
SEM_ACESSO = "Você não tem acesso aos dados deste assistido."
DEMANDA_DE_OUTRO = "A demanda informada é de outro assistido."


def _pode_ver(usuario, encaminhamento):
    return encaminhamento.assistido is None or usuario.pode_ver_evolucao(encaminhamento.assistido)


class EncaminhamentoService:
    @staticmethod
    def registrar(dados, autor):
        from app.models import Assistido, Demanda, Encaminhamento

        assistido = demanda = None
        if dados.get("assistido_id") is not None:
            assistido = db.session.get(Assistido, dados["assistido_id"])
            if assistido is None:
                raise DadoInvalido(ASSISTIDO_INEXISTENTE)
        if dados.get("demanda_id") is not None:
            demanda = db.session.get(Demanda, dados["demanda_id"])
            if demanda is None:
                raise DadoInvalido(DEMANDA_INEXISTENTE)
        if assistido and demanda and demanda.assistido_id not in (None, assistido.id):
            raise DadoInvalido(DEMANDA_DE_OUTRO)
        envolvido = assistido or (demanda.assistido if demanda else None)
        if envolvido is not None:
            exigir_acesso_ao_assistido(autor, envolvido, SEM_ACESSO)

        try:
            encaminhamento = Encaminhamento(
                assistido=assistido,
                demanda=demanda,
                destino=dados["destino"],
                data=dados["data"],
                observacao=dados.get("observacao"),
                responsavel=autor,
            )
        except ValueError as erro:
            raise DadoInvalido(str(erro)) from None
        db.session.add(encaminhamento)
        db.session.flush()
        AuditoriaService.registrar(
            autor, "criar", "encaminhamento", encaminhamento.id, encaminhamento.assistido_id
        )
        db.session.commit()
        return encaminhamento

    @staticmethod
    def listar(autor, pendentes=None, assistido_id=None, demanda_id=None, responsavel_id=None):
        """Do mais antigo para o mais novo, por data. `pendentes=True`: só sem desfecho (RF29)."""
        from app.models import Assistido
        from app.models import Encaminhamento as E

        if assistido_id is not None and db.session.get(Assistido, assistido_id) is None:
            # Sem isso, a auditoria tentaria apontar um assistido que não existe.
            raise NaoEncontrado(ASSISTIDO_INEXISTENTE)
        consulta = db.select(E)
        if pendentes:
            consulta = consulta.where(E.desfecho.is_(None))
        if assistido_id is not None:
            consulta = consulta.where(E.assistido_id == assistido_id)
        if demanda_id is not None:
            consulta = consulta.where(E.demanda_id == demanda_id)
        if responsavel_id is not None:
            consulta = consulta.where(E.responsavel_id == responsavel_id)
        itens = [e for e in db.session.scalars(consulta.order_by(E.data, E.id)) if _pode_ver(autor, e)]
        filtros = {
            "pendentes": pendentes,
            "assistido_id": assistido_id,
            "demanda_id": demanda_id,
            "responsavel_id": responsavel_id,
        }
        AuditoriaService.registrar_leitura(
            autor, "listar", "encaminhamento", assistido_id=assistido_id, detalhe=descrever_filtros(filtros)
        )
        return itens

    @staticmethod
    def obter(encaminhamento_id, para_alterar=False):
        from app.models import Encaminhamento

        encaminhamento = db.session.get(
            Encaminhamento, encaminhamento_id, with_for_update=para_alterar or None
        )
        if encaminhamento is None:
            raise NaoEncontrado(INEXISTENTE)
        return encaminhamento

    @staticmethod
    def _acessivel(encaminhamento_id, autor, para_alterar=False):
        encaminhamento = EncaminhamentoService.obter(encaminhamento_id, para_alterar)
        if encaminhamento.assistido is not None:
            exigir_acesso_ao_assistido(autor, encaminhamento.assistido, SEM_ACESSO)
        return encaminhamento

    @staticmethod
    def registrar_desfecho(encaminhamento_id, texto, autor):
        """Uma vez só, com autor e momento (RF28). Segundo desfecho → 400 pelo model."""
        # Trava a linha: o segundo pedido simultâneo espera e vê o desfecho já gravado.
        encaminhamento = EncaminhamentoService._acessivel(encaminhamento_id, autor, para_alterar=True)
        try:
            encaminhamento.registrar_desfecho(texto, autor)
        except ValueError as erro:
            raise DadoInvalido(str(erro)) from None
        AuditoriaService.registrar(
            autor, "registrar_desfecho", "encaminhamento", encaminhamento.id, encaminhamento.assistido_id
        )
        db.session.commit()
        return encaminhamento

    @staticmethod
    def consultar(encaminhamento_id, autor):
        encaminhamento = EncaminhamentoService._acessivel(encaminhamento_id, autor)
        AuditoriaService.registrar_leitura(
            autor, "consultar", "encaminhamento", encaminhamento.id, encaminhamento.assistido_id
        )
        return encaminhamento
