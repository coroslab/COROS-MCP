[中文](README.md) | [English](README.en.md) | [Skill](skill/coros_mcp_login_gateway/SKILL.md)

# COROS MCP

> 将你的 COROS 运动、健康与训练数据安全连接到支持 MCP 的 AI 客户端。

[![COROS MCP](https://img.shields.io/badge/COROS-MCP-blue)](https://mcp.coros.com)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](skill/coros_mcp_login_gateway/SKILL.md)

COROS MCP 是 COROS 官方提供的 Model Context Protocol 能力。它在用户主动授权后，让 ChatGPT、Claude、Codex、OpenClaw 等支持 MCP 的 AI 客户端安全读取 COROS 服务器上的数据，用于运动分析、健康洞察、训练负荷解读、报告生成和训练计划辅助。

COROS 相信运动员应当拥有自己的数据，并能够以自己选择的方式使用这些数据。MCP 是这一理念在 AI 时代的直接落地：你用自然语言提出问题，AI 通过受控工具读取必要数据，并把数据转化为可理解、可行动的分析。

## 你可以这样使用

- 分析过去三个月的跑步量、配速、距离和训练负荷变化。
- 总结最近一个月的睡眠、静息心率、HRV、压力和恢复趋势。
- 在比赛前让 AI 结合当前训练状态，辅助规划接下来的训练安排。
- 生成年度、月度或单场赛事报告，并结合 FIT 原始文件做更深入分析。
- 查询设备、用户基础资料、训练日程、体能评估和恢复状态。

示例提问：

```text
请调用 COROS MCP，分析我过去 4 周的跑步训练负荷变化，并指出是否有过度训练风险。
```

```text
请查看我最近 30 天的睡眠、静息心率和恢复状态，帮我总结恢复质量趋势。
```

```text
我 6 周后有一场马拉松。请结合我最近的训练记录和体能评估，给出训练建议。
```

## 快速接入

### 方式一：HTTP OAuth

在支持远程 MCP 的客户端中添加下面的 MCP 服务地址：

```text
https://mcp.coros.com/mcp
```

客户端会引导你完成 COROS 账号授权。授权成功后，AI 客户端即可在你的许可范围内调用 COROS MCP 工具。

适合：ChatGPT、Claude、Codex 以及其他支持 HTTP/OAuth MCP 的客户端。

### 方式二：Agent Skill / OpenClaw

本仓库提供一个可用于 OpenClaw 的 Agent Skill，帮助 Agent 完成登录、区域选择、工具发现和 MCP 配置。

```bash
git clone https://github.com/coroslab/COROS-MCP.git
cd COROS-MCP/skill/coros_mcp_login_gateway

python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
openclaw mcp show coros
```

如果浏览器登录需要在另一台设备或手机上完成，建议使用两步流程：

```bash
python3 scripts/coros_mcp_login.py login-start
python3 scripts/coros_mcp_login.py login-finish
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

把 `skill/coros_mcp_login_gateway/` 放到 Agent 可读取的 skills 目录后，也可以直接对 Agent 说：

```text
使用 coros_mcp_login_gateway skill，帮我配置 COROS MCP。
```

部分 Claw 类 AI 助手也支持通过安装指令接入：

```bash
npm install -g coros-mcp
```

## 区域与连接入口

推荐优先使用统一入口：

```text
https://mcp.coros.com/mcp
```

该入口会根据账号所在区域自动选择合适的服务集群。少数 MCP 客户端可能不支持域名重定向，导致 URL 无效或连接失败。遇到这种情况时，可根据账号实际区域改用独立入口：

| 区域 | MCP 地址 |
| --- | --- |
| 中国大陆 | `https://mcpcn.coros.com/mcp` |
| 欧洲 | `https://mcpeu.coros.com/mcp` |
| 美国 | `https://mcpus.coros.com/mcp` |

如果不确定账号区域，先使用统一入口，或在 Skill 中让网关自动发现区域。

## 工具能力

COROS MCP 的工具会持续迭代。下表基于当前公开能力整理，若客户端显示的工具列表与本文略有差异，请以客户端刷新后的 MCP 工具列表为准。

状态说明：

- `available`：当前可用
- `new`：近期新增
- `planned`：即将推出或规划中

### Activity Analytics

| 工具 | 状态 | 能力 |
| --- | --- | --- |
| `querySportRecords` | available | 查询 COROS 运动记录，支持按日期、运动类型编码、距离、时长、配速和地点筛选，并返回后续查询所需的活动标识。 |
| `getActivityDetail` | available | 查询指定活动详情，包括心率、配速/速度、海拔、步频等综合指标。 |
| `analyzeActivityDetail` | available | 基于活动详情生成教练式分析，可指定关注配速、速度或心率。 |
| `queryActivityLapData` | new | 查询活动默认分圈或分段数据，按 COROS App 对应运动类型的展示字段返回。 |
| `queryCustomActivityLapData` | new | 查询活动内指定时间窗的自定义分段数据，适合分析最后 N 分钟或特定片段。 |
| `downloadActivityFitFiles` | new | 下载一个或多个活动的 FIT 文件，用于解析完整原始运动数据。 |
| `queryActivityFitFileDownloadUrls` | new | 获取活动 FIT 文件下载链接，适合客户端无法接收二进制文件时使用。 |

### Health & Recovery

| 工具 | 状态 | 能力 |
| --- | --- | --- |
| `queryDailyHealthData` | available | 查询每日健康总览，包括步数、卡路里、压力、睡眠和心率概览。 |
| `querySleepData` | available | 查询睡眠评分、主睡眠时长、深睡/浅睡/REM 比例、清醒情况、睡眠窗口和午睡信息。 |
| `querySleepHrv` | new | 查询睡眠 HRV 官方评估和原始曲线。 |
| `queryAvgHeartRate` | available | 查询每日平均心率趋势。 |
| `queryRestingHeartRate` | available | 查询每日静息心率趋势。 |
| `queryStressLevel` | available | 查询每日平均压力趋势。 |
| `queryHealthCheckTimeSeries` | new | 查询健康快测原始曲线，包括心率、HRV、压力、呼吸率和血氧；最近查询窗口最多 7 天。 |
| `queryStressTimeSeries` | new | 查询压力原始曲线点，包括时间、压力值、展示分数、压力 HRV 和压力心率值；查询窗口最多 7 天。 |
| `queryRecoveryStatus` | available | 查询当前恢复百分比、恢复等级和预计完全恢复时间。 |
| `queryMenstruationCycles` | new | 查询生理周期数据，包括今日状态、下次经期、每日阶段和周期范围。 |

### Training Management

| 工具 | 状态 | 能力 |
| --- | --- | --- |
| `queryFitnessAssessmentOverview` | available | 查询体能评估概览，包括 VO2max、跑力、阈值配速和 5K/10K/半马/全马成绩预测。 |
| `queryTrainingLoadAssessment` | available | 查询训练负荷评估，包括近期每日评语、短期负荷、长期负荷和负荷比。 |
| `queryTrainingSchedule` | available | 查询训练日程，默认返回本周计划，也支持指定日期范围。 |
| `queryTrainingPlanDetail` | planned | 查询训练计划详情，用于更新计划前确认当前计划、课程标识、预估指标和原始课程结构。 |
| `generateTrainingPlan` | planned | 根据结构化课程创建并保存 COROS 训练计划。 |
| `updateTrainingPlan` | planned | 更新已有 COROS 训练计划；建议先查询计划详情，只提交需要替换的课程。 |

### Device & Profile

| 工具 | 状态 | 能力 |
| --- | --- | --- |
| `queryDevices` | available | 查询用户绑定的 COROS 设备列表，包括设备 ID、固件类型和自定义名称。 |
| `queryUserInfo` | available | 查询用户基础资料，包括身高、体重、生日和性别。 |

使用 Skill 时，也可以动态读取服务端最新工具清单：

```bash
python3 scripts/coros_mcp_login.py list-tools
python3 scripts/coros_mcp_login.py describe-tool --tool queryUserInfo
python3 scripts/coros_mcp_login.py call-tool --tool queryUserInfo --arguments-json '{}'
```

## FIT 文件说明

COROS MCP 支持获取活动 `.fit` 文件，便于进行更深入的数据分析，也能避免把大量秒级数据直接塞进 AI 对话上下文。

可用方式：

- 直接获取 FIT 文件实体。
- 获取 FIT 文件下载链接，由客户端或用户自行处理。

注意：AI 客户端能否展示、下载或解析文件实体，取决于该平台自身能力与权限控制。

为保障服务稳定性，单个账号每个自然日最多可获取 **50 条** `.fit` 文件。

## 常见问题

### COROS MCP 需要付费吗？

COROS MCP 本身不收取费用。部分 AI 平台可能会对 MCP、外部工具连接、高级模型或开发者模式设置会员、订阅或额度限制，这些费用由对应平台收取。

### 授权失败怎么办？

请先确认：

1. COROS 账号可在 COROS App 中正常登录。
2. 账号内已有可查看的数据。
3. 授权页面完整打开，浏览器没有拦截弹窗或跳转。
4. 使用的是正确的 COROS 账号。
5. AI 平台内的旧连接已删除并重新授权。

如果多次重试仍失败，请保存报错截图并联系 COROS 客服排查。

### AI 拉取不到数据怎么办？

请确认对应数据已同步到 COROS App 并上传到云端。然后尝试新建对话窗口，或在支持的客户端中发送 `/new` 后重新提问。

提问时建议明确要求调用 COROS MCP，并给出时间范围和数据类型：

```text
请调用 COROS MCP，查看我最近 7 天的运动记录。
```

### 为什么 AI 回答不准确？

AI 的回答质量会受到模型能力、提问方式、可访问数据范围和工具调用稳定性的影响。若回答明显不准确，建议新建对话，明确要求调用 COROS MCP，并指定时间范围、运动类型或健康指标。

工具调用能力较弱的模型可能漏用工具或传入错误参数。建议使用具备稳定工具调用能力的模型。

### 我的数据安全吗？

只有在你主动授权后，AI 应用才可以通过 COROS MCP 访问授权范围内的数据。你的 COROS 数据仍受 COROS 账号体系和隐私政策保护；AI 对话内容和模型处理方式则受你所使用 AI 平台的政策约束。

建议只在你信任的平台上连接 COROS MCP，并在不再使用时从对应 AI 平台或 COROS 授权管理中移除连接。

## 仓库结构

```text
COROS-MCP/
├── README.md
├── README.en.md
└── skill/
    └── coros_mcp_login_gateway/
        ├── SKILL.md
        ├── scripts/
        │   └── coros_mcp_login.py
        └── tests/
            └── test_skill_script.py
```

## 开发

运行 Skill 的单元测试：

```bash
cd skill/coros_mcp_login_gateway
python3 -m unittest discover -s tests
```

## 链接

- COROS MCP: [https://mcp.coros.com](https://mcp.coros.com)
- MCP Endpoint: `https://mcp.coros.com/mcp`
- Agent Skill: [`skill/coros_mcp_login_gateway/`](skill/coros_mcp_login_gateway/)

## 许可

当前仓库暂未声明许可证。正式发布前请补充 `LICENSE` 文件。
