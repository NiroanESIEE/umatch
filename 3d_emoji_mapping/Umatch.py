# IMPORTS
from imutils import face_utils
import argparse
import imutils
import dlib
import cv2
import os
from math import sqrt, acos
from numpy import *
from PIL import Image
import EmojiModifier


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
    v1 = array(shape[27]) - array(shape[8])
    v1 = v1 / linalg.norm(v1)
    v2 = array([0, -1])
    angle = acos(dot(v1, v2))
    angle = angle * 180 / pi
    if shape[27][0] > shape[8][0]:
        angle = angle * (-1)
    return angle

"""
def replace_face(image, emoji, x, y, w, h):
    #im = Image.open(image, 'r')
    #im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = image
    em = Image.open(emoji, 'r').resize((w, h))

    height, width = im.shape[:2]

    image_matrix = zeros((height, width, 3), dtype=uint8)

    #im_list = list(im.getdata())
    em_list = list(em.getdata())



    for i in range(height):
        for j in range(width):
            if x <= j < x + w and y <= i < y + h:
                color = em_list[(i - y) * w + (j - x)]
                if color[3] != 0:
                    image_matrix[i, j] = list(color[:3])
                else:
                    image_matrix[i, j] = list(im[i][j])
            else:
                image_matrix[i, j] = list(im[i][j])

    new_image = Image.fromarray(image_matrix, 'RGB')
    return new_image
"""

if __name__ == "__main__":
    landmark_predictor = "shape_predictor_68_face_landmarks.dat"
    image_path = "example_03.jpg"
    folder = 'output'

    # Initialize face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(landmark_predictor)

    # Load the input image, resize it, and convert it to grayscale
    image = cv2.imread(image_path)
    #image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    rects = detector(gray, 1)
    # clone = image.copy()

    # Loop over the face detections
    for (i, rect) in enumerate(rects):
        # Detect face points
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Get rotation
        angleY = rotation_head_y(shape)
        angleZ = rotation_head_z(shape)

        # Get 3D Emoji
        emoji = EmojiModifier.EmojiModifier("Umatchicken_CombinedTriangulated", 0, 0, [0, angleY, angleZ])
        emoji.image.save("popo.png", 'png')

        # Place Emoji
        w = int(((shape[8][1] - shape[20][1]) * 2) * 1.15)
        h = w
        x = int(shape[27][0] - w / 2)
        y = int(shape[27][1] - h / 2)

        #image1 = replace_face(image, "popo.png", x, y, w, h)


        tmp2image = cv2.imread("popo.png")
        tmp2image = cv2.resize(tmp2image, (w, h))
        rows, cols, channels = tmp2image.shape

        # Main Image
        ROI = image[y:rows + y, x:cols + x]

        # Read Replacement Image
        img2gray = cv2.cvtColor(tmp2image, cv2.COLOR_RGB2GRAY)

        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(ROI, ROI, mask=mask_inv)
        img2_fg = cv2.bitwise_and(tmp2image, tmp2image, mask=mask)

        # Draw Rectangle for each faces
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        dst = cv2.add(img1_bg, img2_fg)

        # image[y:rows + y, x:cols + x] = dst

        dstY = 0
        for i in range(y, rows + y):
            dstX = 0
            for j in range(x, cols + x):
                image[i][j] = dst[dstY][dstX]
                dstX += 1
            dstY += 1

    if not os.path.exists(folder):
        os.mkdir(folder)

    #image1.save(folder + "\output.png")

    cv2.imwrite(folder + '\output.png', image)
