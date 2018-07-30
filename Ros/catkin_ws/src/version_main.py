#!/usr/bin/python2.7
#-*-coding: utf-8 -*-
import rospy
from test_msg.msg import vehicle_ctrl
import numpy as np
import cv2
# import matplotlib.pyplot as plt
from scipy.misc import imresize
from moviepy.editor import VideoFileClip
from keras.models import load_model
from FrameWork.Nav_model.image_handle.overturn import *
from FrameWork.Nav_model.image_handle.road_base_line import *
from FrameWork.Nav_model.move_with_geometry.move_para_geometry import *
from FrameWork.version_model.lane_detection import *

cap = cv2.VideoCapture(1)
# cap.open('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/video/project_video.mp4')
model = load_model('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_model.h5')

# 透视变换矩阵
pts1 = np.float32([[69, 110], [99, 110], [70, 115], [113, 115]])
pts2 = np.float32(
	[[200, 115 - 3.73 * (113 - 70) / 1.75], [341, 115 - 3.73 * (113 - 70) / 1.75], [200, 431], [341, 431]])

M = cv2.getPerspectiveTransform(pts1, pts2)

# 循环参数
n = 0
angle_list = []

def talker():
	global n
	
	pub = rospy.Publisher('vehicle_ctrl_para', vehicle_ctrl)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(100)  # 10hz
	
	ctrl_para = vehicle_ctrl()
	while not rospy.is_shutdown():
		n = n + 1
		ret, frame = cap.read()
	
		Lanes_1D = road_lines(model, frame)
	
		output = imresize(Lanes_1D, (120, 160, 1))
		
		# 进行转换
		# output = perspective(output)
		dst_img_tran = cv2.warpPerspective(output, M, (500, 700))
		dst_img = imresize(dst_img_tran, (1280, 720))
	
		# 进行反转
		dst_img_tran = np.rot90(dst_img_tran, -1)
	
		road_line = road_base_line(dst_img_tran)
	
		curve_xy = list(road_line.curve_xy)
	
		angle = move_para_geometry(30, curve_xy).steerAngle
		
		angle_list.append(angle)
		
		if n == 20:
			n = 0
			ctrl_para.accspeed = 0.0
			ctrl_para.speed = 0.0
			ctrl_para.angle = np.mean(np.array(angle_list), axis = 0)
			rospy.loginfo(ctrl_para)
			pub.publish(ctrl_para)
		# cv2.imshow('lane', output)
		
		rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass