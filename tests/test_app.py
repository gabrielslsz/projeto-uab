import importlib
import sys
from pathlib import Path


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
    from app.services.job_queue import aguardar_jobs

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
    aguardar_jobs()

    with application.app_context():
        atendente = models_module.UsuarioModel.query.filter_by(email="bruno@empresa.com").first()
        log = models_module.LogOperacaoModel.query.filter_by(acao="CRIAR_ATENDENTE").first()

    assert atendente is not None
    assert atendente.role == "ATENDENTE"
    assert log is not None
    assert log.registro_afetado_id == atendente.id


def test_login_page_renders_accessible_form(tmp_path, monkeypatch):
    application, _, _ = _load_app(tmp_path, monkeypatch)

    response = application.test_client().get("/login")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Pular para o conteúdo principal" in page
    assert "data-enhanced-form" in page
    assert 'aria-live="polite"' in page
    assert 'autocomplete="email"' in page
    assert 'autocomplete="current-password"' in page


def test_admin_panel_renders_form_and_empty_state(tmp_path, monkeypatch):
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

    response = client.get("/admin/painel")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Criar atendente" in page
    assert "data-enhanced-form" in page
    assert "empty-state" in page


def test_frontend_assets_include_responsive_and_accessibility_rules(tmp_path, monkeypatch):
    application, _, _ = _load_app(tmp_path, monkeypatch)
    project_root = Path(application.root_path).parent
    css_path = project_root / "app" / "static" / "css" / "frontend.css"
    js_path = project_root / "app" / "static" / "js" / "frontend.js"

    css = css_path.read_text(encoding="utf-8")
    js = js_path.read_text(encoding="utf-8")

    assert "@media (max-width: 575.98px)" in css
    assert ":focus-visible" in css
    assert ".skeleton" in css
    assert "AbortController" in js
    assert "Tempo limite excedido" in js
    assert "data-enhanced-form" in js


def test_form_endpoints_preserve_error_contracts(tmp_path, monkeypatch):
    application, database, models_module = _load_app(tmp_path, monkeypatch)

    with application.app_context():
        usuario = models_module.UsuarioModel(nome="Ana", email="ana@empresa.com", role="ADMINISTRADOR")
        usuario.set_senha("123456")
        database.session.add(usuario)
        database.session.commit()

    client = application.test_client()

    response_login = client.post("/login", data={"email": "ana@empresa.com", "senha": "senha-incorreta"})
    response_cadastro = client.post(
        "/cadastro-cliente",
        data={"nome": "Ana", "email": "ana@empresa.com", "senha": "123456"},
    )

    assert response_login.status_code == 401
    assert "Credenciais Inválidas" in response_login.get_data(as_text=True)
    assert response_cadastro.status_code == 409
    assert "Email já em uso" in response_cadastro.get_data(as_text=True)