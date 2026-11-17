"""As leituras não fazem uma consulta por linha (N+1).

Na Vercel, cada consulta ao banco é uma ida pela rede: a ficha ou o relatório
com cem linhas não pode virar duzentas consultas.
"""

from datetime import date

import pytest
from sqlalchemy import event

from app.extensions import db as _db
from app.fuso import hoje
from app.models import Assistido, Demanda, Encaminhamento, Evolucao, Prioridade, Reuniao, Setor, Usuario


def _semear(api, quantidade):
    """Um assistido novo com `quantidade` demandas, evoluções (metade retificada) e encaminhamentos."""
    with api.banco() as db:
        direcao = db.session.get(Usuario, api.pessoas["direcao"])
        educadora = db.session.get(Usuario, api.pessoas["educadora"])
        assistido = Assistido(nome_tratamento="Assistido Fictício N")
        assistido.vincular_profissional(educadora)
        reuniao = Reuniao(data=hoje(), setor=Setor.SAUDE, participantes=[direcao])
        db.session.add_all([assistido, reuniao])
        for i in range(quantidade):
            autor = (direcao, educadora)[i % 2]
            db.session.add(Demanda.abrir(autor, descricao=f"demanda {i}", prioridade=Prioridade.BAIXA,
                                         prazo=hoje(), responsavel=autor, reuniao=reuniao, assistido=assistido))
            evolucao = Evolucao.lancar(autor, assistido=assistido, data=date(2026, 11, 1),
                                       area_atuacao="Social", descricao=f"evolução {i}")
            db.session.add(evolucao)
            db.session.flush()
            if i % 2:
                db.session.add(evolucao.retificar(autor, descricao=f"evolução {i} corrigida"))
            db.session.add(Encaminhamento(assistido=assistido, destino=f"destino {i}",
                                          data=date(2026, 11, 2), responsavel=autor))
        db.session.commit()
        return assistido.id


def _consultas(api, url):
    contagem = []

    def contar(*_args, **_kwargs):
        contagem.append(1)

    with api.banco():
        engine = _db.engine
    event.listen(engine, "before_cursor_execute", contar)
    try:
        assert api.get(url).status_code == 200
    finally:
        event.remove(engine, "before_cursor_execute", contar)
    return len(contagem)


@pytest.mark.parametrize(
    "rota",
    [
        "/api/assistidos/{id}/ficha",
        "/api/assistidos/{id}/evolucoes",
        "/api/relatorios/assistidos/{id}?de=2026-10-01&ate=2026-11-30",
        "/api/relatorios/demandas?de={hoje}&ate={hoje}",
        "/api/demandas",
        "/api/demandas/painel",
        "/api/encaminhamentos",
    ],
)
def test_quantidade_de_consultas_nao_cresce_com_as_linhas(api, rota):
    pouco = _semear(api, 2)
    antes = _consultas(api, rota.format(id=pouco, hoje=hoje().isoformat()))
    muito = _semear(api, 8)  # as rotas gerais passam a ver 10 linhas
    depois = _consultas(api, rota.format(id=muito, hoje=hoje().isoformat()))
    assert antes == depois, f"{rota}: {antes} consultas com poucas linhas, {depois} com mais"
