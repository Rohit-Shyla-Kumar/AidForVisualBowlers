import os
import time
import cv2
import numpy as np

while True:
    
##    First image with all pins
    cam = cv2.VideoCapture(0)
    ret, img = cam.read()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = 100
    (thresh, im_bw) = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("all pins",im_bw)
    cv2.waitKey(0)
    cam.release()
    print("All pins image taken")
    
##    Second pic with no pins
    cam = cv2.VideoCapture(0)
    ret, img = cam.read()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh1, im_bw1) = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("no pins",im_bw1)
    cv2.waitKey(0)
    cam.release()
    print("No pins image taken")
    img1 = cv2.absdiff(im_bw,im_bw1)
    
    break

cv2.imwrite("subtracted.jpg",img1)
cv2.imwrite("allpins.jpg",im_bw)
cv2.imwrite("nopins.jpg",im_bw1)