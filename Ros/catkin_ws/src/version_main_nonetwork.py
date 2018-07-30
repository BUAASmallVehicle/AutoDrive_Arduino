#!/usr/bin/python2.7
#-*-coding: utf-8 -*-
import rospy
from test_msg.msg import vehicle_ctrl
from FrameWork.Nav_model.image_handle.lane_detection_no_network.lane_detection import *

# 开启视频
cap = cv2.VideoCapture(1)

# 循环参数
n = 0
angle_list = []

def talker():
	global n
	# publisher参数定义
	pub = rospy.Publisher('version_without_network', vehicle_ctrl)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(100)  # 10hz
	
	# 初始化vehicle_ctrl类
	ctrl_para = vehicle_ctrl()
	
	# 循环
	while not rospy.is_shutdown():
		n = n + 1
		
		ret, img_org = cap.read()
		img = img_org.copy()
		img_org_copy = img_org.copy()
		
		# 阈值过滤
		comb_thresh = hls_select(img, channel='l', thresh=(180, 255))
		
		# 透视变换
		M, Minv = get_M_Minv()
		binary_warped = cv2.warpPerspective(comb_thresh, M, img_org.shape[1::-1], flags=cv2.INTER_LINEAR)
		
		# 检测车道边线
		left_fit, right_fit, left_lane_inds, right_lane_inds = find_line(binary_warped)
		
		# 计算
		curv, theta, dist = calculate_curv_and_pos(binary_warped, left_fit, right_fit)
		angle = theta
		
		angle_list.append(angle)
		
		if n == 20:
			n = 0
			ctrl_para.accspeed = 0.0
			ctrl_para.speed = 0.0
			ctrl_para.angle = np.mean(np.array(angle_list), axis=0)
			rospy.loginfo(ctrl_para)
			pub.publish(ctrl_para)
		# cv2.imshow('lane', output)
		
		rate.sleep()
	

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
