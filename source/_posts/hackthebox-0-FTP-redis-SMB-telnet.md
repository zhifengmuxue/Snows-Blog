---
title: hackthebox 0:FTP redis SMB telnet
date: 2023-02-16 10:42:49
tags: [hackthebox,FTP,redis,SMB,telnet]
categories: 渗透笔记
---

 关于hackthebox上起点0的总结  ICMP Nmap ftp redis smb telnet 等

<!-- more -->

### 一、ICMP

使用ping工具检测目标存活情况

```
ping {ip}
```

### 二、nmap端口扫描

-sV 扫描服务版本 

-p 指定端口

-sC 默认副本扫描

```
nmap -sV -p 1-65535 -sC {ip}
```

### 三、telnet

Telnet协议是TCP/IP协议族中的一员，是Internet远程登录服务的标准协议和主要方式。它为用户提供了在本地计算机上完成远程主机工作的能力。在终端使用者的电脑上使用telnet程序，用它连接到服务器。终端使用者可以在telnet程序中输入命令，这些命令会在服务器上运行，就像直接在服务器的控制台上输入一样。可以在本地就能控制服务器。要开始一个telnet会话，必须输入用户名和密码来登录服务器。Telnet是常用的远程控制Web服务器的方法。

在kali中使用以下代码连接：

```
telnet {ip}
```

连接后需要登入

我们可以猜测用户名，进行暴力破解：

​				一般用户名：admin\administrator\root

​				密码可以先尝试空白登入

### 四、smbclient

SMB(全称是Server Message Block)，被用于Web连接和客户端与服务器之间的信息沟通

一般运行服务于445号端口，用于在计算机间共享文件、打印机、串口等

SMB工作过程：版本协商	会话请求凭据	文件路径凭据	对共享资源进行操作

**使用工具 smbclient**,尝试连接到远程主机并检查是否需要任何身份验证。如果不指定特定的用户名，就将使用攻击机的用户名登入。

**首先查看用户列表**

```
smbclient -L {ip}
```

ADMIN$：administrative share 是由 Windows NT 系列创建的隐藏网络共享，允许系统管理员远程访问
网络连接系统。这些共享可能不会被永久删除，但可能会被禁用

C$：共享c盘内容，这是对系统进行操作的位置

IPC$：进程间通信共享。用于管理进程，并且不是文件系统的一部分

WorkShares：访客

其中带$符号标识的都拥有管理员权限

**尝试登入**

```
smbclient \\\\ip\\{sharename}
```

### 五、redis-cli

redis（Remote Dictionary Server )，即远程字典服务，是一个开源的使用ANSI C语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。

像 Redis 这样的内存数据库通常用于缓存经常请求快速的数据检索。对于具有大量流量的站点，此配置允许更快地检索，大多数请求，同时在主数据库中仍具有稳定的长期存储

**使用工具 redis-cli**

连接代码：

```
redis-cli -h {ip}
```

**info** 查看详细

**info keyspace** 可以查看key空间 每一个数据库中的keys数量会显示出来

**select** 选择数据库 

keys *  列出所有key

### 六、ftp

ftp有三种用户：real、guest、anonymous

**real** :指在FTP服务上拥有帐号,当这类用户登录FTP服务器的时候，其默认的主目录就是其帐号命名的目录。但是，其还可以变更到其他目录中去.

**guest**:只能够访问自己的主目录

**anonymous**:匿名访问。这类用户是指在FTP服务器中没有指定帐户，但是其仍然可以进行匿名访问某些公开的资源。

```
ftp {ip}
Name(): 用户
```

