"""Card #26: as regras críticas testadas na camada de serviço, sem HTTP.

É o que docs/arquitetura.md §3 promete: a regra se prova sem subir servidor.
As mesmas regras têm prova pela rota em test_*_api.py.
"""

from datetime import date, timedelta

import pytest
from flask_jwt_extended import create_access_token, decode_token
from jwt import ExpiredSignatureError

from app.errors import ErroDeNegocio, NaoAutenticado, PermissaoNegada
from app.models import (
    Assistido,
    AssistenteSocial,
    Demanda,
    Direcao,
    EquipePedagogica,
    EstadoDemanda,
    Evolucao,
    HistoricoDemanda,
    Prioridade,
    Profissional,
    Reuniao,
    Setor,
)
from app.models.imutavel import RegistroImutavel
from app.services.acesso import AcessoService, exigir_acesso_ao_assistido
from app.services.demanda import DemandaService
from app.services.evolucao import EvolucaoService

SENHA = "senha-ficticia-1"  # a de hash_de_teste (conftest)


@pytest.fixture
def pessoas(db, hash_de_teste):
    gente = {
        "direcao": Direcao(nome="Direção", email="d@exemplo.test"),
        "assistente": AssistenteSocial(nome="Assistente", email="a@exemplo.test"),
        "educadora": EquipePedagogica(nome="Educadora", email="e@exemplo.test"),
        "inativa": EquipePedagogica(nome="Inativa", email="i@exemplo.test", ativo=False),
    }
    for usuario in gente.values():
        usuario._senha_hash = hash_de_teste
    assistido = Assistido(nome_tratamento="Fictício Z")
    assistido.vincular_profissional(gente["educadora"])
    reuniao = Reuniao(data=date(2026, 11, 3), setor=Setor.SAUDE, participantes=[gente["direcao"]])
    db.session.add_all([*gente.values(), assistido, reuniao])
    db.session.commit()
    return {**gente, "assistido": assistido, "reuniao": reuniao}


# --- Autenticação -------------------------------------------------------------------


def test_autenticacao_correta_devolve_o_usuario(pessoas):
    assert AcessoService.autenticar(" A@exemplo.test ", SENHA) is pessoas["assistente"]


@pytest.mark.parametrize(
    "email, senha",
    [("a@exemplo.test", "senha-errada-1"), ("ninguem@exemplo.test", SENHA), ("i@exemplo.test", SENHA)],
)
def test_senha_errada_email_inexistente_e_conta_inativa_dao_a_mesma_recusa(pessoas, email, senha):
    with pytest.raises(NaoAutenticado, match="E-mail ou senha inválidos."):
        AcessoService.autenticar(email, senha)


def test_token_expirado_e_recusado(pessoas, app):
    token = create_access_token(identity=str(pessoas["direcao"].id), expires_delta=timedelta(seconds=-1))
    with pytest.raises(ExpiredSignatureError):
        decode_token(token)


# --- Transições de estado, inclusive recusadas ------------------------------------------


def _demanda(pessoas):
    demanda = Demanda.abrir(
        pessoas["direcao"], descricao="Demanda fictícia", prioridade=Prioridade.MEDIA,
        prazo=date(2026, 12, 1), responsavel=pessoas["assistente"], reuniao=pessoas["reuniao"],
    )
    from app.extensions import db

    db.session.add(demanda)
    db.session.commit()
    return demanda


def test_servico_aplica_transicao_e_grava_historico(pessoas, db):
    demanda = _demanda(pessoas)
    DemandaService.mudar_estado(demanda.id, "em_andamento", pessoas["educadora"])
    DemandaService.mudar_estado(demanda.id, "concluida", pessoas["educadora"])
    estados = [h.estado_novo for h in demanda.historico]
    assert estados == [EstadoDemanda.ABERTA, EstadoDemanda.EM_ANDAMENTO, EstadoDemanda.CONCLUIDA]
    assert demanda.historico[-1].autor is pessoas["educadora"]


@pytest.mark.parametrize("destino", ["aberta", "em_andamento", "cancelada", "esquecida"])
def test_servico_recusa_sair_de_concluida_sem_gravar(pessoas, db, destino):
    demanda = _demanda(pessoas)
    DemandaService.mudar_estado(demanda.id, "em_andamento", pessoas["direcao"])
    DemandaService.mudar_estado(demanda.id, "concluida", pessoas["direcao"])
    antes = db.session.query(HistoricoDemanda).count()
    with pytest.raises(ErroDeNegocio, match="não pode mudar para esse estado"):
        DemandaService.mudar_estado(demanda.id, destino, pessoas["direcao"])
    db.session.rollback()
    assert db.session.query(HistoricoDemanda).count() == antes
    assert db.session.get(Demanda, demanda.id).estado is EstadoDemanda.CONCLUIDA


# --- pode_ver_evolucao por perfil ---------------------------------------------------------


@pytest.mark.parametrize("quem", ["direcao", "assistente", "educadora"])
def test_acesso_aberto_libera_todo_perfil_ativo(pessoas, quem):
    exigir_acesso_ao_assistido(pessoas[quem], pessoas["assistido"])


def test_conta_inativa_nao_ve_evolucao(pessoas):
    with pytest.raises(PermissaoNegada):
        exigir_acesso_ao_assistido(pessoas["inativa"], pessoas["assistido"])


def test_regra_restritiva_so_libera_quem_acompanha_e_a_direcao(pessoas, monkeypatch):
    monkeypatch.setattr(Profissional, "acesso_restrito", True)
    exigir_acesso_ao_assistido(pessoas["educadora"], pessoas["assistido"])
    exigir_acesso_ao_assistido(pessoas["direcao"], pessoas["assistido"])
    with pytest.raises(PermissaoNegada, match="evoluções deste assistido"):
        exigir_acesso_ao_assistido(pessoas["assistente"], pessoas["assistido"])


# --- Evolução e histórico sem exclusão -----------------------------------------------------


def test_retificar_pelo_servico_preserva_a_anterior(pessoas, db):
    dados = {"data": date(2026, 11, 10), "area_atuacao": "Social", "descricao": "original"}
    original = EvolucaoService.lancar(pessoas["assistido"].id, dados, pessoas["educadora"])
    nova = EvolucaoService.retificar(original.id, {"descricao": "corrigida"}, pessoas["direcao"])
    db.session.expire_all()
    assert db.session.get(Evolucao, original.id).descricao == "original"
    assert nova.retifica_id == original.id
    with pytest.raises(ErroDeNegocio):
        EvolucaoService.retificar(original.id, {"descricao": "de novo"}, pessoas["direcao"])


def test_evolucao_e_historico_nao_saem_do_banco(pessoas, db):
    demanda = _demanda(pessoas)
    dados = {"data": date(2026, 11, 10), "area_atuacao": "Social", "descricao": "registro"}
    evolucao = EvolucaoService.lancar(pessoas["assistido"].id, dados, pessoas["educadora"])
    for registro in (evolucao, demanda.historico[0], demanda):
        db.session.delete(registro)
        with pytest.raises(RegistroImutavel, match="não admite exclusão"):
            db.session.flush()
        db.session.rollback()
    assert db.session.query(Evolucao).count() == 1
    assert db.session.query(HistoricoDemanda).count() == 1
