"""
This code runs as to set up the script to run the VR in ratcave
"""

import pyglet
import pyglet.gl as gl
import ratcave as rc
from ratcave.resources import cube_shader, default_shader
from natnetclient import NatClient
import itertools


def get_screen(idx):
    """These Three lines send the data to the monitor next to the main monitor ( harder to recognize)"""
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()
    return screens[idx]


def main():
    #gettign positions of rigib bodies in real time
    client = NatClient()
    arena_rb = client.rigid_bodies['Arena']
    rat_rb = client.rigid_bodies['Rat']

    window = pyglet.window.Window(resizable=True, fullscreen=True, screen=get_screen(1))  # Opening the basic pyglet window


    # Load Arena
    #remove_image_lines_from_mtl('assets/3D/grass_scene.mtl')
    arena_filename = '../assets/3D/arena.obj'# we are taking an arena which has been opened in blender and rendered to 3D after scanning it does not have flipped normals
    arena_reader = rc.WavefrontReader(arena_filename)  # loading the mesh of the arena through a wavefrontreader
    arena = arena_reader.get_mesh("Arena", position=arena_rb.position)  # making the wafront into mesh so we can extrude texture ont top of it.
    arena.uniforms['diffuse'] = 1., 1., 1.  # adding a white diffuse material to the arena
    arena.rotation = arena.rotation.to_quaternion() # we also need to get arena's rotation not just xyz so it can be tracked and moved if it gets bumped

    # Load the projector as a Ratcave camera, set light to its position
    projector = rc.Camera.from_pickle('../assets/3D/projector.pkl')  # settign the pickle file of the projector, which gives us the coordinates of where the projector is
    projector.position.x += .004
    projector.projection = rc.PerspectiveProjection(fov_y =40.5, aspect=1.777777778)
    light = rc.Light(position=projector.position)

    ## Make Virtual Scene ##
    # fields = []
    # for x, z in itertools.product([-.8, 0, .8], [-1.6, 0, 1.6]):
    #         field = load_textured_mesh(arena_reader, 'grass', 'grass.png')
    #         field.position.x += x
    #         field.position.z += z
    #         fields.append(field)
    #
    # ground = load_textured_mesh(arena_reader, 'Ground', 'dirt.png')
    # sky = load_textured_mesh(arena_reader, 'Sky', 'sky.png')
    # snake = load_textured_mesh(arena_reader, 'Snake', 'snake.png')

    reader = rc.WavefrontReader('arena_uvgrid.obj')
    meshes = {name: reader.get_mesh(name) for name in reader.bodies.keys()}
    root = rc.EmptyEntity()
    root.rotation = root.rotation.to_quaternion()

    for name, mesh in meshes.items():
        root.add_child(mesh)

    rat_camera = rc.Camera(projection=rc.PerspectiveProjection(aspect=1, fov_y=90, z_near=.001, z_far=10), position=rat_rb.position)  # settign the camera to be on top of the rats head

    #meshes = [ground, sky] + fields
    # meshes = [ground, sky, snake] + fields
    for mesh in meshes.values():
        mesh.uniforms['diffuse'] = 1., 1., 1.
        mesh.uniforms['flat_shading'] = False
        mesh.parent = arena

    virtual_scene = rc.Scene(meshes=meshes, light=light, camera=rat_camera, bgColor=(0, 0, 255))  # seetign aset virtual scene to be projected as the mesh of the arena
    virtual_scene.gl_states.states = virtual_scene.gl_states.states[:-1]

    ## Make Cubemapping work on arena
    cube_texture = rc.TextureCube(width=4096, height=4096)  # usign cube mapping to import the image on the texture of the arena
    framebuffer = rc.FBO(texture=cube_texture) ## creating a fr`amebuffer as the texture - in tut 4 it was the blue screen
    arena.textures.append(cube_texture)

    # Stereo
    vr_camgroup = rc.StereoCameraGroup(distance=.05)
    vr_camgroup.rotation = vr_camgroup.rotation.to_quaternion()

    # updating the posiotn of the arena in xyz and also in rotational perspective
    def update(dt):
        """main update function: put any movement or tracking steps in here, because it will be run constantly!"""
        # vr_camgroup.position, vr_camgroup.rotation.xyzw = rat_rb.position, rat_rb.quaternion  # setting the actual osiont of the rat camera to vbe of the rat position
        virtual_scene.camera.position.xyz = rat_rb.position
        arena.uniforms['playerPos'] = rat_rb.position
        arena.position, arena.rotation.xyzw = arena_rb.position, arena_rb.quaternion
        arena.position.y -= .02

        #virtual_scene.root.position.z += 0.2

    pyglet.clock.schedule(update)  # making it so that the app updates in real time


    @window.event
    def on_draw():

        ## Render virtual scene onto cube texture
        with framebuffer:
            with cube_shader:

                # for mask, camside in zip([(True, False, False, True), (False, True, True, True)], [vr_camgroup.left, vr_camgroup.right]):
                #     gl.glColorMask(*mask)
                #     virtual_scene.camera.position.xyz = camside.position_global
                virtual_scene.draw360_to_texture(cube_texture)

        ## Render real scene onto screen
        gl.glColorMask(True, True, True, True)
        window.clear()
        with cube_shader:  # usign cube shader to create the actuall 6 sided virtual cube which gets upated with position and angle of the camera/viewer
            rc.clear_color(255, 0, 0)
              # why is it here 39? e
            with projector, light:
                arena.draw()

    # actually run everything.
    pyglet.app.run()


if __name__ == '__main__':
    main()