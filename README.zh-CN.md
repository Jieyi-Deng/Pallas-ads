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
- **在 Agent 中持续沟通。** `pallas` 统一入口将分析与持久看板请求交给对应 Skill，并使用经过校验的报告模板。

报告会跟随用户请求的语言：中文请求生成中文报告，其他语言暂统一生成英文报告，适用于分析报告、广告看板和竞品研究。显式指定报告语言时优先采用该要求；后台刷新看板时保留已保存的语言。

## 1. 安装

准备好 **macOS、Node.js 22 或更高版本，以及支持插件的 Codex 或 Claude Code**。

直接告诉 Agent：

> 请按照 https://github.com/Jieyi-Deng/Pallas-ads 中的 PLUGIN_INSTALL.md 安装 Pallas 插件，然后用它的 setup Skill 为当前项目完成初始化。

也可以直接添加插件源并安装：

**Codex 终端**

```sh
codex plugin marketplace add Jieyi-Deng/Pallas-ads
codex plugin add pallas@pallas-ads
```

**Claude Code**

```text
/plugin marketplace add Jieyi-Deng/Pallas-ads
/plugin install pallas@pallas-ads
```

安装与旧项目迁移见[插件指南](PLUGIN_INSTALL.md)。使用项目安装方式的用户仍可通过 [npm 安装器](INSTALL.md)运行 `npx pallas-ads install`。

## 2. 在 Agent 中激活

打开你希望保存广告数据的项目，让 `pallas-setup` Skill 完成初始化。确认项目信任及所需权限，然后重新加载或开始新任务。

> 请为当前项目初始化 Pallas，检查它的 11 个工具与 6 个 Skills 是否可用，包括 Pallas 命令和看板 Skill，然后帮我准备需要连接的媒体账户。

初始化会准备运行环境并将 Pallas 绑定到当前项目。媒体账户授权是后面的独立步骤。

## 3. 授权媒体账户

告诉 Agent 你要分析的媒体平台：

> 请帮我将 Meta / Google Ads / TikTok Ads 账户连接到 Pallas。先检查当前 Agent 的连接配置，引导我完成浏览器授权，再列出可访问的广告账户。让我选择账户后，再读取效果数据。

连接配置就绪后，在媒体平台页面完成登录与同意授权，再回到 Agent 选择账户。如果需要补充连接配置或账户访问权限，请按[媒体授权指南](AUTHORIZATION.md)操作，或联系 [support@pallas-ads.com](mailto:support@pallas-ads.com)。

如果只分析上传的广告导出文件，可以跳过账户授权，使用下一步的文件分析方式。

## 4. 分析你的数据

选择读取已连接的广告账户，或上传广告导出文件。

在 Claude Code 中使用 `/pallas:pallas analysis` 或 `/pallas:pallas dashboard`。如果希望使用 `/pallas analysis` 和 `/pallas dashboard`，让 setup 为当前项目添加命令别名。Codex 中选择已安装的 `pallas` Skill，或在宿主支持时使用 `$pallas analysis` / `$pallas dashboard`。设置与示例见[命令指南](PALLAS_COMMAND.md)。

### 直接读取广告账户

> 请用 Pallas 读取刚才授权的广告账户最近七个完整自然日的效果数据。先确认账户、报告日期、币种、时区和可用数据，再分析投放表现及变化，说明判断依据，并生成包含后续建议的 HTML 报告。

Agent 通过已配置的媒体连接获取数据，说明数据覆盖情况后再进行分析。你可以在同一段对话中继续追问账户表现和报告内容。

### 上传广告数据文件

如果 Agent 支持本地文件附件，直接上传 CSV 或 XLSX 广告导出文件；也可以提供文件的本地路径：

> 请用 Pallas 分析我上传的广告导出文件。先展示账户、日期范围、字段映射、币种、时区和缺失数据；我确认后再导入，生成包含投放表现、变化拆解和后续建议的报告。完成后给我 HTML 报告链接。

Pallas 会先预览数据的解释方式，由你确认分析口径后再保存导入。Agent 随后交付报告并解释主要发现。导出准备方式见[广告文件指南](FILE_IMPORT.md)。

### 保留并更新广告看板

> 请用 Pallas 为我选定的账户或已确认文件创建看板，将历史保存在当前项目，展示可用的投放与素材明细，并给我 HTML 链接。后续更新沿用同一个看板，说明缺失或过期的数据来源。

看板保留已有日期并更新选定来源。文件来源需要提供新导出才能更新；缺失的转化和素材明细保持不可用。更新看板不会自动创建定时任务。

## 5. 设置定时巡检

完成一次分析后，如果你的 Agent 提供定时任务功能，可以在同一个 Pallas 项目中安排重复巡检：

> 请帮我为刚才分析的广告账户设置每天上午 9 点的巡检。先与我确认时区、账户、报告期间和通知偏好。每次运行时使用 Pallas 读取最新数据，总结表现变化并保存报告；如果授权失效或取数失败，请明确报告。

由 Agent 管理执行时间，Pallas 负责分析。设置时确认定时任务能够访问项目、运行环境和已授权连接，并保持所需电脑或执行环境可用。基于文件的巡检需要在运行前提供更新后的导出文件；重复读取已保存的文件不会获取账户的新数据。

## 更新 Pallas

GitHub 分发已包含原生插件 **0.2.4** 与 runtime **0.2.0a6**。npm **0.2.0-alpha.6** 现已发布，并设为 `latest`。两个渠道均已提供本次报告语言更新。

通过 Agent 的插件管理器更新，再为每个 Pallas 项目运行 setup Skill，随后开始新任务。详见[插件更新与恢复](PLUGIN_INSTALL.md#update)。

仍使用 npm 安装方式的项目，请使用 [npm 更新命令](NPM_INSTALLER.md)。当前 GitHub 文件的组件版本见 [release.json](release.json)，registry 可用版本见 [npm 包页面](https://www.npmjs.com/package/pallas-ads)；两个渠道可能在不同时间更新。历史版本见 [Releases](https://github.com/Jieyi-Deng/Pallas-ads/releases)。

## 数据处理

Pallas 在本地工作区保存导入证据和报告，不采集遥测。工具结果由你选择的 Agent 按其数据政策处理；连接媒体时，请求发送至对应平台。Pallas 分析广告表现，不修改广告投放。

## 联系支持

如有使用问题、连接配置或其他需要，请联系 **[support@pallas-ads.com](mailto:support@pallas-ads.com)**。反馈可复现的问题时，可参考[反馈指南](NEW_MACHINE_TESTING.md)。

[许可证](LICENSE) · [NOTICE](NOTICE) · [商标说明](TRADEMARKS.md)
