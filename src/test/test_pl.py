import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "config")))

import pl

def test_Empty():
    p = pl.Powerline("ffffff", ["000000", "888888"])
    assert p.widgets() == []
