# Model catalog

This file is the only shipped source of model aliases, effort sets, and Herdr presets. `config.md` states the shape of a worker entry and the free-form alias rule; this file states which aliases and efforts are known. Edit this file, and nothing else, when a provider adds or retires a model.

## Known models

Each harness lists its known model aliases with the effort each alias accepts, then the effort set a free-form alias on that harness accepts. A model alias not listed here is a free-form alias; `config.md` defines its syntax and validity.

### Claude (`harness: claude`)

| Alias    | Allowed effort          |
| -------- | ----------------------- |
| `sonnet` | `low`, `medium`, `high` |
| `fable`  | `low`, `medium`, `high` |
| `opus`   | `low`, `medium`, `high` |

Free-form alias effort: `low`, `medium`, or `high`.

### Codex (`harness: codex`)

Aliases are listed from the most capable model down.

| Alias           | Allowed effort                   |
| --------------- | -------------------------------- |
| `gpt-6-astra`   | `low`, `medium`, `high`, `ultra` |
| `gpt-5.6-sol`   | `low`, `medium`, `high`, `ultra` |
| `gpt-5.6-terra` | `low`, `medium`, `high`, `ultra` |

Free-form alias effort: `low`, `medium`, `high`, or `ultra`. Runtime readiness still verifies model availability.

### Cursor (`harness: cursor`)

| Alias             | Allowed effort          |
| ----------------- | ----------------------- |
| `cursor-grok-4.6` | `low`, `medium`, `high` |

Free-form alias effort: `none`, `low`, `medium`, or `high`.

A Cursor model value names a base model alias, not a complete catalog slug. The Herdr backend appends the effort itself: it passes `--model <model>-<effort>`, or `--model <model>` alone for effort `none`, so the Cursor CLI receives a catalog slug such as `cursor-grok-4.6-high`. Reject a free-form Cursor value that uses bracket syntax or already carries an effort or `fast` suffix, because the backend owns those suffixes. Runtime readiness verifies that the constructed catalog slug is available.

## Herdr presets

Each preset assigns one model and effort per harness. The role-to-harness split is the same for every preset and lives in `config.md`; a preset fills in the model and effort for every role on that harness.

| Preset     | Claude        | Codex                | Summary for the operator                                                                      |
| ---------- | ------------- | -------------------- | --------------------------------------------------------------------------------------------- |
| `Balanced` | `opus` medium | `gpt-5.6-sol` high   | use Claude Opus at medium and Codex Sol at high effort with independent reviewers             |
| `Quality`  | `fable` high  | `gpt-6-astra` high   | use Claude Fable and Codex Astra at high effort with the same independent role split          |
| `Economy`  | `sonnet` high | `gpt-5.6-sol` medium | use Claude Sonnet at high and Codex Sol at medium effort with the same independent role split |

`Balanced` is the recommended preset. In the Custom flow, its model for the chosen harness is the recommended model; for Cursor, which no preset uses, `cursor-grok-4.6` is the recommended model. `medium` is the recommended effort for every model.
