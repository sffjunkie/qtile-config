import os
from pathlib import Path

import yaml

FILENAME = "secrets.yaml"

def load_secrets() -> dict:
    secrets_file = None
    xdg_config = os.environ.get("XDG_CONFIG_HOME", None)
    if xdg_config:
        secrets_file = Path(xdg_config) / "qtile" / FILENAME
    
    if not secrets_file:
        secrets_file = Path(__file__).parent / FILENAME

    if secrets_file.exists():
        with open(secrets_file, "r") as fp:
            secrets = yaml.load(fp, yaml.SafeLoader)
        return secrets
    else:
        return {}
