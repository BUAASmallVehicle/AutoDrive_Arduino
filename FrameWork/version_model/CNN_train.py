# -*- coding: utf-8 -*-
"""
本部分使用keras构建一个CNN网络，用于车道线的识别.

特别注意，训练所使用的数据，由于github上传文件大小限制，需要自行下载，
放到/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network文件下.
"""

# 导入库
import numpy as np
import pickle
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Activation, Dropout, UpSampling2D
from keras.layers import Conv2DTranspose, Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras import regularizers


import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3' # 只显示 Error

### 导入训练集 ###
## 加载训练图片
train_images = pickle.load(open("/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_train.p", "rb" ))

## 加载训练图片标签
labels = pickle.load(open("/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_labels.p", "rb" ))

## 将加载的图片与label转化为数组形式，满足网络的输入需要
train_images = np.array(train_images)
labels = np.array(labels)

## 标准化标签数据
labels = labels / 255

## 将图像与标签一起随机打乱，然后分解为训练/验证集
train_images, labels = shuffle(train_images, labels)

## 将训练图片和标签进行训练集和测试集的划分，数据集样本占比设为10%
X_train, X_val, y_train, y_val = train_test_split(train_images, labels, test_size = 0.1)


### 搭建CNN网络 ###
## 设置参数
batch_size = 128    # 训练批量大小
epochs = 10         # 训练次数
pool_size = (2, 2)  # 池化大小
input_shape = X_train.shape[1 : ]   # 设置输入层的规模

## 搭建网络
# input layer
model = Sequential()
model.add(BatchNormalization(input_shape = input_shape))

# Conv layer 1
model.add(Conv2D(8, (3, 3), padding = 'valid', strides = (1, 1), activation = 'relu', name = 'Conv1'))

# Conv layer 2
model.add(Conv2D(16, (3, 3), padding = 'valid', strides = (1, 1), activation = 'relu', name = 'Conv2'))

# Pooling 1
model.add(MaxPooling2D(pool_size = pool_size))

# Conv layer 3
model.add(Conv2D(16, (3, 3), padding = 'valid', strides = (1, 1), activation = 'relu', name = 'Conv3'))
model.add(Dropout(0.2))

# Conv Layer 4
model.add(Conv2D(32, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv4'))
model.add(Dropout(0.2))

# Conv Layer 5
model.add(Conv2D(32, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv5'))
model.add(Dropout(0.2))

# Pooling 2
model.add(MaxPooling2D(pool_size=pool_size))

# Conv Layer 6
model.add(Conv2D(64, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv6'))
model.add(Dropout(0.2))

# Conv Layer 7
model.add(Conv2D(64, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv7'))
model.add(Dropout(0.2))

# Pooling 3
model.add(MaxPooling2D(pool_size=pool_size))

# Upsample 1
model.add(UpSampling2D(size=pool_size))

# Deconv 1
model.add(Conv2DTranspose(64, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Deconv1'))
model.add(Dropout(0.2))

# Deconv 2
model.add(Conv2DTranspose(64, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Deconv2'))
model.add(Dropout(0.2))

# Upsample 2
model.add(UpSampling2D(size=pool_size))

# Deconv 3
model.add(Conv2DTranspose(32, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Deconv3'))
model.add(Dropout(0.2))

# Deconv 4
model.add(Conv2DTranspose(32, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Deconv4'))
model.add(Dropout(0.2))

# Deconv 5
model.add(Conv2DTranspose(16, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Deconv5'))
model.add(Dropout(0.2))

# Upsample 3
model.add(UpSampling2D(size=pool_size))

# Deconv 6
model.add(Conv2DTranspose(16, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Deconv6'))

# 最终图层 - 仅包含一个通道，因此只有一个filter
model.add(Conv2DTranspose(1, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Final'))


### 训练网络 ###
## 使用ImageDataGenerator来生成一个批次的图像数据
datagen = ImageDataGenerator(channel_shift_range = 0.2)
datagen.fit(X_train)

## 训练模型
model.compile(optimizer = 'Adam', loss = 'mean_squared_error')
model.fit_generator(datagen.flow(X_train, y_train, batch_size = batch_size), steps_per_epoch = len(X_train)/batch_size,
                    epochs = epochs, verbose = 1, validation_data = (X_val, y_val))

## 训练完成后冻结网络层
model.trainable = False
model.compile(optimizer = 'Adam', loss = 'mean_squared_error')

## 保存训练好的模型为full_CNN_model.h5
model.save('/home/lhospital/MyProgramm/AutoDrive_Arduino/DataSource/Network/full_CNN_model.h5')

## 打印模型情况
model.summary()

