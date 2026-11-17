"""Spec 08, card #24: relatórios da direção, com auditoria da emissão."""

from datetime import date, datetime, timedelta, timezone

import pytest

from app.fuso import hoje
from app.models import (
    Assistido,
    Demanda,
    Encaminhamento,
    EstadoDemanda,
    Evolucao,
    Prioridade,
    RegistroAuditoria,
    Reuniao,
    Setor,
    Usuario,
)


@pytest.fixture
def dados(api):
    """Demandas registradas há 3, 15 e 40 dias; evoluções e encaminhamentos em datas fixas."""
    with api.banco() as db:
        direcao = db.session.get(Usuario, api.pessoas["direcao"])
        assistente = db.session.get(Usuario, api.pessoas["assistente"])
        assistido = Assistido(nome_tratamento="Assistido Fictício J")
        reuniao = Reuniao(data=hoje() - timedelta(days=50), setor=Setor.SAUDE, participantes=[direcao])
        db.session.add_all([assistido, reuniao])
        for descricao, atras, prazo, caminho, categoria in (
            ("recente vencida", 3, -1, [], "Saúde"),
            ("meio concluída", 15, -5, [EstadoDemanda.EM_ANDAMENTO, EstadoDemanda.CONCLUIDA], "Educação"),
            ("antiga cancelada", 40, 10, [EstadoDemanda.CANCELADA], "Saúde"),
        ):
            demanda = Demanda.abrir(
                direcao, descricao=descricao, categoria=categoria, prioridade=Prioridade.MEDIA,
                prazo=hoje() + timedelta(days=prazo), responsavel=assistente, reuniao=reuniao,
                criado_em=datetime.now(timezone.utc) - timedelta(days=atras),
            )
            for passo in caminho:
                demanda.mudar_estado(passo, direcao)
            db.session.add(demanda)
        v1 = Evolucao.lancar(assistente, assistido=assistido, data=date(2026, 10, 5),
                             area_atuacao="Social", descricao="dentro, original")
        fora = Evolucao.lancar(assistente, assistido=assistido, data=date(2026, 9, 1),
                               area_atuacao="Social", descricao="fora do período")
        db.session.add_all([v1, fora])
        db.session.flush()
        db.session.add(v1.retificar(assistente, descricao="dentro, retificada"))
        for dia, destino in ((date(2026, 10, 20), "CRAS (fictício)"), (date(2026, 11, 20), "fora")):
            db.session.add(Encaminhamento(assistido=assistido, destino=destino, data=dia, responsavel=assistente))
        db.session.commit()
        api.assistido_id = assistido.id
    return api


def _ultima_auditoria(api):
    with api.banco() as db:
        registro = db.session.scalars(db.select(RegistroAuditoria).order_by(RegistroAuditoria.id.desc())).first()
        return registro and (registro.autor_id, registro.acao, registro.recurso, registro.assistido_id, registro.detalhe,
                             registro.ocorrido_em)


def _periodo(dias_atras_inicio, dias_atras_fim=0):
    return f"de={(hoje() - timedelta(days=dias_atras_inicio)).isoformat()}&ate={(hoje() - timedelta(days=dias_atras_fim)).isoformat()}"


def test_relatorio_de_demandas_do_periodo_com_totais_e_emissao(dados):
    resposta = dados.get(f"/api/relatorios/demandas?{_periodo(20)}")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert {i["descricao"] for i in corpo["itens"]} == {"recente vencida", "meio concluída"}
    assert corpo["totais"]["total"] == 2
    assert corpo["totais"]["por_estado"] == {
        "aberta": 1, "em_andamento": 0, "aguardando_terceiros": 0, "concluida": 1, "cancelada": 0,
    }
    assert corpo["totais"]["vencidas"] == 1
    assert corpo["emissao"]["autor_id"] == dados.pessoas["direcao"]
    assert corpo["emissao"]["autor_nome"] == "Direção Fictícia"

    autor, acao, recurso, assistido_id, detalhe, momento = _ultima_auditoria(dados)
    assert (autor, acao, recurso, assistido_id) == (dados.pessoas["direcao"], "emitir", "relatorio_demandas", None)
    assert detalhe.startswith("de=")
    assert datetime.fromisoformat(corpo["emissao"]["ocorrido_em"]) == momento.replace(tzinfo=timezone.utc)


def test_relatorio_inclui_cancelada_e_aceita_filtros(dados):
    todas = dados.get(f"/api/relatorios/demandas?{_periodo(60)}").get_json()
    assert todas["totais"]["por_estado"]["cancelada"] == 1
    saude = dados.get(f"/api/relatorios/demandas?{_periodo(60)}&categoria=saúde&estado=cancelada").get_json()
    assert [i["descricao"] for i in saude["itens"]] == ["antiga cancelada"]
    assert saude["filtros"] == {"estado": ["cancelada"], "categoria": "saúde", "responsavel_id": None}


def test_relatorio_do_assistido_traz_evolucoes_vigentes_e_encaminhamentos_do_periodo(dados):
    url = f"/api/relatorios/assistidos/{dados.assistido_id}?de=2026-10-01&ate=2026-10-31"
    resposta = dados.get(url)
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["assistido"] == {"id": dados.assistido_id, "nome_tratamento": "Assistido Fictício J"}
    assert corpo["periodo"] == {"de": "2026-10-01", "ate": "2026-10-31"}
    assert [e["descricao"] for e in corpo["evolucoes"]] == ["dentro, retificada"]
    assert [e["destino"] for e in corpo["encaminhamentos"]] == ["CRAS (fictício)"]
    autor, acao, recurso, assistido_id, detalhe, _ = _ultima_auditoria(dados)
    assert (acao, recurso, assistido_id, detalhe) == (
        "emitir", "relatorio_assistido", dados.assistido_id, "de=2026-10-01 ate=2026-10-31",
    )


@pytest.mark.parametrize("quem", ["assistente", "educadora"])
def test_profissional_recebe_403_sem_auditoria(dados, quem):
    for url in (f"/api/relatorios/demandas?{_periodo(20)}",
                f"/api/relatorios/assistidos/{dados.assistido_id}?{_periodo(20)}"):
        resposta = dados.get(url, como=quem)
        assert resposta.status_code == 403
        assert resposta.get_json() == {"erro": "Só a direção emite relatórios."}
    assert _ultima_auditoria(dados) is None


@pytest.mark.parametrize("consulta", ["", "de=2026-10-01", "ate=2026-10-31", "de=2026-11-01&ate=2026-10-01"])
def test_sem_periodo_valido_devolve_422(dados, consulta):
    resposta = dados.get(f"/api/relatorios/demandas?{consulta}")
    assert resposta.status_code == 422
    assert _ultima_auditoria(dados) is None


def test_relatorio_de_assistido_inexistente_devolve_404_sem_auditoria(dados):
    assert dados.get("/api/relatorios/assistidos/9999?de=2026-10-01&ate=2026-10-31").status_code == 404
    assert _ultima_auditoria(dados) is None


def test_relatorio_exige_token(dados):
    assert dados.get(f"/api/relatorios/demandas?{_periodo(20)}", como=None).status_code == 401
