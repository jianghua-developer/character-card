from pathlib import Path


def safe_resolve_path(input_path: Path) -> Path:
    return input_path.resolve()


def sanitize_filename(filename: str) -> str:
    sanitized = filename.replace('/', '').replace('\\', '')
    sanitized = sanitized.replace('\0', '')
    sanitized = ''.join(c for c in sanitized if ord(c) > 31 or c in ['\t', '\n', '\r'])
    return sanitized
