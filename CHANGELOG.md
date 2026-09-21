# Changelog

All notable changes to COROS MCP are documented here.

### 2026-09-21 — Documentation and skill guidance

- Updated the English and Chinese tool catalogs to match the current server source, including training-plan library/details, plan creation and updates, workout-library tools, scheduling, and standalone scheduled-workout creation/details/updates.
- Replaced outdated training tool names and coming-soon labels; clarified running, cycling and trail-running support and the distinction between library templates and scheduled copies.
- Added skill routing and write-safety guidance: inspect live schemas, read before editing, preserve complete days or courses as required, and verify uncertain write outcomes before retrying.
- Corrected current health-check date-range and FIT download-window descriptions; historical entries below remain a record of earlier releases.
- This update changes documentation only; it does not deploy server changes or publish an npm package. Tool availability follows each connected server's refreshed catalog.

### 2026-06-24

- Improved the SKILL login and tool-calling flow to support the new stateless MCP endpoint without relying on the `Mcp-Session-Id` session header.

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

- Support cross-region login authentication, consolidating 3 URLs into `https://mcp.coros.com/mcp`.

### 2026-05-09

- Support connecting to COROS MCP via Skill: `npm install -g coros-mcp`.

### 2026-05-05

- Support querying workout records.
- Support retrieving workout summary data.
- Support querying fitness metrics including VO2max, Running Performance, threshold pace, and race predictions.
- Support querying weekly training load, training volume assessment, and recovery status.
- Support querying user training schedules.
- Support querying daily steps, calories, workout duration, and weekly training load.
- Support querying daily sleep data.
- Support querying daily average heart rate, average HRV, average stress level, and resting heart rate.
- Support querying basic user information.
- Support querying bound user devices.
