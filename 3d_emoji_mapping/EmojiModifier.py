import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import ObjectReader
from PIL import Image
from math import *


class EmojiModifier(object):

    def __init__(self, filename, mouth, eyes, rotations):

        self.image = 0

        emoji = ObjectReader.ObjectReader("3d_object/" + filename + ".obj", "3d_object/" + filename + ".mtl")

        display = (500, 500)
        object_pos = np.array([0.0, 0.0, -18])
        """
        light_pos = np.array([10, 3, -15])
        angle = 0

        new_light_pos = light_pos - object_pos
        new_light_pos = np.linalg.norm(new_light_pos)
        """

        light_pos = np.array([5, -5, -16])

        new_light_pos = self.set_lighting(light_pos, object_pos, rotations)

        pygame.init()
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL, 32)
        pygame.display.set_caption("Nez ro anne")

        self.init_open_gl(display, object_pos, rotations)
        """
        glRotatef(rotations[1], 0, 1, 0)
        glRotatef(rotations[2], 0, 0, 1)
        """

        self.refresh_open_gl()

        self.draw_object(emoji, new_light_pos)

        pygame.display.flip()
        self.image = self.capture_screen(display, filename + ".png")
        pygame.quit()
        # quit()

    def set_lighting(self, light_pos, object_pos, rotation):
        new_light_pos = light_pos - object_pos

        # Rotation Y
        if rotation[1] != 0:
            angleY = rotation[1] * pi / 180
            new_light_pos[0] = light_pos[0] * cos(angleY) - light_pos[2] * sin(angleY)
            new_light_pos[2] = light_pos[0] * sin(angleY) + light_pos[2] * cos(angleY)

        # Rotation Z
        if rotation[2] != 0:
            angleZ = rotation[2] * pi / 180
            new_light_pos[0] = light_pos[0] * cos(angleZ) - light_pos[1] * sin(angleZ)
            new_light_pos[1] = light_pos[0] * sin(angleZ) + light_pos[1] * cos(angleZ)

        if np.linalg.norm(new_light_pos) != 0:
            new_light_pos = new_light_pos / np.linalg.norm(new_light_pos)
        return new_light_pos

    def init_open_gl(self, display, object_pos, rotations):
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(object_pos[0], object_pos[1], object_pos[2])

        glRotate(rotations[1], 0, 1, 0)
        glRotate(rotations[2], 0, 0, 1)

        glEnable(GL_DEPTH_TEST)

    def refresh_open_gl(self):
        glClearColor(0, 0, 0, 0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw_object(self, emoji, new_light_pos):
        glBegin(GL_TRIANGLES)
        for material, faces in emoji.materials_faces.items():
            color = np.array(emoji.materials[material]['Kd'])
            intensity = 1
            for face in faces:
                """
                normal = emoji.face_normals[face]
                output_color = (intensity * color * np.dot(normal, new_light_pos)) / 255
                output_color = color
                """

                normal = emoji.face_normals[face]
                direction = max(np.dot(normal, new_light_pos), 0)
                output_color = (intensity * color * direction)

                glColor3fv(output_color)
                for vertex in emoji.faces[face]:
                    glVertex3fv(emoji.vertices[vertex])
        glEnd()

    def capture_screen(self, display, filename):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glReadBuffer(GL_FRONT)
        data = glReadPixels(0, 0, display[0], display[1], GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", display, data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image
