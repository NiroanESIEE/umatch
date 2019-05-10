# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 14:16:36 2019

@author: cheickas
"""

#IMPORTS
from imutils import face_utils
import imutils
import dlib
import cv2
import pickle
import time
from math import sqrt


#FONCTIONS
def face_detection(rects, loadmod, image):
    """
    """
    for (i, rect) in enumerate(rects):
        #Recupere les points du visages et les stock dans une liste
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        features = []
        features.append(dist_between_eyebrow(shape))
        features.append(dist_corner_eye_right(shape))
        features.append(dist_corner_eye_left(shape))
        features.append(dist_eyebrow_eye_right(shape))
        features.append(dist_eyebrow_eye_left(shape))
        features.append(dist_open_eye_right(shape))
        features.append(dist_open_eye_left(shape))
        features.append(dist_nose_width(shape))
        features.append(dist_nose_height(shape))
        features.append(dist_mouth(shape))
        features.append(dist_min_mouth(shape))
        features.append(dist_mouth_width(shape))
        features.append(dist_mouth_cheeks_right(shape))
        features.append(dist_mouth_cheeks_left(shape))
        features.append(dist_mouth_corner(shape))
        
        #Prediction
        emotion = loadmod.predict([features])
        print(emotion)
        #emoji = cv2.imread("emojis/" + emotion[0] + ".png")
        emoji = cv2.imread("emojis/popo.png")
        
        taille = abs(shape[9][1] - shape[20][1]) * 2
        
        posX = shape[28][0] - abs(shape[9][1] - shape[20][1])
        posY = shape[28][1] - abs(shape[9][1] - shape[20][1])
        
        
        place_emoji(image, emoji, posX, posY, taille)

def dist_points(p1, p2):
    dist = sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return dist


# EYES
def dist_between_eyebrow(shape):
    den = dist_points(shape[16], shape[0])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[22], shape[21]) / den
    return dist


def dist_corner_eye_right(shape):
    den = dist_points(shape[15], shape[22])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[42], shape[22]) / den
    return dist


def dist_corner_eye_left(shape):
    den = dist_points(shape[1], shape[21])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[39], shape[21]) / den
    return dist


def dist_eyebrow_eye_right(shape):
    den = dist_points(shape[41], shape[19])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[37], shape[19]) / den
    return dist


def dist_eyebrow_eye_left(shape):
    den = dist_points(shape[46], shape[24])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[44], shape[24]) / den
    return dist


def dist_open_eye_right(shape):
    den = dist_points(shape[45], shape[42])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[47], shape[43]) / den
    return dist


def dist_open_eye_left(shape):
    den = dist_points(shape[39], shape[36])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[40], shape[38]) / den
    return dist


# NOSE
def dist_nose_width(shape):
    den = dist_points(shape[14], shape[2])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[35], shape[31]) / den
    return dist


def dist_nose_height(shape):
    den = dist_points(shape[6], shape[27])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[31], shape[27]) / den
    return dist


# MOUTH
def dist_mouth(shape):
    width = dist_points(shape[54], shape[48])
    height = dist_points(shape[57], shape[51])
    if height == 0:
        height = 0.1
    dist = float(width) / float(height)
    return dist


def dist_min_mouth(shape):
    width = dist_points(shape[54], shape[48])
    height = dist_points(shape[66], shape[62])
    if height == 0:
        height = 0.1
    dist = float(width) / float(height)
    return dist


def dist_mouth_width(shape):
    den = dist_points(shape[13], shape[3])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[54], shape[48]) / den
    return dist


def dist_mouth_cheeks_right(shape):
    den = dist_points(shape[13], shape[3])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[13], shape[54]) / den
    return dist


def dist_mouth_cheeks_left(shape):
    den = dist_points(shape[13], shape[3])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[48], shape[3]) / den
    return dist


def dist_mouth_corner(shape):
    den = dist_points(shape[8], shape[51])
    if den == 0:
        den = 0.1
    dist = dist_points(shape[54], shape[51]) / den
    return dist


def place_emoji(image, emoji, posX, posY, taille):
    tmp2image = emoji
    tmp2image = cv2.resize(tmp2image, (taille, taille))
    rows, cols, channels = tmp2image.shape
    
    print(posX)
    print(posY)
    print(rows)
    print(cols)
    
    ROI = image[posY:rows + posY, posX:cols + posX]
    
    img2gray = cv2.cvtColor(tmp2image, cv2.COLOR_RGB2GRAY)
    
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(ROI, ROI, mask=mask_inv)
    img2_fg = cv2.bitwise_and(tmp2image,tmp2image, mask=mask)
    
    dst = cv2.add(img1_bg, img2_fg)
    image[posY:rows + posY, posX:cols + posX] = dst
    

#MAIN
if __name__ == "__main__":


    loadmod = pickle.load(open("learning_save.sav", 'rb'))
    # INIT DETECTOR DLIB : Visage et traits
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    start = time.time()
    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread("images/H.jpg")
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    
    # emoji mapper
    face_detection(rects, loadmod, image)
    end = time.time()
    print("Temps de prédiction : " + str(end - start) + " secondes")
    cv2.imshow("windows", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
