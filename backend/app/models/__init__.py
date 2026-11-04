"""Entidades e persistência.

Importar este pacote registra todas as tabelas no metadata do SQLAlchemy.
Destino de encaminhamento, categorias de demanda e campos do assistido
continuam em aberto no contrato da API.
"""

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
    "Direcao",
    "EquipePedagogica",
    "Profissional",
    "Usuario",
]
