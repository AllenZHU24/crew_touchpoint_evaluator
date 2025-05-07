import pandas as pd
import json
from agents.standard_designer import standard_designer
from agents.web_explorer import web_explorer
from agents.evaluator import evaluator
from agents.reporter import reporter
from crewai import Task, Crew

# 1. 读取网页数据（从CSV）
df = pd.read_csv('data/structured_urls.csv')
sample_rows = df.head(5).to_dict(orient='records')  # 前5条用于测试

# 2. 设定标准制定任务（只需做一次）
example_urls = "\n".join([item['url'] for item in sample_rows])
task_define_standard = Task(
    description=f"""请访问以下网页，观察其中的用户互动要素，并总结网页“触点丰富度”的评估标准（如联系方式、二维码、客服等）。
网页列表：
{example_urls}

请输出：
- 建议评估维度（3-6个）
- 每个维度的判断方式（出现、明显程度）
- 最终打分机制建议
""",
    expected_output="一份结构化评估标准，格式为JSON，包含维度名、定义、评分方式",
    agent=standard_designer
)

# 3. 构建其他网页处理任务列表
tasks = [task_define_standard]
for item in sample_rows:
    url = item['url']
    domain = item['domain']
    year = item['year']

    # 网页内容提取任务
    task_extract = Task(
        description=f"访问网页：{url}，提取该页面的主要内容",
        expected_output="返回该网页中可读文本内容的字符串（不要包含HTML标签）",
        agent=web_explorer
    )

    # 网页内容评估任务
    task_evaluate = Task(
        description=(
            f"请根据由标准制定专家提供的评估维度，对以下网页内容进行分析，输出该网页的触点丰富度评分报告。\n"
            f"- 网页来源：{domain}（{year}）\n"
            f"- 网页地址：{url}\n"
            f"网页内容将通过上一步生成的文本提供。"
        ),
        expected_output=(
            "请返回结构化JSON，包括：\n"
            "- domain\n- year\n- url\n- score\n"
            "- summary（评价摘要）\n- touchpoints（每个维度的具体判定结果）"
        ),
        agent=evaluator
    )

    tasks.extend([task_extract, task_evaluate])

# 报告整合任务（后续执行,只做一次）
task_report = Task(
    description="请收集所有网页的评估结果，并整合成一份整体评估报告，包括汇总统计、整体趋势、共性问题和优秀实践。",
    expected_output="一份结构化JSON格式的报告，包含所有网页评估结果及总结。",
    agent=reporter
)

tasks.append(task_report)

# 4. 创建 Crew 并运行
crew = Crew(
    agents=[standard_designer, web_explorer, evaluator, reporter],
    tasks=tasks,
    verbose=True
)

result = crew.kickoff()

# 5. 输出结果保存为 JSON 文件
with open("result.json", "w", encoding="utf-8") as f:
    # json.dump(result, f, indent=2, ensure_ascii=False)
    json.dump({"result": str(result.output)}, f, indent=2, ensure_ascii=False)

print("✅ 分析完成，结果已保存到 result.json")