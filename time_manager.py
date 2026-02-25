from datetime import datetime, timedelta, timezone
from typing import List, Dict
import os

class TimeManager:
    """时间管理类，处理日期和时间段"""

    @staticmethod
    def get_yesterday_range() -> tuple:
        """获取昨天的日期范围"""
        tz = timezone.utc
        today = datetime.now(tz)
        yesterday = today - timedelta(days=1)
        yesterday_start = datetime.combine(yesterday.date(), datetime.min.time())
        yesterday_end = datetime.combine(yesterday.date(), datetime.max.time())
        return yesterday_start, yesterday_end

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """格式化时间戳"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def is_between(date: datetime, start: datetime, end: datetime) -> bool:
        """检查时间是否在范围内"""
        return start <= date <= end

    @staticmethod
    def parse_time(time_str: str) -> datetime:
        """解析时间字符串"""
        return datetime.strptime(time_str, "%H:%M")
