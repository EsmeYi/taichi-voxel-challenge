from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_directional_light((1, 1, -1), 0.5, (1, 0.8, 0.6))
scene.set_background_color(vec3(1, 0.8, 0.6))

@ti.func
def draw_rainBow(center, radius, color):
    for x in range(center.x-radius+1, center.x+radius):
        y = ti.sqrt(radius**2 - (x - center.x)**2) + center.y
        scene.set_voxel(ivec3(x, y, center.z), 1, color)

@ti.func
def draw_circle(center, radius, color):
    for x, y in ti.ndrange((center.x-radius, center.x+radius+1), (center.y-radius, center.y+radius+1)):
        r = (x-center.x)**2 + (y-center.y)**2
        if r < radius**2 :
            scene.set_voxel(ivec3(x, y, center.z), 1, color)
        if (radius-1)**2 < r <= radius**2 :
            scene.set_voxel(ivec3(x, y, center.z), 1, vec3(0, 0, 0))

@ti.func
def draw_line(loc, w, l, color):
    for x, y in ti.ndrange((loc.x, loc.x+w), (loc.y, loc.y+l)):
        scene.set_voxel(ivec3(x, y, loc.z), 1, color)

@ti.func
def dist(loc0, loc1):
    return abs(loc0.x - loc1.x) + abs(loc0.y - loc1.y) + abs(loc0.z - loc1.z)

@ti.func
def draw_box(loc0, loc1, color, corner1, corner2, corner3, corner4):
    for i, j, k, in ti.ndrange((loc0.x,loc1.x+1), (loc0.y,loc1.y+1), (loc0.z,loc1.z+1)):
        if dist(ivec3(i,j,k), ivec3(loc0.x,loc1.y,loc0.z)) >= corner1 and \
           dist(ivec3(i,j,k), ivec3(loc0.x,loc1.y,loc1.z)) >= corner1 and \
           dist(ivec3(i,j,k), ivec3(loc0.x,loc0.y,loc0.z)) >= corner2 and \
           dist(ivec3(i,j,k), ivec3(loc0.x,loc0.y,loc1.z)) >= corner2 and \
           dist(ivec3(i,j,k), ivec3(loc1.x,loc0.y,loc0.z)) >= corner3 and \
           dist(ivec3(i,j,k), ivec3(loc1.x,loc0.y,loc1.z)) >= corner3 and \
           dist(ivec3(i,j,k), ivec3(loc1.x,loc1.y,loc0.z)) >= corner4 and \
           dist(ivec3(i,j,k), ivec3(loc1.x,loc1.y,loc1.z)) >= corner4:
            scene.set_voxel(ivec3(i, j, k), 1, color)

@ti.func
def draw_buttons(x, y, z):
    draw_box(ivec3(x, y, z), ivec3(x+1, y+1, z+1), vec3(0.02, 0.02, 0.02), 0, 0, 0, 0)
    draw_box(ivec3(x-3, y-3, z), ivec3(x-2, y-2, z+1), vec3(0.02, 0.02, 0.02), 0, 0, 0, 0)
    draw_box(ivec3(x, y-6, z), ivec3(x+1, y-5, z+1), vec3(0.02, 0.02, 0.02), 0, 0, 0, 0)
    draw_box(ivec3(x+3, y-3, z), ivec3(x+4, y-2, z+1), vec3(0.02, 0.02, 0.02), 0, 0, 0, 0)  

@ti.kernel
def initialize_voxels():
    draw_box(ivec3(-36, 5, -2), ivec3(-23, 35, 2), vec3(0, 0.4, 1), 6, 6, 0, 0) # left controller
    draw_box(ivec3(23, 5, -2), ivec3(36, 35, 2), vec3(1, 0.1, 0.1), 0, 0, 6, 6) # right controller
    draw_box(ivec3(-24, 5, -2), ivec3(24, 35, 2), vec3(0, 0, 0), 0, 0, 0, 0) # mainframe
    draw_box(ivec3(-22, 7, -2), ivec3(22, 33, 2), vec3(0.1, 0.1, 0.4), 0, 0, 0, 0) # screen
    draw_buttons(-30, 19, 2) # left buttons
    draw_box(ivec3(-32, 24, 2), ivec3(-27, 29, 4), vec3(0.02, 0.02, 0.02), 3, 3, 3, 3)
    draw_box(ivec3(-27, 9, 2), ivec3(-26, 10, 3), vec3(0.04, 0.04, 0.04), 0, 0, 0, 0)
    draw_buttons(30, 28, 2) # right buttons
    draw_box(ivec3(28, 14, 2), ivec3(33, 18, 4), vec3(0.02, 0.02, 0.02), 3, 3, 3, 3)
    draw_box(ivec3(27, 9, 2), ivec3(28, 10, 3), vec3(0.04, 0.04, 0.04), 0, 0, 0, 0)
    draw_rainBow(ivec3(-10, 22, 2), 4, vec3(0.6, 0.2, 1))
    draw_rainBow(ivec3(-10, 22, 2), 5, vec3(0, 0.4, 1))
    draw_rainBow(ivec3(-10, 22, 2), 6, vec3(0.1, 0.5, 0.1))
    draw_rainBow(ivec3(-10, 22, 2), 7, vec3(1, 1, 0))
    draw_rainBow(ivec3(-10, 22, 2), 8, vec3(1, 0.5, 0))
    draw_rainBow(ivec3(-10, 22, 2), 9, vec3(1, 0.1, 0.1))
    draw_circle(ivec3(-8, 20, 2), 3, vec3(1, 0.7, 0.8)) # star Kirby
    draw_circle(ivec3(8, 18, 2), 3, vec3(1, 0.7, 0.8))
    draw_circle(ivec3(-4, 11, 2), 3, vec3(1, 0.2, 0.2))
    draw_circle(ivec3(0, 18, 2), 8, vec3(1, 0.7, 0.8))
    draw_circle(ivec3(5, 13, 2), 3, vec3(1, 0.2, 0.2))
    draw_line(ivec3(0, 16, 2), 1, 2, vec3(0, 0, 0))
    draw_line(ivec3(-1, 19, 2), 1, 3, vec3(0, 0, 0))
    draw_line(ivec3(1, 19, 2), 1, 3, vec3(0, 0, 0))
    draw_line(ivec3(-3, 18, 2), 2, 1, vec3(1, 0.2, 0.2))
    draw_line(ivec3(2, 18, 2), 2, 1, vec3(1, 0.2, 0.2))
    draw_circle(ivec3(15, 25, 2), 2, vec3(1, 1, 0))
    draw_circle(ivec3(10, 28, 2), 2, vec3(1, 1, 0))

initialize_voxels()

scene.finish()
