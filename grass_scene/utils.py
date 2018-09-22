import pyglet

def get_screen(idx):
    """These Three lines send the data to the monitor next to the main monitor ( harder to recognize)"""
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()
    return screens[idx]
