# COROS MCP 工具说明

[返回首页](../../README.zh.md) | [接入指南](getting-started.md) | [English](../en/tools.md)

本文介绍 COROS MCP 各工具的用途、主要参数、返回内容和使用限制。

[运动记录与分析](#activities) | [身体状态与恢复](#health) | [训练计划与课程](#training) | [个人资料与设备](#profile)

<a id="activities"></a>

## 运动记录与分析

<a id="querysportrecords"></a>

### 查询运动记录 · `querySportRecords`

按日期、运动类型、距离、时长、平均配速和地点筛选运动记录，为详情分析、分段查询和 FIT 下载定位活动。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 必填 | 开始日期，格式 yyyyMMdd；传空字符串 `""` 时，取结束日期前 6 天。 |
| `endDate` | string | 必填 | 结束日期，格式 yyyyMMdd；传空字符串 `""` 时取今天，按 COROS 账号时区计算。 |
| `sportTypeCodes` | integer[] | 必填 | 运动记录类型编码列表；不限制运动类型时传 `[65535]`。 |
| `minDistanceKm` | number | 必填 | 最小距离，单位 km；不启用此筛选时传 `0`。 |
| `maxDistanceKm` | number | 必填 | 最大距离，单位 km；不启用此筛选时传 `0`。 |
| `minDurationMinutes` | integer | 必填 | 最小时长，单位分钟；不启用此筛选时传 `0`。 |
| `maxDurationMinutes` | integer | 必填 | 最大时长，单位分钟；不启用此筛选时传 `0`。 |
| `maxAveragePace` | string | 必填 | 最大平均配速，如 `5:30` 表示 5 分 30 秒/km；不启用此筛选时传空字符串 `""`。 |
| `locationKeyword` | string | 必填 | 地点关键字；不启用此筛选时传空字符串 `""`。 |
| `limit` | integer | 必填 | 最多返回条数；未指定条数时传 `20`。 |

**返回内容：** 符合条件的运动记录，包括日期、运动类型、地点、距离、时长、配速或速度，以及供后续详情查询使用的活动标识和起止时间。

**返回示例**

```text
Sport Records — 2026-09-19 to 2026-10-18 (1 records)

1. Sport(9807) — 2026-10-03
   Duration: 2:12:38 | Distance: 12.03 km
   Average Pace: 11:01 /km
```

**限制与提示**

- 默认范围为最近 7 天。需要更早的记录时，应明确指定日期。
- `limit` 控制本次返回条数；返回条数不等于历史记录总数。运动类型须使用数字编码，不能直接传运动名称。

<a id="getactivitydetail"></a>

### 查询单次运动详情 · `getActivityDetail`

查看一条已完成运动的详细数据。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `labelId` | string | 必填 | 活动标识，由运动记录查询结果取得。 |
| `sportType` | integer | 必填 | 该活动对应的运动类型编码，使用查询结果中的值。 |

**返回内容：** 该次运动可用的心率、配速或速度、海拔、步频等详细数据。

**返回示例**

```text
Sport(9807) Activity Details

Workout Time: 2:12:38
Distance: 12.03 km
Average Pace: 11:01 /km
Average Heart Rate: 76 bpm
Calories: 372 kcal
```

**限制与提示**

- 活动标识和运动类型须来自同一条记录；可用指标随设备、运动类型和实际记录内容而变化。

<a id="queryactivitylapdata"></a>

### 查询默认分圈或分段 · `queryActivityLapData`

查询活动已有的分圈、分段数据。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `labelId` | string | 必填 | 活动标识，由运动记录查询结果取得。 |
| `sportType` | integer | 必填 | 该活动对应的运动类型编码，使用查询结果中的值。 |

**返回内容：** JSON 格式的指标字段说明及分圈或分段数据，可包含圈数、距离、单圈和累计时间、配速或速度、平均和最大心率、步频、步幅、累计上升和下降、卡路里等。实际指标随运动类型和记录内容变化。

**返回示例**

```json
{
  "lapGroups": [
    {
      "laps": [
        {
          "lapIndex": 1,
          "distance": 100000,
          "time": 360.41,
          "totalLength": 360.41,
          "avgPace": 360.41,
          "avgSpeedV2": 998.86,
          "vertSpeed": 29.96,
          "avgPower": 236,
          "avgHr": 143,
          "maxHr": 152,
          "groundTime": 269,
          "groundBalance": 0.0,
          "avgCadence": 155,
          "maxCadence": 162,
          "strideRatio": 90,
          "strideHeight": 98,
          "avgStrideLength": 107,
          "formPower": 0,
          "legStiffness": 0,
          "elevGain": 7.0,
          "totalDescent": 4.0,
          "bodyTemperature": 0,
          "adjustedPace": 355
        }
      ]
    }
  ]
}
```

**限制与提示**

- “最后 5 分钟”等自定义时间段请使用 `queryCustomActivityLapData`。

<a id="querycustomactivitylapdata"></a>

### 查询自定义时间段 · `queryCustomActivityLapData`

查询一次活动内指定时间窗口的分段数据，例如最后 5 分钟。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `labelId` | string | 必填 | 活动标识，由运动记录查询结果取得。 |
| `sportType` | integer | 必填 | 该活动对应的运动类型编码，使用查询结果中的值。 |
| `startTimestamp` | integer | 必填 | 所选时间段开始的 Unix 时间戳，单位秒。 |
| `endTimestamp` | integer | 必填 | 所选时间段结束的 Unix 时间戳，单位秒。 |

**返回内容：** 所选时间段内可用的运动数据。

**限制与提示**

- 时间戳单位为秒，不能使用毫秒；所选时段必须位于该次运动的起止范围内。

<a id="downloadactivityfitfiles"></a>

### 下载 FIT 文件 · `downloadActivityFitFiles`

下载一条或多条运动记录的 FIT 文件，供支持文件接收和解析的客户端进一步分析。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `labelId` | string | 条件必填 | 按单次活动下载时提供；与 sportType 一起使用。 |
| `sportType` | integer | 条件必填 | 提供 labelId 时必填；按日期查询时可作为运动类型筛选。 |
| `startDate` | string | 可选 | 按日期查询时使用，格式 yyyyMMdd；省略时取 COROS 账号时区的今天。 |
| `endDate` | string | 可选 | 结束日期 yyyyMMdd；省略时与 startDate 相同。 |
| `limit` | integer | 可选 | 单次最多返回文件数，默认 5，最大 10。 |

**返回内容：** 一个或多个 FIT 运动文件。

**限制与提示**

- 提供 `labelId` 时查询单次运动，同时须提供 `sportType`；否则按日期范围查询。
- 每次默认返回 5 个文件，最多 10 个。文件下载和下载链接共用额度：每位平台用户在 24 小时窗口内最多获取 50 个文件。
- 文件中的数据项目取决于设备、运动类型和记录内容。
- 如果 AI 客户端无法接收文件，可改用 `queryActivityFitFileDownloadUrls` 获取下载链接。

<a id="queryactivityfitfiledownloadurls"></a>

### 获取 FIT 下载链接 · `queryActivityFitFileDownloadUrls`

在客户端不能直接接收 FIT 文件时，获取原始文件下载链接。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `labelId` | string | 条件必填 | 按单次活动下载时提供；与 sportType 一起使用。 |
| `sportType` | integer | 条件必填 | 提供 labelId 时必填；按日期查询时可作为运动类型筛选。 |
| `startDate` | string | 可选 | 按日期查询时使用，格式 yyyyMMdd；省略时取 COROS 账号时区的今天。 |
| `endDate` | string | 可选 | 结束日期 yyyyMMdd；省略时与 startDate 相同。 |
| `limit` | integer | 可选 | 单次最多返回文件数，默认 5，最大 10。 |

**返回内容：** 文件名及对应的 FIT 下载链接。

**限制与提示**

- 提供 `labelId` 时查询单次运动，同时须提供 `sportType`；否则按日期范围查询。
- 每次默认返回 5 个文件，最多 10 个。文件下载和下载链接共用额度：每位平台用户在 24 小时窗口内最多获取 50 个文件。
- 文件中的数据项目取决于设备、运动类型和记录内容。

<a id="health"></a>

## 身体状态与恢复

<a id="querydailyhealthdata"></a>

### 查询每日健康总览 · `queryDailyHealthData`

查询最近数天的每日整体健康数据。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `days` | integer | 可选 | 最近查询天数；默认 7。 |

**返回内容：** 近期每日步数、卡路里、压力、睡眠等汇总，以及总览中的心率信息。

**限制与提示**

- 仅查询平均心率或静息心率时，分别使用对应的心率工具。睡眠记录按 COROS 账号时区的起床日归属。

<a id="querysleepoverview"></a>

### 查询睡眠概览 · `querySleepOverview`

查询睡眠评分、主睡眠和小睡情况。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 可选 | 开始日期，格式 yyyyMMdd；仅提供 endDate 时查询该日。 |
| `endDate` | string | 可选 | 结束日期，格式 yyyyMMdd；省略时取 startDate；两日期均省略时按 days 查询。 |
| `days` | integer | 可选 | 最近查询天数；默认 7。 |

**返回内容：** 睡眠评分、主睡眠时长、睡眠阶段、清醒情况、睡眠起止时间及小睡信息。

**返回示例**

```text
Sleep Overview

2026-10-15
Sleep Score: 91
Daily Sleep: 7h 57min (incl. naps)
Main Sleep (asleep): 7h 57min
Deep Sleep Ratio: 27%
Light Sleep Ratio: 41%
REM Ratio: 31%
Awake Time: 5 min
Main Sleep Window: 2026-10-15 00:28 - 2026-10-15 08:30
Naps Total: 0 min
```

**限制与提示**

- 日期按 COROS 账号时区的起床日计算：“昨晚”对应今天。用户明确指定的日期与 App 中该日期保持一致。
- 指定日期优先于 `days`；仅提供一个日期时查询当天。全天睡眠包含小睡。

<a id="querysleephrv"></a>

### 查询睡眠 HRV · `querySleepHrv`

查看睡眠期间的心率变异性（HRV）及 COROS 评估。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 必填 | 开始日期，格式 yyyyMMdd；仅查询结束日期当天时传 `""`；按最近天数查询时，两日期均传 `""`。 |
| `endDate` | string | 必填 | 结束日期，格式 yyyyMMdd；传 `""` 时取 startDate；两日期均为空时按 days 查询。 |
| `days` | integer | 必填 | 最近查询天数，最多 7 天；未指定天数时传 `7`。指定日期时此参数不生效，仍须传入。 |

**返回内容：** 日均 HRV、正常范围和评价，以及可用的睡眠 HRV 曲线；单位为毫秒（ms）。

**限制与提示**

- 按最近天数查询时最多 7 天；指定日期优先于 `days`。
- 日期按 COROS 账号时区的起床日计算，“昨晚”对应今天。日均值和评价以返回的 COROS 评估为准。

<a id="queryavgheartrate"></a>

### 查询每日平均心率 · `queryAvgHeartRate`

查询每日平均心率及变化趋势。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 可选 | 开始日期，格式 yyyyMMdd；仅提供 endDate 时查询该日。 |
| `endDate` | string | 可选 | 结束日期，格式 yyyyMMdd；省略时取 startDate；两日期均省略时按 days 查询。 |
| `days` | integer | 可选 | 最近查询天数；默认 7。 |

**返回内容：** 查询范围内各日的平均心率，单位为 bpm。

**限制与提示**

- 指定日期优先于 `days`；仅提供一个日期时查询当天。日期按 COROS 账号时区计算。

<a id="queryrestingheartrate"></a>

### 查询每日静息心率 · `queryRestingHeartRate`

查询最近数天的静息心率。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `days` | integer | 可选 | 最近查询天数；默认 7。 |

**返回内容：** 近期各日的静息心率，单位为 bpm。

**限制与提示**

- 按最近天数查询，暂不支持指定起止日期。

<a id="querystresslevel"></a>

### 查询每日平均压力 · `queryStressLevel`

查询每日平均压力趋势。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `days` | integer | 可选 | 最近查询天数；默认 7。 |

**返回内容：** 近期各日的平均压力值。

**限制与提示**

- 本工具返回每日平均值；查看一天内的变化请使用 `queryStressTimeSeries`。

<a id="queryhealthchecktimeseries"></a>

### 查询健康快测数据 · `queryHealthCheckTimeSeries`

查询最近一次可用的完整健康快测。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 必填 | 开始日期，格式 yyyyMMdd；仅查询结束日期当天时传 `""`；按最近天数查询时，两日期均传 `""`。 |
| `endDate` | string | 必填 | 结束日期，格式 yyyyMMdd；传 `""` 时取 startDate；两日期均为空时按 days 查询。 |
| `days` | integer | 必填 | 最近查询天数，最多 7 天；未指定天数时传 `7`。指定日期时此参数不生效，仍须传入。 |

**返回内容：** 最近一次完整快测的测量时间，以及可用的心率、HRV、压力、呼吸率和血氧等数据。

**限制与提示**

- 按最近天数查询时最多 7 天；指定日期优先于 `days`。
- 单次返回最近一次完整快测，而非全部快测记录；测量时间以结果中标注的日期为准。

<a id="querystresstimeseries"></a>

### 查询日内压力曲线 · `queryStressTimeSeries`

查看指定日期内的压力变化。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 必填 | 开始日期，格式 yyyyMMdd；仅查询结束日期当天时传 `""`；按最近天数查询时，两日期均传 `""`。 |
| `endDate` | string | 必填 | 结束日期，格式 yyyyMMdd；传 `""` 时取 startDate；两日期均为空时按 days 查询。 |
| `days` | integer | 必填 | 最近查询天数，最多 7 天；未指定天数时传 `1`。指定日期时此参数不生效，仍须传入。 |

**返回内容：** 压力随时间变化的数据，包含测量时间及可用的相关指标。

**限制与提示**

- 无论按日期还是最近天数查询，每次最多覆盖 7 天；指定日期优先于 `days`。

<a id="queryrecoverystatus"></a>

### 查询当前恢复状态 · `queryRecoveryStatus`

查询当前恢复程度。

**主要参数**

无需参数。

**返回内容：** 当前恢复百分比、恢复等级及预计完全恢复时间。

**限制与提示**

- 仅返回当前状态，暂不提供历史恢复曲线。

<a id="querymenstruationcycles"></a>

### 查询生理周期 · `queryMenstruationCycles`

查询生理周期状态、阶段、周期范围及备注。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDay` | integer | 可选 | 开始日期，整数 yyyyMMdd；省略或 0 时使用今天前 30 天。日期按 COROS 账号时区计算。 |
| `endDay` | integer | 可选 | 结束日期，整数 yyyyMMdd；省略或 0 时使用今天后 365 天。日期按 COROS 账号时区计算。 |

**返回内容：** 当前周期状态、下次经期日期、周期阶段及用户已记录的备注等可用信息。

<a id="training"></a>

## 训练计划与课程

<a id="queryfitnessassessmentoverview"></a>

### 查询体能评估 · `queryFitnessAssessmentOverview`

查看当前体能与跑步能力评估。

**主要参数**

无需参数。

**返回内容：** 最大摄氧量（VO2max）、跑力、阈值配速及比赛成绩预测等可用评估。

<a id="querytrainingloadassessment"></a>

### 查询训练负荷评估 · `queryTrainingLoadAssessment`

了解近期训练负荷是否适当。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `days` | integer | 可选 | 最近查询天数；默认 7。 |

**返回内容：** 近期训练负荷、负荷变化及相关评价。

<a id="querytrainingschedule"></a>

### 查询训练日历 · `queryTrainingSchedule`

查询某天、本周或指定日期范围内已安排的课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `startDate` | string | 可选 | 开始日期 yyyyMMdd；两端均省略时查询当前周一至周日。 |
| `endDate` | string | 可选 | 结束日期 yyyyMMdd；仅提供 startDate 时查询当天，仅提供 endDate 时从今天查询；起止传反时交换。 |

**返回内容：** 按日期排列的训练安排，包括计划内课程和单独安排的课程。

**限制与提示**

- 默认查询本周；日期按 COROS 账号时区计算。
- 查询“有哪些计划”使用 `queryTrainingPlanLibrary`；查询“某天练什么”使用本工具。

<a id="querytrainingplanlibrary"></a>

### 查询训练计划列表 · `queryTrainingPlanLibrary`

查询已有训练计划，按执行状态、来源和周数筛选。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `statusList` | integer[] | 可选 | 0=未开始、1=进行中、2=已完成；默认 [1]。全部计划使用 [0,1,2]，不得传空数组。 |
| `planType` | string | 可选 | 来源筛选：official、custom、mcp。 |
| `weeks` | integer | 可选 | 按计划周数筛选。 |
| `cursor` | string | 可选 | 用于继续查询下一批结果；首次查询省略，后续使用上次返回的分页信息。 |

**返回内容：** 按更新时间排列的计划列表、计划状态、是否可修改，以及继续查询后续结果所需的信息。

**限制与提示**

- 默认只查询进行中的计划；查询全部状态时使用 `[0,1,2]`，不要传空列表。
- 每批最多 50 条，可继续查询后续结果；单批条数不代表计划总数。

<a id="querytrainingplandetails"></a>

### 查询训练计划详情 · `queryTrainingPlanDetails`

查看计划摘要、完整训练阶段和指定日期内的课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `planId` | string | 必填 | 从计划列表或创建结果取得的计划标识，按字符串传入。 |
| `startDay` | string | 可选 | 窗口开始日期 yyyyMMdd。 |
| `endDay` | string | 可选 | 窗口结束日期 yyyyMMdd；窗口最长 28 天。 |

**返回内容：** 计划摘要、训练阶段、指定日期内的课程、完成情况及可修改性说明。

**限制与提示**

- 每次最多返回 28 天的每日课程，默认查看 4 周；查看其他日期时需另行指定范围。
- 日期窗口只限制每日课程明细，计划摘要与阶段信息仍覆盖整个计划。修改前应读取详情，确认内容是否支持调整。

<a id="createtrainingplan"></a>

### 创建训练计划 · `createTrainingPlan`

将已设计好的多周计划保存到 COROS，并按指定开始日期执行。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `planInfo` | object | 必填 | 计划名称、说明、开始日期和周数。 |
| `phaseInfo` | object | 必填 | 完整的训练阶段安排。 |
| `courseList` | object[] | 必填 | 计划中的训练课程。 |

**返回内容：** 计划创建结果，包括开始日期、周数及后续查询所需的计划信息。

**限制与提示**

- 支持跑步、骑行和越野跑；计划长度为 4–16 个自然周，开始日期为 COROS 账号时区的今天至未来 14 天，包含边界。
- 创建时需指定开始日期；自然周按周一至周日计算，第一周可能不足 7 天。
- 创建前应检查已有安排；修改现有计划请使用 `updateTrainingPlan`。

<a id="updatetrainingplan"></a>

### 修改训练计划 · `updateTrainingPlan`

调整已有训练计划的课程、阶段或周数。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `planInfo` | object | 必填 | 需要修改的计划及更新后的计划信息。 |
| `courseList` | object[] | 条件必填 | 调整课程时提供完整的相关课程内容；与 phaseInfo 中的阶段安排至少提供一项。 |
| `phaseInfo` | object | 条件必填 | 调整阶段或周数时提供完整的阶段安排。 |

**返回内容：** 修改结果摘要，包括已更新或跳过的日期，以及计划周数的变化。

**限制与提示**

- 仅支持修改可编辑的进行中计划。若当前计划不可编辑，请先查看返回原因；可能需要在 COROS App 中开始或重新开始计划。
- 修改后仍须满足 4–16 个自然周。包含已完成课程的日期可能被跳过，应核对返回的修改结果。
- 修改前读取最新详情并保留不需改动的训练内容；退出计划请在 COROS App 中操作。

<a id="queryworkoutlibrary"></a>

### 查询课程库 · `queryWorkoutLibrary`

查找课程库中已保存的训练课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `sportType` | integer | 可选 | 训练课程编码，例如 1=跑步、2=骑行、3=游泳、4=力量、5=越野跑。 |
| `courseType` | string | 可选 | 来源筛选：official、custom、mcp。 |

**返回内容：** 按更新时间排列的课程列表、符合条件的总数及后续查询所需的课程信息。

**限制与提示**

- 最多展示 50 条，暂不支持分页；结果较多时可按运动类型或来源缩小范围。
- 可查询库中已有的游泳、力量等课程；创建与修改支持跑步、骑行和越野跑。查看某天已安排的课程请使用 `queryTrainingSchedule`。

<a id="queryworkoutdetails"></a>

### 查看库内课程详情 · `queryWorkoutDetails`

查看课程库中一节课程的训练内容。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `workoutId` | string | 必填 | 从课程库或创建结果取得的课程标识，按字符串传入。 |

**返回内容：** 课程名称、运动类型、训练内容，以及是否支持修改和不可修改原因。

**限制与提示**

- 修改库内课程前应先读取详情。查看某天的课程请使用 `queryScheduledWorkoutDetails`。

<a id="createsingleworkout"></a>

### 创建库内课程 · `createSingleWorkout`

创建一节训练课程并保存到课程库。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `course` | object | 必填 | 完整课程内容，包括名称、运动类型、训练段和训练目标。 |

**返回内容：** 课程保存结果及后续查询所需的课程信息。

**限制与提示**

- 每次创建一节课程，支持跑步、骑行和越野跑。
- 本工具只保存到课程库。直接在某天创建课程使用 `createScheduledWorkout`；修改已有课程使用 `updateWorkoutDetails`。

<a id="updateworkoutdetails"></a>

### 修改库内课程 · `updateWorkoutDetails`

修改课程库中支持编辑的训练课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `workoutId` | string | 必填 | 从课程库或创建结果取得的课程标识，按字符串传入。 |
| `course` | object | 必填 | 完整课程内容，包括名称、运动类型、训练段和训练目标。 |

**返回内容：** 库内课程的修改结果。

**限制与提示**

- 支持跑步、骑行和越野跑。先查询详情，确认课程可修改，并提交完整的调整后内容。
- 修改课程库内容不会同步改变已经安排到日历的课程。删除课程请在 COROS App 中操作。

<a id="scheduleworkout"></a>

### 将库内课程安排到日期 · `scheduleWorkout`

将课程库中的一节已有课程安排到指定日期。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `workoutId` | string | 必填 | 从课程库或创建结果取得的课程标识，按字符串传入。 |
| `date` | string | 必填 | 单个日期 yyyyMMdd；COROS 账号时区的今天至今天后 90 天，包含边界。 |

**返回内容：** 课程安排结果，以及当天已有其他训练的提示。

**限制与提示**

- 每次安排一节课程到一个日期；可选日期为今天至未来 90 天，按 COROS 账号时区计算，包含边界。
- 支持安排库中已有的游泳、力量等课程。同一课程已在当天时，不会再次添加；重复添加需在 App 中操作。
- 修改该日期的课程使用 `updateScheduledWorkout`；移动或移除日历课程请在 COROS App 中操作。

<a id="createscheduledworkout"></a>

### 在指定日期新建课程 · `createScheduledWorkout`

直接在指定日期创建一节新的独立课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `date` | string | 必填 | 单个日期 yyyyMMdd；COROS 账号时区的今天至今天后 90 天，包含边界。 |
| `course` | object | 必填 | 完整课程内容，包括名称、运动类型、训练段和训练目标。 |

**返回内容：** 课程创建与安排结果，以及当天已有其他训练的提示。

**限制与提示**

- 每次创建一节课程，支持跑步、骑行和越野跑。日期为今天至未来 90 天，按 COROS 账号时区计算，包含边界。
- 课程直接加入训练日历，不会同时保存到课程库。

<a id="queryscheduledworkoutdetails"></a>

### 查看日历课程详情 · `queryScheduledWorkoutDetails`

读取某天已安排的一节独立课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `date` | string | 必填 | 从日历定位到的课程日期，格式 yyyyMMdd。 |
| `idInPlan` | string | 必填 | 从训练日历或排期结果取得的该日课程标识，按字符串传入；不要使用课程库标识。 |

**返回内容：** 该日课程的内容、完成情况，以及是否支持修改和不可修改原因。

**限制与提示**

- 适用于单独安排的课程；计划内课程请使用 `queryTrainingPlanDetails`。
- 已完成、日期已过或内容不受支持的课程可能无法修改，具体以返回说明为准。

<a id="updatescheduledworkout"></a>

### 修改日历课程 · `updateScheduledWorkout`

调整某天单独安排且支持修改的课程。

**主要参数**

| 参数 | 类型 | 要求 | 说明 |
|---|---|---|---|
| `date` | string | 必填 | 从日历定位到的课程日期，格式 yyyyMMdd。 |
| `idInPlan` | string | 必填 | 从训练日历或排期结果取得的该日课程标识，按字符串传入；不要使用课程库标识。 |
| `course` | object | 必填 | 完整课程内容，包括名称、运动类型、训练段和训练目标。 |

**返回内容：** 该日课程的修改结果及后续查询所需的最新课程信息。

**限制与提示**

- 支持跑步、骑行和越野跑。先查询该日课程详情，确认可修改，并提交完整的调整后内容。
- 只修改该日期的课程，不改变课程库内容；计划内课程使用 `updateTrainingPlan`。
- 不支持改期或移除，这些操作请在 COROS App 中完成。

<a id="profile"></a>

## 个人资料与设备

<a id="queryuserinfo"></a>

### 查询个人资料 · `queryUserInfo`

查询当前授权账号的基本资料。

**主要参数**

无需参数。

**返回内容：** 身高、体重、生日、性别等账号中已有的个人资料。

<a id="querydevices"></a>

### 查询绑定设备 · `queryDevices`

查看当前授权账号绑定的 COROS 设备。

**主要参数**

无需参数。

**返回内容：** 账号绑定的 COROS 设备及其名称等信息。
