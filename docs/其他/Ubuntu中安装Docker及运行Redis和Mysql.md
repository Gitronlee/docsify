# Ubuntu中安装Docker及运行Redis和Mysql

## 1. Docker安装

```Bash
 # 来自菜鸟教程，简单的安装命令
 curl -sSL https://get.daocloud.io/docker | sh
```

```Bash
# 查看其版本
docker version
```

```Bash
# Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
#:~$ service docker start
# * Docker must be run as root
sudo service docker start
```

```Bash
#下载容器镜像，运行进程启动一个容器
sudo docker search tutorial
sudo docker pull learn/tutorial
sudo docker run learn/tutorial echo "hello world"

```

```Bash
# 安装ping命令
sudo docker run learn/tutorial apt-get install -y ping
```

```Bash
# 获得安装完后的容器的id
sudo docker ps -l
```

```Bash
sudo docker commit 1a9 learn/ping
```

```Bash
# :~$ sudo docker run learn/ping ping www.baidu.com
# docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "ping": executable file not found in $PATH: unknown.
# -c 命令表示后面的参数将会作为字符串读入作为执行的命令。 因此在docker中 很多命令行 如Dockerfile 的cmmand 中均使用 "/bin/sh","-c"
sudo docker run learn/ping /bin/sh -C && ping www.baidu.com
```

## 2. 在Docker 中运行Redis 和 Mysql

拉取对应的镜像 ``docker pull redis:latest``   ``docker pull mysql:latest``

运行Redis容器 ``sudo docker run -itd --name redis-test -p 6379:6379 redis``

```shell
sudo docker exec -i redis-test bash   
redis-server --versionredis
```


运行Mysql容器 ``sudo docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql``

进入到Mysql中的终端 ``sudo docker exec -it mysql-test bash`` 并登陆 Mysql ``mysql -h localhost -u root -p``

创建数据库 ``CREATE DATABASE IF NOT EXISTS DANMUDATA DEFAULT CHARSET utf8 COLLATE utf8_general_ci;``

---
参考 菜鸟教程、 官方Docker getting started
