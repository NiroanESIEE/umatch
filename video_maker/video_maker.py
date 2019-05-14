# -*- coding: utf-8 -*-
"""
Created on Mon May 13 19:17:38 2019

@author: adelphin
"""

# IMPORTS
import cv2

if __name__ == "__main__":
    cap = cv2.VideoCapture('Test.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.mp4', fourcc, 29.97, (1920, 1080))
    frames = 0
    while(cap.isOpened()):
        frames += 1
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            #gray = cv2.flip(gray, 0)
            out.write(frame)
        else:
            break
    print(frames)
    cap.release()
    out.release()
    cv2.destroyAllWindows()