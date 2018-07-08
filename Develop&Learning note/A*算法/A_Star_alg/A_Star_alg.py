# -*- coding: utf-8 -*-
import numpy as np
from .map_test import get_map

## 定义节点类
from numpy.core.multiarray import ndarray


class Node_Elem:
    """
    open与closed列表中存储的元素类型
    """
    def __init__(self, parent, x, y, dist):
        '''
        一个节点中有四个元素，分别为"父节点"、"x坐标"、"y坐标"、"从起点到当前点的距离"
        '''
        self.parent = parent
        self.x = x
        self.y = y
        self.dist = dist
      
    
## 定义A_Star类
class A_Star:
    def __init__(self, s_x, s_y, e_x, e_y, test_map, w=60, h=30):
        self.s_x = s_x
        self.s_y = s_y
        self.e_x = e_x
        self.e_y = e_y
        
        self.width = w
        self.height = h
        
        self.open = []
        self.close = []
        self.path = []
        
        self.test_map = test_map
        
    ## 路径查找
    def find_path(self):
        # 构建起始节点
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
    
        # 循环体
        while True:
            # 扩展当前节点
            self.extend_round(p)
        
            # 如果open set为空，则不存在路径，输出该信息
            if not self.open:
                print('没有路径存在!请检查地图是否正确\n')
                return -1
        
            # 获取open set中f(n)最小的点
            idx, p = self.get_best()
            
            # 如果p就是目标节点，则找到路径并生成路径
            if self.is_target(p):
                self.make_path(p)
                print('已经找到路径!')
                return 1
            
            # 如果p不是目标节点，则将该节点压如close set中，并从open set中删除该列表
            self.close.append(p)
            del self.open[idx]
        
    ## 生成路径
    def make_path(self, p):
        while p:
            self.path.append((p.x, p.y))
            p = p.parent
        
    ## 判断是否是目标点
    def is_target(self, pt):
        return pt.x == self.e_x and pt.y == self.e_y

    ## 获取open set中f(n)最小的点
    def get_best(self):
        best = None
        bv = 1000000000    # 该值随着地图的扩张而增大
        bi = -1         # 记录点在open set中的位置
    
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)   # 获取f(n)值
            if value < bv:
                best = i
                bv = value
                bi = idx
            
        return bi, best

    ## 获取f(n)值
    def get_dist(self, pt):
        '''
        这一部分是A\*算法的精华所在，即f(n) = g(n) + h(n)
        这里采用Manhattan距离作为h(n)
        '''
        g = pt.dist
        h = abs(pt.x - self.e_x) + abs(pt.y - self.e_y)
        
        return g + h

    ## 扩展节点
    def extend_round(self, pt):
        # 八方向扩展
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1,-1,-1,  0, 0,  1, 1, 1)
        
        for x, y in zip(xs, ys):
            new_x, new_y = x + pt.x, y + pt.y
            # 若是无效或者不可行走的区域，则忽略
            if not self.is_valid_coord(new_x, new_y):
                continue
                
            # 构造新的节点
            node = Node_Elem(pt, new_x, new_y, pt.dist + self.get_cost(pt.x, pt.y, new_x, new_y))
        
            # 若新节点在closed set，则忽略
            if self.node_in_close(node):
                continue
            # 若新节点不在closed set
            i = self.node_in_open(node)
            if i != -1:
                # 新节点在open set
                if self.open[i].dist > node.dist:
                    # 现在的路径到open[i]的距离小于原先的距离
                    self.open[i].parent = pt
                    self.open[i].dist = node.dist
                continue
        
            # 加入open set中
            self.open.append(node)
        
    ## 获取前进的代价
    def get_cost(self, x1, x2, y1, y2):
        # 上下直走代价为1, 斜走代价为1.4
        if x1 == x2 or y1 == y2:
            return 1.0
        return 1.4

    ## 判断是否在closed set中
    def node_in_close(self, node):
        for i in self.close:
            if node.x == i.x and node.y == i.y:
                return True
        return False

    ## 判断是否在open set中
    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

    ## 是否是障碍物
    def is_valid_coord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.test_map[y][x] != '#'
    
    ## 得到搜索路径
    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.close:
            l.append((i.x, i.y))
        return l
    
    
## 打印路径
def print_road(map, path):
    for pt in path:
        if map[pt[1]][pt[0]] != 'S' or map[pt[1]][pt[0]] != 'E':
            map[pt[1]][pt[0]] = 'o'
        
    for line in map:
        print(''.join(line))
    
    return 1


## 通过函数获取起点、终点和地图的相关信息
def before_searching(s_x, s_y, e_x, e_y, w=60, h=30):
    return s_x, s_y, e_x, e_y, w, h


## 将tm地图导入test_map
def tm_to_test_map(tm, test_map):
    for line in tm:
        test_map.append(list(line))


## 得到起点与终点
def get_start_XY(test_map):
    return get_symbol_XY('S', test_map)


def get_end_XY(test_map):
    return get_symbol_XY('E', test_map)


def get_symbol_XY(str, test_map):
    for y, line in enumerate(test_map):
        try:
            x = line.index(str)
            return x, y
        except:
            continue

## 得到地图的长宽
def get_map_wh(test_map):
    w = len(test_map[0])
    h = len(test_map)
    return w, h


## 测试
def test():
    test_map = []
    tm = get_map()
    tm_to_test_map(tm, test_map)
    print(len(test_map))
	
    s_x, s_y= get_start_XY(test_map)
    e_x, e_y = get_end_XY(test_map)

    print('起点：')
    print(s_x, s_y)

    print('终点：')
    print(e_x, e_y)

    ## 得到地图的长宽
    w, h = get_map_wh(test_map)
    print('地图长宽：')
    print(w, h)

    a_star = A_Star(s_x, s_y, e_x, e_y, test_map, w, h)
    a_star.find_path()
    searched = a_star.get_searched()
    path = a_star.path
    print(path)
    print_road(a_star.test_map, path)
    
