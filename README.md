# 🔍 DeepResearchAgent

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-green?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**一个基于 LangChain 框架实现的智能深度研究 Agent**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用示例](#-使用示例) • [配置说明](#-配置说明) • [架构设计](#-架构设计)

</div>

---

## 📖 项目简介

DeepResearchAgent 是一个智能深度研究助手，能够针对给定主题进行多轮搜索、反思和总结，最终生成结构化的研究报告。该系统模拟了人类研究者的工作流程，通过迭代式搜索和反思不断完善研究内容。

### 🎯 核心能力

- **智能结构规划**：自动将研究主题分解为多个相关段落
- **多轮深度搜索**：针对每个段落进行多轮网络搜索
- **反思迭代机制**：通过自我反思发现知识盲点并补充搜索
- **结构化报告生成**：自动整合所有内容生成 Markdown 格式报告

---

## ✨ 功能特性

| 特性 | 描述 |
|------|------|
| 🤖 **多模型支持** | 支持 DeepSeek、OpenAI 等多种 LLM 提供商 |
| 🔍 **智能搜索** | 集成 Tavily 搜索引擎，获取实时网络信息 |
| 🔄 **反思迭代** | 自动反思研究内容，发现并填补知识盲区 |
| 📝 **报告生成** | 自动生成结构清晰、内容详实的 Markdown 报告 |
| ⚙️ **灵活配置** | 支持通过环境变量或配置文件自定义参数 |
| 📊 **状态管理** | 基于 Pydantic 的状态管理，确保数据一致性 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 或 conda

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/qpmz1/DeepResearchAgent.git
cd DeepResearchAgent
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API 密钥**

创建 `.env` 文件：
```bash
# DeepSeek API（推荐，性价比高）
DEEPSEEK_API_KEY=your_deepseek_api_key

# 或使用 OpenAI
OPENAI_API_KEY=your_openai_api_key

# Tavily 搜索 API
TAVILY_API_KEY=your_tavily_api_key

# 选择 LLM 提供商（deepseek 或 openai）
DEFAULT_LLM_PROVIDER=deepseek
```

4. **运行示例**
```bash
python example.py
```

---

## 💡 使用示例

### 基本使用

```python
from agent import DeepSearchAgent
from config import load_config

# 加载配置
config = load_config()

# 初始化 Agent
agent = DeepSearchAgent(config)

# 执行研究
query = "人工智能在医疗领域的应用有哪些？"
report = agent.research(query, save_report=True)

print(report)
```

### 自定义配置

```python
from agent import DeepSearchAgent

# 自定义配置
config = {
    "DEEPSEEK_API_KEY": "your_api_key",
    "TAVILY_API_KEY": "your_tavily_key",
    "DEFAULT_LLM_PROVIDER": "deepseek",
    "DEEPSEEK_MODEL": "deepseek-chat",
    "MAX_REFLECTIONS": 3,              # 反思次数
    "SEARCH_RESULTS_PER_QUERY": 5,     # 每次搜索结果数
    "OUTPUT_DIR": "reports"            # 输出目录
}

agent = DeepSearchAgent(config)
report = agent.research("量子计算的最新进展")
```

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `DEEPSEEK_API_KEY` | 是* | - | DeepSeek API 密钥 |
| `OPENAI_API_KEY` | 是* | - | OpenAI API 密钥 |
| `TAVILY_API_KEY` | 是 | - | Tavily 搜索 API 密钥 |
| `DEFAULT_LLM_PROVIDER` | 否 | `deepseek` | LLM 提供商 |
| `DEEPSEEK_MODEL` | 否 | `deepseek-chat` | DeepSeek 模型名称 |
| `OPENAI_MODEL` | 否 | `gpt-4o-mini` | OpenAI 模型名称 |
| `MAX_REFLECTIONS` | 否 | `2` | 最大反思迭代次数 |
| `SEARCH_RESULTS_PER_QUERY` | 否 | `3` | 每次搜索返回结果数 |
| `OUTPUT_DIR` | 否 | `reports` | 报告输出目录 |

> *根据 `DEFAULT_LLM_PROVIDER` 选择填写对应的 API 密钥

### 获取 API 密钥

| 服务 | 链接 | 说明 |
|------|------|------|
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com/) | 推荐，性价比高 |
| OpenAI | [platform.openai.com](https://platform.openai.com/) | GPT 系列模型 |
| Tavily | [tavily.com](https://tavily.com/) | 搜索引擎 API |

---

## 🏗️ 架构设计

### 项目结构

```
langchain_agent/
├── agent.py              # Agent 主逻辑
├── config.py             # 配置管理
├── state.py              # 状态定义
├── example.py            # 使用示例
├── requirements.txt      # 依赖列表
│
├── nodes/                # 节点模块
│   ├── __init__.py
│   └── nodes.py          # 各处理节点实现
│
├── prompts/              # 提示词模块
│   ├── __init__.py
│   └── prompts.py        # Prompt 模板定义
│
└── tools/                # 工具模块
    ├── __init__.py
    └── search.py         # 搜索工具实现
```

### 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                      DeepResearchAgent                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  步骤 1: 生成报告结构                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  输入: 用户查询                                       │    │
│  │  处理: LLM 规划报告结构和段落                         │    │
│  │  输出: 段落列表 (标题 + 预期内容)                     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  步骤 2: 处理每个段落                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  2.1 首次搜索: 生成搜索查询 → 执行搜索               │    │
│  │  2.2 首次总结: 基于搜索结果撰写段落内容              │    │
│  │  2.3 反思循环 (最多 N 次):                           │    │
│  │      ├── 反思: 分析内容不足之处                      │    │
│  │      ├── 搜索: 针对性补充搜索                        │    │
│  │      └── 更新: 整合新信息更新段落                    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  步骤 3: 生成最终报告                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  输入: 所有段落内容                                   │    │
│  │  处理: LLM 整合并格式化                               │    │
│  │  输出: Markdown 格式研究报告                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件

#### 1. AgentState（状态管理）
```python
class AgentState(BaseModel):
    query: str                          # 研究查询
    paragraphs: List[Paragraph]         # 段落列表
    max_reflections: int                # 最大反思次数
    search_results_per_query: int       # 每次搜索结果数
```

#### 2. 节点函数
- `create_report_structure_node()` - 生成报告结构
- `create_first_search_node()` - 首次搜索
- `create_first_summary_node()` - 首次总结
- `create_reflection_node()` - 反思分析
- `create_reflection_summary_node()` - 反思总结
- `create_report_formatting_node()` - 报告格式化

---

## 📊 示例输出

运行 `python example.py` 后，将在 `reports/` 目录下生成研究报告：

```markdown
# 人工智能在医疗健康领域的应用与前沿研究报告

## 医学影像分析与辅助诊断

人工智能在医学影像分析领域的应用已经取得了显著进展...

## 药物研发与发现

AI 技术正在革新传统的药物研发流程...

## 个性化治疗与精准医疗

基于 AI 的精准医疗正在改变传统的治疗模式...

...
```

---

## 🔧 高级用法

### 自定义提示词

可以通过修改 `prompts/prompts.py` 来自定义各个阶段的提示词：

```python
REPORT_STRUCTURE_PROMPT = """你是一位深度研究助手..."""

FIRST_SEARCH_PROMPT = """你是一位深度研究助手..."""

# 更多提示词...
```

### 扩展搜索工具

可以在 `tools/` 目录下添加更多搜索工具：

```python
def custom_search(query: str, max_results: int = 3) -> List[Dict]:
    """自定义搜索实现"""
    # 实现你的搜索逻辑
    return results
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [LangChain](https://www.langchain.com/) - 强大的 LLM 应用开发框架
- [DeepSeek](https://www.deepseek.com/) - 高性价比的大语言模型
- [Tavily](https://tavily.com/) - 专为 AI 设计的搜索引擎

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by DeepResearchAgent Team

</div>
