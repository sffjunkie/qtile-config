import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "config")))

import pl

from libqtile.widget.cpu import CPU

def test_Sement_Empty():
    s = pl.Segment()
    assert s.widgets() == []


def test_Segment_SingleWidget():
    c = CPU()
    s = pl.Segment(c)
    w = s.widgets()
    assert len(w) == 3
