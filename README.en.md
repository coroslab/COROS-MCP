[中文](README.md) | [English](README.en.md) | [Skill](skill/coros_mcp_login_gateway/SKILL.md)

# COROS MCP

> Securely connect your COROS activity, wellness, and training data to AI clients that support MCP.

[![COROS MCP](https://img.shields.io/badge/COROS-MCP-blue)](https://mcp.coros.com)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](skill/coros_mcp_login_gateway/SKILL.md)

COROS MCP is the official Model Context Protocol capability from COROS. After user authorization, it lets MCP-capable AI clients such as ChatGPT, Claude, Codex, and OpenClaw securely read data from COROS servers for activity analysis, wellness insights, training-load interpretation, report generation, and training-plan assistance.

COROS believes athletes should own their data and have the freedom to use it in the way they choose. MCP brings that belief into AI workflows: you ask in natural language, the AI retrieves the necessary data through controlled tools, and the data becomes understandable, actionable analysis.

## What You Can Do

- Analyze running volume, pace, distance, and training-load changes across the past few months.
- Summarize recent sleep, resting heart rate, HRV, stress, and recovery trends.
- Ask for training suggestions before a race based on recent workouts and fitness assessment data.
- Generate yearly, monthly, or race-specific reports, with deeper analysis from FIT files when needed.
- Query devices, profile basics, training schedules, fitness assessment, and recovery status.

Example prompts:

```text
Call COROS MCP and analyze how my running training load changed over the past 4 weeks. Flag any overtraining risk.
```

```text
Review my sleep, resting heart rate, and recovery status from the last 30 days, then summarize my recovery trend.
```

```text
I have a marathon in 6 weeks. Use my recent workouts and fitness assessment to suggest how I should train next.
```

## Quick Start

### Option 1: HTTP OAuth

Add the following MCP service URL to any remote-MCP client that supports HTTP and OAuth:

```text
https://mcp.coros.com/mcp
```

The client will guide you through COROS account authorization. After authorization, the AI client can call COROS MCP tools within the scope you approved.

Best for: ChatGPT, Claude, Codex, and other clients that support HTTP/OAuth MCP.

### Option 2: Agent Skill / OpenClaw

This repository includes an Agent Skill for OpenClaw. It helps an agent complete login, region selection, tool discovery, and MCP configuration.

```bash
git clone https://github.com/coroslab/COROS-MCP.git
cd COROS-MCP/skill/coros_mcp_login_gateway

python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
openclaw mcp show coros
```

If browser login needs to happen on another device or phone, use the two-step flow:

```bash
python3 scripts/coros_mcp_login.py login-start
python3 scripts/coros_mcp_login.py login-finish
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

After placing `skill/coros_mcp_login_gateway/` in a skills directory your agent can read, you can ask the agent:

```text
Use the coros_mcp_login_gateway skill to configure COROS MCP for me.
```

Some Claw-style AI assistants also support installation through a command:

```bash
npm install -g coros-mcp
```

## Regions and Endpoints

Use the global endpoint first:

```text
https://mcp.coros.com/mcp
```

The gateway selects the appropriate service cluster based on the region of your COROS account. A few MCP clients do not support domain redirects, which can lead to invalid URL or connection errors. In that case, use the standalone endpoint for your account region:

| Region | MCP URL |
| --- | --- |
| Mainland China | `https://mcpcn.coros.com/mcp` |
| Europe | `https://mcpeu.coros.com/mcp` |
| United States | `https://mcpus.coros.com/mcp` |

If you are unsure which region applies, start with the global endpoint or let the Skill discover the region through the gateway.

## Tool Capabilities

COROS MCP tools continue to evolve. The table below summarizes the current public capabilities. If your client shows a slightly different list, refresh the MCP tool catalog in that client and treat the live list as authoritative.

Status values:

- `available`: currently available
- `new`: recently added
- `planned`: coming soon or planned

### Activity Analytics

| Tool | Status | Capability |
| --- | --- | --- |
| `querySportRecords` | available | Query COROS activity records with filters for date, sport type code, distance, duration, pace, and location. Returns activity identifiers for follow-up queries. |
| `getActivityDetail` | available | Query detailed activity data including heart rate, pace/speed, elevation, cadence, and other metrics. |
| `analyzeActivityDetail` | available | Generate coach-style analysis from activity detail, with optional focus on pace, speed, or heart rate. |
| `queryActivityLapData` | new | Query default lap or segment data for an activity using the display fields for that sport type in the COROS App. |
| `queryCustomActivityLapData` | new | Query a precise time window inside an activity, such as the final N minutes or a selected segment. |
| `downloadActivityFitFiles` | new | Download FIT files for one or more activities for complete raw-data analysis. |
| `queryActivityFitFileDownloadUrls` | new | Get FIT file download URLs when the client cannot receive binary files directly. |

### Health & Recovery

| Tool | Status | Capability |
| --- | --- | --- |
| `queryDailyHealthData` | available | Query daily wellness overview including steps, calories, stress, sleep, and heart-rate summary. |
| `querySleepData` | available | Query sleep score, main sleep duration, deep/light/REM ratios, awake time, sleep window, and naps. |
| `querySleepHrv` | new | Query official sleep HRV assessment and raw HRV curves. |
| `queryAvgHeartRate` | available | Query daily average heart-rate trends. |
| `queryRestingHeartRate` | available | Query daily resting heart-rate trends. |
| `queryStressLevel` | available | Query daily average stress trends. |
| `queryHealthCheckTimeSeries` | new | Query raw wellness-check curves including heart rate, HRV, stress, respiration rate, and SpO2. Recent query windows are limited to 7 days. |
| `queryStressTimeSeries` | new | Query raw stress data points including time, stress value, display score, stress HRV, and stress heart-rate value. Recent query windows are limited to 7 days. |
| `queryRecoveryStatus` | available | Query current recovery percentage, recovery level, and estimated full recovery time. |
| `queryMenstruationCycles` | new | Query menstrual-cycle data including today's status, next period, daily phase, and cycle range. |

### Training Management

| Tool | Status | Capability |
| --- | --- | --- |
| `queryFitnessAssessmentOverview` | available | Query fitness assessment including VO2max, running performance, threshold pace, and 5K/10K/half-marathon/marathon predictions. |
| `queryTrainingLoadAssessment` | available | Query training-load assessment including recent daily comments, short-term load, long-term load, and load ratio. |
| `queryTrainingSchedule` | available | Query the training schedule for this week by default or for a specified date range. |
| `queryTrainingPlanDetail` | planned | Query training-plan detail before updates, including current plan, workout identifiers, estimated metrics, and original workout structure. |
| `generateTrainingPlan` | planned | Create and save a COROS training plan from structured workouts. |
| `updateTrainingPlan` | planned | Update an existing COROS training plan. Query details first and submit only workouts that need replacement. |

### Device & Profile

| Tool | Status | Capability |
| --- | --- | --- |
| `queryDevices` | available | Query bound COROS devices, including device ID, firmware type, and custom name. |
| `queryUserInfo` | available | Query profile basics such as height, weight, birthday, and gender. |

When using the Skill, you can also read the live tool catalog directly from the service:

```bash
python3 scripts/coros_mcp_login.py list-tools
python3 scripts/coros_mcp_login.py describe-tool --tool queryUserInfo
python3 scripts/coros_mcp_login.py call-tool --tool queryUserInfo --arguments-json '{}'
```

## FIT Files

COROS MCP supports retrieving activity `.fit` files for deeper data analysis. This also avoids pushing large second-by-second datasets directly into the AI conversation context.

Available methods:

- Retrieve the FIT file entity directly.
- Retrieve a FIT file download URL for the client or user to handle.

Note: Whether an AI client can display, download, or parse file entities depends on that platform's own capabilities and permission controls.

To protect service stability, each account can retrieve up to **50** `.fit` files per calendar day.

## FAQ

### Is COROS MCP free?

COROS MCP itself is free. Some AI platforms may apply membership, subscription, or quota limits to MCP, external tool connections, advanced models, or developer-mode settings. Those fees are charged by the platform, not by COROS.

### Authorization failed. What should I check?

First confirm:

1. Your COROS account can sign in normally in the COROS App.
2. Your account already has data that can be viewed.
3. The authorization page opened fully and the browser did not block pop-ups or redirects.
4. You signed in with the correct COROS account.
5. Old connections inside the AI platform were removed before reauthorization.

If repeated attempts still fail, save a screenshot of the error and contact COROS customer support.

### The AI cannot retrieve COROS data. What should I do?

Make sure the relevant data already exists in the COROS App and has been uploaded to the cloud. Then start a new conversation, or send `/new` in clients that support it, before asking again.

Use explicit prompts with a time range and data type:

```text
Please call COROS MCP and check my activity records from the past 7 days.
```

### Why are AI answers inaccurate?

Answer quality depends on model capability, prompt wording, accessible data range, and tool-call reliability. If an answer is clearly wrong, start a new conversation, explicitly ask the model to call COROS MCP, and specify the time range, activity type, or wellness metric.

Models with weak tool-calling capability may skip tools or pass incorrect arguments. Use a model with reliable tool-calling support when possible.

### Is my data safe?

An AI application can access data through COROS MCP only after you actively authorize it. Your COROS data remains protected by the COROS account system and privacy policy. AI conversation content and model processing are governed by the policies of the AI platform you use.

Connect COROS MCP only on platforms you trust, and remove the connection from the AI platform or COROS authorization management when you no longer use it.

## Repository Structure

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

## Development

Run the Skill unit tests:

```bash
cd skill/coros_mcp_login_gateway
python3 -m unittest discover -s tests
```

## Links

- COROS MCP: [https://mcp.coros.com](https://mcp.coros.com)
- MCP Endpoint: `https://mcp.coros.com/mcp`
- Agent Skill: [`skill/coros_mcp_login_gateway/`](skill/coros_mcp_login_gateway/)

## License

This repository does not declare a license yet. Add a `LICENSE` file before public release.
