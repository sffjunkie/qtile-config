# Adaptation of the Net widget provided with QTile.
# Changed to only show upload/download speeds above a thresh.old

# Copyright (c) 2014 Rock Neurotiko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from math import log
from typing import Tuple

import psutil

from libqtile.log_utils import logger
from libqtile.widget import Net, base


class NetMin(Net):
    """
    Displays interface down and up speed but only above a threshold


    Widget requirements: psutil_.

    .. _psutil: https://pypi.org/project/psutil/
    """

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        (
            "format",
            "{down} ↓↑ {up}",
            "Display format of down-/upload speed of given interfaces",
        ),
        ("minimum", 10 * 1024, "The minimum number of bytes before showing values."),
    ]

    def __init__(self, **config):
        Net.__init__(self, **config)
        self.add_defaults(NetMin.defaults)

    def convert_b(self, num_bytes: float) -> Tuple[float, str]:
        """Converts the number of bytes to the correct unit"""
        factor = 1000.0

        if self.use_bits:
            letters = ["b", "kb", "Mb", "Gb", "Tb", "Pb", "Eb", "Zb", "Yb"]
            num_bytes *= 8
        else:
            letters = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

        if num_bytes > 0:
            power = int(log(num_bytes) / log(factor))
            power = max(min(power, len(letters) - 1), 0)
        else:
            power = 0

        converted_bytes = num_bytes / factor ** power
        unit = letters[power]

        return converted_bytes, unit

    def _format_down(self, down, down_letter):
        max_len_down = 7 - len(down_letter)
        down = "{val:{max_len}f}".format(val=down, max_len=max_len_down)
        return down[:max_len_down]

    def _format_up(self, up, up_letter):
        max_len_up = 7 - len(up_letter)
        up = "{val:{max_len}f}".format(val=up, max_len=max_len_up)
        return up[:max_len_up]

    def poll(self):
        ret_stat = []
        try:
            for intf in self.interface:
                new_stats = self.get_stats()
                down = new_stats[intf]["down"] - self.stats[intf]["down"]
                up = new_stats[intf]["up"] - self.stats[intf]["up"]

                down = down / self.update_interval
                up = up / self.update_interval

                if down > self.minimum:
                    down, down_letter = self.convert_b(down)
                    down = self._format_down(down, down_letter)
                    down += down_letter
                else:
                    down = "         ≅0"
                    down_letter = ""

                if up > self.minimum:
                    up, up_letter = self.convert_b(up)
                    up = self._format_up(up, up_letter)
                    up += up_letter
                else:
                    up = "         ≅0"
                    up_letter = ""

                self.stats[intf] = new_stats[intf]
                ret_stat.append(
                    self.format.format(
                        **{
                            "interface": intf,
                            "down": down,
                            "up": up,
                        }
                    )
                )

            return " ".join(ret_stat)
        except Exception as excp:
            logger.error("%s: Caught Exception:\n%s", self.__class__.__name__, excp)

