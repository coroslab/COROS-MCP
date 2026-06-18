[中文](README.md) | [English](README.en.md) | [Skill](skill/coros_mcp_login_gateway/SKILL.md)

# COROS MCP

> 让 AI 客户端在用户授权后读取并分析 COROS 运动与健康数据。

[![COROS MCP](https://img.shields.io/badge/COROS-MCP-blue)](https://mcp.coros.com)
[![Skill](https://img.shields.io/badge/Agent-Skill-green)](skill/coros_mcp_login_gateway/SKILL.md)

这个仓库提供 Agent Skill、使用说明和 OpenClaw 接入脚本。当前连接入口是 `https://mcp.coros.com`，服务会自动选择合适的 CN、EU 或 US 区域。

## 架构

COROS MCP 负责登录授权和数据工具，本仓库负责把这些能力带到 Agent 和本地客户端中。

| 部分 | 作用 |
| --- | --- |
| COROS MCP 服务 | 处理登录授权，并提供运动、健康、训练等数据工具 |
| Agent Skill | 帮 Agent 自动配置 OpenClaw、完成登录、发现工具并调用工具 |
| README 文档 | 面向用户说明可以做什么、怎么开始使用 |

## 仓库结构

```text
coros-mcp/
├── skill/
│   └── coros_mcp_login_gateway/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── coros_mcp_login.py
│       └── tests/
│           └── test_skill_script.py
├── README.md
└── README.en.md
```

## 快速开始

### 在 OpenClaw 中配置 COROS MCP

```bash
git clone https://github.com/coroslab/coros-mcp.git
cd coros-mcp/skill/coros_mcp_login_gateway

python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
openclaw mcp show coros
```

如果登录需要在另一台设备或手机浏览器完成，可以使用更稳的两步流程：

```bash
python3 scripts/coros_mcp_login.py login-start
python3 scripts/coros_mcp_login.py login-finish
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

### 在 Agent 中使用这个 Skill

把 `skill/coros_mcp_login_gateway/` 放到你的 Agent 可读取的 skills 目录中，然后对 Agent 说：

```text
使用 coros_mcp_login_gateway skill，帮我配置 COROS MCP。
```

它会通过 `mcp.coros.com` 发起登录，保存本地登录状态，并把 COROS MCP 写入 OpenClaw。

## MCP 工具

当前 COROS MCP 公开的工具主要覆盖下面这些场景。

| 场景 | 工具 | 能做什么 |
| --- | --- | --- |
| 运动记录 | `querySportRecords` | 查询训练列表，可按日期、运动类型、距离、时长、配速、地点筛选 |
| 单次活动 | `getActivityDetail` | 查询一条活动的心率、配速、速度、爬升、步频等详情 |
| 活动分析 | `analyzeActivityDetail` | 用更像教练总结的方式解释一次训练 |
| 圈数与分段 | `queryActivityLapData` | 查询活动默认圈数或分段数据 |
| 自定义分段 | `queryCustomActivityLapData` | 按指定时间窗口查询一段训练数据，例如最后 5 分钟 |
| FIT 文件 | `downloadActivityFitFiles` | 下载一个或多个活动的 FIT 原始文件 |
| FIT 链接 | `queryActivityFitFileDownloadUrls` | 在客户端不能接收二进制文件时返回 FIT 下载链接 |
| 每日健康 | `queryDailyHealthData` | 查询步数、卡路里、睡眠、压力等每日概览 |
| 睡眠 | `querySleepData` | 查询睡眠评分、时长、深睡/浅睡/REM、清醒和小睡 |
| 心率 | `queryAvgHeartRate` | 查询每日平均心率趋势 |
| 静息心率 | `queryRestingHeartRate` | 查询静息心率趋势 |
| 睡眠 HRV | `querySleepHrv` | 查询睡眠 HRV 评估和原始时间序列 |
| 压力 | `queryStressLevel` | 查询每日平均压力趋势 |
| 健康检测 | `queryHealthCheckTimeSeries` | 查询最近一次完整健康检测的心率、HRV、压力、呼吸率、血氧 |
| 压力曲线 | `queryStressTimeSeries` | 查询一天或近几天的压力变化明细 |
| 体能评估 | `queryFitnessAssessmentOverview` | 查询 VO2max、跑步等级、阈值配速和比赛预测 |
| 训练负荷 | `queryTrainingLoadAssessment` | 查询近期训练负荷、长期负荷和负荷比例 |
| 恢复状态 | `queryRecoveryStatus` | 查询当前恢复百分比、恢复等级和预计完全恢复时间 |
| 训练安排 | `queryTrainingSchedule` | 查询本周或指定日期范围内的训练计划 |
| 设备 | `queryDevices` | 查询已绑定的 COROS 设备 |
| 用户资料 | `queryUserInfo` | 查询身高、体重、生日、性别等基础资料 |
| 经期 | `queryMenstruationCycles` | 查询经期状态、下次经期、周期范围和备注 |

你也可以让 skill 直接从 MCP 服务读取最新工具清单：

```bash
python3 scripts/coros_mcp_login.py list-tools
python3 scripts/coros_mcp_login.py describe-tool --tool queryUserInfo
python3 scripts/coros_mcp_login.py call-tool --tool queryUserInfo --arguments-json '{}'
```

## Skill 模块

| 模块 | 说明 | 路径 |
| --- | --- | --- |
| COROS MCP Skill | 登录 COROS MCP 并配置 OpenClaw | [`skill/coros_mcp_login_gateway/`](skill/coros_mcp_login_gateway/) |
| Skill 指令 | 告诉 Agent 何时使用、如何登录、如何发现和调用工具 | [`SKILL.md`](skill/coros_mcp_login_gateway/SKILL.md) |
| 登录脚本 | 执行登录、刷新、OpenClaw 配置、工具发现和工具调用 | [`coros_mcp_login.py`](skill/coros_mcp_login_gateway/scripts/coros_mcp_login.py) |

## 开发

```bash
cd skill/coros_mcp_login_gateway
python3 -m unittest discover -s tests
```

## 链接

- COROS MCP: [https://mcp.coros.com](https://mcp.coros.com)
- Skill: [`skill/coros_mcp_login_gateway/`](skill/coros_mcp_login_gateway/)

## 许可

当前仓库暂未声明许可证。正式发布前请补充 `LICENSE` 文件。
