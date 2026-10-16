# COROS MCP FAQ

[English](faq.md) | [中文](../zh/faq.md) | [Getting started](getting-started.md) | [Home](../../README.md)

## 1. Which platforms does COROS MCP support?

MCP is an open standard for connecting external systems. You can think of MCP as a "USB port" for AI applications. Whether a platform can connect depends on whether it supports adding MCP services and whether it supports the authentication method required by COROS MCP.

We currently recommend using verified platforms first, such as ChatGPT, Claude, OpenClaw, Workbuddy, and Hermes.

If the platform you use does not yet support MCP, you can follow its future updates. Once the platform opens compatible MCP connection capabilities, you will be able to connect COROS according to that platform's rules.

## 2. Do I need to pay to use COROS MCP?

COROS MCP itself is free of charge. You can authorize and connect your COROS account on AI platforms that support MCP, then use the currently available features.

Please note that some AI platforms may apply membership, subscription, or quota limits to MCP, external tool connections, advanced models, or developer mode settings. These fees are charged by the corresponding AI platform and are not determined by COROS. Please refer to the latest rules of the platform you use.

## 3. Unable to complete authorization?

First, make sure your COROS account can log in and work normally in the COROS App, and that your account already contains data that can be viewed.

If authorization still fails, please check:

1. Whether the authorization page has fully opened, and whether your browser blocked pop-ups or redirects.

2. Whether you signed in with the correct COROS account.

3. Whether the old connection has been removed inside the AI platform and re-authorized.

If repeated attempts still fail, save a screenshot of the error message and contact COROS customer support for troubleshooting.

## 4. MCP URL is invalid?

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
      <td nowrap>United States and other regions</td>
      <td nowrap><code>https://mcpus.coros.com/mcp</code></td>
    </tr>
  </tbody>
</table>

## 5. How do I refresh the MCP tool list after COROS MCP is updated?

When COROS MCP adds or updates tools, refresh the MCP tool list in your AI platform so the assistant can see the latest available capabilities. The exact refresh entry may vary by platform.

If the new tools still do not appear, try starting a new conversation or reconnecting COROS MCP.

## 6. Seeing a session expired message when using the Skill?

This usually happens when you connected to COROS through the Skill method with an older Skill version. Earlier Skill versions used a session-based MCP flow that depended on the `Mcp-Session-Id` session header. COROS MCP now uses the latest stateless MCP flow, and the latest Skill has been updated to support it.

Update the local Skill package:

```bash
npm install -g coros-mcp@latest
```

After the update, reconnect COROS MCP or start the Skill login flow again, then retry your request.

## 7. AI cannot retrieve COROS data?

If COROS MCP has been connected successfully but AI cannot retrieve data, try the following steps:

1. Confirm that the corresponding data already exists in the COROS App. Device data must first sync to the COROS App and then upload to the cloud. If the data does not exist in the App, AI cannot read it.

2. Open a new conversation window, or send `/new` in a supported client before asking again.

3. Use more explicit instruction, such as: "Please call COROS MCP and check my activity records from the past 7 days."

## 8. Why are AI answers inaccurate?

AI response quality can be affected by model capability, prompt wording, accessible data range, and other factors.

If an answer is clearly inaccurate, try starting a new conversation, explicitly ask it to "call COROS MCP," and specify the time range and data type. For example: "Please call COROS MCP and analyze how my running training load changed over the past 4 weeks."

We recommend using models with capabilities equivalent to DeepSeek V4 Flash or higher. Models with weaker tool-calling capability may fail to use tools or may use incorrect parameters.

## 9. Can COROS MCP retrieve .fit files?

**Yes.** COROS MCP supports retrieving `.fit` files for activity records, enabling deeper data analysis.

This approach also helps avoid overwhelming the AI context window with large amounts of second-by-second data.

We provide two ways to retrieve files:

- **Direct retrieval:** Read the `.fit` file entity directly.

- **Link retrieval:** Retrieve the file download link.

<strong>Note:</strong> Whether an AI assistant can directly display or process file entities depends on the capabilities and permission controls of the AI platform you are using. If a file cannot be downloaded or read, we recommend contacting customer support for the corresponding AI platform.

**Download limit:** File retrieval and download-URL retrieval share a **50-file** allowance per fixed **24-hour** window for the connected platform user; later calls do not extend that window.

## 10. Who can see my data? Is it safe?

Only after you actively authorize access can an AI application access data within the authorized scope through COROS MCP. Your COROS data remains protected by the COROS account system and privacy policy. AI conversation content and model processing methods are governed by the policies of the AI platform you use. We recommend connecting COROS MCP only on platforms you trust.
