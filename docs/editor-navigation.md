# Editor navigation from Herdr panes

Agents running in [Herdr](https://herdr.dev) panes constantly name Valcraft artifacts: `FEAT-023`, `FEAT-023/T-001`, `Q-004/QT-001`, a bare `T-003`, or a file path with a line number. The Valcraft Herdr plugin opens any of them in your editor at the defining line, with one key and one pick.

Task numbers restart in every feature and quick file, so a text search cannot find the right `T-001`. The plugin resolves each identity against the repository's specs. When a bare identity matches several definitions, it asks you to choose and never opens a guess.

## Requirements

- Herdr 0.9.1 or later.
- `python3`, Python 3.9 or later. macOS ships one as `/usr/bin/python3`.
- Zed or Visual Studio Code, with its command-line launcher on `PATH`: `zed` (or `zeditor` on some Linux distributions) or `code`.
- A Valcraft project: the repository commits `.valcraft/config.yaml`.

## Turn it on, change it, or turn it off

Run Valcraft Tune and choose the `Editor navigation` section. First-time setup offers it whenever `herdr` is on `PATH`.

- **Enable** records your editor and installs the plugin with `herdr plugin install valzav/valcraft/navigation/herdr --ref v<version>`, at the release that matches your Valcraft version. When only one supported launcher is found, Tune picks it without asking.
- **Change editor** replaces the editor and brings the plugin to the matching release.
- **Disable** removes the record. The plugin stays installed, because it is machine-wide and other repositories may use it.

When `python3` or your editor's launcher is missing, Tune installs nothing and tells you how to provide it:

- Zed on macOS: run `cli: install cli binary` from Zed's command palette.
- Visual Studio Code on macOS: run `Shell Command: Install 'code' and optionally 'copilot' commands in PATH` from the Command Palette.
- Python: `xcode-select --install` or `brew install python` on macOS, or your distribution's `python3` package on Linux.

Then run the section again.

The record lives in your gitignored `.valcraft/config.local.yaml`:

```yaml
editor:
  adapter: zed
  executable: /opt/homebrew/bin/zed
```

It belongs to you and this machine, so it is never committed. In a linked git worktree, Tune and the plugin both use the record in the repository's primary checkout. The plugin refuses a record that git tracks or does not ignore, or that is a symbolic link, because the record names a program to run.

## Bind the keys

A Herdr plugin cannot bind keys itself. Add these entries to Herdr's `config.toml`, then run `herdr server reload-config`:

```toml
[[keys.command]]
key = "prefix+t"
type = "plugin_action"
command = "valcraft-navigation.pick"
description = "Valcraft: pick a reference from the pane"

[[keys.command]]
key = "prefix+y"
type = "plugin_action"
command = "valcraft-navigation.open-selection"
description = "Valcraft: open the selected reference"
```

Neither key is a Herdr default. Choose others if they clash with your own bindings.

## Open a reference

### The pane picker

Press the picker key (`prefix+t` above). A popup lists the Valcraft identities and file references in the focused pane's recent output, newest first. File references appear only when the file exists. Move with the arrow keys or `j` and `k`, press Enter to open, or press Escape to cancel.

The pane picker is the main way in. It needs no selection.

### A selected reference

The open key (`prefix+y` above) opens the reference you selected. Select it in Herdr's copy mode: press `prefix+[`, find the reference, for example with `?` and its text, then press `v` and `E` to select it. Then press the open key.

A mouse selection does not work for this key in Herdr 0.9.1 through 0.9.5. Herdr clears the selection when the key is pressed, before the plugin receives it.

### A hyperlink

Control-click a terminal hyperlink to open it in your editor. The plugin handles `file://` links, with an optional `#L<line>` or `#L<line>C<column>` fragment, and `vscode://file/` and `cursor://file/` links. Herdr turns only `http://` and `https://` text into links by itself, so a path or identity printed as plain text is not clickable. Use the pane picker for those.

## What it recognizes

| Reference | Opens |
| --- | --- |
| `FEAT-NNN` | the feature's `spec.md` |
| `FEAT-NNN/T-XXX` | that task's line in the feature's `tasks.md` |
| `Q-NNN` | the quick-task file |
| `Q-NNN/QT-XXX`, `Q-NNN QT-XXX` | that task's line in the quick-task file |
| bare `T-XXX` | the feature task with that number; a picker when several features define it |
| bare `QT-XXX` | the quick task with that number; a picker when several quick files define it |
| `path`, `path:line`, `path:line:column` | the file, at that line and column |

Surrounding backticks, quotes, brackets, and a trailing period, comma, or colon are ignored. A relative path is resolved against the pane's working directory. An identity is resolved against the git checkout the pane is in, including uncommitted edits in a linked worktree. [`navigation/contract.md`](../navigation/contract.md) defines every rule exactly.

Resolution is local and read-only. The plugin reads your files, never git history, tracker state, or the network, and it changes nothing.

## When something goes wrong

The plugin shows every problem in its own small popup. Press any key to close it. It does not use Herdr notifications, because Herdr shows them only when `ui.toast.delivery` is `herdr`, and the default is off.

When your repository's `valcraft_version` is newer than the plugin's release, the plugin warns and still opens what you asked for. Update the plugin from Tune's `Editor navigation` section.

Herdr keeps a log of every plugin command. Read the plugin's entries with:

```sh
herdr plugin log list --plugin valcraft-navigation
```
