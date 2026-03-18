"""
Deep Search Agent - LangChain版本主类
使用LangChain框架实现深度搜索Agent
"""

import os
from typing import Optional
from datetime import datetime

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .state import AgentState
from .nodes import (
    generate_report_structure,
    initial_search,
    initial_summary,
    reflection_search,
    reflection_summary,
    format_report,
)
from .config import Config, load_config, print_config


class DeepSearchAgent:
    """Deep Search Agent - LangChain版本"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        初始化Agent
        
        Args:
            config: 配置对象，如果不提供则自动加载
        """
        self.config = config or load_config()
        self.llm = self._initialize_llm()
        self.state = AgentState()
        
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        print(f"Deep Search Agent (LangChain版) 已初始化")
        print(f"使用LLM: {self.config.default_llm_provider} - {self._get_model_name()}")
    
    def _initialize_llm(self) -> BaseChatModel:
        """初始化LLM"""
        if self.config.default_llm_provider == "deepseek":
            return ChatOpenAI(
                api_key=self.config.deepseek_api_key,
                base_url="https://api.deepseek.com",
                model=self.config.deepseek_model,
                temperature=0.7,
            )
        elif self.config.default_llm_provider == "openai":
            return ChatOpenAI(
                api_key=self.config.openai_api_key,
                model=self.config.openai_model,
                temperature=0.7,
            )
        else:
            raise ValueError(f"不支持的LLM提供商: {self.config.default_llm_provider}")
    
    def _get_model_name(self) -> str:
        """获取当前模型名称"""
        if self.config.default_llm_provider == "deepseek":
            return self.config.deepseek_model
        return self.config.openai_model
    
    def research(self, query: str, save_report: bool = True) -> str:
        """
        执行深度研究
        
        Args:
            query: 研究查询
            save_report: 是否保存报告
            
        Returns:
            最终报告内容
        """
        print(f"\n{'='*60}")
        print(f"开始深度研究: {query}")
        print(f"{'='*60}")
        
        try:
            self.state = AgentState(query=query)
            
            self.state = generate_report_structure(self.state, self.llm)
            
            self._process_paragraphs()
            
            self.state = format_report(self.state, self.llm)
            
            if save_report:
                self._save_report()
            
            print(f"\n{'='*60}")
            print("深度研究完成！")
            print(f"{'='*60}")
            
            return self.state.final_report
            
        except Exception as e:
            print(f"研究过程中发生错误: {str(e)}")
            raise e
    
    def _process_paragraphs(self):
        """处理所有段落"""
        total = len(self.state.paragraphs)
        
        for i in range(total):
            print(f"\n[步骤 2.{i+1}] 处理段落: {self.state.paragraphs[i].title}")
            print("-" * 50)
            
            self.state = initial_search(
                self.state, self.llm, i,
                self.config.tavily_api_key,
                self.config.max_search_results
            )
            
            self.state = initial_summary(
                self.state, self.llm, i,
                self.config.max_content_length
            )
            
            for reflection_num in range(self.config.max_reflections):
                print(f"\n  [反思 {reflection_num + 1}/{self.config.max_reflections}]")
                
                self.state = reflection_search(
                    self.state, self.llm, i,
                    self.config.tavily_api_key,
                    self.config.max_search_results
                )
                
                self.state = reflection_summary(
                    self.state, self.llm, i,
                    self.config.max_content_length
                )
            
            self.state.paragraphs[i].research.mark_completed()
            
            progress = (i + 1) / total * 100
            print(f"段落处理完成 ({progress:.1f}%)")
    
    def _save_report(self):
        """保存报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.md"
        filepath = os.path.join(self.config.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.state.final_report)
        
        print(f"\n报告已保存到: {filepath}")
    
    def get_progress_summary(self) -> dict:
        """获取进度摘要"""
        return self.state.get_progress_summary()
