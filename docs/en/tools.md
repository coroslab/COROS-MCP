# COROS MCP Tool Guide

[Home](../../README.md) | [Setup Guide](getting-started.md) | [中文](../zh/tools.md)

This guide describes COROS MCP tools, their main parameters, returned information, and usage limits.

[Activities and analysis](#activities) | [Health and recovery](#health) | [Training plans and workouts](#training) | [Routes](#routes) | [Profile and devices](#profile)

<a id="activities"></a>

## Activities and analysis

<a id="querysportrecords"></a>

### `querySportRecords`

Find activities by date, sport, distance, duration, average pace, and location for detail queries, segment analysis, or FIT downloads.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format; defaults to six days before the end date. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to today in the COROS account timezone. |
| `sportTypeCodes` | integer[] | Optional | List of activity sport codes; omit to include all sports. |
| `minDistanceKm` | number | Optional | Minimum distance in km. |
| `maxDistanceKm` | number | Optional | Maximum distance in km. |
| `minDurationMinutes` | integer | Optional | Minimum duration in minutes. |
| `maxDurationMinutes` | integer | Optional | Maximum duration in minutes. |
| `maxAveragePace` | string | Optional | Maximum average pace, such as 5:30 for 5 minutes 30 seconds/km. |
| `locationKeyword` | string | Optional | Location keyword. |
| `limit` | integer | Optional | Maximum records to return; default 20. |

**Returns:** Matching activities with date, sport, location, distance, duration, pace or speed, and activity identifiers and times for follow-up queries.

**Response example**

```text
Sport Records — 2026-09-19 to 2026-10-18 (1 records)

1. Sport(9807) — 2026-10-03
   Duration: 2:12:38 | Distance: 12.03 km
   Average Pace: 11:01 /km
```

**Limits and notes**

- The default range is the last 7 days. Specify dates to find older activities.
- `limit` controls the number returned by this call, not the total number of historical activities. Sport types must be numeric codes, not sport names.

<a id="getactivitydetail"></a>

### `getActivityDetail`

View detailed data for one completed activity.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `labelId` | string | Required | Activity identifier obtained from the activity list. |
| `sportType` | integer | Required | Sport code for that activity; use the value returned with the activity. |

**Returns:** Available heart rate, pace or speed, elevation, cadence, and other details for the activity.

**Response example**

```text
Sport(9807) Activity Details

Workout Time: 2:12:38
Distance: 12.03 km
Average Pace: 11:01 /km
Average Heart Rate: 76 bpm
Calories: 372 kcal
```

**Limits and notes**

- The activity identifier and sport code must come from the same record. Available metrics depend on the device, sport, and recorded data.

<a id="queryactivitylapdata"></a>

### `queryActivityLapData`

Query the recorded laps or segments of an activity.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `labelId` | string | Required | Activity identifier obtained from the activity list. |
| `sportType` | integer | Required | Sport code for that activity; use the value returned with the activity. |

**Returns:** JSON containing metric field labels and lap or segment data. Available metrics can include lap number, distance, lap and cumulative time, pace or speed, average and maximum heart rate, cadence, stride length, elevation gain and descent, and calories. Metrics vary by sport and recorded data.

**Response example**

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

**Limits and notes**

- Use `queryCustomActivityLapData` for a custom time segment such as the last 5 minutes.

<a id="querycustomactivitylapdata"></a>

### `queryCustomActivityLapData`

Query data for a selected time window within one activity, such as the last five minutes.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `labelId` | string | Required | Activity identifier obtained from the activity list. |
| `sportType` | integer | Required | Sport code for that activity; use the value returned with the activity. |
| `startTimestamp` | integer | Required | Start of the selected window as a Unix timestamp in seconds. |
| `endTimestamp` | integer | Required | End of the selected window as a Unix timestamp in seconds. |

**Returns:** Available activity data within the selected time segment.

**Limits and notes**

- Timestamps use seconds, not milliseconds. The selected segment must stay within the activity start and end times.

<a id="downloadactivityfitfiles"></a>

### `downloadActivityFitFiles`

Download FIT files for one or more activities for analysis in clients that can receive and parse files.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `labelId` | string | Conditional | Activity identifier for a single-activity query. |
| `sportType` | integer | Conditional | Activity sport code; required when labelId is supplied. |
| `startDate` | string | Optional | Start date in yyyyMMdd format for a date-range query; defaults to today in the COROS account timezone. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. |
| `limit` | integer | Optional | Maximum files per call; defaults to 5, with a maximum of 10. |

**Returns:** One or more activity FIT files.

**Limits and notes**

- When `labelId` is supplied, query that activity and also provide `sportType`; otherwise query by date range.
- Each call returns 5 files by default, up to 10. File downloads and download links share a quota of 50 files per platform user within a 24-hour window.
- Available file contents depend on the device, sport, and recorded data.
- If the AI client cannot receive files, use `queryActivityFitFileDownloadUrls` to get download links.

<a id="queryactivityfitfiledownloadurls"></a>

### `queryActivityFitFileDownloadUrls`

Get original FIT file download links when the client cannot receive FIT files directly.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `labelId` | string | Conditional | Activity identifier for a single-activity query. |
| `sportType` | integer | Conditional | Activity sport code; required when labelId is supplied. |
| `startDate` | string | Optional | Start date in yyyyMMdd format for a date-range query; defaults to today in the COROS account timezone. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. |
| `limit` | integer | Optional | Maximum files per call; defaults to 5, with a maximum of 10. |

**Returns:** File names and their FIT download links.

**Limits and notes**

- When `labelId` is supplied, query that activity and also provide `sportType`; otherwise query by date range.
- Each call returns 5 files by default, up to 10. File downloads and download links share a quota of 50 files per platform user within a 24-hour window.
- Available file contents depend on the device, sport, and recorded data.

<a id="health"></a>

## Health and recovery

<a id="querydailyhealthdata"></a>

### `queryDailyHealthData`

Query overall daily health data for recent days.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `days` | integer | Optional | Number of recent days to query; defaults to 7. |

**Returns:** Recent daily summaries of steps, calories, stress, sleep, and heart-rate information within the overview.

**Limits and notes**

- For average or resting heart rate alone, use the corresponding heart-rate tool. Sleep belongs to its wake-up date in the COROS account timezone.

<a id="querysleepoverview"></a>

### `querySleepOverview`

Query sleep scores, main sleep, and naps.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format; when only endDate is supplied, query that date. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. If both dates are omitted, use days. |
| `days` | integer | Optional | Number of recent days to query; defaults to 7. |

**Returns:** Sleep score, main sleep duration, sleep stages, awake periods, sleep start and end times, and naps.

**Response example**

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

**Limits and notes**

- Dates are wake-up dates in the COROS account timezone: last night corresponds to today. An explicitly requested date matches that date in the app.
- Explicit dates take priority over `days`. A single date queries that day. Daily sleep includes naps.

<a id="querysleephrv"></a>

### `querySleepHrv`

View heart rate variability (HRV) during sleep and its COROS assessment.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format; if only endDate is provided, query that day. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. If both dates are omitted, use days. |
| `days` | integer | Optional | Number of recent days; default 7, maximum 7. Ignored when dates are specified. |

**Returns:** Daily average HRV, plus the normal range, evaluation, and sleep HRV time series where available. HRV values are in milliseconds (ms).

**Limits and notes**

- Recent-days queries cover up to 7 days. Explicit dates take priority over `days`.
- Dates are wake-up dates in the COROS account timezone; last night corresponds to today. Use the returned COROS assessment for the daily value and evaluation.

<a id="queryavgheartrate"></a>

### `queryAvgHeartRate`

Query daily average heart rate and trends.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format; when only endDate is supplied, query that date. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. If both dates are omitted, use days. |
| `days` | integer | Optional | Number of recent days to query; defaults to 7. |

**Returns:** Average heart rate for each day in the query range, in bpm.

**Limits and notes**

- Explicit dates take priority over `days`; a single date queries that day. Dates use the COROS account timezone.

<a id="queryrestingheartrate"></a>

### `queryRestingHeartRate`

Query resting heart rate for recent days.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `days` | integer | Optional | Number of recent days to query; defaults to 7. |

**Returns:** Resting heart rate for each recent day, in bpm.

**Limits and notes**

- Queries use a recent-days window; explicit start/end dates are not supported.

<a id="querystresslevel"></a>

### `queryStressLevel`

Query daily average stress trends.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `days` | integer | Optional | Number of recent days to query; defaults to 7. |

**Returns:** Average stress for each recent day.

**Limits and notes**

- This tool returns daily averages. Use `queryStressTimeSeries` for changes within a day.

<a id="queryhealthchecktimeseries"></a>

### `queryHealthCheckTimeSeries`

Find the latest available complete wellness check.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format; if only endDate is provided, query that day. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. If both dates are omitted, use days. |
| `days` | integer | Optional | Number of recent days; default 7, maximum 7. Ignored when dates are specified. |

**Returns:** The measurement time and available heart rate, HRV, stress, respiration rate, and SpO2 data from the latest complete check.

**Limits and notes**

- Recent-days queries cover up to 7 days. Explicit dates take priority over `days`.
- One call returns the latest complete check, not all checks. Use the measurement date shown in the result.
- If a recent-days query finds no complete check within the window, it may return the latest complete check from an earlier date and indicate this in the result. Explicit date queries only return data within the selected range.

<a id="querystresstimeseries"></a>

### `queryStressTimeSeries`

View stress changes over time for the selected dates.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format; if only endDate is provided, query that day. |
| `endDate` | string | Optional | End date in yyyyMMdd format; defaults to startDate. If both dates are omitted, use days. |
| `days` | integer | Optional | Number of recent days; default 1, maximum 7. Ignored when dates are specified. |

**Returns:** Stress measurements over time, with measurement times and available related metrics.

**Limits and notes**

- Each query covers up to 7 days, whether using dates or recent days. Explicit dates take priority over `days`.

<a id="queryrecoverystatus"></a>

### `queryRecoveryStatus`

Query the current recovery level.

**Main parameters**

No parameters.

**Returns:** Current recovery percentage, recovery level, and estimated time to full recovery.

**Limits and notes**

- Only current status is available; historical recovery curves are not provided.

<a id="querymenstruationcycles"></a>

### `queryMenstruationCycles`

Query menstrual status, phases, cycle ranges, and notes.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDay` | integer | Optional | Start date as an integer in yyyyMMdd format; omitted or 0 uses 30 days before today. Dates use the COROS account timezone. |
| `endDay` | integer | Optional | End date as an integer in yyyyMMdd format; omitted or 0 uses 365 days after today. Dates use the COROS account timezone. |

**Returns:** Available cycle status, next period date, cycle phases, and recorded notes.

<a id="training"></a>

## Training plans and workouts

<a id="queryfitnessassessmentoverview"></a>

### `queryFitnessAssessmentOverview`

View current fitness and running ability assessments.

**Main parameters**

No parameters.

**Returns:** Available assessments such as VO2max, running level, threshold pace, and predicted race times.

<a id="querytrainingloadassessment"></a>

### `queryTrainingLoadAssessment`

Review whether recent training load is appropriate.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `days` | integer | Optional | Number of recent days to query; defaults to 7. |

**Returns:** Recent training load, changes in load, and related assessments.

<a id="querytrainingschedule"></a>

### `queryTrainingSchedule`

Query workouts scheduled for a day, the current week, or a date range.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `startDate` | string | Optional | Start date in yyyyMMdd format. Omitting both dates queries the current Monday–Sunday week. |
| `endDate` | string | Optional | End date in yyyyMMdd format. With only startDate, query that day; with only endDate, start from today. Reversed endpoints are swapped. |

**Returns:** Workouts grouped by date, including plan workouts and separately scheduled workouts.

**Limits and notes**

- The default range is the current week in the COROS account timezone.
- Use `queryTrainingPlanLibrary` to list plans, and this tool to find what is scheduled on a date.

<a id="querytrainingplanlibrary"></a>

### `queryTrainingPlanLibrary`

Find existing training plans by execution status, source, and length.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `statusList` | integer[] | Optional | 0=not started, 1=in progress, 2=completed; defaults to [1]. Use [0,1,2] for all statuses. An empty array is not allowed. |
| `planType` | string | Optional | Source filter: official, custom, or mcp. |
| `weeks` | integer | Optional | Plan length filter in weeks. |
| `cursor` | string | Optional | Continues to the next page. Omit for the first query; use the previous result for subsequent pages. |

**Returns:** Plans sorted by update time, their status and editability, and information for retrieving further results.

**Limits and notes**

- By default, only in-progress plans are returned. Use `[0,1,2]` for all statuses; do not pass an empty list.
- Each page contains up to 50 records. Further pages may be available; one page is not a total count.

<a id="querytrainingplandetails"></a>

### `queryTrainingPlanDetails`

View the plan summary, all training phases, and workouts within selected dates.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `planId` | string | Required | Plan identifier from the plan list or creation result; pass it as a string. |
| `startDay` | string | Optional | Window start date in yyyyMMdd format. |
| `endDay` | string | Optional | Window end date in yyyyMMdd format; the window is limited to 28 days. |

**Returns:** Plan summary, training phases, workouts for the selected dates, completion status, and editability information.

**Limits and notes**

- Each call returns up to 28 days of daily workouts, with a default window of 4 weeks. Specify another range to view other dates.
- The date window limits daily workouts only; plan summary and phase information cover the whole plan. Read the details before editing to check what can be changed.

<a id="createtrainingplan"></a>

### `createTrainingPlan`

Save a designed multi-week training plan to COROS and execute it from the specified start date.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `planInfo` | object | Required | Plan name, description, start date, and length in weeks. |
| `phaseInfo` | object | Required | The complete training phase schedule. |
| `courseList` | object[] | Required | The workouts included in the plan. |

**Returns:** The creation result, including start date, plan length, and information for follow-up queries.

**Limits and notes**

- Supports running, cycling, and trail running. Plans span 4–16 calendar weeks and start from today through 14 days after today, inclusive, in the COROS account timezone.
- A start date is required. Calendar weeks run Monday through Sunday, so the first week may contain fewer than 7 days.
- Check existing schedules before creating a plan. Use `updateTrainingPlan` to change an existing plan.

<a id="updatetrainingplan"></a>

### `updateTrainingPlan`

Adjust workouts, phases, or the length of an existing training plan.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `planInfo` | object | Required | The plan to edit and its updated plan information. |
| `courseList` | object[] | Conditional | Complete relevant workout content when changing workouts; supply this or the phase schedule in phaseInfo, or both. |
| `phaseInfo` | object | Conditional | The complete phase schedule when changing phases or plan length. |

**Returns:** An update summary, including updated or skipped dates and any change in plan length.

**Limits and notes**

- Only editable, in-progress plans can be changed. If a plan cannot be edited, check the returned reason; it may need to be started or restarted in the COROS app.
- The updated plan must still span 4–16 calendar weeks. Dates containing completed workouts may be skipped; check the update result.
- Read the latest details and preserve training content that should not change. Exit a plan through the COROS app.

<a id="queryworkoutlibrary"></a>

### `queryWorkoutLibrary`

Find workouts saved in the workout library.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `sportType` | integer | Optional | Workout sport code: 1=running, 2=cycling, 3=swimming, 4=strength, 5=trail running. |
| `courseType` | string | Optional | Source filter: official, custom, or mcp. |

**Returns:** Workouts sorted by update time, the total matching count, and information for follow-up queries.

**Limits and notes**

- Displays up to 50 records without pagination. Narrow the sport or source filters when more match.
- Existing swimming, strength, and other workouts can be queried. Creation and editing support running, cycling, and trail running. Use `queryTrainingSchedule` for workouts on a date.

<a id="queryworkoutdetails"></a>

### `queryWorkoutDetails`

View the content of a workout in the library.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `workoutId` | string | Required | Workout identifier from the library or creation result; pass it as a string. |

**Returns:** Workout name, sport, training content, and whether it can be edited, with reasons when it cannot.

**Limits and notes**

- Read these details before changing a library workout. Use `queryScheduledWorkoutDetails` for a workout on a specific date.

<a id="createsingleworkout"></a>

### `createSingleWorkout`

Create a workout and save it to the library.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `course` | object | Required | Complete workout content, including its name, sport, sections, and training targets. |

**Returns:** The save result and workout information for follow-up queries.

**Limits and notes**

- Creates one workout per call, supporting running, cycling, and trail running.
- This tool saves to the library only. Use `createScheduledWorkout` for a new workout on a date, or `updateWorkoutDetails` to change an existing workout.

<a id="updateworkoutdetails"></a>

### `updateWorkoutDetails`

Edit a supported workout in the library.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `workoutId` | string | Required | Workout identifier from the library or creation result; pass it as a string. |
| `course` | object | Required | Complete workout content, including its name, sport, sections, and training targets. |

**Returns:** The result of updating the library workout.

**Limits and notes**

- Supports running, cycling, and trail running. Read the details, confirm that the workout is editable, and provide its complete updated content.
- Library edits do not change workouts already scheduled on the calendar. Delete workouts through the COROS app.

<a id="scheduleworkout"></a>

### `scheduleWorkout`

Schedule an existing library workout on a selected date.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `workoutId` | string | Required | Workout identifier from the library or creation result; pass it as a string. |
| `date` | string | Required | One date in yyyyMMdd format, from today through 90 days after today, inclusive, in the COROS account timezone. |

**Returns:** The scheduling result and information about other training already on that date.

**Limits and notes**

- Schedules one workout on one date per call. Dates range from today through 90 days after today, inclusive, in the COROS account timezone.
- Existing swimming, strength, and other library workouts can be scheduled. The same workout is not added again if already on that date; duplicate additions require the app.
- Use `updateScheduledWorkout` to change the workout on that date. Move or remove calendar workouts through the COROS app.

<a id="createscheduledworkout"></a>

### `createScheduledWorkout`

Create a new standalone workout directly on a selected date.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `date` | string | Required | One date in yyyyMMdd format, from today through 90 days after today, inclusive, in the COROS account timezone. |
| `course` | object | Required | Complete workout content, including its name, sport, sections, and training targets. |

**Returns:** The workout creation and scheduling result, plus information about other training on that date.

**Limits and notes**

- Creates one workout per call, supporting running, cycling, and trail running. Dates range from today through 90 days after today, inclusive, in the COROS account timezone.
- The workout is added directly to the calendar and is not also saved to the library.

<a id="queryscheduledworkoutdetails"></a>

### `queryScheduledWorkoutDetails`

Read one standalone workout already scheduled on a date.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `date` | string | Required | Workout date located in the calendar, in yyyyMMdd format. |
| `idInPlan` | string | Required | Identifier for the workout on that date, obtained from the calendar or scheduling result; pass it as a string, not a library workout identifier. |

**Returns:** The workout content, completion status, and whether it can be edited, with reasons when it cannot.

**Limits and notes**

- Use this for separately scheduled workouts. For plan workouts, use `queryTrainingPlanDetails`.
- Completed, past-date, or unsupported workouts may not be editable; check the returned explanation.

<a id="updatescheduledworkout"></a>

### `updateScheduledWorkout`

Edit a supported workout scheduled separately on a date.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `date` | string | Required | Workout date located in the calendar, in yyyyMMdd format. |
| `idInPlan` | string | Required | Identifier for the workout on that date, obtained from the calendar or scheduling result; pass it as a string, not a library workout identifier. |
| `course` | object | Required | Complete workout content, including its name, sport, sections, and training targets. |

**Returns:** The update result and current workout information for follow-up queries.

**Limits and notes**

- Supports running, cycling, and trail running. Read the workout details for that date, confirm it is editable, and provide its complete updated content.
- Only the workout on that date is changed; library content stays unchanged. Use `updateTrainingPlan` for plan workouts.
- Rescheduling and removal are not supported; use the COROS app for those actions.

<a id="routes"></a>

## Routes

<a id="uploadroutefile"></a>

### `uploadRouteFile`

Import a GPX or KML route file into the COROS app for later syncing to a watch for navigation.

**Main parameters**

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `fileName` | string | Required | Original file name, including the `.gpx` or `.kml` extension. |
| `fileContent` | string | Required | The complete, original XML text of the file, without truncation or rewriting. |
| `routeType` | integer | Required | Route type: 1=cycling; 2=walking, running, trail running, or hiking. |
| `routeName` | string | Optional | Route name shown in the app; defaults to the file name without its extension. Names longer than 95 characters are truncated. |

**Returns:** File acceptance result, including the route name, file format, route type, number of track points, and distance in km; a reason is returned if the upload fails.

**Limits and notes**

- Uploads one GPX or KML file per call. The file must contain at least 2 track points.
- An accepted result means the file has been submitted for processing; it does not confirm that the import is complete. The route usually appears in the COROS app's Routes list within a few minutes. If it does not appear, the file may contain a track format COROS cannot parse.
- After import, sync the route to your watch through the COROS app. This tool does not sync directly to the watch.
- The same file cannot be uploaded again while its route remains in the app or is still being processed. It can be imported again after the existing route is deleted in the app.
- File size and upload limits apply; follow the returned guidance if a limit is exceeded.

<a id="profile"></a>

## Profile and devices

<a id="queryuserinfo"></a>

### `queryUserInfo`

Query the currently authorized account’s profile.

**Main parameters**

No parameters.

**Returns:** Available profile information, such as height, weight, birthday, and gender.

<a id="querydevices"></a>

### `queryDevices`

View COROS devices bound to the currently authorized account.

**Main parameters**

No parameters.

**Returns:** COROS devices linked to the account and information such as their names.
