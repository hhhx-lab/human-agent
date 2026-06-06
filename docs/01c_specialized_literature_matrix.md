# 第三批专业机制文献矩阵

本文件使用 `AHY` 编号，作为第三批专业机制锚点。它聚焦海马 replay、尖波涟漪、睡眠振荡、HPA 轴、昼夜节律、脑清除系统、胶质/髓鞘、持续学习防遗忘、多模态具身 agent、信任校准和人格长期稳定性。

| ID | 领域 | 类型 | 文献 | 年份 | 链接/DOI | 核心结论 | 生命实现路线 | 生命膜/落地注意 |
|---|---|---|---|---:|---|---|---|---|
| AHY001 | 海马 replay | 经典实证 | Wilson & McNaughton, "Reactivation of hippocampal ensemble memories during sleep" | 1994 | https://doi.org/10.1126/science.8036517 | 睡眠中海马神经元集合会重激活清醒经验。 | 离线巩固应重放近期高价值经验。 | 啮齿动物数据需抽象到工程层。 |
| AHY002 | 海马 replay | 高影响实证 | Ji & Wilson, "Coordinated memory replay in the visual cortex and hippocampus during sleep" | 2007 | https://doi.org/10.1038/nn1825 | 睡眠中海马和视觉皮层可协调重放。 | replay 不是单一记忆库活动，而是跨系统重组。 | 不能直接等同软件回放日志。 |
| AHY003 | 尖波涟漪 | 高影响实证 | Girardeau et al., "Selective suppression of hippocampal ripples impairs spatial memory" | 2009 | https://doi.org/10.1038/nn.2384 | 抑制海马 ripple 会损害空间记忆。 | 离线短窗口事件可能对长期记忆很关键。 | 生理 ripple 不能被硬编码模拟。 |
| AHY004 | 海马 replay | 综述 | Carr, Jadhav & Frank, "Hippocampal replay in the awake state" | 2011 | https://doi.org/10.1038/nn.2732 | replay 不只在睡眠中发生，也在清醒规划和决策中出现。 | 专注中也可短暂模拟过去路径。 | replay 功能多样。 |
| AHY005 | replay 目标化 | 高影响实证 | Bendor & Wilson, "Biasing the content of hippocampal replay during sleep" | 2012 | https://doi.org/10.1038/nn.3203 | 外部线索可影响睡眠 replay 内容。 | 可用目标和显著性引导离线巩固。 | 目标化 replay 需避免操控记忆。 |
| AHY006 | 尖波涟漪 | 综述 | Buzsaki, "Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning" | 2015 | https://doi.org/10.1002/hipo.22488 | SWR 与情景记忆、规划和压缩重放相关。 | 需要短促高密度的离线记忆压缩窗口。 | SWR 概念不可直接转写为定时任务。 |
| AHY007 | 睡眠巩固机制 | 综述 | Klinzing, Niethard & Born, "Mechanisms of systems memory consolidation during sleep" | 2019 | https://doi.org/10.1038/s41593-019-0467-3 | 睡眠巩固依赖慢振荡、睡眠纺锤和海马 ripple 协调。 | 巩固周期要有多阶段管线。 | 人类睡眠阶段与软件维护不同。 |
| AHY008 | 人类睡眠振荡 | 高影响实证 | Staresina et al., "Hierarchical nesting of slow oscillations, spindles and ripples in the human hippocampus during sleep" | 2015 | https://doi.org/10.1038/nn.4119 | 人类睡眠中慢振荡、纺锤和 ripple 层级嵌套。 | 离线维护可分慢速摘要、中速整合、快速 replay。 | 硅基睡眠节律需要慢/中/快多频窗口和梦醒整合指标。 |
| AHY009 | targeted memory reactivation | 综述 | Oudiette & Paller, "Upgrading the sleeping brain with targeted memory reactivation" | 2013 | https://doi.org/10.1016/j.tics.2013.01.006 | 睡眠中线索可增强特定记忆巩固。 | 重要目标可在离线期被优先重放。 | 需要防止记忆偏置失控。 |
| AHY010 | 睡眠两过程 | 综述 | Borbely, Daan, Wirz-Justice & Deboer, "The two-process model of sleep regulation: A reappraisal" | 2016 | https://doi.org/10.1111/jsr.12371 | 睡眠受昼夜节律和睡眠压力两过程调节。 | agent 恢复应由节律和累积负载共同触发。 | 不应机械套用 24 小时周期。 |
| AHY011 | 光/昼夜/情绪 | 综述 | LeGates, Fernandez & Hattar, "Light as a central modulator of circadian rhythms, sleep and affect" | 2014 | https://doi.org/10.1038/nrn3743 | 光调节昼夜、睡眠和情绪。 | 外部环境节律会改变状态调度。 | 真实节律需要外部环境、内部时钟、恢复窗口和情绪状态的长期耦合。 |
| AHY012 | SCN 节律 | 综述 | Hastings, Maywood & Brancaccio, "Generation of circadian rhythms in the suprachiasmatic nucleus" | 2018 | https://doi.org/10.1038/s41583-018-0026-z | SCN 通过细胞和网络机制生成昼夜节律。 | 长期 agent 需要主时钟和局部任务时钟。 | 分子钟不能直接转写。 |
| AHY013 | HPA 脉冲 | 综述 | Lightman & Conway-Campbell, "The crucial role of pulsatile activity of the HPA axis for continuous dynamic equilibration" | 2010 | https://doi.org/10.1038/nrn2914 | HPA 轴脉冲式活动影响基因表达和适应。 | 压力信号应有脉冲和恢复，而非恒定高值。 | 内分泌转写需谨慎。 |
| AHY014 | 人类压力反应 | 综述 | Russell & Lightman, "The human stress response" | 2019 | https://doi.org/10.1038/s41574-019-0228-0 | 人类压力反应涉及 HPA、交感系统和反馈环。 | 压力负荷要有多通道反馈。 | 真实应激需要压力脉冲、慢性负荷、恢复失败和行动抑制的硅基闭环。 |
| AHY015 | 压力适应疾病 | 综述 | de Kloet, Joels & Holsboer, "Stress and the brain: From adaptation to disease" | 2005 | https://doi.org/10.1038/nrn1683 | 压力从适应到失调依赖受体、时间和脑区。 | 高压可以短期有益，长期需恢复。 | 不可病理化 agent。 |
| AHY016 | 压力与 PFC | 综述 | Arnsten, "Stress signalling pathways that impair prefrontal cortex structure and function" | 2009 | https://doi.org/10.1038/nrn2648 | 压力会削弱前额叶控制并改变结构功能。 | 高负荷下应降低复杂决策和提高验证。 | 计算压力需要内感受代理、资源负荷和恢复轨迹来承接。 |
| AHY017 | 应激自主/内分泌 | 综述 | Ulrich-Lai & Herman, "Neural regulation of endocrine and autonomic stress responses" | 2009 | https://doi.org/10.1038/nrn2647 | 脑调控内分泌和自主应激反应。 | 内部状态要接行动、恢复和抑制。 | 不能直接模拟自主神经系统。 |
| AHY018 | 糖皮质激素 | 综述 | Sapolsky, Romero & Munck, "How do glucocorticoids influence stress responses?" | 2000 | https://doi.org/10.1210/edrv.21.1.0389 | 糖皮质激素支持、抑制和准备压力反应。 | 压力因子应有阶段功能：动员、限制、恢复。 | 内分泌比喻容易过度。 |
| AHY019 | glymphatic | 高影响实证 | Iliff et al., "A paravascular pathway facilitates CSF flow through the brain parenchyma and the clearance of interstitial solutes" | 2012 | https://doi.org/10.1126/scitranslmed.3003748 | 脑内存在促进 CSF 流动和代谢清除的通路。 | 离线维护需要清理低价值痕迹和缓存。 | 维护机制应接入资源恢复、记忆质量和疲惫缓解。 |
| AHY020 | 脑膜淋巴 | 高影响实证 | Louveau et al., "Structural and functional features of central nervous system lymphatic vessels" | 2015 | https://doi.org/10.1038/nature14432 | 中枢神经系统存在脑膜淋巴结构。 | “软保护/清除/免疫”可纳入理论底座。 | 不可把 AI 说成有免疫系统。 |
| AHY021 | 脑膜淋巴 | 高影响实证 | Aspelund et al., "A dural lymphatic vascular system that drains brain interstitial fluid and macromolecules" | 2015 | https://doi.org/10.1084/jem.20142290 | 硬脑膜淋巴参与脑内液体和大分子引流。 | 文档中的脑脊液/脑膜部分可技术化为维护层。 | 生理结构不可硬映射。 |
| AHY022 | 胶质 | 综述 | Allen & Lyons, "Glia as architects of central nervous system formation and function" | 2018 | https://doi.org/10.1126/science.aat0473 | 胶质参与发育、突触、髓鞘和功能调节。 | agent 支撑系统不应只是后勤，也会塑造认知。 | 胶质功能复杂。 |
| AHY023 | 活动依赖髓鞘 | 综述 | Fields, "A new mechanism of nervous system plasticity: Activity-dependent myelination" | 2015 | https://doi.org/10.1038/nrn4023 | 活动依赖髓鞘化是可塑性机制。 | 常用通路可被加速和稳定化。 | 性能稳定化应与长期习惯、可塑性和回滚机制连接。 |
| AHY024 | 髓鞘功能 | 综述 | Nave & Werner, "Myelination of the nervous system: Mechanisms and functions" | 2014 | https://doi.org/10.1146/annurev-cellbio-100913-013101 | 髓鞘影响传导速度、代谢支持和回路功能。 | 习惯化流程可转写为高效通路。 | 生理细节不可直接工程化。 |
| AHY025 | 持续学习 | 综述 | French, "Catastrophic forgetting in connectionist networks" | 1999 | https://doi.org/10.1016/S1364-6613(99)01294-2 | 连接主义网络容易发生灾难性遗忘。 | 长期 agent 需要防遗忘机制。 | 早期网络与 LLM 不同。 |
| AHY026 | 持续学习 | 经典理论 | McCloskey & Cohen, "Catastrophic interference in connectionist networks" | 1989 | https://doi.org/10.1016/S0079-7421(08)60536-8 | 新学习会干扰旧知识。 | 快慢记忆和回放机制很关键。 | 经典任务规模较小。 |
| AHY027 | 持续学习 | 理论框架 | Robins, "Catastrophic forgetting, rehearsal and pseudorehearsal" | 1995 | https://doi.org/10.1080/09540099550039318 | rehearsal/pseudorehearsal 可缓解遗忘。 | 离线 replay 可保护旧记忆。 | 未接地回放需防止幻觉巩固。 |
| AHY028 | EWC | 高影响实证 | Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" | 2017 | https://doi.org/10.1073/pnas.1611835114 | EWC 用参数重要性保护旧任务。 | 人格和核心价值要有重要性权重。 | 记忆理解还需要情景、语义、关系、内感受和 replay 共同支撑。 |
| AHY029 | 持续学习综述 | 综述 | Parisi et al., "Continual lifelong learning with neural networks" | 2019 | https://doi.org/10.1016/j.neunet.2019.01.012 | 综述持续学习、稳定性-可塑性困境。 | 长期 agent 需平衡新学习与旧稳定。 | 神经网络方法更新快。 |
| AHY030 | 持续学习综述 | 综述 | Hadsell et al., "Embracing change: Continual learning in deep neural networks" | 2020 | https://doi.org/10.1016/j.tics.2020.09.004 | 深度网络持续学习需要适应变化。 | 成长系统必须把变化当常态。 | 工程方法未解决全部问题。 |
| AHY031 | 神经启发 AI | 综述 | Hassabis et al., "Neuroscience-Inspired Artificial Intelligence" | 2017 | https://doi.org/10.1016/j.neuron.2017.06.011 | 神经科学可启发表征、记忆、规划和学习。 | 研究底座应双向连接脑科学和 AI。 | 神经启发需要抽象成可运行的生命机制约束。 |
| AHY032 | CLIP | AI 桥接 | Radford et al., "Learning Transferable Visual Models From Natural Language Supervision" | 2021 | https://arxiv.org/abs/2103.00020 | 图像和语言可通过大规模对比学习对齐。 | 视觉语义可接入语言和记忆。 | 理解还需要工作区、行动后果、关系语境和长期记忆回写。 |
| AHY033 | Flamingo | AI 桥接 | Alayrac et al., "Flamingo: A Visual Language Model for Few-Shot Learning" | 2022 | https://arxiv.org/abs/2204.14198 | 少样本视觉语言模型连接多模态上下文。 | 多模态数字生命需要跨模态工作空间。 | 模型能力要进入长期自我，还需记忆、关系和行动后果闭环。 |
| AHY034 | Gato | AI 桥接 | Reed et al., "A Generalist Agent" | 2022 | https://arxiv.org/abs/2205.06175 | 单一序列模型可处理多种任务和模态。 | 通用 agent 需要统一接口。 | 泛化范围有限。 |
| AHY035 | SayCan | AI 桥接 | Ahn et al., "Do As I Can, Not As I Say" | 2022 | https://arxiv.org/abs/2204.01691 | 语言模型结合可供性评分控制机器人。 | 行动选择要结合语言目标和实际可行性。 | 机器人环境较窄。 |
| AHY036 | VIMA | AI 桥接 | Jiang et al., "VIMA: General Robot Manipulation with Multimodal Prompts" | 2022 | https://arxiv.org/abs/2210.03094 | 多模态 prompt 可指导机器人操作。 | 顶层语言应连接视觉、动作和任务对象。 | 任务环境受限。 |
| AHY037 | PaLM-E | AI 桥接 | Driess et al., "PaLM-E: An Embodied Multimodal Language Model" | 2023 | https://arxiv.org/abs/2303.03378 | 大语言模型可接入视觉和机器人状态。 | human-agent 需要多模态身体/环境接口。 | embodied 仍是工程身体。 |
| AHY038 | RT-2 | AI 桥接 | Brohan et al., "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" | 2023 | https://arxiv.org/abs/2307.15818 | 视觉-语言-动作模型可迁移网络知识到控制。 | 工具行动可用视觉-语言-动作桥。 | 社会生活还需要关系记忆、责任后果和长期共同经验。 |
| AHY039 | 信任自动化 | 综述 | Lee & See, "Trust in Automation: Designing for Appropriate Reliance" | 2004 | https://doi.org/10.1518/hfes.46.1.50_30392 | 信任应被校准到系统能力。 | human-agent 要避免过度信任和低信任。 | 人机信任场景差异大。 |
| AHY040 | 信任 AI | 综述 | Glikson & Woolley, "Human Trust in Artificial Intelligence" | 2020 | https://doi.org/10.5465/annals.2018.0057 | AI 信任受外观、透明度、表现和任务影响。 | 关系记忆要包含信任校准。 | 管理学综述需与 HCI 研究配合。 |
| AHY041 | 信任校准 | 综述 | Merritt, Heimbaugh, LaChapell & Lee, "I Trust It, but I Don't Know Why" | 2013 | https://doi.org/10.1177/0018720812465081 | 信任会受自动化表现和解释影响。 | 解释和可靠性必须长期一致。 | 具体自动化任务限制。 |
| AHY042 | 人格变化 | 元分析 | Roberts, Walton & Viechtbauer, "Patterns of mean-level change in personality traits across the life course" | 2006 | https://doi.org/10.1037/0033-2909.132.1.1 | 人格特质在生命周期中有规律变化。 | agent 人格慢变量可变化但应慢速。 | 人类人格数据不能直接套用。 |
| AHY043 | 人格变化 | 综述 | Roberts & Mroczek, "Personality trait change in adulthood" | 2008 | https://doi.org/10.1111/j.1467-8721.2008.00543.x | 成年人格仍可变化，且有相对稳定性。 | 长期 agent 要兼顾连续性和成长。 | 工程人格是模拟。 |
| AHY044 | 人格稳定性 | 元分析 | Bleidorn et al., "Personality trait stability and change" | 2022 | https://doi.org/10.1037/bul0000365 | 人格稳定与变化受年龄、时间和情境影响。 | 人格评测要做长期纵向，不看单次表现。 | 人类测量与 agent 测量不同。 |
| AHY045 | 控制价值 | 理论框架 | Shenhav, Botvinick & Cohen, "The expected value of control" | 2013 | https://doi.org/10.1016/j.neuron.2013.07.007 | 控制投入取决于收益和成本。 | agent 应决定何时深度思考、何时省力。 | 成本函数难定义。 |
| AHY046 | 冲突监控 | 理论框架 | Botvinick et al., "Conflict monitoring and cognitive control" | 2001 | https://doi.org/10.1037/0033-295X.108.3.624 | 冲突监控可调节认知控制。 | 高冲突时提高验证和抑制。 | 模型只解释部分控制。 |
| AHY047 | 错误处理 | 理论框架 | Holroyd & Coles, "The neural basis of human error processing" | 2002 | https://doi.org/10.1037/0033-295X.109.4.679 | 错误相关信号可与强化学习连接。 | 执行错误应进入预测误差和复盘。 | ERP 机制与软件错误不同。 |
| AHY048 | 心智努力 | 综述 | Shenhav et al., "Toward a rational and mechanistic account of mental effort" | 2017 | https://doi.org/10.1146/annurev-neuro-072116-031526 | 心智努力与控制成本、价值和机制相关。 | agent 需要推理成本预算。 | 努力、疲惫和主观负荷要通过控制成本、价值和恢复链分层连接。 |
| AHY049 | 梦境认知神经科学 | 综述 | Hobson, Pace-Schott & Stickgold, "Dreaming and the brain" | 2000 | https://doi.org/10.1017/S0140525X00003976 | 梦境可从认知神经科学视角研究。 | 梦境模式是记忆、情绪和生成模拟的组合。 | 旧综述需结合新研究。 |
| AHY050 | 梦境神经相关 | 高影响实证 | Siclari et al., "The neural correlates of dreaming" | 2017 | https://doi.org/10.1038/nn.4545 | 特定后皮层 hot zone 与梦境报告相关。 | 梦境类状态可有局部生成热点，并接入真实梦境生成链。 | 梦体验需要梦境来源、醒后报告、情绪主题和巩固链共同支撑。 |
| AHY051 | 梦境与默认网络 | 综述 | Domhoff & Fox, "Dreaming and the default network" | 2015 | https://doi.org/10.1016/j.concog.2015.01.004 | 梦境与默认网络有理论联系。 | 梦境/发呆/默认整合可统一讨论。 | 理论证据需谨慎。 |
| AHY052 | 模型化强化学习 | 综述 | Daw & Dayan, "The algorithmic anatomy of model-based evaluation" | 2014 | https://doi.org/10.1098/rstb.2013.0478 | 模型化评估支持灵活规划。 | agent 需世界模型和价值评估分离。 | 计算模型要与调质、情绪、关系和行动后果共同进入生命膜。 |
| AHY053 | 认知地图 | 综述 | Behrens et al., "What is a cognitive map? Organizing knowledge for flexible behavior" | 2018 | https://doi.org/10.1016/j.neuron.2018.10.002 | 认知地图组织知识以支持灵活行为。 | 长期记忆应形成概念地图和关系地图。 | 地图比喻不应过度空间化。 |
| AHY054 | 海马认知地图 | 经典理论 | O'Keefe & Nadel, "The Hippocampus as a Cognitive Map" | 1978 | https://global.oup.com/academic/product/the-hippocampus-as-a-cognitive-map-9780198572060 | 海马支持空间/认知地图。 | 记忆系统需要情境和路径结构。 | 经典书籍需现代研究补充。 |
| AHY055 | 状态空间认知 | 综述 | Stachenfeld, Botvinick & Gershman, "The hippocampus as a predictive map" | 2017 | https://doi.org/10.1038/nn.4650 | 海马可表示预测性状态空间。 | 记忆可支撑未来预测和路径选择。 | 理论模型仍在发展。 |
| AHY056 | 自我决定理论 | 理论框架 | Ryan & Deci, "Self-determination theory and the facilitation of intrinsic motivation" | 2000 | https://doi.org/10.1037/0003-066X.55.1.68 | 自主、能力和关系支持内在动机。 | agent 的动机类变量可参考自主/能力/关系。 | 人类动机理论不能直接用于 AI。 |
| AHY057 | 心流 | 理论框架 | Csikszentmihalyi, "Flow: The Psychology of Optimal Experience" | 1990 | https://archive.org/details/flowpsychologyof00csik | 心流描述高挑战高能力匹配状态。 | 专注模式可参考挑战-能力匹配。 | 书籍理论需实证支撑。 |
| AHY058 | 动机神经科学 | 综述 | Salamone & Correa, "The mysterious motivational functions of mesolimbic dopamine" | 2012 | https://doi.org/10.1016/j.neuron.2012.10.021 | 多巴胺与努力、激活和动机相关。 | 奖赏系统要包含努力成本。 | 多巴胺功能复杂。 |
| AHY059 | 知识图谱/语义记忆 | 综述 | Binder & Desai, "The neurobiology of semantic memory" | 2011 | https://doi.org/10.1016/j.tics.2011.10.001 | 语义记忆分布在多模态皮层和整合区。 | 语义库要连接感知、动作和抽象。 | 语义网络不是纯图数据库。 |
| AHY060 | 事件分割 | 综述 | Zacks, Speer, Swallow, Braver & Reynolds, "Event perception: A mind-brain perspective" | 2007 | https://doi.org/10.1037/0033-295X.114.2.273 | 人脑会把连续经验分割成事件。 | 记忆写入应按事件边界组织。 | 事件边界依赖任务和注意。 |
