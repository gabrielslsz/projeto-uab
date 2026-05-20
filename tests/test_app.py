import importlib
import sys

import pytest


@pytest.fixture()
def app_context(tmp_path, monkeypatch):
    database_path = tmp_path / "gratia.db"
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("GRATIA_DATABASE_URI", f"sqlite:///{database_path}")

    for module_name in [name for name in list(sys.modules) if name == "config" or name == "app" or name.startswith("app.") or name == "seed"]:
        sys.modules.pop(module_name, None)

    importlib.import_module("config")
    app_module = importlib.import_module("app")
    database_module = importlib.import_module("app.database")
    models_module = importlib.import_module("app.models.models")

    application = app_module.create_app()

    with application.app_context():
        database_module.db.drop_all()
        database_module.db.create_all()

    return application, database_module.db, models_module


def test_factory_registers_expected_blueprints(app_context):
    application, _, _ = app_context

    assert set(application.blueprints) == {"fiel", "sacerdote"}


def test_recepcao_lista_sacerdote_disponivel(app_context):
    application, database, models_module = app_context

    with application.app_context():
        sacerdote = models_module.Sacerdote(nome="Padre Antônio", pin_acesso="123456", status="DISPONIVEL")
        database.session.add(sacerdote)
        database.session.commit()

    response = application.test_client().get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Padre Antônio" in page
    assert "Escolha seu Confessor" in page


def test_fiel_entra_na_fila_e_ve_status(app_context):
    application, database, models_module = app_context

    with application.app_context():
        sacerdote = models_module.Sacerdote(nome="Padre José", pin_acesso="654321", status="DISPONIVEL")
        database.session.add(sacerdote)
        database.session.commit()
        sacerdote_id = sacerdote.id

    client = application.test_client()
    response = client.post(
        "/entrar-fila",
        data={"sacerdote_id": sacerdote_id, "nome_exibicao": "Gabriel", "whatsapp": "11999999999"},
    )

    assert response.status_code == 302
    assert "/status/" in response.headers["Location"]

    with application.app_context():
        atendimento = models_module.Atendimento.query.filter_by(identificador_exibicao="Gabriel").first()
        atendimento_id = atendimento.id

    assert atendimento is not None
    status_page = application.test_client().get(f"/status/{atendimento_id}").get_data(as_text=True)

    assert "Gabriel" in status_page
    assert "Sua posição na fila é:" in status_page
    assert "1º" in status_page


def test_sacerdote_login_dashboard_e_chamada(app_context):
    application, database, models_module = app_context

    with application.app_context():
        sacerdote = models_module.Sacerdote(nome="Padre João", pin_acesso="123456", status="DISPONIVEL")
        database.session.add(sacerdote)
        database.session.commit()
        sacerdote_id = sacerdote.id

        atendimento = models_module.Atendimento(
            identificador_exibicao="Fiel-1",
            telefone="11988887777",
            tipo="FILA",
            sacerdote_id=sacerdote_id,
            status="AGUARDANDO",
        )
        database.session.add(atendimento)
        database.session.commit()
        atendimento_id = atendimento.id

    client = application.test_client()
    login_response = client.post("/sacerdote/login", data={"pin": "123456"})

    assert login_response.status_code == 302
    assert login_response.headers["Location"].endswith("/sacerdote/dashboard")

    dashboard_page = client.get("/sacerdote/dashboard").get_data(as_text=True)
    assert "Padre João" in dashboard_page
    assert "Fiel-1" in dashboard_page or "CHAMANDO AGORA" in dashboard_page

    chamar_response = client.post("/sacerdote/chamar-proximo")
    assert chamar_response.status_code == 200
    assert chamar_response.get_json()["success"] is True

    with application.app_context():
        atendimento_atualizado = models_module.Atendimento.query.filter_by(id=atendimento_id).first()
        sacerdote_atualizado = models_module.Sacerdote.query.filter_by(id=sacerdote_id).first()

    assert atendimento_atualizado.status == "CHAMADO"
    assert sacerdote_atualizado.status == "DISPONIVEL"

    status_response = client.post(
        "/sacerdote/alterar-status",
        json={"status": "PAUSADO"},
    )

    assert status_response.status_code == 200
    assert status_response.get_json()["success"] is True

    with application.app_context():
        sacerdote_atualizado = models_module.Sacerdote.query.filter_by(id=sacerdote_id).first()

    assert sacerdote_atualizado.status == "PAUSADO"


def test_seed_cria_sacerdotes_de_teste(app_context):
    application, database, models_module = app_context
    import seed

    seed.seed()

    with application.app_context():
        sacerdotes = models_module.Sacerdote.query.order_by(models_module.Sacerdote.nome.asc()).all()

    assert len(sacerdotes) == 2
    assert {s.nome for s in sacerdotes} == {"Padre Antônio", "Padre José"}
