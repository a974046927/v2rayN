# fujie-codex-pet

## 名称

- Codex pet id: `fujie`
- displayName: `富江`
- description: `富江`
- spritesheetPath: `spritesheet.webp`

## 当前本地文件

- 本地 Codex 宠物目录: `C:\Users\lenovo\.codex\pets\fujie`
- 本地桌面宠物工程: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Mac/转移包: `E:\Codex 项目\杂谈\fujie-codex-pet-transfer.zip`
- 最新本地提交: `e95d53d Improve emotion dialogue and idle pacing`
- 当前验证: `26` 项测试通过

## 角色设定

黑白漫画风桌面宠物，整体是冷艳、病态、黏人、会撒娇也会吓人的双形态角色。

### 少女形态

- 更可爱，表情更生动。
- 称呼只使用: `夜雨哥哥`、`哥哥`、`凌凌哥哥`。
- 语气更软、更贴近真人短句，不使用明显 AI 说明腔。
- 被点击脸、头发、手、身体时会撒娇或调皮回应。
- 被点裙子/下半身时会害羞、躲闪，但保持非露骨表达。

### 御姐形态

- 更冷艳、眼神更压迫，脸型自然，不要尖下巴。
- 可以使用更冷的称呼和命令式语气。
- 用户长时间不理她时，会切换到冷淡/吃醋/佯装生气状态。
- 右键或惊吓状态会触发分裂脸、吐舌鬼脸等恐怖漫画风反馈。

## 视觉设计

- 黑色长发，带漫画墨线高光。
- 眼下/脸部保留标志性痣。
- 黑白短上衣、黑色分层裙、腰带、链条、小包、厚底黑靴。
- 整体不要紫色描边。
- 桌面显示优先使用高分辨率行图，避免直接放大 `192x208` Codex atlas 造成模糊。
- 分裂头状态更偏从脸部裂出第二张脸，御姐版和少女版外形不要完全一样。

## 动画状态

Codex atlas 使用标准 9 行状态:

- `idle`: 慢速待机、呼吸、眨眼，不能过快。
- `running-right`: 向右拖动/移动。
- `running-left`: 向左拖动/移动。
- `waving`: 打招呼、被注意到。
- `jumping`: 突然反应。
- `failed`: 分裂脸/惊吓/吐舌鬼脸。
- `waiting`: 等待关注、佯装不满。
- `running`: 工作中、专注陪伴。
- `review`: 检查、盯进度、提醒用户认真。

当前待机节奏:

- 默认动画: `260ms` 每帧。
- idle: `520ms` 每帧。
- waiting: `380ms` 每帧。
- review: `360ms` 每帧。
- failed: `340ms` 每帧。
- 待机自言自语/惊吓检查间隔已拉长，避免一直跳动。

## 情绪系统

当前状态会保存:

- `persona`: `girl` 或 `mature`
- `mood`: 当前情绪
- `mood_intensity`: 情绪强度
- `affection`: 亲密度

主要情绪:

- `happy`: 开心、被理会。
- `shy`: 害羞，主要用于裙子/下半身点击。
- `annoyed`: 被冷落、吃醋、佯装生气。
- `calm`: 御姐冷静提醒。
- `scare`: 惊吓、分裂脸、吐舌鬼脸。
- `work`: 工作陪伴。
- `review`: 检查/审阅。
- `rest`: 休息提醒。
- `move`: 起来走动提醒。
- `late_night`: 深夜提醒。
- `rain`: 下雨提醒。
- `sunny`: 天气好提醒。

## 对话系统

对话不是固定句式，而是由以下上下文生成:

- 当前人格
- 当前情绪
- 触发部位或触发事件
- 亲密度
- 情绪强度

对话要求:

- 更像真人在旁边说短句。
- 少解释，不说“系统”“触发”“当前”“生成”“模板”等 AI 味词。
- 少用过度工整长句。
- 保留少量漫画感符号，例如 `♡`、`♪`、`✨`、`ฅ`。
- 情绪不同，气泡 UI 的颜色、装饰、边框强度也不同。

## 对话框 UI

- 漫画风白底/浅粉底圆角气泡。
- 黑色粗描边。
- 气泡尾巴指向宠物。
- 根据情绪切换填充色、阴影色、强调色、文字色、装饰符号。
- 强烈情绪时边框更重。
- 字体候选: `YouYuan`、`幼圆`、`Comic Sans MS`、`FZYaoti`、`Microsoft YaHei UI`。

## 互动行为

- 点脸: 撒娇、被注意到、打招呼。
- 点头发: 头发被弄乱、轻微抱怨。
- 点手: 牵手、靠近、可爱反馈。
- 点身体: 工作陪伴或注意力反馈。
- 点裙子/下半身: 少女害羞，非露骨。
- 右键: 惊吓/分裂脸/吐舌鬼脸。
- 长时间不理: 佯装生气，切御姐或冷淡状态。
- 用户回应/点击: 情绪软化，变得更可爱。

## 提醒行为

- 休息提醒: 提醒眼睛和肩膀休息。
- 走动提醒: 提醒坐久了起来活动。
- 深夜提醒: 晚上提醒收尾休息。
- 天气提醒: 自动连接天气；下雨提醒带伞，晴天提醒起来走走。

## 本地验证

最近验证结果:

```text
Ran 26 tests in 0.432s
OK
```

关键文件 SHA256:

```text
42E4FE7A303BB9CC88D82C2BE85395F9405311D7EC3BE77B60B7F7DE37C410DD  codex-pet-fujie/pet.json
9E814514DD3C878D886827E58A0F4E1C6C1ACBBA5808075A74C78BE0A070677D  codex-pet-fujie/spritesheet.webp
B905A80B76A6F1C8031F14D8A89F71FDCE4B3E0B75FBBFD24AC8EF799E81C45C  design/FUJIE_DESIGN_SPEC.md
902450414B49FC1E3A72ADD22784B7FD719A4A76D2E09E6E75C648023F2F4175  assets/contact-sheet.png
142B18D03F67228ED8981ABD2782DF84DACA3D6751278D20EFC26AEF21755839  assets/resolution-preview.png
```

转移包 SHA256:

```text
50C43133A40483215F67E6AB5F40379F1017F1FF2D80CF43D2AC199831F0C20D  fujie-codex-pet-transfer.zip
```

## Mac 同步说明

Mac 端可以按此文档复刻设计，并从转移包中拷贝:

```text
codex-pet-fujie/pet.json
codex-pet-fujie/spritesheet.webp
assets/high-res-rows/*.png
design/FUJIE_DESIGN_SPEC.md
```

Codex 宠物包目标结构:

```text
~/.codex/pets/fujie/pet.json
~/.codex/pets/fujie/spritesheet.webp
```

保留描述为 `富江`。