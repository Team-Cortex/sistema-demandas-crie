from sqlalchemy import text


def test_banco_de_teste_aplica_chave_estrangeira(db):
    assert db.session.execute(text("PRAGMA foreign_keys")).scalar_one() == 1