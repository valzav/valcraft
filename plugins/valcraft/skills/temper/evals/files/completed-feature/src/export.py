"""Record export."""


def export_record(record):
    """Return a record's stored fields in key order."""
    return {key: record[key] for key in sorted(record)}
