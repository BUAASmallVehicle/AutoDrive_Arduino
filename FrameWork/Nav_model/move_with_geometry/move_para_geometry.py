## 提供接口来使小车控制程序获取数据
import math
import numpy as np
from sympy import Symbol, diff, lambdify
from FrameWork.Nav_model.vehicle_control_para.control_parameters import control_parameters
from FrameWork.Nav_model.coordinateTrans.sq_to_xy import coordinateTrans_sq_to_xy

class move_para_geometry(control_parameters):
	def __init__(self, d, curve_xy):
		self.d = d
		self.curve_xy = curve_xy
		self.steerAngle = self.get_steerAngle()
		
	# 获取转向角
	def get_steerAngle(self):
		# 构造曲线方程
		x = Symbol('x')
		yx = self.curve_xy[0] * x ** 4 + \
			 self.curve_xy[1] * x ** 3 + \
			 self.curve_xy[2] * x ** 2 + \
			 self.curve_xy[3] * x + \
			 self.curve_xy[4]
		dyx = diff(yx, x)
		
		def curve(x):
			# 定义系数
			a = self.curve_xy[0]
			b = self.curve_xy[1]
			c = self.curve_xy[2]
			d = self.curve_xy[3]
			e = self.curve_xy[4]
			
			return a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e
		
		# 计算Fernet坐标系下(d, 0)位置的Descarts坐标
		Descarts = coordinateTrans_sq_to_xy(self.d, 0, self.curve_xy)
		
		x_pre = Descarts.pt_x_proj
		y_pre = Descarts.pt_y_proj
		
		# 计算斜率
		dyx = lambdify(x, dyx)
		k = dyx(x_pre)
		theta = math.atan(k)
		
		return (theta*180)/3.1415926
	
def test_move_para_geometry():
	curve_xy = np.array([6., 5., 4., 3., 2.]) * (10 ** (-3))
	d = 5
	
	steerAngle = move_para_geometry(d, curve_xy).steerAngle
	
	print(steerAngle)
	
if __name__ == '__main__':
	test_move_para_geometry()
	
	
	
	