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
        #emoji = cv2.imread("emojis/test.png")
        
        #taille = abs(shape[9][1] - shape[20][1]) * 2
        
        #posX = shape[28][0] - abs(shape[9][1] - shape[20][1])
        #posY = shape[28][1] - abs(shape[9][1] - shape[20][1])
        
        #place_emoji(image, emoji, posX, posY, taille)


# EYES
def dist_between_eyebrow(shape):
    den = abs(float(shape[16][0] - shape[0][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[22][0] - shape[21][0])) / den
    return dist

def dist_corner_eye_right(shape):
    den = abs(float(shape[15][1] - shape[22][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[42][1] - shape[22][1])) / den
    return dist


def dist_corner_eye_left(shape):
    den = abs(float(shape[1][1] - shape[21][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[39][1] - shape[21][1])) / den
    return dist


def dist_eyebrow_eye_right(shape):
    den = abs(float(shape[41][1] - shape[19][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[37][1] - shape[19][1])) / den
    return dist


def dist_eyebrow_eye_left(shape):
    den = abs(float(shape[46][1] - shape[24][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[44][1] - shape[24][1])) / den
    return dist


def dist_open_eye_right(shape):
    den = abs(float(shape[45][0] - shape[42][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[47][1] - shape[43][1])) / den
    return dist


def dist_open_eye_left(shape):
    den = abs(float(shape[39][0] - shape[36][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[40][1] - shape[38][1])) / den
    return dist


# NOSE
def dist_nose_width(shape):
    den = abs(float(shape[14][0] - shape[2][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[35][0] - shape[31][0])) / den
    return dist


def dist_nose_height(shape):
    den = abs(float(shape[6][1] - shape[27][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[31][1] - shape[27][1])) / den
    return dist


# MOUTH
def dist_mouth(shape):
    width = abs(shape[54][0] - shape[48][0])
    height = abs(shape[57][1] - shape[51][1])
    if height == 0:
        height = 0.1

    dist = float(width) / float(height)
    return dist


def dist_min_mouth(shape):
    width = abs(shape[54][0] - shape[48][0])
    height = abs(shape[66][1] - shape[62][1])
    if height == 0:
        height = 0.1

    dist = float(width) / float(height)
    return dist


def dist_mouth_width(shape):
    den = abs(float(shape[13][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[54][0] - shape[48][0])) / den
    return dist


def dist_mouth_cheeks_right(shape):
    den = abs(float(shape[13][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[13][0] - shape[54][0])) / den
    return dist


def dist_mouth_cheeks_left(shape):
    den = abs(float(shape[13][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[48][0] - shape[3][0])) / den
    return dist


def dist_mouth_corner(shape):
    den = abs(float(shape[8][1] - shape[51][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[54][1] - shape[51][1])) / den
    return dist


def place_emoji(image, emoji, posX, posY, taille):
    tmp2image = emoji
    tmp2image = cv2.resize(tmp2image, (taille, taille))
    rows, cols, channels = tmp2image.shape
    
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
    image = cv2.imread("images/example_01.jpg")
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
