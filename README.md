<div align="center">

# 🚀 ImmortalWrt for Hiveton H5000M

**专为海微腾 Hiveton H5000M (MT7987A / Filogic 880 + MT5700M 5G) 深度定制的高性能、现代化 ImmortalWrt 固件自动化构建工程**

[![Build Firmware](https://github.com/loong486/immortalwrt-h5000m/actions/workflows/build-immortalwrt.yml/badge.svg)](https://github.com/loong486/immortalwrt-h5000m/actions/workflows/build-immortalwrt.yml)
[![Latest Release](https://img.shields.io/github/v/release/loong486/immortalwrt-h5000m?color=blue&logo=github&label=Release)](https://github.com/loong486/immortalwrt-h5000m/releases)
[![Target](https://img.shields.io/badge/Target-MediaTek%20Filogic%20880-orange?logo=openwrt)](https://openwrt.org)
[![Kernel](https://img.shields.io/badge/Kernel-Linux%206.12-informational?logo=linux)](https://kernel.org)
[![Modem](https://img.shields.io/badge/5G%20Modem-MT5700M%20NR-success)](#-5g-模块与现代化-qmodem-生态)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[固件特性](#-核心特性亮点) • [硬件规格](#-硬件与固件规格) • [快速刷机](#-快速刷机与升级指南) • [使用指引](#-核心功能配置指南) • [云端编译](#-云端自定义构建) • [开源致谢](#-开源致谢与上游项目)

</div>

---

## 📖 项目简介 (About)

本项目基于 **[ImmortalWrt 25.12](https://github.com/immortalwrt/immortalwrt)** 官方源码仓库，针对 **海微腾 Hiveton H5000M** 5G CPE / 路由器量身定制。依托 GitHub Actions 实现每周自动追踪最新上游源码与自动化云端构建。

### 为什么选择本项目？
* **解决原生系统痛点**：官方原生固件普遍存在设备树温控锁频竞争导致风扇啸叫或降频、缺少 MT5700M 5G 模组管理看板、缺乏短信自动转发等问题。
* **现代化组件全套重构**：
  - 模组控制彻底拥抱 **QModem 现代总线架构**，解决传统私有脚本抢占串口导致的掉线问题。
  - 核心代理换装极速轻量的 **OpenWrt-momo + sing-box 1.14+**，告别庞大冗余的旧式代理插件。
* **编译速度极致精简**：剥离重型交叉编译工具链（如 `llvm-bpf` 与巨型 Go 模块），将 GitHub Actions 云端编译时间由原本的 50+ 分钟大幅压缩至 **15~20 分钟**。
* **平滑升级与配置继承**：内建迁移清理脚本，支持无缝“保留配置升级”，升级固件后原有 Wi-Fi、代理订阅与基础网络设置不丢失。

---

## 📋 硬件与固件规格

| 属性 | 详细规格 |
| :--- | :--- |
| **设备型号** | 海微腾 Hiveton H5000M (5G CPE 高性能路由器) |
| **主控芯片 (SoC)** | 联发科 MediaTek Filogic 880 (MT7987A)，4 核心 ARM Cortex-A53 @ 2.0 GHz |
| **网络接口** | 2 × 2.5 Gbps (2.5G 网口) + 高性能 Wi-Fi 原生无线支持 |
| **5G 模组** | 鼎桥 TD Tech MT5700M 5G NR 工业级模组 (M.2 Key-B 接口) |
| **系统架构** | ARM64 (aarch64_cortex-a53) |
| **固件底包** | ImmortalWrt 25.12 分支（Linux 6.12 内核，全量 Firewall4 / nftables 架构） |
| **时区与语言** | 默认中国时区 (`Asia/Shanghai` / UTC+8)，全量集成简体中文语言包与亚洲时区库 |

---

## 🌟 核心特性亮点

### 1. 🌡️ 硬件级智能风扇温控 (DTS Patched)
* 自动注入专门针对 H5000M 定制的设备树 DTS 补丁，解除内核原生 Thermal Governor 的固定温控竞争。
* 深度整合 `luci-app-h5000m-fancontrol`，根据 CPU/5G 模组实时温度实现平滑阶梯调速，兼顾高负荷散热与日常静音。

### 2. 📶 5G 模块与现代化 QModem 生态
* **无冲突串口总线**：基于 `ubus-at-daemon` 统一调度，避免多程序争抢物理串口导致模组掉线。
* **开机自动 SIM 卡初始化**：集成 `qmodem-mt5700-fix` 服务，开机自动执行 `AT^SCICHG=0,1` 唤醒 SIM 卡槽，彻底根除基带返回 `+CME ERROR: 10`（SIM 未识别）的问题。
* **现代化模组控制后台 (`luci-app-qmodem-next`)**：
  - 官方现代响应式管理后台，提供实时会话式短信收发与完整短信转发配置。
* **MT5700 专属独立现代 WebUI 看板 ([inotdream/mt5700webui-openwrt-server](https://github.com/inotdream/mt5700webui-openwrt-server))**：
  - 集成 `at-webserver` 与 `luci-app-at-webserver`，提供独立前端界面（浏览器访问 `http://192.168.1.1/5700/`）。
  - 拥有专属可视化仪表盘、载波聚合 (CA) 状态、夜间/日间定时自动锁频/锁小区、微信通知及交互式 AT 终端。

### 3. 📩 全自动多通道短信转发 (`sms-forwarder-next`)
* 收到运营商流量提醒、验证码或欠费短信时，无需打开路由后台，系统通过后台守护进程即时推送到您的随身设备。
* **原生支持主流渠道**：
  - **Telegram Bot**（支持自定义 Bot Token 和 Chat ID）
  - **通用 Webhook**（完美兼容 **Bark**（iOS 推送）、**企业微信机器人**、**钉钉机器人**、**PushPlus** 等）
  - **Server酱 / PushDeer**
  - **自定义 Shell 脚本**（支持通过环境变量获取短信内容、发件人与时间戳自由扩展）

### 4. ⚡ Momo (sing-box 1.14+) 高性能透明代理
* 选用社区备受好评的轻量级透明代理方案 **[OpenWrt-momo](https://github.com/nikkinikki-org/OpenWrt-momo)**，原生利用 Linux `nftables` 实现极速 TProxy / TUN 流量劫持。
* 核心引擎升级至 **sing-box 1.14+** 最新版本，占用极低，NAT 转发性能拉满。
* 预置 `zoneinfo-asia` 时区数据库，解决 Go 语言程序日志与系统时间偏差 8 小时的问题。

### 5. 📂 生产力与文件服务 (OpenList & FRP)
* **OpenList 4.2.6**：内置官方最新版本，支持将阿里云盘、115、百度网盘、WebDAV、本地移动硬盘等统一聚合挂载，支持 Web 浏览与本地 FUSE 映射。
* **FRP 内网穿透**：集成 `luci-app-frpc`，配合远端 VPS 实现无公网 IP 场景下的安全内网穿透。
* **MiniUPnPd (nftables)**：完美适配 Firewall4，游戏主机与下载工具端口自动映射。

---

## 📦 插件矩阵与上游致谢 (Credits)

| 功能分类 | 插件 / 组件名称 | 上游维护者 | 上游项目仓库 | 核心功能说明 |
| :--- | :--- | :--- | :--- | :--- |
| **系统核心** | ImmortalWrt 源码 | ImmortalWrt Team | [immortalwrt/immortalwrt](https://github.com/immortalwrt/immortalwrt) | 固件核心底包 (25.12, Linux 6.12) |
| **硬件温控** | `luci-app-h5000m-fancontrol` | FAN789 | [FAN789/luci-app-h5000m-fancontrol](https://github.com/FAN789/luci-app-h5000m-fancontrol) | H5000M 硬件风扇温控与调速 |
| **MT5700 独立看板** | `at-webserver` / `luci-app-at-webserver` | inotdream | [inotdream/mt5700webui-openwrt-server](https://github.com/inotdream/mt5700webui-openwrt-server) | MT5700 模组现代化看板、WebSocket 守护与定时锁频 |
| **5G 协议栈** | `qmodem` / `luci-app-qmodem-next` | FUjr | [FUjr/QModem](https://github.com/FUjr/QModem) | QModem 核心、AT 守护与现代 Web 界面 |
| **短信自动转发**| `sms-forwarder-next` | FUjr | [FUjr/QModem](https://github.com/FUjr/QModem) | 多平台短信监听与 Webhook 自动转发 |
| **网络代理** | `luci-app-momo` / `momo` | Joseph Mory | [nikkinikki-org/OpenWrt-momo](https://github.com/nikkinikki-org/OpenWrt-momo) | 现代轻量 nftables 透明代理 |
| **代理内核** | `sing-box` (v1.14+) | SagerNet | [SagerNet/sing-box](https://github.com/SagerNet/sing-box) | 全协议现代代理引擎 |
| **聚合网盘** | `luci-app-openlist` / `openlist` | OpenListTeam | [OpenListTeam/OpenList-OpenWRT](https://github.com/OpenListTeam/OpenList-OpenWRT) | 多存储与网盘聚合管理系统 |
| **内网穿透** | `luci-app-frpc` / `frpc` | fatedier | [fatedier/frp](https://github.com/fatedier/frp) | 高性能反向代理通道 |
| **端口映射** | `miniupnpd-nftables` | Thomas Bernard | [miniupnp/miniupnp](https://github.com/miniupnp/miniupnp) | Firewall4 原生 UPnP IGD 映射服务 |

---

## 🛠️ 快速刷机与升级指南

### 1. 默认登录信息
* **管理后台 IP**：`192.168.1.1`
* **默认用户**：`root`
* **默认密码**：无密码（初次进入直接点击登录）

### 2. 升级固件 (保留现有配置)
如果您目前正在运行本固件或兼容系统：
1. 从 GitHub 仓库的 **[Releases](https://github.com/loong486/immortalwrt-h5000m/releases)** 页面下载最新的 `sysupgrade.bin` 固件包。
2. 进入路由器后台：**系统 → 备份/升级 → 刷写固件**。
3. 上传固件包，**勾选“保留配置”**，确认刷写。
4. > **提示**：固件内置了自动化迁移清理脚本（`99-cleanup-legacy`），首次启动会自动重置旧版菜单临时缓存并清理残留旧配置，原有的 LAN IP、Wi-Fi 密码、Momo 节点规则均会完好保留。

### 3. 全新安装 (不保留配置)
首次从官方原厂固件或其他第三方固件切换时，建议取消勾选“保留配置”进行全新刷写，以获得最纯净稳定的运行环境。

---

## ⚙️ 核心功能配置指南

### 📶 5G 模组与联网调试
* 固件启动后会自动识别 MT5700M 并完成 SIM 初始化。
* 可在 **调制解调器 (Modem) / 服务** 中查看模组连接状态，或通过专属的 **AT WebServer (`/5700/`)** 看板进行详细射频参数、载波聚合 (CA) 监控与锁频配置。

### 🎛️ MT5700 独立看板 (AT WebServer)
* **独立前端访问**：浏览器直接打开 `http://192.168.1.1/5700/` 即可进入专属 MT5700 管理控制台。
* **参数配置**：进入后台 **服务 → AT WebServer**：
  * **网络连接（推荐）**：连接模式选择 `NETWORK`，IP 设为 `192.168.8.1`，端口 `20249`（MT5700 模组默认网关地址）。
  * **串口连接**：连接模式选择 `SERIAL`，设备路径选择 `/dev/ttyUSB0`（波特率 `115200`）。
  * 勾选“启用服务”并保存应用，后台守护进程将自动启动，提供实时信号曲线、CA 载波聚合查看、定时锁频与微信通知。

### 📩 配置短信自动转发
1. 进入后台：**调制解调器 → 短信 → 短信转发**。
2. 勾选 **启用短信转发服务**。
3. 添加转发实例：
   * **Telegram 示例**：选择 `Telegram Bot`，配置 JSON：
     ```json
     {
       "bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
       "chat_id": "987654321"
     }
     ```
   * **Bark 示例 (iOS)**：选择 `Generic Webhook`，配置 JSON：
     ```json
     {
       "webhook_url": "https://api.day.app/YOUR_BARK_KEY/$sms_body?title=收到新短信($sms_sender)"
     }
     ```
   * **企业微信群机器人示例**：选择 `Generic Webhook`，指向企微 Webhook 地址即可。

### 🚀 Momo 代理配置
1. 进入后台：**服务 → Momo**。
2. 在订阅设置中填入您的代理节点订阅链接，更新节点。
3. 推荐使用 **TProxy 模式**（nftables 原生转发，性能最佳）。勾选“启用”并点击“保存并应用”。

---

## 💻 云端自定义构建

本项目完全基于 GitHub Actions 自动化运维：

### 1. 快速 Fork 编译属于自己的固件
1. 点击本仓库右上角 **Fork** 到您的个人 GitHub 账号。
2. 进入您 Fork 后的仓库页面：**Settings → Actions → General → Workflow permissions**，勾选 **Read and write permissions** 并保存。
3. 进入 **Actions** 标签页，在左侧选择 **Build ImmortalWrt H5000M Firmware**，点击右侧 **Run workflow** 即可开始全自动云端构建。
4. 构建完成后，前往 **Releases** 即可下载生成的固件。

### 2. 升级与调整 sing-box 核心版本
如需体验未来最新发布的 sing-box，仅需修改 [`scripts/diy-part2.sh`](scripts/diy-part2.sh) 第 9 行：
```bash
SING_BOX_VERSION="1.14.2"  # 直接修改为您需要的版本号
```
提交代码后，GitHub Actions 将会自动以指定版本完成拉取与编译。

---

## 📂 仓库文件组织

```text
immortalwrt-h5000m/
├── .github/
│   └── workflows/
│       └── build-immortalwrt.yml     # GitHub Actions 自动化云端编译流水线
├── config/
│   └── h5000m.config                 # H5000M 固件编译种子配置文件
├── patches/
│   └── h5000m-userspace-fan-control.patch # 设备树 DTS 用户态智能温控补丁
├── scripts/
│   ├── diy-part1.sh                  # 编译前阶段：自定义 Feed 软件源注册
│   └── diy-part2.sh                  # 编译中阶段：插件拉取、版本覆盖与迁移注入
├── .gitignore                        # Git 版本控制忽略配置
├── LICENSE                           # MIT 开源授权协议
└── README.md                         # 项目使用说明文档
```

---

## 📜 开源许可

本项目源码及相关脚本基于 [MIT License](LICENSE) 协议开源。集成的第三方软件包与插件均遵循其各自的原生开源协议。
