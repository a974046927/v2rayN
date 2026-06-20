# Girl Persona Addressing Rule

Source commit: `1af844b Enforce girl persona address rules`

## Rule

Girl persona may only address the user as:

- `夜雨哥哥`
- `哥哥`
- `凌凌哥哥`

Girl persona output must not contain bare `夜雨` anywhere after the approved names are removed.

## Source Changes

- `src/yoruame_pet/dialogue.py`
  - Adds `GIRL_APPROVED_NAMES = ("夜雨哥哥", "哥哥", "凌凌哥哥")`.
  - Uses that constant for `names_by_persona["girl"]`.
  - Changes late-night and rain fragments so they do not introduce bare `夜雨`.
  - Adds `_normalize_persona_addressing()` as a final safety pass for girl-persona output.
- `src/yoruame_pet/weather.py`
  - Rain reminder now says `哥哥` instead of bare `夜雨`.
- `src/yoruame_pet/loop_benchmark.py`
  - Adds `girl_addressing_rule`, now included in the 15/15 loop baseline.

## Test Coverage

- `tests/test_core_behavior.py::test_girl_persona_only_uses_approved_names`
- `tests/test_core_behavior.py::test_girl_persona_never_uses_bare_yeyu_address`
- `tests/test_core_behavior.py::test_weather_summary_classifies_rain_and_sun`
- `tests/test_loop_benchmark.py::test_loop_benchmark_covers_updated_goal_requirements`

Verified locally on 2026-06-20:

```text
Ran 38 tests in 0.891s
OK

Loop engineering baseline: 15/15 checks pass.
```
