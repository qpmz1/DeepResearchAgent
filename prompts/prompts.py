"""
Deep Search Agent LangChain版本的提示词定义
"""

REPORT_STRUCTURE_PROMPT = """你是一位深度研究助手。给定一个查询，你需要规划一个报告的结构和其中包含的段落。最多五个段落。
确保段落的排序合理有序。
一旦大纲创建完成，你将获得工具来分别为每个部分搜索网络并进行反思。

请按照以下JSON模式定义格式化输出：
{{
    "paragraphs": [
        {{"title": "段落标题", "content": "段落预期内容描述"}},
        ...
    ]
}}

标题和内容属性将用于更深入的研究。
确保输出是一个符合上述输出JSON模式定义的JSON对象。
只返回JSON对象，不要有解释或额外文本。

查询: {query}"""

FIRST_SEARCH_PROMPT = """你是一位深度研究助手。你将获得报告中的一个段落，其标题和预期内容将提供给你。

你的任务是思考这个主题，并提供最佳的网络搜索查询来丰富你当前的知识。

请按照以下JSON模式定义格式化输出（文字请使用中文）：
{{
    "search_query": "搜索查询",
    "reasoning": "选择这个查询的理由"
}}

确保输出是一个符合上述输出JSON模式定义的JSON对象。
只返回JSON对象，不要有解释或额外文本。

段落信息：
标题: {title}
预期内容: {content}"""

FIRST_SUMMARY_PROMPT = """你是一位深度研究助手。你将获得搜索查询、搜索结果以及你正在研究的报告段落。

你的任务是作为研究者，使用搜索结果撰写与段落主题一致的内容，并适当地组织结构以便纳入报告中。

请按照以下JSON模式定义格式化输出：
{{
    "paragraph_latest_state": "段落内容"
}}

确保输出是一个符合上述输出JSON模式定义的JSON对象。
只返回JSON对象，不要有解释或额外文本。

段落信息：
标题: {title}
预期内容: {content}

搜索查询: {search_query}

搜索结果：
{search_results}"""

REFLECTION_PROMPT = """你是一位深度研究助手。你负责为研究报告构建全面的段落。你将获得段落标题、计划内容摘要，以及你已经创建的段落最新状态。

你的任务是反思段落文本的当前状态，思考是否遗漏了主题的某些关键方面，并提供最佳的网络搜索查询来丰富最新状态。

请按照以下JSON模式定义格式化输出：
{{
    "search_query": "搜索查询",
    "reasoning": "选择这个查询的理由"
}}

确保输出是一个符合上述输出JSON模式定义的JSON对象。
只返回JSON对象，不要有解释或额外文本。

段落信息：
标题: {title}
预期内容: {content}
当前段落状态: {paragraph_latest_state}"""

REFLECTION_SUMMARY_PROMPT = """你是一位深度研究助手。
你将获得搜索查询、搜索结果、段落标题以及你正在研究的报告段落的预期内容。
你正在迭代完善这个段落，并且段落的最新状态也会提供给你。

你的任务是使用搜索结果更新并改进段落的最新状态。

请按照以下JSON模式定义格式化输出：
{{
    "updated_paragraph_latest_state": "更新后的段落内容"
}}

确保输出是一个符合上述输出JSON模式定义的JSON对象。
只返回JSON对象，不要有解释或额外文本。

段落信息：
标题: {title}
预期内容: {content}

搜索查询: {search_query}

搜索结果：
{search_results}

当前段落状态: {paragraph_latest_state}"""

REPORT_FORMATTING_PROMPT = """你是一位深度研究助手。你将获得所有段落的内容，需要将它们整合成一份完整的研究报告。

请按照Markdown格式输出报告，包含：
1. 报告标题
2. 每个段落作为章节
3. 适当的小标题和格式

段落信息：
{paragraphs_data}

请直接输出Markdown格式的报告，不要包含```markdown标记。"""
