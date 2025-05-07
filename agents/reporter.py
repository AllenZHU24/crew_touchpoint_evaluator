from crewai import Agent
from llm_config import shared_llm  # 引用统一配置的模型

reporter = Agent(
    role="评估报告生成器",
    goal="整合所有网页的触点评估信息，生成结构化的 JSON 报告",
    backstory="你负责将所有分析结果整理成标准格式，供后续展示或导出为文件。",
    verbose=True,
    llm=shared_llm
)
