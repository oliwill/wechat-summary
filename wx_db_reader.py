"""
微信数据库读取模块
使用 PyWxDump 读取微信电脑版本地数据库
"""
import os
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess


class WxAccount:
    """微信账号信息"""

    def __init__(self, wxid: str, name: str, mobile: str = "", mail: str = "",
                 file_path: str = "", key: bytes = b""):
        self.wxid = wxid
        self.name = name
        self.mobile = mobile
        self.mail = mail
        self.file_path = file_path  # 微信数据目录
        self.key = key  # 数据库解密密钥

    def __repr__(self):
        return f"WxAccount(wxid={self.wxid}, name={self.name})"


class WxDbReader:
    """微信数据库读取器

    使用 PyWxDump 读取微信电脑版本地数据库
    """

    # 微信消息类型映射
    MSG_TYPES = {
        1: "文本",
        3: "图片",
        34: "语音",
        43: "视频",
        47: "表情",
        49: "链接/文件",
        10000: "系统消息",
    }

    def __init__(self, account: WxAccount):
        """
        初始化数据库读取器

        Args:
            account: 微信账号信息
        """
        self.account = account
        self.db_path = os.path.join(account.file_path, "MSG")
        self.conn = None

    @classmethod
    def get_wx_accounts(cls, wx_dir: str = None) -> List[WxAccount]:
        """
        获取系统中所有微信账号信息

        Args:
            wx_dir: 微信数据目录，默认为 ~/Documents/WeChat Files

        Returns:
            微信账号列表
        """
        if wx_dir is None:
            wx_dir = os.path.expanduser("~/Documents/WeChat Files")

        if not os.path.exists(wx_dir):
            raise FileNotFoundError(
                f"未找到微信数据目录: {wx_dir}\n"
                f"请确保已安装微信电脑版并登录过账号"
            )

        accounts = []
        for item in os.listdir(wx_dir):
            wxid_path = os.path.join(wx_dir, item)
            # 跳过非目录文件
            if not os.path.isdir(wxid_path):
                continue
            # 跳过 All Users、Applet、WMPF 等系统目录
            if item in ["All Users", "Applet", "WMPF", "msg"]:
                continue

            # 检查是否存在 MSG 目录（微信数据目录的标志）
            msg_path = os.path.join(wxid_path, "MSG")
            if not os.path.exists(msg_path):
                continue

            # 创建账号对象（密钥和详细信息稍后获取）
            account = WxAccount(
                wxid=item,
                name=item,  # 暂时使用 wxid 作为名称
                file_path=wxid_path
            )
            accounts.append(account)

        return accounts

    @classmethod
    def get_db_key(cls, wxid: str = None) -> List[Dict]:
        """
        使用 pywxdump 获取数据库解密密钥

        Args:
            wxid: 指定微信账号 ID，为 None 时获取所有账号

        Returns:
            账号信息列表，包含密钥
        """
        try:
            # 使用 pywxdump-mini 读取微信信息
            result = subprocess.run(
                ["python", "-m", "pywxdump", "bias", "addr"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                # 尝试另一种方式
                result = subprocess.run(
                    ["pywxdump", "info"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            # 解析输出（实际使用时需要根据 pywxdump 的输出格式调整）
            # 这里提供一个简化的实现框架
            return cls._parse_wx_info(result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            # pywxdump 不可用时的降级方案
            print(f"⚠️ 无法自动获取密钥: {e}")
            print("提示: 请手动输入密钥或确保微信正在运行")
            return []

    @classmethod
    def _parse_wx_info(cls, output: str) -> List[Dict]:
        """解析 pywxdump 输出"""
        # 这里需要根据 pywxdump-mini 的实际输出格式来解析
        # 暂时返回空列表，实际使用时需要完善
        return []

    def connect_db(self) -> bool:
        """
        连接到微信数据库

        Returns:
            是否连接成功
        """
        db_file = os.path.join(self.db_path, "MSG.db")
        if not os.path.exists(db_file):
            # 尝试查找 MicroMsg.db
            db_file = os.path.join(self.db_path, "MicroMsg.db")

        if not os.path.exists(db_file):
            raise FileNotFoundError(
                f"未找到数据库文件: {db_file}\n"
                f"请确保已在微信电脑版中备份聊天记录到电脑"
            )

        try:
            # 如果有密钥，使用 SQLCipher 解密
            # 否则尝试直接连接（某些版本微信可能未加密）
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = sqlite3.Row
            return True
        except sqlite3.DatabaseError as e:
            if "encrypted" in str(e).lower() or "file is not a database" in str(e).lower():
                raise RuntimeError(
                    f"数据库已加密，需要解密密钥: {e}\n"
                    f"请使用 pywxdump 获取密钥: pip install pywxdump-mini"
                )
            raise

    def get_chatrooms(self) -> List[Dict[str, str]]:
        """
        获取群聊列表

        Returns:
            群聊列表，每个元素包含 {wxid, name, nickname}
        """
        if not self.conn:
            self.connect_db()

        cursor = self.conn.cursor()

        # 尝试不同的表名（不同版本微信可能不同）
        tables = [
            ("ChatRoom", "ChatRoomInfo"),
            ("ChatRoomInfo",),
        ]

        chatrooms = []

        for table_set in tables:
            try:
                # 构建查询
                query_parts = []
                params = []

                for table in table_set:
                    query_parts.append(f"SELECT * FROM {table}")

                # 尝试第一个表
                query = query_parts[0]
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    # 解析行数据
                    row_dict = dict(row)
                    chatroom = {
                        "wxid": row_dict.get("ChatRoomName", "") or row_dict.get("wxid", ""),
                        "name": row_dict.get("DisplayName", "") or row_dict.get("nickname", ""),
                        "nickname": row_dict.get("nickname", ""),
                    }
                    # 过滤掉空值
                    if chatroom["wxid"]:
                        chatrooms.append(chatroom)

                if chatrooms:
                    break

            except sqlite3.OperationalError:
                continue

        return chatrooms

    def get_messages(self, room_wxid: str = None,
                     start_time: datetime = None,
                     end_time: datetime = None,
                     msg_types: List[int] = None,
                     limit: int = 500) -> List[Dict[str, Any]]:
        """
        获取消息

        Args:
            room_wxid: 群聊 wxid，为 None 时获取所有消息
            start_time: 开始时间
            end_time: 结束时间
            msg_types: 消息类型列表，None 表示所有类型
            limit: 最大消息数

        Returns:
            消息列表
        """
        if not self.conn:
            self.connect_db()

        cursor = self.conn.cursor()

        # 构建查询
        query = "SELECT * FROM MSG"
        conditions = []
        params = []

        if room_wxid:
            conditions.append("strTalker = ?")
            params.append(room_wxid)

        if start_time:
            conditions.append("CreateTime >= ?")
            params.append(int(start_time.timestamp() * 1000))

        if end_time:
            conditions.append("CreateTime <= ?")
            params.append(int(end_time.timestamp() * 1000))

        if msg_types:
            placeholders = ",".join(["?" for _ in msg_types])
            conditions.append(f"MsgType IN ({placeholders})")
            params.extend(msg_types)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY CreateTime DESC LIMIT ?"
        params.append(limit)

        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
            # 表名可能不同，尝试其他可能的表名
            if "MSG" in str(e):
                return self._get_messages_fallback(
                    cursor, room_wxid, start_time, end_time, msg_types, limit
                )
            raise

        messages = []
        for row in rows:
            row_dict = dict(row)
            msg = self._parse_message(row_dict)
            if msg:
                messages.append(msg)

        # 按时间正序排列
        messages.reverse()

        return messages

    def _get_messages_fallback(self, cursor, room_wxid: str,
                               start_time: datetime, end_time: datetime,
                               msg_types: List[int], limit: int) -> List[Dict]:
        """备用消息获取方法"""
        # 这里可以实现备用逻辑，例如尝试其他表名
        return []

    def _parse_message(self, row: Dict) -> Optional[Dict[str, Any]]:
        """
        解析单条消息

        Args:
            row: 数据库行数据

        Returns:
            解析后的消息字典
        """
        try:
            msg_type = row.get("MsgType", 0)

            # 只处理文本消息或指定类型
            if msg_type not in [1] + (self.MSG_TYPES.keys() if hasattr(self, 'MSG_TYPES') else []):
                return None

            # 解析时间戳（微信使用毫秒级时间戳）
            create_time = row.get("CreateTime", 0)
            if isinstance(create_time, str):
                create_time = int(create_time)

            # 转换时间戳
            if create_time > 1000000000000:  # 毫秒级
                create_time = create_time / 1000

            return {
                "msg_id": row.get("localId", ""),
                "type": msg_type,
                "type_name": self.MSG_TYPES.get(msg_type, f"类型{msg_type}"),
                "content": row.get("StrContent", "") or "",
                "sender": row.get("strTalker", ""),
                "room_id": row.get("strTalker", ""),
                "timestamp": datetime.fromtimestamp(create_time),
                "is_sender": row.get("isSender", 0) == 1,
            }

        except Exception as e:
            if os.getenv("DEBUG") == "true":
                print(f"解析消息失败: {e}, row: {row}")
            return None

    def get_contacts(self) -> List[Dict[str, str]]:
        """
        获取联系人列表

        Returns:
            联系人列表
        """
        if not self.conn:
            self.connect_db()

        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT * FROM Contact")
            rows = cursor.fetchall()

            contacts = []
            for row in rows:
                row_dict = dict(row)
                contact = {
                    "wxid": row_dict.get("UserName", ""),
                    "nickname": row_dict.get("NickName", ""),
                    "remark": row_dict.get("Remark", ""),
                }
                if contact["wxid"]:
                    contacts.append(contact)

            return contacts

        except sqlite3.OperationalError:
            return []

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None


def format_messages_for_llm(messages: List[Dict[str, Any]]) -> str:
    """
    将消息格式化为 LLM 可处理的文本

    Args:
        messages: 消息列表

    Returns:
        格式化后的文本
    """
    lines = []
    for msg in messages:
        timestamp = msg.get("timestamp", datetime.now())
        time_str = timestamp.strftime("%H:%M")
        sender = msg.get("sender", "Unknown")
        content = msg.get("content", "")

        # 尝试提取发送者名称（群消息格式通常是 "wxid:\n昵称"）
        if ":" in sender:
            sender = sender.split(":")[-1]

        lines.append(f"[{time_str}] {sender}: {content}")

    return "\n".join(lines)
