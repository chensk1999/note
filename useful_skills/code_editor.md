# VSCode

vscode的设置都存储在settings.json中，每个键值对对应一项设置

```json
{
    "workbench.colorTheme": "Default Dark+",
    "editor.rulers": [
        79,
        120
    ]
}
```

部分文件位置：

设置：`%APPDATA%\Code\User\settings.json`（`%APPDATA% = C:\Users\current user\AppData\Roaming`）

扩展：`%USERPROFILE%\.vscode\extensions`（`%USERPROFILE% = C:\Users\current user`）

## language-specific settings

```json
"[verilog]": {
    "files.autoGuessEncoding": true
}
```

# Vim

## 模式

用vim编辑时，需要在不同模式间切换。在Normal模式按下下表的快捷键进入对应模式，其他模式Esc回到Normal

| Keystroke | Mode         | Description                  |
| --------- | ------------ | ---------------------------- |
| i         | Insert       | 类似一般的文本编辑器         |
| v         | visual       | 选择                         |
| :         | Command Line | 执行命令（执行后回到Normal） |
| shift + r | Replace      |                              |
| shift + v | Visual Line  |                              |
| ctrl + v  | Visual Block |                              |

## Normal

**移动光标**

| Keystroke              | Usage                                                |
| ---------------------- | ---------------------------------------------------- |
| `hjkl`                 | 左、下、上、右                                       |
| `wbe`                  | word（下一个词）、begin（词的开头）、end（词的结尾） |
| `0^$`                  | 行的开头、第一个非空白字符、行的结尾                 |
| `HML`                  | 屏幕顶、屏幕中间、屏幕底                             |
| `ctrl + u`, `ctrl + d` | 上下滚屏                                             |
| `gg, G`                | 文件开头、文件结尾                                   |

**搜索**

1. `/`（正向搜索），或`?`（反向搜索）
2. 输入搜索关键字，Enter
3. 按n和N查看各个结果

**编辑**

| Keystroke     | Usage                                                        |
| ------------- | ------------------------------------------------------------ |
| `oO`          | 下方 / 上方插入行                                            |
| `d, c`        | 删除（delete），更改（change，相当于delete然后进入Insert模式） |
| `dd`          | 删除一行                                                     |
| `x`           | 删除一个字符                                                 |
| `u, ctrl + r` | 撤销 & 重做（undo & redo）                                   |
| `y, p`        | 复制 & 粘贴（yank & paste）                                  |

另外，部分指令可以指定范围：

```shell
h5j         # 向下移动5行
d3w         # 删除3个词
d2d         # 删除2行
```

## Visual

进入这个模式之后

## Command-Line

| Command         | Usage               |
| --------------- | ------------------- |
| `:q`            | quit (close window) |
| `:w`            | write (save file)   |
| `:e [filename]` | open file for edit  |

