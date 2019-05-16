import numpy as np


class ObjectReader(object):

    def __init__(self, file_name_obj, file_name_mtl):
        self.original_vertices = []
        self.vertices = []
        self.faces = []
        self.colors = []
        self.vertex_normals = []
        # self.face_vertex_normals = {}
        self.face_normals = []
        self.materials_faces = {}
        self.materials = {}
        self.vts = []
        
        self.left_eye = []
        self.right_eye = []
        
        self.mouth_up = []
        self.mouth_down = []
        
        self.mouth_left = []
        self.mouth_right = []
        
        
        self.y_min_left = 10000
        self.y_max_left = -10000
        self.x_min_left = 10000
        self.x_max_left = -10000
        
        self.y_min_right = 10000
        self.y_max_right = -10000
        self.x_min_right = 10000
        self.x_max_right = -10000
        
        self.z_min_mouth_up = 10000
        self.z_max_mouth_up = -10000
        self.y_min_mouth_up = 10000
        self.y_max_mouth_up = -10000
        
        self.z_min_mouth_down = 10000
        self.z_max_mouth_down = -10000
        self.y_min_mouth_down = 10000
        self.y_max_mouth_down = -10000
        
        self.x_moy_mouth = 0
        self.x_min_mouth = 10000
        self.x_max_mouth = -10000
        
        self.y_moy_mouth = 0
        self.y_min_mouth = 10000
        self.y_max_mouth = -10000
        
        self.eps = 0.05

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
                    self.original_vertices.append(vertex)
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
                elif line[:3] == "vn ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vn = [round(float(line[index1:index2]), 3), round(float(line[index2:index3]), 3), round(float(line[index3:-1]), 3)]
                    self.vertex_normals.append(vn)

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
            
            self.get_mouth_vertices()
            #self.get_eyes()

        except IOError:
            print(".obj file not found.")
    
    
    def get_mouth_vertices(self):
        if "BeakUpSG" in self.materials_faces:
            for face in self.materials_faces["BeakUpSG"]:
                for vertex in self.faces[face]:
                    #self.mouth_up.append(self.vertices[vertex])
                    self.mouth_up.append(vertex)
                    
                    v = self.vertices[vertex]
                    if self.z_min_mouth_up > v[2]:
                        self.z_min_mouth_up = v[2]
                    if self.z_max_mouth_up < v[2]:
                        self.z_max_mouth_up = v[2]
                        
                    if self.y_min_mouth_up > v[1]:
                        self.y_min_mouth_up = v[1]
                    if self.y_max_mouth_up < v[1]:
                        self.y_max_mouth_up = v[1]
                    
                    if self.x_min_mouth > v[0]:
                        self.x_min_mouth = v[0]
                    if self.x_max_mouth < v[0]:
                        self.x_max_mouth = v[0]
            
            #self.mouth_up = sorted(self.mouth_up, key=lambda x: x[0])
            self.mouth_up = set(self.mouth_up)
            
            self.x_moy_mouth = (self.x_min_mouth + self.x_max_mouth) / 2
            
            for face in self.materials_faces["BeakUpSG"]:
                for vertex in self.faces[face]:
                    v = self.vertices[vertex]
                    if (v[0] < (self.x_moy_mouth - self.eps)):
                        self.mouth_left.append(vertex)
                    elif (v[0] > (self.x_moy_mouth + self.eps)):
                        self.mouth_right.append(vertex)
            
            
            for face in self.materials_faces["BeakDownSG"]:
                for vertex in self.faces[face]:
                    #self.mouth_down.append(self.vertices[vertex])
                    self.mouth_down.append(vertex)
                    
                    v = self.vertices[vertex]
                    if self.z_min_mouth_down > v[2]:
                        self.z_min_mouth_down = v[2]
                    if self.z_max_mouth_down < v[2]:
                        self.z_max_mouth_down = v[2]
                        
                    if self.y_min_mouth_down > v[1]:
                        self.y_min_mouth_down = v[1]
                    if self.y_max_mouth_down < v[1]:
                        self.y_max_mouth_down = v[1]
                    
                    if (v[0] < (self.x_moy_mouth - self.eps)):
                        self.mouth_left.append(vertex)
                    elif (v[0] > (self.x_moy_mouth + self.eps)):
                        self.mouth_right.append(vertex)
            
            #self.mouth_down = sorted(self.mouth_down, key=lambda x: x[0])
            self.mouth_down = set(self.mouth_down)
            
            self.mouth_left = set(self.mouth_left)
            self.mouth_right = set(self.mouth_right)
            
        else:
            for face in self.materials_faces["Mouth"]:
                for vertex in self.faces[face]:
                    
                    v = self.vertices[vertex]
                    
                    if self.x_min_mouth > v[0]:
                        self.x_min_mouth = v[0]
                    if self.x_max_mouth < v[0]:
                        self.x_max_mouth = v[0]
                        
                    if self.y_min_mouth > v[1]:
                        self.y_min_mouth = v[1]
                    if self.y_max_mouth < v[1]:
                        self.y_max_mouth = v[1]
            
            self.x_moy_mouth = (self.x_min_mouth + self.x_max_mouth) / 2
            self.y_moy_mouth = (self.y_min_mouth + self.y_max_mouth) / 2
            
            for face in self.materials_faces["Mouth"]:
                for vertex in self.faces[face]:
                    
                    v = self.vertices[vertex]
                    
                    if (v[0] <= self.x_moy_mouth):
                        self.mouth_left.append(vertex)
                    else:
                        self.mouth_right.append(vertex)
                    
                    if (v[1] <= self.y_moy_mouth):
                        self.mouth_down.append(vertex)
                    else:
                        self.mouth_up.append(vertex)
            
            self.mouth_down = set(self.mouth_down)
            self.mouth_up = set(self.mouth_up)
            self.mouth_left = set(self.mouth_left)
            self.mouth_right = set(self.mouth_right)
                    
        
    def get_eyes(self):
        
        for face in self.materials_faces["LeftEyeColorSG"]:
            for vertex in self.faces[face]:
                
                v = self.vertices[vertex]
                if self.y_min_left > v[1]:
                    self.y_min_left = v[1]
                if self.y_max_left < v[1]:
                    self.y_max_left = v[1]
                
                if self.x_min_left > v[0]:
                    self.x_min_left = v[0]
                if self.x_max_left < v[0]:
                    self.x_max_left = v[0]
                    
                #self.left_eye.append(v)
                self.left_eye.append(vertex)
        
        
        self.y_min_left += ((self.y_max_left - self.y_min_left)/2)
        
        i = 0
        while i < len(self.left_eye):
            if self.vertices[self.left_eye[i]][1] < self.y_min_left:
                #if self.left_eye[i] < self.y_min_left:
                self.left_eye.pop(i)
                continue
            i += 1
        
        for face in self.materials_faces["RightEyeColorSG"]:
            for vertex in self.faces[face]:
                v = self.vertices[vertex]
                
                if self.y_min_right > v[1]:
                    self.y_min_right = v[1]
                if self.y_max_right < v[1]:
                    self.y_max_right = v[1]
                    
                if self.x_min_right > v[0]:
                    self.x_min_right = v[0]
                if self.x_max_right < v[0]:
                    self.x_max_right = v[0]
                
                #self.right_eye.append(v)
                self.right_eye.append(vertex)
        
        self.y_min_right += ((self.y_max_right - self.y_min_right)/2)
        
        i = 0 
        while i < len(self.right_eye):
            if self.vertices[self.right_eye[i]][1] < self.y_min_right:
                #if self.right_eye[i] < self.y_min_right:
                self.right_eye.pop(i)
                continue
            i += 1
        
        
        
        
        
        
        
        