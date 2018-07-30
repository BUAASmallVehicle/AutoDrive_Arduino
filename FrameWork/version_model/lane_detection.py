#-*-coding: utf-8 -*-

## ---------------------- ##
## 通过神经网络实现路面的识别 ##
## ---------------------- ##

import numpy as np
import cv2
# import matplotlib.pyplot as plt
from scipy.misc import imresize
from moviepy.editor import VideoFileClip
from keras.models import load_model
from FrameWork.Nav_model.image_handle.overturn import *
from FrameWork.Nav_model.image_handle.road_base_line import *
from FrameWork.Nav_model.move_with_geometry.move_para_geometry import *

# 定义进行车道线检测结果的均值化
class Lanes():
	def __init__(self):
		self.recent_fit = []
		self.avg_fit = []
		
# 定义车道线检测的函数

def road_lines(model, image):
	# 对即将输入给模型的图片进行预处理
	small_img = imresize(image, (80, 160, 3))
	small_img = np.array(small_img)
	small_img = small_img[None, :, :, :]
		
	# 应用模型对图片进行车道线检测并进行反标准化
	prediction = model.predict(small_img)
	prediction = prediction[0] * 255
		
	# 将预测结果添加到lanes列表中已进行均值化操作
	lanes = Lanes()
	lanes.recent_fit.append(prediction)
	# 用后五个值计算均值
	if len(lanes.recent_fit) > 20:
		lanes.recent_fit = lanes.recent_fit[1:]
	
	# 计算平均检测值
	lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis=0)
	lanes_prediction_1D = lanes.avg_fit.reshape(80, 160)
	
	return lanes_prediction_1D
	
def test_lane_detection():
	model = load_model('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_model.h5')
	
	# 获取视频
	cap = cv2.VideoCapture(1)
	cap.open('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/video/project_video.mp4')
	fps = cap.get(cv2.CAP_PROP_FPS)
	frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	
	# 进行循环
	for i in range(int(frames)):
		ret, frame = cap.read()
		# 进行识别
		Lanes_1D = road_lines(model, frame)
		
		output = imresize(Lanes_1D, (120, 160, 1))
		
		# 透视变换矩阵
		pts1 = np.float32([[69, 110], [99, 110], [70, 115], [113, 115]])
		pts2 = np.float32(
			[[200, 115 - 3.73 * (113 - 70) / 1.75], [341, 115 - 3.73 * (113 - 70) / 1.75], [200, 431], [341, 431]])
		
		M = cv2.getPerspectiveTransform(pts1, pts2)
		
		# 透视变换
		dst_img_tran = cv2.warpPerspective(output, M, (500, 700))
		dst_img = imresize(dst_img_tran, (1280, 720))
		
		# 进行反转
		dst_img_tran = np.rot90(dst_img_tran, -1)
		# dst_img = rotation(dst_img)
		
		road_line = road_base_line(dst_img_tran)
		
		curve_xy = list(road_line.curve_xy)
		
		ctrl_para = move_para_geometry(30, curve_xy)
		
		print('SteerAngle:' + str(ctrl_para.steerAngle))
		
		cv2.imshow('lanes', output)
		
		# 输入q退出
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	# 释放
	cap.release()
	cv2.destroyAllWindows()
	