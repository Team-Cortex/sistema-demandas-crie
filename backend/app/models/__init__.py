"""Entidades e persistência.

Importar este pacote registra todas as tabelas no metadata do SQLAlchemy.
Destino de encaminhamento, categorias de demanda e campos do assistido
continuam em aberto no contrato da API.
"""

from app.models.assistido import Assistido, AssistidoProfissional
from app.models.demanda import Demanda, EstadoDemanda, Prioridade
from app.models.historico import HistoricoDemanda, TipoHistorico
from app.models.reuniao import Reuniao, Setor
from app.models.usuario import (
    CLASSE_POR_PERFIL,
    AssistenteSocial,
    Direcao,
    EquipePedagogica,
    Profissional,
    Usuario,
)

__all__ = [
    "CLASSE_POR_PERFIL",
    "AssistenteSocial",
    "Assistido",
    "AssistidoProfissional",
    "Demanda",
    "Direcao",
    "EquipePedagogica",
    "EstadoDemanda",
    "HistoricoDemanda",
    "Prioridade",
    "Profissional",
    "Reuniao",
    "Setor",
    "TipoHistorico",
    "Usuario",
]
