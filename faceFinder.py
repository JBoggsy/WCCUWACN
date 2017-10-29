#!/usr/bin/env python
import rospy
import cv2
import numpy as np

from time import sleep

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')

CURRENT_IMAGE = None
bridge = CvBridge()

def image_callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        final_image = see_faces(cv_image)
        cv2.imshow("Image window", final_image)
        cv2.waitKey(3)
    except CvBridgeError as e:
        print(e)

def see_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    return img

image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)

rospy.init_node('tracker', anonymous=True)
try:
  rospy.spin()
except KeyboardInterrupt:
  print("Shutting down")
