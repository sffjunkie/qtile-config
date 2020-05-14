import re

from typing import List

from libqtile.config import Match, Rule


def build_rules() -> List[Rule]:
    return [
        # Floating types
        Rule(
            Match(
                wm_type=[
                    "confirm",
                    "dialog",
                    "download",
                    "notification",
                    "toolbar",
                    "splash",
                    "dialog",
                    "error",
                    "file_progress",
                    "confirmreset",
                    "makebranch",
                    "maketag",
                    "branchdialog",
                    "pinentry",
                    "sshaskpass",
                ]
            ),
            float=True,
            break_on_match=False,
        ),
        # Floating classes
        Rule(
            Match(
                wm_class=[
                    "Nitrogen",
                    "Lightdm-gtk-greeter-settings",
                    "Pavucontrol",
                    "Volumeicon",
                    "Virt-manager",
                    "Gnome-calculator",
                    "Arandr",
                    "vlc",
                    "Gucharmap",
                    re.compile("VirtualBox"),
                ]
            ),
            float=True,
            break_on_match=False,
        ),
    ]
