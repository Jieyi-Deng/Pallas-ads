# Pallas 0.2.0a1 · 本地分析 Alpha 测试

面向 macOS + Codex / Claude Code，Python 3.12–3.13。本版优先验收安装、文件解释、分析思路和报告交付，真实广告材料可在之后补充。无数据可使用包内 samples 合成 CSV；它们不能作为真实效果验收。

## 一次自然语言安装

将测试 ZIP 解压，在该目录打开自己的 Agent，说：

> 请阅读 NEW_MACHINE_TESTING.md，用这里的 install_macos.py 和 wheel 安装 Pallas。
> 在我的主目录创建一个新的 pallas-test 文件夹；使用我当前的 Codex／Claude Code 客户端。
> 先检查 Python 3.12/3.13，再完成默认本地安装。暂不连接媒体、不准备证书，
> 不要求我提供任何 API key、Token 或 Google 配置文件。告诉我应打开哪个项目并开始新任务。

Agent 执行（选择 codex 或 claude）：

```sh
python3.13 install_macos.py --directory "$HOME/pallas-test" --client codex
```

安装器检查 wheel SHA-256，创建相邻的 pallas-test-runtime 环境，安装 Pallas 和依赖、MCP 配置与两套 Skills。只写新/空项目，不改全局配置或已有工作区。安装依赖需要联网；Python 和 Agent 不是包内软件。

完成后 **打开新生成的 pallas-test 文件夹，信任项目并开始新任务**。不同 Agent 使用不同目录。无需额外启动 MCP 终端。保留相邻 runtime 和 .pallas 目录。

检查命令：`pallas agent doctor --directory PROJECT`。默认仅把本地工作区、MCP 和 Skills 故障视为阻塞；未配置媒体标为可选缺失。它不证明真人授权或宿主工具加载成功。

安装中断后不要覆盖重装；先保留错误并检查已经创建的目录。项目存在时用 doctor 定位；只有 runtime 被创建时记录 pip 失败原因后由 Agent 修复该环境。

## 第一次报告

将包内 samples/meta_campaign_daily.csv 放在可访问位置，说：

> 请使用 Pallas 的工作流与分析 Skill 分析这份合成广告文件。先核对媒体、账户、
> 字段映射、日期、币种和时区，展示预览；我确认后导入并生成报告。
> 报告分为账户与期间总结、变化与原因拆解、主要发现与建议。
> 区分实际数字、算术贡献与业务假设，不猜测购买、利润或素材疲劳，不连接真实账户。

也可使用 Google/TikTok 样例，或按 FILE_IMPORT.md 准备真实导出。文件模式无需产品档案，不应为了生成报告要求用户先填写完整营销问卷。

## 本轮必测项目

| 项目 | 预期 |
|---|---|
| 默认安装 | 不索要运行密钥/Token；不要求 Google 配置或 Meta 证书；10 个 Pallas 工具与两套 Skills 可加载 |
| 文件预览 | 自动识别支持的列，展示范围与缺失；不修改源文件，不立即保存分析数据 |
| 用户确认 | 用户能看懂确认内容；Agent 不让用户填写 hash、dataset_id 或 JSON |
| CSV/XLSX | 同样数据得出同样指标；多个 sheet 时选择；公式/汇总/重复行/歧义日期给出具体错误 |
| 分析计算 | CTR=汇总点击/汇总展示，CPC=花费/点击，CPM=花费/展示×1000；缺失和零分母保持未知 |
| 分析思路 | 说明变化来自 CPM/CTR 的算术贡献及系列构成，业务原因标作假设并提出下一步核验 |
| 报告交付 | 共用三段式 HTML，单位清楚；聊天解释与报告一致，附件可打开 |
| 重复与重启 | 同文件重导不重复累计；重开项目后仍能从 dataset_id 生成报告；旧报告保留 |
| 限制 | 无产品/目标/转化证据时不编造；日期断档不推断趋势；不跨文件合计 |
| 反馈 | 原件本地保留，分享前审阅脱敏副本，不自动上传 |

状态用 passed / failed / blocked / not_run / not_applicable。请记录 OS、Agent/Pallas 版本、wheel SHA-256、步骤、预期/实际、错误与重试、用户额外操作次数。真实数据缺失填 not_run，不能用合成测试升级为 live passed。

## 可选实时连接

实时授权不是默认安装前置。免费个人项目也不代表任意媒体外部准入自动完成；下表是测试路线，不是无限公众接入承诺。

| 路线 | 使用方式 | 本版范围 |
|---|---|---|
| TikTok | 默认 Pallas 官方 MCP 连接 → 浏览器授权 → 选择账户 | 实验性，已有部分实测；新增测试者需验证实际账户 |
| Google | 需要维护者提供含已配置 Desktop 身份的构建，或已有显式运营者配置 | 无身份的 core 包仍可分析文件；不要让广告用户准备开发者凭据；外部受众及 API 项目权限另验收 |
| Meta / Claude Code | 安装时 `--client claude --enable-meta`；宿主 `/mcp` 授权 | 宿主持有令牌；无应用角色的新用户全流程待验收 |
| Meta / Codex | 维护者确认测试资格后，安装时显式提供 `--meta-client-id` | 预注册 App + 本机 HTTPS 的内测路线；不保证陌生用户免邀请 |

Codex Meta 只有明确选择后才生成本机证书。信任证书需要解释后用户确认，并显式使用 `--trust-local-certificate`；不在默认安装中触发。当前 App ID 和访问资格由维护者提供，不让普通广告用户创建应用。

按选择运行 `pallas agent doctor --directory PROJECT --media google`（或 meta、tiktok、all）。媒体失败记录具体阶段，可继续文件分析；不复制其他宿主的授权、不改用 Ads Manager 抓数。真人流程必须由用户完成登录、同意、MFA 与必要系统确认。

## 升级与卸载

此版是新版本，不覆盖 0.1.4 旧包。已安装用户升级 runtime 内的 wheel 前先备份整个本地项目；不删除 .pallas、不重新生成媒体证书、不复制其他人的令牌。安装器不覆盖已有项目。

升级运行时：`RUNTIME/bin/python -m pip install /absolute/new.whl`。已有项目 Skills 是安装时的副本，不会随 pip 自动更新；用 `pallas agent refresh-skills --directory PROJECT` 更新，它保留原 Skills 备份，之后重启 Agent 任务。如有自定义 Skill 改动，比较备份再合并。

移除本地测试时只清理由本次安装创建的项目/runtime；删除 .pallas 会删除本地分析数据。媒体远端授权需要在对应平台/宿主另行撤销，删除文件不等于撤销授权。

## 回传反馈

先运行 `pallas acceptance start --directory PROJECT/test-runs/UNIQUE_NAME`。在 RUN/share/SUMMARY.md 记录上述文件测试；既有 results.json 的媒体授权项按实际执行记录，未测保留 not_run。所有报告原件登记在 RUN/LOCAL_REPORT_INDEX.md，不自动回传原始 report.json、账户名称/ID、文件路径或凭据。

请 Agent 准备经脱敏且附件齐全的报告副本供用户审阅。用户确认后再运行 `pallas acceptance pack --directory RUN --reviewed`，用户自行决定是否发送 feedback.zip。不得用“已打包”表示已经发出。
