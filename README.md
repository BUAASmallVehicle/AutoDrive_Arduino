# AutoDrive_Arduino
This project will provide an auto driving ability for small vehicle controlled by Arduino.

## 1-Structure
将data与code独立开，data放入DataSource文件夹，工程的code放入FrameWork中. 

### 1.1-DataSource
All the data in our project, include train-set and test-set which used in object recognition and maps used in Nav, should be saved in this file container. 

本部分存放各类数据，主要包括视觉识别部分的数据集、地图数据等.


### 1.2-FrameWork
整个工程分为三个部分: vehicle_control, version_model与Nav_model. 

#### vehicle_control
负责与小车、传感器进行交互, 运行在Arduino控制板上, 需要完成的任务包括**车辆姿态判断/控制, 超声雷达测距, 摄像头回传数据, 前进/后退, 转向**等. 

能够将车辆姿态、与障碍物距离数据传给路径规划模块，能够将摄像头获取的图像传给version_model模块. 

#### version_model
视觉识别模块，需要完成的任务包括：
1. 车道线识别
2. 障碍物识别
3. 局部地图绘制

运行在TX2开发板上, 能够实时绘制出车辆周围的地图, 并将该信息传给路径规划模块. 

#### Nav_model
路径规划模块，包括**车辆定位, 全局路径规划, 局部路径规划**三部分. 运行在TX2开发板上, 接收map数据(DataSource中的全局Map, version_model实时绘制的local_map)与车辆姿态信息(速度、角度、与障碍物的距离等). 

车辆定位要求能够根据确定车在当前地图中的位置; 全局路径规划要求能够根据全局地图规划出一条从起点到终点的路径； 局部路径规划要求能够使车沿着车道线前进, 根据当前车的姿态, 选择合适的路线避开障碍物/停车防止碰撞. 