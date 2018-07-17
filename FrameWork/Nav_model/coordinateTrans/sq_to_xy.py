# 导入包
from scipy.optimize import fsolve, leastsq
from scipy.integrate import quad
from scipy.optimize import newton
from sympy import *
import numpy as np
import symbol
import math
import matplotlib.pyplot as plt


## 坐标转换类：从Fernet坐标系到笛卡尔坐标系
class coordinateTrans_sq_to_xy():
	'''
	从上游传回sq坐标，曲线信息(方程)
	'''
	
	def __init__(self, s, q, curve_xy):
		# 变量赋值
		self.curve_xy = curve_xy  # curve_xy是一个数组，表示拟合方程的系数和常数项(按幂降序)
		self.pt_s = s
		self.pt_q = q
		self.pt_x_proj, self.pt_y_proj = self.computing_projectionPoint()
		self.pt_x = self.computing_x()
		self.pt_y = self.computing_y()
	
	def computing_projectionPoint(self):
		## 定义f, df
		# 定义系数
		a = self.curve_xy[0]
		b = self.curve_xy[1]
		c = self.curve_xy[2]
		d = self.curve_xy[3]
		e = self.curve_xy[4]
		# 定义y(x)与y'(x)
		x = Symbol('x')
		yx = a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e
		dyx = diff(yx, x)
		yx = lambdify(x, yx)
		dyx = lambdify(x, dyx)
		
		# 定义df，即sqrt(1 + dy^2)
		def df(x):
			return math.sqrt(1 + (dyx(x) ** 2))
		
		# 定义f
		def f(x):
			result = quad(df, 0, x)
			return result[0] - self.pt_s
		
		# 牛顿法求解方程，即得出弧长为s对应的投影点，误差小于10^-6
		x_0 = newton(f, 0, df, tol=1e-6)
		
		# 通过x_0计算y_0
		y_0 = yx(x_0)
		
		return [x_0, y_0]
	
	## 计算x
	def computing_x(self):
		# TODO: 补充x的计算
		return 'null'
	
	## 计算y
	def computing_y(self):
		# TODO: 补充y的计算
		return 'null'


## 测试
def test_coordinateTrans_sq_to_xy():
	curve_xy = np.array([6., 5., 4., 3., 2.]) * (10 ** (-3))
	print(curve_xy)
	
	s = 3
	q = 5
	
	# 得到s-q坐标
	Descarts = coordinateTrans_sq_to_xy(s, q, curve_xy)
	
	print(Descarts.pt_x_proj)
	print(Descarts.pt_y_proj)


if __name__ == '__main__':
	test_coordinateTrans_sq_to_xy()