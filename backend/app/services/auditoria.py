"""Registro e consulta da auditoria. Spec 05, card #17.

Escrita: `registrar` só põe o registro na sessão; quem chama faz o commit,
junto com a operação. Leitura: `registrar_leitura` grava na hora, antes
de a resposta sair. Sem registro, sem leitura.
"""

from app.extensions import db
from app.fuso import fim_do_dia, inicio_do_dia


class AuditoriaService:
    @staticmethod
    def registrar(autor, acao, recurso, recurso_id=None, assistido_id=None, detalhe=None):
        from app.models import RegistroAuditoria

        registro = RegistroAuditoria(
            autor=autor,
            acao=acao,
            recurso=recurso,
            recurso_id=recurso_id,
            assistido_id=assistido_id,
            detalhe=detalhe,
        )
        db.session.add(registro)
        return registro

    @staticmethod
    def registrar_leitura(autor, acao, recurso, recurso_id=None, assistido_id=None, detalhe=None):
        """Grava antes de a resposta sair, sem descartar o que já foi lido.

        O commit normal expira tudo na sessão, e montar a resposta faria uma
        consulta por linha. Aqui o que foi lido nesta transação continua
        carregado: é exatamente o que a auditoria registrou como consultado.
        """
        registro = AuditoriaService.registrar(autor, acao, recurso, recurso_id, assistido_id, detalhe)
        sessao = db.session()
        expirava = sessao.expire_on_commit
        sessao.expire_on_commit = False
        try:
            sessao.commit()
        finally:
            sessao.expire_on_commit = expirava
        return registro

    @staticmethod
    def consultar(autor_id=None, assistido_id=None, recurso=None, acao=None, de=None, ate=None,
                  pagina=1, por_pagina=50):
        """Do mais recente para o mais antigo. Devolve (itens, total)."""
        from app.models import RegistroAuditoria as R

        consulta = db.select(R)
        if autor_id is not None:
            consulta = consulta.where(R.autor_id == autor_id)
        if assistido_id is not None:
            consulta = consulta.where(R.assistido_id == assistido_id)
        if recurso:
            consulta = consulta.where(R.recurso == recurso)
        if acao:
            consulta = consulta.where(R.acao == acao)
        if de is not None:
            consulta = consulta.where(R.ocorrido_em >= inicio_do_dia(de))
        if ate is not None:
            consulta = consulta.where(R.ocorrido_em < fim_do_dia(ate))

        total = db.session.scalar(db.select(db.func.count()).select_from(consulta.subquery()))
        itens = db.session.scalars(
            consulta.order_by(R.ocorrido_em.desc(), R.id.desc())
            .limit(por_pagina)
            .offset((pagina - 1) * por_pagina)
        ).all()
        return itens, total
