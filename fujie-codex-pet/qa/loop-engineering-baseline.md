# Loop engineering baseline

Loop engineering baseline: 16/16 checks pass.

- `click_regions`: PASS - face/hair/body/hand/skirt_legs mapped
- `affection_attention_state`: PASS - affection, attention, mood persist
- `random_scare`: PASS - scare chance configured as 0.04
- `form_switch`: PASS - double-click form switch action exists
- `dialogue_system`: PASS - generated emotion dialogue is active
- `girl_addressing_rule`: PASS - girl persona only uses 夜雨哥哥/哥哥/凌凌哥哥
- `rest_reminder`: PASS - rest reminder due after focus interval
- `move_reminder`: PASS - movement reminder due after sitting interval
- `late_night_reminder`: PASS - late-night reminder due after configured hour
- `weather_location_source`: PASS - weather keeps resolved location and source
- `interactive_question_mode`: PASS - question mode returns a pet-styled answer
- `local_search`: PASS - local search adapter is available and safe
- `ai_adapter_fallback`: PASS - AI adapter has offline fallback
- `voice_interaction_flow`: PASS - recognized speech is answered and sent to voice reply
- `voice_fallback`: PASS - voice recognizer degrades without crashing
- `github_sync_folder`: PASS - sync target is fujie-codex-pet/
