"""
LLM 分析模块
使用 LLM API 分析微信群消息
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from openai import OpenAI


class LLMAnalyzer:
    """LLM 分析器，支持多提供商"""

    def __init__(self, api_key: str, base_url: str, model: str = "glm-4-flash"):
        """
        初始化 LLM 分析器

        Args:
            api_key: API Key
            base_url: API Base URL
            model: 模型名称
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def analyze_discussions(self, messages: List[Dict[str, Any]],
                            date_range: tuple,
                            system_prompt: str = None) -> Dict[str, Any]:
        """
        分析群讨论内容

        Args:
            messages: 群消息列表
            date_range: 时间范围 (start, end)
            system_prompt: 自定义系统提示词

        Returns:
            包含 success, data, usage 的字典
        """
        start_time, end_time = date_range

        # 构建提示词
        prompt = self._build_prompt(messages, start_time, end_time)

        # 默认系统提示词（美股群分析）
        if system_prompt is None:
            system_prompt = (
                "你是一个专业的群讨论分析助手。"
                "请仔细分析群里的讨论内容，按照要求提取结构化信息。"
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000,
                timeout=60.0
            )

            # 解析响应
            result_text = response.choices[0].message.content
            result = self._parse_response(result_text)

            return {
                "success": True,
                "data": result,
                "usage": response.usage.model_dump() if hasattr(response, 'usage') else {}
            }

        except Exception as e:
            error_msg = str(e)

            # 错误分类
            if "401" in error_msg:
                return {
                    "success": False,
                    "error": "API Key 无效或未配置"
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

    def _build_prompt(self, messages: List[Dict[str, Any]],
                      start_time: datetime, end_time: datetime) -> str:
        """构建 LLM 提示词"""

        # 格式化消息
        formatted_messages = []
        for msg in messages[:500]:  # 限制消息数量
            timestamp = msg.get("timestamp")
            if timestamp:
                if isinstance(timestamp, datetime):
                    time_str = timestamp.strftime("%H:%M")
                elif isinstance(timestamp, str):
                    time_str = timestamp.split(" ")[-1][:5]
                else:
                    time_str = "??:??"
            else:
                time_str = "??:??"

            sender = msg.get("sender", "Unknown")
            content = msg.get("content", "")

            # 清理发送者名称
            if "\n" in sender:
                sender = sender.split("\n")[-1]

            formatted_messages.append(f"[{time_str}] {sender}: {content}")

        messages_text = "\n".join(formatted_messages) if formatted_messages else "无消息"

        prompt = f"""
请分析以下群讨论内容（时间范围：{start_time.strftime('%Y-%m-%d %H:%M')} 至 {end_time.strftime('%H:%M')}），提取信息：

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
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass

            # 解析完全失败，返回原始文本
            return {
                "topics": [
                    {
                        "title": "未解析",
                        "discussion": response_text[:500] + "..." if len(response_text) > 500 else response_text,
                        "conclusion": "",
                        "stocks": []
                    }
                ]
            }
