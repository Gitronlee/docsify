# Linux小白の小明起步


小明终于入职了，嘿嘿~ 可是要跟黑框的linux打交道，很慌~

- 嗯，本地电脑是windows的， 得先用ssh链接远程服务器`ssh ip ` eg:`ssh 192.168.1.2`
- 看一下登陆后我所在的目录是个啥：`pwd` 所在目录
- 嗯，晓得了。
顺便看下内存占用信息吧`free` :

    > ~$ free  
    > 总计         已用        空闲      共享    缓冲/缓存    可用  
    > 内存：     8037016     3030620     1761264      140448     3245132     4715392  
    > 交换：     2097148      333400     1763748  

- 不够直观，那看一下磁盘空间吧：`df -lh` :

    > ~$ df -lh  
    > 文件系统        容量  已用  可用 已用% 挂载点  
    > udev            3.9G     0  3.9G    0% /dev  
    > tmpfs           785M  2.0M  783M    1% /run  
    > /dev/sda5       117G   19G   92G   17% /  
    > tmpfs           3.9G  8.0K  3.9G    1% /dev/shm  
    > tmpfs           5.0M  4.0K  5.0M    1% /run/lock  

- 嗯，还行，那看看项目占用多少空间，`du -sh *` :

    > ~/mygit$ du -sh *  
    > 420M    gin-vue-admin  
    > ...

- 嗯还行，瞄一眼readme吧：`cat readme.md`
  哦，还行~
- 我是啥系统啊？`uname -a` 查看系统版本:

    > /mygit$ uname -a  
    > Linux ronlee-Aspire-V3-571G 5.11.0-34-generic #3620.04.1-Ubuntu SMP Fri Aug 27 08:06:32 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux  

   哦，原来是大名鼎鼎的乌班图啊~

- 要写golang，看看go装在哪了~

    > $ which go  
    > /usr/bin/go  

- 先下载个软件`wget xxx.tar.gz`
- 然后解压下载的压缩包`tar -zxvf xxxx.tar.gz` 解压
- 想找一下弹幕的go代码，唉，弹幕英文不会拼，就模糊查找下吧`find -name '*D*.go*'` 查找

    > ~/mygit$ find -name '*D*.go*'  
    > ./routes/DanmakuRoutes.go  
    > ./model/Danmaku.go  
    > ./dto/CommentDto.go  
    > ./dto/MessageDto.go  

- 不会写的英文干脆命名为拼音吧~~`mv Danmaku.go Danmu.go` 改名
- 看下机器在运行哪些进程`ps -ef `查看进程

    > ~/mygit$ ps -ef  
    > UID          PID    PPID  C STIME TTY          TIME CMD  
    > root           1       0  0 9月22 ?       00:02:38 /sbin/init splash  
    > root           2       0  0 9月22 ?       00:00:01 [kthreadd]  
    > root           3       2  0 9月22 ?       00:00:00 [rcu_gp]  
    > root           4       2  0 9月22 ?       00:00:00 [rcu_par_gp]  
    > root           8       2  0 9月22 ?       00:00:00 [mm_percpu_wq]  

    又多又看不懂，反正就是老nb了。。

- 不如筛选一下 `ps -ef | grep 'go'`  掷筛选go相关的进程

    > ~/mygit$ ps -ef | grep 'go'  
    > ronlee      1605    1526  0 9月22 ?       00:00:00 /usr/libexec/gvfs-goa-volume-monitor  
    > ronlee      1609    1526  0 9月22 ?       00:00:12 /usr/libexec/goa-daemon  
    > ronlee      1616    1526  0 9月22 ?       00:00:03 /usr/libexec/goa-identity-service  
    > ronlee   3370474 3370341  1 20:40 ?        00:00:17 /home/ronlee/go/bin/gopls -mode=stdio  
    > ronlee   3372299 3372298  0 21:03 ?        00:00:00 /usr/lib/git-core/git-remote-https origin https://github.com/Gitronlee/go-danmu.git  
    > ronlee   3372446 3370368  0 21:03 pts/1    00:00:00 grep --color=auto go  

    嗯 还行~

- 查看端口占用情况`netstat -ntlp `

    > ~/mygit$ netstat -ntlp  
    > （并非所有进程都能被检测到，所有非本用户的进程信息将不会显示，如果想看到所有信息，则必须切换到 root 用户）  
    > 激活Internet连接 (仅服务器)  
    > Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name  
    > tcp        0      0 127.0.0.1:16308         0.0.0.0:*               LISTEN      -  
    > tcp        0      0 127.0.0.1:36501         0.0.0.0:*               LISTEN      3369671/node  
    > tcp        0      0 192.168.194.38:26805    0.0.0.0:*               LISTEN      -  

- 早就知道`curl localhost：8082/xx` 可以访问网址
- 查看最近的日子记录`tail -n 10 log.log `最新十条的查看
- `kill -9` 杀死进程
- `top` 进程状态

    > 进程号 USER      PR  NI    VIRT    RES    SHR    %CPU  %MEM     TIME+ COMMAND  
    > 714 root      20   0  924304  18776  12824 S   2.7   0.2   1918:48 sunloginclient  
    > 1261 root      20   0 1169440  37316  15404 S   1.0   0.5   2467:44 Xorg  
    > 2895743 systemd+  20   0 2323516 400500  32464 S   1.0   5.0  33:26.24 mysqld  

- `chmod a+x start.sh` 加执行权限
- `history` 命令记录
嗯，还是很慌~~

