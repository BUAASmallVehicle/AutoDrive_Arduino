#-*-coding: utf-8 -*-
# 功能: 视觉模块的主入口

import numpy as np
import cv2
from FrameWork.version_model.lane_detection import *
from FrameWork.Nav_model.image_handle.overturn import *

# 调用摄像头
cap = cv2.VideoCapture(1)

model = load_model('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_model.h5')

# 透视变换矩阵
pts1 = np.float32([[69, 110], [99, 110], [70, 115], [113, 115]])
pts2 = np.float32(
	[[200, 115 - 3.73 * (113 - 70) / 1.75], [341, 115 - 3.73 * (113 - 70) / 1.75], [200, 431], [341, 431]])

M = cv2.getPerspectiveTransform(pts1, pts2)

# 循环获取图像
while(1):
	# get a frame
	ret, frame = cap.read()
	
	# 进行识别
	lanes_1d = road_lines(model, frame)
	output_1d = imresize(lanes_1d, (720, 1280, 1))
	
	# 进行转换
	# output = perspective(output)
	dst_img_tran = cv2.warpPerspective(output_1d, M, (500, 700))
	dst_img = imresize(dst_img_tran, (1280, 720, 3))
	
	# 进行翻转
	# dst_img = rotation(dst_img)
	
	# 输出图像
	cv2.imshow('lanes', output_1d)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
