English | [中文](README.zh.md) | [Setup Guide](docs/en/getting-started.md) | [Tool Guide](docs/en/tools.md) | [FAQ](docs/en/faq.md) | [Changelog](changelog/CHANGELOG.md)

# COROS MCP

**Connect COROS with AI. Put your training data to work.**

COROS MCP lets you use your preferred AI assistant to query activity and health data, review performance, and create or adjust training plans and workouts—all through conversation.

COROS believes athletes should own their data and be free to choose how they use it. Through MCP (Model Context Protocol), you can authorize an AI platform of your choice to access your COROS data and explore new ways to use it.

## What you can do

### Review your training and see what has changed

From laps in a single run to months of training trends, let AI answer your questions using your actual records.

> “Compare my last two long runs. How did my pace and heart rate differ in the second half?”

### Understand your body's response

Review sleep, HRV, heart rate, stress, and activity records together to understand recent changes and how they relate to your training.

> “Summarize my sleep and HRV trends over the past two weeks alongside my training volume. What has changed?”

### Turn training ideas into a schedule

Build a plan around your current fitness and race goals and save it to COROS. You can also create individual workouts or adjust sessions already on your schedule.

> “I'm preparing for a half marathon in 8 weeks. Review my recent training and fitness data, draft a plan, and save it to COROS after I confirm.”

### Find your own ways to use your data

Create an annual activity map, generate a personal training report, or build your own training assistant. Combined with your AI platform's other capabilities, you can also research routes, organize race information, and bring COROS data into more of what you do.

These are just starting points. How you use your activity data is up to you.

## Quick start

COROS is available in the following official plugin or connector directories. Add it directly without configuring an MCP URL.

| Platform | Add COROS |
|---|---|
| ChatGPT | [Open the plugin directory](https://chatgpt.com/plugins/plugin_asdk_app_6a0694cbb2608191bbefb74ba810ab68) |
| Claude | [Open the connector directory](https://claude.ai/directory/coros) |
| Doubao Work | Search for **COROS** in the plugin directory |
| Workbuddy | Search for **COROS** in the connector directory |

Follow the prompts to add COROS, sign in, and authorize access. Then start a conversation.

For other platforms, manual MCP setup, or Skill access, see the [Setup Guide](docs/en/getting-started.md).

## Capabilities

| Feature | What it supports |
|---|---|
| Activity records and details | Query activities, detailed metrics, laps, and custom segments; retrieve FIT files. |
| Health and recovery | Query sleep, HRV, heart rate, stress, daily health data, health checks, menstrual cycles, and recovery status. |
| Fitness and training load | View fitness assessments, race predictions, and training load. |
| Training plans and workouts | Query, create, and modify training plans and workouts; schedule workouts on your training calendar. |
| Profile and devices | Query basic profile information and linked devices. |

For full tool descriptions, parameters, and usage limits, see the [Tool Guide](docs/en/tools.md).

## Frequently asked questions

### Which AI platforms are supported?

In addition to the platforms listed above, COROS MCP supports compatible MCP clients and Skill access. Availability depends on the platform's connection and authentication capabilities.

See the [Setup Guide](docs/en/getting-started.md) for connection options.

### Does COROS MCP cost anything?

COROS MCP itself is free to use. Your AI platform may require a subscription or impose usage limits for connectors, models, or tool calls. Check that platform's policies for details.

For more questions, see the [full FAQ](docs/en/faq.md).

## Data and privacy

You decide whether to connect and which AI platform to authorize. Once authorized, that platform can access data within the permitted scope. Training content you ask it to save or modify is written to your COROS account.

Before using the service, read the COROS [Terms of Service](https://coros.com/terms) and [Privacy Policy](https://coros.com/privacy), and understand how your AI platform handles conversations, files, and tool-call data. Connect COROS only to platforms you trust.

## Updates and feedback

- [Changelog](changelog/CHANGELOG.md): See feature updates.
- [GitHub Issues](https://github.com/coroslab/COROS-MCP/issues): Report a problem or suggest an improvement. Include your AI platform, steps to reproduce, and any error messages. Do not include account credentials or personal health data.
- COROS Support: For account-related help, contact support through the COROS App.
