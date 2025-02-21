# git init
```bash
git init
```
**说明：** 在当前目录中初始化新的仓库

<br>

```bash
git init <directory>
```
**说明：** 在\<directory\>目录中初始化一个新的仓库

<br>

# git config
```bash
git config --global init.defaultBranch # 当执行git init命令时，初始化的git仓库的默认分支就是该分支
```
**说明：** 查看全局的默认分支设置

<br>

```bash
git config --global init.defaultBranch [branch-name] # 当执行git init命令时，初始化的git仓库的默认分支就会变成该分支
```
**说明：** 更改初始化新仓库时的默认分支名称


<br>

# git clone
```bash
git clone <repo url>
```
**说明：** 克隆一个现有的仓库\
创建一个目录，目录名为仓库的名称，并将远程仓库的内容克隆到本地目录中

<br>

# git branch
```bash
git branch
```
**说明：** 查看所有分支

<br>

```bash
git branch feature-branch
```
**说明：** 创建新的分支

<br>

# git checkout

```
git checkout <branch_name>
```
**说明：** 工作区内的文件切换到指定分支

<br>

```bash
git checkout -b new_branch_name
```
**说明：** 创建并切换到指定分支

<br>

```bash
git checkout -- filename
```
**说明：** 将工作目录中的某个文件恢复到最新提交的状态(不是暂存区)

<br>

# git switch
```bash
git switch -c <branch_name>
```
**说明：** 创建分支，并切换到该分支

<br>

# git checkout和git switch的区别
- **功能专一性：**\
git checkout：是一个多用途命令，既可以用于切换分支，也可以用于恢复文件\
git switch：专用于分支操作，只用于切换分支和创建新分支

- **命令的语义清晰度：**\
git switch：使分支切换操作更加直观和简洁，减少了命令的复杂性\
git checkout：由于其多功能性，命令语义相对不够直观，需要更多记忆和理解

- **用户体验：**\
git switch： 提供了明确的分支切换和创建功能，降低了误操作的可能性\
git checkout： 因其多功能性，易导致用户混淆或误操作

- **实际使用场景:**\
git switch：当只需要进行分支管理（切换分支或创建新的分支）时，推荐使用 git switch。它具有更清晰的语义，更易于理解和使用\
git checkout：当需要恢复文件到暂存区或最新提交版本时，需要使用 git checkout。另外，某些情况下如果你使用的是较旧版本的 Git，git switch 可能不可用（Git 2.23 之前没有 git switch）

<br>

# git status
```bash
git status
```
**说明：**
查看当前仓库状态

<br>

# git diff
```bash
git diff
```
**说明：** 比较工作区与暂存区的差异

<br>

```bash 
git diff --staged
or
git diff --cached
```
**说明：** 比对暂存区与最新提交之间的差异

<br>

```bash
git diff HEAD 
```
**说明：** 显示工作区与最新提交之间的差异

<br>

```bash
git diff branch1 branch2
```
**说明：** 比较分支之间的差异

<br>

```bash
git diff <commit1> <commit2>
git diff 6fbf3d8 8f0d3a9 #例
```
**说明：** 比较两个提交之间的差异

<br>

```bash
git diff [options] -- <file>

#例: 显示main分支和dev分支中，src/app.js文件的差异
git diff main dev -- src/app.js 

#例: 显示commit1和commit2这两个提交中， src/app.js文件的差异
git diff commit1 commit2 -- <file> 
```
**说明：** 显示特定文件的差异

<br>

```bash
git diff --name-only
```
**说明：** 只显示修改的文件名

<br>

```bash
git diff --name-status
```
**说明：** 显示文件名和文件状态（新增、修改、删除）

<br>

```bash
git diff -p
or
git diff --patch
```
**说明：**
生成差异补丁格式，这通常是默认选项\
该格式显示了更详细的、更结构化的差异信息，包括上下文行和修改的具体位置

<br>

```bash
git diff --stat
```
**说明：** 显示差异的统计信息，包括文件、插入行和删除行的数量

<br>

```bash
git diff --word-diff
```
**说明：** 以单词为单位显示差异

<br>

```bash
git diff --color #强制启用彩色显示
git diff --no-color #强制禁用彩色显示
```
**说明：** 显示/禁用彩色差异

<br>

# git add
```bash
git add <file>
git add README.md #例
```
**说明：** 添加单个文件到暂存区

<br>

```bash
git add <file1> <file2> <file3>
git add file1.txt file2.txt file3.txt #例
```
**说明：** 添加多个文件到暂存区

<br>

```bash
git add <directory>
git add src/  #例
```
**说明：** 添加多个文件到暂存区

<br>

```bash
git add .  #添加当前目录及其子目录中的更改
or
git add -A  #添加工作区中的所有更改
```
**说明：** 将工作区中的所有更改（包括已修改、已删除和新建的文件）添加到暂存区

<br>

```bash
git add --update
```
**说明：** 添加更改但排除删除的文件, 即将所有已修改和新建的文件添加到暂存区，但不会包括删除的文件

<br>

```bash
git add -i
```
**说明：** 以交互方式添加文件的更改，允许选择具体的更改块来添加到暂存区

<br>

```bash
git add -n .
git add --dry-run
```
**说明：** 显示哪些文件将被添加，但不实际添加

<br>

```bash
git add -v .
git add --verbose .
```
**说明：** 显示更详细的输出

<br>

```bash
git add -f <file>
git add -f ignored-file.txt #例
```
**说明：** 强制添加被忽略的文件

<br>

# git mv
```bash
git mv <source> <destination>
```
**说明：**
\<source\>: 要移动或重命名的文件或目录的当前路径\
\<destination\>: 文件或目录的新路径\
在工作区和暂存区移动或重命名文件或目录，不会直接commit

<br>

```bash
git mv <old file name> <new file name>

#例： 将old_name.txt重命名为new_name.txt， Git会自动将这个重命名操作添加到暂存区，准备在下一次提交时记录
git mv old_name.txt new_name.txt 
```
**说明：** 重命名文件

<br>

```bash
git mv <old file> <new directory>
git mv file.txt new_directory/
```
**说明：** 将file.txt移动到new_directory目录下, Git会自动处理文件的路径更新，并记录这个移动操作

<br>

```bash
git mv <old directory> <new directory>

#将old_directory重命名为new_directory, Git会处理目录中所有文件的路径更新，并记录这个重命名操作
git mv old_directory new_directory 
```
**说明：** 重命名目录

<br>

```bash
git mv <old directory>/<old file name> <new directory>/<new file name>

#例： 将old_directory目录下的old_name.txt文件移动到new_directory目录下，并重命名为new_name.txt
git mv old_directory/old_name.txt new_directory/new_name.txt  
```
**说明：** 移动并重命名文件

<br>

# git rm
git rm命令用于从工作区和暂存区中删除文件\
它不仅删除文件，还将删除操作记录在暂存区，以便在下一次提交时将文件的删除包含在提交中

<br>

```bash
git rm <file>

git rm example.txt
```
**说明：** 删除文件并将删除操作添加到暂存区

<br>

```bash
git rm -f <file>
git rm --force <file>

git rm -f example.txt
```
**说明：** 强制删除文件\
如果文件被修改且尚未提交，Git会阻止删除操作以防止数据丢失\
使用 -f（或 --force）选项可以强制删除文件

<br>

```bash
git rm --cached <file>

git rm --cached example.txt
```
**说明：** 保留工作区中的文件但删除在暂存区中的记录\
该命令会从暂存区中移除文件 <file>，但保留工作区中的实际文件\
这在希望停止跟踪某个文件但不实际删除它时非常有用

<br>

```bash
git rm -r <directory>
git rm --recursive <directory>
```
**说明：** 递归删除目录中的所有文件
该命令会递归删除目录 <directory> 及其所有内容，并将这些删除操作添加到暂存区

<br>

# git commit
将暂存区（staging area）中的更改记录到本地仓库的历史中\
每次提交都会创建一个新的提交对象，包括作者信息、提交信息和更改记录

<br>

```bash
git commit -m "Your commit message"
```
**说明：** 命令行里，输入提交信息

<br>

```bash
git commit
```
**说明：** 打开默认编辑器，允许输入详细的提交信息，包括标题和详细描述\
当提交信息有多行时，可以使用该方式

<br>

```bash
git commit -a -m "Your commit message"
```
**说明：** -a选项会自动暂存所有已跟踪文件，然后进行提交，但不包括新创建的未跟踪文件\
如果不使用-a，则需要手动的把每一个文件add一遍，然后commit\
如果使用-a，只要这个文件在仓库历史上曾经被提交过，就不需要每一个通过add命令添加到暂存区后再commit

**关于文件跟踪：**
- 已跟踪文件：已经Git仓库中进行过跟踪的文件，即之前已经被添加并提交过的文件\
- 未跟踪文件：新创建的文件或未被Git跟踪的文件，-a选项不会将这些文件添加到暂存区\
  比如，有<文件A>和<文件B>它们都在之前曾经被提交过（从仓库创建到现在都不曾被提交过），此时创建一个<文件C>是不会被添加到缓存区的

**-a 选项与 git add 的区别:**
- git add：用于将新文件或修改的文件添加到暂存区。需要手动指定文件
- git commit -a：自动将所有已跟踪文件的更改（修改和删除）添加到暂存区，不会包含新文件

<br>

```bash
git commit --amend
```
**说明：** 用于修改最近一次的提交
该命令可以用来编辑提交消息，或将新的更改添加到最近的提交中，而不创建一个新的提交对象\
当发现最近一次提交有错误或不完整时，使用该命令非常有用

- 执行该命令，会打开默认文本编辑器，并编辑提交消息， 保存并关闭编辑器后，新提交消息将替换旧的提交消息\
- 如果已经提交了更改，但忘记了一些文件或有新的更改需要包含在最近的提交中，可以先暂存这些新更改，然后使用 git commit --amend 添加它们到最近的提交中

<br>

# git log
```bash
git log
```
**说明：** 用于查看Git仓库的提交历史

<br>

```bash
git log --oneline
```
**说明：** 一行显示提交历史,即每次的提交信息只显示一行

<br>

```bash
git log -n <number>

#例：显示最近的 3 个提交
git log -n 3
```
**说明：** 限制显示的提交数量

<br>

```bash
git log <file>
```
**说明：** 查看某个文件的提交历史

<br>

```bash
git log --pretty=oneline
git log --pretty=short
git log --pretty=medium
git log --pretty=full
git log --pretty=fuller
git log --pretty=format:"%h - %an, %ar : %s"
```
**说明：** 使用 --pretty 选项来定制输出格式

<br>

```bash
git log --graph
git log --graph --oneline --all #结合 --oneline 和 --all 选项一起使用
```
**说明：** 使用--graph选项来查看提交历史的图形表示

<br>

```bash
git log --since="2 weeks ago"
git log --until="2023-01-01"
git log --since="2023-01-01" --until="2023-12-31"
```
**说明：** 使用 --since 和 --until 选项来查看某个时间段内的提交

<br>

```bash
git log --author="John Doe"
```
**说明：** 使用 --author 选项来查看特定作者的提交

<br>

```bash
git log -p
git log -p -n 3 #-n选项限制显示的文件更改数量
```
**说明：** 使用 -p 选项来查看每个提交中具体的文件更改

<br>

# git blame
git blame 命令用于显示文件内每一行内容的最后修改记录\
主要用于跟踪文件中特定行或块的更改\
通过git blame命令，可以了解是谁在何时对文件的某一行进行了修改\
这在代码审查、调试以及了解代码历史时非常有用

```bash
git blame <file>

# 显示 app.js 文件的每一行的作者、最近的提交ID、日期和提交消息
git blame app.js
```
**说明：** 显示文件的每一行的作者、最近的提交ID、日期和提交消息

<br>

```bash
git blame -p <file>
```
**说明：** 使用 -p 选项来显示详细的提交信息

<br>

```bash
git blame -w <file>
```
**说明：** 使用 -w 选项来忽略由于空白字符变化导致的差异

<br>

```bash
git blame -L <start line>,<end line> <file>
git blame -L 1,3 <file> # 追踪文件第1行到第3行的变更历史
```
**说明：** 使用 -L 选项来指定文件的行范围

<br>

```bash
git blame -e <file>
```
**说明：** 显示任何可归因的内联注释,使用 -e 选项，将作者的电子邮件地址显示在输出中
