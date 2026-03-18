"""
搜索工具实现 - 使用Tavily搜索
"""

from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from tavily import TavilyClient
import os


def get_tavily_client(api_key: Optional[str] = None) -> TavilyClient:
    """获取Tavily客户端"""
    if api_key is None:
        api_key = os.getenv("TAVILY_API_KEY")
    return TavilyClient(api_key=api_key)


def tavily_search(
    query: str,
    api_key: Optional[str] = None,
    max_results: int = 5,
    timeout: int = 240
) -> List[Dict[str, Any]]:
    """
    执行Tavily搜索
    
    Args:
        query: 搜索查询
        api_key: Tavily API密钥
        max_results: 最大结果数量
        timeout: 超时时间
        
    Returns:
        搜索结果列表
    """
    try:
        client = get_tavily_client(api_key)
        response = client.search(
            query=query,
            max_results=max_results,
            include_raw_content=True,
            timeout=timeout
        )
        
        results = []
        if 'results' in response:
            for item in response['results']:
                results.append({
                    "title": item.get('title', ''),
                    "url": item.get('url', ''),
                    "content": item.get('content', ''),
                    "score": item.get('score')
                })
        
        return results
        
    except Exception as e:
        print(f"搜索错误: {str(e)}")
        return []


@tool
def search_tool(query: str) -> str:
    """
    搜索网络获取信息。输入搜索查询，返回相关搜索结果。
    
    Args:
        query: 搜索查询字符串
        
    Returns:
        搜索结果的格式化字符串
    """
    results = tavily_search(query)
    if not results:
        return "未找到相关搜索结果"
    
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_results.append(
            f"{i}. {result['title']}\n"
            f"   URL: {result['url']}\n"
            f"   内容: {result['content'][:500]}...\n"
        )
    
    return "\n".join(formatted_results)
