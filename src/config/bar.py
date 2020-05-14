import os
import socket
from pathlib import Path
from typing import List
from subprocess import Popen

from libqtile import bar, widget, config
from libqtile.command import lazy

from widgets import NetMin, EscapedWindowName, FixedWidthVolume, OpenWeatherMap

# from pl import Powerline, Segment, Side

def build_bar(settings: dict, secrets: dict = {}) -> List[bar.Bar]:
    theme = settings["theme"]
    barheight = theme["barheight"]
    font = theme["font"]
    iconfont = theme["iconfont"]
    fontsize = theme["fontsize"]
    theme_colors = theme["color"]
    owm_location_args = {}
    if "latitude" in secrets:
        owm_location_args["latitude"] = secrets["latitude"]
    if "longitude" in secrets:
        owm_location_args["longitude"] = secrets["longitude"]
    

    def _fg_sep():
        return widget.Sep(linewidth=0, padding=6, background=theme_colors["panel_fg"],)

    def _bg_sep():
        return widget.Sep(linewidth=0, padding=6, background=theme_colors["panel_bg"],)

    def _line_sep():
        return widget.Sep(
            linewidth=1,
            size_percent=50,
            padding=18,
            foreground="888888",
            background=theme_colors["panel_bg"],
        )

    top_bar_widgets = [
        # region LHS
        _fg_sep(),
        widget.TextBox(
            text=chr(983044),
            font=iconfont,
            fontsize=fontsize + 6,
            foreground=theme_colors["panel_bg"],
            background=theme_colors["panel_fg"],
        ),
        _fg_sep(),
        _bg_sep(),
        widget.GroupBox(
            margin_y=3,
            margin_x=2,
            padding_y=5,
            padding_x=5,
            borderwidth=0,
            foreground=theme_colors["panel_fg"],
            background=theme_colors["panel_bg"],
            active=theme_colors["group_active_fg"],
            inactive=theme_colors["group_inactive_fg"],
            rounded=True,
            highlight_method="block",
            this_current_screen_border=theme_colors["group_current_bg"],
            this_screen_border=theme_colors["group_current_bg"],
            # other_current_screen_border=theme_colors["panel_bg"],
            # other_screen_border=theme_colors["panel_bg"],
        ),
        _line_sep(),
        widget.CurrentLayout(
            foreground=theme_colors["panel_fg"], background=theme_colors["panel_bg"],
        ),
        _line_sep(),
        EscapedWindowName(
            padding=5,
            foreground=theme_colors["panel_fg"],
            background=theme_colors["panel_bg"],
        ),
        # endregion
        # region RHS
        # Systray
        widget.TextBox(
            text=theme["powerline_separator"][0],
            fontsize=barheight + 8,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][4],
            background=theme_colors["panel_bg"],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][4],),
        widget.Systray(
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][4],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][4],),
        widget.TextBox(
            text=chr(987798),
            font=iconfont,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][4],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][4],),
        # OpenWeatherMap
        widget.TextBox(
            text=theme["powerline_separator"][0],
            font=font,
            fontsize=barheight + 6,
            margin=0,
            padding=0,
            foreground=theme_colors["powerline_bg"][3],
            background=theme_colors["powerline_bg"][4],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][3],),
        OpenWeatherMap(
            format='{temp:.1f}{temp_units} <span face="{icon_font}">{icon}</span>',
            apikey=secrets["owm_apikey"],
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][3],
            **owm_location_args,
        ),
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=theme_colors["panel_fg"],
            background=theme_colors["powerline_bg"][3],
        ),
        # volume control
        widget.TextBox(
            text=theme["powerline_separator"][0],
            font=font,
            fontsize=barheight + 6,
            margin=0,
            padding=0,
            foreground=theme_colors["powerline_bg"][2],
            background=theme_colors["powerline_bg"][3],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][2],),
        FixedWidthVolume(
            # iconfont = "Material Design Icons",
            volume_up_command=settings["volume"]["up"],
            volume_down_command=settings["volume"]["down"],
            mute_command=settings["volume"]["toggle"],
            volume_app=settings["volume"]["app"],
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][2],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][2],),
        widget.TextBox(
            text=theme["powerline_separator"][0],
            fontsize=barheight + 6,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][1],
            background=theme_colors["powerline_bg"][2],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][1],),
        widget.Mpd2(
            status_format="{play_status} {artist} | {title} | {album}",
            idle_format="Play queue empty",
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][1],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][1],),
        widget.TextBox(
            text=chr(984922),
            font=iconfont,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][1],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][1],),
        # Clock
        widget.TextBox(
            text=theme["powerline_separator"][0],
            fontsize=barheight + 6,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][0],
            background=theme_colors["powerline_bg"][1],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][0],),
        widget.Clock(
            format="%a %Y-%m-%d",
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][0],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][0],),
        # calendar symbol
        widget.TextBox(
            text=chr(983277),
            font=iconfont,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][0],
        ),
        widget.Sep(
            linewidth=0,
            padding=12,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][0],
        ),
        widget.Clock(
            format="%H:%M",
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][0],
        ),
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][0],
        ),
        # clock symbol
        widget.TextBox(
            text=chr(983376),
            font=iconfont,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][0],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][0],),
        # endregion
    ]

    if "logo" in theme:
        top_bar_widgets.append(
            widget.TextBox(
                text=f"  {theme['logo']}  ",
                font=theme["logofont"],
                foreground=theme_colors["powerline_fg"],
                background=theme_colors["powerline_bg"][-1],
            ),
        )

    # def cpu_button(*args, **kwargs):
    #     command = [settings["term"], "-e", "htop"]
    #     Popen(command, shell=True)
    # with open(os.path.expanduser("~/cpu_button"), "w") as fp:
    #     fp.write(f"command={command}")

    bottom_bar_widgets = [
        # Updates
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][3],),
        widget.TextBox(
            text=chr(984752),
            font=iconfont,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][3],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][3],),
        widget.CheckUpdates(
            distro="Arch",
            execute="alacritty",
            update_interval=1800,
            display_format="{updates} Updates",
            colour_no_updates=theme_colors["powerline_fg"],
            colour_have_updates=theme_colors["panel_fg"],
            background=theme_colors["powerline_bg"][3],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][3],),
        widget.TextBox(
            text=theme["powerline_separator"][1],
            fontsize=barheight + 6,
            padding=0,
            margin=2,
            foreground=theme_colors["powerline_bg"][3],
            background=theme_colors["powerline_bg"][4],
        ),
        # region Net
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][4],),
        widget.TextBox(
            text=chr(986631),
            font=iconfont,
            fontsize=barheight - 4,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][4],
        ),
        NetMin(
            font=font,
            interface="wlp4s0f3u2",
            format="{up} ",
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][4],
        ),
        widget.TextBox(
            text=chr(985999),
            font=iconfont,
            fontsize=barheight - 4,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][4],
        ),
        NetMin(
            font=font,
            interface="wlp4s0f3u2",
            format="{down}",
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][4],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][4],),
        widget.TextBox(
            text=theme["powerline_separator"][1],
            fontsize=barheight - 4,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][4],
            background=theme_colors["powerline_bg"][5],
        ),
        # endregion
        # region Memory
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][5],),
        widget.TextBox(
            text=chr(983899),
            font=iconfont,
            fontsize=barheight - 4,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][5],
        ),
        widget.Memory(
            format="{MemUsed:5d}M/{MemTotal}M",
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][5],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][5],),
        widget.TextBox(
            text=theme["powerline_separator"][1],
            fontsize=barheight - 4,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][5],
            background=theme_colors["powerline_bg"][6],
        ),
        # endregion
        # region CPU
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][6],),
        widget.TextBox(
            text=chr(986848),
            font=iconfont,
            fontsize=barheight - 4,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][6],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][6],),
        widget.CPU(
            format="{load_percent:4.1f}%",
            update_interval=5,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][6],
            # mouse_callbacks={"Button1": cpu_button},
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][6],),
        widget.TextBox(
            text=theme["powerline_separator"][1],
            fontsize=barheight - 4,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][6],
            background=theme_colors["powerline_bg"][7],
        ),
        # endregion
        # region Temps
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][7],),
        widget.TextBox(
            text=chr(984335),
            font=iconfont,
            fontsize=barheight - 4,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][7],
        ),
        widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_bg"][7],),
        widget.ThermalSensor(
            foreground=theme_colors["powerline_fg"],
            background=theme_colors["powerline_bg"][7],
        ),
        widget.Sep(
            linewidth=0, padding=12, background=theme_colors["powerline_bg"][7],
        ),
        widget.TextBox(
            text=theme["powerline_separator"][1],
            font=font,
            fontsize=barheight - 4,
            padding=0,
            margin=0,
            foreground=theme_colors["powerline_bg"][7],
            background=theme_colors["panel_bg"],
        ),
        # endregion
    ]

    # bottom_pl = Powerline(
    #     theme_colors["powerline_fg"], theme_colors["powerline_bg"], barheight,
    # )
    # ud = Segment(
    #     [
    #         widget.TextBox(
    #             text=chr(984752),
    #             font=iconfont,
    #             foreground=self.fg,
    #             background=self.segment_colors[3],
    #         ),
    #         widget.Sep(linewidth=0, padding=6, background=self.segment_colors[3],),
    #         widget.CheckUpdates(
    #             distro="Arch",
    #             execute="alacritty",
    #             update_interval=1800,
    #             display_format="{updates} Updates",
    #             colour_no_updates=self.fg,
    #             colour_have_updates=theme_colors["panel_fg"],
    #             background=self.segment_colors[3],
    #         ),
    #     ]
    # )

    return [
        bar.Bar(top_bar_widgets, size=barheight, background=theme_colors["panel_bg"]),
        bar.Bar(
            bottom_bar_widgets, size=barheight, background=theme_colors["panel_bg"],
        ),
    ]
