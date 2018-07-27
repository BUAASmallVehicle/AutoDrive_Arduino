# -*- coding:utf8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
## ------------------ ##
#  功能:将图像进行翻转   ##
## ------------------ ##

def rotation(image):
	# 保证image是一个灰度图
	assert(len(list(image.shape)) == 2)
	# 找出中心点
	w = image.shape[1]
	h = image.shape[0]
	center = (int(w/2), int(h/2))
	# 旋转缩放矩阵
	M = cv2.getRotationMatrix2D(center, -90, 1)
	rotated = cv2.warpAffine(image, M, (h, w))
	
	return rotated

def test_rotation():
	# 导入精灵王子
	elfPrince = cv2.imread('rotation_origin.jpg')
	
	# 灰度图
	im_gray = cv2.cvtColor(elfPrince, cv2.COLOR_BGR2GRAY)
	
	# 固定阈值二值化
	retval, elfPrince_at_fixed = cv2.threshold(im_gray, 50, 255, cv2.THRESH_BINARY)
	plt.imshow(elfPrince_at_fixed)
	
	# 旋转
	elfPrince_rota = rotation(elfPrince_at_fixed)
	plt.imshow(elfPrince_rota)
	
	pass
	
