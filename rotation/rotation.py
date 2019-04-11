from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
import cv2
from math import sqrt, acos
from numpy import *
import pickle


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
    if shape[27][0] < shape[8][0]:
        angle = angle * (-1)
    return angle


def rotation_head_x(shape):
    den = dist_points(shape[1], shape[15])
    if den == 0:
        den = 0.1
    num = dist_points(shape[30], shape[33])
    angle = num / den
    print(str(num) + "/" + str(den))
    return angle


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start()
time.sleep(2.0)

start = time.time()

font = cv2.FONT_HERSHEY_COMPLEX

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    end = time.time()
    start = time.time()

    # loop over the face detections
    for rect in rects:
        print("coco")
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        i = 1
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
            #cv2.putText(frame, str(i), (x, y), font, 0.3, (0, 255, 0))
            i += 1

        p31 = shape[30]
        p34 = shape[33]
        p52 = shape[51]
        cv2.line(frame, (p31[0], p31[1]), (p34[0], p34[1]), (0, 255, 0))
        cv2.line(frame, (p31[0], p31[1]), (p52[0], p52[1]), (255, 0, 0))

        angleY = rotation_head_y(shape)
        #print("angleY = " + str(angleY) + "°")

        angleZ = rotation_head_z(shape)
        #print("angleZ = " + str(angleZ) + "°")

        angleX = rotation_head_x(shape)
        #print("angleX = " + str(angleX) + "°")

    # show the frame
    end = time.time()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()