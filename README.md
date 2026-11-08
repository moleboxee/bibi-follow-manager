# BIBI 关注管理器

哔哩哔哩(B站)关注/粉丝管理工具 · **原生桌面应用**。零依赖 Python 标准库实现(桌面窗口需可选安装 pywebview),或直接使用打包好的免安装 exe。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![依赖](https://img.shields.io/badge/依赖-零-green) ![平台](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-yellow) ![版本](https://img.shields.io/badge/版本-v3.0-blue)

## 功能总览

**我的关注 / 我的粉丝**
- 全量加载(最高 2 万),头像、昵称、签名、关注日期、分组标签
- **互粉检测**(attribute=6 权威语义)、单向关注、特别关注、**已注销识别**、未分组 一键筛选
- **活跃度检测**:逐个查询最后投稿时间,无视频自动回退查动态(防误判),卡片显示「📡 N天前更新」
- 搜索 + 多维筛选 + 排序,条件自动记忆;卡片**右键菜单**(保护/复制UID/复制主页/回关/取关)
- 关注分组管理,批量移入

**批量操作(全链路防误伤 + 防风控)**
- 批量取关/回关/移入分组:**实时进度条**、随时停止、风控自动暂停并保留勾选
- **清理向导**:10+ 条件维度(关系/特别/分组/注销/时长/距上次投稿/关键词/无签名/勾选上限)+ **预设保存** + 实时计数
- **保护名单**:全选/向导/取关全链路跳过
- **每日取关预算**(可设,超限显著警告);实时批量统计

**变化报告(谁取关了你)**
- 每次加载自动对比本机快照:新增关注、不再关注、改名、新增粉丝、取关你的粉丝(自己的操作自动排除)

**常驻与提醒**
- 原生桌面窗口 + **深色标题栏** + **系统托盘**;关闭可最小化到托盘
- 每 60 分钟自动检查取关/掉粉,变化弹**系统通知**;开机自启动(可选)

**通用**
- 深色/浅色/**跟随系统** + 4 种主题色;快捷键 Ctrl+A / Ctrl+F / // Esc
- 统计面板(含已注销、双趋势图);**离线缓存**(风控期间照常可用)
- **全量备份/恢复**(换机迁移);清空缓存;操作日志
- 帮助中心(错误码对照、风控指引);版本更新检查
- 安全:仅监听 127.0.0.1 + Host 校验 + POST 令牌,防跨站操控

## 使用方法

### 方式一:免安装 exe(推荐)

到 [Releases](../../releases) 下载 `BIBI-Follow-Manager.exe`,双击即用,数据保存在 exe 同目录。

### 方式二:Python 运行

1. 安装 [Python](https://www.python.org/downloads/)(勾选 *Add to PATH*)
2. `pip install pywebview`(可选,启用桌面窗口模式)
3. 双击 `start.bat` 或执行 `python bibi_follow_manager.py`

> 缺 WebView2 或未装 pywebview 时自动回退浏览器;`BIBI_FORCE_BROWSER=1` 强制浏览器;单实例;仅监听本机。

### Cookie 登录(备用)

复制 `SESSDATA`、`bili_jct`、`DedeUserID` 三项粘贴:`SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx`

## 注意事项

- **风控**:频繁操作会触发 -352/-412 临时限制,程序自动暂停并保留勾选,等 30 分钟~几小时解除。建议每天取关 ≤300(可设预算,程序会提示今日累计)。
- 活跃度检测每用户 1 个请求,只检测向导筛出的候选池。
- 万级关注全量加载需 1-2 分钟;加载失败自动回退本地缓存。
- 本机数据文件均存程序目录(设置页可一键打开/导出备份),**勿外传、勿提交仓库**。
- exe 可能被个别杀软误报,可自行从源码构建。

## 目录结构

```
bibi-follow-manager/
├── bibi_follow_manager.py   # 主程序(前端与二维码库已内嵌)
├── start.bat                # Windows 一键启动(Python 方式)
├── build_exe.bat            # 一键打包免安装 exe
├── app.ico                  # 应用图标
├── .github/workflows/ci.yml # CI(多平台多版本语法检查)
└── README.md · LICENSE · .gitignore
```

## 免责声明

本项目仅供学习交流与个人账号管理使用,请勿用于批量营销、骚扰等任何违反B站用户协议的场景。使用本项目产生的一切后果由使用者自行承担。

接口参考: [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) · 二维码组件: [qrcode-generator (MIT)](https://github.com/kazuhikoarase/qrcode-generator)
