# 夜雨影姬桌面宠物

## 启动

在 PowerShell 里运行：

```powershell
.\run_pet.ps1
```

## 当前功能

- 透明置顶小窗口。
- 左键拖动移动位置。
- 点击脸、头发、手、身体、裙摆/腿部会出现不同台词。
- 右键会触发短暂惊吓/分裂动作。
- 对话先查本地资料，没查到时用本地宠物语气回复，不接外部 API。
- Codex 线程 `添加宠物对话` 已配置为你和富江的专用对话栏。
- 使用 Codex 时，大号桌宠会读取本机 Codex 会话事件，并显示开始、执行命令、同步、完成等任务状态气泡。
- 长时间不理她会佯装生气。
- 普通待机也会低频出现挥手、跑步、跳跃等动作，不只停在站立状态。
- 会按配置提醒休息、起身走动、深夜休息。
- 天气默认尝试自动定位；也可以在 `config/settings.json` 里填写
  `weather_city`，例如 `Tokyo` 或 `Kyoto`。

## 文件

- 角色素材来自：`C:\Users\lenovo\.codex\pets\yoruame-kagehime\spritesheet.webp`
- 状态存档：`data/state.json`
- 日志：`logs/pet.log`
