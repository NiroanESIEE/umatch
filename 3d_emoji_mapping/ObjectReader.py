import numpy as np


class ObjectReader(object):

    def __init__(self, file_name_obj, file_name_mtl):
        self.vertices = []
        self.faces = []
        self.colors = []
        self.vertex_normals = []
        # self.face_vertex_normals = {}
        self.face_normals = []
        self.materials_faces = {}
        self.materials = {}
        self.vts = []


        try:
            fileOBJ = open(file_name_obj)
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
                    if key not in self.materials_faces:
                        self.materials_faces[key] = []
                elif line[0] == "f":
                    string = line.replace("//", "/-1/")
                    face = []
                    vt = []
                    # vn = []
                    # i = string.find(" ") + 1
                    faceLine = string.split(" ")

                    for f in range(1, len(faceLine)):
                        faceSplit = faceLine[f].split("/")
                        face.append(int(faceSplit[0]) - 1)
                        vt.append(int(faceSplit[1]) - 1)
                        # vn.append(int(faceSplit[2]) - 1)
                        # self.face_vertex_normals[int(faceSplit[0]) - 1] = int(faceSplit[2]) - 1

                    self.faces.append(tuple(face))
                    lenFaces += 1
                    self.vts.append(tuple(vt))

                    self.materials_faces[key].append(lenFaces - 1)
                """
                elif line[:3] == "vn ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vn = [round(float(line[index1:index2]), 3), round(float(line[index2:index3]), 3), round(float(line[index3:-1]), 3)]
                    # vn = tuple(round(vn[0], 3), round(vn[1], 3), round(vn[2], 3))
                    self.vertex_normals.append(vn)
                """

            fileOBJ.close()
            fileMTL = open(file_name_mtl)
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

                v1 = np.array(self.vertices[face[0]]) - np.array(self.vertices[face[1]])
                v2 = np.array(self.vertices[face[2]]) - np.array(self.vertices[face[1]])
                n = np.array(np.cross(v1, v2))
                if np.linalg.norm(n) != 0:
                    n = n / np.linalg.norm(n)
                self.face_normals.append(n)

                """
                # vnsList = []
                n = np.array([0.0, 0.0, 0.0])

                for vertex in face:
                    # vnsList.append(np.array(self.vertex_normals[self.face_vertex_normals[vertex]]))
                    n = n + np.array(self.vertex_normals[self.face_vertex_normals[vertex]])
                # vnsList = np.array(vnsList)
                # norm = np.mean(vnsList)
                # norm = norm / 3
                if np.linalg.norm(n) != 0:
                    n = n / np.linalg.norm(n)
                self.face_normals.append(n)
                """


        except IOError:
            print(".obj file not found.")
