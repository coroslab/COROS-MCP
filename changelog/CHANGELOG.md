# Changelog

[English](CHANGELOG.md) | [中文](CHANGELOG.zh.md) | [Back to README](../README.md)

Explore COROS MCP updates.

### 2026-10-23

- Removed the `analyzeActivityDetail` tool.
- Fixed an issue that prevented some AI clients (including Gemini and DSH) from loading COROS tools ([#10](https://github.com/coroslab/COROS-MCP/issues/10)).
- Fixed some known issues.

### 2026-09-21

- Use AI to create road running, trail running, and cycling plans and workouts based on your fitness and goals, and sync them to COROS. Plans must be 4–16 weeks long.
- Save to your Training Plan Library or Workout Library without a start date, or schedule on your Training Calendar starting anytime from today to 14 days from now.
- Search and edit plans and workouts with AI; delete them in the COROS app.

### 2026-09-09

- COROS is now listed in the Doubao plugin directory. Add it directly without manual configuration.

### 2026-08-27

- COROS is now listed in the Workbuddy connector directory. Add it directly without manual configuration.

### 2026-07-24

- COROS is now listed in the [Claude connector directory](https://claude.ai/directory/coros). Add it directly without manual configuration.

### 2026-07-01

- COROS is now listed in the [ChatGPT plugin directory](https://chatgpt.com/plugins/plugin_asdk_app_6a0694cbb2608191bbefb74ba810ab68). Add it directly without manual configuration.

### 2026-06-24

- Improved Skill login and tool calling for the stateless MCP endpoint.

### 2026-06-23

- Support querying workout split data.
- Support querying workout feedback and notes.
- Support retrieving workout record `.fit` files, including GPS and second-by-second data; limited to 50 file requests per calendar day.
- Fixed issues that caused workout summary data to be missing in some cases.
- Support querying menstrual cycle data.
- Support querying stress time-series data.
- Support querying health check time-series data.
- Support querying sleep HRV time-series data.
- Fixed several known issues.

### 2026-05-19

- Added cross-region login with a unified endpoint: `https://mcp.coros.com/mcp`.

### 2026-05-09

- Added Skill access: `npm install -g coros-mcp`.

### 2026-05-05

Initial launch with queries for:

- Workout records, workout summaries, and training schedules.
- Fitness metrics: VO2max, Running Performance, threshold pace, and race predictions.
- Training status: weekly training load, training volume assessment, and recovery status.
- Daily health data: steps, calories, workout duration, sleep, average heart rate, average HRV, average stress, and resting heart rate.
- User information and linked devices.
