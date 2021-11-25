# 基本概念

## 工作区，暂存区和版本库

工作区（working directory）就是我们看见的文件目录；暂存区（index, or stage）标记了下一次要提交的内容，通常在`.git/index`文件夹；版本库（repository）就是`.git`文件夹下的其他东西，包括了所有历史版本和快照。版本库内的内容总是有办法恢复的，但是没有commit的内容可以被弄丢

```mermaid
sequenceDiagram
    participant working directory
    participant index / stage
    participant repository

    working directory ->> index / stage: git add
    index / stage ->> repository: git commit
    working directory ->> repository: git commit -a
    repository ->> working directory: git checkout
```



## 文件状态

```mermaid
sequenceDiagram
    participant untracked
    participant unmodified
    participant modified
    participant staged

    untracked ->> staged: git add
    modified ->> staged: git add
    staged ->> unmodified: git commit
```

## gitignore

`.gitignore`文件规定了不纳入git管理的文件模式。每行是一条规则，使用glob模式（一种简化的正则表达式，包括`*, ?, []`，`**`匹配任意中间目录）递归应用于整个工作区。特别地，以`/`开头防止递归，以`/`结尾指定目录，以`!`开头表示取反

```
#-------------------------------------------------------------------------------
# 文件

# 忽略所有的.txt文件
*.txt

# 忽略根目录的.txt文件，但不忽略其他文件夹的.txt文件
/*.txt

# 忽略a文件夹下的.txt文件，但不忽略a的子文件夹中的.txt文件
a/*.txt

# 跟踪所有的lib.txt，即便你在前面忽略了.txt文件
!lib.txt

#-------------------------------------------------------------------------------
# 文件夹

# 忽略所有名为 build 的文件夹以及它们的子文件夹，但不忽略子目录中的文件
build/

# 忽略 doc/notes.txt，但不忽略 doc/server/arch.txt
doc/*.txt

# 忽略 doc/ 目录及其所有子目录下的 .pdf 文件
doc/**/*.pdf
```

## 分支

git版本库里有三类对象：blob，存储文件快照；tree，记录文件目录结构和若干blob对象索引；commit，记录了提交的元信息、一个tree索引和指向上一次提交的commit索引（合并分支产生的提交，指向多个父commit对象）

分支就是指向commit对象的可变指针，一般用master表示主支

git中有一个特殊指针HEAD，它指向某个分支，标志着当前的分支。当进行提交时，HEAD以及当前分支自动向前移动

# 常用指令

## 配置

```bash
git config [--global] user.name "Chen Shaokun"
git config [--global] user.email "chensk@mail.com"

# 取消代理
# 能解决代理导致的“failed to connect to github.com port 443”错误
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 获取git仓库

```bash
# 在当前目录下建立.git子目录，即初始化一个仓库
git init

# 克隆git仓库
# source是仓库地址，比如user@server:path/to/repo.git
git clone <source> [name]
```

## 文件操作

```bash
# 添加文件/暂存修改
git add <file>

# 移除文件
# 注意，删除文件却不移除不会从git中去除文件；如果有未提交的修改，不能直接移除（防止数据丢失）
git rm <file>

# 移动/重命名
# 相当于移动文件、git rm old、git add new，效果和分开做完全一样
git mv <src> <dest>

# 取消暂存，注意这个操作可能丢弃数据，尽量把全部修改都暂存了再reset
git reset

# 提交修改
git commit
git commit -a        # 提交所有修改（包括未暂存的）
git commit --amend   # 修订提交，将现在暂存区里的更改合并到上一个提交

# 撤销修改到上一次提交
git checkout -- <file>

# 检查文件状态（查看modified，staged）
git status

# 查看文件区别
git diff

# 查看提交历史
git log
```

## 远程仓库

```bash
# 查看远程仓库
git remote -v             # 查看远程仓库表
git remote show <remote>  # 查看一个远程仓库的信息

# 添加、移除远程仓库
git remote add <remote> <url>
git remote remove <remote>

# 重命名远程仓库
git remote rename <old> <new>

# 从远程仓库抓取
git fetch <remote>

# 从远程仓库拉取
git pull

# 推送到远程仓库
git push <remote> [branch]
```

## 标签

```bash
# 查看标签
git tag --list "v1.8.*"
git show <tag>

# 创建轻量标签（相当于提交的别名，除了名字什么都没有。通常只用作临时标签）
git tag this-is-a-lightweight-tag

# 创建附注标签（可以包含很多信息，一般建议用这个）
git tag -a v1.4 -m "some message about the annotated tag"

# 使用例：给过去的提交加标签
git log --pretty=oneline
git tag -a v1.2 9fceb02       # 9fceb02是对应提交的部分校验和

# 删除标签
git tag -d <tag>

# 推送标签：push默认不推送标签
git push origin <tagname>    # 推送一个标签
git push origin --tags       # 推送全部标签
git push --delete <tagname>  # 移除远程仓库的标签
```

## 分支

```bash
# 查看分支
git branch [-v]

# 切换分支
git checkout <branch>

# 创建同时切换
git checkout -b <branch>

# 合并分支（将目标分支合并到当前分支）
git merge <branch>

# 删除分支
git merge -d <branch>

# 变基
# 首先，撤销从upstream与branch分支点开始、到branch为止的所有commit
# 然后移动到upstream，再逐个施加这些commit
git rebase upstream [branch]

# 例如
git rebase master dev
# A - B - C - master
#      \ D - E - dev
# 转变为
# A - B - C - master
#                \ D' - E' - dev
```

# 工作流程

```bash
# 创建并切换到新分支。此举在于让master相对独立，不至于大家一起编辑master
git checkout -b dev

# 编辑文件

# 在分支内提交更改
git add --all
git commit

# 当master发生更改时，与主干同步。方便日后合并分支
git fetch origin
git rebase origin/master

# 合并提交。将分支内的多个commit合并为一个
# 方法1
git rebase -i origin/master
# 方法2
git reset HEAD~5
git add --all
git commit -am "Here's the bug fix that closes #28"

# 推送。如果因合并提交导致分支历史改变，git push --force
git push

# 确认无误后，合并到master分支
git merge master
```

全部在master上弄的偷懒办法

```bash
# 修改并提交

# 拉取master分支，并合并。有问题就手动解决
git fetch
git merge origin/master

# 推送
git push
```



