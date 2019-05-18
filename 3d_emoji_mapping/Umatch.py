# IMPORTS
from imutils import face_utils
import argparse
import imutils
import dlib
import cv2
import os
from math import sqrt, acos
import numpy as np
from PIL import Image
import EmojiModifier

people = []

def dist_points(p1, p2):
    dist = sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return dist


def dist_cheeks_left(shape):
    den = dist_points(shape[14], shape[2])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[33], shape[2]) / den
    return dist


def dist_cheeks_right(shape):
    den = dist_points(shape[14], shape[2])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[14], shape[33]) / den
    return dist


def rotation_head_y(shape):
    angle_y_max = 90
    ratio_left = dist_cheeks_left(shape)
    ratio_right = dist_cheeks_right(shape)
    ratio = (ratio_left - ratio_right)
    angle = ratio * angle_y_max
    return angle


def rotation_head_z(shape):
    v1 = np.array(shape[27]) - np.array(shape[8])
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.array([0, -1])
    angle = acos(np.dot(v1, v2))
    angle = angle * 180 / np.pi
    if shape[27][0] > shape[8][0]:
        angle = angle * (-1)
    return angle


def dist_mouth_vertical(shape, rect):
    den = abs(rect.tl_corner().y - rect.br_corner().y)
    if den == 0:
        den = 0.1
    dist = dist_points(shape[51], shape[57]) / den
    return dist


def dist_mouth_horizontal(shape, rect):
    den = abs(rect.tl_corner().x - rect.br_corner().x)
    if den == 0:
        den = 0.1
    dist = dist_points(shape[48], shape[54]) / den
    return dist

def place_emoji(image_cv2, image_pil, detector, predictor, models):
    
    #image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)

    # Detect faces
    rects = detector(gray, 1)
    
    model_index = 0
    # Loop over the face detections
    for (i, rect) in enumerate(rects):
        #Check people
        if(len(people) == 0):
            tmp = []
            tmp.append(rect)
            center = ( (rect.tr_corner().x - rect.tl_corner().x) / 2 + rect.tl_corner().x, (rect.bl_corner().y - rect.tl_corner().y) / 2 + rect.tl_corner().y)
            tmp.append(center)
            tmp.append(model_index)
            people.append(tmp) #[Rect, Center, Model]
        else:
            new_center = ( (rect.tr_corner().x - rect.tl_corner().x) / 2 + rect.tl_corner().x, (rect.bl_corner().y - rect.tl_corner().y) / 2 + rect.tl_corner().y)
            for p in people:
                if(p[0].tl_corner().x <= new_center[0] <= p[0].tr_corner().x and p[0].tl_corner().y <= new_center[1] <= p[0].br_corner().y):
                    model_index = p[2]
                    p[0] = rect
                    p[1] = new_center
                    break
            else:
                tmp = []
                tmp.append(rect)
                center = ( (rect.tr_corner().x - rect.tl_corner().x) / 2 + rect.tl_corner().x, (rect.bl_corner().y - rect.tl_corner().y) / 2 + rect.tl_corner().y)
                tmp.append(center)
                
                if people[-1][-1] >= (len(models) - 1):
                    
                    model_index = 0
                else:
                    model_index += 1
                
                tmp.append(model_index)
                people.append(tmp) #[Rect, Center, Model]
        
        # Detect face points
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        # Get rotation
        angleY = rotation_head_y(shape)
        angleZ = rotation_head_z(shape)
        
        # Choose 3D model
        #model = models[model_index]
        model = "Umatchii_Normal_Mouth"
        
        # Get mouth
        mouthX = dist_mouth_horizontal(shape, rect)
        mouthY = dist_mouth_vertical(shape, rect)
        mouth = [mouthX, mouthY]

        if model.find("Normal_Mouth") >= 0:
            mouth.append(shape[48:67])
        
        # Get 3D Emoji
        emoji = EmojiModifier.EmojiModifier(model, mouth, 0, [0, angleY, angleZ])
        emoji.image.save("popo.png", "png")
        
        # Place Emoji
        w = abs(shape[8][1] - shape[19][1]) * 2
        h = w
        x = shape[27][0] - abs(shape[8][1] - shape[19][1])
        y = shape[27][1] - abs(shape[8][1] - shape[19][1])
        
        emoji.image = emoji.image.resize((w, h), Image.ANTIALIAS)
        
        image_pil.paste(emoji.image, (x, y, (x + w), (y + h)), emoji.image)
        image_pil.save("imagePil.png", 'png')
        
#        if model_index >= (len(models) - 1):
#            model_index = 0
#        else:
#            model_index += 1
        

    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return image_pil
    
    
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--picture",help="Image path")
    ap.add_argument("-v","--video", help="Video path")
    args = ap.parse_args()
    landmark_predictor = "shape_predictor_68_face_landmarks.dat"
    folder = 'output\\'
    
    models = ["Umatchicken_Beak_Mouth", "Umapion_Beak_Mouth", "Umatchii_Normal_Mouth"]
    #models = ["Umatchicken_Beak_Mouth", "Umapion_Beak_Mouth"]
    

    # Initialize face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(landmark_predictor)

    image_cv2 = cv2.imread("D.jpg")
    image_pil = Image.open("D.jpg")
    new_image = place_emoji(image_cv2, image_pil, detector, predictor, models)
    new_image.save(folder + "output.png", 'png')


    # Image
    """if args.picture:
        image_cv2 = cv2.imread(args.picture)
        image_pil = Image.open(args.picture)
        new_image = place_emoji(image_cv2, image_pil, detector, predictor, models)
        new_image.save(folder + "output.png", 'png')
        
    elif args.video:
        # Video
        cap = cv2.VideoCapture(args.video)
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(folder + 'output.mp4', fourcc, cap.get(5), (int(cap.get(3)), int(cap.get(4))))
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imwrite("tmp.jpg", frame)
                image_cv2 = cv2.imread("tmp.jpg")
                image_pil = Image.open("tmp.jpg")
                #image_pil = Image.fromarray(frame)
                new_image = place_emoji(image_cv2, image_pil, detector, predictor, models)
                imagev2 = cv2.cvtColor(np.array(new_image), cv2.COLOR_BGR2RGB)
                out.write(imagev2)
            else:
                break
        
        os.remove("tmp.jpg")
        cap.release()
        out.release()
        cv2.destroyAllWindows()"""
    