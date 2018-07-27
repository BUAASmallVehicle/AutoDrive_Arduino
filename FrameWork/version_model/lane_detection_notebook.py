# -*- coding: utf-8 -*-
"""
使用模型进行车道线识别
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.misc import imresize
from moviepy.editor import VideoFileClip
from keras.models import load_model

# 加载网络模型
model = load_model('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_model.h5')


# 定义类进行车道线检测结果的均值化
class Lanes():
	def __init__(self):
		self.recent_fit = []
		self.avg_fit = []


def road_lines(image):
	""" 拍摄道路图像，运用模型进行车道线检测
	并以绿色标出然后与原图像进行合并
	"""
	
	print(image.shape)
	
	# 对即将输入给模型的图片进行预处理
	small_img = imresize(image, (80, 160, 3))
	small_img = np.array(small_img)
	small_img = small_img[None, :, :, :]
	
	# 应用模型对图片进行车道线检测并进行反标准化
	prediction = model.predict(small_img)
	prediction = prediction[0] * 255
	print(prediction.shape)
	'''
	plt.imshow(prediction)
	plt.show()
	'''
	# 将预测结果添加到lanes列表中已进行均值化操作
	lanes.recent_fit.append(prediction)
	# 用后五个值计算均值
	if len(lanes.recent_fit) > 5:
		lanes.recent_fit = lanes.recent_fit[1:]
	
	# 计算平均检测值
	lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis=0)
	print(lanes.avg_fit.shape)
	
	# 生成R和B颜色维度，与G颜色维度堆叠
	blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
	lane_drawn = np.dstack((blanks, lanes.avg_fit, blanks))
	tmp_img = imresize(lane_drawn, (80, 160))
	cv2.imwrite('tmp.png', tmp_img)
	plt.imshow(lanes.avg_fit.reshape(80, 160))
	plt.show()
	
	# 重新设定图像大小以匹配原图像
	lane_image = imresize(lane_drawn, (720, 1280, 3))
	
	# 将车道线图像与原图像进行合并
	# result = cv2.addWeighted(image, 1, lane_image, 1, 0)
	
	# cv2.imwrite('tmp_all.png', result)
	
	result = lane_image
	
	return result


lanes = Lanes()

# 定义生成视频的保存路径
vid_output = 'proj_reg_vid_only_lane.mp4'

# 加载原始视频
clip1 = VideoFileClip("/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/video/project_video.mp4")

# 将预测图像生成GIF动画
vid_clip = clip1.fl_image(road_lines)
vid_clip.write_videofile(vid_output, audio=False)
