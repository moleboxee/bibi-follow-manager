# BIBI 关注管理器

哔哩哔哩(B站)关注/粉丝管理工具 · 本地网页版。**零依赖**,只需要电脑上装有 Python 3.8+(或直接使用打包好的 exe)。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![依赖](https://img.shields.io/badge/依赖-零-green) ![平台](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能

**我的关注**
- 扫码登录 / Cookie 登录,凭据只保存在本机
- 关注列表全量加载:头像、昵称、签名、关注日期、分组标签
- 互粉检测:一键筛出「互相关注 / 单向关注 / 特别关注 / 未分组」
- 搜索(昵称、签名、UID)+ 多维筛选 + 排序
- 关注分组:新建 / 删除,批量移入分组
- 批量取关:确认弹窗 → 自动分批限速,触发风控自动暂停
- 统计面板:关注数、互粉率、特别关注、近30天新增、近12周关注趋势图

**我的粉丝**
- 粉丝列表全量加载,未回关检测(已回关 / 未回关筛选)
- 一键回关:单个或批量,同样自动限速
- 导出粉丝列表

**通用**
- 深色 / 浅色主题切换
- 批量操作限速参数可调(设置页)
- 导出 CSV(Excel 可直接打开)/ JSON
- 快捷键:Ctrl+A 全选当前筛选结果

## 使用方法

### 方式一:Python 运行(推荐,体积最小)

1. 安装 [Python](https://www.python.org/downloads/)(安装时勾选 *Add to PATH*)
2. 双击 `start.bat`(或在本目录执行 `python bibi_follow_manager.py`)
3. 浏览器自动打开 `http://127.0.0.1:8410`,扫码登录

### 方式二:打包成免安装 exe

双击 `build_exe.bat`,完成后得到 `dist\BIBI-Follow-Manager.exe`,
双击 exe 即可运行,无需安装 Python。

> 程序只监听本机 `127.0.0.1`,局域网内其他设备无法访问。

### Cookie 登录(备用方案)

浏览器登录B站 → `F12` 开发者工具 → Application → Cookies →
复制 `SESSDATA`、`bili_jct`、`DedeUserID` 三项,按如下格式粘贴:

```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

缺少 `bili_jct` 时只能浏览列表,无法执行取关/回关/分组等写操作。

## 注意事项

- 批量取关/回关请**适量**:B站对频繁写操作有风控(返回 `-412`),程序遇到会自动暂停,等几小时再试。批量参数可在「设置」页调整。
- 关注/粉丝列表翻页接口对超大量数据(数千人)可能有分页限制,属B站接口限制。
- 「移入分组」的实现是 *把用户加入目标分组*(B站允许一人同时属于多个分组),不会从原分组移除。
- `bibi_data.json` 保存了你的登录凭据,**不要分享给他人、不要提交到公开仓库**(已写入 .gitignore)。
- PyInstaller 打包的 exe 可能被个别杀毒软件误报,属常见现象,可自行从源码构建。

## 目录结构

```
bibi-follow-manager/
├── bibi_follow_manager.py   # 主程序(前端页面与二维码库已内嵌)
├── start.bat                # Windows 一键启动(Python 方式)
├── build_exe.bat            # 一键打包免安装 exe
├── app.ico                  # 应用图标
├── .github/workflows/ci.yml # CI(多平台多版本语法检查)
├── README.md · LICENSE · .gitignore
```

## 免责声明

本项目仅供学习交流与个人账号管理使用,请勿用于批量营销、骚扰等任何违反B站用户协议的场景。使用本项目产生的一切后果由使用者自行承担。

接口参考: [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) · 二维码组件: [qrcode-generator (MIT)](https://github.com/kazuhikoarase/qrcode-generator)
