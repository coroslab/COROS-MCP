[中文](README.md) | [English](README.en.md) | [Skill](skill/)

# COROS MCP

[![COROS MCP](https://img.shields.io/badge/COROS-MCP-blue)](https://mcp.coros.com)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](skill/)

## 简介

COROS 推出了 MCP（Model Context Protocol） 能力——这是一座安全、标准化的桥梁，能让AI安全地读取您在COROS服务器上的数据。这也是主要运动手表品牌首个官方支持的MCP。

您只需通过自然语言描述需求，AI 便能根据需求，通过 COROS MCP 拉取用户相应的运动、健康数据，用于进行运动分析、报表生成、健康分析、规划训练计划等多种需求：

- *“过去三个月我的跑步量趋势如何？”*

- *“过去一个月我的睡眠情况如何？”*

- *“六周后我有一场马拉松比赛——根据我的训练情况，帮我规划一个训练计划。”*

- “*帮我生成一张2026年度马拉松数据报告，要具有科技感和运动风格的图片。”*

您也可以使用它探索更多的玩法，最大化发挥数据的价值。COROS认为运动员应该拥有自己的数据，并有权自由地以任何他们选择的方式使用这些数据，而MCP就是这种信念迄今为止最直接的体现。

您可以在您常用的AI平台上配置 COROS MCP，例如 ChatGPT、OpenClaw、Codex，具体的连接方式如下：

## 接入指南

选择以下任一方式快速配置 COROS MCP

### 1. HTTP OAuth

将以下 URL 添加到你的 MCP 客户端配置中

```text
https://mcp.coros.com/mcp
```

> 支持 ChatGPT、Codex、Claude 等主流平台

---

### 2. Skill

将以下指令发送给你的AI 助手，通过对话进行安装

```text
npm install -g coros-mcp
```

> 支持 OpenClaw、Workbuddy、Hermes 等 Claw 类AI

## 工具列表

<details open>
<summary><strong>Activity Analytics</strong></summary>

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>工具</th>
      <th align="left" width="480">说明</th>
      <th align="left" width="120" nowrap>状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>querySportRecords</code></td>
      <td>查询 COROS 运动记录，支持按日期、运动类型编码、距离、时长、配速和地点筛选；返回后续查询详情、分圈所需的活动标识和时间信息。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>getActivityDetail</code></td>
      <td>查询指定活动详情，包含心率、配速/速度、海拔、步频等综合数据。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>analyzeActivityDetail</code></td>
      <td>基于活动详情生成教练式分析，可指定关注配速、速度或心率等重点。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryActivityLapData</code></td>
      <td>查询指定活动的默认分圈或分段数据，按 COROS App 对应运动类型的展示字段返回。</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryCustomActivityLapData</code></td>
      <td>查询指定活动内某个精确时间窗的自定义分段数据，适合最后 N 分钟、指定片段等分析。</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>downloadActivityFitFiles</code></td>
      <td>下载一个或多个活动 FIT 文件，用于解析完整运动原始数据；支持按单个活动或日期范围下载。</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryActivityFitFileDownloadUrls</code></td>
      <td>查询活动 FIT 文件原始下载链接，作为客户端无法接收二进制文件时的兜底方式。</td>
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
      <th align="left" width="320" nowrap>工具</th>
      <th align="left" width="480">说明</th>
      <th align="left" width="120" nowrap>状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>queryDailyHealthData</code></td>
      <td>查询每日健康总览，包括步数、卡路里、压力、睡眠和心率概览；纯心率问题应使用心率专项工具。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>querySleepData</code></td>
      <td>查询睡眠评分、主睡眠时长、深睡/浅睡/REM 比例、清醒情况、睡眠窗口和午睡信息。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>querySleepHrv</code></td>
      <td>查询睡眠 HRV 官方评估和原始曲线；日均值、正常范围和评价以官方评估为准。</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryAvgHeartRate</code></td>
      <td>查询每日平均心率趋势。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryRestingHeartRate</code></td>
      <td>查询每日静息心率趋势。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryStressLevel</code></td>
      <td>查询每日平均压力趋势。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryHealthCheckTimeSeries</code></td>
      <td>查询健康快测原始曲线，包括心率、HRV、压力、呼吸率和血氧；最近查询窗口最多 7 天。</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryStressTimeSeries</code></td>
      <td>查询压力原始曲线点，包括时间、压力值、展示分数、压力 HRV 和压力心率值；查询窗口最多 7 天。</td>
      <td nowrap><code>new</code></td>
    </tr>
    <tr>
      <td nowrap><code>queryRecoveryStatus</code></td>
      <td>查询当前恢复百分比、恢复等级和预计完全恢复时间。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryMenstruationCycles</code></td>
      <td>查询生理周期数据，包括今日状态、下次经期、每日阶段、周期范围。</td>
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
      <th align="left" width="320" nowrap>工具</th>
      <th align="left" width="480">说明</th>
      <th align="left" width="120" nowrap>状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>queryFitnessAssessmentOverview</code></td>
      <td>查询体能评估概览，包括 VO2max、跑力、阈值配速和 5K/10K/半马/全马成绩预测。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryTrainingLoadAssessment</code></td>
      <td>查询训练负荷评估，包括近期每日评语、短期负荷、长期负荷和负荷比。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryTrainingSchedule</code></td>
      <td>查询训练日程，默认返回本周计划，也支持指定日期范围；结果包含供后续计划工具使用的内部标识。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryTrainingPlanDetail</code></td>
      <td>查询训练计划详情，用于更新计划前确认当前计划、课程 dayNo、idInPlan、预估指标和原始课程结构。</td>
      <td nowrap><code>coming&nbsp;soon</code></td>
    </tr>
    <tr>
      <td nowrap><code>generateTrainingPlan</code></td>
      <td>根据已设计好的结构化课程创建并保存 COROS 训练计划；支持跑步、骑行、力量、休息课程和阶段说明。</td>
      <td nowrap><code>coming&nbsp;soon</code></td>
    </tr>
    <tr>
      <td nowrap><code>updateTrainingPlan</code></td>
      <td>更新已有 COROS 训练计划；应先查询计划详情，只提交需要替换的 dayNo 课程。</td>
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
      <th align="left" width="320" nowrap>工具</th>
      <th align="left" width="480">说明</th>
      <th align="left" width="120" nowrap>状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap><code>queryDevices</code></td>
      <td>查询用户绑定的 COROS 设备列表，包括设备 ID、固件类型和自定义名称。</td>
      <td nowrap></td>
    </tr>
    <tr>
      <td nowrap><code>queryUserInfo</code></td>
      <td>查询用户基础资料，包括身高、体重、生日和性别。</td>
      <td nowrap></td>
    </tr>
  </tbody>
</table>

</details>

> 注：随着项目持续迭代，MCP 工具列表可能发生变化，如需了解最新可用工具，请在 AI 平台中手动刷新 MCP 工具列表。

## FAQ

#### 1. COROS MCP 支持在哪些平台上使用？

MCP 是一种连接外部系统的开源标准，可以把 MCP 理解成 AI 应用的 “USB 接口”。能否接入，取决于该平台是否支持添加 MCP 服务，以及是否支持 COROS MCP 所需的认证方式。

目前建议优先使用已验证支持的平台，如 ChatGPT、Claude、OpenClaw、Workbuddy、Hermes 等。

如果你使用的平台暂未支持 MCP，可以关注该平台后续更新。只要平台开放兼容的 MCP 接入能力，即可按平台规则连接 COROS。

#### 2. 使用 COROS MCP 需要付费吗？

COROS MCP 本身不收取费用。你可以在支持 MCP 的 AI 平台中授权连接 COROS 账号并使用已开放的功能。

但请注意，部分 AI 平台可能会对 MCP、外部工具连接、高级模型或开发者模式设置会员、订阅或额度限制。这些费用由对应的 AI 平台收取，并非 COROS 决定。请以你所用平台的最新规则为准。

#### 3. 无法完成授权？

请先确认你的 COROS 账号可以在 COROS App 中正常登录和使用，并且账号内已有可查看的数据。

如果仍无法授权，请检查：

1. 授权页面是否已完整打开，浏览器是否拦截了弹窗或跳转。

2. 是否使用了正确的 COROS 账号登录。

3. AI 平台内是否已删除旧连接并重新授权。

如果多次重试仍失败，请保存报错截图，并联系 COROS 客服排查。

#### 4. MCP URL 无效？

当前 COROS MCP 使用了域名跳转技术（[https://mcp.coros.com/mcp](https://mcp.coros.com/mcp)），会根据您账号所在的实际区域自动切换至最佳服务器。但部分 AI 平台不支持域名重定向，从而导致报错或连接失效。

如果遇到 URL 无效，请根据您**账号所在的实际地区**，直接复制并填写对应的独立分流 URL：

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>账号地区</th>
      <th align="left" width="600">独立分流 URL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap>中国大陆</td>
      <td nowrap><code>https://mcpcn.coros.com/mcp</code></td>
    </tr>
    <tr>
      <td nowrap>欧洲</td>
      <td nowrap><code>https://mcpeu.coros.com/mcp</code></td>
    </tr>
    <tr>
      <td nowrap>美国</td>
      <td nowrap><code>https://mcpus.coros.com/mcp</code></td>
    </tr>
  </tbody>
</table>

#### 5. AI 无法拉取到 COROS 数据？

如果已成功连接 COROS MCP，但 AI 没有拉取到数据，可以按以下步骤排查：

1. 确认 COROS App 内已有对应数据。设备数据需要先同步到 COROS App，再上传至云端。如果 App 内本身就没有这条数据，AI 也是无法读取到的。

2. 新建一个对话窗口，或在支持的客户端中发送 /new 后重新提问。

3. 使用更明确的指令，例如：“请调用 COROS MCP，查看我最近 7 天的运动记录。”

#### 6. 为什么 AI 回答不准确？

AI 的回答质量会受到模型能力、提问方式、可访问数据范围等因素影响。

如果回答明显不准确，可以尝试换一个新对话，明确要求“调用 COROS MCP”，并指定时间范围和数据类型，例如“请调用 COROS MCP，分析我过去 4 周的跑步训练负荷变化”。

推荐使用deepseek V4 flash及以上能力的模型，工具调用能力较弱的模型可能会漏用工具，或使用错误参数。

#### 7. 能否拉取 .fit 文件？

**支持。** COROS MCP 支持拉取运动记录的 `.fit` 文件，以便您进行更深入的数据分析。

同时，通过这种方式可以避免大量秒级数据直接挤爆 AI 的上下文窗口。

我们提供以下两种获取方式：

- **直接获取：** 直接读取 `.fit` 文件实体。

- **链接获取：** 获取文件的下载链接。

<strong>注：</strong> AI 助手是否能直接为您展示或处理文件实体，取决于您当前使用的 AI 平台自身的能力与权限控制。如果遇到文件无法下载或读取，建议咨询对应的 AI 平台客服。

**每日额度限制：** 为保障服务稳定性，每个自然日内，单个账号最多支持获取 **50 条** `.fit` 文件。

#### 8. 我的数据会被谁看到？安全吗？

只有在你主动授权后，AI 应用才可以通过 COROS MCP 访问授权范围内的数据。你的 COROS 数据仍受 COROS 账号体系和隐私政策保护；AI 对话内容和模型处理方式则受你所使用 AI 平台的政策约束。建议只在你信任的平台上连接 COROS MCP。

## 注意事项

使用 COROS MCP 服务须遵守 COROS 的[《服务条款》](https://coros.com/terms)及[《隐私政策》](https://coros.com/privacy)。在授权第三方 AI 平台前，请确认你理解该平台对对话内容、文件和工具调用数据的处理方式；建议只在你信任的平台上连接 COROS MCP，并在不再使用时及时撤销授权。
