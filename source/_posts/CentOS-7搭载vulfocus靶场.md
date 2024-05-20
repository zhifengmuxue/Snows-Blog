---
title: CentOS 7搭载vulfocus靶场
date: 2023-02-07 22:47:33
tags: [指南,vulfocus]
categories: 网络安全
---

 在CentOS 7 虚拟机上搭载vulfocus靶场

后续使用doker ps -a; docker start {id};开启靶场

<!-- more -->

### 一、挂载镜像

​			mkdir /mnt/cdrom  创建挂载点

​			mount  /dev/cdrom  /mnt/cdrom	挂载

### 二、配yum源

​			cd  /etc/yum.repos.d/

​			vim CentOS-Media.repo

```
[c7-media]
name=CentOS-$releasever - Media
baseurl=file://mnt/cdrom
gpgcheck=0
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
```

### 三、docker安装

```
curl -sSL https://get.daocloud.io/docker | sh
```

启动：systemctl start docker

卸载：yum remove docker-ce删除安装包

​			rm -rf /var/lib/docker删除镜像等

### 四、部署vulfocus环境

拉取镜像：docker pull vulfocus/vulfocus:latest

查看库：docker images (取得IMAGE ID)

```
docker run -d -p 映射端口:80 -v /var/run/docker.sock:/var/run/docker.sock -e VUL_IP=(CentOS主机IP) (IMAGE ID)
```

对于我：

```
docker run -d -p 8081:80 -v /var/run/docker.sock:/var/run/docker.sock -e VUL_IP=10.0.0.128 8e55f85571c8
```

用浏览器访问地址的映射端口

admin/admin

### 五、开启

systemctl start docker 开启docker

docker ps -a 查看创建容器

找到对应的ID后，docker start id

