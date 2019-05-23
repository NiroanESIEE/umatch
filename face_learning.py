# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 11:03:35 2019

"""

#IMPORTS
from imutils import face_utils
import imutils
import dlib
import cv2
import os
from sklearn.linear_model import LogisticRegression
import pickle
import argparse
from face_parameter import *
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


#FONCTIONS
def face_detection(rects, emotion, learning_matrix, gray):
    """
    """
    for (i, rect) in enumerate(rects):
        #Recupere les points du visages et les stock dans une liste
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        result.append(emotion)
        features = get_features(shape)
        if learning_matrix == "learning":
            param.append(features)
        elif learning_matrix == "matrix":
            predicted_emotion = loadmod.predict([features])
            predict.append(predicted_emotion)


def main(option, file_path):
    
    #Parcours les images de différentes emotions
    for folder in os.listdir(file_path):
        for img in os.listdir(file_path + "/" + folder):
            # Charge l'image, la redimensionne et la met en noir et blanc
            image = cv2.imread(file_path + "/" + folder + "/" + img)
            image = imutils.resize(image, width=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detection des visages
            rects = detector(gray, 1)
            face_detection(rects, folder, option,gray)
            
    if option == "learning":
        #face_detection(rects, folder, "learning", gray)
        logreg = LogisticRegression(C=1e5, max_iter= 20000,solver='sag', multi_class='multinomial')
        logreg.fit(param, result)
        #Sauvegarder le modele
        filename = "new_LR_learning.sav"
        pickle.dump(logreg, open(filename, 'wb'))
    elif option == "matrix":
        conf_matrix = confusion_matrix(result, predict, labels=["angry", "disgusted", "happy", "neutral", "sad", "surprised"])
        conf_matrix = np.array(conf_matrix)
        class_names = ["Angry", "Disgusted", "Happy", "Neutral", "Sad", "Surprised"]
        fig, ax = plot_confusion_matrix(conf_mat=conf_matrix,
                                        colorbar=True,
                                        show_absolute=False,
                                        show_normed=True,
                                        class_names=class_names)
        plt.show()
        
#MAIN
if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--learning",help="Face training")
    ap.add_argument("-t","--confusion_matrix", help="Test learning")
    args = ap.parse_args()
    
    param = [] 
    result = []
    predict = []

    # INIT DETECTOR DLIB : Visage et traits
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    if args.learning:
        print("Learning : " + args.learning)
        main("learning", args.learning)
    elif args.confusion_matrix:
        print("Confusion matrix : " + args.confusion_matrix)
        loadmod = pickle.load(open("new_LR_learning.sav", 'rb'))
        main("matrix", args.confusion_matrix)
    
    
    


