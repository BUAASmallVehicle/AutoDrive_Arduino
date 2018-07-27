# -*- coding:utf8 -*-
# 导入包
from scipy.optimize import fsolve, leastsq
from scipy.integrate import quad
from sympy import *
import numpy as np
import symbol
import math
import matplotlib.pyplot as plt

"""
特别注意：求投影点是通过迭代的方式来计算的，在计算时，要保证有着足够的空间来减少迭代产生的误差，
"""


## 坐标转换类
class coordinateTrans_xy_to_sq():
	'''
	从上游传回xy坐标、曲线信息
	'''
	
	def __init__(self, x, y, curve_xy):
		# TODO: 保证curve_xy是四次方程
		# 变量赋值
		self.curve_xy = curve_xy
		self.pt_x = x
		self.pt_y = y
		self.pt_pro_x, self.pt_pro_y = self.computing_porjectionPoint()
		self.pt_s = self.computing_s()
		self.pt_q = self.computing_q()
	
	# 计算投影点
	def function_for_projection(self, var):
		# 四次方程
		A = 4 * self.curve_xy[0]
		B = 3 * self.curve_xy[1]
		C = -4 * self.curve_xy[0] * self.pt_y
		D = 2 * self.curve_xy[2]
		E = -3 * self.curve_xy[1] * self.pt_y
		F = 1 - 2 * self.curve_xy[2] * self.pt_y
		G = self.curve_xy[3]
		H = -self.pt_x - self.curve_xy[3] * self.pt_y
		
		x = var[0]
		y = var[1]
		
		funs = [
			A * pow(x, 3) * y + B * pow(x, 2) * y + C * pow(x, 3) + D * x * y + E * pow(x, 2) + F * x + G * y + H,
			self.curve_xy[0] * pow(x, 4) + self.curve_xy[1] * pow(x, 3) + self.curve_xy[2] * pow(x, 2)
			+ self.curve_xy[3] * x + self.curve_xy[4] - y
		]
		
		return funs
	
	def computing_porjectionPoint(self):
		result = leastsq(self.function_for_projection, np.array([0, 0]))
		pt_pro_x = result[0][0]
		pt_pro_y = result[0][1]
		
		return [pt_pro_x, pt_pro_y]
	
	# 计算s
	def computing_s(self):
		# 曲线积分
		x = Symbol("x")
		fun = self.curve_xy[0] * (x ** 4) + self.curve_xy[1] * (x ** 3) + self.curve_xy[2] * (x ** 2) + self.curve_xy[
			3] * x + self.curve_xy[4]
		
		dy = diff(fun, x)
		f_curve_intg = (1 + expand(dy ** 2)) ** 0.5
		f_curve_intg = lambdify(x, f_curve_intg)
		
		tmp = quad(f_curve_intg, 0, self.pt_pro_x)
		
		s = abs(tmp[0])
		
		return s
	
	# 计算q
	def computing_q(self):
		q = math.sqrt((self.pt_x - self.pt_pro_x) ** 2 + (self.pt_y - self.pt_pro_y) ** 2)
		
		return q


## 测试
def test_coordinateTrans_xy_to_sq():
	curve_xy = np.array([6., 5., 4., 3., 2.]) * (10 ** (-3))
	print(curve_xy)
	
	x = 2.8874050026554485
	y = 0.5814178610196696
	
	# 得到s-q坐标
	Fernet = coordinateTrans_xy_to_sq(x, y, curve_xy)
	
	print(Fernet.pt_s)
	print(Fernet.pt_q)


if __name__ == '__main__':
	test_coordinateTrans_xy_to_sq()