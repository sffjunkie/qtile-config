import os
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

import yaml

from secrets import load_secrets
from theme import load_theme

DEFAULT_SETTINGS = {
    "mod": "mod4",
    "term": "alacritty",
    "natural_scroll": False,
}

VOLUMESTEP = 5


class VolumeType(Enum):
    PULSE = 1
    ALSA = 2


VOLUME_TYPE = VolumeType.PULSE


def volume_control_commands() -> Dict:
    if VOLUME_TYPE == VolumeType.PULSE:
        return {
            "up": f"pulsemixer --change-volume +{VOLUMESTEP}",
            "down": f"pulsemixer --change-volume -{VOLUMESTEP}",
            "mute": "pulsemixer --mute",
            "toggle": "pulsemixer --toggle-mute",
            "app": "pavucontrol",
        }
    else:
        return {
            "up": f"amixer sset Master '{VOLUMESTEP}'%+",
            "down": f"amixer sset Master '{VOLUMESTEP}'%-",
            "mute": "amixer sset Master mute",
            "toggle": "amixer sset Master toggle-mute",
            "app": "pavucontrol",
        }


def load_settings() -> Dict:
    settings = {
        "theme": load_theme(),
        "volume": volume_control_commands(),
    }

    settings.update(DEFAULT_SETTINGS)

    settings["secrets"] = load_secrets()

    settings_file = Path(__file__).parent / "settings.yaml"
    if settings_file.exists():
        with open(settings_file, "r") as fp:
            settings_yaml = yaml.load(fp, yaml.SafeLoader)
        settings.update(settings_yaml)

    return settings
