import os
import glob
from pathlib import Path
from typing import Dict, Optional
import yaml

from utils import is_base16, is_color

# from logger import log


FONT = "Roboto Mono for Powerline"
ICON_FONT = "Material Design Icons"
FONT_SIZE = 14
BAR_HEIGHT = 22

COLOR_SCHEME = {
    "base00": "f9f5d7",
    "base01": "ebdbb2",
    "base02": "d5c4a1",
    "base03": "bdae93",
    "base04": "665c54",
    "base05": "504945",
    "base06": "3c3836",
    "base07": "282828",
    "base08": "9d0006",
    "base09": "af3a03",
    "base0A": "b57614",
    "base0B": "79740e",
    "base0C": "427b58",
    "base0D": "076678",
    "base0E": "8f3f71",
    "base0F": "d65d0e",
}

WIDGET = {
    "font": FONT,
    "fontsize": FONT_SIZE,
    "margin": 0,
    "padding": 0,
    "foreground": "base07",
    "background": "base01",
}


EXTENSION = {
    "font": FONT,
    "fontsize": FONT_SIZE,
    "foreground": "base07",
    "background": "base01",
}

LAYOUT = {
    "margin": 3,
    "border_width": 3,
    "border_focus": "d5c4a1",
    "border_normal": "282828",
}


# def _update_colors(d, color_scheme=COLOR_SCHEME):
#     res = {}
#     for k, v in d.items():
#         if isinstance(v, str) and is_base16(v):
#             try:
#                 v = COLOR_SCHEME[v]
#             except KeyError:
#                 pass  # TODO: raise and exception here?
#         res[k] = v
#     return res


def _default_colors(color_scheme: Dict = COLOR_SCHEME) -> Dict:
    return {
        "panel_fg": color_scheme["base07"],
        "panel_bg": color_scheme["base01"],
        "group_current_fg": color_scheme["base05"],
        "group_current_bg": color_scheme["base03"],
        "group_active_fg": color_scheme["base07"],
        "group_active_bg": color_scheme["base04"],
        "group_inactive_fg": color_scheme["base07"],
        "group_inactive_bg": color_scheme["base04"],
        "powerline_fg": color_scheme["base01"],
        "powerline_bg": [
            color_scheme["base08"],
            color_scheme["base09"],
            color_scheme["base0A"],
            color_scheme["base0B"],
            color_scheme["base0C"],
            color_scheme["base0D"],
            color_scheme["base0E"],
            color_scheme["base0F"],
        ],
    }


DEFAULT_THEME = {
    "font": FONT,
    "iconfont": ICON_FONT,
    "fontsize": FONT_SIZE,
    "barheight": BAR_HEIGHT,
    "color": COLOR_SCHEME,
    "widget": WIDGET,
    "layout": LAYOUT,
    "extension": EXTENSION,
}


def _deref_colors(theme_info, color_scheme, colors):
    d = {}
    for name, value in theme_info.items():
        if not isinstance(value, (int, float, bool)) and not is_color(value):
            if is_base16(value):
                if color_scheme is None:
                    color_scheme = COLOR_SCHEME
                value = color_scheme[value]
            elif value in colors:
                value = colors[value]

        d[name] = value
    return d


def _load_color_scheme(
    scheme_file: str, scheme_folder: Optional[str] = None
) -> Optional[Dict]:
    if not scheme_folder:
        xdg_data_home = os.environ.get("XDG_DATA_HOME", None)
        if xdg_data_home is not None:
            scheme_folder = Path(xdg_data_home) / "base16" / "schemes"
        else:
            scheme_folder = Path(__file__).parent.parent / "schemes"

    scheme_file = Path(scheme_file)
    if scheme_file.suffix != ".yaml":
        scheme_file = scheme_file.with_suffix(".yaml")

    for file_path in scheme_folder.rglob(os.path.join("**", "*.yaml")):
        if file_path.name.endswith(scheme_file.name):
            with open(file_path, "r") as fp:
                colors = yaml.load(fp, Loader=yaml.SafeLoader)
                return colors
    return COLOR_SCHEME


def _load_theme_config(filename: str) -> Dict:
    if filename[0] != "/":
        xdg_config = os.environ.get("XDG_CONFIG_HOME", None)
        if xdg_config:
            p = Path(xdg_config)
            theme_conf = p / "qtile" / "theme.yaml"
        else:
            theme_conf = Path(__file__).parent / "theme.yaml"
    else:
        theme_conf = Path(filename)

    if theme_conf.exists():
        with open(theme_conf, "r") as fp:
            theme = yaml.load(fp, yaml.SafeLoader)
        return theme


def load_theme(filename: str = "theme.yaml") -> Dict:
    theme = DEFAULT_THEME.copy()
    theme_config = _load_theme_config(filename)

    if "base16_scheme_name" in theme_config:
        color_scheme = _load_color_scheme(theme_config.pop("base16_scheme_name"))
        theme_config["base16_scheme"] = color_scheme
    elif "base16_scheme" not in theme_config:
        theme_config["base16_scheme"] = COLOR_SCHEME

    colors = _default_colors(theme_config["base16_scheme"])

    widget = WIDGET.copy()
    if "widget" in theme_config:
        widget.update(theme_config["widget"])

    tc = _deref_colors(widget, theme_config["base16_scheme"], colors)
    widget.update(tc)

    extension = EXTENSION.copy()
    if "extension" in theme_config:
        extension.update(theme_config["extension"])

    tc = _deref_colors(extension, theme_config["base16_scheme"], colors)
    extension.update(tc)

    layout = LAYOUT.copy()
    if "layout" in theme_config:
        layout.update(theme_config["layout"])

    tc = _deref_colors(layout, theme_config["base16_scheme"], colors)
    layout.update(tc)

    theme["color"] = colors
    theme["widget"] = widget
    theme["extension"] = extension
    theme["layout"] = layout

    for k, v in theme_config.items():
        if k not in ["color", "widget", "extension", "layout"]:
            # for item in ["font", "iconfont", "fontsize", "barheight", "powerline_separator"]:
            #     if item in theme_config:
            theme[k] = theme_config[k]

    return theme
