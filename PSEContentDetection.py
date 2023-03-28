#!/usr/bin/env python3

# PSEContentDetection.py
##################################################
# This is a simple script for detecting visual
# patterns that are known to commonly trigger
# photosensitive epilepsy. This is by no means 
# exhaustive for finding any potentially triggering
# content, but it is capable of detecting rapid
# gamma and color changes within video files.
##################################################
# MIT License
##################################################
# Author: Harviel Arcilla
# Copyright: Copyright 2023, 
# License: MIT License
# Version: 1.0.0
# Email: karcilla@stanford.edu
# Status: TO BE EXPANDED UPON
##################################################

import numpy as np
import cv2 as cv
import os

filepath = input("\nPlease input filepath: ")  # input video
cap = cv.VideoCapture(filepath)  

fps = int(cap.get(cv.CAP_PROP_FPS))  # const
totalFrames = cap.get(cv.CAP_PROP_FRAME_COUNT)  # const
numPixels = cap.get(cv.CAP_PROP_FRAME_WIDTH) * cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # const
deltaLimit = numPixels * 255 * 3  # const

flashFound = False  # found patterns that may be triggering
frameIndex = 0  # current frame
delta = 0  # value used to calculate flashing lights

cap.set(cv.CAP_PROP_POS_FRAMES, frameIndex)
res, frame1 = cap.read()
res, frame2 = cap.read()
gray1 = np.array(cv.cvtColor(frame1, cv.COLOR_BGR2GRAY), dtype=np.int16)
gray2 = np.array(cv.cvtColor(frame2, cv.COLOR_BGR2GRAY), dtype=np.int16)
delta += np.sum(np.absolute(np.subtract(gray2, gray1)))

for i in range(fps):  # initialization of first second of video
    frame1 = frame2
    gray1 = np.array(cv.cvtColor(frame1, cv.COLOR_BGR2GRAY), dtype=np.int16)
    res, frame2 = cap.read()
    gray2 = np.array(cv.cvtColor(frame2, cv.COLOR_BGR2GRAY), dtype=np.int16)
    delta += np.sum(np.absolute(np.subtract(gray2, gray1)))
    

while(frameIndex + fps < totalFrames):  # scan entire video for triggering content
    os.system('clear')
    print("Scanning: Frame ", frameIndex, " of ", int(totalFrames - fps - 1), " | DELTA: ", int(delta*100/deltaLimit), "%")
    if delta > deltaLimit:  # if over perceived visual limit end scan and return warning.
        flashFound = True
        break
    else:
        cap.set(cv.CAP_PROP_POS_FRAMES, frameIndex)  # analyze one second of video for rapid imagery
        res, frame1 = cap.read()
        trailGray1 = np.array(cv.cvtColor(frame1, cv.COLOR_BGR2GRAY), dtype=np.int16)
        res, frame2 = cap.read()
        trailGray2 = np.array(cv.cvtColor(frame2, cv.COLOR_BGR2GRAY), dtype=np.int16)
        delta -= np.sum(np.absolute(np.subtract(trailGray2, trailGray1)))

        cap.set(cv.CAP_PROP_POS_FRAMES, frameIndex + fps-1)
        res, frame1 = cap.read()
        leadGray1 = np.array(cv.cvtColor(frame1, cv.COLOR_BGR2GRAY), dtype=np.int16)
        res, frame2 = cap.read()
        leadGray2 = np.array(cv.cvtColor(frame2, cv.COLOR_BGR2GRAY), dtype=np.int16)
        delta += np.sum(np.absolute(np.subtract(leadGray2, leadGray1)))
    frameIndex += 1

cap.release()
if (flashFound):
    print("\n===============================================================================")
    print("WARNING: This video might be triggering for those with photosensitive epilepsy.")
    print("===============================================================================\n")
else:
    print("\n===============================================================================")
    print("                     Triggering content not detected.")
    print("===============================================================================\n")



