"""
微信消息获取模块 - Mock 版本（用于开发测试）
后续可以替换为真实的 Wechaty 或其他 API
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import time
import random


class WeChatManager:
    """微信管理器 - Mock 版本"""

    def __init__(self, use_mock: bool = True):
        """
        初始化微信管理器

        Args:
            use_mock: 是否使用 Mock 数据（默认 True）
        """
        self.use_mock = use_mock
        self.mock_messages = self._generate_mock_messages()
        self.message_count = 0

    async def login(self):
        """登录微信"""
        if self.use_mock:
            print("✅ Mock 模式：模拟微信登录成功")
        else:
            print("✅ 正在登录微信...")
            # 这里会调用真实的 Wechaty 登录
            # await self.client.start()
            pass

    async def get_messages(self, date_range: tuple) -> List[Dict[str, Any]]:
        """
        获取指定时间范围内的群消息

        Args:
            date_range: 时间范围 (start, end)

        Returns:
            消息列表
        """
        if self.use_mock:
            # 使用 Mock 数据
            return self._get_mock_messages(date_range)
        else:
            # 使用真实的 Wechaty
            # return await self.client.get_messages(date_range)
            return []

    async def stop(self):
        """停止监听"""
        if self.use_mock:
            print("❌ Mock 模式：模拟监听停止")
        else:
            # await self.client.stop()
            pass

    def _generate_mock_messages(self) -> List[Dict[str, Any]]:
        """
        生成模拟消息数据
        开发时使用，后续替换为真实的 API 调用
        """
        messages = []

        # 模拟美股群讨论内容
        message_templates = [
            {"sender": "用户A", "content": "大家看下AAPL今天的表现，感觉挺强的"},
            {"sender": "用户B", "content": "是的，苹果新发布会消息影响很大"},
            {"sender": "用户C", "content": "TSLA怎么样？"},
            {"sender": "用户D", "content": "特斯拉FSD进展不错，值得关注"},
            {"sender": "用户A", "content": "NVDA呢？"},
            {"sender": "用户B", "content": "英伟达数据中心业务增长很快，AI需求旺盛"},
            {"sender": "用户E", "content": "现在大盘怎么样？"},
            {"sender": "用户F", "content": "科技股整体表现不错，纳斯达克涨了1.5%"},
            {"sender": "用户G", "content": "各位对下周美联储加息预期怎么看？"},
            {"sender": "用户A", "content": "应该不会加息了，通胀已经控制住了"},
            {"sender": "用户B", "content": "AMD感觉被低估了，可以考虑建仓"},
            {"sender": "用户C", "content": "同意，GPU渠道库存消化得差不多了"},
            {"sender": "用户D", "content": "我看好周五的财报季表现"},
        ]

        # 生成 50-100 条消息
        num_messages = random.randint(50, 100)
        start_time = datetime(2024, 8, 20, 8, 0, 0)

        for i in range(num_messages):
            template = random.choice(message_templates)
            message_time = start_time + timedelta(minutes=i)
            messages.append({
                "timestamp": message_time.timestamp(),
                "sender": template["sender"],
                "content": template["content"]
            })

        return messages

    def _get_mock_messages(self, date_range: tuple) -> List[Dict[str, Any]]:
        """
        获取 Mock 消息

        Args:
            date_range: 时间范围

        Returns:
            时间范围内的消息
        """
        start_time, end_time = date_range

        filtered_messages = []
        for msg in self.mock_messages:
            msg_time = datetime.fromtimestamp(msg["timestamp"])

            # 检查时间范围
            if start_time <= msg_time <= end_time:
                filtered_messages.append(msg)

        return filtered_messages


# 测试代码
if __name__ == "__main__":
    import asyncio

    async def test():
        print("=" * 60)
        print("测试 Mock 微信管理器")
        print("=" * 60)

        # 创建 Mock 管理器
        wechat_mgr = WeChatManager(use_mock=True)

        # 登录
        await wechat_mgr.login()

        # 获取昨天 00:00-23:59 的消息
        from time_manager import TimeManager
        start_time, end_time = TimeManager.get_yesterday_range()

        print(f"\n获取消息：{start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}")
        messages = await wechat_mgr.get_messages((start_time, end_time))

        print(f"✅ 获取到 {len(messages)} 条消息")

        # 显示前 5 条
        print("\n前 5 条消息：")
        for msg in messages[:5]:
            print(f"  [{msg['timestamp']}] {msg['sender']}: {msg['content']}")

        # 停止
        await wechat_mgr.stop()

        print("\n✅ 测试完成！")

    asyncio.run(test())
