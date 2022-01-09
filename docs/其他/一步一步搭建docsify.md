# 搭建docsify教程
本站就是用docsify搭建的，它足够简单简洁~
## 1. 首先全局安装docsify并初始化
`npm i docsify-cli -g`
新建项目的文件夹，并在文件夹内进入cmd
`docsify init ./`
执行一下命令，查看初始页面
`docsify serve ./`
## 2.接着修改配置
```
<script>
    window.$docsify = {
        <!-- 本站的名字 -->
      name: '',
      <!-- 右上角跳转的github -->
      repo: '',
      <!-- 是否开启封面，需创建——coverpage.md文件 -->
      coverpage: true
    }
  </script>
```

可以设置封面的logo 以及 文字 及跳转

```
![logo](.\static\yds.jpg)

# 可以不起名字

 在此记录一点学习和生活.

> My blade is yours！  
> Defend yourself. Never await victory.Do not let your pride blind you. A true master is an eternal student. Look inward.Watch, and learn.

[GitHub](https://github.com/gitronlee)
[Get Started](#headline)
```

设置主题

```
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsify-themeable@0/dist/css/theme-defaults.css">
```

启用侧边栏,需要搭配_sidebar.md文件

```
loadSidebar: true
```

或启用导航,需要搭配_navbar.md文件

```
loadNavbar: true,
```

## 3.插件
搜索、高亮等，去百度。或者直接来我的仓库参考下即可~
[GitHub_ronlee_docsify](https://github.com/Gitronlee/gitronlee.github.io/blob/master/index.html)
## 4. 发布脚本
docsify的一点不方便之处就是导航侧边栏需要根据文章来做相应的维护。所以我就写了个自动生成navbar 和 sidebar的脚本。代码写的很烂，也懒得去优化了，以下：
```python
'''
Author: ronlee
Date: 2022-01-07 11:09:16
LastEditors: ronlee
LastEditTime: 2022-01-09 16:24:58
Description: 自动生成导航栏和侧边栏
FilePath: \_1_learn\gitronlee.github.io\autoNavbarFiles.py
'''
import os
import sys
import re
import shutil
new_line = "  * [首页](README)"  # 全局变量
readmetext = "# 本站目录\n\n"


def write2file(fname, newsidebartext, rmovestr):
    src_fobj = open(fname, 'a+', encoding='utf-8', errors='ignore')
    src_fobj.seek(0)
    src_fobj.truncate()
    src_fobj.flush()
    src_fobj.write(newsidebartext.replace(
        rmovestr+"\\", "/").replace("\\", "/"))

    src_fobj.close()


def GetFirstLine(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
        for line in fp:
            results = line.lstrip('#').strip()
            item2 = "".join(results)  # 根据实际需要使用相应的分隔符连接列表元素,如 , : ; 或者空字符串
            return "  * ["+item2+"]("+filepath+")\n"


def hasMDFile(filepath):
    print("haseMDFile:", filepath)
    pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回 List
    for s in pathDir:
        newDir = os.path.join(filepath, s)  # 将文件命加入到当前文件路径后面
        if os.path.isfile(newDir):  # 如果是文件
            if newDir.endswith('.md'):  # 如果是md文件
                return True
    return False

# 由于我主要在本地查看自己的笔记，你可以将这里改写为图床地址
def copy2assets(filepath, base_path):
    pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回 List
    for s in pathDir:
        newDir = os.path.join(filepath, s)  # 将文件命加入到当前文件路径后面
        toDir = os.path.join(base_path, s)
        print("srcDir:", newDir)
        print("toDir:", toDir)
        if os.path.isfile(newDir):  # 如果是文件
            print("++++++++++++++++")
            shutil.copyfile(newDir, toDir)


def eachFile(filepath, path):
    pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回 List
    for s in pathDir:
        newDir = os.path.join(filepath, s)  # 将文件命加入到当前文件路径后面
        # print("s:", s)
        global new_line
        global readmetext
        if os.path.isfile(newDir):  # 如果是文件
            if newDir.endswith('.md'):  # 如果是md文件
                new_line = new_line + GetFirstLine(newDir)
                readmetext = readmetext + GetFirstLine(newDir)
        elif s == "assets":
            print("newDir:", newDir)
            copy2assets(newDir, path)
        elif hasMDFile(newDir):
            # 如果不是文件，只递归有md文件的目录
            new_line = new_line + "\n* " + s + "\n"
            readmetext = readmetext + "\n## " + s + "\n"
            eachFile(newDir, path)


if __name__ == '__main__':
    path, filename = os.path.split(os.path.abspath(sys.argv[0]))
    print("当前路径：", path)
    newsidebarpath = os.path.join(path, "_sidebar.md")
    newnavbarpath = os.path.join(path, "_navbar.md")
    oldsidebarpath = os.path.join(path, "_sidebar.md.bk")

    # path = os.path.abspath('.')
    # 删除旧备份，保存新备份
    os.popen(f'del {oldsidebarpath}')
    os.popen(f'copy {newsidebarpath} {oldsidebarpath}')
    # 生成新的侧边栏
    eachFile(os.path.join(path, 'docs'), os.path.join(path, "assets"))
    write2file(os.path.join(path, "_sidebar.md"), new_line, path)
    write2file(os.path.join(path, "README.md"), readmetext, path)
    os.popen(f'copy {newsidebarpath} {newnavbarpath}')
```


