# git init
```bash
git init [directory]
```
**说明：**
在当前目录中初始化新的仓库

<br><br>

```bash
git init <directory>
```
**说明：**
在<directory>目录中初始化一个新的仓库\

<br><br>

# git config
```bash
git config --global init.defaultBranch
```
**说明：** 
查看全局的默认分支设置\
当执行git init命令时，初始化的git仓库的默认分支就是该分支

<br><br>

```bash
git config --global init.defaultBranch [branch-name]
```
**说明：**
更改初始化新仓库时的默认分支名称\
当执行git init命令时，初始化的git仓库的默认分支就会变成该分支

<br><br>

# git clone
获取一个现有的仓库\
创建一个目录，并将远程仓库的内容克隆到本地目录中
```bash
git clone <repo url>
```

<br><br>

# git branch
- 查看所有分支
```bash
git branch
```

<br><br>

- 创建新的分支
```bash
git branch feature-branch
```

<br><br>

# git checkout

- 切换到指定分支
```
git checkout <branch_name>
```

<br><br>

- 创建并切换到指定分支
```bash
git checkout -b new_branch_name
```

- 将工作目录中的某个文件恢复到暂存区或最新提交的状态
```bash
git checkout -- filename
```

<br><br>

# git switch
创建分支，并切换到该分支
```bash
git switch -c <branch_name>
```

<br><br>

# git checkout和git switch的区别
- 功能专一性：
git checkout 是一个多用途命令，既可以用于切换分支，也可以用于恢复文件
git switch 专用于分支操作，只用于切换分支和创建新分支

- 命令的语义清晰度：
git switch 的引入使得分支切换操作更加直观和简洁，减少了命令的复杂性
git checkout 由于其多功能性，命令语义相对不够直观，需要更多记忆和理解

- 用户体验：
git switch 提供了明确的分支切换和创建功能，降低了误操作的可能性
git checkout 因其多功能性，易导致用户混淆或误操作

- 实际使用场景:
git switch：当只需要进行分支管理（切换分支或创建新的分支）时，推荐使用 git switch。它具有更清晰的语义，更易于理解和使用\
git checkout：当需要恢复文件到暂存区或最新提交版本时，需要使用 git checkout。另外，某些情况下如果你使用的是较旧版本的 Git，git switch 可能不可用（Git 2.23 之前没有 git switch）

<br><br>

# git status
```bash
git status
```
**说明：**
查看当前仓库状态

<br><br>

# git diff
```bash
git diff
```
**说明：**
用于比较Git工作区与暂存区或与其他分支或提交之间的差异\

<br><br>

```bash 
git diff --staged
or
git diff --cached
```
**说明：**
比对暂存区与最新提交之间的差异

<br><br>

```bash
git diff HEAD 
```
**说明：**
显示工作区与最新提交之间的差异

<br><br>

```bash
git diff branch1 branch2
```
**说明：**
比较分支之间的差异

<br><br>

```bash
git diff <commit1> <commit2>
git diff 6fbf3d8 8f0d3a9 #例
```
**说明：**
比较两个提交之间的差异

<br><br>

```bash
git diff [options] -- <file>

#例: 显示main分支和dev分支中，src/app.js文件的差异
git diff main dev -- src/app.js 

#例: 显示commit1和commit2这两个提交中， src/app.js文件的差异
git diff commit1 commit2 -- <file> 
```
**说明：**
显示特定文件的差异

<br><br>

```bash
git diff --name-only
```
**说明：**
只显示修改的文件名

<br><br>

```bash
git diff --name-status
```
**说明：**
显示文件名和文件状态（新增、修改、删除）

<br><br>

```bash
git diff -p
or
git diff --patch
```
**说明：**
生成差异补丁格式，这通常是默认选项\
该格式显示了更详细的、更结构化的差异信息，包括上下文行和修改的具体位置

<br><br>

```bash
git diff --stat
```
**说明：**
显示差异的统计信息，包括文件、插入行和删除行的数量

<br><br>

```bash
git diff --word-diff
```
**说明：**
以单词为单位显示差异

<br><br>

```bash
git diff --color #强制启用彩色显示
git diff --no-color #强制禁用彩色显示
```
**说明：**
显示/禁用彩色差异

<br><br>

# git add
```bash
git add <file>
git add README.md #例
```
**说明：**
添加单个文件到暂存区

<br><br>

```bash
git add <file1> <file2> <file3>
git add file1.txt file2.txt file3.txt #例
```
**说明：**
添加多个文件到暂存区

<br><br>

```bash
git add <directory>
git add src/  #例
```
**说明：**
添加多个文件到暂存区

<br><br>

```bash
git add .  #添加当前目录及其子目录中的更改
or
git add -A  #添加工作区中的所有更改
```
**说明：**
将工作区中的所有更改（包括已修改、已删除和新建的文件）添加到暂存区

<br><br>

```bash
git add --update
```
**说明：**
添加更改但排除删除的文件, 即将所有已修改和新建的文件添加到暂存区，但不会包括删除的文件

<br><br>

```bash
git add -i
```
**说明：**
以交互方式添加文件的更改，允许选择具体的更改块来添加到暂存区

<br><br>

```bash
git add -n .
git add --dry-run
```
**说明：**
显示哪些文件将被添加，但不实际添加

<br><br>

```bash
git add -v .
git add --verbose .
```
**说明：**
显示更详细的输出

<br><br>

```bash
git add -f <file>
git add -f ignored-file.txt #例
```
**说明：**
强制添加被忽略的文件

<br><br>

# git mv
```bash
git mv <source> <destination>
```
**说明：**
\<source\>: 要移动或重命名的文件或目录的当前路径\
\<destination\>: 文件或目录的新路径\
git mv命令的操作会在工作区和暂存区进行，不会直接commit

<br><br>

```bash
git mv <old file name> <new file name>

#例： 将old_name.txt重命名为new_name.txt， Git会自动将这个重命名操作添加到暂存区，准备在下一次提交时记录
git mv old_name.txt new_name.txt 
```
**说明：** 重命名文件

<br><br>

```bash
git mv <old file> <new directory>
git mv file.txt new_directory/
```
**说明：** 将file.txt移动到new_directory目录下, Git会自动处理文件的路径更新，并记录这个移动操作

<br><br>

```bash
git mv <old directory> <new directory>

#将old_directory重命名为new_directory, Git会处理目录中所有文件的路径更新，并记录这个重命名操作
git mv old_directory new_directory 
```
**说明：** 重命名目录

<br><br>

```bash
git mv <old directory>/<old file name> <new directory>/<new file name>

#例： 将old_directory目录下的old_name.txt文件移动到new_directory目录下，并重命名为new_name.txt
git mv old_directory/old_name.txt new_directory/new_name.txt  
```
**说明：** 移动并重命名文件
