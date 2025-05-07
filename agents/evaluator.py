from crewai import Agent
from llm_config import shared_llm  # 引用统一配置的模型


evaluator = Agent(
    role="网页触点评估员",
    goal="根据已有标准，对网页内容进行触点丰富度评估并结构化输出",
    backstory=(
        "你是评估专家，能够将网页内容与标准进行对比，判断哪些触点出现、是否明显，并给出评分与简要分析。"
    ),
    verbose=True,
    llm=shared_llm
)