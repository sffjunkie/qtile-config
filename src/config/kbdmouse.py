# Keybindings for groups are defined in groups.py

from os import environ
from typing import List  # noqa: F401

from libqtile import extension
from libqtile.config import Key, Drag, Click
from libqtile.command import lazy

import settings

alt = "mod1"


def bind_keys(settings) -> List[Key]:
    return [
        # region QTile Control
        Key([settings["mod"], alt], "r", lazy.restart(), desc="Restart QTile"),
        Key([settings["mod"], alt], "q", lazy.shutdown(), desc="Quit QTile"),
        # endregion
        # region Window Control
        Key(
            [settings["mod"], "shift"],
            "c",
            lazy.window.kill(),
            desc="Close window",
        ),
        Key(
            [settings["mod"], "mod1"],
            "Left",
            lazy.screen.prev_group(),
            desc="Switch to next group",
        ),
        Key(
            [settings["mod"], "mod1"],
            "Right",
            lazy.screen.next_group(),
            desc="Switch to previous group",
        ),
        Key(
            [settings["mod"], alt],
            "f",
            lazy.window.toggle_floating(),
            desc="Toggle floating window",
        ),
        # Toggle between different layouts as defined below
        Key([settings["mod"]], "grave", lazy.next_layout(), desc="Switch to next layout"),
        # Move window in stack
        Key(
            [settings["mod"], "shift"],
            "Right",
            lazy.layout.shuffle_down(),
            desc="Move window down in stack",
        ),
        Key(
            [settings["mod"], "shift"],
            "Left",
            lazy.layout.shuffle_up(),
            desc="Move window up in stack",
        ),
        Key(
            [settings["mod"], "shift"],
            "l",
            lazy.layout.shuffle_down(),
            desc="Move window down in stack",
        ),
        Key(
            [settings["mod"], "shift"],
            "h",
            lazy.layout.shuffle_up(),
            desc="Move window up in stack",
        ),
        # Switch between windows in current stack pane
        Key([settings["mod"]], "h", lazy.layout.up(), desc="Previous window"),
        Key([settings["mod"]], "l", lazy.layout.down(), desc="Next window"),
        Key([settings["mod"]], "Left", lazy.layout.up(), desc="Previous window"),
        Key([settings["mod"]], "Right", lazy.layout.down(), desc="Next window"),
        # Resize
        Key(
            [settings["mod"], "control"],
            "Right",
            lazy.layout.grow_main(),
            desc="Increase Main Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "l",
            lazy.layout.grow_main(),
            desc="Increase Main Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "Left",
            lazy.layout.shrink_main(),
            desc="Decrease Main Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "h",
            lazy.layout.shrink_main(),
            desc="Decrease Main Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "Up",
            lazy.layout.grow(),
            desc="Increase Sub Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "j",
            lazy.layout.grow(),
            desc="Increase Sub Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "Down",
            lazy.layout.shrink(),
            desc="Decrease Sub Window Size",
        ),
        Key(
            [settings["mod"], "control"],
            "k",
            lazy.layout.shrink(),
            desc="Decrease Sub Window Size",
        ),
        # endregion
    ]


# Drag floating layouts.
def bind_mouse_buttons(settings):
    return [
        Drag(
            [settings["mod"]],
            "Button1",
            lazy.window.set_position_floating(),
            start=lazy.window.get_position(),
        ),
        Drag(
            [settings["mod"]],
            "Button3",
            lazy.window.set_size_floating(),
            start=lazy.window.get_size(),
        ),
        Click([settings["mod"]], "Button2", lazy.window.bring_to_front()),
    ]
