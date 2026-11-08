# BIBI 关注管理器

哔哩哔哩(B站)关注/粉丝管理工具 · **原生桌面应用**。零依赖 Python 标准库实现(桌面窗口需可选安装 pywebview),或直接使用打包好的免安装 exe。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![依赖](https://img.shields.io/badge/依赖-零-green) ![平台](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能总览

**我的关注**
- 全量加载(最高 2 万),头像、昵称、签名、关注日期、分组标签
- **互粉检测**:互相关注 / 单向关注 / 特别关注 / 已注销 / 未分组 一键筛选
- **已注销账号识别**:自动打标灰色删除线徽章
- **活跃度检测**:逐个查询选中用户最后投稿时间(自动回退查动态,防误判),卡片显示「📡 N天前更新」
- 搜索(昵称、签名、UID)+ 多维筛选 + 排序,筛选条件自动记忆
- 关注分组:新建 / 删除,批量移入
- 批量取关:实时进度条、随时停止、触发风控自动暂停并保留勾选、**每日取关预算提示**

**我的粉丝**
- 全量加载,未回关检测、已注销筛选
- 一键回关(单个/批量,自动限速)

**变化报告(谁取关了你)**
- 每次加载自动与本机快照对比:新增关注(区分你回关的)/ 不再关注(区分你取关还是对方取关)/ 改名 / 新增粉丝 / 取关你的粉丝

**清理向导(按条件选择)**
- 10 个条件维度自由组合:关系方向、特别关注、分组、注销、关注时长、距上次投稿天数、关键词包含/排除、无签名、活跃度数据、勾选上限
- 全部实时计数,条件自动记忆,只帮你勾选、核对后才执行

**常驻与提醒**
- 原生桌面窗口 + **系统托盘**(显示/退出)
- 关闭最小化到托盘(可选);**每 60 分钟自动检查取关/掉粉**,发现变化弹系统通知
- 开机自启动(可选,写入注册表 Run 项)

**通用**
- 深色 / 浅色主题 + 4 种主题色;快捷键:Ctrl+A 全选、Ctrl+F / / 聚焦搜索、Esc 关弹窗
- 统计面板:关注、互粉率、特别关注、已注销、粉丝、近30天新增、关注趋势、粉丝历史趋势
- 操作日志(仅存本机);CSV / JSON 导出;批量参数可调
- 版本更新检查(GitHub Releases,可手动触发)
- 安全:仅监听 127.0.0.1 + Host 校验 + POST 令牌,防止其他网页跨站请求本机服务

## 使用方法

### 方式一:免安装 exe(推荐)

到 [Releases](../../releases) 下载 `BIBI-Follow-Manager.exe`,双击即用——
**原生桌面窗口**打开,无需安装 Python,数据文件自动保存在 exe 同目录。

### 方式二:Python 运行

1. 安装 [Python](https://www.python.org/downloads/)(勾选 *Add to PATH*)
2. `pip install pywebview`(可选,启用桌面窗口模式)
3. 双击 `start.bat`(或执行 `python bibi_follow_manager.py`)
4. 装了 pywebview 时以**原生桌面窗口**打开;未装则自动回退为浏览器打开 `http://127.0.0.1:8410`

> - 桌面窗口基于系统自带的 WebView2 运行时(Win10/11 一般自带);缺失时自动回退浏览器
> - 强制浏览器模式:环境变量 `BIBI_FORCE_BROWSER=1`
> - 单实例:重复启动会直接给运行中的程序再开一个窗口
> - 程序只监听本机 `127.0.0.1`,局域网内其他设备无法访问

### Cookie 登录(备用方案)

浏览器登录B站 → `F12` → Application → Cookies → 复制 `SESSDATA`、`bili_jct`、`DedeUserID`:

```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

缺少 `bili_jct` 时只能浏览,无法执行写操作。

## 注意事项

- **风控**:B站对频繁的取关/关注/翻页有临时限制(-412/-352),程序会自动暂停并保留勾选,一般等 30 分钟~几小时自动解除。建议每天取关不超过 300 人(程序会提示今日累计)。
- **活跃度检测**每用户 1 个请求,建议只检测向导筛出的候选池,不要全量检测。
- 万级关注全量加载需 1-2 分钟(每页随机间隔防风控)。
- 「移入分组」= 把用户加入目标分组(B站允许一人属多个分组),不从原分组移除。
- 本机数据文件(登录凭据 `bibi_data.json`、快照、日志、历史、活跃度缓存)均在程序目录,**勿分享、勿提交仓库**(已写 .gitignore),设置页可一键打开数据文件夹。
- PyInstaller 打包的 exe 可能被个别杀软误报,可自行从源码构建。

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
