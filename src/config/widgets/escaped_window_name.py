from libqtile import bar, hook
from libqtile.widget import base


class EscapedWindowName(base._TextBox):
    """Displays the name of the window that currently has focus"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('show_state', True, 'show window status before window name'),
        ('for_current_screen', False, 'instead of this bars screen use currently active screen')
    ]

    def __init__(self, width=bar.STRETCH, **config):
        base._TextBox.__init__(self, width=width, **config)
        self.add_defaults(EscapedWindowName.defaults)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.client_name_updated(self.update)
        hook.subscribe.focus_change(self.update)
        hook.subscribe.float_change(self.update)

        @hook.subscribe.current_screen_change
        def on_screen_changed():
            if self.for_current_screen:
                self.update()

    def update(self, *args):
        if self.for_current_screen:
            w = self.qtile.current_screen.group.current_window
        else:
            w = self.bar.screen.group.current_window
        state = ''
        if self.show_state and w is not None:
            if w.maximized:
                state = '[] '
            elif w.minimized:
                state = '_ '
            elif w.floating:
                state = 'V '
        
        wname = w.name if w and w.name else " "
        wname = wname.replace("&", "&amp;")
        self.text = "%s%s" % (state, wname)
        self.bar.draw()