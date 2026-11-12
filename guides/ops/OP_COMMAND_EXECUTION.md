# command_execution Op

Executes a shell command with optional working directory, env and shell; captures stdout/stderr and exit status.

## Input Structure

```json
{
  "run": "npm test",
  "working_directory": "/path/to/repo",
  "shell": "bash",
  "env": {
    "CI": "true"
  },
  "continue_on_error": false
}
```

## Output Structure

```json
{
  "stdout": "test output",
  "stderr": "",
  "exit_code": 0,
  "success": true,
  "timed_out": false,
  "error_message": ""
}
```

Recipes must omit execution timeouts. The command operation accepts omission;
it creates a timed context only for a nonempty timeout input. Omission preserves
cancellation and inherited runtime authority bounds. Other operations may select
runtime-owned defaults on omission; inspect their contracts rather than supplying
zero, null, a larger limit, or a watchdog. See the [authoring policy](../RECIPE_AUTHORING_GUIDE.md#execution-timeouts).
