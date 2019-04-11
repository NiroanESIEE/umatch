from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
import cv2
import pickle
from math import sqrt
from skimage import transform as tf

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


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
loadmod = pickle.load(open("learning_save.sav", 'rb'))

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start()
time.sleep(2.0)

start = time.time()
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

    #if(end - start > 2) :
    start = time.time()
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

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

        # Prediction
        emotion = loadmod.predict([features])
        print(emotion)

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