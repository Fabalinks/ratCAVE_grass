import pyglet
import ratcave as rc


def get_screen(idx):
    """These Three lines send the data to the monitor next to the main monitor ( harder to recognize)"""
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()
    return screens[idx]


def load_textured_mesh(reader, name, image_filename, image_dirname='assets/img/'):
    mesh = reader.get_mesh(name)
    mesh.textures.append(rc.Texture.from_image(image_dirname + image_filename))
    return mesh