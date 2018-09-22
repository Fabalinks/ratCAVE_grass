import pyglet
import ratcave as rc


def get_screen(idx):
    """These Three lines send the data to the monitor next to the main monitor ( harder to recognize)"""
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()
    return screens[idx]


def load_textured_mesh(reader, name, image_filename=None, image_dirname='assets/img/'):
    mesh = reader.get_mesh(name)
    if image_filename:
        mesh.textures.append(rc.Texture.from_image(image_dirname + image_filename))
    return mesh


def remove_image_lines_from_mtl(mtl_filename):
    lines = []
    with open(mtl_filename) as f:
        for line in f:
            if 'map_Kd' in line:
                continue
            if 'map_Bump' in line:
                continue
            lines.append(line)

    with open(mtl_filename, 'w') as f:
        f.writelines(lines)