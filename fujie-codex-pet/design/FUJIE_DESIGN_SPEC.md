# 富江 Design Spec

## Identity

`富江` is a black-and-white horror manga style desktop/Codex pet based on the
current `夜雨影姬` design work. She has a dual persona: a cute girl form and a
cool mature form. Both forms are affectionate, possessive, teasing, and slightly
dangerous.

## Visual Elements

- Black long hair with manga ink highlights.
- Pale black-and-white face and body rendering.
- Beauty mark near the eye.
- Black-and-white cropped top and black layered skirt.
- Belt, chain decorations, small black bag, and chunky black boots.
- Girl form: cute, softer face, more lively expressions.
- Mature form: colder gaze, more composed expression, natural jawline, not a
  sharp V-shaped chin.
- Split-face horror state: second face emerges from the face area, more scary
  and distorted than normal expressions.

## Animation States

The Codex atlas uses the standard 9-row state contract:

- `idle`: quiet breathing/blinking.
- `running-right`: dragging/moving right.
- `running-left`: dragging/moving left.
- `waving`: greeting.
- `jumping`: sudden reaction.
- `failed`: mature split-face scare/failure state.
- `waiting`: waiting for attention or approval.
- `running`: focused work/thinking.
- `review`: review/inspection gaze.

## Interaction Rules

- Face/hair click: affectionate or teasing response.
- Hand/body click: attention and work-related response.
- Skirt/legs click: shy, evasive, non-explicit response.
- Right click: scare/split-face gag.
- Double left click: switch between girl and mature forms.
- Middle click or Ctrl+left click: open the interactive question panel.
- Ignored too long: she pouts, becomes mature/cold, or demands attention.
- Responding after ignored: she softens and becomes cute again.

## Dialogue And Emotion System

Girl persona names:

- `夜雨哥哥`
- `哥哥`
- `凌凌哥哥`

Mature persona may use colder variants such as `夜雨`, `哥哥`, or `凌凌哥哥`.
Girl persona uses warmer, shorter, more openly cute spoken lines. Mature persona
uses colder, more commanding lines while still sounding attached.

Dialogue should be generated from emotion context, not selected from fixed full
sentence templates. The generator should combine:

- current persona: `girl` or `mature`
- current emotion: `happy`, `shy`, `annoyed`, `calm`, `scare`, `work`,
  `review`, `rest`, `move`, `late_night`, `rain`, or `sunny`
- trigger source: face, hair, hand, body, skirt/legs, ignored, reminder, or
  weather
- affection level and emotion intensity

The pet state should persist the current emotion and intensity. User attention
or clicks soften her; ignoring her increases possessive or annoyed moods;
scare/split events use a stronger horror mood. Stronger moods should also make
the bubble visually more intense.

Lines should feel like short human turns, not AI explanations: avoid words such
as "system", "trigger", "current", or "generated"; prefer casual pauses, small
mouth sounds, and direct reactions.

Dialogue UI should look like a cute manga speech bubble:

- Emotion-dependent fill and accent colors.
- Thick black comic outline, heavier for high-intensity emotions.
- Small speech-tail pointing toward the pet.
- Cute font candidates such as `YouYuan`, `Comic Sans MS`,
  `Microsoft YaHei UI`, or platform equivalents.
- Light use of symbols or emoji such as `♡`, `♪`, `✨`, `ฅ`; do not make every
  line noisy.

## Interactive Question Mode

The desktop shell includes an interactive question mode:

- The user can open a small manga-styled question panel from the pet window.
- Typed questions are answered by checking local pet documents first.
- If local documents do not contain a useful answer, the request is passed to an
  AI provider interface.
- If no AI provider is configured, the pet degrades naturally and asks the user
  to type more context instead of crashing.
- Answers are shown through the same pet dialogue bubble and use the `review`
  mood so they still feel like Fujie rather than a generic assistant.

Current local-search roots:

- desktop project root
- `transfer/` handoff folder

The AI provider is currently an adapter boundary with an offline fallback. It is
ready for a future OpenAI, local model, or other provider implementation without
changing the UI contract.

## Voice Input

Voice input is present as an optional interface:

- Voice is disabled by default in config.
- When no speech-recognition backend is installed or enabled, the pet says she
  cannot hear clearly and asks for typed input.
- If a compatible speech recognition backend is installed later, the same
  `VoiceRecognizer` interface can pass recognized Chinese text into interactive
  question mode.

## Reminder Behavior

- Rest reminder after a focus interval.
- Movement reminder after sitting too long.
- Late-night reminder after the configured night hour.
- Weather reminder when weather data is available.
- Weather should mention rain or sunny weather when detected.
- Weather should record the resolved location and source, using a configured
  city first and IP-based location when no city is configured.

## Runtime Notes

For a desktop shell, prefer high-resolution row strips over the final Codex
`192x208` atlas cells. The Codex atlas is correct for Codex pets, but desktop
display looks sharper when rendered from `assets/high-res-rows/`.

Idle animation should stay calm and slow. Use a slower idle frame delay than
active click/reaction states, and keep spontaneous idle talk/scare checks
infrequent enough that the pet does not feel jittery.
