# Snows-Blog

基于 Hexo 搭建的个人博客源码仓库，当前使用 Butterfly 主题，主要用于沉淀后端开发、微服务、深度学习与计算机视觉方向的学习笔记与技术文章。

- 博客地址: <https://zhifengmuxue.top/>
- 框架: Hexo 8
- 主题: Butterfly
- 内容形式: Markdown + 文章资源目录

## 项目简介

这个仓库存放的是博客的源代码，而不是生成后的静态页面。  
你可以把它理解为博客的“写作后台”：

- `source/_posts` 用于存放文章与配图
- `themes/butterfly` 是当前主题
- `_config.yml` 负责站点配置
- `package.json` 负责依赖和常用脚本

如果你只是想阅读文章，直接访问线上博客即可；如果你想继续维护、迁移或二次开发这个博客，这个仓库就是入口。

## 技术栈

- **Hexo**: 静态博客框架
- **Butterfly**: 博客主题
- **Node.js / npm**: 依赖管理与构建运行
- **MathJax**: 数学公式渲染
- **hexo-abbrlink**: 固定文章链接
- **hexo-asset-img**: 文章资源目录图片引用
- **hexo-generator-search / feed / sitemap**: 搜索、订阅与站点地图

## 内容方向

当前博客内容主要围绕以下几个方向展开：

- Java 后端与 Spring 生态
- Spring Cloud 与微服务架构
- 深度学习与计算机视觉
- 图像处理与 OpenCV 实践
- 技术学习笔记与工程总结

## 目录结构

```text
Snows-Blog/
├─ source/               # 站点源文件
│  └─ _posts/            # 博客文章与文章资源目录
├─ themes/
│  └─ butterfly/         # Butterfly 主题
├─ scaffolds/            # 新文章模板
├─ _config.yml           # Hexo 主配置
├─ package.json          # 项目依赖与脚本
└─ README.md
```

## 环境要求

在本地运行本项目前，建议准备以下环境：

- Node.js 18 及以上
- npm
- Git

建议优先使用较新的 LTS 版本 Node.js，以避免 Hexo 及其插件的兼容性问题。

## 快速开始

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd Snows-Blog
```

### 2. 安装依赖

```bash
npm install
```

### 3. 本地预览

```bash
npm run clean
npm run build
npm run server
```

启动后可在本地访问：

```text
http://localhost:4000
```

## 常用命令

```bash
# 清理缓存与静态文件
npm run clean

# 生成静态文件
npm run build

# 启动本地预览服务
npm run server

# 部署到远端
npm run deploy
```

## 写作与维护说明

### 新建文章

可使用 Hexo 命令创建新文章：

```bash
npx hexo new "文章标题"
```

如果已经全局安装了 `hexo-cli`，也可以使用：

```bash
hexo new "文章标题"
```

### 图片与资源目录

当前项目启用了：

- `post_asset_folder: true`
- `hexo-asset-img`

因此推荐使用“文章文件 + 同名资源目录”的方式管理图片。例如：

```text
source/_posts/2026/06/2026-06-03.md
source/_posts/2026/06/2026-06-03/
```

在文章中插入图片时，优先使用：

```md
{% asset_img "image.png" "图片说明" %}
```

这种写法和当前仓库的文章组织方式最一致，也更适合长期维护。

### 数学公式

项目已经集成 `hexo-filter-mathjax`，文章 front matter 中可按需开启：

```yaml
mathjax: true
```

### 固定链接

项目使用 `hexo-abbrlink` 生成文章固定链接。  
发布文章后，建议保留已生成的 `abbrlink`，避免历史链接失效。

## 部署说明

当前项目使用 `hexo-deployer-git` 进行部署，部署配置位于根目录 `_config.yml` 的 `deploy` 段。

执行部署命令前，请确认：

- 远端仓库地址已正确配置
- 本机 SSH Key 或 Git 凭据可正常使用
- 站点基础配置（如 `url`、`author`）符合当前环境

部署命令：

```bash
npm run deploy
```

如果你是将该项目迁移到自己的环境，请优先修改以下配置：

- 站点地址 `url`
- 作者信息 `author`
- 部署仓库 `deploy.repo`
- 域名或服务器相关配置

## 恢复一个可运行的博客环境

如果你是从远端重新拉取该仓库，只需要完成下面几步：

```bash
git clone <your-repo-url>
cd Snows-Blog
npm install
```

然后执行：

```bash
npm run server
```

如果依赖安装正常，说明博客环境已经恢复成功。

## 致谢

- [Coolfan](https://yangyi.fan/)
- [Hexo](https://hexo.io/)
- [Butterfly Theme](https://butterfly.js.org/)


## 说明

本仓库主要用于个人博客内容维护与技术沉淀。  
如果你想基于这个仓库搭建自己的博客，建议将配置项、主题细节和部署目标替换为你自己的版本后再使用。
