#  Git踩坑记录

## git的一些报错解决方法
1. Git报错解决：OpenSSL SSL_read: Connection was reset, errno 10054 错误解决（但是每次都要搞一下）
   修改设置，解除ssl验证``git config --global http.sslVerify "false"``
2. Failed to connect to github.com port 443: Timed out 时，修改 ssh_config的配置，在文件中追加：
   ```
   Host github.com
   User git
   Hostname ssh.github.com
   PreferredAuthentications publickey
   IdentityFile ~/.ssh/id_rsa.pub
   Port
   ```
3. github加速，通过修改hosts的方式，打开 
```www.ipaddress.com``` 查询下面四个网站的 IP
    ```
    https://github.com/
    https://assets-cdn.github.com/
    http://global.ssl.fastly.net/
    codeload.github.com
    ```

## git的简单命令
1. <font color=green>本地代码强制覆盖</font>```git fetch --all && git reset --hard origin/master && git pull```

2. 配置用户名和邮箱

    ```shell
    $ git config --global user.name "your_username"  # 配置用户名
    $ git config --global user.email "your_email"  # 配置邮箱
    ```

3. 查看git中配置的用户名和邮箱

    ```shell
    $ git config user.name
    $ git config user.email
    ```

