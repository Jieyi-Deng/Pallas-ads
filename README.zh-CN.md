# Pallas Ads

[English](README.md) · **本地分析 Alpha 0.2.0a1**

在自己的 Codex 或 Claude Code 中分析广告数据。Pallas 负责数据检查、计算和本地报告，Agent 负责对话与推理。

这里是**公开分发仓库**，完整开发仓库仍为私有。可下载的 Python wheel 包含可读运行时代码、两套 Skills 和报告模板，不是隐藏源码的二进制产品；分发内容保留 Apache-2.0 许可证。

## 一条 npm 命令安装

已提供 npm 格式安装器，当前可以直接从 GitHub 运行：

```sh
npx github:Jieyi-Deng/Pallas-ads#npm-v0.2.0-alpha.1 install
```

选择 Codex / Claude Code 和新的项目目录后，安装器自动处理 Python、MCP 与两套 Skills。需要 macOS（Apple Silicon / Intel）和 Node.js 22+，无需提前安装 Python。安装后在 Agent 打开生成项目并确认信任。

npm registry 的短命令 `npx pallas-ads install` 正等待发布者完成 npm 的安全验证；目前请使用上面的 GitHub 命令。支持 `doctor` 和 `update`，详见 [npm 安装器说明](NPM_INSTALLER.md)。现有 ZIP 入口仍保留。

## 让 Agent 安装

本地版需要安装，但下载、安装与配置可以交给 Agent。将下面这句话发给自己的 Codex 或 Claude Code：

> 请按照 https://github.com/Jieyi-Deng/Pallas-ads/blob/v0.2.0a1/INSTALL.md 为我当前的 Agent 安装 Pallas。使用新的项目目录和默认本地分析模式，下载并校验版本后完成安装，告诉我打开哪个项目并开始新任务。暂不连接真实媒体账户。

ZIP 路线需要 **macOS、Python 3.12 或 3.13、Codex / Claude Code**，安装依赖需要联网。安装器创建独立环境和项目，不覆盖已有项目或修改全局 Agent 配置。宿主要求的安装许可、项目信任和媒体同意仍由用户确认。默认本地分析无需额外 OpenAI 运行密钥、Meta 证书或 Google 开发者文件。

[安装说明](INSTALL.md) · [下载 v0.2.0a1](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/v0.2.0a1) · [测试与反馈流程](NEW_MACHINE_TESTING.md)

下载 Release 附件 `pallas-0.2.0a1-local-alpha.zip`。GitHub 自动生成的 Source code 压缩包只包含本分发仓库的文档，不是安装包。

## 首次分析

安装完成后，在 Agent 打开生成的项目、信任项目并开始新任务，说：

> 使用 Pallas 分析 samples/meta_campaign_daily.csv，先展示账户、期间、字段映射、币种、时区和缺失预览。我确认口径后再导入，生成三段式 HTML。区分实际观测、算术贡献和未验证业务原因。这是合成样例，不连接真实账户。

包内还提供 Google、TikTok 合成样例。真实 CSV/XLSX 需符合[支持格式](FILE_IMPORT.md)：单媒体、单账户、单币种、广告系列日粒度，不能有重复行或公式。不同文件独立保存，不自动跨文件相加。

## 本版能力与边界

已实现预览、确认、导入、共用报告，分析花费/展示/点击、CTR/CPC/CPM、变化的算术贡献和系列构成。空值不补零，缺乏转化或业务证据时不推断购买、盈利或素材疲劳。重复导入幂等，重启后可以继续使用留存数据。

801 项自动回归通过，并从独立安装环境验证了两种客户端配置的 MCP 合成流程。这不等于真人 Agent 完整遵循流程，也不等于真实账户数值对账通过。

实时媒体是可选实验能力，详见[媒体矩阵](NEW_MACHINE_TESTING.md#可选实时连接)。Google 实时连接需要维护者配置和平台准入；Meta/Claude 使用宿主官方 MCP，Meta/Codex 的显式预注册路线仍用于内测；不承诺所有陌生用户免邀请接入。TikTok 新账户资格也需实测。

本阶段不包含 ChatGPT 托管服务、多文件/多媒体自动整合或无人值守账户托管，不修改投放。

## 数据与反馈

Pallas 无遥测，证据本地保存；工具结果仍会提供给所选 Agent，并适用其数据政策。可选媒体请求会发送到对应平台。公开 Issue 不要上传凭据、原始账户导出或未审阅的私人报告。按测试说明准备并审阅脱敏反馈，打包不会自动上传。

这是个人 portfolio 项目，本版没有付费服务；不代表媒体或 Agent 提供商背书。

[许可证](LICENSE) · [NOTICE](NOTICE) · [商标说明](TRADEMARKS.md)
