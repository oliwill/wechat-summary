"""
消息过滤模块
按时间、群组、消息类型过滤微信消息
"""
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta


class TimeFilter:
    """消息过滤器"""

    @staticmethod
    def filter_by_time(messages: List[Dict[str, Any]],
                       start: datetime,
                       end: datetime) -> List[Dict[str, Any]]:
        """
        按时间范围过滤消息

        Args:
            messages: 消息列表
            start: 开始时间
            end: 结束时间

        Returns:
            过滤后的消息列表
        """
        return [
            msg for msg in messages
            if start <= msg.get("timestamp", datetime.min) <= end
        ]

    @staticmethod
    def filter_by_room(messages: List[Dict[str, Any]],
                       room_ids: Set[str]) -> List[Dict[str, Any]]:
        """
        按群组过滤消息

        Args:
            messages: 消息列表
            room_ids: 群组 ID 集合

        Returns:
            过滤后的消息列表
        """
        return [
            msg for msg in messages
            if msg.get("room_id") in room_ids
        ]

    @staticmethod
    def filter_by_type(messages: List[Dict[str, Any]],
                       msg_types: List[int]) -> List[Dict[str, Any]]:
        """
        按消息类型过滤

        Args:
            messages: 消息列表
            msg_types: 消息类型列表（1=文本, 3=图片, etc.）

        Returns:
            过滤后的消息列表
        """
        msg_type_set = set(msg_types)
        return [
            msg for msg in messages
            if msg.get("type") in msg_type_set
        ]

    @staticmethod
    def filter_content(messages: List[Dict[str, Any]],
                       min_length: int = 1) -> List[Dict[str, Any]]:
        """
        过滤掉内容为空或过短的消息

        Args:
            messages: 消息列表
            min_length: 最小内容长度

        Returns:
            过滤后的消息列表
        """
        return [
            msg for msg in messages
            if len(msg.get("content", "").strip()) >= min_length
        ]

    @staticmethod
    def filter_system_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        过滤掉系统消息

        Args:
            messages: 消息列表

        Returns:
            过滤后的消息列表
        """
        return [
            msg for msg in messages
            if msg.get("type") != 10000  # 10000 是系统消息类型
        ]

    @staticmethod
    def sort_by_time(messages: List[Dict[str, Any]],
                     reverse: bool = False) -> List[Dict[str, Any]]:
        """
        按时间排序消息

        Args:
            messages: 消息列表
            reverse: 是否倒序（最新的在前）

        Returns:
            排序后的消息列表
        """
        return sorted(
            messages,
            key=lambda x: x.get("timestamp", datetime.min),
            reverse=reverse
        )

    @staticmethod
    def limit_messages(messages: List[Dict[str, Any]],
                       limit: int,
                       strategy: str = "recent") -> List[Dict[str, Any]]:
        """
        限制消息数量

        Args:
            messages: 消息列表
            limit: 最大数量
            strategy: 限制策略
                - "recent": 保留最近的消息
                - "oldest": 保留最早的消息
                - "sample": 均匀采样

        Returns:
            限制后的消息列表
        """
        if len(messages) <= limit:
            return messages

        if strategy == "recent":
            return messages[-limit:]
        elif strategy == "oldest":
            return messages[:limit]
        elif strategy == "sample":
            # 均匀采样
            step = len(messages) / limit
            indices = [int(i * step) for i in range(limit)]
            return [messages[i] for i in indices]
        else:
            return messages[-limit:]


class DateRange:
    """日期范围工具"""

    @staticmethod
    def today() -> tuple[datetime, datetime]:
        """获取今天的日期范围（00:00 - 23:59）"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = today
        end = today.replace(hour=23, minute=59, second=59)
        return start, end

    @staticmethod
    def yesterday() -> tuple[datetime, datetime]:
        """获取昨天的日期范围（00:00 - 23:59）"""
        yesterday = datetime.now() - timedelta(days=1)
        start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end = yesterday.replace(hour=23, minute=59, second=59)
        return start, end

    @staticmethod
    def this_week() -> tuple[datetime, datetime]:
        """获取本周的日期范围（周一 00:00 - 现在）"""
        now = datetime.now()
        # 计算本周一
        days_since_monday = now.weekday()
        monday = now - timedelta(days=days_since_monday)
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        return start, now

    @staticmethod
    def last_n_days(n: int) -> tuple[datetime, datetime]:
        """获取最近 N 天的日期范围"""
        now = datetime.now()
        start = (now - timedelta(days=n)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, now

    @staticmethod
    def specific_date(date_str: str) -> tuple[datetime, datetime]:
        """
        获取指定日期的范围

        Args:
            date_str: 日期字符串，格式如 "2025-02-25"

        Returns:
            (开始时间, 结束时间)
        """
        try:
            date = datetime.fromisoformat(date_str)
            start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = date.replace(hour=23, minute=59, second=59)
            return start, end
        except ValueError:
            raise ValueError(f"日期格式无效: {date_str}，请使用 YYYY-MM-DD 格式")

    @staticmethod
    def custom(start_str: str, end_str: str) -> tuple[datetime, datetime]:
        """
        自定义日期范围

        Args:
            start_str: 开始日期，格式 "YYYY-MM-DD"
            end_str: 结束日期，格式 "YYYY-MM-DD"

        Returns:
            (开始时间, 结束时间)
        """
        start = datetime.fromisoformat(start_str).replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.fromisoformat(end_str).replace(hour=23, minute=59, second=59)
        return start, end

    @staticmethod
    def format_range(start: datetime, end: datetime) -> str:
        """格式化日期范围为字符串"""
        if start.date() == end.date():
            return start.strftime("%Y-%m-%d")
        return f"{start.strftime('%Y-%m-%d')} 至 {end.strftime('%Y-%m-%d')}"
