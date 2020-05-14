# Copyright (c) 2008, 2010 Aldo Cortesi
# Copyright (c) 2011 Mounier Florian
# Copyright (c) 2012, 2015 Tycho Andersen
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2013 Craig Barnes
# Copyright (c) 2014 Sean Vig
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

# Code adpated from QTile Clock widget

import sys
import time
from datetime import datetime, timedelta, timezone

from libqtile.log_utils import logger
from libqtile.widget import base

try:
    import pytz
except ImportError:
    pass


class UnicodeClock(base.InLoopPollText):
    """Returns a clock unicode character to match the current hour"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('update_interval', 60., 'Update interval for the clock character'),
        ('timezone', None, 'The timezone to use for this clock, either as'
         ' string if pytz is installed (e.g. "US/Central" or anything in'
         ' /usr/share/zoneinfo), or as tzinfo (e.g. datetime.timezone.utc).'
         ' None means the system local timezone and is the default.')
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(UnicodeClock.defaults)
        if isinstance(self.timezone, str):
            if "pytz" in sys.modules:
                self.timezone = pytz.timezone(self.timezone)
            else:
                logger.warning('UnicodeClock widget can not infer its timezone from a'
                               ' string without the pytz library. Install pytz'
                               ' or give it a datetime.tzinfo instance.')
        if self.timezone is None:
            logger.info('Defaulting to the system local timezone.')

    def tick(self):
        self.update(self.poll())
        return self.update_interval - time.time() % self.update_interval

    def poll(self):
        if self.timezone:
            now = datetime.now(timezone.utc).astimezone(self.timezone)
        else:
            now = datetime.now(timezone.utc).astimezone()
        
        if now.minute > 50:
            offset = (now.hour + 1) % 13
        else:
            if now.hour == 0:
                offset = 12
            else:
                offset = now.hour % 13

        if now.minute > 20 and now.minute <= 50:
            offset += 12

        return chr(128336 + offset)
