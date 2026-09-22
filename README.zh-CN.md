<p align="center">
  <a href="https://pallas-ads.com/"><img src="https://raw.githubusercontent.com/Jieyi-Deng/Pallas-ads/main/assets/pallas-logo.png" width="96" height="96" alt="Pallas 品牌标志"></a>
</p>

# Pallas

**在你自己的 Agent 中，完成广告数据分析。**

[English](README.md) | **简体中文** · [产品官网](https://pallas-ads.com/) · [npm](https://www.npmjs.com/package/pallas-ads)

Pallas 将广告数据分析带入 Codex 和 Claude Code。使用 Meta、Google Ads、TikTok Ads 的广告导出文件，或连接可用的媒体账户，通过自然语言提出分析需求。Pallas 检查数据、计算效果指标，并生成可以追溯到来源的分析报告。

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

> 请检查当前项目中的 Pallas、工作流 Skill 和分析 Skill 是否可用，告诉我是否可以开始分析广告数据。

这里的激活指在 Agent 中加载 Pallas。媒体账户授权是后面的独立步骤。

## 3. 分析你的数据

将广告平台导出的 CSV 或 XLSX 文件路径提供给 Agent：

> 请用 Pallas 分析 /path/to/my-ad-export.csv。先展示账户、日期范围、字段映射、币种、时区和缺失数据；我确认后再导入，生成包含投放表现、变化拆解和后续建议的报告。完成后给我 HTML 报告链接。

Pallas 会先预览数据的解释方式，由你确认分析口径后再保存导入。Agent 随后交付报告并解释主要发现。导出准备方式见[广告文件指南](FILE_IMPORT.md)。

## 4. 授权媒体账户

需要读取在线账户数据时，可以说：

> 请帮我将 Meta / Google Ads / TikTok Ads 账户连接到 Pallas。先检查当前 Agent 的连接配置，引导我完成浏览器授权，再列出可访问的广告账户。让我选择账户和报告期间后，再读取效果数据。

连接配置就绪后，在媒体平台页面完成登录与同意授权，回到 Agent 选择账户并开始分析。如果需要补充连接配置或账户访问权限，请按[媒体授权指南](AUTHORIZATION.md)操作，或联系 [support@pallas-ads.com](mailto:support@pallas-ads.com)。文件分析可以独立于账户授权使用。

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
