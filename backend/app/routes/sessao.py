"""Sessão por JWT. Spec 01.

Autenticação (quem é você) fica aqui. Cada blueprint de dado chama
`exigir_login(bp)`: a verificação roda antes de qualquer rota dele, então
rota nova já nasce protegida.

O usuário é lido do banco a cada requisição: conta desativada ou
inexistente derruba a sessão na hora, e o perfil vale o do banco, não o
do token.
"""

from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import current_user, verify_jwt_in_request

from app.errors import PermissaoNegada
from app.extensions import db

ENTRE = "Entre no sistema para continuar."
INVALIDA = "Sessão inválida. Entre de novo."
EXPIRADA = "Sessão expirada. Entre de novo."
ENCERRADA = "Sessão encerrada. Entre de novo."


def _nao_autorizado(mensagem):
    return jsonify({"erro": mensagem}), 401


def configurar_sessao(jwt):
    """Liga o JWTManager ao banco e às mensagens da spec 01."""
    from app.models import TokenRevogado, Usuario

    @jwt.token_in_blocklist_loader
    def _encerrado_por_logout(_cabecalho, dados):
        return TokenRevogado.revogado(dados["jti"])

    @jwt.user_lookup_loader
    def _carregar_usuario(_cabecalho, dados):
        try:
            usuario_id = int(dados["sub"])
        except (KeyError, TypeError, ValueError):
            return None
        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None or not usuario.ativo:
            return None
        return usuario

    @jwt.user_lookup_error_loader
    def _usuario_fora(_cabecalho, _dados):
        return _nao_autorizado(ENCERRADA)

    @jwt.unauthorized_loader
    def _sem_token(_motivo):
        return _nao_autorizado(ENTRE)

    @jwt.invalid_token_loader
    def _token_invalido(_motivo):
        return _nao_autorizado(INVALIDA)

    @jwt.token_verification_failed_loader
    def _verificacao_falhou(_cabecalho, _dados):
        return _nao_autorizado(INVALIDA)

    @jwt.expired_token_loader
    def _token_expirado(_cabecalho, _dados):
        return _nao_autorizado(EXPIRADA)

    @jwt.revoked_token_loader
    def _token_revogado(_cabecalho, _dados):
        return _nao_autorizado(ENCERRADA)


def exigir_login(blueprint):
    """Toda rota do blueprint exige token válido e conta ativa."""

    @blueprint.before_request
    def _sessao_valida():
        # Pré-voo do CORS não leva Authorization; quem responde é o flask-cors.
        if request.method == "OPTIONS":
            return None
        verify_jwt_in_request()
        return None

    return blueprint


def usuario_atual():
    """O Usuario do token, carregado do banco nesta requisição."""
    return current_user._get_current_object()


def exige_permissao(permissao, mensagem):
    """Autorização por rota (card #15). Sem a permissão, 403 com `mensagem`.

    `permissao` é o nome de um método polimórfico de Usuario, como
    "pode_gerir_usuarios": a rota não compara o texto do perfil.
    """

    def decorador(rota):
        @wraps(rota)
        def protegida(*args, **kwargs):
            verify_jwt_in_request()
            if not getattr(usuario_atual(), permissao)():
                raise PermissaoNegada(mensagem)
            return rota(*args, **kwargs)

        return protegida

    return decorador
