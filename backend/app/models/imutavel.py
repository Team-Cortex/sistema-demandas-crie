"""Guardas de imutabilidade. RNF19.

`SomenteInsercao`: a linha nasce e nunca muda nem sai (histórico, auditoria).
`SemExclusao`: a linha pode mudar por método controlado, mas nunca sai.

A guarda roda no flush do ORM, então vale para qualquer caminho de código
que use a sessão. No PostgreSQL, a migração também nega UPDATE e DELETE
por trigger, para quem escrever SQL direto.
"""

from sqlalchemy import event
from sqlalchemy.orm import Session

from app.errors import ErroDeNegocio


class RegistroImutavel(ErroDeNegocio):
    pass


class SemExclusao:
    """Mixin: a sessão recusa apagar a linha."""

    # Como o registro aparece na mensagem de erro para o usuário.
    nome_registro = "Este registro"


class SomenteInsercao(SemExclusao):
    """Mixin: a sessão recusa apagar e alterar a linha."""


@event.listens_for(Session, "before_flush")
def _recusa_alteracao(sessao, _contexto, _instancias):
    for objeto in sessao.deleted:
        if isinstance(objeto, SemExclusao):
            raise RegistroImutavel(f"{objeto.nome_registro} não admite exclusão.")
    for objeto in sessao.dirty:
        if isinstance(objeto, SomenteInsercao) and sessao.is_modified(objeto, include_collections=False):
            raise RegistroImutavel(f"{objeto.nome_registro} não admite alteração.")
