"""Hora local do CRIE (Extrema, MG) e formato de data do contrato.

O banco grava em UTC. A API devolve ISO 8601 com o fuso (-03:00), como
pede o contrato §1. Brasília não tem horário de verão desde 2019; o fuso
fixo evita depender do pacote tzdata no Windows.
"""

from datetime import datetime, timedelta, timezone

FUSO = timezone(timedelta(hours=-3))


def hoje():
    """A data de hoje no CRIE, não a do servidor em UTC."""
    return datetime.now(FUSO).date()


def no_fuso(momento):
    """Momento gravado → texto ISO 8601 com -03:00.

    O SQLite devolve o momento sem fuso; o servidor sempre grava em UTC.
    """
    if momento is None:
        return None
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    return momento.astimezone(FUSO).isoformat()
