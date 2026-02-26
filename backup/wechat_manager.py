from typing import List, Dict
from datetime import datetime
import asyncio
from wechaty import Wechaty, Message, Contact
from wechaty.user import Message as WechatyMessage

class WeChatManager:
    """微信管理器，负责获取群消息"""

    def __init__(self, token: str, group_ids: List[str] = None):
        self.token = token
        self.group_ids = group_ids or []
        self.client = None
        self.message_queue = []

    async def login(self):
        """登录微信"""
        from wechaty import Wechaty
        from wechaty_puppet_wechat import WechatyPuppetWechat

        self.client = Wechaty(WechatyPuppetWechat())
        await self.client.init()
        print("✅ 微信登录成功")

    async def get_messages(self, date_range: tuple) -> List[Dict[str, Any]]:
        """
        获取指定时间范围内的群消息

        Args:
            date_range: 时间范围 (start, end)

        Returns:
            消息列表，每个消息包含 sender, content, timestamp
        """
        self.message_queue = []

        # 监听消息
        await self.client.on('message', self._on_message)

        # 获取所有消息
        await self.client.start()

        # 等待获取足够消息
        await asyncio.sleep(5)  # 给予一些时间接收消息

        # 筛选时间范围内的消息
        start_time, end_time = date_range
        filtered_messages = [
            msg for msg in self.message_queue
            if self._is_time_in_range(msg.get('timestamp', 0), start_time, end_time)
        ]

        return filtered_messages

    async def _on_message(self, msg: WechatyMessage):
        """处理接收到的消息"""
        # 获取消息时间
        try:
            # wechaty 的消息时间可能需要转换
            timestamp = msg.timestamp()
            sender = msg.talker().name()
            content = msg.text()

            # 如果是群消息
            if msg.room():
                room = msg.room()
                room_name = room.topic()
                sender = f"{sender} (在 {room_name})"

            message_data = {
                "timestamp": timestamp,
                "sender": sender,
                "content": content
            }

            self.message_queue.append(message_data)

        except Exception as e:
            print(f"处理消息时出错: {e}")

    def _is_time_in_range(self, timestamp: int, start: datetime, end: datetime) -> bool:
        """检查时间戳是否在范围内"""
        try:
            msg_time = datetime.fromtimestamp(timestamp)
            return start <= msg_time <= end
        except:
            return False

    async def stop(self):
        """停止监听"""
        if self.client:
            await self.client.stop()
            print("❌ 微信监听已停止")
