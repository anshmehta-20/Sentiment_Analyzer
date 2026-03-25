from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def data_file(filename: str) -> Path:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Expected data file was not found: {path}")
    return path


def output_file(filename: str) -> Path:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUTS_DIR / filename


def existing_output_file(filename: str) -> Path:
    path = output_file(filename)
    if not path.exists():
        raise FileNotFoundError(f"Expected output file was not found: {path}")
    return path
