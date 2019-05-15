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
        self.min_mouth_x = 0.17
        self.max_mouth_x = 0.46
        self.max_move_mouth_x = 0.18
        self.min_mouth_y = 0.12
        self.max_mouth_y = 0.40

        emoji = ObjectReader.ObjectReader("3d_object/" + filename + ".obj", "3d_object/" + filename + ".mtl")

        display = (500, 500)
        object_pos = np.array([0.0, 0.0, -18])

        light_pos = np.array([5, -5, -15])
        #light_pos_2 = np.array([0, 0, -15])
        #light_pos_3 = np.array([0, 5, -15])
        light_pos_4 = np.array([-5, 5, -15])
        
        lights = []
        lights.append(light_pos)
        #lights.append(light_pos_2)
        #lights.append(light_pos_3)
        lights.append(light_pos_4)

        new_light_pos = self.set_lighting(lights, object_pos, rotations)

        pygame.init()
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL, 32)
        pygame.display.set_caption("Nez ro anne")

        self.init_open_gl(display, object_pos, rotations)

        self.refresh_open_gl()
        
        if filename.find("Beak_Mouth") >= 0:
            self.beak_open_mouth_x(filename, emoji, mouth[0])
            self.beak_open_mouth_y(filename, emoji, mouth[1])
        elif filename.find("Normal_Mouth") >= 0:
            self.mouth_open_mouth_y(filename, emoji, mouth)
        
        
        #self.open_mouth(emoji, 1)
        #self.set_angry(emoji)
        #self.set_sad(emoji)
        
        self.draw_object(emoji, new_light_pos)

        pygame.display.flip()
        self.image = self.capture_screen(display, filename + ".png")
        pygame.quit()
        # quit()

    def set_lighting(self, lights, object_pos, rotation):
        l = []
        
        for light_pos in lights:
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
            
            l.append(new_light_pos)
        return l

    def init_open_gl(self, display, object_pos, rotations):
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(object_pos[0], object_pos[1], object_pos[2])

        glRotate(rotations[0], 1, 0, 0)
        glRotate(rotations[1], 0, 1, 0)
        glRotate(rotations[2], 0, 0, 1)

        glEnable(GL_DEPTH_TEST)

    def refresh_open_gl(self):
        glClearColor(0, 0, 0, 0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw_object(self, emoji, lights):
        glBegin(GL_TRIANGLES)
        for material, faces in emoji.materials_faces.items():
            color = np.array(emoji.materials[material]['Kd'])
            intensity = 1
            for face in faces:
                
                normal = emoji.face_normals[face]
                output_color = (0, 0, 0)
                
                for light in lights:
                    direction = max(np.dot(normal, light), 0)
                    output_color = (output_color[0] + (intensity * color * direction)[0], output_color[1] + (intensity * color * direction)[1], output_color[2] + (intensity * color * direction)[2])
                
                glColor3fv(output_color)
                
                #glColor3fv(color)
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
    
    """
    def open_mouth(self, emoji, open_y):
        for vertex in emoji.mouth_up:
            emoji.vertices[vertex] = (emoji.vertices[vertex][0], emoji.vertices[vertex][1] + open_y, emoji.vertices[vertex][2])
        for vertex in emoji.mouth_down:
            emoji.vertices[vertex] = (emoji.vertices[vertex][0], emoji.vertices[vertex][1] - open_y, emoji.vertices[vertex][2])
    """
    
    def get_affine_image(self, a, b, x):
        return (a * x + b)
    
    def beak_open_mouth_x(self, filename, emoji, mouth_x):
        #move = 0.18
        move = abs(mouth_x - self.min_mouth_x) * (self.max_move_mouth_x) / abs(self.max_mouth_x - self.min_mouth_x)
        for vertex in emoji.mouth_left:
            v = emoji.vertices[vertex]
            emoji.vertices[vertex] = (v[0] - move, v[1], v[2])
        for vertex in emoji.mouth_right:
            v = emoji.vertices[vertex]
            emoji.vertices[vertex] = (v[0] + move, v[1], v[2])
    
    def beak_open_mouth_y(self, filename, emoji, mouth_y):
        max_down = abs(mouth_y - self.min_mouth_y) * abs(emoji.y_max_mouth_down - emoji.y_min_mouth_down) / abs(self.max_mouth_y - self.min_mouth_y)
        for vertex in emoji.mouth_down:
            v = emoji.vertices[vertex]
            down = abs(v[2] - emoji.z_min_mouth_down) / abs(emoji.z_max_mouth_down - emoji.z_min_mouth_down)
            emoji.vertices[vertex] = (v[0], v[1] - max_down * down, v[2])
    
    def mouth_open_mouth_y(self, filename, emoji, mouth):
        x_min = x_min_mouth
        x_inc = (x_max_mouth - x_min_mouth) / 5
        
    
    def set_angry(self, emoji):
        self.set_angry_eye_left(emoji)
        self.set_angry_eye_right(emoji)
    
    def set_angry_eye_left(self, emoji):
        p1 = (emoji.x_min_left, emoji.y_max_left)
        p2 = (emoji.x_max_left, emoji.y_min_left)
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - a * p1[0]
        for i in range(len(emoji.left_eye)):
            v = emoji.vertices[emoji.left_eye[i]]
            emoji.vertices[emoji.left_eye[i]] = (v[0], self.get_affine_image(a, b, v[0]), v[2])
    
    def set_angry_eye_right(self, emoji):
        p1 = (emoji.x_min_right, emoji.y_min_right)
        p2 = (emoji.x_max_right, emoji.y_max_right)
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - a * p1[0]
        for i in range(len(emoji.right_eye)):
            v = emoji.vertices[emoji.right_eye[i]]
            emoji.vertices[emoji.right_eye[i]] = (v[0], self.get_affine_image(a, b, v[0]), v[2])
    
    def set_sad(self, emoji):
        self.set_sad_eye_left(emoji)
        self.set_sad_eye_right(emoji)
    
    
    def set_sad_eye_left(self, emoji):
        p1 = (emoji.x_min_left, emoji.y_min_left * 1.2)
        p2 = (emoji.x_max_left, emoji.y_max_left * 0.9)
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - a * p1[0]
        for i in range(len(emoji.left_eye)):
            v = emoji.vertices[emoji.left_eye[i]]
            emoji.vertices[emoji.left_eye[i]] = (v[0], self.get_affine_image(a, b, v[0]), v[2])
    
    def set_sad_eye_right(self, emoji):
        p1 = (emoji.x_min_right, emoji.y_max_right * 0.9)
        p2 = (emoji.x_max_right, emoji.y_min_right * 1.2)
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - a * p1[0]
        for i in range(len(emoji.right_eye)):
            v = emoji.vertices[emoji.right_eye[i]]
            emoji.vertices[emoji.right_eye[i]] = (v[0], self.get_affine_image(a, b, v[0]), v[2])
    
    
        
        