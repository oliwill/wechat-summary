from typing import List, Dict, Any
from datetime import datetime
import os
import json
import sys
from openai import OpenAI

class LLMAnalyzer:
    """LLM 分析器，负责分析群消息"""

    def __init__(self, api_key: str, base_url: str = "https://open.bigmodel.cn/api/paas/v4", model: str = "glm-4-flash"):
        """
        初始化 LLM 分析器

        Args:
            api_key: API Key
            base_url: API base URL
            model: 模型名称（智谱 AI: glm-4-flash/glm-4-plus/glm-4-air，DeepSeek: deepseek-chat，OpenAI: gpt-3.5-turbo/gpt-4o-mini）
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def analyze_discussions(self, messages: List[Dict[str, Any]], date_range: tuple) -> Dict[str, Any]:
        """
        分析群讨论内容

        Args:
            messages: 群消息列表，每个消息包含 sender, content, timestamp
            date_range: 时间范围 (start, end)

        Returns:
            分析结果
        """
        start_time, end_time = date_range

        # 构建提示词
        prompt = self._build_prompt(messages, start_time, end_time)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的美股群讨论分析助手。请仔细分析群里的讨论内容，按照要求提取信息。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000,
                timeout=60.0  # 增加超时时间到 60 秒
            )

            # 解析响应
            result_text = response.choices[0].message.content
            result = self._parse_response(result_text)

            return {
                "success": True,
                "data": result,
                "usage": response.usage.model_dump()
            }

        except Exception as e:
            error_msg = str(e)
            print(f"❌ LLM API 错误: {error_msg}")

            # 尝试提取错误信息
            if "401" in error_msg:
                return {
                    "success": False,
                    "error": "API Key 无效或未配置，请检查 .env 文件中的 API Key"
                }
            elif "403" in error_msg:
                return {
                    "success": False,
                    "error": "API Key 无权限或余额不足"
                }
            elif "429" in error_msg:
                return {
                    "success": False,
                    "error": "API 调用次数超限，请稍后再试"
                }
            else:
                return {
                    "success": False,
                    "error": error_msg
                }

    def _build_prompt(self, messages: List[Dict[str, Any]], start_time: datetime, end_time: datetime) -> str:
        """构建 LLM 提示词"""

        # 筛选指定时间范围内的消息
        filtered_messages = [
            msg for msg in messages
            if self._is_time_in_range(msg.get("timestamp", 0), start_time, end_time)
        ]

        # 格式化消息
        formatted_messages = []
        for msg in filtered_messages[:500]:  # 限制消息数量，避免超 token
            formatted_messages.append(
                f"[{msg.get('timestamp', '')}] {msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
            )

        messages_text = "\n".join(formatted_messages) if formatted_messages else "无消息"

        prompt = f"""
请分析以下美股群讨论内容（时间范围：{start_time.strftime('%Y-%m-%d %H:%M')} 至 {end_time.strftime('%H:%M')}），提取信息：

讨论主题（列出所有话题及其主题）：
讨论内容（每个话题的详细讨论内容和结论）：
具体个股（每个话题提及的股票名称、代码及对个股的看法）：

---
{messages_text}
---

请按照以下 JSON 格式返回结果（不要有任何其他文字）：
{{
    "topics": [
        {{
            "title": "话题标题",
            "discussion": "详细讨论内容",
            "conclusion": "结论",
            "stocks": [
                {{
                    "name": "股票名称",
                    "code": "股票代码",
                    "view": "对个股的看法"
                }}
            ]
        }}
    ]
}}
"""

        return prompt

    def _is_time_in_range(self, timestamp: int, start: datetime, end: datetime) -> bool:
        """检查时间戳是否在范围内"""
        try:
            msg_time = datetime.fromtimestamp(timestamp)
            return start <= msg_time <= end
        except:
            return False

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析 LLM 响应"""
        try:
            # 尝试直接解析 JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # 如果解析失败，尝试提取 JSON 部分
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                return {
                    "topics": [
                        {
                            "title": "未解析",
                            "discussion": response_text,
                            "conclusion": "",
                            "stocks": []
                        }
                    ]
                }
