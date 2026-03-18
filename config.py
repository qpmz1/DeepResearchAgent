"""
配置管理
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Config(BaseModel):
    """配置类"""
    deepseek_api_key: str = ""
    openai_api_key: str = ""
    tavily_api_key: str = ""
    default_llm_provider: str = "deepseek"
    deepseek_model: str = "deepseek-chat"
    openai_model: str = "gpt-4o-mini"
    max_reflections: int = 2
    max_search_results: int = 3
    max_content_length: int = 20000
    output_dir: str = "reports"


def load_config() -> Config:
    """加载配置"""
    config = Config(
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        tavily_api_key=os.getenv("TAVILY_API_KEY", ""),
        default_llm_provider=os.getenv("DEFAULT_LLM_PROVIDER", "deepseek"),
        deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        max_reflections=int(os.getenv("MAX_REFLECTIONS", "2")),
        max_search_results=int(os.getenv("SEARCH_RESULTS_PER_QUERY", "3")),
        max_content_length=int(os.getenv("SEARCH_CONTENT_MAX_LENGTH", "20000")),
        output_dir=os.getenv("OUTPUT_DIR", "reports"),
    )
    return config


def print_config(config: Config):
    """打印配置信息"""
    print(f"配置信息:")
    print(f"  - LLM提供商: {config.default_llm_provider}")
    print(f"  - DeepSeek模型: {config.deepseek_model}")
    print(f"  - OpenAI模型: {config.openai_model}")
    print(f"  - 最大反思次数: {config.max_reflections}")
    print(f"  - 每次搜索结果数: {config.max_search_results}")
    print(f"  - 输出目录: {config.output_dir}")
