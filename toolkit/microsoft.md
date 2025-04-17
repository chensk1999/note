# Windows 10

## 关闭网络搜索

使用注册表编辑器，在`HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Search`新建一个DWORD值，命名为`BingSearchEnabled`，并将数值设为0，重启

## 右键菜单栏

右键菜单，也叫做Context Menu，相关注册表项参考[这里](http://up.houheaven.com/Regedit/Reg_03.htm)

### 移除软件的右键菜单

可能的注册表位置（注：若不注明，一般放在该路径的`shell`，`background\shell`，`ShellEx\ContextMenuHandlers`等文件夹内）：

```bash
# 文件夹
\HKEY_CLASSES_ROOT\Folder
\HKEY_CLASSES_ROOT\Directory
# 文件
\HKEY_CLASSES_ROOT\*
\HKEY_CLASSES_ROOT\AllFilesystemObjects
# 桌面
\HKEY_CLASSES_ROOT\DesktopBackground

# 删的时候发现了，但是删完看不到效果的
\HKEY_CLASSES_ROOT\YunShellExt.YunShellExtContextMenu
```

### 添加自定义右键菜单

1. 创建项`<somewhere>\shell\<prompt>\command`，其中`<somewhere>`具体路径见后文，`<prompt>`为菜单中显示的文字
2. 将command的值设为指令，如`notepad.exe %1`

`<somewhere>`具体是哪里：

1. 特定文件类别的菜单：`HKEY_CLASSES_ROOT\SystemFileAssociations\<.ext>`，其中`<.ext>`为文件扩展名，比如`.zip`

# Word

## 多级列表与标题

1. 开始 - 段落 - 多级列表
2. 在列表库 / 当前列表中选一个 / 点击文档中的一个列表编号（若选了，则以选中的样式为基础 / 对选中的列表进行编辑）
3. 定义新的多级列表 - 打开“更多”选项 - 将级别链接到样式

若勾选“正规形式编号”，则强制编号格式统一，如实现“第一章 - 1.1节“（不勾选会变成”第一章 - 一.1节“）

## 样式

**隐藏不需要的样式**：开始 - 样式 - 右下角的小标记 - 管理样式（一个有铅笔的小图标） - 推荐，可以隐藏不想看见的样式

**更改样式的大纲级别**：选中要修改的样式 - 右键 - 修改 - 格式 - 段落 - 常规 - 大纲级别

## 页眉与页脚

插入 - 页眉和页脚

不同部分的页眉页脚不同，比如说从第三页开始标页码：首先在分节处插入布局 - 分隔符 - 分节符，然后选中页眉页脚，设计 - 导航 - 取消链接到前一节

调整页眉的横线：选中页眉 - 开始 - 段落 - 边框 - 无边框

## 公式

- **行宽**：如果想要公式和普通的行一样宽，选中公式，右键，段落 - 取消“如果定义了文档网格，则对齐到文档网格”
- **编号**：输入`公式#编号`然后回车。若想自动编号，使用插入 - 文本 - 文档部件 - 域 - AutoNum
- **空格**：`\ensp`，`\emsp`

## 尾注

引用 - 脚注 - 插入尾注

默认在脚注与正文之间有一条分割线，删除方法是

1. 视图 - 大纲
2. 引用 - 脚注 - 显示备注
3. 在备注界面选择尾注 - 尾注分隔符，删除掉
4. 关闭备注，退出大纲视图

另外，默认脚注格式是上标，修改方法是

- 引用 - 脚注 - 右下角的小箭头
- 查找和替换（Ctrl+H）
  - 查找内容：更多 - 特殊格式 - 尾注标记（或者直接输入`^e`，并选中区分全/半角选项）
  - 替换为：`[^&]`（`^&`是通配符，此格式用方括号括起序号），并设置格式 - 字体 - 取消上标

# Visio

## 解决字符间距变化问题

有时候复制粘贴到word之后字符间距变化。解决方法a) 换用较大字体；b) 导出为矢量图再导入到word

## 修改字体

Visio字体由其Master shape的style定义（[来源](https://social.technet.microsoft.com/Forums/ie/en-US/f1642572-dc3b-4baa-a3cd-8e252571cf89/how-to-set-default-font-in-visio-2016?forum=visiogeneral)）

**修改style全局修改字体**

1. 文件 - 选项 - 高级 - 以开发人员模式运行（这一步好像可以省略）
2. 文件 - 选项 - 自定义功能区 - 开发工具，设置之后会显示开发工具选项卡
3. 开发工具 - 绘图资源管理器
4. 绘图资源管理器 - 样式 - 主题，右键，定义样式 - 更改 - 文本，设置想要的字体、字号

## 打开旧版文件

部分旧版文件（比如`.vss`文件）需要修改信任中心才能打开：

1. 文件 - 选项 - 信任中心 - 信任中心设置
2. 文件阻止设置 - 选中要打开的文件类型
3. 受信任位置 - 添加文件所在位置
4. 打开文件

# Libre Office

菜单无法正常显示：Tools - Options - LibreOffice - VIew - 勾选Use OpenGL
