import ulid as _ulid


def ulid() -> str:
    """
    generate id
    """
    return _ulid.microsecond.new().str.lower()
