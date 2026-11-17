"""Hora local do CRIE (Extrema, MG) e formato de data do contrato.

O banco grava em UTC. A API devolve ISO 8601 com o fuso (-03:00), como
pede o contrato §1. Brasília não tem horário de verão desde 2019; o fuso
fixo evita depender do pacote tzdata no Windows.
"""

from datetime import datetime, time, timedelta, timezone

FUSO = timezone(timedelta(hours=-3))


def hoje():
    """A data de hoje no CRIE, não a do servidor em UTC."""
    return datetime.now(FUSO).date()


def inicio_do_dia(data):
    """00:00 da data no CRIE, em UTC, para comparar com momento gravado."""
    return datetime.combine(data, time(0), FUSO).astimezone(timezone.utc)


def fim_do_dia(data):
    """00:00 do dia seguinte no CRIE, em UTC: limite exclusivo do período."""
    return inicio_do_dia(data + timedelta(days=1))


def no_fuso(momento):
    """Momento gravado → texto ISO 8601 com -03:00.

    O SQLite devolve o momento sem fuso; o servidor sempre grava em UTC.
    """
    if momento is None:
        return None
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    return momento.astimezone(FUSO).isoformat()
