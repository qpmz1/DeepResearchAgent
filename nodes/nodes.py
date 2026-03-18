"""
节点实现 - 使用LangChain的Runnable接口
"""

import json
from typing import Dict, Any, List, Optional
from langchain_core.runnables import RunnableLambda
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from ..state import AgentState, Paragraph, ResearchState
from ..tools import tavily_search
from ..prompts import (
    REPORT_STRUCTURE_PROMPT,
    FIRST_SEARCH_PROMPT,
    FIRST_SUMMARY_PROMPT,
    REFLECTION_PROMPT,
    REFLECTION_SUMMARY_PROMPT,
    REPORT_FORMATTING_PROMPT,
)


def clean_json_output(output: str) -> str:
    """清理LLM输出中的JSON"""
    output = output.strip()
    if output.startswith("```json"):
        output = output[7:]
    if output.startswith("```"):
        output = output[3:]
    if output.endswith("```"):
        output = output[:-3]
    return output.strip()


def parse_json_safely(text: str) -> Dict[str, Any]:
    """安全解析JSON"""
    try:
        cleaned = clean_json_output(text)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}


def generate_report_structure(state: AgentState, llm: BaseChatModel) -> AgentState:
    """生成报告结构节点"""
    print(f"\n[步骤 1] 生成报告结构...")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REPORT_STRUCTURE_PROMPT),
        ("human", "{query}")
    ])
    
    chain = prompt | llm | StrOutputParser() # 解析JSON输出
    response = chain.invoke({"query": state.query})
    
    result = parse_json_safely(response)
    paragraphs_data = result.get("paragraphs", [])
    
    if not paragraphs_data:
        paragraphs_data = [
            {"title": "概述", "content": f"对'{state.query}'的总体概述"},
            {"title": "详细分析", "content": f"深入分析'{state.query}'的相关内容"}
        ]
    
    for para_data in paragraphs_data:
        state.add_paragraph(
            title=para_data.get("title", ""),
            content=para_data.get("content", "")
        )
    
    print(f"报告结构已生成，共 {len(state.paragraphs)} 个段落:")
    for i, paragraph in enumerate(state.paragraphs, 1):
        print(f"  {i}. {paragraph.title}")
    
    return state


def initial_search(state: AgentState, llm: BaseChatModel, paragraph_index: int, 
                   api_key: str, max_results: int = 3) -> AgentState:
    """初始搜索节点"""
    paragraph = state.paragraphs[paragraph_index]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", FIRST_SEARCH_PROMPT),
        ("human", "")
    ])
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "title": paragraph.title,
        "content": paragraph.content
    })
    
    result = parse_json_safely(response)
    search_query = result.get("search_query", paragraph.title)
    reasoning = result.get("reasoning", "")
    
    print(f"  - 搜索查询: {search_query}")
    print(f"  - 推理: {reasoning}")
    
    print("  - 执行网络搜索...")
    search_results = tavily_search(search_query, api_key=api_key, max_results=max_results)
    
    if search_results:
        print(f"  - 找到 {len(search_results)} 个搜索结果")
        for j, result in enumerate(search_results, 1):
            print(f"    {j}. {result['title'][:50]}...")
    else:
        print("  - 未找到搜索结果")
    
    paragraph.research.add_search_results(search_query, search_results)
    
    return state


def initial_summary(state: AgentState, llm: BaseChatModel, paragraph_index: int,
                    max_content_length: int = 20000) -> AgentState:
    """初始总结节点"""
    paragraph = state.paragraphs[paragraph_index]
    
    search_history = paragraph.research.search_history
    if not search_history:
        paragraph.research.latest_summary = "未能获取搜索结果"
        return state
    
    latest_search = search_history[-1]
    search_results_text = f"查询: {latest_search.query}\n\n"
    for i, search in enumerate(search_history, 1):
        content = search.content[:max_content_length] if len(search.content) > max_content_length else search.content
        search_results_text += f"{i}. {search.title}\nURL: {search.url}\n内容: {content}\n\n"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", FIRST_SUMMARY_PROMPT),
        ("human", "")
    ])
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "title": paragraph.title,
        "content": paragraph.content,
        "search_query": latest_search.query,
        "search_results": search_results_text
    })
    
    result = parse_json_safely(response)
    summary = result.get("paragraph_latest_state", response)
    
    paragraph.research.latest_summary = summary
    print("  - 成功生成初始总结")
    
    return state


def reflection_search(state: AgentState, llm: BaseChatModel, paragraph_index: int,
                      api_key: str, max_results: int = 3) -> AgentState:
    """反思搜索节点"""
    paragraph = state.paragraphs[paragraph_index]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REFLECTION_PROMPT),
        ("human", "")
    ])
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "title": paragraph.title,
        "content": paragraph.content,
        "paragraph_latest_state": paragraph.research.latest_summary
    })
    
    result = parse_json_safely(response)
    search_query = result.get("search_query", "")
    reasoning = result.get("reasoning", "")
    
    if not search_query:
        print("  - 反思未生成新的搜索查询")
        return state
    
    print(f"  - 反思搜索查询: {search_query}")
    print(f"  - 反思推理: {reasoning}")
    
    search_results = tavily_search(search_query, api_key=api_key, max_results=max_results)
    
    if search_results:
        print(f"  - 找到 {len(search_results)} 个新搜索结果")
        paragraph.research.add_search_results(search_query, search_results)
    
    return state


def reflection_summary(state: AgentState, llm: BaseChatModel, paragraph_index: int,
                       max_content_length: int = 20000) -> AgentState:
    """反思总结节点"""
    paragraph = state.paragraphs[paragraph_index]
    
    search_history = paragraph.research.search_history
    if len(search_history) < 2:
        return state
    
    latest_search = search_history[-1]
    search_results_text = f"查询: {latest_search.query}\n\n"
    for i, search in enumerate(search_history[-3:], 1):
        content = search.content[:max_content_length] if len(search.content) > max_content_length else search.content
        search_results_text += f"{i}. {search.title}\nURL: {search.url}\n内容: {content}\n\n"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REFLECTION_SUMMARY_PROMPT),
        ("human", "")
    ])
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "title": paragraph.title,
        "content": paragraph.content,
        "search_query": latest_search.query,
        "search_results": search_results_text,
        "paragraph_latest_state": paragraph.research.latest_summary
    })
    
    result = parse_json_safely(response)
    updated_summary = result.get("updated_paragraph_latest_state", response)
    
    paragraph.research.latest_summary = updated_summary
    paragraph.research.increment_reflection()
    print(f"  - 反思总结完成 (第 {paragraph.research.reflection_iteration} 次反思)")
    
    return state


def format_report(state: AgentState, llm: BaseChatModel) -> AgentState:
    """格式化最终报告"""
    print(f"\n[步骤 3] 格式化最终报告...")
    
    paragraphs_data = []
    for paragraph in state.paragraphs:
        paragraphs_data.append({
            "title": paragraph.title,
            "paragraph_latest_state": paragraph.research.latest_summary
        })
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REPORT_FORMATTING_PROMPT),
        ("human", "")
    ])
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "paragraphs_data": json.dumps(paragraphs_data, ensure_ascii=False, indent=2)
    })
    
    state.final_report = response
    print("最终报告已生成")
    
    return state
