


import cv2
import numpy as np
import os
import time
import math
import mediapipe as mp
import tensorflow as tf
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# Initialize the camera and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

classifier = Classifier("model/keras_model.h5","model/labels.txt")

# Set offset for cropping and desired output image size
offset = 50
imgSize = 300


labels = ["A","B""BAD","BANG BANG","C","D","E","F","G","GOOD","H","Hi","I","J","K","L","LOVE","M","N","O","OK","P","Q","R","ROCK","S","T","U","V","W","Y","Z",]

while True:
    # Read a frame from the camera
    success, img = cap.read()
    imgOutput = img.copy()
    # Find hands in the frame using the hand detector
    hands, img = detector.findHands(img)
    
    if hands:
        # Get information about the first detected hand
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Create a white image with the specified size
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        # Crop the hand region with an offset
        imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]

        # Calculate aspect ratio of the cropped region
        aspectRatio = h / w

        if aspectRatio > 1:
            # If the aspect ratio is greater than 1 (taller than wide)
            k = imgSize / h
            hCal = imgSize
            wCal = math.ceil(k * w)

            # Check if dimensions are valid
            if wCal > 0 and hCal > 0:
                # Resize the cropped image while preserving aspect ratio
                imgResize = cv2.resize(imgCrop, (wCal, hCal))
                wGap = math.ceil((imgSize - wCal) / 2)

                # Overlay the resized image onto the white image
                imgWhite[0:hCal, wGap:wGap + wCal] = imgResize
                prediction, index = classifier.getPrediction(imgWhite,draw=False)
                print(prediction, index)
        else:
            # If the aspect ratio is less than or equal to 1 (wider than tall)
            k = imgSize / w
            wCal = imgSize
            hCal = math.ceil(k * h)

            # Check if dimensions are valid
            if wCal > 0 and hCal > 0:
                # Resize the cropped image while preserving aspect ratio
                imgResize = cv2.resize(imgCrop, (wCal, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)

                # Overlay the resized image onto the white image
                imgWhite[hGap:hGap + hCal, 0:wCal] = imgResize
                prediction, index = classifier.getPrediction(imgWhite,draw=False)

        # Display the cropped hand and overlaid image
    
        cv2.rectangle(imgOutput, (x-offset, y-offset-50), (x-offset+90, y-offset-50 + 50),(255,0,255),cv2.FILLED )
        cv2.putText(imgOutput,labels[index],(x, y-27), cv2.FONT_HERSHEY_COMPLEX,1.8,(255,0,255),2)
        cv2.rectangle(imgOutput, (x-offset, y-offset), (x + w + offset, y + h + offset),(255,0,255),4 )
        cv2.imshow("imageWhite", imgWhite)
        

    # Display the original image
    cv2.imshow("image", imgOutput)
    
    # Wait for a key press and update the display
    cv2.waitKey(1)
   
