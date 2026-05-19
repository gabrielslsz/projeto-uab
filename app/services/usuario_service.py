from dataclasses import dataclass
from threading import RLock

from werkzeug.security import check_password_hash

from app.database import db
from app.models.usuario_model import UsuarioModel


class EmailJaEmUsoError(ValueError):
    pass


@dataclass(frozen=True)
class UsuarioResumo:
    id: int
    role: str
    senha_hash: str


_CACHE_SENTINEL = object()
_cache = {}
_cache_lock = RLock()


def limpar_cache_usuarios():
    with _cache_lock:
        _cache.clear()


def normalizar_email(email):
    return (email or "").strip().lower()


def _cache_get(email):
    with _cache_lock:
        return _cache.get(email, _CACHE_SENTINEL)


def _cache_set(email, usuario_resumo):
    with _cache_lock:
        _cache[email] = usuario_resumo


def buscar_usuario_resumo_por_email(email):
    email_normalizado = normalizar_email(email)
    cached = _cache_get(email_normalizado)
    if cached is not _CACHE_SENTINEL:
        return cached

    usuario = UsuarioModel.query.filter_by(email=email_normalizado).first()
    if usuario is None:
        _cache_set(email_normalizado, None)
        return None

    resumo = UsuarioResumo(id=usuario.id, role=usuario.role, senha_hash=usuario.senha_hash)
    _cache_set(email_normalizado, resumo)
    return resumo


def autenticar_usuario(email, senha):
    usuario = buscar_usuario_resumo_por_email(email)
    if usuario is None:
        return None
    if not check_password_hash(usuario.senha_hash, senha):
        return None
    return usuario


def email_em_uso(email):
    return buscar_usuario_resumo_por_email(email) is not None


def criar_usuario(nome, email, senha, role, criado_por_id=None):
    email_normalizado = normalizar_email(email)
    if email_em_uso(email_normalizado):
        raise EmailJaEmUsoError(email_normalizado)

    usuario = UsuarioModel(
        nome=(nome or "").strip(),
        email=email_normalizado,
        role=role,
        criado_por_id=criado_por_id,
    )
    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()
    limpar_cache_usuarios()
    return usuario


def garantir_proprietario_inicial(application):
    email = application.config["PROPRIETARIO_EMAIL"]
    if email_em_uso(email):
        return None

    return criar_usuario(
        nome="Proprietário Principal",
        email=email,
        senha=application.config["PROPRIETARIO_PASSWORD"],
        role="PROPRIETARIO",
    )