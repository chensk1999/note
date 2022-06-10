# 序贯模型

Sequential是若干线性堆叠的层构成的神经网络，其中每层输入输出都为一个张量

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 定义Sequential模型
model = keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation='relu'))   # 128节点的全连接层
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.summary()    # 查看每层的输入输出形状、总参数数量

# 加载训练数据集
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# mnist是手写数字数据集
# train_images是一个60000*28*28的numpy数组（60000张28*28的手写数字图片）
# train_labels是长度60000的numpy数组，代表图片中的数字
# test与train类似，不过只有10000张
x_train, x_test = x_train / 255.0, x_test / 255.0  # 转为0~1浮点数

# 指定训练配置：优化器、损失、指标
model.compile(optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'])

# 训练与验证模型
history = model.fit(train_images, train_labels, epochs=5)
result = model.evaluate(test_images, test_labels, verbose=2)

# 保存与加载模型
model.save('my_model')    # 创建my_model的文件夹，并将模型架构、权重、训练配置存进去
my_model = keras.models.load_model('my_model')
```

