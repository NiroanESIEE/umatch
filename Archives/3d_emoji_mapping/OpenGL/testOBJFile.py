import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import readOBJ as objReader
import numpy as np
from PIL import Image
import math


def drawObject(readOBJ, newPos):
    glBegin(GL_TRIANGLES)

    for material, faces in readOBJ.materialsFace.items():
        color = np.array(readOBJ.materials[material]['Kd'])
        # intensity = readOBJ.materials[material]['illum'][0]
        intensity = 0.1
        # color.append(readOBJ.materials[material]['Ni'][0])
        # glColor4fv(color)

        for face in faces:
            normal = readOBJ.fns[face]
            outputColor = (intensity * color * np.dot(normal, newPos)) / 255
            glColor3fv(outputColor)
            for vertex in readOBJ.faces[face]:
                glVertex3fv(readOBJ.vertices[vertex])

    glEnd()


def CaptureScreen(display, filename):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadBuffer(GL_FRONT)
    data = glReadPixels(0, 0, display[0], display[1], GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", display, data)
    image = image.transpose(Image.ROTATE_180)
    image.save(filename, 'png')


def main1():
    readOBJ = objReader.readOBJ("umatchiiV1.obj", "umatchiiV1.mtl")

    # INIT DE LA FENETRE
    pygame.init()
    display = (500, 500)
    window = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL, 32)
    pygame.display.set_caption("Nez ro anne")

    objectPos = np.array([0.0, -2.5, -9])

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(objectPos[0], objectPos[1], objectPos[2])

    glEnable(GL_DEPTH_TEST)

    angle = 0

    x = 10
    y = 3
    z = -15
    # lightPos = np.array([x, y, z])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotatef(1, 0, 1, 0)
        angle += 1

        # lightX = x * math.cos(math.radians(-angle)) - z * math.sin(math.radians(-angle))
        # lightZ = x * math.sin(math.radians(-angle)) + z * math.cos(math.radians(-angle))

        lightPos = np.array([x, y, z])

        newPos = lightPos - objectPos
        newPos = np.linalg.norm(newPos)

        glClearColor(0, 0, 0, 0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        drawObject(readOBJ, newPos)

        if angle == 2:
            CaptureScreen(display, "cocoMajor.png")

        pygame.display.flip()
        pygame.time.wait(10)



if __name__ == '__main__':
    main1()
