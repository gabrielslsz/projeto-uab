import importlib
import sys


def _load_app(tmp_path, monkeypatch):
    database_path = tmp_path / "atendimento.db"
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("DATABASE_URI", f"sqlite:///{database_path}")
    monkeypatch.setenv("DEBUG_MODE", "False")
    monkeypatch.setenv("PROPRIETARIO_EMAIL", "admin@empresa.com")
    monkeypatch.setenv("PROPRIETARIO_PASSWORD", "senha_segura_inicial")

    for module_name in [name for name in list(sys.modules) if name == "config" or name == "app" or name.startswith("app.")]:
        sys.modules.pop(module_name, None)

    config_module = importlib.import_module("config")
    importlib.reload(config_module)

    app_module = importlib.import_module("app")
    database_module = importlib.import_module("app.database")
    models_module = importlib.import_module("app.models")

    application = app_module.create_app()

    with application.app_context():
        database_module.db.drop_all()
        database_module.db.create_all()

    return application, database_module.db, models_module


def test_factory_registers_expected_blueprints(tmp_path, monkeypatch):
    application, _, _ = _load_app(tmp_path, monkeypatch)

    assert set(application.blueprints) == {
        "auth",
        "proprietario",
        "administrador",
        "atendente",
        "cliente",
    }


def test_owner_is_seeded_on_bootstrap(tmp_path, monkeypatch):
    application, _, models_module = _load_app(tmp_path, monkeypatch)

    from run import initialize_database

    initialize_database(application)

    with application.app_context():
        owner = models_module.UsuarioModel.query.filter_by(email="admin@empresa.com").first()

    assert owner is not None
    assert owner.role == "PROPRIETARIO"
    assert owner.check_senha("senha_segura_inicial")


def test_login_redirects_by_role(tmp_path, monkeypatch):
    application, database, models_module = _load_app(tmp_path, monkeypatch)

    with application.app_context():
        usuario = models_module.UsuarioModel(nome="Ana", email="ana@empresa.com", role="ADMINISTRADOR")
        usuario.set_senha("123456")
        database.session.add(usuario)
        database.session.commit()

    client = application.test_client()
    response = client.post("/login", data={"email": "ana@empresa.com", "senha": "123456"})

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/painel")


def test_admin_can_create_atendente_and_log(tmp_path, monkeypatch):
    application, database, models_module = _load_app(tmp_path, monkeypatch)

    with application.app_context():
        admin = models_module.UsuarioModel(nome="Admin", email="admin@empresa.com", role="ADMINISTRADOR")
        admin.set_senha("123456")
        database.session.add(admin)
        database.session.commit()
        admin_id = admin.id

    client = application.test_client()
    with client.session_transaction() as session_data:
        session_data["user_id"] = admin_id
        session_data["user_role"] = "ADMINISTRADOR"

    response = client.post(
        "/admin/atendentes/novo",
        data={"nome": "Bruno", "email": "bruno@empresa.com", "senha": "abcdef"},
    )

    assert response.status_code == 201

    with application.app_context():
        atendente = models_module.UsuarioModel.query.filter_by(email="bruno@empresa.com").first()
        log = models_module.LogOperacaoModel.query.filter_by(acao="CRIAR_ATENDENTE").first()

    assert atendente is not None
    assert atendente.role == "ATENDENTE"
    assert log is not None
    assert log.registro_afetado_id == atendente.id