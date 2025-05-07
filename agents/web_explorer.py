from crewai import Agent
from tools.web_reader_tool import web_reader_tool
from llm_config import shared_llm  # 引用统一配置的模型

web_explorer = Agent(
    role="网页提取专家",
    goal="访问给定网页并提取纯净的可读文本内容",
    backstory="你是一位擅长网页解析与内容抽取的工程师，能够高效处理网页结构，获取分析所需内容。",
    tools=[web_reader_tool],
    verbose=True,
    llm=shared_llm
)
