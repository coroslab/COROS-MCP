[中文](README.md) | [English](README.en.md) | [Skill](skill/)

# COROS MCP

[![COROS MCP](https://img.shields.io/badge/COROS-MCP-blue)](https://mcp.coros.com)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](skill/)

## Introduction

COROS has introduced MCP (Model Context Protocol), a secure and standardized bridge that allows AI to safely access your data on COROS servers. It is also the first officially supported MCP from a major sports watch brand.

Simply describe what you need in natural language, and AI can use COROS MCP to retrieve the relevant activity and health data from your COROS account for activity analysis, report generation, health insights, training plan creation, and more:

- "How has my running volume changed over the past three months?"

- "How has my sleep been over the past month?"

- "I have a marathon in six weeks. Based on my training so far, help me create a training plan."

- "Generate a 2026 London Marathon race report for me, with a tech-inspired visual style and running-themed imagery."

You can also use it to explore more possibilities and unlock the full value of your data. COROS believes athletes should own their own data and have the freedom to use it in whatever way they choose, and MCP is a direct expression of that belief.

You can configure COROS MCP on your preferred AI platform, such as ChatGPT, OpenClaw, or Codex. Connection methods are listed below.

## Setup Guide

Choose either of the following methods to quickly configure COROS MCP.

### HTTP OAuth

Add the following URL to your MCP client configuration:

https://mcp.coros.com/mcp

> Supports mainstream platforms such as ChatGPT, Codex, and Claude.

---

### SKILL

Send the following command to your AI assistant to install it through conversation:

npm install -g coros-mcp

> Supports OpenClaw, Workbuddy, Hermes, and other Claw-style AI assistants.

## Tool List

<details open>
<summary><strong>Activity Analytics</strong></summary>

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>Tool</th>
      <th align="left" width="480">Description</th>
      <th align="left" width="120" nowrap>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>querySportRecords</code></td>
      <td>Query COROS activity records with filters for date, sport type code, distance, duration, pace, and location. Returns activity IDs and time info needed for subsequent detail and lap queries.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>getActivityDetail</code></td>
      <td>Query detailed activity data including heart rate, pace/speed, elevation, cadence, and other comprehensive metrics.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>analyzeActivityDetail</code></td>
      <td>Generate coach-style analysis based on activity details, with optional focus on pace, speed, or heart rate.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryActivityLapData</code></td>
      <td>Query default lap or segment data for a specified activity, returned according to the display fields for that sport type in the COROS App.</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryCustomActivityLapData</code></td>
      <td>Query custom segment data within a precise time window of a specified activity, suitable for analyzing the last N minutes or a particular segment.</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>downloadActivityFitFiles</code></td>
      <td>Download FIT files for one or more activities for parsing complete raw activity data. Supports download by individual activity or date range.</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryActivityFitFileDownloadUrls</code></td>
      <td>Query raw download URLs for activity FIT files, as a fallback when the client cannot receive binary files.</td>
      <td nowrap><code>new</code></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><strong>Health &amp; Recovery</strong></summary>

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>Tool</th>
      <th align="left" width="480">Description</th>
      <th align="left" width="120" nowrap>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>queryDailyHealthData</code></td>
      <td>Query daily health overview including steps, calories, stress, sleep, and heart rate summary. For heart-rate-only queries, use the dedicated heart rate tools.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>querySleepData</code></td>
      <td>Query sleep score, main sleep duration, deep/light/REM ratios, wakefulness, sleep window, and nap information.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>querySleepHrv</code></td>
      <td>Query official sleep HRV assessment and raw curves. Daily averages, normal ranges, and evaluations are based on official assessment.</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryAvgHeartRate</code></td>
      <td>Query daily average heart rate trends.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryRestingHeartRate</code></td>
      <td>Query daily resting heart rate trends.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryStressLevel</code></td>
      <td>Query daily average stress trends.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryHealthCheckTimeSeries</code></td>
      <td>Query raw health check measurement curves including heart rate, HRV, stress, respiratory rate, and SpO2. Maximum query window is 7 days.</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryStressTimeSeries</code></td>
      <td>Query raw stress data points including time, stress value, display score, stress HRV, and stress heart rate. Maximum query window is 7 days.</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryRecoveryStatus</code></td>
      <td>Query current recovery percentage, recovery level, and estimated full recovery time.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryMenstruationCycles</code></td>
      <td>Query menstrual cycle data including today&#x27;s status, next period, daily phase, and cycle range.</td>
      <td nowrap><code>new</code></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><strong>Training Management</strong></summary>

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>Tool</th>
      <th align="left" width="480">Description</th>
      <th align="left" width="120" nowrap>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>queryFitnessAssessmentOverview</code></td>
      <td>Query fitness assessment overview including VO2max, Running Performance, threshold pace, and 5K/10K/half-marathon/marathon race predictions.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryTrainingLoadAssessment</code></td>
      <td>Query training load assessment including recent daily comments, short-term load, long-term load, and load ratio.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryTrainingSchedule</code></td>
      <td>Query training schedule. Defaults to this week&#x27;s plan and also supports specifying a date range. Results include internal identifiers for subsequent planning tools.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryTrainingPlanDetail</code></td>
      <td>Query training plan details for confirming the current plan, workout dayNo, idInPlan, estimated metrics, and original workout structure before updating a plan.</td>
      <td nowrap><code>coming&nbsp;soon</code></td>
    </tr>
    <tr>
      <td nowrap><code>generateTrainingPlan</code></td>
      <td>Create and save a COROS training plan based on designed structured workouts. Supports running, cycling, strength, rest workouts, and phase descriptions.</td>
      <td nowrap><code>coming&nbsp;soon</code></td>
    </tr>
    <tr>
      <td nowrap><code>updateTrainingPlan</code></td>
      <td>Update an existing COROS training plan. Plan details should be queried first, and only the dayNo workouts that need replacement should be submitted.</td>
      <td nowrap><code>coming&nbsp;soon</code></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><strong>Other</strong></summary>

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>Tool</th>
      <th align="left" width="480">Description</th>
      <th align="left" width="120" nowrap>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>queryDevices</code></td>
      <td>Query the list of COROS devices bound to the user, including device ID, firmware type, and custom name.</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryUserInfo</code></td>
      <td>Query basic user profile including height, weight, birthday, and gender.</td>
      <td nowrap></td>
    </tr>
  </tbody>
</table>

</details>

> Note: As the project continues to evolve, the MCP tool list may change. To view the latest available tools, manually refresh the MCP tool list in your AI platform.

## FAQ

#### 1. Which platforms does COROS MCP support?

MCP is an open standard for connecting external systems. You can think of MCP as a "USB port" for AI applications. Whether a platform can connect depends on whether it supports adding MCP services and whether it supports the authentication method required by COROS MCP.

We currently recommend using verified platforms first, such as ChatGPT, Claude, OpenClaw, Workbuddy, and Hermes.

If the platform you use does not yet support MCP, you can follow its future updates. Once the platform opens compatible MCP connection capabilities, you will be able to connect COROS according to that platform's rules.

#### 2. Do I need to pay to use COROS MCP?

COROS MCP itself is free of charge. You can authorize and connect your COROS account on AI platforms that support MCP, then use the currently available features.

Please note that some AI platforms may apply membership, subscription, or quota limits to MCP, external tool connections, advanced models, or developer mode settings. These fees are charged by the corresponding AI platform and are not determined by COROS. Please refer to the latest rules of the platform you use.

#### 3. Unable to complete authorization?

First, make sure your COROS account can log in and work normally in the COROS App, and that your account already contains data that can be viewed.

If authorization still fails, please check:

1. Whether the authorization page has fully opened, and whether your browser blocked pop-ups or redirects.

2. Whether you signed in with the correct COROS account.

3. Whether the old connection has been removed inside the AI platform and re-authorized.

If repeated attempts still fail, save a screenshot of the error message and contact COROS customer support for troubleshooting.

#### 4. MCP URL is invalid?

The current COROS MCP uses domain redirection technology (https://mcp.coros.com/mcp), which automatically switches to the best server based on the actual region of your account. However, some AI platforms do not support domain redirects, which may cause errors or connection failures.

If you encounter an invalid URL error, copy and enter the corresponding standalone routing URL based on the actual region of your account.

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>Account region</th>
      <th align="left" width="600">Standalone routing URL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap>Mainland China</td>
      <td nowrap><code>https://mcpcn.coros.com/mcp</code></td>
    </tr>
    <tr>
      <td nowrap>Europe</td>
      <td nowrap><code>https://mcpeu.coros.com/mcp</code></td>
    </tr>
    <tr>
      <td nowrap>United States</td>
      <td nowrap><code>https://mcpus.coros.com/mcp</code></td>
    </tr>
  </tbody>
</table>

#### 5. AI cannot retrieve COROS data?

If COROS MCP has been connected successfully but AI cannot retrieve data, try the following steps:

1. Confirm that the corresponding data already exists in the COROS App. Device data must first sync to the COROS App and then upload to the cloud. If the data does not exist in the App, AI cannot read it.

2. Open a new conversation window, or send `/new` in a supported client before asking again.

3. Use more explicit instruction, such as: "Please call COROS MCP and check my activity records from the past 7 days."

#### 6. Why are AI answers inaccurate?

AI response quality can be affected by model capability, prompt wording, accessible data range, and other factors.

If an answer is clearly inaccurate, try starting a new conversation, explicitly ask it to "call COROS MCP," and specify the time range and data type. For example: "Please call COROS MCP and analyze how my running training load changed over the past 4 weeks."

We recommend using models with capabilities equivalent to DeepSeek V4 Flash or higher. Models with weaker tool-calling capability may fail to use tools or may use incorrect parameters.

#### 7. Can COROS MCP retrieve .fit files?

**Yes.** COROS MCP supports retrieving `.fit` files for activity records, enabling deeper data analysis.

This approach also helps avoid overwhelming the AI context window with large amounts of second-by-second data.

We provide two ways to retrieve files:

- **Direct retrieval:** Read the `.fit` file entity directly.

- **Link retrieval:** Retrieve the file download link.

<strong>Note:</strong> Whether an AI assistant can directly display or process file entities depends on the capabilities and permission controls of the AI platform you are using. If a file cannot be downloaded or read, we recommend contacting customer support for the corresponding AI platform.

**Daily quota limit:** To ensure service stability, each account can retrieve up to **50** `.fit` files per calendar day.

#### 8. Who can see my data? Is it safe?

Only after you actively authorize access can an AI application access data within the authorized scope through COROS MCP. Your COROS data remains protected by the COROS account system and privacy policy. AI conversation content and model processing methods are governed by the policies of the AI platform you use. We recommend connecting COROS MCP only on platforms you trust.

## Notice

Use of COROS MCP is subject to the COROS [Terms of Service](https://coros.com/terms) and [Privacy Policy](https://coros.com/privacy). Before authorizing a third-party AI platform, make sure you understand how that platform handles conversations, files, and tool-call data. We recommend connecting COROS MCP only on platforms you trust and revoking access when you no longer use it.
