import os
import socket
import subprocess
import sys
from pathlib import Path
from typing import List  # noqa: F401

from libqtile import bar, extension, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Group, Key, Screen

import yaml

import bar
import group
import kbdmouse
import rule
import secrets
import settings

sec = secrets.load_secrets()
s = settings.load_settings()
keys = kbdmouse.bind_keys(s)
mouse = kbdmouse.bind_mouse_buttons(s)
groups = group.build_groups(s)
group.bind_group_keys(s, keys)
bar = bar.build_bar(s, sec)

theme = s["theme"]
layouts = [
    layout.MonadTall(**theme["layout"]),
    layout.Max(**theme["layout"]),
]

screens = [Screen(top=bar[0], bottom=bar[1])]

widget_defaults = theme["widget"].copy()
extension_defaults = theme["extension"].copy()

dgroups_key_binder = None
dgroups_app_rules = rule.build_rules()  # type: List
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.client_new
def client_to_group(client):
    wm_class = client.window.get_wm_class()[0]
    group_name = group.find_group_for(wm_class)
    if group_name:
        client.togroup(group_name)
        # lazy.group[group_name].cmd_toscreen()


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
