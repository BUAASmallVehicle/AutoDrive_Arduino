# -*- coding:utf8 -*-
## 小车控制参数的抽象类
import abc

class control_parameters:
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod
	# 速度
	def get_velocity(self):
		return 0
	
	# 加速度
	def get_acceleratedSpeed(self):
		return 0
	
	# 转向角
	def get_steerAngle(self):
		return 0
