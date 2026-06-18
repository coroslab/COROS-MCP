[中文](README.md) | [English](README.en.md) | [Gateway Skill](skill/coros_mcp_login_gateway/SKILL.md)

# COROS MCP

> The integration home for COROS MCP: Agent Skill, usage docs, and lightweight helpers for connecting to the COROS MCP gateway.

[![MCP Gateway](https://img.shields.io/badge/MCP-Gateway-blue)](https://mcp.coros.com)
[![Skill](https://img.shields.io/badge/Agent-Skill-green)](skill/coros_mcp_login_gateway/SKILL.md)

COROS MCP lets MCP-capable AI clients read a user's COROS activity and wellness data after authorization. The current gateway is `https://mcp.coros.com`, which automatically routes the session to the CN, EU, or US cluster.

## Architecture

This repository focuses on the client integration side of COROS MCP. The hosted MCP service handles authentication and data tools; this repository brings those capabilities into agents and local clients.

| Part | Purpose |
| --- | --- |
| COROS MCP Gateway | Unified entry point for login, regional routing, and MCP calls |
| `coros_mcp_login_gateway` Skill | Helps an agent configure OpenClaw, complete login, discover tools, and call tools |
| README Docs | Explain what COROS MCP can do and how to start using it |

## Repository Structure

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

## Quick Start

### Configure COROS MCP in OpenClaw

```bash
git clone https://github.com/coroslab/coros-mcp.git
cd coros-mcp/skill/coros_mcp_login_gateway

python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
openclaw mcp show coros
```

If the browser login needs to happen on another device, use the more resilient two-step flow:

```bash
python3 scripts/coros_mcp_login.py login-start
python3 scripts/coros_mcp_login.py login-finish
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

### Use This Skill With an Agent

Put `skill/coros_mcp_login_gateway/` in a skills directory your agent can read, then ask the agent:

```text
Use the coros_mcp_login_gateway skill to configure COROS MCP for me.
```

The skill starts login through `mcp.coros.com`, stores local login state, and writes the COROS MCP entry into OpenClaw.

## MCP Tools

COROS MCP currently exposes tools for these main scenarios.

| Scenario | Tool | What it does |
| --- | --- | --- |
| Workout records | `querySportRecords` | Query workout lists with optional date, sport type, distance, duration, pace, and location filters |
| Activity detail | `getActivityDetail` | Query heart rate, pace, speed, elevation, cadence, and other details for one activity |
| Activity analysis | `analyzeActivityDetail` | Explain one workout in a coach-style summary |
| Laps and segments | `queryActivityLapData` | Query default lap or segment data for an activity |
| Custom segment | `queryCustomActivityLapData` | Query a selected time window, such as the final 5 minutes of a workout |
| FIT files | `downloadActivityFitFiles` | Download one or more original activity FIT files |
| FIT URLs | `queryActivityFitFileDownloadUrls` | Return FIT download URLs when the client cannot receive binary files |
| Daily health | `queryDailyHealthData` | Query daily summaries such as steps, calories, sleep, and stress |
| Sleep | `querySleepData` | Query sleep score, duration, deep/light/REM sleep, awake time, and naps |
| Heart rate | `queryAvgHeartRate` | Query daily average heart-rate trends |
| Resting heart rate | `queryRestingHeartRate` | Query resting heart-rate trends |
| Sleep HRV | `querySleepHrv` | Query sleep HRV assessment and raw time-series points |
| Stress | `queryStressLevel` | Query daily average stress trends |
| Wellness check | `queryHealthCheckTimeSeries` | Query heart rate, HRV, stress, respiration rate, and SpO2 from the latest complete wellness check |
| Stress timeline | `queryStressTimeSeries` | Query detailed stress changes for a day or recent days |
| Fitness assessment | `queryFitnessAssessmentOverview` | Query VO2max, running level, threshold pace, and race predictions |
| Training load | `queryTrainingLoadAssessment` | Query recent training load, long-term load, and load ratio |
| Recovery | `queryRecoveryStatus` | Query current recovery percentage, recovery level, and estimated full recovery time |
| Training schedule | `queryTrainingSchedule` | Query this week's schedule or a custom date range |
| Devices | `queryDevices` | Query bound COROS devices |
| User profile | `queryUserInfo` | Query profile basics such as height, weight, birthday, and gender |
| Menstrual cycle | `queryMenstruationCycles` | Query cycle status, next period date, date ranges, and notes |

You can also let the skill read the live tool catalog directly from the MCP service:

```bash
python3 scripts/coros_mcp_login.py list-tools
python3 scripts/coros_mcp_login.py describe-tool --tool queryUserInfo
python3 scripts/coros_mcp_login.py call-tool --tool queryUserInfo --arguments-json '{}'
```

## Skill Modules

| Module | Description | Path |
| --- | --- | --- |
| Gateway Skill | Logs in through `mcp.coros.com` and configures OpenClaw | [`skill/coros_mcp_login_gateway/`](skill/coros_mcp_login_gateway/) |
| Skill Instructions | Tells the agent when to use the skill and how to login, discover tools, and call tools | [`SKILL.md`](skill/coros_mcp_login_gateway/SKILL.md) |
| Login Helper | Handles login, refresh, OpenClaw configuration, tool discovery, and tool calls | [`coros_mcp_login.py`](skill/coros_mcp_login_gateway/scripts/coros_mcp_login.py) |

## Development

```bash
cd skill/coros_mcp_login_gateway
python3 -m unittest discover -s tests
```

## Links

- COROS MCP Gateway: [https://mcp.coros.com](https://mcp.coros.com)
- Skill: [`skill/coros_mcp_login_gateway/`](skill/coros_mcp_login_gateway/)

## License

This repository does not declare a license yet. Add a `LICENSE` file before public release.
