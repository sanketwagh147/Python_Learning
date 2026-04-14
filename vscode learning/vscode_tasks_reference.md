# VS Code `tasks.json` Documentation

## Introduction
The `tasks.json` file in Visual Studio Code automates custom scripts and workflows (like building, running tests, or starting servers) directly from the editor. It bridges the gap between CLI tools and the VS Code IDE.

## 1. Global Properties
| Property | Type | Description |
| :--- | :--- | :--- |
| **`version`** | `string` | Task configuration version (Standard is `"2.0.0"`). |
| **`tasks`** | `array` | A list of task objects detailing individual commands and their configurations. |
| **`inputs`** | `array` | Defines variables that prompt the user for input when executing a parameterized task. |

## 2. Task Object Properties
| Property | Type | Description |
| :--- | :--- | :--- |
| **`label`** | `string` | The display name of the task in the VS Code UI. |
| **`type`** | `string` | Defines execution context. Options: `"shell"` (runs in terminal), `"process"` (runs as direct process), or extension-specific (e.g., `"npm"`, `"cargo"`). |
| **`command`** | `string` | The actual command, script, or executable to run (e.g., `uv run pytest`, `npm start`). |
| **`args`** | `array` | Arguments passed to the command. |
| **`isBackground`** | `boolean` | If `true`, the task runs continuously in the background (e.g., a dev server or file watcher). |
| **`dependsOn`** | `array/string` | Tasks that must run before this task. |
| **`dependsOrder`** | `string` | `"sequence"` (run dependencies sequentially) or `"parallel"` (run simultaneously). |
| **`group`** | `string/object` | Groups tasks together. Common values: `"build"`, `"test"`. Can be an object like `{"kind": "build", "isDefault": true}` to set as default build task. |
| **`problemMatcher`** | `array/string` | Parses terminal output to highlight errors/warnings in the editor. E.g., `"$python"`, `"$tsc"`. |

## 3. Presentation Options (`presentation` object)
Controls the terminal behavior when the task runs.
| Property | Type | Description |
| :--- | :--- | :--- |
| **`reveal`** | `string` | When to show the terminal: `"always"`, `"silent"`, or `"never"`. |
| **`panel`** | `string` | Terminal instance handling: `"shared"` (reuses), `"dedicated"` (keeps task isolated), or `"new"` (opens new tab every time). |
| **`clear`** | `boolean` | Clears terminal before execution. |
| **`focus`** | `boolean` | Focuses the terminal window upon execution. |
| **`group`** | `string` | Groups multiple tasks into a single split terminal pane. |

## 4. Input Variables (`inputs` object)
Used to parameterize tasks interactively.
| Property | Type | Description |
| :--- | :--- | :--- |
| **`id`** | `string` | The variable identifier used in tasks as `${input:id}`. |
| **`type`** | `string` | `"promptString"` (free text input) or `"pickString"` (dropdown list). |
| **`description`** | `string` | The text prompt shown to the user. |
| **`default`** | `string` | Default value if the user presses Enter. |
| **`options`** | `array` | List of string options (Required if `type` is `"pickString"`). |

## 5. Built-in Variables
VS Code provides environment variables you can use in commands.
| Variable | Description |
| :--- | :--- |
| **`${workspaceFolder}`** | The absolute path of the folder opened in VS Code. |
| **`${file}`** | The currently opened file. |
| **`${env:Name}`** | References system environment variables (e.g., `${env:PATH}`). |
| **`${input:Name}`** | Prompts for a user input defined in the `inputs` array. |
