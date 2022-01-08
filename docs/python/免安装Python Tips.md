# 免安装Python Tips

python程序的发布总是有一些问题：如用户需要自己配python环境，打包的exe会报毒，打包后即使压缩了还是很大，源码被暴露...

用embed python搞定环境问题，搭配Cython来提速且避免源码暴露，不失为一种好方式。

## 一、embed python下载与文件布局

[python-3.9.7-embed-amd64.zip](https://www.python.org/ftp/python/3.9.7/python-3.9.7-embed-amd64.zip)

下载后解压后，将文件夹与源文件放在一起，可编写bat来直接执行。

```Bash
cd %~dp0
.\python39\python.exe .\main.py
pause
```

## 二、Cython 安装与使用
安装命令为
    ```Bash
    pip install Cython
    ```
以Hello World项目为例，需要创建 `hello.pyx`和 `setup.py`两个文件

```python
#file: hello.pyx
def say_hello_to(name):
    print("Hello %s!" % name)

```

```python
#file: [setup.py]
from distutils.core import setup
from Cython.Build import cythonize
setup(name='Hello world app',
    ext_modules=cythonize("hello.pyx"))

```

编译项目：`python setup.py build_ext --inplace`会生成 `hello.so`以及一些中间文件。生成后使用：

```python
coding: utf-8
# main.py
#这个import会先找hello.py,找不到就会找hello.so
import hello 
hello.say_hello_to('张三')

```

## 三、python绿色版安装lib

1. 查看当前已安装的lib:
运行cmd，目录切换至python-3.7.3rc1-embed-win32，输入
python.exe .\Scripts\pip3.exe list，结果如下：
    ```Bash
    D:\software\python-3.7.3rc1-embed-win32>python.exe .\Scripts\pip3.exe list

    Package    Version
    ---------- -------
    pip        19.2.1
    pywin32    224
    pywinauto  0.6.7
    setuptools 41.0.1
    six        1.12.0
    wheel      0.33.4

    ```

2. 安装新lib
以安装django为例，输入
    ```Bash
    python.exe .\Scripts\pip3.exe install django==1.10.1
    ```
    强制使用清华源下载则为
    ```Bash
    .\python.exe .\Scripts\pip3.7.exe install django==1.10.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```
