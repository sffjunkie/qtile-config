import pl
p = pl.Powerline("ffff", ["000000", "888888"])
print(p.widgets())

from libqtile.widget.cpu import CPU
c = CPU()
s = pl.Segment(c)
p.add(s)
print(p.widgets())
