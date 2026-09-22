<p align="center">
  <a href="https://pallas-ads.com/"><img src="https://raw.githubusercontent.com/Jieyi-Deng/Pallas-ads/main/assets/pallas-logo.png" width="96" height="96" alt="Pallas 品牌标志"></a>
</p>

# Pallas

**在你自己的 Agent 中，完成广告数据分析。**

[English](README.md) | **简体中文** · [产品官网](https://pallas-ads.com/) · [npm](https://www.npmjs.com/package/pallas-ads)

Pallas 将广告数据分析带入 Codex 和 Claude Code。连接可用的 Meta、Google Ads、TikTok Ads 账户，或提供广告导出文件，通过自然语言提出分析需求。Pallas 检查数据、计算效果指标，并生成可以追溯到来源的分析报告。

访问 **[pallas-ads.com](https://pallas-ads.com/)**，了解产品与广告分析方法。

## 从广告数据到行动建议

- **了解投放表现。** 在明确的账户和日期范围内，查看花费、展示、点击及效率指标。
- **解释指标变化。** 分析广告系列构成与指标变化的算术原因；证据不足的业务解释会标明为待验证假设。
- **交付可回看的报告。** 报告包含账户与期间总结、变化拆解，以及主要发现和后续建议。
- **在 Agent 中持续沟通。** `pallas-workflow` 与 `pallas-analysis` 两套 Skills 为支持的数据来源提供一致的分析流程。

## 1. 安装

准备好 **macOS、Node.js 22 或更高版本，以及 Codex 或 Claude Code**，运行：

```sh
npx pallas-ads install
```

选择使用的 Agent 和一个新的项目文件夹。安装器会配置运行环境、MCP 连接与分析 Skills；需要时自动准备 Python。

也可以直接告诉 Agent：

> 请按照 https://github.com/Jieyi-Deng/Pallas-ads/blob/main/INSTALL.md 为我当前的 Agent 安装 Pallas。创建新的 Pallas 项目，检查安装结果，并告诉我打开哪个文件夹来激活它。

指定客户端的命令见[安装指南](INSTALL.md)。

## 2. 在 Agent 中激活

在 Codex 或 Claude Code 中打开安装器提示的文件夹，确认项目信任及所需 MCP 权限，然后开始新任务，让 Pallas 工具与 Skills 加载。

> 请检查当前项目中的 Pallas、工作流 Skill 和分析 Skill 是否可用，然后帮我准备需要连接的媒体账户。

这里的激活指在 Agent 中加载 Pallas。媒体账户授权是后面的独立步骤。

## 3. 授权媒体账户

告诉 Agent 你要分析的媒体平台：

> 请帮我将 Meta / Google Ads / TikTok Ads 账户连接到 Pallas。先检查当前 Agent 的连接配置，引导我完成浏览器授权，再列出可访问的广告账户。让我选择账户后，再读取效果数据。

连接配置就绪后，在媒体平台页面完成登录与同意授权，再回到 Agent 选择账户。如果需要补充连接配置或账户访问权限，请按[媒体授权指南](AUTHORIZATION.md)操作，或联系 [support@pallas-ads.com](mailto:support@pallas-ads.com)。

如果只分析上传的广告导出文件，可以跳过账户授权，使用下一步的文件分析方式。

## 4. 分析你的数据

选择读取已连接的广告账户，或上传广告导出文件。

### 直接读取广告账户

> 请用 Pallas 读取刚才授权的广告账户最近七个完整自然日的效果数据。先确认账户、报告日期、币种、时区和可用数据，再分析投放表现及变化，说明判断依据，并生成包含后续建议的 HTML 报告。

Agent 通过已配置的媒体连接获取数据，说明数据覆盖情况后再进行分析。你可以在同一段对话中继续追问账户表现和报告内容。

### 上传广告数据文件

如果 Agent 支持本地文件附件，直接上传 CSV 或 XLSX 广告导出文件；也可以提供文件的本地路径：

> 请用 Pallas 分析我上传的广告导出文件。先展示账户、日期范围、字段映射、币种、时区和缺失数据；我确认后再导入，生成包含投放表现、变化拆解和后续建议的报告。完成后给我 HTML 报告链接。

Pallas 会先预览数据的解释方式，由你确认分析口径后再保存导入。Agent 随后交付报告并解释主要发现。导出准备方式见[广告文件指南](FILE_IMPORT.md)。

## 5. 设置定时巡检

完成一次分析后，如果你的 Agent 提供定时任务功能，可以在同一个 Pallas 项目中安排重复巡检：

> 请帮我为刚才分析的广告账户设置每天上午 9 点的巡检。先与我确认时区、账户、报告期间和通知偏好。每次运行时使用 Pallas 读取最新数据，总结表现变化并保存报告；如果授权失效或取数失败，请明确报告。

由 Agent 管理执行时间，Pallas 负责分析。设置时确认定时任务能够访问项目、运行环境和已授权连接，并保持所需电脑或执行环境可用。基于文件的巡检需要在运行前提供更新后的导出文件；重复读取已保存的文件不会获取账户的新数据。

## 更新 Pallas

```sh
npx pallas-ads@latest update --directory /path/to/your-pallas-project
```

更新后重新开始 Agent 任务。[安装器说明](NPM_INSTALLER.md)提供检查与维护命令，版本变更记录见 [Releases](https://github.com/Jieyi-Deng/Pallas-ads/releases)。

## 数据处理

Pallas 在本地工作区保存导入证据和报告，不采集遥测。工具结果由你选择的 Agent 按其数据政策处理；连接媒体时，请求发送至对应平台。Pallas 分析广告表现，不修改广告投放。

## 联系支持

如有使用问题、连接配置或其他需要，请联系 **[support@pallas-ads.com](mailto:support@pallas-ads.com)**。反馈可复现的问题时，可参考[反馈指南](NEW_MACHINE_TESTING.md)。

[许可证](LICENSE) · [NOTICE](NOTICE) · [商标说明](TRADEMARKS.md)
