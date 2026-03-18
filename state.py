"""
状态管理 - 使用Pydantic定义状态数据结构
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SearchRecord(BaseModel):
    """单个搜索记录"""
    query: str = ""
    url: str = ""
    title: str = ""
    content: str = ""
    score: Optional[float] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ResearchState(BaseModel):
    """段落研究过程的状态"""
    search_history: List[SearchRecord] = Field(default_factory=list)
    latest_summary: str = ""
    reflection_iteration: int = 0
    is_completed: bool = False
    
    def add_search_results(self, query: str, results: List[Dict[str, Any]]):
        """批量添加搜索结果"""
        for result in results:
            search = SearchRecord(
                query=query,
                url=result.get("url", ""),
                title=result.get("title", ""),
                content=result.get("content", ""),
                score=result.get("score")
            )
            self.search_history.append(search)
    
    def increment_reflection(self):
        """增加反思次数"""
        self.reflection_iteration += 1
    
    def mark_completed(self):
        """标记为完成"""
        self.is_completed = True


class Paragraph(BaseModel):
    """报告段落"""
    title: str
    content: str
    research: ResearchState = Field(default_factory=ResearchState)


class AgentState(BaseModel):
    """Agent整体状态"""
    query: str = ""
    report_title: str = ""
    paragraphs: List[Paragraph] = Field(default_factory=list)
    final_report: str = ""
    current_paragraph_index: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    def add_paragraph(self, title: str, content: str):
        """添加段落"""
        self.paragraphs.append(Paragraph(title=title, content=content))
        self.update_timestamp()
    
    def update_timestamp(self):
        """更新时间戳"""
        self.updated_at = datetime.now().isoformat()
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """获取进度摘要"""
        total = len(self.paragraphs)
        completed = sum(1 for p in self.paragraphs if p.research.is_completed)
        return {
            "total_paragraphs": total,
            "completed_paragraphs": completed,
            "progress_percentage": (completed / total * 100) if total > 0 else 0,
            "is_completed": completed == total and total > 0
        }
