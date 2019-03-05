import logging
import logging.handlers
import argparse
import sys
import os
import time
import cv2
import numpy as np
from bluetooth import *

def isPinPresent(pinMat):
    c = pinMat.sum()
    print(c)
    if c>1000:
        return True
    else:
        return False
    
def showSavePin(pinImg,num):
    cv2.imshow('pin',pinImg)
    s = 'pin'+str(num)+'.jpg'
    cv2.imwrite(s,pinImg)
    
# Main loop
def main():
    # Setup logging
    
    bg_img = cv2.imread("nopins.jpg")
    gray_image = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    threshold = 140
    (thresh, bg_img) = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
##    cv2.imshow("all pins", bg_img)
##    cv2.waitKey(0)
    xPos=[462,349,425,236,323,397,125,219,296,378]
    yPos=[227,229,232,230,235,235,189,198,238,238]
    width = [16,17,12,16,13,14,8,10,9,8]
    height = [18,22,18,18,16,22,6,9,14,14]
    
    
    cam = cv2.VideoCapture(0)
    # We need to wait until Bluetooth init is done
    time.sleep(10)

    # Make device visible
    os.system("hciconfig hci0 piscan")

    # Create a new server socket using RFCOMM protocol
    server_sock = BluetoothSocket(RFCOMM)
    # Bind to any port
    server_sock.bind(("", PORT_ANY))
    # Start listening
    server_sock.listen(1)

    # Get the port the server socket is listening
    port = server_sock.getsockname()[1]

    # The service UUID to advertise
    uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

    # Start advertising the service
    advertise_service(server_sock, "RaspiBtSrv",
                       service_id=uuid,
                       service_classes=[uuid, SERIAL_PORT_CLASS],
                       profiles=[SERIAL_PORT_PROFILE])


    # Main Bluetooth server loop
    while True:

        print "Waiting for connection on RFCOMM channel %d" % port

        try:
            client_sock = None

            # This will block until we get a new connection
            client_sock, client_info = server_sock.accept()
            print "Accepted connection from ", client_info

            # Read the data sent by the client
            data = client_sock.recv(1024)
            if len(data) == 0:
                break

            print "Received [%s]" % data

            # Handle the request
            if data == "check":
                # insert program here to read images and process
                cam.release()
                cam = cv2.VideoCapture(0)
                ret, img = cam.read()
##                cv2.imshow("input", img)
##                cv2.waitKey(0)
                
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                threshold = 110
                (thresh, im_bw) = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
                
                ref_img = cv2.absdiff(im_bw,bg_img)
                
                pin1 = ref_img[xPos[0]:xPos[0]+width[0],yPos[0]:yPos[0]+height[0]]
                pin2 = ref_img[xPos[1]:xPos[1]+width[1],yPos[1]:yPos[1]+height[1]]
                pin3 = ref_img[xPos[2]:xPos[2]+width[2],yPos[2]:yPos[2]+height[2]]
                pin4 = ref_img[xPos[3]:xPos[3]+width[3],yPos[3]:yPos[3]+height[3]]
                pin5 = ref_img[xPos[4]:xPos[4]+width[4],yPos[4]:yPos[4]+height[4]]
                pin6 = ref_img[xPos[5]:xPos[5]+width[5],yPos[5]:yPos[5]+height[5]]
                pin7 = ref_img[xPos[6]:xPos[6]+width[6],yPos[6]:yPos[6]+height[6]]
                pin8 = ref_img[xPos[7]:xPos[7]+width[7],yPos[7]:yPos[7]+height[7]]
                pin9 = ref_img[xPos[8]:xPos[8]+width[8],yPos[8]:yPos[8]+height[8]]
                pin10 = ref_img[xPos[9]:xPos[9]+width[9],yPos[9]:yPos[9]+height[9]]
                
                response = ""
                ctr = 0
                
                if isPinPresent(pin1):
                    ctr = ctr + 1
                    response+="1"
                if isPinPresent(pin2):
                    ctr = ctr + 1
                    response+="2"
                if isPinPresent(pin3):
                    ctr = ctr + 1
                    response+="3"
                if isPinPresent(pin4):
                    ctr = ctr + 1
                    response+="4"
                if isPinPresent(pin5):
                    ctr = ctr + 1
                    response+="5"
                if isPinPresent(pin6):
                    ctr = ctr + 1
                    response+="6"
                if isPinPresent(pin7):
                    ctr = ctr + 1
                    response+="7"
                if isPinPresent(pin8):
                    ctr = ctr + 1
                    response+="8"
                if isPinPresent(pin9):
                    ctr = ctr + 1
                    response+="9"
                if isPinPresent(pin10):
                    ctr = ctr + 1
                    response+="10"
                    
                response = str(ctr)+" "+response
                
                showSavePin(pin1,1)
                showSavePin(pin2,2)
                showSavePin(pin3,3)
                showSavePin(pin4,4)
                showSavePin(pin5,5)
                showSavePin(pin6,6)
                showSavePin(pin7,7)
                showSavePin(pin8,8)
                
            # Insert more here
            else:
                response = "msg:Not supported"

            client_sock.send(response)
            print "Sent back [%s]" % response

        except IOError:
            pass

        except KeyboardInterrupt:

            if client_sock is not None:
                client_sock.close()

            server_sock.close()

            print "Server going down"
            break

main()