from flask import Flask, render_template, Response
import cv2
import numpy as np
import mediapipe as mp
from cvzone.ClassificationModule import Classifier
import math  # Add this import statement for the math module

app = Flask(__name__)

# Initialize the camera and hand detector
cap = cv2.VideoCapture(0)
classifier = Classifier("model/keras_model.h5", "model/labels.txt")

# Set offset for cropping and desired output image size
offset = 50
imgSize = 300

# Define a list of labels for classification
labels = ["A", "B", "BAD", "BANG BANG", "C", "D", "E", "F", "G", "GOOD", "H", "Hi", "I", "J", "K", "L", "LOVE", "M",
          "N", "O", "OK", "P", "Q", "R", "ROCK", "S", "T", "U", "V", "W", "Y", "Z"]

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def generate_frames():
    while True:
        success, img = cap.read()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        _, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_labels():
    while True:
        success, img = cap.read()
        imgOutput = img.copy()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_coords = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in hand_landmarks.landmark]
                bounding_box = cv2.boundingRect(np.array(landmarks_coords))
                x, y, w, h = bounding_box

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    hCal = imgSize
                    wCal = math.ceil(k * w)

                    if wCal > 0 and hCal > 0:
                        imgResize = cv2.resize(imgCrop, (wCal, hCal))
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[0:hCal, wGap:wGap + wCal] = imgResize
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)

                        if 0 <= index < len(labels):
                            label = labels[index]
                            yield f"data: {label}\n\n"

        _, jpeg = cv2.imencode('.jpg', imgOutput)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/label_feed')
def label_feed():
    return Response(generate_labels(), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
