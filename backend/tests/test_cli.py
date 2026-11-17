"""Spec 01 §3.1: primeiro acesso sem semente nem autocadastro."""

from datetime import timedelta

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.fuso import hoje
from app.models import Assistido, AssistenteSocial, Demanda, Direcao, EquipePedagogica, Reuniao, Usuario
from config import TestingConfig

SENHA = "senha-ficticia-inicial-1"
ARGUMENTOS = [
    "criar-primeira-direcao", "--nome", " Direção Fictícia ",
    "--email", " Direcao@Exemplo.TEST ",
]


def criar(app, argumentos=None, senha=SENHA):
    return app.test_cli_runner().invoke(
        args=ARGUMENTOS if argumentos is None else argumentos,
        input=f"{senha}\n{senha}\n",
    )


def test_cria_so_a_primeira_direcao_com_hash_e_sem_exibir_senha(app, db):
    resultado = criar(app)

    assert resultado.exit_code == 0, resultado.output
    direcao = db.session.scalars(db.select(Usuario)).one()
    assert isinstance(direcao, Direcao)
    assert direcao.nome == "Direção Fictícia"
    assert direcao.email == "direcao@exemplo.test"
    assert direcao.ativo
    assert direcao._senha_hash != SENHA
    assert direcao.senha_confere(SENHA)
    assert SENHA not in resultado.output
    for model in (Assistido, Demanda, Reuniao):
        assert db.session.query(model).count() == 0


@pytest.mark.parametrize("classe", [Direcao, AssistenteSocial, EquipePedagogica])
@pytest.mark.parametrize("ativo", [True, False])
def test_qualquer_conta_previa_impede_bootstrap_sem_altera_la(app, db, hash_de_teste, classe, ativo):
    existente = classe(nome="Pessoa Fictícia", email="outra@exemplo.test", ativo=ativo)
    existente._senha_hash = hash_de_teste
    db.session.add(existente)
    db.session.commit()

    resultado = criar(app)

    assert resultado.exit_code != 0
    assert SENHA not in resultado.output
    usuario = db.session.scalars(db.select(Usuario)).one()
    assert usuario.email == "outra@exemplo.test"
    assert usuario.perfil == existente.perfil
    assert usuario.ativo is ativo
    assert usuario._senha_hash == hash_de_teste


def test_repetir_nao_troca_senha_nem_duplica(app, db):
    assert criar(app).exit_code == 0
    hash_inicial = db.session.scalars(db.select(Usuario)).one()._senha_hash

    resultado = criar(app, senha="outra-senha-ficticia-2")

    assert resultado.exit_code != 0
    assert db.session.scalars(db.select(Usuario)).one()._senha_hash == hash_inicial


@pytest.mark.parametrize(
    "nome,email,senha,mensagem",
    [
        (" ", "direcao@exemplo.test", SENHA, "Informe o nome."),
        ("x" * 121, "direcao@exemplo.test", SENHA, "120"),
        ("Direção Fictícia", "sem-email", SENHA, "Informe um e-mail válido."),
        ("Direção Fictícia", "direcao@exemplo.test", "curta", "8 caracteres"),
    ],
)
def test_entrada_invalida_nao_cria_conta(app, db, nome, email, senha, mensagem):
    argumentos = ["criar-primeira-direcao", "--nome", nome, "--email", email]
    resultado = criar(app, argumentos, senha)

    assert resultado.exit_code != 0
    assert mensagem in resultado.output
    assert senha not in resultado.output
    assert db.session.query(Usuario).count() == 0


@pytest.mark.parametrize("entrada", ["", f"{SENHA}\nconfirmacao-diferente\n"])
def test_abortar_ou_errar_confirmacao_nao_cria_conta(app, db, entrada):
    resultado = app.test_cli_runner().invoke(args=ARGUMENTOS, input=entrada)

    assert resultado.exit_code != 0
    assert SENHA not in resultado.output
    assert db.session.query(Usuario).count() == 0


def test_falha_do_banco_desfaz_criacao_sem_vazar_detalhes(app, db, monkeypatch):
    detalhe = "credencial-interna-que-nao-pode-aparecer"

    def falhar():
        raise SQLAlchemyError(detalhe)

    monkeypatch.setattr(db.session, "commit", falhar)
    resultado = criar(app)

    assert resultado.exit_code != 0
    assert detalhe not in resultado.output
    assert SENHA not in resultado.output
    assert not db.session.new
    assert db.session.query(Usuario).count() == 0


def test_sem_banco_recusa_com_mensagem_legivel():
    class SemBanco(TestingConfig):
        SQLALCHEMY_DATABASE_URI = ""

    resultado = criar(create_app(SemBanco))

    assert resultado.exit_code != 0
    assert "banco" in resultado.output.lower()
    assert "Traceback" not in resultado.output


def test_primeiro_acesso_pela_api_e_logout(app, db):
    assert criar(app).exit_code == 0
    cliente = app.test_client()
    assert cliente.get("/api/usuarios").status_code == 401

    login = cliente.post("/api/auth/login", json={"email": "direcao@exemplo.test", "senha": SENHA})
    assert login.status_code == 200
    corpo = login.get_json()
    assert corpo["perfil"] == "direcao"
    assert SENHA not in login.get_data(as_text=True)
    headers = {"Authorization": f"Bearer {corpo['token']}"}

    usuarios = cliente.get("/api/usuarios", headers=headers)
    assert usuarios.status_code == 200
    assert len(usuarios.get_json()) == 1
    assert usuarios.get_json()[0]["email"] == "direcao@exemplo.test"
    painel = cliente.get("/api/demandas/painel", headers=headers)
    assert painel.status_code == 200
    assert painel.get_json()["total"] == 0

    direcao_id = corpo["usuario"]["id"]
    reuniao = cliente.post("/api/reunioes", headers=headers, json={
        "data": hoje().isoformat(), "setor": "saude", "participante_ids": [direcao_id],
    })
    assert reuniao.status_code == 201
    demanda = cliente.post("/api/demandas", headers=headers, json={
        "descricao": "Validar articulação de rede (fictício).",
        "prioridade": "media", "responsavel_id": direcao_id,
        "prazo": (hoje() + timedelta(days=7)).isoformat(), "reuniao_id": reuniao.get_json()["id"],
    })
    assert demanda.status_code == 201
    assert demanda.get_json()["estado"] == "aberta"
    demanda_id = demanda.get_json()["id"]
    for estado in ("em_andamento", "concluida"):
        resposta = cliente.patch(f"/api/demandas/{demanda_id}/estado", headers=headers, json={"estado": estado})
        assert resposta.status_code == 200
        assert resposta.get_json()["estado"] == estado
    historico = cliente.get(f"/api/demandas/{demanda_id}/historico", headers=headers)
    assert historico.status_code == 200
    assert [item["estado_novo"] for item in historico.get_json()] == ["aberta", "em_andamento", "concluida"]
    assert all(item["autor_id"] == direcao_id for item in historico.get_json())
    assert cliente.get("/api/demandas/painel", headers=headers).get_json()["total"] == 0

    assert cliente.post("/api/auth/logout", headers=headers).status_code == 200
    assert cliente.get("/api/usuarios", headers=headers).status_code == 401
