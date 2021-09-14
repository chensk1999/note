# 一个简单例子

```python
import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)  #Qt要求有一个applicaton
w = QtWidgets.QWidget()   #QWidget是一切控件的基础类
w.setWindowTitle('Example')
w.show()

sys.exit(app.exec_())   #开始主循环
```

# 面向对象

```python
import sys
from PyQt5 import QtWidgets, QtGui


class PromptText(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 设置提示框
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))  # 设置提示框的字体
        self.setToolTip('This is a <b>QWidget</b> widget')
        self.setGeometry(300, 100, 600, 600)
        self.setWindowIcon(QtGui.QIcon(t1.jpg))
        self.setWindowTitle('Tooltips')

        # 创建一个按钮并且设置其格式
        self.btn = QtWidgets.QPushButton('Button', self)
        self.btn.setToolTip('This is a <b>QPushButton</b> widget')  # 设置按钮提示框
        self.btn.resize(100, 50)
        self.btn.move(250, 500)
        
        # 绑定按钮的slot (Qt的signal触发slot)
        self.btn.clicked.connect(self.func)
        
    def func(self):
        # called when btn is clicked


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pt = PromptText()
    pt.show()
    sys.exit(app.exec_())
```

# 关闭事件以及QMessageBox

```python
from PyQt5.QtWidgets import QWidget, QMessageBox
class CloseConfirmWidget(QWidget):
    def closeEvent(self, event):
        # 覆盖默认的closeEvent，当关闭时被调用
        reply = QtWidgets.QMessageBox.question(
                self, 'title', 'prompt',
                QMessageBox.Yes | QMessageBox.No # 按钮的union
                QMessageBox.No   # 默认按钮
        )
        if reply == QMessageBox.Yes:
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
```



将设计文件转换为脚本

```
pyuic5 -o name.py name.ui
```

