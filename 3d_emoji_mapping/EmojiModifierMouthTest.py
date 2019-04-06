import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import ObjectReader
from PIL import Image


def get_mouth_vertices(emoji):
    coords = [(-0.721, 1.096, 2.792), (0.003, 1.058, 3.046), (0.072, 1.058, 3.046), (0.797, 1.096, 2.792), (0.551, 0.920, 2.783), (0.045, 0.892, 2.932), (0.031, 0.892, 2.932), (-0.475, 0.920, 2.783)]
    indices = {}
    for ci in range(len(coords)):
        c = coords[ci]
        for i in range(len(emoji.vertices)):
            ver = emoji.vertices[i]
            if (round(ver[0], 3) == c[0]) and (round(ver[1], 3) == c[1]) and (round(ver[2], 3) == c[2]):
                if ci not in indices:
                    indices[ci] = [i]
                else:
                    indices[ci].append(i)
    return indices


def get_mouth_points(emoji, mouth):
    left = []
    left.extend(mouth[0])
    left.extend(mouth[7])
    right = []
    right.extend(mouth[3])
    right.extend(mouth[4])
    top = []
    top.extend(mouth[1])
    top.extend(mouth[2])
    bottom = []
    bottom.extend(mouth[5])
    bottom.extend(mouth[6])
    return left, right, top, bottom

def open_vert_mouth(emoji, mouth):
    left, right, top, bottom = get_mouth_points(emoji, mouth)
    for p in top:
        emoji.vertices[p] = (emoji.vertices[p][0], emoji.vertices[p][1] + 0.1, emoji.vertices[p][2])
    for p in bottom:
        emoji.vertices[p] = (emoji.vertices[p][0], emoji.vertices[p][1] - 0.1, emoji.vertices[p][2])

def close_vert_mouth(emoji, mouth):
    left, right, top, bottom = get_mouth_points(emoji, mouth)
    for p in top:
        emoji.vertices[p] = (emoji.vertices[p][0], emoji.vertices[p][1] - 0.1, emoji.vertices[p][2])
    for p in bottom:
        emoji.vertices[p] = (emoji.vertices[p][0], emoji.vertices[p][1] + 0.1, emoji.vertices[p][2])

def open_horiz_mouth(emoji, mouth):
    left, right, top, bottom = get_mouth_points(emoji, mouth)
    for p in left:
        emoji.vertices[p] = (emoji.vertices[p][0] - 0.1, emoji.vertices[p][1], emoji.vertices[p][2])
    for p in right:
        emoji.vertices[p] = (emoji.vertices[p][0] + 0.1, emoji.vertices[p][1], emoji.vertices[p][2])

def close_horiz_mouth(emoji, mouth):
    left, right, top, bottom = get_mouth_points(emoji, mouth)
    for p in left:
        emoji.vertices[p] = (emoji.vertices[p][0] + 0.1, emoji.vertices[p][1], emoji.vertices[p][2])
    for p in right:
        emoji.vertices[p] = (emoji.vertices[p][0] - 0.1, emoji.vertices[p][1], emoji.vertices[p][2])

def init_open_gl(display, object_pos):
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(object_pos[0], object_pos[1], object_pos[2])

    glEnable(GL_DEPTH_TEST)


def refresh_open_gl():
    glClearColor(0., 0, 0, 0)
    glClearDepth(1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def draw_object(emoji, new_light_pos):
    glBegin(GL_TRIANGLES)
    for material, faces in emoji.materials_faces.items():
        color = np.array(emoji.materials[material]['Kd'])
        intensity = 0.1
        for face in faces:
            normal = emoji.face_normals[face]
            output_color = (intensity * color * np.dot(normal, new_light_pos)) / 255
            glColor3fv(output_color)
            for vertex in emoji.faces[face]:
                glVertex3fv(emoji.vertices[vertex])
    glEnd()


def capture_screen(display, filename):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadBuffer(GL_FRONT)
    data = glReadPixels(0, 0, display[0], display[1], GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", display, data)
    #image = image.transpose(Image.ROTATE_180)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(filename, 'png')


def main(filename):
    emoji = ObjectReader.ObjectReader("3d_object/" + filename + ".obj", "3d_object/" + filename + ".mtl")
    mouth = get_mouth_vertices(emoji)
    print(mouth)
    #mouth = [405, 604, 203, 404, 601, 204, 104, 312, 105, 311]
    
    display = (500, 500)
    object_pos = np.array([0.0, -2.5, -9])
    light_pos = np.array([10, 3, -15])
    angle = 0

    new_light_pos = light_pos - object_pos
    new_light_pos = np.linalg.norm(new_light_pos)

    pygame.init()
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL, 32)
    pygame.display.set_caption("Nez ro anne")

    init_open_gl(display, object_pos)
    
    while True:
        angle += 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                open_vert_mouth(emoji, mouth)
            elif event.key == pygame.K_DOWN:
                close_vert_mouth(emoji, mouth)
            elif event.key == pygame.K_RIGHT:
                open_horiz_mouth(emoji, mouth)
            elif event.key == pygame.K_LEFT:
                close_horiz_mouth(emoji, mouth)
        
        #glRotate(1, 0, 1, 0)
        refresh_open_gl()
        
        draw_object(emoji, new_light_pos)
        
        pygame.display.flip()
        pygame.time.wait(10)
        #capture_screen(display, filename + ".png")

if __name__ == '__main__':
    main("umatchii")
