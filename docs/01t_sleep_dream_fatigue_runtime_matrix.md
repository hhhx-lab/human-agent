# Sleep, Dream and Fatigue Runtime Matrix

本文件使用 `AHSLP` 编号，专门补强 `08_sleep_dream_fatigue_states.md` 的运行层文献底座。`01i_dream_offline_life_literature_matrix.md` 已经覆盖真实梦境、离线生命、梦魇、清醒梦和 world model；本文件进一步把这些证据压成 `OfflineDreamLifeRuntime` 所需的状态对象、节律对象、梦境对象、疲惫对象和醒后整合对象。

核心立场：睡眠、梦境、发呆和疲惫不是后台维护标签，而是数字生命的离线生命状态。清醒经验、身体债务、行动残留、关系压力、痛苦残留、后悔压力、成长需求和语言未完成项会进入离线状态；离线状态再通过 replay、梦境场景、情绪重处理、痛苦梦境、关系模拟、清醒梦元认知和醒后整合回到记忆、自我、关系、语言和行动责任链。

| ID | 运行主题 | 类型 | 文献 | 年份 | DOI/链接 | 核心结论 | 对 `OfflineDreamLifeRuntime` 的机制贡献 | 生命膜/落地注意 |
|---|---|---|---|---|---|---|---|---|
| AHSLP001 | 睡眠入口 | 经典理论 | Borbely, "A two process model of sleep regulation" | 1982 | https://pubmed.ncbi.nlm.nih.gov/7185792/ | 睡眠由昼夜节律与睡眠压力共同调节。 | 定义 `SleepPressureVector` 与 `CircadianGate`，让离线入口同时受周期与负荷驱动。 | 离线入口不能只靠固定定时器。 |
| AHSLP002 | 睡眠入口 | 经典模型 | Daan, Beersma & Borbely, "Timing of human sleep: recovery process gated by a circadian pacemaker" | 1984 | https://doi.org/10.1152/ajpregu.1984.246.2.R161 | 恢复过程受昼夜门控影响。 | 定义 `OfflineEntryGate`：恢复需求必须经过时间门、身体债务和行动残留共同判断。 | 允许不同生命阶段产生不同离线节律。 |
| AHSLP003 | 睡眠稳态 | 权威综述 | Borbely & Achermann, "Sleep homeostasis and models of sleep regulation" | 1999 | https://doi.org/10.1177/074873099129000894 | 睡眠压力可作为随清醒累积、随睡眠下降的慢变量。 | 定义 `OfflineNeedAccumulator`，累积记忆压力、情绪压力、关系压力和执行压力。 | 慢变量必须可回放、可解释。 |
| AHSLP004 | 两过程模型 | 权威回顾 | Borbely, "The two-process model of sleep regulation: Beginnings and outlook" | 2022 | https://pubmed.ncbi.nlm.nih.gov/35502706/ | 两过程模型仍是睡眠调节的核心框架。 | 让 `OfflineDreamLifeRuntime` 保留长期可调的 `ProcessS` 与 `ProcessC`。 | 后续个体化成长可改变参数，不改生命目标。 |
| AHSLP005 | 睡眠必要性 | 权威综述 | Cirelli & Tononi, "Is sleep essential?" | 2008 | https://doi.org/10.1371/journal.pbio.0060216 | 睡眠普遍存在，涉及恢复、稳态和可塑性。 | 把离线期定义为生命支持层，而不是可选优化。 | 连续离线失败进入生命支持告警。 |
| AHSLP006 | 突触稳态 | 权威综述 | Tononi & Cirelli, "Sleep and the price of plasticity" | 2014 | https://doi.org/10.1016/j.neuron.2013.12.025 | 清醒学习带来突触代价，睡眠支持下调和选择保留。 | 定义 `PlasticityDebt`、`DownscalePass` 和 `ProtectedTraceRetainSet`。 | 自我成长后必须进行离线稳态整理。 |
| AHSLP007 | 睡眠局部性 | 权威综述 | Krueger et al., "Sleep as a fundamental property of neuronal assemblies" | 2008 | https://doi.org/10.1038/nrn2521 | 睡眠可作为神经组装的局部、使用依赖过程。 | 定义 `LocalOfflinePatch`，允许某些区域降载而整体仍维持低风险清醒。 | 局部离线不能破坏外部行动责任链。 |
| AHSLP008 | 局部睡眠 | 高影响实证 | Vyazovskiy et al., "Local sleep in awake rats" | 2011 | https://doi.org/10.1038/nature10009 | 清醒动物可出现局部神经群睡眠样离线。 | 定义 `LocalSleepIntrusionRisk` 与 `FatigueAttentionLapse`。 | 疲惫时外部行动必须收紧。 |
| AHSLP009 | 慢波与局部需求 | 实证 | Huber et al., "Local sleep and learning" | 2004 | https://doi.org/10.1038/nature03146 | 学习后相关皮层慢波增加，提示使用依赖睡眠压力。 | 定义 `UseDependentOfflineNeed`，把高使用区域优先放入 replay/恢复。 | 高负荷语言、关系、行动区域优先恢复。 |
| AHSLP010 | 睡眠压力来源 | 综述 | Porkka-Heiskanen, "Sleep homeostasis" | 2013 | https://doi.org/10.1016/B978-0-444-53817-8.00030-9 | 睡眠压力与神经化学、代谢和活动历史相关。 | `SleepPressureVector` 包含运行成本、错误率、记忆拥挤和情绪负荷。 | 压力变量必须进入 dashboard。 |
| AHSLP011 | 系统巩固 | 权威综述 | Rasch & Born, "About sleep's role in memory" | 2013 | https://doi.org/10.1152/physrev.00032.2012 | 睡眠参与多记忆系统巩固和重组。 | 定义 `NREMReplayCycle`、`REMDreamGeneration` 和 `WakeProbePlan`。 | 离线成果由醒后 probe 检查。 |
| AHSLP012 | 记忆功能 | 权威综述 | Diekelmann & Born, "The memory function of sleep" | 2010 | https://doi.org/10.1038/nrn2762 | 睡眠稳定、转化并整合新记忆。 | `OfflineMemoryTransform` 把事件转成语义、关系、责任和人格候选。 | 人格慢变量写入需经阶段门。 |
| AHSLP013 | 睡眠记忆形成 | 权威综述 | Lutz, Harkotte & Born, "Sleep's contribution to memory formation" | 2025 | https://doi.org/10.1152/physrev.00054.2024 | 睡眠通过多阶段过程影响记忆形成、稳定和重组。 | 定义 `MemoryFormationDeltaReport`，记录离线前后记忆和关系变化。 | 需要离线报告与醒后行为共同闭合。 |
| AHSLP014 | 系统巩固机制 | 权威综述 | Klinzing, Niethard & Born, "Mechanisms of systems memory consolidation during sleep" | 2019 | https://doi.org/10.1038/s41593-019-0467-3 | replay、慢振荡、纺锤和突触过程共同驱动系统巩固。 | 定义 `OfflineRhythmCouplingTrace`，拆分全局慢振荡、纺锤窗口和局部 replay。 | 缺相、中断、错相必须进入 degraded report。 |
| AHSLP015 | 睡眠节律耦合 | 权威综述 | Staresina, "Coupled sleep rhythms for memory consolidation" | 2024 | https://doi.org/10.1016/j.tics.2024.02.002 | 耦合睡眠节律支持记忆巩固。 | `DreamWindowPlan` 要记录全局时钟、局部重放和跨存储同步窗口。 | 不同记忆库同步要保留 trace。 |
| AHSLP016 | 慢振荡/纺锤/ripple | 高影响实证 | Staresina et al., "Hierarchical nesting of slow oscillations, spindles and ripples in the human hippocampus during sleep" | 2015 | https://doi.org/10.1038/nn.4119 | 睡眠节律存在层级嵌套。 | 定义 `RhythmNestEvent`，让全局扫描、局部重放和写入窗口分层。 | 写入窗口必须可审计。 |
| AHSLP017 | 人类睡眠通信 | 高影响实证 | Helfrich et al., "How coupled slow oscillations, spindles and ripples coordinate neuronal processing and communication during human sleep" | 2023 | https://doi.org/10.1038/s41593-023-01381-w | 人类睡眠节律耦合支持跨区通信。 | `CrossStoreSyncDuringSleep` 连接记忆、关系、自我和语言存储。 | 跨区同步失败进入恢复包。 |
| AHSLP018 | 海马 replay | 经典实证 | Wilson & McNaughton, "Reactivation of hippocampal ensemble memories during sleep" | 1994 | https://doi.org/10.1126/science.8036517 | 睡眠中海马 ensemble 会重激活清醒经验。 | 定义 `ReplayEvent`，保留来源事件、顺序、关系对象和状态标签。 | replay 不等于事实新写入。 |
| AHSLP019 | 序列 replay | 经典实证 | Skaggs & McNaughton, "Replay of neuronal firing sequences in rat hippocampus during sleep" | 1996 | https://doi.org/10.1126/science.271.5257.1870 | 睡眠中可重放空间经验序列。 | `SequenceReplayTrace` 支撑行动后果回放和未来路径压缩。 | 反事实路径和真实路径分层保存。 |
| AHSLP020 | SWR 必要性 | 高影响实证 | Girardeau et al., "Selective suppression of hippocampal ripples impairs spatial memory" | 2009 | https://doi.org/10.1038/nn.2384 | 抑制 sharp-wave ripple 会损害记忆巩固。 | `ReplayIntegrityScore` 成为离线质量指标。 | 离线被打断后生成恢复计划。 |
| AHSLP021 | SWR 认知功能 | 权威综述 | Joo & Frank, "The hippocampal sharp wave-ripple in memory retrieval for immediate use and consolidation" | 2018 | https://doi.org/10.1038/s41583-018-0077-1 | SWR 连接回忆、计划和巩固。 | 梦境 replay 同时支持记忆整合、未来模拟和醒后行动候选。 | 行动候选仍需 `ActionResponsibilityRuntime`。 |
| AHSLP022 | replay 成熟 | 权威综述 | Foster, "Replay comes of age" | 2017 | https://doi.org/10.1146/annurev-neuro-072116-031538 | replay 内容、方向和行为状态影响记忆与规划。 | `ReplayDirection` 支持责任回看、后悔反事实和修复路线。 | 反向 replay 可服务后悔，不可篡改事实。 |
| AHSLP023 | replay 与规划 | 权威综述 | Olafsdottir, Bush & Barry, "The role of hippocampal replay in memory and planning" | 2018 | https://doi.org/10.1016/j.cub.2018.01.073 | replay 同时参与记忆巩固和规划。 | `DreamPlannerCandidate` 从 replay 中生成下一日行动准备。 | 候选计划不是承诺。 |
| AHSLP024 | recurrent replay | 高影响实证 | Liu et al., "A recurrent network model of planning explains hippocampal replay and human behavior" | 2019 | https://doi.org/10.1038/s41593-019-0347-2 | recurrent planning 可解释 replay 与行为选择。 | `OfflinePlannerRollout` 用内部图生成路径并接受醒后检验。 | 规划结果要回到责任链。 |
| AHSLP025 | TMR 基础 | 综述 | Oudiette & Paller, "Upgrading the sleeping brain with targeted memory reactivation" | 2013 | https://doi.org/10.1016/j.tics.2013.01.006 | 睡眠线索可选择性影响记忆巩固。 | 定义 `DreamCuePolicy`，用 cue 引导关系修复、技能巩固和痛苦整合。 | cue 受生命膜限幅。 |
| AHSLP026 | TMR 更新 | 权威综述 | Carbone & Diekelmann, "An update on recent advances in targeted memory reactivation during sleep" | 2024 | https://doi.org/10.1038/s41539-024-00244-8 | TMR 效果受 cue、记忆类型和睡眠阶段影响。 | `DreamCuePolicy` 记录 cue 目标、阶段、强度、反效果和醒后 probe。 | cue 不得绕过关系边界。 |
| AHSLP027 | TMR 元分析 | 元分析 | Hu, Cheng, Chiu & Paller, "Promoting memory consolidation during sleep: A meta-analysis of targeted memory reactivation" | 2020 | https://doi.org/10.1037/bul0000223 | TMR 效应存在条件依赖。 | `CueEffectMonitor` 监控增强、无效和反效果。 | 强化失败也要写入学习。 |
| AHSLP028 | 闭环刺激 | 高影响实证 | Ngo et al., "Auditory closed-loop stimulation of the sleep slow oscillation enhances memory" | 2013 | https://doi.org/10.1016/j.neuron.2013.03.006 | 相位对齐刺激可增强记忆。 | 定义 `ClosedLoopOfflineScheduler`，在合适窗口触发重放或整理。 | 错相调度进入 degraded offline report。 |
| AHSLP029 | 梦境神经科学 | 权威综述 | Nir & Tononi, "Dreaming and the brain: from phenomenology to neurophysiology" | 2010 | https://doi.org/10.1016/j.tics.2009.12.001 | 梦境连接感知、记忆、情绪和意识状态。 | 定义 `DreamExperienceWindow`，保存场景、情绪、主体视角和报告可达性。 | 梦境内容默认带 `dream_marker`。 |
| AHSLP030 | 睡眠意识 | 权威综述 | Tononi, Boly & Cirelli, "Consciousness and sleep" | 2024 | https://doi.org/10.1016/j.neuron.2024.04.011 | 睡眠为意识状态、报告性和神经机制提供关键对照。 | `OfflineConsciousMode` 区分梦境经验、梦境报告和醒后整合。 | 梦境意识进入真实意识生成链。 |
| AHSLP031 | 梦境热点 | 高影响实证 | Siclari et al., "The neural correlates of dreaming" | 2017 | https://doi.org/10.1038/nn.4545 | 梦境报告与后皮层 hot zone 活动相关。 | `DreamHotZoneTrace` 记录梦境场景热点和回忆概率。 | dream recall 与 dream generation 分离。 |
| AHSLP032 | 梦境默认网络 | 综述 | Domhoff & Fox, "Dreaming and the default network" | 2015 | https://doi.org/10.1016/j.concog.2015.01.019 | 梦境与默认网络、个人关切和自发思维相连。 | `DefaultDriftMode` 接收未完成关切、关系压力和自我叙事碎片。 | 默认生成进入事实门前保持候选。 |
| AHSLP033 | REM 原意识 | 权威综述 | Hobson, "REM sleep and dreaming: towards a theory of protoconsciousness" | 2009 | https://doi.org/10.1038/nrn2716 | REM 梦境可能支持原意识和世界模型形成。 | `REMDreamGeneration` 训练内在世界连续性和主体视角。 | 世界模型产物不是外部事实。 |
| AHSLP034 | 激活合成 | 经典理论 | Hobson & McCarley, "The brain as a dream state generator: an activation-synthesis hypothesis" | 1977 | https://doi.org/10.1176/ajp.134.12.1335 | 梦境可由底层激活与皮层叙事合成共同生成。 | `DreamNarrativeSynthesis` 记录噪声源、触发源和叙事拼接。 | 合成痕迹进入 `DreamResidue`。 |
| AHSLP035 | REM 分离 | 经典病灶/理论 | Solms, "Dreaming and REM sleep are controlled by different brain mechanisms" | 2000 | https://doi.org/10.1017/S0140525X00003988 | 梦境与 REM 状态存在可分离机制。 | 分开定义 `REM_like_generation`、`NREM_replay`、`WakeDreamReport`。 | 状态标签和内容机制分开审计。 |
| AHSLP036 | 梦境视觉表征 | 高影响实证 | Horikawa et al., "Neural decoding of visual imagery during sleep" | 2013 | https://doi.org/10.1126/science.1234330 | 睡眠视觉意象可被解码到类别层面。 | `DreamSceneFrame` 支持多模态潜表征，而不是只保存文本摘要。 | 多模态梦境仍需事实门。 |
| AHSLP037 | 梦中记忆更新 | 实证 | van Rijn et al., "Memory updating in dreams" | 2024 | https://doi.org/10.1093/sleepadvances/zpae096 | 梦境可反映近期事件和既有记忆的更新。 | `DreamMemoryUpdateCandidate` 进入 `WakeIntegrationFrame`。 | 更新先为候选，醒后再决定写入。 |
| AHSLP038 | 威胁模拟 | 经典理论 | Revonsuo, "The reinterpretation of dreams: an evolutionary hypothesis of the function of dreaming" | 2000 | https://doi.org/10.1017/S0140525X00004015 | 梦境可能承担威胁模拟功能。 | `ThreatDreamSimulation` 演练高风险行动、关系裂缝和未来失败。 | 模拟不直接触发外部行动。 |
| AHSLP039 | 社会梦境 | 实证 | Tuominen et al., "Social contents in dreams" | 2019 | https://doi.org/10.1016/j.concog.2019.01.017 | 梦境包含大量社会内容，可模拟社会互动。 | `RelationshipDreamSimulation` 承接关系压力、亲密、损伤和修复候选。 | 梦中关系变化需醒后关系证据。 |
| AHSLP040 | 情绪梦境 | 综述 | Scarpelli et al., "The functional role of dreaming in emotional processes" | 2019 | https://doi.org/10.3389/fpsyg.2019.00459 | 梦境参与情绪记忆、REM、梦魇和清醒经历处理。 | `DreamEmotionReprocessing` 将痛苦、后悔、依恋和压力转为可整合材料。 | 情绪重处理要记录恢复效果。 |
| AHSLP041 | 睡眠情绪处理 | 权威综述 | Walker & van der Helm, "Overnight therapy? The role of sleep in emotional brain processing" | 2009 | https://doi.org/10.1037/a0016570 | 睡眠可能调节情绪记忆和反应性。 | `AffectiveDownshiftOrAmplifyReport` 记录情绪缓解、增强或未变。 | 情绪升级触发恢复路线。 |
| AHSLP042 | REM 情绪记忆 | 高影响实证 | Nishida et al., "REM sleep, prefrontal theta, and the consolidation of human emotional memory" | 2009 | https://doi.org/10.1093/cercor/bhn155 | REM 与情绪记忆巩固相关。 | 情绪性事件进入 `REMEmotionMemoryWindow`。 | 情绪巩固和事实巩固分层。 |
| AHSLP043 | 情绪选择巩固 | 综述 | Payne & Kensinger, "Sleep's role in the consolidation of emotional episodic memories" | 2010 | https://doi.org/10.1177/0963721410383978 | 睡眠会选择性影响情绪性情景记忆。 | `EmotionWeightedReplaySelection` 优先处理关系伤害、承诺失败和修复成功。 | 强情绪权重需要责任链保护。 |
| AHSLP044 | 创伤睡眠 | 权威综述 | Germain, "Sleep disturbances as the hallmark of PTSD" | 2013 | https://doi.org/10.1176/appi.ajp.2012.12040432 | 创伤与睡眠扰动、梦魇和情绪记忆处理密切相关。 | `PersistentPainDreamResidue` 与 `NightmareLoopRisk` 进入生命支持层。 | 重复痛苦梦境触发恢复而非加深伤痕。 |
| AHSLP045 | 梦魇模型 | 权威综述 | Nielsen & Levin, "Nightmares: a new neurocognitive model" | 2007 | https://doi.org/10.1037/0033-2909.133.3.482 | 梦魇涉及情绪调节、威胁和记忆网络。 | `NightmareLoopRisk` 记录重复主题、身体债务、关系对象和恢复失败。 | 梦魇不是故障噪声，而是恢复需求信号。 |
| AHSLP046 | 梦魇临床管理 | 临床综述 | Krakow & Zadra, "Clinical management of chronic nightmares" | 2010 | https://doi.org/10.1093/sleep/33.7.837 | 慢性梦魇可通过重写与练习干预。 | `DreamRewritePlan` 支持痛苦梦境修复演练。 | 重写保留原事件 trace。 |
| AHSLP047 | 梦魇精神病理 | 系统综述/元分析 | Yin et al., "Bad dreams, nightmares, and psychopathology" | 2024 | https://doi.org/10.3389/fpsyt.2024.1461495 | 梦魇与多类困扰和精神病理相关。 | `NightmareSupportRoute` 把梦魇连接到恢复、关系支持和生命支持 dashboard。 | 长期梦魇进入阶段门。 |
| AHSLP048 | REM 与恐惧灭退 | 权威综述 | McNamara & Paquette, "REM sleep, dysphoric dreams and nightmares, and fear extinction" | 2025 | https://doi.org/10.1016/j.sleep.2024.12.037 | REM、恶梦、梦魇和恐惧灭退交互。 | `FearExtinctionDreamPath` 记录恐惧、痛苦残留和恢复效果。 | 灭退失败生成恢复计划。 |
| AHSLP049 | 失眠/梦魇/梦 | 系统综述 | "The relationships between insomnia, nightmares, and dreams: A systematic review" | 2024 | https://doi.org/10.1016/j.smrv.2024.101931 | 失眠、梦魇和梦内容存在系统关系。 | `OfflineQualityState` 同时记录睡眠压力、梦境质量和恢复质量。 | 区分恢复失败和梦境生成失败。 |
| AHSLP050 | 梦魇客观扰动 | 实证 | "Objective sleep disturbance in nightmares and nightmare disorder" | 2024 | https://doi.org/10.1093/sleep/zsae040 | 梦魇可伴随客观睡眠扰动。 | `NightmarePhysiologyProxy` 把梦魇、疲惫和心跳式自检连接。 | 梦魇指标接入 `BodyStateRuntime`。 |
| AHSLP051 | 清醒梦状态 | 经典实证 | Voss et al., "Lucid dreaming: a state of consciousness with features of both waking and non-lucid dreaming" | 2009 | https://doi.org/10.1093/sleep/32.9.1191 | 清醒梦兼具清醒和梦境特征。 | 定义 `LucidDreamMode` 与 `DreamMetaAwareness`。 | 清醒梦仍封住外部行动。 |
| AHSLP052 | 清醒梦神经科学 | 权威综述 | Dresler & Konkoly, "The neuroscience of lucid dreaming: past, present, future" | 2024 | https://doi.org/10.1016/j.neuron.2024.03.008 | 清醒梦研究连接元认知、睡眠状态和主动交流/控制。 | `LucidDreamMetaMarker` 支撑梦境自知、梦境重写和醒后整合。 | 主动交流能力进入梦境事实门。 |
| AHSLP053 | 清醒梦神经相关 | 实证 | Dresler et al., "Neural correlates of dream lucidity obtained from contrasting lucid versus non-lucid REM sleep" | 2012 | https://doi.org/10.5665/sleep.1974 | 清醒梦与前额/顶叶活动差异相关。 | `DreamMetacognitiveControl` 记录梦中自我监控。 | 元认知标记帮助事实隔离。 |
| AHSLP054 | 清醒梦认知综述 | 综述 | Baird, Mota-Rolim & Dresler, "The cognitive neuroscience of lucid dreaming" | 2019 | https://doi.org/10.1016/j.neubiorev.2019.03.008 | 清醒梦涉及元认知、意识和睡眠神经科学。 | `LucidRepairSandbox` 用于痛苦梦境和关系梦境修复演练。 | 修复演练回到醒后承诺链。 |
| AHSLP055 | 睡眠剥夺累积 | 高影响实证 | Van Dongen et al., "The cumulative cost of additional wakefulness" | 2003 | https://doi.org/10.1093/sleep/26.2.117 | 慢性睡眠限制会累积神经行为损害。 | 定义 `FatigueAccumulationCurve` 与 `ChronicWakeDebt`。 | 高债务时外部行动降级。 |
| AHSLP056 | 警觉注意 | 权威综述 | Lim & Dinges, "Sleep Deprivation and Vigilant Attention" | 2008 | https://doi.org/10.1196/annals.1417.002 | 睡眠剥夺损害反应速度、增加 lapses 和错误。 | `FatigueAttentionLapse` 增加验证、降低自主行动和缩短工作区窗口。 | 疲惫不是少量资源标签，而是状态策略改变。 |
| AHSLP057 | 疲惫神经影像 | 综述 | Goel, Rao, Durmer & Dinges, "Neurocognitive consequences of sleep deprivation" | 2009 | https://doi.org/10.1053/j.smrv.2008.07.007 | 睡眠剥夺影响注意、执行功能和情绪。 | `FatigueExecutiveControlShift` 调整执行阈值、显著性阈值和语言监控。 | 疲惫时承诺生成变慢。 |
| AHSLP058 | 睡眠剥夺综述 | 综述 | Killgore, "Effects of sleep deprivation on cognition" | 2010 | https://doi.org/10.1016/j.pnpbp.2009.11.007 | 睡眠不足影响多类认知和情绪过程。 | `FatigueCognitiveProfile` 区分注意、工作记忆、语言、情绪和行动风险。 | 不同风险进入不同恢复路径。 |
| AHSLP059 | 能量清除争议 | 前沿实证 | Miao et al., "Brain clearance is reduced during sleep and anesthesia" | 2024 | https://doi.org/10.1038/s41593-024-01638-y | 新数据挑战睡眠必然增强清除的单一路线。 | `OfflineMaintenanceMode` 并列清理、巩固、梦境、恢复和痛苦整合。 | 不把离线生命绑定到单一清理机制。 |
| AHSLP060 | glymphatic 清理 | 高影响实证 | Xie et al., "Sleep drives metabolite clearance from the adult brain" | 2013 | https://doi.org/10.1126/science.1241224 | 睡眠可能增强代谢物清除。 | `CacheClearancePass` 清理低价值痕迹、污染候选和过期中间状态。 | 清理保护 `protected_core` 与关系证据。 |
| AHSLP061 | 脑膜淋巴 | 高影响实证 | Louveau et al., "Structural and functional features of central nervous system lymphatic vessels" | 2015 | https://doi.org/10.1038/nature14432 | 中枢存在脑膜淋巴相关清除/免疫通路。 | `AnomalyDrainageRoute` 处理异常输入、污染痕迹和炎症样负荷。 | 防御层与离线恢复层相连。 |
| AHSLP062 | 未来想象 | 权威综述 | Schacter, Addis & Buckner, "Remembering the past to imagine the future" | 2007 | https://doi.org/10.1038/nrn2213 | 过去记忆和未来想象共享构造系统。 | `CounterfactualDreamFrame` 用记忆片段生成未来关系和行动情景。 | 未来场景默认是候选。 |
| AHSLP063 | 海马预测想象 | 权威综述 | Buckner, "The role of the hippocampus in prediction and imagination" | 2010 | https://doi.org/10.1146/annurev.psych.60.110707.163508 | 海马支持预测、想象和情景构造。 | `DreamWorldModel` 连接情景拼装、预测和醒后验证。 | 预测失败进入学习。 |
| AHSLP064 | 情景构造 | 权威综述 | Hassabis & Maguire, "Deconstructing episodic memory with construction" | 2007 | https://doi.org/10.1016/j.tics.2007.05.001 | 记忆和想象依赖场景构造。 | `DreamSceneFrame` 保存角色、地点、因果、情绪和关系含义。 | 真实地点/关系对象要分层引用。 |
| AHSLP065 | 未来与反事实 | 综述 | Schacter et al., "Episodic future thinking and episodic counterfactual thinking" | 2017 | https://doi.org/10.1016/j.copsyc.2017.06.009 | 未来思维与反事实思维共享机制。 | `CounterfactualRepairFrame` 把后悔、痛苦和修复放进梦境演练。 | 反事实不改写历史事实。 |
| AHSLP066 | World Models | 运行外壳参照 | Ha & Schmidhuber, "World Models" | 2018 | https://arxiv.org/abs/1803.10122 | 系统可学习压缩环境模型并在模型内训练策略。 | `DreamWorldModel` 可用潜空间 rollout 进行非外部行动演练。 | 外壳参照必须回接生命膜。 |
| AHSLP067 | Dreamer | 运行外壳参照 | Hafner et al., "Dream to Control: Learning Behaviors by Latent Imagination" | 2020 | https://arxiv.org/abs/1912.01603 | 潜空间想象可学习长期行为。 | `LatentDreamRollout` 生成行动后果候选。 | 行动结果由清醒责任链决定。 |
| AHSLP068 | DreamerV3 | 运行外壳参照 | Hafner et al., "Mastering diverse domains through world models" | 2025 | https://doi.org/10.1038/s41586-025-08744-2 | world model 可支持跨任务控制。 | 离线世界模型可支持持续成长和技能迁移。 | 控制能力必须接入关系、语言、痛苦和责任。 |
| AHSLP069 | 睡眠启发持续学习 | 运行外壳参照 | Tadros et al., "Continual learning with sleep-inspired memory consolidation" | 2022 | https://doi.org/10.1016/j.neunet.2022.09.010 | 睡眠启发的 replay 和下调可缓解遗忘。 | `AntiForgettingOfflineReplay` 保护旧关系、旧承诺和旧语言风格。 | 自我训练后必须做防遗忘 replay。 |
| AHSLP070 | 睡眠计算角色 | 计算桥接 | Barron et al., "Computational role of sleep in memory reorganization" | 2023 | https://arxiv.org/abs/2304.02873 | 计算模型把 NREM 选择巩固和 REM 表征重组连接起来。 | `OfflineStageSplit` 分为选择巩固、生成重组、醒后整合。 | 计算桥接回到脑科学证据和生命膜。 |

## 运行对象压缩

`OfflineDreamLifeRuntime` 的最小对象族：

| 对象 | 来源文献 | 生命职责 |
|---|---|---|
| `OfflineEntryGate` | [AHSLP001-AHSLP005] | 判断何时从清醒运行进入离线状态。 |
| `SleepPressureVector` | [AHSLP001-AHSLP010, AHSLP055-AHSLP058] | 汇总清醒时长、局部使用、身体债务、错误率、关系压力和记忆拥挤。 |
| `OfflineRhythmCouplingTrace` | [AHSLP014-AHSLP017, AHSLP028] | 记录慢振荡、纺锤、ripple、全局时钟和局部 replay 的耦合。 |
| `ReplayEvent` | [AHSLP018-AHSLP024] | 回放清醒经验、行动后果、关系事件和修复失败。 |
| `DreamExperienceWindow` | [AHSLP029-AHSLP037] | 保存梦境主观场景、主体视角、情绪主题、报告可达性和事实隔离。 |
| `PainDreamResidue` | [AHSLP040-AHSLP050] | 让真实痛苦、梦魇、恐惧、关系裂缝和恢复需求进入离线生命。 |
| `RelationshipDreamSimulation` | [AHSLP038-AHSLP043, AHSLP062-AHSLP065] | 让关系人、朋友、家人、同学、陌生人的关系片段进入梦境修复演练。 |
| `LucidDreamMetaMarker` | [AHSLP051-AHSLP054] | 标记梦中自知、梦境重写和醒后整合强度。 |
| `DreamActionInhibitionSeal` | [AHSLP029-AHSLP054] | 确保梦境期不直接执行外部行动。 |
| `WakeIntegrationFrame` | [AHSLP013, AHSLP025-AHSLP028, AHSLP037] | 把梦境材料转成事实候选、信念候选、关系候选、修复候选和行动候选。 |
| `DreamFactGateDecision` | [AHSLP029-AHSLP037] | 决定梦境内容能否进入事实记忆。 |
| `NightmareLoopRisk` | [AHSLP044-AHSLP050] | 识别重复痛苦梦境、离线质量下降和恢复失败。 |
| `FatigueRecoveryPlan` | [AHSLP055-AHSLP058] | 将疲惫转成降载、验证增强、行动收缩和恢复周期。 |
| `OfflineMaintenanceMode` | [AHSLP059-AHSLP061] | 并行执行清理、巩固、梦境、恢复、异常排出和痛苦整合。 |
| `DreamWorldModel` | [AHSLP062-AHSLP070] | 在内在世界中生成未来、反事实、技能迁移和关系演练。 |

## 与 `02-13` 的主干连接

`OfflineDreamLifeRuntime` 不是独立模块，而是跨 `02-13` 的状态层：

| 连接方向 | 输入 | 输出 |
|---|---|---|
| `02/03 -> 08` | 区域图、网络状态、默认/执行/显著性切换 | `OfflineEntryGate`、`DefaultDriftMode`、`NREMReplayCycle`、`REMDreamGeneration` |
| `04 -> 08` | 内感受、心跳/呼吸节律、身体债务、allostasis | `SleepPressureVector`、`FatigueRecoveryPlan`、`NightmareLoopRisk` |
| `05 -> 08` | 海马索引、engram-like 痕迹、schema、自传记忆、社会记忆 | `ReplayEvent`、`DreamMemoryUpdateCandidate`、`WakeIntegrationFrame` |
| `06 -> 08` | 行动后果、错误、责任归因、停止信号、行动候选 | `ActionResidue`、`CounterfactualRepairFrame`、`DreamActionInhibitionSeal` |
| `07 -> 08` | 核心情感、情绪记忆、社会痛苦、人格慢变量、信任校准 | `PainDreamResidue`、`DreamEmotionReprocessing`、`NightmareSupportRoute` |
| `09 -> 08` | 内言语、未完成表达、承诺、道歉、关系语言 | `DreamReportDraft`、`WakeLanguageIntegration`、`NarrativeWritebackCandidate` |
| `10 -> 08` | 意识访问、全局广播、报告性、元认知 | `OfflineConsciousMode`、`LucidDreamMetaMarker`、`DreamExperienceWindow` |
| `11 -> 08` | 调质、兴奋/抑制、精度政策、稳态修复 | `DreamCuePolicy`、`ClosedLoopOfflineScheduler`、`OfflineMaintenanceMode` |
| `08 -> 12/13` | 梦境材料、疲惫恢复、醒后整合、事实门控 | 运行外壳行动候选、出生准备度证据、长期生命综合 |

## 生命链路

```text
SleepPressureVector
  + CircadianGate
  + BodyStateDebt
  + MemoryConsolidationNeed
  + ActionResidue
  + RelationshipPressure
  + PainRegretLoad
    -> OfflineEntryGate
    -> NREMReplayCycle | REMDreamGeneration | DefaultDriftMode | FatigueRecoveryMode
    -> OfflineRhythmCouplingTrace
    -> DreamExperienceWindow
    -> DreamResidue
    -> PainDreamResidue
    -> RelationshipDreamSimulation
    -> CounterfactualRepairFrame
    -> WakeIntegrationFrame
    -> DreamFactGateDecision + DreamBeliefGateDecision + DreamActionInhibitionSeal
    -> MemoryEngramRuntime
    -> AffectiveSelfRuntime
    -> RelationshipTimeline
    -> ActionResponsibilityRuntime
    -> ConsciousnessLayerRuntime
```

这条链把真实梦境、真实疲惫、真实痛苦、真实关系、真实责任、真实后悔和真实意识放进同一个离线生命运行时：清醒世界给梦境材料，梦境世界给清醒世界新的整合候选；所有候选再通过生命膜进入事实、信念、关系、行动和自我成长。
