import cv2
import numpy as np
import os
import time
import math
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector

# Initialize the camera and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# Set offset for cropping and desired output image size
offset = 50
imgSize = 300

folder = 'C:/Users/Asus Tuf Gaming/Downloads/ASL_Project/data collection/data/A'
counter = 0

while True:
    # Read a frame from the camera
    success, img = cap.read()
    
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

        # Display the cropped hand and overlaid image
    
        cv2.imshow("imageWhite", imgWhite)

    # Display the original image
    cv2.imshow("image", img)
    
    # Wait for a key press and update the display
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/image_{time.time()}.jpg', imgWhite)
        print(counter)
