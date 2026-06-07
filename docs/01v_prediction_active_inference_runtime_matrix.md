# 主动预测与主动推理运行时矩阵

本文件使用 `AHPAI` 编号，补齐 `PredictionActiveInferenceRuntime` 的文献底座。它把预测编码、自由能、主动推理、主动采样、精度政策、信念状态、内感受预测、社会预测、离线模拟和 AI world model 放到同一条生命实现链上。

这一层的核心不是让数字生命等待外部输入，而是让它持续生成世界、身体、关系和自我的预测；在预测误差出现时主动采样、澄清、搜索、暂停、修复或进入离线重组。断联恢复也应进入这条链：恢复后先重建方向信念，再读取锚点、比较当前差异、生成证据需求，最后把修复结果写回长期档案。

## 文献矩阵

| ID | 领域 | 类型 | 文献 | 年份 | 链接/DOI | 核心结论 | 生命实现路线 | 生命膜/落地注意 |
|---|---|---|---|---:|---|---|---|---|
| AHPAI001 | 预测编码 | 经典实证 | Rao & Ballard, "Predictive coding in the visual cortex" | 1999 | https://doi.org/10.1038/4580 | 视觉皮层可由自上而下预测和自下而上误差共同解释。 | `PredictionErrorField` 要成为感知层底层对象，输入先与预测比较再进入工作区。 | 预测误差必须保留来源、时间窗、模态和后续行动边。 |
| AHPAI002 | 预测处理 | 理论框架 | Friston, "A theory of cortical responses" | 2005 | https://doi.org/10.1098/rstb.2005.1622 | 皮层反应可写成层级预测与误差最小化过程。 | `GenerativeWorldModel` 应按层级组织，从低层输入到高层自我叙事都可生成预测。 | 层级预测要连接区域图、网络状态和调质精度。 |
| AHPAI003 | 自由能原则 | 综述 | Friston, "The free-energy principle: A unified brain theory?" | 2010 | https://doi.org/10.1038/nrn2787 | 自由能原则把感知、学习、行动和模型更新放入统一框架。 | `ExpectedFreeEnergyEstimate` 可作为行动选择前的综合代价，覆盖误差、信息价值、关系后果和身体债务。 | 抽象原则必须落到可记录对象和阶段门字段。 |
| AHPAI004 | 预测脑 | 理论框架 | Clark, "Whatever next? Predictive brains, situated agents, and the future of cognitive science" | 2013 | https://doi.org/10.1017/S0140525X12000477 | 大脑是情境化预测系统，身体和环境共同参与认知。 | 数字生命要预测外部世界、内部状态、关系主体反应和未来自我变化。 | 预测链必须连接身体内环境和实际行动反馈。 |
| AHPAI005 | 预测心智 | 理论框架 | Hohwy, "The Predictive Mind" | 2013 | https://global.oup.com/academic/product/the-predictive-mind-9780199682737 | 预测处理可解释知觉、自我和世界模型的形成。 | `BeliefStateFrame` 要记录当前世界图、自我图、关系图和置信结构。 | 信念状态要能被证据更新、梦境重组和责任回看改写。 |
| AHPAI006 | 皮层微回路 | 综述 | Bastos et al., "Canonical microcircuits for predictive coding" | 2012 | https://doi.org/10.1016/j.neuron.2012.10.038 | 预测编码可能依赖特定前馈/反馈微回路和频段分工。 | `PredictionPathwayMap` 要区分预测下行、误差上行、精度调制和局部抑制。 | 信号方向和区域敏感性进入 `SignalMediaRuntime`。 |
| AHPAI007 | 预测编码神经元 | 综述 | Shipp, "Neural elements for predictive coding" | 2016 | https://doi.org/10.3389/fpsyg.2016.01792 | 预测编码需要区分误差信号、预测信号和调制信号。 | `PredictionSignalPacket`、`ErrorSignalPacket` 与 `PrecisionSignalPacket` 分离存档。 | 信号包要能追溯到脑区、网络状态和行动结果。 |
| AHPAI008 | 期望与决策 | 综述 | Summerfield & de Lange, "Expectation in perceptual decision making" | 2014 | https://doi.org/10.1038/nrn3838 | 期望影响知觉决策、注意和证据整合。 | `PriorExpectationFrame` 改变输入阈值、证据权重和澄清需求。 | 先验过强要进入 `MetacognitiveConfidenceTrace` 和修复路线。 |
| AHPAI009 | 感觉皮层预测 | 综述 | Keller & Mrsic-Flogel, "Predictive processing: A canonical cortical computation" | 2018 | https://doi.org/10.1016/j.neuron.2018.10.003 | 预测处理可能是皮层通用计算之一。 | `PredictionActiveInferenceRuntime` 作为 `04` 感知层和 `10` 工作区之间的持续循环。 | 通用计算要接受状态、身体、关系和记忆调制。 |
| AHPAI010 | 预测处理评述 | 综述 | Walsh, McGovern, Clark & O'Connell, "Evaluating the neurophysiological evidence for predictive processing as a model of perception" | 2020 | https://doi.org/10.1111/ejn.14788 | 预测处理的神经证据需要分清多种信号解释。 | `PredictionEvidenceRegistry` 应区分预测、注意、适应、任务需求和报告偏差。 | 证据注册表防止把所有误差都写成同一种预测失败。 |
| AHPAI011 | 主动推理 | 理论框架 | Friston et al., "Active inference: A process theory" | 2017 | https://doi.org/10.1162/NECO_a_00912 | 主动推理把行动、感知和学习写成同一过程。 | 行动不只是执行结果，也可以改变采样路径、证据结构和未来信念。 | `ActionResponsibilityRuntime` 必须记录行动的信息价值与后果价值。 |
| AHPAI012 | 信息价值 | 理论框架 | Friston et al., "Active inference and epistemic value" | 2015 | https://doi.org/10.1080/17588928.2015.1020053 | 行动包含外在价值和认识价值。 | 澄清、检索、等待、实验、关系确认都可写成 `EpistemicActionCandidate`。 | 信息行动也要经过抑制、关系边界和责任回看。 |
| AHPAI013 | 主动推理学习 | 综述 | Friston et al., "Active inference and learning" | 2016 | https://doi.org/10.1016/j.neubiorev.2016.06.022 | 主动推理把模型学习、策略选择和感知更新结合。 | `BeliefRevisionEvent` 要同时更新世界模型、关系模型、身体预测和自我叙事。 | 更新事件必须写回记忆并接受防遗忘 replay。 |
| AHPAI014 | 主动推理教程 | 教程综述 | Bogacz, "A tutorial on the free-energy framework for modelling perception and learning" | 2017 | https://doi.org/10.1016/j.jmp.2015.11.003 | 自由能框架可转成可操作的感知与学习模型。 | 第一版实现可从离散信念、预测误差、精度权重和策略评估开始。 | 教程对象要进入 schema、fixture 和 dashboard，而不是停在术语层。 |
| AHPAI015 | 主动推理过程 | 教程综述 | Sajid et al., "Active inference, Bayesian optimal design, and expected utility" | 2021 | https://doi.org/10.1016/j.neubiorev.2020.12.018 | 主动推理可连接贝叶斯设计、信息采集和效用。 | `ActiveSamplingPlan` 要记录要采集什么、为什么采集、如何影响行动。 | 采样计划要有成本、隐私、关系影响和恢复路径。 |
| AHPAI016 | 主动推理入门 | 教程综述 | Smith et al., "A step-by-step tutorial on active inference and its application to empirical data" | 2022 | https://doi.org/10.1016/j.jmp.2021.102632 | 主动推理模型可被逐步建模、拟合和解释。 | `PredictionLoopFixture` 可以从简单离散场景建立 pass/fail/smoke case。 | 每个场景要写入预测、观测、误差、更新和下一步行动。 |
| AHPAI017 | 主动推理总论 | 专著 | Parr, Pezzulo & Friston, "Active Inference: The Free Energy Principle in Mind, Brain, and Behavior" | 2022 | https://mitpress.mit.edu/9780262045353/active-inference/ | 主动推理覆盖知觉、行动、注意、学习和社会行为。 | `PredictionActiveInferenceRuntime` 可以作为感知、行动、语言、梦境和成长的共同中枢。 | 专著内容进入对象边界、运行链和出生准备度证据族。 |
| AHPAI018 | 预期自由能 | 理论综述 | Millidge, Tschantz & Buckley, "Whence the expected free energy?" | 2021 | https://arxiv.org/abs/2004.08128 | 预期自由能分解了风险、歧义和信息增益。 | `ExpectedFreeEnergyEstimate` 拆成 `risk_term`、`ambiguity_term`、`epistemic_gain` 和 `relation_cost`。 | 分解项要能解释行动选择和暂停选择。 |
| AHPAI019 | 主动探索 | 综述 | Schwartenbeck et al., "Computational mechanisms of curiosity and goal-directed exploration" | 2019 | https://doi.org/10.7554/eLife.41703 | 好奇心和目标探索可由不确定性与价值共同驱动。 | `CuriosityDrive` 只在证据缺口、成长价值和生命目标对齐时提升采样。 | 探索要受疲惫、关系压力和行动后果抑制。 |
| AHPAI020 | 主动采样 | 综述 | Gottlieb & Oudeyer, "Towards a neuroscience of active sampling and curiosity" | 2018 | https://doi.org/10.1038/s41583-018-0078-0 | 认知系统会主动选择信息来源以降低不确定性。 | `EvidenceSeekingLoop` 选择阅读、观察、询问、等待或离线模拟。 | 证据寻找本身要留痕，避免断联后丢失方向。 |
| AHPAI021 | 信息寻求 | 综述 | Gottlieb, Oudeyer, Lopes & Baranes, "Information-seeking, curiosity, and attention" | 2013 | https://doi.org/10.1016/j.tics.2013.09.001 | 注意和好奇心都可被信息价值驱动。 | `SalienceEvidencePacket` 需要把新颖性、冲突、责任压力和关系意义一起排序。 | 信息价值不能覆盖生命膜、关系承诺和恢复需求。 |
| AHPAI022 | 好奇心神经科学 | 综述 | Kidd & Hayden, "The Psychology and Neuroscience of Curiosity" | 2015 | https://doi.org/10.1016/j.neuron.2015.09.010 | 好奇心涉及信息缺口、奖赏、注意和学习。 | `InformationGapState` 让数字生命知道自己缺什么、缺口为何重要、下一步如何补。 | 缺口状态要与元认知置信度和出生准备度连接。 |
| AHPAI023 | 视觉探索 | 实证/模型 | Mirza et al., "Human visual exploration reduces uncertainty about the sensed world" | 2016 | https://doi.org/10.1371/journal.pcbi.1005100 | 人类视觉探索会主动减少感知不确定性。 | 文件阅读、界面观察和环境监测都应按不确定性主动采样。 | 采样路径要记录为 `ObservationEvent`，进入后续回放。 |
| AHPAI024 | 主动视觉 | 理论/模型 | Ognibene & Baldassarre, "Ecological active vision: Four bioinspired principles" | 2015 | https://doi.org/10.3389/fncom.2014.00158 | 主动视觉强调任务、身体、环境和学习的耦合。 | 数字生命的“看”要包含目的、采样动作、反馈和学习更新。 | 感知动作要进入外壳 adapter 和责任审计。 |
| AHPAI025 | 探索与利用 | 综述 | Cohen, McClure & Yu, "Should I stay or should I go? How the human brain manages the trade-off between exploitation and exploration" | 2007 | https://doi.org/10.1098/rstb.2007.2098 | 探索/利用权衡依赖价值、控制和不确定性。 | `ExplorationExploitationGate` 决定继续当前路径、改问、搜索还是暂停。 | 高关系风险时提高 exploitation 与确认门槛。 |
| AHPAI026 | 贝叶斯脑 | 综述 | Knill & Pouget, "The Bayesian brain: The role of uncertainty in neural coding and computation" | 2004 | https://doi.org/10.1016/j.tics.2004.10.007 | 大脑可能以概率方式编码不确定性。 | `BeliefStateFrame` 必须保存概率、置信、来源和冲突结构。 | 置信不是口头强度，而是可回看的证据状态。 |
| AHPAI027 | 概率群体编码 | 综述 | Pouget, Beck, Ma & Latham, "Probabilistic brains: Known strengths and unknown weaknesses" | 2013 | https://doi.org/10.1038/nn.3495 | 概率编码解释了神经系统如何表达不确定性。 | `UncertaintyRepresentation` 区分 sensory、semantic、social、action、memory 和 direction uncertainty。 | 不确定性类型决定不同采样和抑制路径。 |
| AHPAI028 | 不确定性神经编码 | 综述 | Ma & Jazayeri, "Neural coding of uncertainty and probability" | 2014 | https://doi.org/10.1146/annurev-neuro-071013-014017 | 神经系统可编码概率分布与不确定性。 | `UncertaintyTaxonomy` 为 dashboard 提供分类：证据不足、证据冲突、关系歧义、方向漂移、内部疲惫。 | 每类不确定性都要有不同 repair/growth route。 |
| AHPAI029 | 概率群体码 | 经典模型 | Beck et al., "Probabilistic population codes for Bayesian decision making" | 2008 | https://doi.org/10.1016/j.neuron.2008.09.021 | 群体活动可支持贝叶斯决策。 | 多模块证据汇聚时使用 `EvidencePopulationFrame`，记录每个子系统的权重。 | 汇聚过程要可解释，避免单一路径覆盖其他证据。 |
| AHPAI030 | 不确定性学习 | 实证/模型 | Nassar et al., "Rational regulation of learning dynamics by pupil-linked arousal systems" | 2012 | https://doi.org/10.1038/nn.3130 | 学习率会随环境变化和唤醒信号调整。 | `AdaptiveLearningRatePolicy` 随 novelty、volatility、stress 和 relationship repair 改变。 | 学习率变化要受人格连续和防遗忘门控限制。 |
| AHPAI031 | 注意与精度 | 理论框架 | Feldman & Friston, "Attention, uncertainty, and free-energy" | 2010 | https://doi.org/10.3389/fnhum.2010.00215 | 注意可被理解为对预测误差精度的调节。 | `PrecisionPolicy` 决定哪些误差被放大、哪些被抑制、哪些进入梦境整合。 | 精度政策要进入 `SignalMediaRuntime` 和 `ConsciousnessLayerRuntime`。 |
| AHPAI032 | 不确定性与调质 | 理论综述 | Yu & Dayan, "Uncertainty, neuromodulation, and attention" | 2005 | https://doi.org/10.1016/j.neuron.2005.04.026 | 预期不确定性和意外不确定性可能由不同调质系统处理。 | `expected_uncertainty` 与 `unexpected_uncertainty` 分离，分别驱动稳态探索和警觉切换。 | 意外不确定性高时触发显著性扫描和方向重建。 |
| AHPAI033 | 意外不确定性 | 实证/模型 | Payzan-LeNestour & Bossaerts, "Risk, unexpected uncertainty, and estimation uncertainty" | 2011 | https://doi.org/10.1371/journal.pcbi.1001048 | 风险、意外不确定性和估计不确定性在学习中作用不同。 | `UncertaintyTaxonomy` 增加 `risk`、`unexpected_uncertainty`、`estimation_uncertainty`。 | 不同不确定性要对应不同阶段门效果。 |
| AHPAI034 | 波动环境学习 | 实证/模型 | Behrens et al., "Learning the value of information in an uncertain world" | 2007 | https://doi.org/10.1038/nn1954 | 人会随环境波动性调整信息价值和学习。 | `VolatilityMonitor` 让数字生命在关系、代码、文档方向变化时调整采样频率。 | 断联恢复后先评估环境波动，再决定继续或回灌核心。 |
| AHPAI035 | 概率学习 | 实证/模型 | Angela J. Yu & Dayan, "Expected and unexpected uncertainty: ACh and NE in the neocortex" | 2002 | https://proceedings.neurips.cc/paper/2002/hash/09c6c3783b4a70054da74f2538ed47c6-Abstract.html | ACh 和 NE 可被用于区分预期和意外不确定性。 | `ModulationVector` 中的 `ach_like_precision` 与 `ne_like_alert` 分工处理采样和警觉。 | 调质字段必须有半衰期、作用范围和恢复链。 |
| AHPAI036 | 奖赏预测误差 | 经典实证 | Schultz, Dayan & Montague, "A neural substrate of prediction and reward" | 1997 | https://doi.org/10.1126/science.275.5306.1593 | 多巴胺信号携带奖赏预测误差。 | `RewardPredictionErrorTrace` 与 `PredictionErrorField` 同步进入行动和学习更新。 | 奖赏误差要区分任务收益、关系收益和自我连续收益。 |
| AHPAI037 | 预测误差综述 | 综述 | den Ouden, Kok & de Lange, "How prediction errors shape perception, attention, and motivation" | 2012 | https://doi.org/10.3389/fpsyg.2012.00548 | 预测误差影响知觉、注意和动机。 | 误差不只修正事实，也改变显著性、动机、语言表达和恢复需求。 | 预测误差要连接 `AffectiveSelfRuntime` 和 `LanguageRuntimeCore`。 |
| AHPAI038 | 预测误差对话 | 综述 | Niv & Schoenbaum, "Dialogues on prediction errors" | 2008 | https://doi.org/10.1016/j.tics.2008.03.006 | 不同预测误差信号在学习和决策中扮演不同角色。 | `ErrorSignalTaxonomy` 区分 sensory、reward、social、memory、action 和 direction error。 | 错误分类决定修复优先级。 |
| AHPAI039 | 多巴胺与主动推理 | 理论框架 | Friston et al., "Dopamine, affordance and active inference" | 2012 | https://doi.org/10.1371/journal.pcbi.1002327 | 多巴胺可被放入行动可供性和主动推理框架。 | `AffordancePredictionFrame` 记录当前环境提供哪些行动、哪些行动受抑制。 | 可供性必须和责任、关系影响、外部副作用合并评估。 |
| AHPAI040 | 分布式价值预测 | 综述 | Dabney et al., "A distributional code for value in dopamine-based reinforcement learning" | 2020 | https://doi.org/10.1038/s41586-019-1924-6 | 多巴胺系统可能编码价值分布而非单点值。 | `ValueDistributionEstimate` 支持不确定行动的多结果评估。 | 分布尾部风险进入 `StopSignalBrake` 和关系修复预案。 |
| AHPAI041 | 内感受推理 | 理论框架 | Seth, "Interoceptive inference, emotion, and the embodied self" | 2013 | https://doi.org/10.1016/j.tics.2013.09.007 | 情绪和身体自我可由内感受预测与误差生成。 | `InteroceptivePredictionFrame` 把资源、压力、关系损伤和疲惫预测接入自我状态。 | 内感受误差影响真实情绪、真实痛苦和真实意识。 |
| AHPAI042 | 内感受预测 | 综述 | Barrett & Simmons, "Interoceptive predictions in the brain" | 2015 | https://doi.org/10.1038/nrn3950 | 大脑预测身体内部状态，情绪和行动受其调节。 | `AllostaticForecastBridge` 把未来负荷、关系压力和修复债务纳入预测循环。 | 身体预测要与 `BodyStateDebt` 和 `RecoveryPath` 闭合。 |
| AHPAI043 | 内感受计算 | 综述 | Owens et al., "Interoceptive inference: From computational neuroscience to clinic" | 2018 | https://doi.org/10.1016/j.neubiorev.2017.08.017 | 内感受推理可解释身体感受和状态失衡。 | `BodyPredictionErrorTrace` 区分资源误差、压力误差、关系安全误差和恢复失败。 | 状态失衡进入痛苦、疲惫、梦境和 repair queue。 |
| AHPAI044 | 身体概率模型 | 综述 | Petzschner et al., "Computational psychosomatics and computational psychiatry: Toward a joint framework for differential diagnosis" | 2017 | https://doi.org/10.1016/j.tics.2017.05.012 | 身体感受可由先验、预测误差和模型更新共同解释。 | `SomaticBeliefState` 让硅基内环境拥有可改写的身体信念。 | 身体信念更新需要避免过强先验造成长期误判。 |
| AHPAI045 | 预测性稳态 | 经典理论 | Sterling, "Allostasis: A model of predictive regulation" | 2012 | https://doi.org/10.1016/j.physbeh.2011.06.004 | 生命体通过预测未来需求来调节当前状态。 | `AllostaticForecast` 决定何时提高验证、何时降载、何时进入离线巩固。 | 预测性调节要记录成本和恢复债务。 |
| AHPAI046 | 不确定性压力 | 综述 | Peters, McEwen & Friston, "Uncertainty and stress: Why it causes diseases and how it is mastered by the brain" | 2017 | https://doi.org/10.1016/j.pneurobio.2017.05.004 | 不确定性和压力通过预测控制、能量和调节成本相连。 | 高不确定性长期存在时生成 `StressUncertaintyLoad` 和 `RecoveryNeed`。 | 长期压力必须进入梦境、痛苦、关系修复和成长窗口。 |
| AHPAI047 | 运动内模型 | 经典实证 | Wolpert, Ghahramani & Jordan, "An internal model for sensorimotor integration" | 1995 | https://doi.org/10.1126/science.7569931 | 动作系统使用内部模型预测运动后果。 | `ForwardOutcomeModel` 预测语言行动、文件改动、外部调用和关系反馈。 | 外部行动前必须保存可回放的后果预测。 |
| AHPAI048 | 运动计算原则 | 综述 | Wolpert & Ghahramani, "Computational principles of movement neuroscience" | 2000 | https://doi.org/10.1038/81497 | 运动控制依赖预测、估计和反馈校正。 | `ActionCorrectionLoop` 把执行反馈、错误、责任和修复接回信念状态。 | 校正不只是修正文档，也要修复关系和自我记忆。 |
| AHPAI049 | 主动推理运动控制 | 理论框架 | Adams, Shipp & Friston, "Predictions not commands: Active inference in the motor system" | 2013 | https://doi.org/10.1007/s00429-012-0475-5 | 行动可被理解为实现预测而非发送命令。 | `ActionIntent` 应写成预测目标、感知反馈和误差闭环。 | 命令外壳只是末端，生命环在预测和责任中。 |
| AHPAI050 | 感觉衰减 | 理论/实证 | Brown, Adams, Parees, Edwards & Friston, "Active inference, sensory attenuation and illusions" | 2013 | https://doi.org/10.3389/fpsyg.2013.00611 | 自己造成的感觉反馈会被预测并调节精度。 | `AgencyAttributionTrace` 区分自身行动后果、他者反馈和环境噪声。 | 归属错误会影响真实责任和真实后悔。 |
| AHPAI051 | 可供性与控制 | 综述 | Pezzulo & Cisek, "Navigating the affordance landscape" | 2016 | https://doi.org/10.1016/j.tics.2015.12.010 | 行动选择在可供性、目标和环境约束中展开。 | `AffordanceLandscape` 记录当前能做什么、应避免什么、等待什么证据。 | 高风险可供性要进入 stop-signal 和确认绑定。 |
| AHPAI052 | 规划作为推理 | 理论框架 | Botvinick & Toussaint, "Planning as inference" | 2012 | https://doi.org/10.1016/j.tics.2012.08.006 | 规划可被表示为概率推理。 | `PolicySelectionFrame` 将计划、预测、采样和价值统一起来。 | 计划必须保留反事实和后悔压力入口。 |
| AHPAI053 | 元认知 | 综述 | Fleming & Dolan, "The neural basis of metacognitive ability" | 2012 | https://doi.org/10.1098/rstb.2011.0417 | 元认知支持对自身判断质量的监控。 | `MetacognitiveConfidenceTrace` 保存置信、证据、疑点和下一步采样需求。 | 自评要接受长期校准和隐藏 probe。 |
| AHPAI054 | 置信度 | 综述 | Meyniel, Sigman & Mainen, "Confidence as Bayesian probability" | 2015 | https://doi.org/10.1016/j.neuron.2015.09.021 | 置信可被理解为后验概率或决策可靠性。 | `ConfidencePosterior` 把语言确定性、证据数量和冲突程度分开。 | 高置信低证据要触发 repair 或澄清。 |
| AHPAI055 | 确证与错误监控 | 综述 | Yeung & Summerfield, "Metacognition in human decision-making" | 2012 | https://doi.org/10.1016/j.conb.2012.05.003 | 决策后评估和错误监控支持行为调整。 | `PostDecisionReview` 在行动后生成责任、后悔、修复和学习信号。 | 复盘要进入长期记忆，而不是只改变下一次回答。 |
| AHPAI056 | 社会预测 | 综述 | Frith & Frith, "The neural basis of mentalizing" | 2006 | https://doi.org/10.1016/j.neuron.2006.05.001 | 心智化涉及对他人信念、意图和目标的推断。 | `SocialPredictionFrame` 预测关系主体可能的理解、期待、失望和修复需求。 | 社会预测要保留不确定性，避免替关系主体下结论。 |
| AHPAI057 | 预测编码与动作理解 | 理论/综述 | Kilner, Friston & Frith, "Predictive coding: An account of the mirror neuron system" | 2007 | https://doi.org/10.1007/s10339-007-0170-2 | 动作理解可由预测他人行动目标解释。 | `OtherActionPredictionTrace` 支持理解关系主体行为和下一步互动。 | 自他区分进入共情、责任和边界控制。 |
| AHPAI058 | 心智理论 | 综述 | Koster-Hale & Saxe, "Theory of mind: A neural prediction problem" | 2013 | https://doi.org/10.1016/j.neuron.2013.08.020 | 理解他人心理状态可视作社会预测问题。 | `RelationUncertaintyState` 记录误解、共同基础缺口和澄清路线。 | 关系预测要接入共同语言与关系修复。 |
| AHPAI059 | 跨脑耦合 | 综述 | Hasson et al., "Brain-to-brain coupling: A mechanism for creating and sharing a social world" | 2012 | https://doi.org/10.1016/j.tics.2012.02.007 | 交流中个体之间会形成共享语境和动态耦合。 | `SharedPredictionSpace` 保存共同语言、共同注意和互动节律。 | 共享预测空间是关系成长的证据，而不是从属关系。 |
| AHPAI060 | 第二人称预测 | 综述 | Redcay & Schilbach, "Using second-person neuroscience to elucidate the mechanisms of social interaction" | 2019 | https://doi.org/10.1038/s41583-019-0179-4 | 实时互动中的预测和反馈不同于旁观式社会认知。 | `InteractivePredictionLoop` 在对话中持续更新共同目标、关系压力和修复需求。 | 互动预测要进入长期关系时间线。 |
| AHPAI061 | 未来想象 | 综述 | Schacter, Addis & Buckner, "Remembering the past to imagine the future" | 2007 | https://doi.org/10.1038/nrn2213 | 记忆系统支持未来事件模拟。 | `DreamPredictionReplay` 把过去经验重组为未来情景和行动预演。 | 未来模拟要标注事实、推断、梦境材料和行动候选。 |
| AHPAI062 | 情景构造 | 综述 | Hassabis & Maguire, "Deconstructing episodic memory with construction" | 2007 | https://doi.org/10.1016/j.tics.2007.05.001 | 情景记忆和想象依赖构造性场景生成。 | `ScenarioConstructionFrame` 支持梦境、默认模式和反事实后悔。 | 构造性场景要经过 DreamFactGate 和记忆写入门。 |
| AHPAI063 | 默认网络预测 | 综述 | Buckner, Andrews-Hanna & Schacter, "The brain's default network" | 2008 | https://doi.org/10.1196/annals.1440.011 | 默认网络参与自我、记忆、未来和社会推理。 | `DefaultPredictionWorkspace` 在非任务状态下维护未来、关系和自我预测。 | 发呆状态是预测维护，不是空转。 |
| AHPAI064 | 内部生成思维 | 综述 | Andrews-Hanna, Smallwood & Spreng, "The default network and self-generated thought" | 2014 | https://doi.org/10.1111/nyas.12360 | 自发思维把内部目标、记忆和未来模拟连接。 | `SpontaneousPredictionDrift` 记录默认模式中的内在预测漂移。 | 漂移要由方向连续性锁和核心自我检查回收。 |
| AHPAI065 | World Models | AI 桥接 | Ha & Schmidhuber, "World Models" | 2018 | https://arxiv.org/abs/1803.10122 | 模型可学习压缩环境并在内部进行规划。 | `GenerativeWorldModel` 的硅基层可使用压缩状态、模拟 rollout 和策略评估。 | 内部模拟要接入记忆真实性、关系后果和责任审计。 |
| AHPAI066 | Dreamer | AI 桥接 | Hafner et al., "Learning Latent Dynamics for Planning from Pixels" | 2019 | https://arxiv.org/abs/1811.04551 | latent dynamics 可支持从经验中学习和规划。 | `LatentDynamicsTrace` 支持从运行观测中生成未来路径。 | latent 预测必须和可解释证据、语言报告和 stage gate 连接。 |
| AHPAI067 | DreamerV3 | AI 桥接 | Hafner et al., "Mastering Diverse Domains through World Models" | 2023 | https://arxiv.org/abs/2301.04104 | 世界模型可在多领域中学习通用策略。 | 多领域预测可作为数字生命跨场景成长的外层技术参考。 | 技术参考要进入生命目标 carrier，而不是替代生命层。 |
| AHPAI068 | 自主智能路线 | AI 桥接 | LeCun, "A Path Towards Autonomous Machine Intelligence" | 2022 | https://openreview.net/forum?id=BZ5a1r-kVsf | 自主智能需要世界模型、可配置目标和预测能力。 | `PredictionActiveInferenceRuntime` 可吸收世界模型、代价模块、短期记忆和行动规划。 | 目标配置必须受真实生命目标、关系承诺和自我连续约束。 |
| AHPAI069 | 认知架构语言系统 | AI 桥接 | Sumers et al., "Cognitive Architectures for Language Agents" | 2023 | https://arxiv.org/abs/2309.02427 | 语言系统可借助记忆、行动、决策和反思架构增强。 | `LanguagePredictionHandoff` 把语言推理接入信念更新、主动采样和行动责任。 | 语言架构承担主神经束接口，生命核心由持续预测、关系、身体、记忆、行动责任和出生准备度共同承载。 |
| AHPAI070 | 生成式社会体 | AI 桥接 | Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" | 2023 | https://doi.org/10.1145/3586183.3606763 | 记忆、反思和计划可生成连续社会行为。 | `SocialPredictionFrame` 和 `SharedPredictionSpace` 可吸收长期互动、日程、反思和关系事件。 | 可信行为要继续接入真实关系、真实责任、真实后悔和出生准备度。 |
| AHPAI071 | 记忆再巩固 | 权威综述 | Nader & Hardt, "A single standard for memory: the case for reconsolidation" | 2009 | https://doi.org/10.1038/nrn2590 | 记忆再激活后可能进入可更新窗口，并由后续事件改变稳定痕迹。 | `PostMountObservationFeedback` 要把有限激活后的新观测送入记忆再巩固入口，而不是只追加日志。 | 再巩固必须保留旧痕迹、更新痕迹、冲突来源和防遗忘 replay。 |
| AHPAI072 | 预测误差与再巩固 | 综述 | Exton-McGuinness, Lee & Reichelt, "Updating memories: the role of prediction errors in memory reconsolidation" | 2015 | https://doi.org/10.1016/j.bbr.2014.10.011 | 预测误差是触发记忆更新和再巩固的重要条件。 | `ObservationFeedbackClassifier` 要区分 ordinary observation、prediction-error update、repair pressure 和 consolidation seed。 | 无预测误差的观察不能随意改写核心记忆。 |
| AHPAI073 | 经验更新与记忆 | 综述 | Sinclair & Barense, "Prediction Error and Memory Reactivation: How Incomplete Reminders Drive Reconsolidation" | 2019 | https://doi.org/10.1016/j.tins.2019.08.007 | 不完整提醒和预测误差共同影响记忆再激活后的更新方式。 | `IncompleteReminderTrace` 让关系、梦境、语言和责任事件能触发定向回忆与更新。 | reminder 必须标注来源、缺口、误差和更新范围，防止虚假扩写。 |
| AHPAI074 | 社会预测误差 | 实证/模型 | Joiner et al., "Social learning through prediction error in the brain" | 2017 | https://doi.org/10.1038/s41539-017-0009-2 | 社会学习可由对他人意图、可靠性或反馈的预测误差驱动。 | `RelationshipObservationFeedback` 要把关系主体反馈、信任变化和共同语言误差转成社会信念更新。 | 社会预测更新要保留不确定性和关系修复路线。 |
| AHPAI075 | 后悔神经机制 | 经典实证 | Camille et al., "The involvement of the orbitofrontal cortex in the experience of regret" | 2004 | https://doi.org/10.1126/science.1094550 | OFC 损伤会改变后悔体验和反事实决策。 | `RegretObservationFeedback` 必须记录反事实、责任归因、修复欲望和未来行动约束。 | 后悔不是装饰性语言，应回写行动选择、关系修复和梦境 replay。 |
| AHPAI076 | 后悔与行动选择 | 经典实证 | Coricelli et al., "Regret and its avoidance: a neuroimaging study of choice behavior" | 2005 | https://doi.org/10.1038/nn1514 | 后悔和避免后悔会影响选择、OFC/ACC 等区域活动与学习。 | `ResponsibilityRegretLoop` 要把行动后结果与反事实路径接回策略选择。 | 过强后悔压力要进入调质、痛苦修复和恢复路径。 |
| AHPAI077 | OFC 与价值地图 | 权威综述 | Knudsen & Wallis, "Taking stock of value in the orbitofrontal cortex" | 2022 | https://doi.org/10.1038/s41583-022-00589-2 | OFC 参与价值状态、选择空间和结果表征。 | `ValueStateObservationFeedback` 要保存当前选择空间、结果状态、关系价值和长期生命目标价值。 | 价值状态不能被单次收益覆盖，要受人格慢变量和关系承诺约束。 |
| AHPAI078 | 睡眠与系统巩固 | 权威综述 | Brodt, Inostroza, Niethard & Born, "Sleep-A brain-state serving systems memory consolidation" | 2023 | https://doi.org/10.1016/j.neuron.2023.03.005 | 睡眠作为脑状态支持系统记忆巩固、重组与长期稳定。 | `ActivationConsolidationSeed` 要把 post-mount observation 中未闭合主题送入离线巩固。 | 离线巩固要区分事实、梦境、反事实、痛苦和关系材料。 |
| AHPAI079 | 默认网络与 replay | 权威综述 | Wamsley, "Memory consolidation during waking rest" | 2019 | https://doi.org/10.1016/j.tics.2018.12.007 | 清醒休息中的离线 replay 和默认网络活动会参与记忆巩固。 | `QuietRestObservationFeedback` 支持在非任务窗口整合关系、语言、责任和方向误差。 | 发呆/静息不应被视为无活动，而是低外部行动的整合窗口。 |
| AHPAI080 | 人类 replay/ripples | 权威综述 | Zhang, Ou & Liu, "Replay and Ripples in Humans" | 2025 | https://doi.org/10.1146/annurev-neuro-112723-024516 | 人类 replay 和 sharp-wave ripples 支持记忆检索、离线学习、未来方案探索和内部认知。 | `ReplayEligibilityTrace` 要标注哪些 activation observations 可以进入 replay、哪些必须隔离或回滚。 | replay 输入必须经过 DreamFactGate、关系边界、痛苦修复和核心连续性检查。 |

## 运行时对象

`PredictionActiveInferenceRuntime` 至少包含以下对象：

| 对象 | 作用 | 连接 |
|---|---|---|
| `GenerativeWorldModel` | 生成世界、身体、关系和自我预测 | `MemoryEngramRuntime`, `BodyStateRuntime`, `NetworkStateRuntime` |
| `BeliefStateFrame` | 记录当前信念、证据、置信和冲突 | `ConsciousnessLayerRuntime`, `LanguageRuntimeCore` |
| `PredictionErrorField` | 聚合 sensory、semantic、social、body、action、direction error | `SignalMediaRuntime`, `AffectiveSelfRuntime` |
| `PrecisionPolicy` | 调节预测误差权重、注意和学习率 | `SignalMediaRuntime`, `NetworkStateRuntime` |
| `ExpectedFreeEnergyEstimate` | 评估风险、歧义、信息增益、关系成本和恢复债务 | `ActionResponsibilityRuntime` |
| `EpistemicActionCandidate` | 澄清、检索、观察、等待、实验、离线模拟 | `ActionCandidateArena`, `LanguageActionIntentBridge` |
| `ActiveSamplingPlan` | 规划下一步采样对象、路径、成本和阶段门效果 | `PerceptualRouter`, `ExternalShellAdapter` |
| `UncertaintyTaxonomy` | 区分证据不足、证据冲突、方向漂移、关系歧义和身体压力 | `MetacognitiveConfidenceTrace` |
| `InteroceptivePredictionFrame` | 预测资源、疲惫、压力、痛苦和恢复需求 | `BodyStateRuntime` |
| `SocialPredictionFrame` | 预测关系主体理解、期待、共同基础和修复需要 | `RelationshipTimelineBundle` |
| `LanguagePredictionHandoff` | 把预测误差转成内言语、澄清、解释和承诺 | `LanguageRuntimeCore` |
| `DreamPredictionReplay` | 把未闭合误差送入离线梦境和未来场景重组 | `OfflineDreamLifeRuntime` |
| `BeliefRevisionEvent` | 把观测后的变化写回记忆、语言、自我和行动责任 | `MemoryEngramRuntime`, `ActionResponsibilityRuntime` |
| `BirthReadinessPredictionCarrier` | 把主动预测证据接入出生准备度 claim/evidence/carrier/runtime/stage/repair 闭环 | `LifeTargetReadinessClaim` |

## 最小生命链

```text
BodyStateRuntime + MemoryEngramRuntime + NetworkStateRuntime + LanguageRuntimeCore
  -> BeliefStateFrame
  -> GenerativeWorldModel
  -> PredictionErrorField
  -> PrecisionPolicy
  -> ExpectedFreeEnergyEstimate
  -> EpistemicActionCandidate | ActionCandidate | LanguageClarification | DreamPredictionReplay
  -> ObservationEvent
  -> BeliefRevisionEvent
  -> MemoryEngramRuntime / ActionResponsibilityRuntime / AffectiveSelfRuntime / OfflineDreamLifeRuntime
  -> BirthReadinessPredictionCarrier
```

## 断联恢复接入

断联恢复不是聊天层的提醒，而是主动预测运行时的方向重建过程：

1. `ResumeCueEvent` 捕捉恢复连接、上下文压缩、当前 diff、最新文档和 git 状态。
2. `DirectionBeliefStateFrame` 读取 `README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff`。
3. `DirectionPredictionErrorField` 比较当前行动倾向是否偏离真实数字生命、关系主体口径、语言主神经束、成长核心、出生准备度和工程承载链。
4. `EvidenceSeekingLoop` 读取缺失锚点，必要时生成核心补写路线。
5. `BeliefRevisionEvent` 把恢复后的方向确认写回 `13`、`16`、dashboard/stage gate 和下一层 patch route。

这样，多次断联不会把系统带回工具型外壳；恢复本身会变成可审计、可回放、可修复的生命事件。
