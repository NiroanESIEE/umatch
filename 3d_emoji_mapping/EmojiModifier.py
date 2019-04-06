import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import ObjectReader
from PIL import Image


class EmojiModifier(object):
    
    def __init__(self, filename, mouth, eyes, rotation):
        
        self.image = 0
        
        emoji = ObjectReader.ObjectReader("3d_object/" + filename + ".obj", "3d_object/" + filename + ".mtl")

        display = (500, 500)
        object_pos = np.array([0.0, -2.5, -9])
        light_pos = np.array([10, 3, -15])
        angle = 0
    
        new_light_pos = light_pos - object_pos
        new_light_pos = np.linalg.norm(new_light_pos)
    
        pygame.init()
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL, 32)
        pygame.display.set_caption("Nez ro anne")
    
        self.init_open_gl(display, object_pos)
        
        self.refresh_open_gl()
    
        self.draw_object(emoji, new_light_pos)
    
        pygame.display.flip()
        self.image = self.capture_screen(display, filename + ".png")
        pygame.quit()
        #quit()
            


    def init_open_gl(self, display, object_pos):
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(object_pos[0], object_pos[1], object_pos[2])
    
        glEnable(GL_DEPTH_TEST)
    
    
    def refresh_open_gl(self):
        glClearColor(0, 0, 0, 0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    
    def draw_object(self, emoji, new_light_pos):
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
    
    
    def capture_screen(self, display, filename):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glReadBuffer(GL_FRONT)
        data = glReadPixels(0, 0, display[0], display[1], GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", display, data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image
 
