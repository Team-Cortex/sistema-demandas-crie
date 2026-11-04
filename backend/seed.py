"""Carga inicial com dados fictícios. Spec 01 §3, card #57.

Executar a partir de backend/, depois de `flask db upgrade`:
    python seed.py

Regras:
- Nenhum dado real do CRIE, em nenhuma hipótese. Nomes, e-mails e textos
  abaixo são inventados; e-mails usam o domínio reservado exemplo.test.
- Senhas vêm do ambiente (SEED_DIRECAO_SENHA, SEED_SENHA_PADRAO), nunca
  deste arquivo.
- Rodar de novo não duplica: o usuário direção é buscado pelo e-mail e a
  carga de demonstração só entra se ainda não houver assistido.
- Recusa FLASK_ENV=production.
"""

import os
import sys
from datetime import date, timedelta

VARIAVEIS = ("SEED_DIRECAO_NOME", "SEED_DIRECAO_EMAIL", "SEED_DIRECAO_SENHA", "SEED_SENHA_PADRAO")


class SeedRecusado(RuntimeError):
    pass


def ler_ambiente(ambiente=None):
    ambiente = os.environ if ambiente is None else ambiente
    if ambiente.get("FLASK_ENV") == "production":
        raise SeedRecusado("A carga fictícia não roda com FLASK_ENV=production.")
    faltando = [nome for nome in VARIAVEIS if not ambiente.get(nome)]
    if faltando:
        raise SeedRecusado("Defina no .env: " + ", ".join(faltando))
    return {nome: ambiente[nome] for nome in VARIAVEIS}


def garantir_direcao(db, nome, email, senha):
    from app.models import Direcao, Usuario

    existente = db.session.scalars(
        db.select(Usuario).where(Usuario.email == email.strip().lower())
    ).first()
    if existente is not None:
        return existente, False
    direcao = Direcao(nome=nome, email=email, senha=senha)
    db.session.add(direcao)
    db.session.flush()
    return direcao, True


def carregar_demonstracao(db, direcao, senha, hoje=None):
    """Um registro fictício de cada tipo. Devolve o que criou, por nome."""
    from app.models import (
        Assistido,
        AssistenteSocial,
        Demanda,
        Encaminhamento,
        EquipePedagogica,
        Evolucao,
        Prioridade,
        Reuniao,
        Setor,
    )

    hoje = hoje or date.today()

    assistente = AssistenteSocial(nome="Bruna Fictícia", email="assistente.social@exemplo.test", senha=senha)
    educadora = EquipePedagogica(nome="Carlos Fictício", email="pedagogico@exemplo.test", senha=senha)
    db.session.add_all([assistente, educadora])

    assistido = Assistido(nome_tratamento="Assistido Fictício A")
    assistido.vincular_profissional(assistente, hoje - timedelta(days=90))
    assistido.vincular_profissional(educadora, hoje - timedelta(days=60))
    db.session.add(assistido)

    reuniao = Reuniao(
        data=hoje - timedelta(days=7),
        setor=Setor.CONVIVENCIA,
        participantes=[direcao, assistente, educadora],
    )
    db.session.add(reuniao)

    demanda = Demanda.abrir(
        direcao,
        descricao="Solicitar ao CRAS a atualização do cadastro da família (fictício).",
        categoria="Assistência social",
        prioridade=Prioridade.MEDIA,
        prazo=hoje + timedelta(days=14),
        responsavel=assistente,
        reuniao=reuniao,
        assistido=assistido,
    )
    db.session.add(demanda)

    evolucao = Evolucao.lancar(
        educadora,
        assistido=assistido,
        data=hoje - timedelta(days=3),
        area_atuacao="Pedagógica",
        descricao="Participou da oficina de música com apoio visual (registro fictício).",
    )
    db.session.add(evolucao)

    encaminhamento = Encaminhamento(
        demanda=demanda,
        destino="CRAS Centro (fictício)",
        data=hoje - timedelta(days=2),
        responsavel=assistente,
        observacao="Levar comprovante de endereço.",
    )
    db.session.add(encaminhamento)
    db.session.flush()

    return {
        "assistente": assistente,
        "educadora": educadora,
        "assistido": assistido,
        "reuniao": reuniao,
        "demanda": demanda,
        "evolucao": evolucao,
        "encaminhamento": encaminhamento,
    }


def semear(db, variaveis, hoje=None):
    """Roda a carga numa sessão aberta. Idempotente."""
    from app.models import Assistido

    direcao, criou_direcao = garantir_direcao(
        db,
        variaveis["SEED_DIRECAO_NOME"],
        variaveis["SEED_DIRECAO_EMAIL"],
        variaveis["SEED_DIRECAO_SENHA"],
    )
    ja_tem_dados = db.session.scalars(db.select(Assistido).limit(1)).first() is not None
    criados = {}
    if not ja_tem_dados:
        criados = carregar_demonstracao(db, direcao, variaveis["SEED_SENHA_PADRAO"], hoje=hoje)
    db.session.commit()
    return {"direcao_criada": criou_direcao, "demonstracao_criada": not ja_tem_dados, **criados}


def main():
    try:
        variaveis = ler_ambiente()
    except SeedRecusado as erro:
        print(f"seed: {erro}", file=sys.stderr)
        return 1

    from app import create_app
    from app.extensions import db

    app = create_app()
    with app.app_context():
        resultado = semear(db, variaveis)
    print(
        "seed: direção "
        + ("criada" if resultado["direcao_criada"] else "já existia")
        + "; demonstração "
        + ("carregada" if resultado["demonstracao_criada"] else "já existia")
        + "."
    )
    return 0


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    sys.exit(main())
