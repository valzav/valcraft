from src.config.loader import load_model_reference


def test_loads_four_fields(tmp_path, monkeypatch):
    monkeypatch.setenv("KEY", "x")
    cfg = tmp_path / "c.toml"
    cfg.write_text('[model]\nprovider="p"\nmodel="m"\nbase_url="http://h"\napi_key_env="KEY"\n')
    assert load_model_reference(str(cfg)).provider == "p"
