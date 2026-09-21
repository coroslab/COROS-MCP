---
name: coros_mcp_login_gateway
description: Connect or refresh COROS MCP through the global gateway, configure OpenClaw, and discover and call COROS tools for private activity and health queries, training plans, workout templates, and scheduled workouts.
metadata:
  openclaw:
    requires:
      bins: ["python3", "openclaw"]
---

# COROS MCP Login (Gateway)

Use this skill to connect through `mcp.coros.com`, keep the gateway-selected CN, EU, or US cluster, and handle the user's COROS data or training requests through the helper's dynamically discovered tools.

## What to do

1. Work from this skill directory, which contains `scripts/coros_mcp_login.py`.
2. Prefer the resilient two-step flow when the browser might open on another machine, or when the CLI process may not stay alive the whole time:

```bash
python3 scripts/coros_mcp_login.py login-start
python3 scripts/coros_mcp_login.py login-finish
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

3. For a single-machine or quick refresh flow, use the one-shot helper:

```bash
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

4. The helper defaults to `https://mcp.coros.com`, reads the gateway-selected issuer from discovery, and then pins login, token refresh, MCP calls, and local cache files to that concrete regional issuer.

5. If there is no local token cache yet, the helper will print a browser login link. Tell the user to open that link on their phone or computer browser and complete the COROS login there.

6. If you used `login-start`, the helper saves the pending login locally on that same machine. After the user finishes the browser login, run `login-finish` on the original machine to complete the token save.

7. To discover what this COROS MCP server currently supports, list tools dynamically. This command reuses a short-lived local cache first, so repeated requests stay fast:

```bash
python3 scripts/coros_mcp_login.py list-tools
```

Use `--refresh` only when you specifically want to force a live re-fetch from `/mcp`:

```bash
python3 scripts/coros_mcp_login.py list-tools --refresh
```

8. Before calling an unfamiliar tool, inspect its schema:

```bash
python3 scripts/coros_mcp_login.py describe-tool --tool queryUserInfo
```

9. To call a tool directly through this helper, pass a JSON object for the tool arguments:

```bash
python3 scripts/coros_mcp_login.py call-tool --tool queryUserInfo --arguments-json '{}'
```

10. After the OpenClaw setup command succeeds, verify the saved MCP entry exists:

```bash
openclaw mcp show coros
```

11. Tell the user plainly whether:
   - the saved COROS MCP entry was created or refreshed
   - a fresh login was needed or cached login was reused
   - the gateway resolved to CN, EU, or US if that matters for the request
   - the helper was able to initialize `/mcp` and discover/call the requested tool
   - any manual next step is still needed

## Training requests

Read this section when the user wants to create, modify, save or schedule training. These actions change the user's COROS account; a request for advice or a draft alone is not permission to save it.

Refresh `list-tools --refresh` if newly documented tools are missing, then use the actual tool names and schemas returned by the connected server. Before each unfamiliar write tool, use `describe-tool` to inspect its full description and nested arguments. Do not guess fields from the examples below or assume that all regions have the same deployed version.

| User intent | Tool route | Important distinction |
| --- | --- | --- |
| View my training plans | `queryTrainingPlanLibrary` → `queryTrainingPlanDetails` when detail is needed | A plan library is not the day-by-day schedule. |
| Create a multi-week plan | `queryTrainingPlanLibrary` → `createTrainingPlan` | Check existing plans first; explain overlapping in-progress plans and obtain confirmation before creation. |
| Modify an existing plan | `queryTrainingPlanLibrary` → `queryTrainingPlanDetails` → `updateTrainingPlan` | Use only an in-progress execution record with `recordRole=execution` and `editable=true`. |
| Browse reusable workouts | `queryWorkoutLibrary` → `queryWorkoutDetails` when needed | These are templates in the user's own library. |
| Save a reusable template | `createSingleWorkout` | Saves only to the library, without a date. |
| Modify a library template | `queryWorkoutDetails` → `updateWorkoutDetails` | Does not alter copies already placed on the schedule. |
| Create a brand-new workout on a date | `createScheduledWorkout` | Saves directly to that date, not to the library; do not create a template just to schedule it. |
| Put an existing library workout on a date | `queryWorkoutLibrary` → `scheduleWorkout` | Copies the existing template, leaving the original unchanged. |
| View or modify a standalone workout on a date | `queryTrainingSchedule` → `queryScheduledWorkoutDetails` → `updateScheduledWorkout` only when an edit is requested | Use the returned date and `idInPlan`; plan workouts instead use `updateTrainingPlan`. |

### Preserve the correct training content

- Obtain all identifiers from actual results. Pass plan, library-workout and scheduled-copy identifiers as full decimal strings where the live schema requires them; never interchange them or display internal IDs to the user.
- Always read the corresponding details before editing. For a library workout or standalone scheduled workout, start from the returned course JSON, change only what the user requested and submit the complete course. Preserve unchanged sections, intensity metrics and values, free-mode targets and unset-intensity fields.
- Plan updates are incremental by day, not by individual workout: omitted days stay unchanged, but each submitted day replaces all workouts on that day. Include every workout that must remain that day. A rest entry clears the whole day. A day with any completed workout is skipped; report these skips honestly.
- New plans cover 4–16 natural Monday–Sunday weeks and start between today and 14 days from today. The first week may be partial; the final week must contain a workout. Changing the total length requires the complete matching phase table, and shortening can remove workouts after the new end date.
- New structured workouts support running, cycling and trail running. Training-course sport codes are 1/2/5 (4 for a plan rest day), not activity-record codes such as 100/200. Existing library strength or swimming workouts may be scheduled even though creating or editing them is unsupported.
- `createScheduledWorkout` and `scheduleWorkout` accept a single date from today through today + 90 days, inclusive, using the COROS account timezone. Read the live description for date, target, intensity and course-size constraints. Keep names and descriptions in natural athlete-facing language.
- Multiple existing workouts on one date do not block adding another, but tell the user about other workouts returned by the server. Scheduling the same library workout on the same date does not add another copy; do not assume direct workout creation has the same duplicate protection.
- Library templates and scheduled copies are independent. After updating a scheduled workout, use the saved `idInPlan` returned by that update for further changes, as it may differ.
- Do not use creation as a workaround for a modification request, bypass `editable=false`, or clear all days to simulate quitting a plan. Moving or removing standalone scheduled workouts and quitting or deleting plans require the COROS App.

### Verify writes and handle uncertain outcomes

- A successful helper process does not by itself mean the requested training change succeeded: inspect `isError` and the returned content for rejection reasons, skipped days and actual saved results.
- On a timeout, interrupted connection or incomplete response from a write, do not blindly repeat the call. Query the relevant library, plan or date first to determine whether the change was saved; if still uncertain, ask the user to verify in the COROS App before another write.
- If a tool is absent after a live refresh, explain that the current connection does not expose it. Never claim a change was saved when only a proposed plan was produced.

### Example routing

- "Add a new 30-minute easy run for tomorrow": inspect `createScheduledWorkout`, resolve tomorrow's date, design the course and save directly to the schedule.
- "Shorten tomorrow's run": query the schedule, identify whether it is a plan workout or a standalone copy, read the appropriate details, then update that object while preserving other content.
- "Save this as a reusable workout": use `createSingleWorkout`; do not schedule it unless the user also requests a date.

## Notes

- Use `apply-openclaw` for setup or refresh. It will reuse saved login when possible and otherwise start the browser-based login flow.
- Use `login-start` + `login-finish` when the browser may be on a different computer, or when the original terminal might be interrupted before the login completes.
- Use `login-status` to check whether the original machine still has a saved pending login and to reprint the browser link.
- Gateway mode keeps separate local state under `~/.coros-mcp-skill-gateway/<region>/`, so CN, EU, and US tokens do not overwrite each other.
- If you must force a specific cluster, pass `--issuer https://mcpcn.coros.com`, `--issuer https://mcpeu.coros.com`, or `--issuer https://mcpus.coros.com`.
- `list-tools`, `describe-tool`, and `call-tool` automatically reuse the local token cache and refresh the token before MCP requests when it is near expiry.
- `list-tools` and `describe-tool` reuse a short-lived local tool catalog cache by default. Use `--refresh` when you want the latest live tool list immediately.
- MCP runtime calls use the current stateless `/mcp` flow; do not require `Mcp-Session-Id` and do not send `notifications/initialized`.
- For natural-language requests, first run cached `list-tools`, choose the best matching tool from the current server response, inspect it with `describe-tool` only when the arguments are not obvious, then run `call-tool`.
- If the selected tool needs required arguments that are still missing, ask the user only for those missing fields instead of dumping the full schema back to them.
- If the user explicitly asks to keep using the old password-based flow, run the helper with `--legacy` and pass `--username`. The password will be prompted interactively.
- Use `logout` only if the user explicitly asks to clear saved local login state.
- Do not invent a second config path; always use the helper in this skill's `scripts/` directory.
- This is the hardened version. Token values are never printed to stdout. Error messages are sanitized to prevent sensitive data leakage.
