# git init
```bash
git init
```
**说明：**
在当前目录中初始化新的仓库

<br>

```bash
git init <directory>
```
**说明：**
在\<directory\>目录中初始化一个新的仓库

<br>

# git config
```bash
git config --global init.defaultBranch
```
**说明：** 
查看全局的默认分支设置\
比如，当执行git init命令时，初始化的git仓库的默认分支就是该分支

<br>

```bash
git config --global init.defaultBranch [branch-name]
```
**说明：**
更改初始化新仓库时的默认分支名称\
比如，当执行git init命令时，初始化的git仓库的默认分支就会变成该分支

<br>

# git clone

```bash
git clone <repo url>
```
**说明：** 克隆一个现有的仓库\
它会创建一个目录(目录名称为repo的名称)，并将远程仓库的内容克隆到该目录中

<br>

```bash
git clone -b <branch name> <repo url>
```
**说明：** 克隆一个现有的仓库的指定分支\
它会创建一个目录(目录名称为repo的名称)，并将远程仓库指定分支的内容克隆到该目录中

<br>

# git branch
```bash
git branch
```
**说明：** 查看所有本地仓库所有分支\
**注：** 如果本地仓库新建，且没有任何提交记录，则执行git branch命令后，不会有任何返回结果

<br>

```bash
git branch -a
```
**说明：** 查看本地仓库和远程仓库的所有分支

<br>
```bash
git branch <new-branch>
```
**说明：** 创建新的分支\
**注：** 如果本地仓库新建，且没有任何提交记录，则执行git branch <new-branch>命令后，会报"fatal: not a valid object name: <default branch name>"错误

<br>

```bash
git branch -d <branch name>
git branch -D <branch name> # 强制删除
```
**说明：** 用于删除指定的分支\
**注：** 如果该分支上有未合并的更改，Git不会允许删除, 需要使用-D强制删除

<br>

```bash
git branch -m <new branch name>
```
**说明：** 当前分支重命名

<br>

# git checkout

```
git checkout <branch_name/tag>
```
**说明：** 工作区和暂存区的内容切换到指定分支或tag\
**注：** 如果当前分支下，有新增为追踪的文件，切换分支后，它依然会存在于切换后分支下的工作区内

<br>

```bash
git checkout -b new_branch_name
```
**说明：** 创建并切换到指定分支, 工作区的文件保持不变

<br>

```bash
git checkout -- <filename>
git checkout <filename>

```
**说明：** 将工作区中的某个文件恢复到暂存区的状态（不是版本库最新提交的状态）

<br>

```bash
git checkout <branch> -- <file-or-directory>
```
**说明：** 从当前分支最新提交中checkout出指定文件或文件夹到当前工作区\
当需要恢复文件或目录到指定版本时非常有用

<br>

```bash
git checkout <commit>
```
**说明：** 将工作区重置到指定的提交的状态\
这会进入"分离头指针"的状态（detached HEAD），即不再位于任何分支上，可以再执行git checkout <branch>命令回到分支上


**分离头指针状态”（Detached HEAD State）**\
Git中的一个术语，指的是当正在检查一个指定的提交（而不是分支）时，Git的HEAD指针不再指向任何分支，而是指向某个具体的提交对象\
这种状态下，可以查看、修改和测试代码，但所做的更改并不属于任何分支


<br>

```bash
git checkout HEAD .
git checkout HEAD <file name>
```
**说明：** 将HEAD指向的分支中的全部或者部分文件替换重置暂存区和以及工作区中的文件

<br>

# git switch

```bash
git switch -c <branch_name>
```
**说明：** 创建分支，并切换到该分支, 工作区的文件保持不变

<br>

# git checkout和git switch的区别
- **功能专一性**
git checkout: 是一个多用途命令，既可以用于切换分支，也可以用于恢复文件
git switch: 专用于分支操作，只用于切换分支和创建新分支

- **命令的语义清晰度**
git switch: 使得分支切换操作更加直观和简洁，减少了命令的复杂性
git checkout: 由于其多功能性，命令语义相对不够直观，需要更多记忆和理解

- **用户体验**
git switch: 提供了明确的分支切换和创建功能，降低了误操作的可能性
git checkout: 因其多功能性，易导致用户混淆或误操作

- **实际使用场景**
git switch：当只需要进行分支管理（切换分支或创建新的分支）时，推荐使用git switch, 它具有更清晰的语义，更易于理解和使用\
git checkout：当需要恢复文件到暂存区或最新提交版本时，需要使用git checkout。另外，某些情况下如果使用的是较旧版本的Git，git switch 可能不可用（Git 2.23 之前没有 git switch）

<br>

# git status
```bash
git status
```
**说明：** 查看当前仓库状态

<br>

# git diff
```bash
git diff
```
**说明：** 用于比较工作目区尚未暂存的更改与暂存区（索引）中的内容之间的差异

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
**说明：** 显示工作区与版本库最新提交之间的差异

<br>

```bash
git diff <branch name1> <branch name2>
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
**说明：** 生成差异补丁格式，这通常是默认选项\
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
**说明：** 在工作区和暂存区移动或重命名文件或目录，不会直接commit

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
**说明：** 删除工作区中的文件但保留在暂存区中的记录\
该命令会从暂存区中移除文件 <file>，但保留工作区中的实际文件\
这在希望停止跟踪某个文件但不实际删除它时非常有用

<br>

```bash
git rm -r <directory>
git rm --recursive <directory>

git rm --cached example.txt
```
**说明：** 递归删除目录中的所有文件
该命令会递归删除目录 <directory> 及其所有内容，并将这些删除操作添加到暂存区

<br>

# git commit
将暂存区中的更改记录到本地仓库的历史中\
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
**说明：** -a选项会自动暂存所有已跟踪文件，然后进行提交，但不包括新创建的未跟踪文件
如果不使用-a，则需要手动的把每一个文件add一遍，然后commit\
如果使用-a，只要这个文件在仓库历史上曾经被提交过，就不需要每一个通过add命令添加到暂存区后再commit

**关于文件跟踪：**
- **已跟踪文件：** 
已经Git仓库中进行过跟踪的文件，即之前已经被添加并提交过的文件\
- **未跟踪文件：** 
新创建的文件或未被Git跟踪的文件，-a选项不会将这些文件添加到暂存区\
比如，有<文件A>和<文件B>它们都在之前曾经被提交过（从仓库创建到现在都不曾被提交过），此时创建一个<文件C>是不会被添加到缓存区的

**-a 选项与 git add 的区别:**
- git add： 用于将新文件或修改的文件添加到暂存区。需要手动指定文件
- git commit -a：自动将所有已跟踪文件的更改（修改和删除）添加到暂存区，不会包含新文件

<br>

```bash
git commit --amend
```
**说明：** 用于修改最近一次的提交
该命令可以用来编辑提交消息，或将新的更改添加到最近的提交中，而不创建一个新的提交对象\
当发现最近一次提交有错误或不完整时，使用该命令非常有用

- 执行该命令，会打开默认文本编辑器，并编辑提交消息， 保存并关闭编辑器后，新提交消息将替换旧的提交消息
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

#例：显示最近的3个提交
git log -n 3
git log --oneline -n 3 #结合--oneline使用
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
**说明：** 使用--pretty选项来定制输出格式

<br>

```bash
git log --all
```
**说明：** --all表示表示要显示所有引用（references）的提交信息，包括所有的分支、标签等，而不仅仅是当前分支的提交\
使用--all可以查看整个仓库的所有活动，了解所有分支的提交情况

<br>

```bash
git log --graph
git log --graph --oneline --all #结合--oneline和--all选项一起使用
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
**说明：** 使用--author选项来查看特定作者的提交

<br>

```bash
git log -p
git log -p -n 3 #-n选项限制显示的文件更改数量
```
**说明：** 使用-p选项来查看每个提交中具体的文件更改

<br>

# git blame
git blame命令用于显示每一行文件内容的最后修改记录\
这对于跟踪文件中特定行或块的更改非常有用\
通过git blame命令，可以了解是谁在何时对文件的某一行进行了修改\
这在代码审查、调试以及了解代码历史时非常有用。

```bash
git blame <file>

# 显示app.js文件的每一行的作者、最近的提交ID、日期和提交消息
git blame app.js
```
**说明：** 显示文件的每一行的作者、最近的提交ID、日期和提交消息

<br>

```bash
git blame -p <file>
```
**说明：** 使用-p选项来显示详细的提交信息

<br>

```bash
git blame -w <file>
```
**说明：** 使用-w选项来忽略由于空白字符变化导致的差异

<br>

```bash
git blame -L 1,3 <file>
```
**说明：** 使用-L选项来指定文件的行范围，例如，第1行到第3行

<br>

```bash
git blame -e <file>
```
**说明：** 显示任何可归因的内联注释,使用-e选项，将作者的电子邮件地址显示在输出中

<br>

# git reset
git reset是Git用来撤销更改的命令\
它会影响暂存区（index/staging area）和提交历史（commit history）\
这个命令非常强大，需要小心使用，因为它可以重写提交历史，这在共享仓库中可能是不理想的

```bash
git reset [选项] [<commit>]
```
**说明：** 基本格式

<br>

```bash
git reset --soft HEAD~1
```
**说明：** 将当前分支的HEAD指针回退到上一个提交，同时保留所有的更改（包括工作区和索引区中的更改）\
这个命令可以用来将最近的一次提交取消，但保持更改，允许进行修改后重新提交（amend）或进一步调整

<br>

```bash
git reset HEAD
or
git reset --mixed HEAD
```
**说明：** 将当前分支的HEAD指针指向最新提交，并将最新提交内容重置到索引区（暂存区），但保留工作目录中的更改

<br>

```bash
git reset HEAD~1
or
git reset --mixed HEAD~1
```
**说明：** 将当前分支的HEAD指针指向上一个提交，并将上一个提交内容重置到索引区（暂存区），但保留工作目录中的更改

<br>

```bash
git reset --hard HEAD    # 将当前分支的状态重置到最近的提交（即 HEAD 指向的提交）
git reset --hard HEAD~1  # 将当前分支的状态重置到最近的提交的上一个提交（HEAD指针回退到上一个提交）
```
**说明：** 将当前分支的HEAD指针回退到指定的提交，同时重置索引区和工作目录

<br>

```bash
git reset <commit>
```
**说明：** 将当前分支重置到指定的提交，保留工作区中的未暂存更改

**具体执行如下：**
- 将HEAD指针移至指定的提交
- 将索引区重置为与指定提交相同的状态，任何在暂存区中的更改将被丢弃
- 工作区保持不变，已经修改但未暂存的文件保留下来

<br>

```bash
git reset --keep <commit>
```
**说明：** 将仓库和暂存区重置为与 <commit> 匹配\
如果工作区中的更改不与目标提交产生冲突，则尝试保留工作区中未暂存的更改

**具体执行如下：**
- 将HEAD指针移至指定的提交
- 将索引区重置为与指定提交相同的状态，任何在暂存区中的更改将被丢弃
- 保留工作目录：工作目录中的任何未暂存更改会保留下来，前提是这些更改不会与目标提交的文件产生冲突。如果冲突，操作将失败并提示错误
- 在执行重置前，会检查未暂存的更改是否与目标提交冲突，如果有冲突，将会拒绝操作并显示错误信息

<br>

# git revert

```bash
git revert <commit>
```
**说明：** 创建一个新的提交，反转<commit>提交的内容\
比如，一共依次有五个提交，A,B,C,D,E, 如果C提交中修改了文件file.txt中的某一行文本，执行"git revert <commit C>"会创建一个新的提交F，它会修改file.txt，将内容改回C提交之前的状态

<br>

# git tag

Git中的标签（tag）是用于标记项目历史中某个特定点的引用\
标签通常用于标记发布点（例如 v1.0.0），因此开发者可以非常方便地标记和定位项目的重要里程碑

- **轻量标签（Lightweight Tag）**
它们只是提交对象的一个引用（类似于分支，但不会移动），没有额外的元数据

- **附注标签（Annotated Tag）**
它们存储额外的信息，包括打标签者的名字、电子邮件地址、日期和标签消息\
附注标签实际上是存储在Git数据库中的一个独立对象

```bash
git tag
```
**说明：** 列出仓库中的所有标签

<br>

```bash
git tag <tagname>

git tag v1.0.0 # 例
```
**说明：** 在当前分支的最新提交（HEAD）上创建一个轻量标签

<br>

```bash
git tag -a <tagname> -m "your message"
```
**说明：** 在当前分支的最新提交（HEAD）上创建一个附注标签

<br>

```bash
git tag -d <tagname>
```
**说明：** 删除标签

<br>

# git merge

```bash
git merge <branch name>
```
**说明：** 合并分支\<branch name\>到当前分支

<br>

```bash
git merge <remote>/<branch name>
git merge origin/feature #合并origin的feature分支到当前分支
```
**说明：** 合并远程分支到当前分支

<br>

# gir rebase
git rebase命令用于将一个分支中的一系列提交转移到另一个分支之上

**使用场景:**

- **保持提交历史整洁**
git rebase可以用来避免合并提交，保持项目历史干净、线性

- **更新特性分支**
将主分支的新变化包含到特性分支中，使特性分支保持最新

```bash
git rebase <upstream-branch>
git rebase main # 将当前分支的所有提交在main分支的基础上再提交依次
```
**说明：** 将当前分支的提交重新应用到<upstream-branch>分支\
这种操作的效果是将当前分支的提交基于上游分支的最新提交点进行重新排列，从而生成一个线性的提交历史

例如：\
1) 基于main分支创建feature分支\
2) 针对main分支的main.txt文件，有三次修改，并依次进行了A,B,C三个提交\
3) 同时针对feature分支的feature.txt文件，也有三次修改，并依次进行了D,E,F三次提交\
4) 在feature分支下，执行git rebase main命令后，首先会将feature分支下的main.txt文件的A,B,C三次提交更新进来，然后再将feature分支下的feature.txt文件的D,E,F三次提交也更新进来\
   这样，feature分支就把main分支的最新更改更新进来了，同时featture分支的历史记录里可以看到提交历史是线性的，A-B-C-D-E-F\
   而不是当查看A,B,C三个提交时去main分支，查看D,E,F三次提交时去feature分支了，这样会方便查看

<br>

```bash
git rebase --continue
```
**说明：** 继续rebase操作

<br>

```bash
git rebase --abort
```
**说明：** 中途放弃rebase操作


<br>

# git merge和git rebase

## Git Rebase

git rebase主要用于将一个分支中的一系列提交重新应用到另一个基底分支之上，从而生成一个线性的提交历史

**特点**
- 线性历史：Rebase 会重新应用提交，因此生成的历史看起来是线性的
- 不产生额外的合并提交：Rebase 不会像 merge 那样产生一个额外的合并提交
- 提交ID变化：Rebase 会重新生成被重新应用提交的提交对象，导致这些提交有新的提交ID

**优点：**
- 提交历史更加干净和线性，易于理解和阅读
- 在代码评审时，线性的历史可以更好地追踪更改

**缺点：**
- 改变了提交的SHA-1散列值，违反了Git中不要在共享分支上重写历史的最佳实践
- 在处理复杂历史时，可能会遇到更多的冲突

**使用示例**\
假设当前有如下分支：\
A---B---C main\
&emsp;&emsp;\\\
&emsp;&emsp;&ensp;D---E feature


在feature分支上执行git rebase main
```bash
git checkout feature
git rebase main
```

执行之后，会变成如下结构：\
A---B---C---D'---E' main\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\\\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;feature


## Git Merge

git merge用于将另一个分支的更改合并到当前分支，并保持原有的提交历史。

**特点**
- 保留历史：Merge保留了所有分支的提交历史
- 产生一个合并提交：Merge 会生成一个新的合并提交，这个合并提交的父提交有两个或多个
- 不改变提交 ID：Merge 不会改变已有提交的提交 ID

**优点：**
- 保留了完整的历史，包括分支和合并的过程
- 更适合在长期维护的分支上进行操作，因为可以清楚地看到分支和合并点

**缺点：**
- 提交历史可能会变得复杂，尤其是当有大量的分支和合并时
- 生成的合并提交有时可能会使历史变得混乱

**使用示例**

假设当前有如下分支：\
A---B---C main\
&emsp;&emsp;\\\
&emsp;&emsp;&ensp;D---E feature


在main分支上执行git merge feature
```bash
git checkout main
git merge feature
```

执行之后，会变成如下结构, 其中，F为合并提交\
A---B---C---F main\
&emsp;&emsp;\\&emsp;&emsp;/\
&emsp;&emsp;D---E feature
	  
## 何时使用 Rebase 和 Merge
- git rebase：
  - 想要保持提交历史的线性和整洁
  - 在共享或发布代码之前进行清理
  - 在个人分支上进行操作，以便将所有更改合并到一个单一的线性历史中

- git merge：
  - 想要保留完整的历史记录，包括分支和合并点
  - 在进行长期维护的分支上操作，以保留所有的变更历史
  - 合并已经公共的分支，以避免潜在的历史重写问题

## 总结
- rebase重新应用提交，生成线性的历史，适用于清理历史和创建线性的提交图
- merge保留所有合并点和完整的分支历史，适用于保留详细的历史记录和长期维护分支

<br>

# git remote
git remote命令用于管理和操作Git仓库的远程存储库\
远程存储库是指托管在服务器上的Git仓库，通常用于与其他开发人员共享和协作代码

```bash
git remote
```
**说明：** 列出所有配置的远程仓库名称

<br>

```bash
git remote -v
```
**说明：** 列出所有远程仓库的名称及其URL, -v选项表示显示详细信息（verbose）

<br>

```bash
git remote add <remote> <url>
git remote add origin https://github.com/user/repo.git #例
```
**说明：** 用于添加一个新的远程仓库
- \<name\>：远程仓库的名字（例如 origin）
- \<url\>：远程仓库的 URL 地址（例如 https://github.com/user/repo.git）

<br>

```bash
git remote remove <name>
```
**说明：** 用于删除一个远程仓库, 
- \<name\>：要删除的远程仓库的名字

<br>

```bash
git remote rename <old-name> <new-name>
```
**说明：** 重命名一个远程仓库

<br>

```bash
git remote set-url <name> <newurl>
```
**说明：** 修改远程仓库的 URL

<br>

```bash
git remote show <name>
```
**说明：** 显示远程仓库的详细信息


# git fetch
用于从远程仓库获取最新的更改，但不会自动合并这些更改到当前的工作分支\
简而言之，git fetch只是更新本地对远程分支的记录，而当前分支及其提交状态、暂存区和工作区将保持不变

```bash
git fetch
```
**说明：** 从所有配置的远程仓库中拉取更新

<br>

```bash
git fetch <remote>

git fetch origin # 从远程仓库origin拉取更新
```
**说明：** 从指定的远程仓库中拉取更新

<br>

```bash
git fetch <remote> <branch>
 
git fetch origin main # 从远程仓库origin的main分支拉取更新
```
**说明：** 从指定的远程仓库中拉取指定分支的更新

<br>

# git pull
git pull是一个用于从远程仓库获取更新并将这些更新合并到当前分支的Git命令\
它的功能可以视为git fetch和git merge两个命令的组合

```bash
git pull
```
**说明：** 运行git pull时，会依次执行以下操作
- **获取最新的提交：**
  首先从远程仓库（通常是 tracking branch，如 origin/main）下载所有的新提交和更新， 相当于执行git fetch
- **合并更新：**
  将这些新的提交合并到当前所在的分支，相当于执行git merge\
  如果没有冲突，合并将自动完成\
  如果有冲突，需要手动解决这些冲突

<br>

```bash
git pull <remote> <branch_name>

git pull origin main #例
```
**说明：** 从远程仓库指定分支拉取更新\
remote是远程仓库的名称\
branch_name是想要从中拉取更新的分支

<br>

```bash
git pull --rebase
```
**说明：** 使用--rebase选项来代替默认的合并方式, 用于从远程仓库拉取更改时将本地的未提交更改应用到远程更改之上，而不是合并它们\
这种方法可以保持项目历史的清晰和线性，避免了合并提交（merge commits）的产生

<br>

# git push
用于将本地仓库中的提交（commits）推送到远程仓库

```bash
git push <remote> <local branch name>
git push origin main #例：推送当前main分支到远程仓库origin的main分支

git push <remote> <local_branch>:<remote branch> #推送当前仓库指定分支到远程仓库的指定分支
```
**说明：** 推送本地分支到远程仓库的同名分支或不同分支

<br>

```bash
git push <remote> --delete <branch name/tag>
git push <remote> :<branch name> #注意，"："前有一个空格，
```
**说明：** 删除远程仓库的指定分支或标签

<br>

```bash
git push --force origin main
```
**说明：** --force表示强制推送，覆盖远程分支的内容\
一般不推荐使用，除非知道自己在做什么，因为这可能会导致数据丢失

<br>

```bash
git push -u origin new-branch
git push --set-upstream origin new-branch
```
**说明：** --set-upstream 或 -u： 在首次推送一个本地分支到远程时，使用这个选项可以将本地分支与远程分支关联，这样下次可以直接使用git push

<br>

```bash
git push --tags
git push --tags <remote>
```
**说明：** 推送所有标签到远程仓库\
如果省略 <remote>，默认将标签推送到默认的远程仓库（通常是 origin）

<br>

# git clean
git clean用于清理违背追踪的文件和目录\
执行git clean时需谨慎，因为它会永久删除未被追踪的文件和目录，无法恢复\
因此，务必在执行前使用 git clean -n进行检查确认

```bash
git clean -n
```
**说明：** 确认删除未被追踪的文件

<br>

```bash
git clean -f #删除文件
git clean -d #删除目录
git clean -d #删除文件和目录
```
**说明：** 强制删除未被追踪的文件或目录\
