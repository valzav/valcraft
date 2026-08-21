from src.export import export_record
from src.report import field_count


def test_export_reports_field_count():
    assert field_count(export_record({"a": 1, "b": 2})) == 2
