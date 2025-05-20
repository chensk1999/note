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

