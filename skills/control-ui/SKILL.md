---
name: control-ui
description: Verify a web or Electron interface using available browser automation, current page state, and observable interaction evidence.
---

# Control a UI

Use host browser tools or the project's existing Playwright/Cypress/Electron harness. Do not assume a particular MCP tool, in-app browser, port, or selector. If no suitable browser is available, report the missing capability instead of claiming a UI check.

1. Identify the app, requested flow, local launch command, and test environment. Reuse an existing dev server or start an owned one; record which resources you own.
2. Select the page by URL and stable app markers, not tab order. Inspect current accessibility/DOM state or a screenshot.
3. Choose a current target, preferably a semantic role/label or stable test ID. Perform one interaction, capture fresh state, and verify the expected change before continuing.
4. Inspect console/network failures when relevant. Use disposable test data; do not treat a successful click API call as proof of the desired state.
5. Save focused screenshots/traces when they support the claim. Use before/after views under comparable viewport/theme/data conditions. Minimize sensitive content.
6. Close only resources this run created. An attached CDP browser or user session must remain available; use the tool's disconnect semantics rather than a generic browser-close call unless you own that browser.

Use coordinate actions only with a fresh screenshot. Prefer explicit readiness conditions over sleeps. Do not add framework dependencies solely for a one-off check unless requested. Report the tested flow, evidence, failures, and unavailable features. Link local artifacts using the host's preview mechanism.
