# 基本例子

```python
import tkinter as tk
from tkinter import ttk
```

# 基础知识

Tcl的控件是树状的，根窗口为Tk实例，各种控件如同windows的文件一样树状排布
三个基本要素：widgets, geometry management, and event handling

## themed widgets

```
基本
    Frame       框架；在屏幕上显示一个矩形区域，多用来作为容器
    LabelFrame  带标题的Frame

接受输入
    Button      按钮
    Checkbutton 选择；在选项前打勾的单选框
    Radiobutton 单选按钮；类似Checkbutton，不过选项之间是互斥的
    Entry       输入文本
    Combobox    列表框；从下拉列表中选择一个
    Scale       拉滚动条选择数值

显示
    Label       标签；显示文本和位图
    Progressbar 进度条

特殊
    Scrollbar   滚动条控件，当内容超过可视化区域时使用，如列表框
    Sizegrip    调整大小(小方块状，用鼠标拖动可以调整窗口大小)
    Seperator   分割线
    PanedWindow 可以往里面放多个控件，然后在PanedWindow之内可以拖动各个控件的大小
                使用add方法添加控件，orient参数控制摆放的方向
    Notebook    可以往里面放多个控件，选择一个显示
                add(widget, text='title')添加控件
    Treeview    树状浏览器
    Menubutton  菜单按钮控件，用于显示菜单项
    Message     消息控件；用来显示多行文本，与label比较类似
    tkMessageBox用于显示你应用程序的消息框
```



## widgets

```
显示
    Spinbox     选择；上下箭头切换选项
    Listbox     列表框；显示多个单行字符串
    Text        显示多行文本

窗口与菜单
    Menu        菜单控件；显示菜单栏,下拉菜单和弹出菜单
    Toplevel    提供一个单独的对话框

特别
    Canvas      画布，显示图形/图片
```



## toplevel

```
title()          设置标题
bind()           把事件绑定到主窗口
mainloop()       循环事件，在最后加上mainloop才会运行gui
after(ms, func)  隔一定时间就执行一次
update()         刷新
update_idletasks 刷新各种显示，但是不会处理event
```



## 全局变量

```
StringVar, IntVar, DoubleVar, BooleanVar
**属性**
    get     获取
    set     设置
```



# widget

大部分控件都有tkinter.widget和ttk.widget两种
使用方法基本没有差异，最大的差异在于：tkinter.widget使用很多个属性来定义样式，
ttk.widget使用style属性定义样式
ttk的往往比较美观

padding的几种方法：
1. 有的控件，比如frame，自身就有padding属性。控件向里留了一段空白
2. grid方法的padx, pady参数。在控件的左右/上下留一段空白
3. grid方法的ipanx, ipady参数。与2的差别详见grid方法
4. columnconfigure, rowconfigure方法的pad参数。在某一行的上下/某一列的左右留空白


## 通用的使用方法

### 初始化

```
ttk.Widget(master, **kw)
keywords : attribute = value
e.g. text='Hello'

widget['attr']查看属性（好像也可以直接修改，不通过configure方法）
str(widget)返回该控件的路径
```

### 属性

大部分属性都能通过configure属性来设置/获取，有的也可以通过instance['attribute']获取

#### 样式

```
width, height   宽度，高度。不指定就会由geometry manager自动分配
                '350'=350 pixels, '350i'=350 inches, '350c'=350 cm, '350p'=350 printer's points
    padding         四周留白宽度。一个数字=四周，二元tuple=横向纵向， 四元素tuple=左上右下
    borderwidth     边框宽度
    relief          边框样式，"flat" (default), "raised", "sunken", "solid", "ridge", or "groove"
    sytle           风格
```

#### 显示内容

```
    text            显示的文字
    textvariable    实时改变的文字变量(实时显示/即时获取输入)
    image           显示图片(PhotoImage实例)，空字符串''表示清除图片
    compound        混合显示图片和文字。默认"none"（无图显示文字，有图只显示图片）
                只显示某一种："text", "textvariable", "image"
                同时显示时规定图片位置："center", "top", "left", "bottom", "right".
    anchor          文字在label中显示的位置（当geometry manager给的空间大于必须用到的空间时）
                "n", "ne", "e", "se", "s", "sw", "w", "nw" or "center"
    justify         类似anchor， 当文字有多行时更好用。"left", "center" or "right"`
```
#### 交互

```
    command         按钮被按下时执行的指令
```

### 方法

#### 控件状态

```
configure()
    获取/修改控件的属性
    None        包含所有信息的dict
    'text'      包含text属性信息的tuple
    text='x'    将text属性修改为'x'
state(statespec=None)
    查询/修改控件的状态(themed widgets only)
    statespec应该是一个list(e.g. ['disabled'])
    '!state'表示清除某个状态flag（好像不完全是这样）
    "active", "disabled", "focus", "pressed", "selected",
    "background", "readonly", "alternate", and "invalid"
instate(statespec, callback=None, *args, **kw)
    查询控件状态并执行相应指令(themed widgets only)
    如果callback = None，查询控件是否在statespec状态
    否则，当控件在statespec状态时执行指令（以args和kw为参数）
iconify()
    Display widget as icon
```



#### 几何管理器

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

place(**kw)
    geometry manager，直接控制把控件放在哪个位置
pack(**kw)
    geometry manager
forget()
    把控件从当前mapping中移除。其几何管理器参数也会被删除
```

#### 其他方法

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

bind(sequence=None, func=None, add=None)
    把事件-操作关系绑定给控件
    sequence    表示事件的str
    func        事件发生时调用它；如果返回值时'break‘， 则阻止后续其他bind
    add         布尔值，specifies whether FUNC will be called
                additionally to the other bound function or
                whether it will replace the previous function
bind_class(self, className, sequence=None, func=None, add=None)
    绑定给整个class
bind_all()
    绑定给全部控件
依据绑定的位置不同，有五种不同优先级的event handler，从高到低为
application level   bind_all
top level           root.bind
class level         bindIclass
instance level      widget.bind
item level          widget.bind_tag
触发事件时，从最低级开始，到为止，每个等级选择一个
最符合的event handler执行
```



## Button

### 属性

​        state
​        if 'disabled' in state : 不能选择

​        default     默认为normal，若调整为active，会使用系统默认的按钮样式

### 方法

​        invoke()
​            invoke the command callback of the button

## Canvas

### 属性

​        scrollregion    画布大小

### 方法

```
create_line(x1, y1, ..., xn, yn, **kw)
    画出(x1, y1)到(x2, y2)...一直到(xn, yn)的折线段，x, y为横，纵轴，左上角为原点
    返回对象的id，可以用在tag_bind等处
    部分kw：
    fill    颜色
    width   线的粗细
    tags    标签，可以是str/int或其tuple，可以在以后方便地引用/批量处理
create_rectangale(x1, x2, y1, y2)
    类似create_line，画一个长方形，坐标也可以用一个tuple装着
create_image(position, **options)
    anchor
    image
    tags

addtag  添加标签
dtags   删除标签
gettags 获得某个id的标签
find    获得有某个标签的所有物品id
    以上四个方法的参数说明：
    若干各标签， ‘withtag', 若干个标签
    例如，addtag('tag1', 'withtag', 1)表示向带有标签1（即id=1）的物品添加标签'tag1'
    find('withtag', 'draw')表示返回所有带有标签'draw'的物品（也可以用find_withtag）
    addtag和find还有其他的特殊意义的标签

delete(id)  删除物品
coords      改变物品的坐标，参数同创建物品时的参数，返回新的坐标
move        移动物品
raise
lower       更改堆叠次序
```



## Checkbutton

### 属性

        variable    每当按钮被点击时会改变
        onvalue     被选中时的值，默认为'1'
        offvalue    没有被选中时的值，默认为'0'
        当variable既不是on value又不是off value时，state flag 'alternate' is set
        可以用instate方法把它改回来

### 方法
        select
        deselect    仅限tk，ttk直接设置variable

## Combobox

    Combobox会产生一个&lt;ComboboxSelected&gt;虚拟事件，可以把它绑定给控件
    widget.bind('&lt;&lt;ComboboxSelected&gt;&gt;', function)

### 属性

        textvariable    被选中的选项会即时地赋值给textvariable，代表Combobox的值
        values          选项列表

### 方法

        get     get current value
        set
        current(newindex=None)  如果有newindex，把当前值改为newindex选项的
                                否则，返回当前被选中的项目的index
                                如果当前值不在values中，返回-1

## Entry

    if 'readonly' in state : 不能输入，但还能复制
    if 'invalid' in state : 变灰色


<attribute>
    textvariable    输入内容会即时地赋值给textvariable
    show            当show!=''时，显示show而不是输入的文本（如密码显示成*号）
</attribute>
<method>
    delete(first, last=None)    删除index = [first,last]区间的字符(0-based)
    insert(index, string)       在index处插入string
</method>

</class>

## Label

标签可以直接用font, foreground, background属性来修改样式。当某个
样式只需要使用一次时，这比使用sytle要方便
TkDefaultFont       The default for all GUI items not otherwise specified.
TkTextFont          Used for entry widgets, listboxes, etc.
TkFixedFont         A standard fixed-width font.
TkMenuFont          The font used for menu items.
TkHeadingFont       The font typically used for column headings in lists and tables.
TkCaptionFont       A font for window and dialog caption bars.
TkSmallCaptionFont  A smaller caption font for subwindows or tool dialogs
TkIconFont          A font for icon captions.
TkTooltipFont       A font for tooltips.

foreground（字体颜色）和background参数
color names (e.g. "red") or hex RGB codes (e.g. "#ff340a")

## Menu

```
import tkinter as tk
from tkinter import ttk
```

    使用流程：
    root.option_add('*tearOff', False)  #不清楚有什么用，好像是排版不会乱
    创建一个tkinter.Menu实例作为根菜单
    窗口['menu'] = 菜单实例（注意：Menu实例的parent并不重要，一个menubar也可以被重复使用）
    创建更多的Menu实例，并用add_cascade和add_command指定它们的层次和功用
    <attribute>
    </attribute>
    <method>
        add_cascade
            附加一个子菜单(cascade)，注：子菜单在别处定义，可以重复使用
            menu = Menu实例
            label = 子菜单名
        add_command
            增加一个命令(command)
            label = 操作名
            command = 操作
        add_separator
            增加一个分割线
        add_checkbutton
            打勾的选项
            label
            checkbutton的各种参数
        add_radiobutton
            多选一的选项，参数同radiobutton
        insert
            index = 插入位置
            itemType = 种类（'cascade', 'command', and so on)
            cnf = {设置（如label）}
        delete
            index1, [index2]，删除index1（或1和2中间）的cascade(s) and
            command(s)，包含两端
        post(x, y)
            在(x, y)展开一个菜单（例如右键打开菜单）
    </method>
</class>

## Progressbar

    <attribute>
        orient      "horizontal" or "vertical"
        length      好像只能用像素数
        mode        'determinate'显示已完成多少，'indeterminate'不显示完成多少，只在不停滚动
        maximun     determinate进度条的总量，默认为100
        value       determinate进度条已经完成的量
        variable    如果绑定了，则以它来实时更新进度条
    </attribute>
    <method>
        step(amount=1.0)    增加进度条
        start(interval=50)  自动滚动进度条，每次1%，每过interval毫秒一次
    </method>
</class>

## Radiobutton

    <attribute>
        variable    同一组radiobutton共享同一个全局变量variable
        value       当被选中时，把value赋值给variable；同时充当on value
## Scale

​    <attribute>
​        length      像素数
​        from_
​        to          选择范围上下界。注意from是保留词，故用from_
​        resolution  选择的精度，默认为1，即只能选整数
​    </attribute>
​    <method>
​        set         设置
​        get         获得
​    </method>

## Scrollbar

    ttk.Scrollbar(parent, orient, command)
        parent  被scrollbar拖动的控件
        orient  scrollbar的方向，'vertical' or 'horizontal'
        command 用来控制被拖动控件的函数。widget.yview(纵向)或xview(横向)
                必须有这个方法才能被拖动
    
    被拖动物体的configure方法中，把yscrollcommand, xscrollcommand属性设置
    为scrollbar.set
    
    scrollbar通过scrollbar['command']告诉parent显示那些部分，
    parent通过parent['yscrollconfigure']告诉scrollbar自己正在显示哪些部分

## Toplevel

一个新窗口。实例被创建的同时打开窗口
它的方法应该都是针对窗口的，可以直接应用于根窗口

### 方法

```
destroy()   关闭窗口
title()     修改窗口标题
geometry()  调整窗口大小，参数形如'300x200-5+40'
            宽度*高度±窗口边缘到屏幕边缘的距离，正为到左/上边的距离，负为到右/下边的距离
resizable(width=None, height=None)
            参数为布尔值，指定能够调整大小
minsize()   最小尺寸，返回值为(width, hight)
maxsize()   最大尺寸
```



## Treeview

```
columns     展示内容时每一列的名称
show        tree显示首列，headings显示其他列，默认"tree headings"
displaycolumn  被显示的列的list，'#all'指代全部
selectmode  'extended' default, 'browse' 一次只能选一个, 'none' 不能选择
             注意：只限制了用户选择的能力，仍然可以用指令选择
```

### 方法

```
insert(parent, index, iid=None, **kw)
    将一个新节点插入到树中，返回其id
    parent = 父节点的id，None生成新树
    index = 在兄弟中排第几，小于等于0/大于等于最大则排在最前/最后，'end'也排最后
    iid 如果指定并且没有被占用，就作为这个节点的id（可以用字符串）
    部分keywords : text    展示时显示的文本
move(src, dest, index)
    将一个节点/子树/树嫁接到另一处
    src, dest同样都是item identifier，index意义同insert方法
detach(*items)
    将枝叶剪下来。还可以用move接回去
delete(*items)
    销毁掉item以及所有decendants
    如果items直接用一个list好像会出一些奇怪的问题
item(item, option=None, **kw)
    类似configure方法，查询/设置树的性质。部分选项：
    text    文字
    values  显示在列中的信息
    tags    不确定，可以用来设置显示格式
    open    当前分支是否展开
            把要选出来的设置为True,查询就能够直接得到筛选后的结果

parent(item)    返回父节点id
prev(item)      返回上一个sibling的id
next(item)      返回下一个sibling的id
get_children    返回子节点的id的list

column(column, option=None, **kw)
    设置列显示的选项，部分参数示例：
    width=100, anchor='center'
    values  把指定值按顺序填充进这一列
    默认的一列（即显示text的一列）可以用'#0'引用
heading(column, option=None, **kw)
    设置每一列最顶上那个条，可用参数：
    text    显示的文字
    image   图片
    anchor  Specifies how the heading text should be aligned.
    command 被点击时的操作
set(item, column=None, value=None)
    设置/获取单个column显示的内容

selection()
    返回被选中的item的tuple
selection_add(*items)
selection_set(*items)
selection_remove(*items)
tag_bind(tagname, sequence=None, callback=None)
    把指令绑定到树中某个节点

identify_row(event.y)
    返回相应行
```

# 事件

## 鼠标事件

| <event字符串>（尖括号均省略） | 说明                                                   |
| ----------------------------- | ------------------------------------------------------ |
| Button-1                      | 左键点击。也可以用ButtonPress-1或1。中、右键分别为2，3 |
| B1-Motion                     | 左键拖动                                               |
| ButtonRelease-1               | 左键松开                                               |
| Double-Button-1               | 左键双击                                               |
| Enter                         | 鼠标进入控件的范围                                     |
| Leave                         | 鼠标离开控件的范围                                     |
| FocusIn                       | focus移动到控件                                        |
| FocusOut                      | focus移出控件                                          |
| Configure                     | 控件大小改变                                           |
| Key                           | 任一个键盘按键                                         |

## 键盘事件

不带尖括号的字符表示相应的按键，如&lt;1&gt;表示左键，1表示按下键盘上的数字1

### 常用键盘事件

Return (回车), BackSpace, Space, Delete, Escape, Tab
Up, Down, Right, Left
Shift-按钮 (按住shift同时按按钮)

### 不常用键盘事件

Shift_L, Control_L, Alt_L (任何一个shift/ctrl/alt键都可以)
Caps_Lock, Prior(page up), Next(page down)
Cancel, Pause, End, Home, Print, Insert
Num_Lock, Scroll_Lock
F1 ~ F12

## 属性

| 名称           | 描述                                                   |
| -------------- | ------------------------------------------------------ |
| widget         | 产生事件的控件                                         |
| x, y           | 事件发生时鼠标的坐标，单位为pixel                      |
| x_root, y_root | 当前鼠标与x, y的相对位置                               |
| type           | 事件类型                                               |
| num            | The button number (mouse button events only)           |
| char           | The character code (keyboard events only), as a string |
| keysym         | The key symbol (keyboard events only)                  |
| keycode        | The key code (keyboard events only)                    |

# 子模组

## 文件选择

```python
from tkinter import filedialog

askopenfilename()
filedialog.asksaveasfilename(
    initialdir='.',
    initialfile='whatever.png',
    filetypes = (('png files','*.png'),)
)
askdirectory()
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
myimg = ImageTk.PhotoImage(Image.open('myimage.png'))
```