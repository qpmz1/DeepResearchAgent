"""
基本使用示例 - LangChain版本
演示如何使用Deep Search Agent (LangChain版)进行深度搜索
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from langchain_agent import DeepSearchAgent, load_config, print_config


def basic_example():
    """基本使用示例"""
    print("=" * 60)
    print("Deep Search Agent (LangChain版) - 基本使用示例")
    print("=" * 60)
    
    try:
        print("正在加载配置...")
        config = load_config()
        print_config(config)
        
        print("\n正在初始化Agent...")
        agent = DeepSearchAgent(config)
        
        query = "人工智能在医疗领域的应用有哪些？"
        print(f"\n开始研究: {query}")
        
        final_report = agent.research(query, save_report=True)
        
        print("\n" + "=" * 60)
        print("研究完成！最终报告预览:")
        print("=" * 60)
        print(final_report[:500] + "..." if len(final_report) > 500 else final_report)
        
        progress = agent.get_progress_summary()
        print(f"\n进度信息:")
        print(f"- 总段落数: {progress['total_paragraphs']}")
        print(f"- 已完成段落: {progress['completed_paragraphs']}")
        print(f"- 完成进度: {progress['progress_percentage']:.1f}%")
        print(f"- 是否完成: {progress['is_completed']}")
        
    except Exception as e:
        print(f"示例运行失败: {str(e)}")
        print("请检查：")
        print("1. 是否安装了所有依赖")
        print("2. 是否设置了必要的API密钥")
        print("3. 网络连接是否正常")


if __name__ == "__main__":
    basic_example()
