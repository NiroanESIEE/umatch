from OpenGL.GL import *
import numpy as np


class readOBJ(object):

    def __init__(self, fileNameOBJ, fileNameMTL):
        self.vertices = []
        self.faces = []
        self.colors = []
        self.vts = []
        self.vns = []
        self.fns = []
        self.materialsFace = {}
        self.materials = {}

        try:
            fileOBJ = open(fileNameOBJ)
            key = ""
            lenFaces = 0
            for line in fileOBJ:
                if line[:2] == "v ":

                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                    self.vertices.append(vertex)
                elif line[:6] == "usemtl":
                    i = line.find(" ") + 1
                    key = line[i:-1]
                    if key not in self.materialsFace:
                        self.materialsFace[key] = []
                elif line[0] == "f":
                    string = line.replace("//", "/-1/")
                    face = []
                    vt = []
                    vn = []
                    i = string.find(" ") + 1
                    faceLine = string.split(" ")

                    for f in range(1, len(faceLine)):
                        faceSplit = faceLine[f].split("/")
                        face.append(int(faceSplit[0]) - 1)
                        vt.append(int(faceSplit[1]) - 1)
                        vn.append(int(faceSplit[2]) - 1)

                    self.faces.append(tuple(face))
                    lenFaces += 1
                    self.vts.append(tuple(vt))
                    self.vns.append(tuple(vn))
                    self.materialsFace[key].append(lenFaces - 1)

            fileOBJ.close()
            fileMTL = open(fileNameMTL)
            materialName = ""
            caract = {}
            for line in fileMTL:
                if line[:6] == "newmtl":
                    index1 = line.find(" ") + 1
                    materialName = line[index1:-1]
                    self.materials[materialName] = {}
                    caract = {}
                else:
                    if line[0] == "#":
                        continue
                    string = line.split(" ")
                    caract[string[0]] = [float(i) for i in string[1:]]
                    self.materials[materialName] = caract
            fileMTL.close()

            # Face normals
            for face in self.faces:
                vnsList = []

                for vertex in face:
                    vnsList.append(self.vns[vertex])
                vnsList = np.array(vnsList)

                self.fns.append(np.linalg.norm(np.mean(vnsList)))


        except IOError:
            print(".obj file not found.")


if __name__ == '__main__':

    readOBJ = readOBJ("MAJORCUBE.obj", "MAJORCUBE.mtl")

    for vertice in readOBJ.vertices:
        print(vertice)

    for face in readOBJ.faces:
        print(face)

    print(list(readOBJ.materials['initialShadingGroup']))

    print(list(readOBJ.materialsFace['initialShadingGroup']))

    for materialFace in readOBJ.materialsFace:
        print(materialFace)
