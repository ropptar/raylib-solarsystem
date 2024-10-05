# UNFINISHED

import math

import pyray as pr
import raylib

EARTH_RADIUS = 6378
EARTH_INC = 365.25
INC_MUL = pr.ffi.new("float *", 10)
A_E = 3

pr.init_window(1920, 1080, "Hello Pyray")
pr.set_window_state(2)
pr.set_target_fps(60)

class Planet:
    d = 5.9

    def __init__(self, name='Earth', r=EARTH_RADIUS, inc=EARTH_INC, ae=1, col=pr.BLUE, iscenter=False, r_div=1,
                 ae_div=1,
                 center=pr.Vector3(0, 0, 0)):
        self.name = name
        self.angle = 0
        self.pos = pr.Vector3(0, 0, 0)
        self.r = r / EARTH_RADIUS / r_div
        try:
            self.inc = EARTH_INC / inc / 1000
        except ZeroDivisionError:
            self.inc = 0
        self.ae = A_E * ae / (4 if iscenter else 1) / ae_div
        self.col = col
        self.center = center

    def update(self):
        pr.draw_sphere(self.pos, self.r, self.col)
        self.pos = pr.Vector3(self.center.x + math.cos(self.angle) * Planet.d * self.ae,
                              self.center.y + 0,
                              self.center.z + math.sin(self.angle) * Planet.d * self.ae)
        self.angle = (self.angle + self.inc * pr.ffi.unpack(INC_MUL,1)[0]) % 360


camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [1.0, 5.0, 2.0], 45.0, 0)
earth_inc = 1
center_ind =0

sun = Planet('Sun', Planet.d * EARTH_RADIUS, 0, 0, pr.YELLOW, iscenter=True)
mercury = Planet('Mercury', 2439.7, 87.969, 0.4, pr.Color(113, 113, 113, 255))
venus = Planet('Venus', 6052, 224.701, 0.7, pr.Color(174, 107, 31, 255))
earth = Planet()
moon = Planet('Moon', EARTH_RADIUS / 4, 27.321661, 0.1, pr.LIGHTGRAY)
mars = Planet('Mars', 3396.2, 686.98, 1.5, pr.Color(184, 88, 39, 255))
jupiter = Planet('Jupiter', 69911, 4332.589, 5.2, pr.Color(165, 144, 123, 255), r_div=5, ae_div=2.2)
saturn = Planet('Saturn', 58232, 10759.22, 9.5, pr.Color(191, 182, 160, 255), r_div=5, ae_div=2.7)
uranus = Planet('Uranus', 25362, 30685.4, 19.6, pr.Color(201, 239, 241, 255), r_div=3, ae_div=4)
neptune = Planet('Neptune', 24622, 60190.03, 30, pr.Color(115, 152, 215, 255), r_div=3, ae_div=7)
# pluto != Planet   # get cancelled idiot
system = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, moon]

while not pr.window_should_close():
    pr.gui_enable()
    pr.update_camera(camera, pr.CameraMode.CAMERA_ORBITAL)
    camera.center = system[center_ind].pos
    moon.center = earth.pos


    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    pr.begin_mode_3d(camera)
    pr.draw_grid(100, 2)
    for planet in system:
        planet.update()
    # pr.draw_ring(pr.vector2_rotate([saturn.pos[0], saturn.pos[2]],45), 1, 100, 0, 360, 6, pr.BLUE)
    pr.end_mode_3d()
    pr.gui_slider(pr.Rectangle(10, 10, 300, 50), '', 'Time multiplier', INC_MUL, 1, 100)

    # USE LATER
    # vec = pr.get_world_to_screen(earth.pos, camera)
    # pr.set_mouse_position(int(vec.x), int(vec.y))
    pr.end_drawing()

pr.close_window()
