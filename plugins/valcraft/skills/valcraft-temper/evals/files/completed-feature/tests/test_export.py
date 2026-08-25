from src.export import export_record


def test_export_returns_stored_fields():
    assert export_record({"b": 2, "a": 1}) == {"a": 1, "b": 2}
