# Loop Engineering Baseline

This project uses a local loop-engineering baseline to keep feature work from
stopping at a design note.

The loop is:

1. List concrete requirements.
2. Write tests that fail while the feature is missing.
3. Implement the smallest working behavior.
4. Run the full test suite.
5. Run the local baseline command.
6. Update transfer/GitHub sync documents.
7. Restart the pet and verify the runtime process.
8. Sync the latest changed files to GitHub under `富江/`.

## Current Baseline

```text
Loop engineering baseline: 18/18 checks pass.

click_regions
affection_attention_state
random_scare
form_switch
dialogue_system
girl_addressing_rule
rest_reminder
move_reminder
late_night_reminder
weather_location_source
interactive_question_mode
local_search
local_pet_reply
voice_interaction_flow
voice_fallback
codex_task_status_bridge
github_sync_folder
```

Command:

```powershell
$env:PYTHONPATH='src'
python -m yoruame_pet.loop_benchmark
```
