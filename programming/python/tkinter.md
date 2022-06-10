# 基础知识

参考：[Tk Docs](https://tkdocs.com/tutorial/index.html)，[Tkinter 8.5 Reference](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html)

tkinter是跨平台gui工具包Tcl/Tk（更具体地说，Tcl是一种脚本语言，Tk是使用Tcl编写的gui框架，两者并称Tcl/Tk）的python接口（Tk interface）

```bash
python -m tkinter    # 检查是否安装tkinter，以及其版本
```

Tcl/Tk在安装python时一起安装。如果没有tkinter，需要重新安装python，并且在安装时勾选Tcl/Tk

## 例子

Tk包含三个基本要素：控件、几何管理与事件处理

```python
import tkinter as tk
from tkinter import ttk     # themed tk

# 根窗口
root = tk.Tk()

# 添加控件
frm = ttk.Frame(root, padding=10)
lbl = ttk.Label(frm, text="Hello World!")
btn = ttk.Button(frm, text="Quit", command=root.destroy)

# 几何管理
frm.grid()
lbl.grid(column=0, row=0)
btn.grid(column=0, row=1)

# 运行gui
root.mainloop()
```

# 控件

控件（widget）是gui的对象（比如，按钮、文本框、窗口）。控件呈树状，根节点为Tk实例。大部分控件都有`tkinter.widget`和`ttk.widget`两种，ttk比较新而且可以做的稍微好看一点点，除此之外区别不大

**基本**

| 种类     | 用途                                      |
| -------- | ----------------------------------------- |
| Spinbox  | 选择；上下箭头切换选项                    |
| Listbox  | 列表框；显示多个单行文本                  |
| Text     | 显示多行文本                              |
| Menu     | 菜单栏、下拉菜单和弹出菜单                |
| Toplevel | 窗口                                      |
| Canvas   | 画布，显示图形/图片，也是所有widget的父类 |

**显示内容**

| 种类        | 用途           |
| ----------- | -------------- |
| Frame       | 框架；用作容器 |
| LabelFrame  | 带标题的Frame  |
| Label       | 显示文本和位图 |
| Progressbar | 进度条         |

**输入**

| 种类        | 用途                                            |
| ----------- | ----------------------------------------------- |
| Button      | 按钮                                            |
| Checkbutton | 选择；在选项前打勾的单选框                      |
| Radiobutton | 单选按钮；类似Checkbutton，不过选项之间是互斥的 |
| Entry       | 输入文本                                        |
| Combobox    | 列表框；从下拉列表中选择一个                    |
| Scale       | 拉滚动条选择数值                                |

**特殊**

| 种类         | 用途                                                         |
| ------------ | ------------------------------------------------------------ |
| Scrollbar    | 滚动条，当内容超过可视化区域时使用，如列表框                 |
| Sizegrip     | 调整大小（小方块状，用鼠标拖动可以调整窗口大小）             |
| Seperator    | 分割线                                                       |
| PanedWindow  | 可以往里面放多个控件，然后在PanedWindow之内可以拖动各个控件的大小。使用add方法添加控件，orient参数控制摆放的方向 |
| Notebook     | 可以往里面放多个控件，选择一个显示。add(widget, text='title')添加控件 |
| Treeview     | 树状浏览器                                                   |
| Menubutton   | 显示菜单项                                                   |
| Message      | 显示多行文本，与label比较类似                                |
| tkMessageBox | 应用程序的消息框                                             |

## 配置控件

```python
# 用关键字参数初始化控件
btn1 = ttk.Button(root, text='Yes')

# 用参数名索引设置控件
btn2 = ttk.Button(root)
btn2['text'] = 'No'

# 使用configure方法设置（参数名索引和configure方法也可以用来获取参数值）
btn3 = ttk.Button(root)
btn3.configure(text='Cancel')
```

部分常用且通用的属性：

```python
lbl = ttk.Label(root)

# 尺寸
lbl['width'] = 350      # 350 pixels。'350'也是同样的效果
lbl['height'] = '400'   # 400 cm。其他后缀还有i（inch）、p（print points）

# 边框
lbl['relief'] = 'flat'   # 边框样式，其他还有raised, sunken, solid, ridge, groove
lbl['borderwidth'] = 20  # 边框宽度

# 显示文字/图像
lbl['text'] = 'Hello, world'                      # 显示文字
lbl['textvariable'] = tk.StringVar(root)          # 显示变量
lbl['image'] = tk.PhotoImage(file='example.jpg')  # 显示图片
lbl['compound'] = 'image'
    # 选择如何同时显示图像和文字。默认"none"，无图显示文字，有图只显示图片
    # center, top, left, bottom, right同时显示图片和文字，参数种类表示图片相对文字位置
    # text只显示文字，image只显示图片
lbl['anchor'] = tk.CENTER   # 文字/图片居中。其他还有N, W, NW等，与表示东南西北相同

# 获取尺寸
lbl.update()    # 尺寸改变后才需调用。如果有用到<Configure>事件，应该放在其回调函数内
lbl.winfo_height()
lbl.winfo_width()
```

tk & ttk的外观属性：tk使用控件属性来定义样式

```python
lbl = tk.Label('root')

lbl['background'] = 'black'   # 背景色
lbl['foreground'] = '#FF340A' # 前景色（文字的颜色）
lbl['font'] = ('Helvetica', 14)
```

ttk的外观属性：ttk使用`ttk.Style`定义样式

```python
s = ttk.Style()

# built-in styles
# 内建style名是widget.winfo_class()
s.configure('TLabel', foreground='green')
lbl = ttk.Label(root, style='TLabel')

# 继承style
s.configure('new.TLabel', foreground='maroon')
label_new = ttk.Label(root, style='new.TLabel')
```

## 控件用法

比较复杂，此处不抄文档了，仅列出部分示例代码。具体可以参考[这里](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html)的7~46节

### Canvas

```python
canvas = tk.Canvas(root)

# 绘制
line_id = canvas.create_line(0, 0, 10, 10, fill='red')
img = tk.PhotoImage(file='sample.jpg')
img_id = canvas.create_image(0, 0, image=img, anchor=tk.NW)

# 修改
canvas.itemconfigure(line_id, width=2)
canvas.coords(line_id, 0, 0)
canvas.delete(img_id)
```

### Menu

```python
# 创建根菜单并设置为窗口的菜单栏
menu_bar = tk.Menu(root)
root['menu'] = menu_bar

# 创建子菜单。此处仅列出一级菜单，二级、三级同理
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='File', menu=file_menu)

# 添加命令
file_menu.add_command(label='New', command=lambda: 0)

# 右键菜单（需要另外建一个menu。此处略去，直接用绑给root的菜单，实际代码不能这么做）
root.bind('<Button-3>', lambda e: menu_bar.post(e.x, e.y))
```

# 几何管理器

几何管理器控制各个控件的位置。所有控件都必须指定几何管理器，否则不会显示出来

## pack

pack是最简单的几何管理器，适合用于元素比较少的界面

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
buttons = [ttk.Button(root, text=str(i)) for i in range(0, 4)]

buttons[0].pack(side='top', expand=True)
buttons[1].pack(side='left', fill=tk.Y)
buttons[2].pack(side='top')
buttons[3].pack(side='top')

root.mainloop()
```

- side参数将可用空间分为两部分，并占据其中一块（比如说，第7行将整个窗口分为两部分，将`button[0]`放在上面的一块；第8行将剩余部分分为两块，`button[1]`占据左边，即整个窗口的左下部分）
- fill在指定的方向（水平`X`、垂直`Y`、全部`BOTH`）填充已分配的可用空间
- expand让几何管理器额外分配空间

上述代码应该会产生类似下图的gui

```
  ┌───┐
  │ 0 │
  └───┘
┌───┐┌───┐
│   ││ 2 │
│ 1 │└───┘
│   │┌───┐
│   ││ 3 │
└───┘└───┘
```

## grid

grid是最常用的几何管理器

```
grid()
    指定某个控件显示在父控件的哪个位置
    column, row
        格子的位置
    columnspan, rowspan
        跨行/列显示
    sticky='NSEW'
        当格子比控件大时，决定了控件粘在哪一边
        nsew四个字母中至少一个组成的字符串/字符列表
        没有时居中，一个方向或两个相邻方向，只粘在一边，相对方向，如'we'，则把控件拉大
    padx, pady
        在格子之间留白。padx相当于横向把格子中间留空，pady相当于纵向
        一个参数，在左右/上下留同样宽的空白；二元，不同宽度
    ipadx, ipady
        internal padding
        相对比较少用的方式。和padx, pady有微妙的差别
        例如一个20*20 + pad=5的控件，
        使用pad，会向几何管理器要20*20的空间，然后再周围围一圈空白
        用ipad，会要30*30空间，依据sticky决定怎么在这里面放下一个20*20的控件
columnconfiugre, rowconfigure(index, cnf={}, **kw)
    修改第index行/列的显示方式
    minsize 行/列的最小尺寸，表示相对值
    weight  窗口变大时，行/列相应变大的程度。默认为0，表示相对值
    pad     留空
grid_slaves(row=None, column=None)
    Return a list of all slaves of this widget in its packing order
grid_info()
    Return information about the options for positioning this widget in a grid
grid_configure(cnf={}, **kw)
    修改grid参数。关键字同grid方法
grid_remove()
    把控件从当前mapping中移除（仍然保留它的grid参数）

lift(aboveThis=None)
    把该widget堆叠到abouveThis之上/提高一层
lower(belowThis=None)
    把widget塞到底下，类似lift。它们也可以用于窗口次序的管理
focus_set()
    Direct input focus to this widget
focus()
    和focus_set基本相同
    treeview的focus方法能够指定item
focus_force()
    Direct input focus to this widget even if the application does not have the focus
    注：用在窗口上能够取得窗口的focus
```

## 其他

```python
btn = ttk.Button(text='example')

btn.place(x=0, y=0)   # 可以任意放置的几何管理器。很少使用
btn.forget()          # 把控件从当前mapping中移除。其几何管理器参数也会被删除
```

# 事件处理

将用户操作（事件）与控件绑定，就能对事件进行反应

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
label = ttk.Label(root, text='hello')
label.pack()
label.bind('<Button-1>', on_click)  # 当<Button-1>（鼠标左键点击）时，触发on_click函数
label.bind('<Button-1>', on_click2, add=True)
# 如果没有add=True，第二个绑定会覆盖掉前一个

def on_click(event):
    print(f'Click on x={event.x}, y={event.y}')

def on_click2(event):
    print(f'You clicked.')

root.mainloop()
```

上面例子中，回调函数`on_click`只能接受event参数，并且返回值无法被接收，因此很难用。更常用的做法是用类的继承实现回调函数

```python
class IncrementalLabel(ttk.Label):
    def __init__(self, parent):
        super(IncrementalLabel, self).__init__(parent, text='1')
        self.bind('<Button-1>', self.increment)

    def increment(self, event):
        n = int(self['text'])
        self['text'] = str(n + 1)
```

## 事件

事件用事件序列（Event Sequence）表示，比如`<Control-KeyPress-k>`。一个序列中可以包含多个事件，当它们同时发生时触发，比如上例子中同时按下Ctrl和K才能触发事件

**鼠标事件**

| event字符串          | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| `<Button-1>`         | 左键点击。也可以用`<ButtonPress-1>`或`<1>`。中、右键分别为2，3 |
| `<B1-Motion>`        | 拖动                                                         |
| `<ButtonRelease-1>`  | 松开                                                         |
| `<Double-Button-1>`  | 双击                                                         |
| `<MouseWheel>`       | 滚轮滚动。`event.delta`表示滚动距离                          |
| `<Enter>`, `<Leave>` | 鼠标进入 / 离开控件的范围                                    |
| `<Key>`              | 任一个键盘按键                                               |

**键盘事件**

例子：

- `e`表示按键E（注意，如果用了`E`，就需要Shift+E或者打开大写锁定才能触发）
- `<Escape>`表示Esc键
- `<Control-z>`表示Ctrl+Z

**其他事件**

| 事件序列                  | 说明|
| ------------------------- | ------------ |
| `<FocusIn>`, `<FocusOut>` | focus移动到控件 / 移出控件 |
| `<Configure>`             | 控件大小改变 |

详细列表可以参考[这里](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html)。event对象具体用法参考[这里](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/event-handlers.html)

## 方法

```
wait_variable(var)
    wait until the variable is modified
    参数必须是tkinter.Var
wait_window(window=None)
    wait until a WIDGET is destroyed
    if no parameter is given self is used
wait_visibility(window=None)
    wait until the visibility of a WIDGET changes.(e.g. it appears).
    if no parameter is given self is used
```

# 子模组

## 文件选择

```python
from tkinter import filedialog

filedialog.askopenfilename()
filedialog.asksaveasfilename(
    initialdir='.',
    initialfile='whatever.png',
    filetypes = (('png files','*.png'),)
)
filedialog.askdirectory()
#均返回一个完整的文件路径或空字符串
```

## 选色器

```python
from tkinter import colorchooser
```

## 信息窗口

```python
from tkinter import messagebox

choice = messagebox.showinfo(
    title='example',
    message='this is message',
    type='yesnocancel',
    	#ok, okcancel, yesno, yesnocancel, retrycancel, abortretryignore
    detail='this is detail',
    icon='info'
    	#"info" (default), "error", "question" or "warning"
)

print(choice)
```

# 图像

```python
from PIL import ImageTk, Image
img = ImageTk.PhotoImage(Image.open('myimage.png'))

# opencv图像（numpy数组）转PIL图像
cv_img = cv2.imread('example.png')
tk_img = ImageTk.PhotoImage(Image.fromarray(cv_img))
```

注意：一定要给`ImageTk`对象留一个索引，否则会被gc

# 其他

## Tk变量

```python
import tkinter as tk

root = tk.Tk()

# 定义tk变量
i = tk.IntVar(root, value=0)

# 访问tk变量
i.set(i.get() + 1)

# 回调函数。在变量被访问时调用
def callback(var_name, index, mode):
    var = tk.IntVar(var_name)    # 好像是个singleton
    print(f'{var_name} accessed: {mode}')   # mode = read, write, unset
i.trace_add('write', callback)

# 使用例
label = tk.Label(root, textvariable=i)
label.pack()
root.mainloop()
```

类似地，有`StringVar`，`IntVar`，`DoubleVar`，`BooleanVar`四种类型

## 杂项

```python
import tkinter

root = tkinter.Tk()
root.withdraw()           # 隐藏根菜单
root.clipboard_get()      # 操作剪贴板
```

