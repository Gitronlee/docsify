'''
Author: ronlee
Date: 2022-01-07 11:09:16
LastEditors: ronlee
LastEditTime: 2022-01-07 22:46:55
Description: 自动生成导航栏和侧边栏
FilePath: \_1_learn\docsify\autoNavbarFiles.py
'''
import os
import sys
import re
import shutil
new_line = ""  # 全局变量


def write2file(fname, rmovestr):
    global new_line
    # print(new_line.replace(rmovestr+"\\", ""))
    src_fobj = open(fname, 'a+', encoding='utf-8', errors='ignore')
    src_fobj.seek(0)
    src_fobj.truncate()
    src_fobj.flush()
    src_fobj.write(new_line.replace(rmovestr+"\\", "/").replace("\\", "/"))

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
        if os.path.isfile(newDir):  # 如果是文件
            if newDir.endswith('.md'):  # 如果是md文件
                new_line = new_line + GetFirstLine(newDir)
        elif s == "assets":
            print("newDir:", newDir)
            copy2assets(newDir, path)
        elif hasMDFile(newDir):
            # 如果不是文件，只递归有md文件的目录
            new_line = new_line + "* " + s + "\n\n"
            eachFile(newDir, path)


if __name__ == '__main__':
    path, filename = os.path.split(os.path.abspath(sys.argv[0]))
    print("当前路径：", path)
    newpath = os.path.join(path, "_sidebar.md")
    newpath2 = os.path.join(path, "_navbar.md")
    oldpath = os.path.join(path, "_sidebar.md.bk")

    # path = os.path.abspath('.')
    # 删除旧备份，保存新备份
    os.popen(f'del {oldpath}')
    os.popen(f'copy {newpath} {oldpath}')
    # 生成新的侧边栏
    eachFile(os.path.join(path, 'docs'), os.path.join(path, "assets"))
    write2file(os.path.join(path, "_sidebar.md"), path)
    os.popen(f'copy {newpath} {newpath2}')
    # todo：将每个assets下的图片文件放到根目录的assets文件夹下
