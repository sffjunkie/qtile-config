"""
pl_rhs = Powerline(
    s["theme"]["color"]["powerline_fg"],
    s["theme"]["color"]["powerline_background"],
)
systray = Segment(
    [
    widget.Systray(
        foreground=theme_colors["powerline_fg"],
        background=theme_colors["powerline_background"][3],
    ),
    widget.Sep(linewidth=0, padding=6, background=theme_colors["powerline_background"][3],),
    widget.TextBox(
        text=chr(987798),
        font=icon_font,
        foreground=theme_colors["powerline_fg"],
        background=theme_colors["powerline_background"][3],
    ),
    ]
)
pl_rhs.add(systray, side=Side.RIGHT)
widgets = pl_rhs.widgets()
bar.extend(widgets)
"""

from enum import Enum
from itertools import cycle
from typing import List, Union

from libqtile import widget, bar

import settings

s = settings.load_settings()


class Side(Enum):
    RIGHT = 1
    LEFT = 2


WIDGET_BASE = widget.base._Widget
WIDGET = Union[List[WIDGET_BASE], WIDGET_BASE]


def _segment_separator() -> widget.TextBox:
    return widget.base._TextBox(
        text=separator,
        font=font,
        fontsize=22 - 4,
        padding=0,
        margin=0,
        foreground=background,
        background=foreground,
    )


class Segment:
    def __init__(self, widgets: WIDGET = []):
        self._fg = ""
        self._background = ""
        if isinstance(widgets, list):
            self.widget_list = widgets
        else:
            self.widget_list = [widgets]
        self.sep = widget.Sep(linewidth=0, padding=6,)

    def add(self, widgets: WIDGET) -> None:
        if isinstance(widgets, list):
            self.widget_list.extend(widgets)
        else:
            self.widget_list.append(widgets)

    def add_separator(self):
        self.widget_list.append(self.sep)

    @property
    def foreground(self) -> str:
        return self._fg

    @foreground.setter
    def foreground(self, value: str) -> None:
        self._fg = value
        self.sep.foreround = value

    @property
    def background(self) -> str:
        return self._background

    @background.setter
    def background(self, value: str) -> None:
        self._background = value
        self.sep.background = value

    def widgets(self) -> List[WIDGET_BASE]:
        if not self.widget_list:
            return []

        l = []
        l.append(self.sep)
        l.extend(self.widget_list)
        l.append(self.sep)
        return l


class SegmentSeparator(widget.TextBox):
    def __init__(
        self,
        text=" ",
        width=bar.CALCULATED,
        foreground="ffffff",
        background="444444",
        **config
    ):
        config["foreground"] = foreground
        config["background"] = background
        config["padding"] = 0
        config["margin"] = 2

        super().__init__(text, width, **config)

    def _configure(self, qtile, bar):
        self.fontsize = bar.height + 6


class Powerline:
    def __init__(
        self,
        foreground: str,
        segment_colors: List[str],
        separators: List[str] = ["\uE0B2", "\uE0B0"],
    ):
        self.foreground = foreground
        self.segment_colors = segment_colors
        self.separators = separators
        self._segment_color_iter = cycle(self.segment_colors)

        self._widgets_left = []
        self._widgets_right = []
        self._next_background = None

    def add(self, segment, side: Side = Side.RIGHT) -> None:
        segment.foreground = self.foreground
        if not self._next_background:
            self._background = self._segment_color_iter.__next__()
            self._next_background = self._segment_color_iter.__next__()
        else:
            self._background = self._next_background
            self._next_background = self._segment_color_iter.__next__()

        segment.background = self._background

        if side == Side.LEFT:
            self._widgets_left.extend(segment.widgets())
            text = self.separators[0]
        else:
            self._widgets_right.extend(segment.widgets())
            text = self.separators[1]

        self._widgets_right.append(
            SegmentSeparator(
                text=text,
                foreground=self._background,
                background=self._next_background,
            )
        )

    def widgets(self) -> List[WIDGET_BASE]:
        if not self._widgets_left and not self._widgets_right:
            return []
            
        widget_list = []

        stretchy = False
        for w in self._widgets_left:
            if w.length_type == bar.STRETCH:
                stretchy = True
            widget_list.append(w)

        # If none of the left hand widgets stretch, make the last one stretch
        if self._widgets_left and not stretchy:
            widget_list[-1].length_type = bar.STRETCH
            widget_list[-1].length = 0

        for w in self._widgets_right[::-1]:
            widget_list.append(w)

        if self._widgets_left and not isinstance(self._widgets_left[0], widget.Sep):
            widgets_list.insert(0, widget.Sep(linewidth=0, padding=6, background=self.widgets[0].background,))

        if self._widgets_right and not isinstance(widget_list[-1], widget.Sep):
            widget_list.append(widget.Sep(linewidth=0, padding=6, background=self.widgets[-1].background,))

        return widget_list
