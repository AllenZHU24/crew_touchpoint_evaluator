from crewai.tools import tool

@tool("Web Reader")
def web_reader_tool(url: str) -> str:
    """访问网页并提取清晰可读的正文内容"""
    import requests
    from bs4 import BeautifulSoup
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.get_text(separator="\n").strip()
    except Exception as e:
        return f"[ERROR] 网页访问失败: {str(e)}"