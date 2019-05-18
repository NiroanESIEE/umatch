from imutils import face_utils
import imutils
import dlib
import cv2
import os
from sklearn.metrics import confusion_matrix
import pickle
from math import sqrt

from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


result = []
predict = []

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


def dist_mouth_vertical(shape, rect):
    den = abs(rect.tl_corner().y - rect.br_corner().y)
    if den == 0:
        den = 0.1
    dist = dist_points(shape[51], shape[57]) / den
    return dist


def face_detection(rects, emotion):
    for (i, rect) in enumerate(rects):
        # Recupere les points du visages et les stock dans une liste
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

        result.append(emotion)
        emotion = loadmod.predict([features])
        predict.append(emotion)
        
if __name__ == "__main__":
    # INIT DETECTOR DLIB : Visage et traits
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    loadmod = pickle.load(open("new_LR_learning.sav", 'rb'))

    # Parcours les images de différentes emotions
    for folder in os.listdir("learning_images_v3"):
        for img in os.listdir("learning_images_v3/" + folder):
            # Charge l'image, la redimensionne et la met en noir et blanc
            image = cv2.imread("learning_images_v3/" + folder + "/" + img)
            image = imutils.resize(image, width=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detection des visages
            rects = detector(gray, 1)
            face_detection(rects, folder)

    # Confusion Matrix
    conf_matrix = confusion_matrix(result, predict, labels=["angry", "disgusted", "happy", "neutral", "sad", "surprised"])
    print(conf_matrix)
    """class_names = ["Angry", "Disgusted", "Happy", "Neutral", "Sad", "Surprised"]

    fig, ax = plot_confusion_matrix(conf_mat=conf_matrix,
                                    colorbar=True,
                                    show_absolute=False,
                                    show_normed=True,
                                    class_names=class_names)
    plt.show()"""