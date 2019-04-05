import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import readOBJ as objReader
import numpy as np
import glfw
import cv2
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


def main2():
    light_ambient = [0.25, 0.25, 0.25]
    light_position = [-10, 5, 0, 2]
    DISPLAY_WIDTH = 900
    DISPLAY_HEIGHT = 900
    display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    # Initialize the library
    if not glfw.init():
        return
    # Set window hint NOT visible
    glfw.window_hint(glfw.VISIBLE, False)
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(DISPLAY_WIDTH, DISPLAY_HEIGHT, "hidden window", None, None)
    if not window:
        glfw.terminate()
        return
    # Make the window's context current
    glfw.make_context_current(window)
    objectPos = np.array([0.0, 0, -25])

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(objectPos[0], objectPos[1], objectPos[2])

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    readOBJ = objReader.readOBJ("umatchiiV1.obj", "umatchiiV1.mtl")
    x = 10
    y = 3
    z = -15
    lightPos = np.array([x, y, z])
    newPos = lightPos - objectPos
    newPos = np.linalg.norm(newPos)

    drawObject(readOBJ, newPos)

    image_buffer = glReadPixels(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(DISPLAY_WIDTH, DISPLAY_HEIGHT, 3)
    cv2.imwrite("image.png", image)
    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    main1()
