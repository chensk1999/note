# 基础例子

## 图像基本操作

```python
import cv2
# 不知道为什么语法检查有时候提示有问题，把import语句改成from cv2 import cv2就好了
import numpy as np

#读取图片。读出来的是一个numpy.ndarray
color_img = cv2.imread('test.jpg')
print(color_img.shape)      #(640, 640, 3)

#存储图片。由于jpg格式限制，灰度图会被还原成三通道
cv2.imwrite('test_grayscale.jpg', gray_img)

#裁剪图片
img_slice = img[20:150, -180:-50]

#缩放图片。可以用interpolation=cv2.INTER_NEAREST，不进行插值
img_200x200 = cv2.resize(color_img, (width, height))
#扩张图片。例中将图片上下扩张50像素
img_300x200 = cv2.copyMakeBorder(img_200x200, 50, 50, 0, 0,
                                 cv2.BORDER_CONSTANT,
                                 value=(0, 0, 0))

#拼接图片（利用numpy的矩阵拼接）
img_conc = np.concatenate((img1,img2), axis=0)

#二值化
cv2.threshold(src=img, thresh=127, maxval=255, type=cv2.THRESH_BINARY)
```

# 读取图片

```python
#读取灰度图
gray_img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)

# 读取带alpha通道的图
alpha_img = cv2.imread('test.png', cv2.IMREAD_UNCHANGED)
```



# 绘制形状

```python
import cv2
import numpy as np

canvas = np.zeros((400, 600, 3), dtype=np.uint8) + 255

#绘制直线。参数：画布，起点，终点，颜色，线宽
cv2.line(canvas, (300, 0), (300, 399), (0, 0, 0), 2)

#绘制圆。参数：圆心，半径，颜色，线宽（负数表示填充）
cv2.circle(canvas, (200, 300), 75, (0, 0, 255), 5)

#绘制长方形。参数：左上角端点，右下角端点，颜色，线宽
cv2.rectangle(canvas, (20, 240), (100, 360), (255, 0, 0), 3)

triangles = np.array([
    [(200, 240), (145, 333), (255, 333)],
    [(60, 180), (20, 237), (100, 237)]])
#绘制多边形。参数：多边形列表，是否闭合，颜色，线宽
cv2.polylines(img,[pts],True,(0,255,255), 2)
#填充多边形。参数：多边形列表，颜色
cv2.fillPoly(canvas, triangles, (0, 255, 0))

#添加文字
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
```

## GUI

```python
import cv2
img = cv2.imread('test.jpg')

#键盘事件
key = 0
while key != 27:   # esc退出
    cv2.imshow('image', img)
    key = cv2.waitKey()

#鼠标事件：先定义回调函数，然后绑定到窗口
def on_mouse(event, x, y, flags, param):
    #可以在这里做出操作，但是没办法传递返回值。目前没找到比global更好的方法
    events = [
        cv2.EVENT_LBUTTONDOWN,
        cv2.EVENT_LBUTTONUP,
        cv2.EVENT_LBUTTONDBCLICK  #中键（MBUTTON），右键（RBUTTON）同理
        cv2.EVENT_MOUSEMOVE
    ]
cv2.namedWindow('image')
cv2.setMouseCallback('image', on_mouse)
key = 0
while key != 27:
    cv2.imshow('image', img)
    key = cv2.waitKey()
cv2.destroyAllWindows()

#滑条
cv2.namedwindow('window')
cv2.createTrackbar('name', 'window', min_value, max_value, func)
    #取[min, max]区间整数。当滑条改变时，func被调用，传入一个参数（滑条值）
#设置/读取滑条的值
cv2.setTrackbarValue('name', 'window', value)
cv2.getTrackbarValue('name', 'window')
while True:
    cv2.imshow('window', img)
    cv2.waitKey(1)    #因为要不断更新窗口，每隔1ms就重新show一次
    bar = cv2.getTrackbarPos('name','window')

#关闭窗口
cv2.destroyWindow(winname)
cv2.destroyAllWindows()
```

