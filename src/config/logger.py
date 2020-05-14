from pathlib import Path

log_path = Path(__file__).parent / "settings.log"

def log(text):
    with open(log_path, "a") as fp:
        fp.write(text + "\n")
    