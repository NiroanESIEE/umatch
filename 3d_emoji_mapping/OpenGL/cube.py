import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import grafkom1Framework as graphics

"""
vertices = ()
surfaces = ()
"""

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

"""
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )
"""


colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (0,1,1),
    (1,0,1)
    )


def getVertices(obj):
    vertices = obj.vertices

def getSurfaces(obj):
    surfaces = obj.faces

def Form(objFile):
    obj = graphics.ObjLoader(objFile)
    getVertices(obj)
    getSurfaces(obj)
    
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            #glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()


def Cube():
    """glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()"""
    
    glBegin(GL_QUADS)
    s = 0
    for surface in surfaces:
        x = 0
        glColor3f(colors[s][0], colors[s][1], colors[s][2])
        for vertex in surface:
            x+=1
            #glColor3fv(colors[x])
            #glVertex3fv(vertices[vertex])
            glVertex3f(vertices[vertex][0], vertices[vertex][1], vertices[vertex][2])
        s += 1
    glEnd()


def main():
    
    objFile = "Love Emoji 3D.obj"
    objFile = "teddy.obj"
    
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

    glClearDepth(1.0)

    #glDisable(GL_POLYGON_OFFSET_FILL)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 0, 1, 0)
        glClearColor(0, 0, 0, 0)

        glClearDepth(1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        #Form(objFile)
        pygame.display.flip()
        pygame.time.wait(10)
    

main()