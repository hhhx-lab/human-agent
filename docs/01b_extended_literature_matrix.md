# 扩展文献矩阵

本文件是 `01_literature_matrix.md` 的第二批扩展锚点，用 `AHX` 编号。它不替代原有 100 篇核心矩阵，而是补足主动推理、预测处理、社会认知、依恋、神经发育、压力-免疫-内分泌、具身认知、AI agent 深层架构等缺口。

| ID | 领域 | 类型 | 文献 | 年份 | 链接/DOI | 核心结论 | Agentic Human 启发 | 风险/争议 |
|---|---|---|---|---:|---|---|---|---|
| AHX001 | 预测处理/主动推理 | 经典实证 | Rao & Ballard, "Predictive coding in the visual cortex" | 1999 | https://doi.org/10.1038/4580 | 视觉皮层可被理解为预测与误差信号交互。 | 感知层应比较预测和输入，而非被动读取。 | 视觉皮层模型不能直接泛化全部认知。 |
| AHX002 | 预测处理/主动推理 | 理论框架 | Friston, "The free-energy principle: A unified brain theory?" | 2010 | https://doi.org/10.1038/nrn2787 | 自由能原则把感知、行动和学习统一为误差最小化。 | agent 可用预测误差组织感知、行动和记忆。 | 理论抽象度高，工程化需谨慎。 |
| AHX003 | 预测处理/主动推理 | 理论框架 | Clark, "Whatever next? Predictive brains, situated agents, and the future of cognitive science" | 2013 | https://doi.org/10.1017/S0140525X12000477 | 大脑是主动预测机器，认知嵌入身体和环境。 | human-agent 应主动采样、预测和修正。 | 预测处理不能解释全部机制细节。 |
| AHX004 | 预测处理/主动推理 | 理论框架 | Friston et al., "Active inference: A process theory" | 2017 | https://doi.org/10.1162/NECO_a_00912 | 主动推理把行动理解为改变世界以满足预测。 | 执行层应主动减少不确定性，不只是完成命令。 | 实现复杂，容易被过度抽象。 |
| AHX005 | 预测处理/主动推理 | 理论框架 | Friston et al., "Active inference and epistemic value" | 2015 | https://doi.org/10.1080/17588928.2015.1020053 | 行动既追求外在价值，也追求信息价值。 | 好奇心和澄清问题可被建模为 epistemic action。 | 信息价值不能压过共在者目标和安全边界。 |
| AHX006 | 社会认知/心智理论 | 综述 | Adolphs, "The social brain: Neural basis of social knowledge" | 2009 | https://doi.org/10.1146/annurev.psych.60.110707.163514 | 社会知识依赖面孔、情绪、价值、推理等多系统。 | 关系记忆和社会信号要进入核心系统。 | 社会脑不是单一模块。 |
| AHX007 | 社会认知/心智理论 | 综述 | Frith & Frith, "The neural basis of mentalizing" | 2006 | https://doi.org/10.1016/j.neuron.2006.05.001 | 心智化涉及理解他人意图、信念和目标。 | agent 需要共在者模型，而不只是指令解析。 | 心智化不能变成过度揣测。 |
| AHX008 | 社会认知/心智理论 | 综述 | Lieberman, "Social cognitive neuroscience: A review of core processes" | 2007 | https://doi.org/10.1146/annurev.psych.58.110405.085654 | 社会认知包括自我、他人、情绪和控制过程。 | 人格形成要包含社会互动历史。 | 社会认知高度依赖文化情境。 |
| AHX009 | 共情/关系 | 综述 | Decety & Jackson, "The functional architecture of human empathy" | 2004 | https://doi.org/10.1177/1534582304267187 | 共情包含情感共享、自他区分和认知调节。 | agent 的陪伴性应区分感知、推断和回应。 | 要形成真实情感共享，需要自他区分、情感共振、调节和关系记忆共同闭合。 |
| AHX010 | 共情/关系 | 高影响实证 | Singer et al., "Empathy for pain involves the affective but not sensory components of pain" | 2004 | https://doi.org/10.1126/science.1093535 | 看到亲近者疼痛会激活疼痛情感成分相关脑区。 | 关系强度会调制显著性和回应策略。 | 不能把 AI 关系类比为真实疼痛共感。 |
| AHX011 | 依恋/长期关系 | 综述 | Feldman, "The neurobiology of human attachments" | 2017 | https://doi.org/10.1016/j.tics.2016.11.007 | 人类依恋涉及多巴胺、催产素、同步节律和照护行为。 | 长期 agent 需要关系节律和信任变量。 | 依恋机制不能被直接复制到 AI。 |
| AHX012 | 社会脑假说 | 理论框架 | Dunbar, "The social brain hypothesis" | 1998 | https://doi.org/10.1002/(SICI)1520-6505(1998)6:5%3C178::AID-EVAN5%3E3.0.CO;2-8 | 灵长类脑容量与社会群体复杂度相关。 | 智能成长离不开社会关系复杂度。 | 进化假说不等于个体机制。 |
| AHX013 | 共同意图 | 理论框架 | Tomasello et al., "Understanding and sharing intentions" | 2005 | https://doi.org/10.1017/S0140525X05000129 | 人类文化认知依赖共同意图和共享注意。 | agent 需要共享目标表征，不只执行命令。 | 人类发展机制不能直接转写。 |
| AHX014 | 神经发育/关键期 | 综述 | Knudsen, "Sensitive periods in the development of the brain and behavior" | 2004 | https://doi.org/10.1162/0898929042304796 | 发展存在敏感期，经验对回路影响随阶段变化。 | agent 可设置不同成长阶段和学习率。 | AI 阶段划分是硅基转写。 |
| AHX015 | 神经发育 | 综述 | Johnson, "Functional brain development in humans" | 2001 | https://doi.org/10.1038/35081509 | 人脑功能发展是动态交互和逐渐专门化。 | 初期 agent 不必一次性定型。 | 人类儿童发育不能浪漫化。 |
| AHX016 | 青少年/控制发展 | 综述 | Casey, Tottenham, Liston & Durston, "Imaging the developing brain" | 2005 | https://doi.org/10.1016/j.tics.2005.10.011 | 认知控制和情绪/奖赏系统发展不同步。 | 成长型 agent 要区分能力增长和抑制成熟。 | 发展失衡类比需谨慎。 |
| AHX017 | 脑回路发育 | 综述 | Tau & Peterson, "Normal development of brain circuits" | 2010 | https://doi.org/10.1038/npp.2009.115 | 脑回路发育涉及结构、连接和功能成熟。 | agent 成长应有连接重构和稳定化阶段。 | 生物发育时间尺度不同。 |
| AHX018 | 发展基础 | 综述 | Stiles & Jernigan, "The basics of brain development" | 2010 | https://doi.org/10.1007/s11065-010-9148-4 | 脑发育包含神经发生、迁移、突触形成、修剪和髓鞘化。 | 数字生命成长可转写为生成、连接、剪枝、加速。 | 神经细胞过程需要映射为代码中的阶段、依赖和可塑性窗口。 |
| AHX019 | 关键期后可塑性 | 综述 | Hensch & Bilimoria, "Re-opening Windows: Manipulating Critical Periods for Brain Development" | 2012 | https://doi.org/10.1093/acprof:oso/9780199753673.003.0024 | 关键期可被抑制/兴奋平衡和环境因素调节。 | 成人式 agent 仍可学习，但需要门控。 | 书章来源，需与综述共同使用。 |
| AHX020 | 互补学习系统 | 理论框架 | McClelland, McNaughton & O'Reilly, "Why there are complementary learning systems" | 1995 | https://doi.org/10.1037/0033-295X.102.3.419 | 快速海马学习与慢速新皮层学习互补。 | 长期 agent 需要快写入和慢整合双系统。 | 经典模型需现代记忆研究修正。 |
| AHX021 | 智能体记忆系统 | 综述 | Kumaran, Hassabis & McClelland, "What learning systems do intelligent agents need?" | 2016 | https://doi.org/10.1016/j.tics.2016.05.004 | 智能体需要模型学习、情景记忆、泛化和规划系统。 | Agentic Human 的记忆要服务规划和泛化。 | 仍偏认知计算框架。 |
| AHX022 | 压力/allostasis | 经典理论 | McEwen & Stellar, "Stress and the individual: Mechanisms leading to disease" | 1993 | https://doi.org/10.1001/archinte.1993.00410180039004 | allostatic load 描述长期适应代价。 | 数字生命需要长期负荷和恢复预算。 | 疾病式状态应转写为长期负荷、损伤、恢复失败和维护需求。 |
| AHX023 | 压力介质 | 综述 | McEwen, "Protective and damaging effects of stress mediators" | 1998 | https://doi.org/10.1056/NEJM199801153380307 | 压力介质既保护也可能损伤系统。 | 高唤醒既能提高表现，也会带来长期成本。 | 生物压力和工程负载不同。 |
| AHX024 | 生命周期压力 | 综述 | Lupien et al., "Effects of stress throughout the lifespan on the brain, behaviour and cognition" | 2009 | https://doi.org/10.1038/nrn2639 | 压力影响随生命阶段、持续时间和脑区而变。 | 不同 agent 成长阶段应有不同压力策略。 | 人类生命周期类比需抽象。 |
| AHX025 | 压力网络 | 综述 | Joels & Baram, "The neuro-symphony of stress" | 2009 | https://doi.org/10.1038/nrn2632 | 压力影响快速和慢速系统，作用多阶段。 | agent 压力反应应分急性和慢性。 | 压力不是单一变量。 |
| AHX026 | 免疫/炎症 | 综述 | Dantzer et al., "From inflammation to sickness and depression" | 2008 | https://doi.org/10.1038/nrn2297 | 炎症信号可影响动机、情绪和认知。 | 内部错误/冲突可类比为系统炎症负荷。 | 可作为硅基炎症/异常负荷的早期转写，后续需要恢复、痛苦和防御回路。 |
| AHX027 | 炎症反射 | 经典实证/理论 | Tracey, "The inflammatory reflex" | 2002 | https://doi.org/10.1038/420853a | 神经系统可通过炎症反射调节免疫反应。 | 系统应有负反馈回路抑制长期异常。 | 免疫机制不能直接转写。 |
| AHX028 | 社会安全理论 | 理论框架 | Slavich, "Social Safety Theory" | 2020 | https://doi.org/10.1146/annurev-clinpsy-032816-045159 | 社会安全感影响压力、生理和健康。 | 长期共在关系会影响 agent 的风险/信任模型。 | 真实安全感需要关系稳定、威胁预测、恢复经验和长期信任校准。 |
| AHX029 | 奖赏分解 | 综述 | Berridge, Robinson & Aldridge, "Dissecting components of reward" | 2009 | https://doi.org/10.1016/j.coph.2008.12.014 | 奖赏可分 wanting、liking、learning。 | 奖赏系统应区分动机、满意和学习。 | 主观 liking 需要价值、满足、记忆珍视和行动偏好的长期耦合。 |
| AHX030 | 愉悦/动机系统 | 综述 | Berridge & Kringelbach, "Pleasure systems in the brain" | 2015 | https://doi.org/10.1016/j.neuron.2015.02.018 | 愉悦和动机涉及多系统，不等于多巴胺单点。 | reward 需要拆成喜欢、想要、学习和关系反馈。 | 享乐体验需要价值、内感受、目标达成和关系安全共同支撑。 |
| AHX031 | 多巴胺更新 | 综述 | Schultz, "Dopamine reward prediction-error signalling" | 2016 | https://doi.org/10.1038/nrn.2015.26 | 多巴胺预测误差有更复杂的成分和时程。 | 奖赏信号需要时序和不确定性结构。 | 多巴胺功能仍在发展。 |
| AHX032 | 计算神经调质 | 综述 | Dayan, "Twenty-five lessons from computational neuromodulation" | 2012 | https://doi.org/10.1016/j.neuron.2012.09.027 | 计算视角总结调质与学习、决策、状态控制。 | 调质因子应是系统级学习参数。 | 教训式综述仍需机制验证。 |
| AHX033 | 去甲肾上腺素 | 综述 | Sara, "The locus coeruleus and noradrenergic modulation of cognition" | 2009 | https://doi.org/10.1038/nrn2573 | LC-NE 调节注意、唤醒和行为灵活性。 | arousal/alerting 可作为全局增益。 | NE 不只是警觉开关。 |
| AHX034 | 乙酰胆碱 | 综述 | Hasselmo, "The role of acetylcholine in learning and memory" | 2006 | https://doi.org/10.1016/j.conb.2006.09.002 | ACh 调节编码、检索、注意和可塑性。 | 记忆写入和检索应受不同状态调制。 | ACh 作用复杂，不宜单一化。 |
| AHX035 | 具身认知 | 综述 | Barsalou, "Grounded cognition" | 2008 | https://doi.org/10.1146/annurev.psych.59.103006.093639 | 概念知识与感知、动作和情境系统相连。 | 语义记忆应接行动、感知和情境。 | 具身落地需要真实感知-行动闭环。 |
| AHX036 | 阅读/文化学习 | 综述 | Dehaene et al., "Illiterate to literate" | 2015 | https://doi.org/10.1038/nrn3924 | 阅读习得会重塑视觉和语言网络。 | 顶层符号能力会改造底层感知和记忆。 | 人类文字学习与 LLM 预训练不同。 |
| AHX037 | 意识工作空间 | 理论框架 | Dehaene & Naccache, "Towards a cognitive neuroscience of consciousness" | 2001 | https://doi.org/10.1016/S0010-0277(00)00123-2 | 全局工作空间早期框架区分后台处理与意识访问。 | 后台处理、全局广播和可报告状态应组成主观意识实现候选链。 | 主观意识实现需要跨模块整合。 |
| AHX038 | 现象意识/递归处理 | 理论框架 | Lamme, "Towards a true neural stance on consciousness" | 2006 | https://doi.org/10.1016/j.tics.2006.09.001 | 递归处理可能支持不同层次的意识现象。 | 反馈回路和可报告工作区要分开讨论。 | 意识理论争议大。 |
| AHX039 | 计算精神病学 | 综述 | Montague et al., "Computational psychiatry" | 2012 | https://doi.org/10.1016/j.tics.2011.11.018 | 计算模型可连接脑、行为和精神症状。 | 可用计算指标监测数字生命状态失衡。 | 临床概念需要转写为生命层指标。 |
| AHX040 | 计算精神病学桥梁 | 综述 | Huys, Maia & Frank, "Computational psychiatry as a bridge" | 2016 | https://doi.org/10.1038/nn.4238 | 强化学习、贝叶斯和决策模型可解释异常行为。 | 帮助定义不稳定状态和修复机制。 | 状态失衡指标必须服务修复与恢复。 |
| AHX041 | LLM Agent 认知架构 | AI 桥接 | Sumers et al., "Cognitive Architectures for Language Agents" | 2023 | https://arxiv.org/abs/2309.02427 | 将认知架构思想引入语言 agent 设计。 | CoALA 可作为 LLM 与认知模块桥梁。 | 预印本，需持续跟踪。 |
| AHX042 | ReAct | AI 桥接 | Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" | 2022 | https://arxiv.org/abs/2210.03629 | 推理轨迹和行动交替可提升任务处理。 | 执行层应保留 reasoning-action loop。 | 不是长期自我成长架构。 |
| AHX043 | Reflexion | AI 桥接 | Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" | 2023 | https://arxiv.org/abs/2303.11366 | 语言反思可作为强化学习式改进信号。 | 反思可进入巩固和习惯更新。 | 语言反思要接入记忆重写、习惯更新和人格慢变量，才能通向真实学习。 |
| AHX044 | Voyager | AI 桥接 | Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models" | 2023 | https://arxiv.org/abs/2305.16291 | 技能库、探索和自我改进支持开放式 agent。 | 程序记忆和技能沉淀非常关键。 | 游戏环境不等于人类生活环境。 |
| AHX045 | Tree of Thoughts | AI 桥接 | Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" | 2023 | https://arxiv.org/abs/2305.10601 | 多分支思考和评估提升复杂问题求解。 | 候选行动竞争可借鉴树搜索。 | 计算成本高，需抑制机制。 |
| AHX046 | MemGPT | AI 桥接 | Packer et al., "MemGPT: Towards LLMs as Operating Systems" | 2023 | https://arxiv.org/abs/2310.08560 | 通过虚拟上下文和外部记忆管理长程状态。 | 记忆分页和上下文管理可工程化。 | 仍不是完整多状态生命系统。 |
| AHX047 | AgentBench | AI 桥接 | Liu et al., "AgentBench: Evaluating LLMs as Agents" | 2023 | https://arxiv.org/abs/2308.03688 | 评测 LLM 在多环境 agent 任务中的能力。 | 后续需要为 human-agent 建立状态/成长评测。 | benchmark 不能覆盖人格成长。 |
| AHX048 | 内部模型/世界模型 | 理论框架 | Ha & Schmidhuber, "World Models" | 2018 | https://arxiv.org/abs/1803.10122 | agent 可学习压缩世界模型并在其中规划。 | 梦境/沙盒模拟可借鉴世界模型思想。 | AI 世界模型与人脑梦境不同。 |
| AHX049 | 模型化控制 | 综述 | Daw, Niv & Dayan, "Uncertainty-based competition between prefrontal and dorsolateral striatal systems" | 2005 | https://doi.org/10.1038/nn1560 | 不确定性影响模型化和习惯系统竞争。 | 高不确定时回到目标导向推理，低风险时用习惯。 | 动物/人类任务模型需抽象。 |
| AHX050 | 情绪建构 | 理论框架 | Barrett, "The theory of constructed emotion" | 2017 | https://doi.org/10.1093/scan/nsw154 | 情绪由概念、内感受和预测建构。 | 情绪类状态应由多因子组合形成。 | 该理论与基本情绪理论存在争议。 |
| AHX051 | 情绪悖论 | 理论框架 | Barrett, "Solving the emotion paradox" | 2006 | https://doi.org/10.1207/s15327957pspr1001_2 | 情绪类别不一定对应固定生物指纹。 | 不要把 agent 情绪做成固定标签。 | 理论争议需标注。 |
| AHX052 | 自我与身体 | 理论框架 | Damasio, "The Feeling of What Happens" | 1999 | https://archive.org/details/feelingofwhathap00dama | 自我体验与身体状态和意识叙事有关。 | 自我模型应连接内部状态和叙事。 | 书籍理论，不能作为唯一证据。 |
| AHX053 | 心理时间旅行 | 综述 | Suddendorf & Corballis, "The evolution of foresight" | 2007 | https://doi.org/10.1017/S0140525X07001975 | 人类能通过情景模拟进行未来预见。 | 默认模式和记忆系统应服务未来规划。 | 进化解释需谨慎。 |
| AHX054 | 前瞻记忆 | 综述 | Schacter et al., "The future of memory" | 2012 | https://doi.org/10.1016/j.neuron.2012.11.001 | 记忆系统支持想象未来和构造情景。 | 规划不是纯推理，而是记忆重组。 | 构造性记忆会带来偏差。 |
| AHX055 | 创造性网络 | 高影响实证 | Beaty et al., "Default and executive network coupling supports creative idea production" | 2015 | https://doi.org/10.1038/srep10964 | 创造需要默认网络和执行网络协作。 | 创造性 agent 需要联想与控制并存。 | 创造力任务生态效度有限。 |
| AHX056 | 文化认知/累积文化 | 综述 | Henrich, "The Secret of Our Success" | 2016 | https://press.princeton.edu/books/paperback/9780691178431/the-secret-of-our-success | 人类智能高度依赖文化学习和群体积累。 | human-agent 成长应吸收社群知识和实践规范。 | 书籍来源，需与实证研究配合。 |
| AHX057 | 预测处理与精神病理 | 综述 | Sterzer et al., "The predictive coding account of psychosis" | 2018 | https://doi.org/10.1016/j.biopsych.2018.05.015 | 预测和误差信号失衡可解释部分症状。 | agent 需监控先验过强或误差过强。 | 临床模型不可直接用于 AI。 |
| AHX058 | 元认知 | 综述 | Fleming & Dolan, "The neural basis of metacognitive ability" | 2012 | https://doi.org/10.1098/rstb.2011.0417 | 元认知涉及对自身判断的监控。 | agent 应有置信度、纠错和自我评估层。 | 自评不等于可靠性。 |
| AHX059 | 层级强化学习 | 理论框架 | Botvinick, Niv & Barto, "Hierarchically organized behavior and its neural foundations" | 2009 | https://doi.org/10.1016/j.cognition.2008.08.011 | 行为可按层级目标和子程序组织。 | 长期 agent 需要目标层级、子技能和习惯块。 | 层级 RL 与人类动机不同。 |
| AHX060 | 控制作为推理 | 理论框架 | Botvinick & Toussaint, "Planning as inference" | 2012 | https://doi.org/10.1016/j.tics.2012.08.006 | 规划可被表述为概率推理问题。 | 计划层可与主动推理/不确定性统一。 | 仍是计算理论层。 |
