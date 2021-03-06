#-*-coding: utf-8 -*-
import numpy as np
import cv2
# import matplotlib.pyplot as plt
import math

## 阈值过滤
#
def abs_sobel_thresh(img, orient = 'x', thresh_min = 0, thresh_max = 255):
	# 转换为灰度图
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# 使用cv2.Sobel计算x方向、y方向的导数
	if orient == 'x':
		abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
	if orient == 'y':
		abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
	
	# 阈值过滤
	scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
	binary_output = np.zeros_like(scaled_sobel)
	binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
	
	return binary_output

#
def mag_thresh(img, sobel_kernel=3, mag_thresh=(0, 255)):
	# Convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# Take both Sobel x and y gradients
	sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
	sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
	# Calculate the gradient magnitude
	gradmag = np.sqrt(sobelx**2 + sobely**2)
	# Rescale to 8 bit
	scale_factor = np.max(gradmag)/255
	gradmag = (gradmag/scale_factor).astype(np.uint8)
	
	# Create a binary image of ones where threshold is met, zeros otherwise
	binary_output = np.zeros_like(gradmag)
	binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1
	
	# Return the binary image
	return binary_output


#
def hls_select(img, channel='s', thresh=(0, 255)):
	hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
	
	if channel == 'h':
		channel = hls[:, :, 0]
	elif channel == 'l':
		channel = hls[:, :, 1]
	else:
		channel = hls[:, :, 2]
	binary_output = np.zeros_like(channel)
	binary_output[(channel > thresh[0]) & (channel <= thresh[1])] = 1
	return binary_output

def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):
	# Grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	
	# Calculate the x and y gradients
	sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
	sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
	
	# Take the absolute value of the gradient direction,
	# apply a threshold, and create a binary image result
	absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
	binary_output =  np.zeros_like(absgraddir)
	binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1
	
	# Return the binary image
	return binary_output

def luv_select(img, thresh=(0, 255)):
	luv = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
	l_channel = luv[:,:,0]
	binary_output = np.zeros_like(l_channel)
	binary_output[(l_channel > thresh[0]) & (l_channel <= thresh[1])] = 1
	return binary_output

def lab_select(img, thresh=(0, 255)):
	lab = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
	b_channel = lab[:,:,2]
	binary_output = np.zeros_like(b_channel)
	binary_output[(b_channel > thresh[0]) & (b_channel <= thresh[1])] = 1
	return binary_output

# 组合过滤
def thresholding(img):
	x_thresh = abs_sobel_thresh(img, orient='x', thresh_min=10 ,thresh_max=230)
	m_thresh = mag_thresh(img, sobel_kernel=27, mag_thresh=(70, 100))
	dir_thresh = dir_threshold(img, sobel_kernel=27, thresh=(0.7, 1.3))
	hls_thresh = hls_select(img, thresh=(180, 255))
	lab_thresh = lab_select(img, thresh=(155, 200))
	luv_thresh = luv_select(img, thresh=(225, 255))
	
	# Thresholding combination
	threshholded = np.zeros_like(x_thresh)
	threshholded[((x_thresh == 1) & (m_thresh == 1)) | ((dir_thresh == 1) & (hls_thresh == 1)) | (lab_thresh == 1) | (luv_thresh == 1)] = 1

	return threshholded


## 透视变换
# 得到变形矩阵和逆变形矩阵
def get_M_Minv():
	'''
	src = np.float32([[(400, 720), (580, 380), (780, 380), (950, 720)]])
	dst = np.float32([[(320, 720), (320, 0), (960, 0), (960, 720)]])
	'''
	src = np.float32([[(100, 720), (400, 400), (900, 400), (1250, 720)]])
	dst = np.float32([[(320, 720), (320, 0), (960, 0), (960, 720)]])
	M = cv2.getPerspectiveTransform(src, dst)
	Minv = cv2.getPerspectiveTransform(dst,src)
	return [M,Minv]

## 车道线检测
def find_line(binary_warped):
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
	nwindows = 20
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
		if len(good_left_inds) > minpix and leftx_empty < 3:
			left_lane_inds.append(good_left_inds)
			leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
			if leftx_empty > 0:
				leftx_empty -= 1
		else:
			leftx_empty += 1
		
		if len(good_right_inds) > minpix and rightx_empty < 3:
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


## 计算车道线曲率和车距中心距离
def calculate_curv_and_pos(binary_warped, left_fit, right_fit):
	# Define y-value where we want radius of curvature
	ploty = np.linspace(0, binary_warped.shape[0] - 1, binary_warped.shape[0])
	leftx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
	rightx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]
	
	# Define conversions in x and y from pixels space to meters
	ym_per_pix = 30. / 720  # meters per pixel in y dimension
	xm_per_pix = 3.7 / 700  # meters per pixel in x dimension
	y_eval = np.max(ploty)
	
	# Fit new polynomials to x,y in world space
	left_fit_cr = np.polyfit(ploty * ym_per_pix, leftx * xm_per_pix, 2)
	right_fit_cr = np.polyfit(ploty * ym_per_pix, rightx * xm_per_pix, 2)
	
	# Calculate the new radii of curvature
	left_curverad = ((1 + (2 * left_fit_cr[0] * y_eval * ym_per_pix + left_fit_cr[1]) ** 2) ** 1.5) / np.absolute(
		2 * left_fit_cr[0])
	right_curverad = ((1 + (2 * right_fit_cr[0] * y_eval * ym_per_pix + right_fit_cr[1]) ** 2) ** 1.5) / np.absolute(
		2 * right_fit_cr[0])
	curvature = ((left_curverad + right_curverad) / 2)
	
	# Calculate the tangent
	left_tangent = 2 * left_fit_cr[0] * y_eval * ym_per_pix + left_fit_cr[1]
	right_tangent = 2 * right_fit_cr[0] * y_eval * ym_per_pix + right_fit_cr[1]
	tangent = ((left_tangent + right_tangent) / 2)
	theta = math.atan(tangent) + 90
	
	# print(curvature)
	lane_width = np.absolute(leftx[719] - rightx[719])
	lane_xm_per_pix = 3.7 / lane_width
	veh_pos = (((leftx[719] + rightx[719]) * lane_xm_per_pix) / 2.)
	cen_pos = ((binary_warped.shape[1] * lane_xm_per_pix) / 2.)
	distance_from_center = veh_pos - cen_pos
	return curvature, theta, -distance_from_center


## 还原
def draw_area(undist, binary_warped, Minv, left_fit, right_fit):
	# Generate x and y values for plotting
	ploty = np.linspace(0, binary_warped.shape[0] - 1, binary_warped.shape[0])
	left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
	right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]
	
	# Create an image to draw the lines on
	warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
	color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
	
	# Recast the x and y points into usable format for cv2.fillPoly()
	pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
	pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
	pts = np.hstack((pts_left, pts_right))
	
	# Draw the lane onto the warped blank image
	cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))
	
	# Warp the blank back to original image space using inverse perspective matrix (Minv)
	newwarp = cv2.warpPerspective(color_warp, Minv, (undist.shape[1], undist.shape[0]))
	
	# Combine the result with the original image
	result = cv2.addWeighted(undist, 1, newwarp, 0.3, 0)
	return result


### 主函数
if __name__ == '__main__':
	# 获取图像
	cap = cv2.VideoCapture(1)
	# cap.open('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/video/project_video.mp4')
	cap.set(3, 1280)
	cap.set(4, 720)
	
	while(1):
		img_org = cap.read()[1]
		img = img_org.copy()
		img_org_copy = img_org.copy()
		
		# 阈值过滤
		comb_thresh = hls_select(img, channel='l',thresh=(180, 255))
		
		# 透视变换
		M, Minv = get_M_Minv()
		binary_warped = cv2.warpPerspective(comb_thresh, M, img_org.shape[1::-1], flags = cv2.INTER_LINEAR)
		
		# 检测车道边线
		left_fit, right_fit, left_lane_inds, right_lane_inds = find_line(binary_warped)
		
		# print(left_fit, right_fit, left_lane_inds, right_lane_inds)
		
		# 计算
		curv, theta, dist = calculate_curv_and_pos(binary_warped, left_fit, right_fit)
		print(curv, theta, dist)
		
		# 还原
		img_result = draw_area(img_org_copy, binary_warped, Minv, left_fit, right_fit)
		
		
		cv2.imshow('lane', img_result)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	


