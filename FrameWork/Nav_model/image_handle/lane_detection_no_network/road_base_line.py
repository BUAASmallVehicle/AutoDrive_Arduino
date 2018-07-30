#-*-coding: utf-8 -*-
import numpy as np
import cv2
# import matplotlib.pyplot as plt
import math

## 左右车道线检测
def find_line(binary_warped):
	"""
	通过阈值过滤后的图像对左右车道线建模
	:param binary_warped: 阈值过滤后的图像信息
	:return:
		left_fit, right_fit 左右车道线拟合曲线系数
	"""
	# Take a histogram of the bottom half of the image
	histogram = np.sum(binary_warped[binary_warped.shape[0] // 2:, :], axis=0)
	
	# print(histogram.shape)
	# plt.plot(range(1280), histogram)
	
	# Find the peak of the left and right halves of the histogram
	# These will be the starting point for the left and right lines
	midpoint = np.int(histogram.shape[0] / 2)
	leftx_base = np.argmax(histogram[:midpoint])
	rightx_base = np.argmax(histogram[midpoint:]) + midpoint
	lane_weight_px = rightx_base - leftx_base
	
	# Choose the number of sliding windows
	nwindows = 9
	# Set height of windows
	window_height = np.int(binary_warped.shape[0] / nwindows)
	# Identify the x and y positions of all nonzero pixels in the image
	nonzero = binary_warped.nonzero()
	nonzeroy = np.array(nonzero[0])
	nonzerox = np.array(nonzero[1])
	# Current positions to be updated for each window
	leftx_current = leftx_base
	rightx_current = rightx_base
	# Set the width of the windows +/- margin
	margin = 150
	# Set minimum number of pixels found to recenter window
	minpix = 20
	# Create empty lists to receive left and right lane pixel indices
	left_lane_inds = []
	right_lane_inds = []
	
	# 防止弯道情况的指标初始化
	leftx_empty = 0
	rightx_empty = 0
	# Step through the windows one by one
	for window in range(nwindows):
		# Identify window boundaries in x and y (and right and left)
		win_y_low = binary_warped.shape[0] - (window + 1) * window_height
		win_y_high = binary_warped.shape[0] - window * window_height
		win_xleft_low = leftx_current - margin
		win_xleft_high = leftx_current + margin
		win_xright_low = rightx_current - margin
		win_xright_high = rightx_current + margin
		
		'''
		# 观察选取的框
		img_show = plt.imshow(binary_wraped)
		currentAxis = plt.gca()
		rect = patches.Rectangle((win_xleft_low, win_y_low), 2 * margin, window_height, linewidth=1, edgecolor='r',
		                         facecolor='none')
		currentAxis.add_patch(rect)

		img_show = plt.imshow(binary_wraped)
		currentAxis = plt.gca()
		rect = patches.Rectangle((win_xright_low, win_y_low), 2 * margin, window_height, linewidth=1, edgecolor='r',
		                         facecolor='none')
		currentAxis.add_patch(rect)
		'''
		# Identify the nonzero pixels in x and y within the window
		good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
		                  (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
		good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
		                   (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
		# Append these indices to the lists
		
		# If you found > minpix pixels, recenter next window on their mean position
		if len(good_left_inds) > minpix and leftx_empty < 5:
			left_lane_inds.append(good_left_inds)
			leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
			if leftx_empty > 0:
				leftx_empty -= 1
		else:
			leftx_empty += 1
		
		if len(good_right_inds) > minpix and rightx_empty < 5:
			right_lane_inds.append(good_right_inds)
			rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
			if rightx_empty > 0:
				rightx_empty -= 1
		else:
			rightx_empty += 1
	
	# print(leftx_current, rightx_current)
	
	# Concatenate the arrays of indices
	if left_lane_inds != [] and right_lane_inds != []:
		left_lane_inds = np.concatenate(left_lane_inds)
		right_lane_inds = np.concatenate(right_lane_inds)
		leftx = nonzerox[left_lane_inds]
		lefty = nonzeroy[left_lane_inds]
		rightx = nonzerox[right_lane_inds]
		righty = nonzeroy[right_lane_inds]
	elif left_lane_inds == [] and right_lane_inds != []:
		right_lane_inds = np.concatenate(right_lane_inds)
		rightx = nonzerox[right_lane_inds]
		righty = nonzeroy[right_lane_inds]
		leftx = rightx - lane_weight_px
		lefty = righty
	elif left_lane_inds != [] and right_lane_inds == []:
		left_lane_inds = np.concatenate(left_lane_inds)
		leftx = nonzerox[left_lane_inds]
		lefty = nonzeroy[left_lane_inds]
		rightx = leftx + lane_weight_px
		righty = lefty
	else:
		print('No lane line in here!')
	# Extract left and right line pixel positions
	
	# Fit a second order polynomial to each
	left_fit = np.polyfit(lefty, leftx, 2)
	right_fit = np.polyfit(righty, rightx, 2)
	
	'''
	plt.plot(lefty, leftx, 'o')
	left_fitx = left_fit[0]*lefty**2 + left_fit[1]*lefty + left_fit[2]
	plt.plot(lefty, left_fitx)

	plt.plot(righty, rightx, 'o')
	right_fitx = right_fit[0]*righty**2 + right_fit[1]*righty + right_fit[2]
	plt.plot(righty, right_fitx)
	'''
	
	return left_fit, right_fit, left_lane_inds, right_lane_inds


