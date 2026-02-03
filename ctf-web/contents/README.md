# CTF Web Guidé

## Scenario
A damaged orbital station leaves behind a diagnostics console. The gate uses a bootstrap code, and the console evaluates expressions on the server. Your goal is to retrieve the flag.

## Steps
1. Find the bootstrap code by inspecting the frontend scripts (base64 in the console logs).
2. Use the code to unlock the diagnostics console.
3. Exploit the eval-based injection to read the flag file.
