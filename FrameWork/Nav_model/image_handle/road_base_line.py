import numpy as np
import matplotlib.pyplot as plt
import cv2
## ------------------ ##
#  功能:找出车道基准线   ##
## ------------------ ##

## -------------------------------------------------------  ##
# 本模块上游给的数据已经变为了我们想要的形式:                      ##
#  1. 车辆位置x = 0;                                          ##
#  2. 传来的数据为组合类型, 包括图像(np.array), 图像的长和宽(int); ##
#  3. 已经经过锐化处理, 路面对应位置的值大于200.                  ##
## -------------------------------------------------------  ##

## TODO: 将image_recognized变为上游传入的一个类
class road_base_line():
	# 构造函数
	def __init__(self, image_recognized):
		self.img = image_recognized
		self.curve_xy = self.get_curve()
	
	# 计算道路基准线
	def get_curve(self):
		# 得到图像的长和宽
		pixel_num_x = self.img.shape[1]
		pixel_num_y = self.img.shape[0]
		
		# 初始化拟合点集合
		fitting_pts = []
		
		# 采用路边线的中心点来作为拟合点
		for x in range(pixel_num_x):
			# 每隔30个像素取一个点
			if ((x + 1) % 30) == 0:
				# 找到中点
				p = list(np.where(self.img[:, x] >= 200)[0])
				if p != []:
					a = min(p)
					b = max(p)
					c = int((a + b)/2)
					fitting_pts.append([c, x])
					
		# 定义自变量x与因变量y
		x = np.array(fitting_pts).T[1]
		y = np.array(fitting_pts).T[0]
		
		# 拟合为四次方程
		fitting_curve = np.polyfit(x, y, 4)
		
		return fitting_curve
	
	# 画出中心线，当需要观察道路中心线时使用
	def draw_roadCenterLine(self):
		img_tmp = self.img.copy()
		# 得到图像的长和宽
		pixel_num_x = img_tmp.shape[1]
		pixel_num_y = img_tmp.shape[0]
		
		# 画出道路中心线
		for x in range(pixel_num_x):
			p = list(np.where(img_tmp[:, x] >= 200)[0])
			if p != []:
				a = min(p)
				b = max(p)
				c = int((a + b)/2)
				
				for j in range(c - 2, c + 2):
					img_tmp[j, x] = 127
					
		plt.imshow(img_tmp)
		plt.show()
		
		
def test_road_base_line_1():
	# 读入图像1
	map_road = cv2.imread('map_road_stright.png')
	map_road = np.array(map_road)
	
	roadBaseLine = road_base_line(map_road)
	
	# 打印各种数据
	print(roadBaseLine.curve_xy)
	roadBaseLine.draw_roadCenterLine()
	
	
def test_road_base_line_2():
	# 读入图像2
	map_road = cv2.imread('map_road_cur.png')
	map_road = np.array(map_road)
	
	roadBaseLine = road_base_line(map_road)
	
	# 打印各种数据
	print(roadBaseLine.curve_xy)
	roadBaseLine.draw_roadCenterLine()
	
		
		