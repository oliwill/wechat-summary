"""
配置管理模块
基于环境变量的配置系统，支持多 LLM 提供商
"""
import os
import ast
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """配置类，从环境变量读取配置"""

    # ==================== LLM API 配置 ====================
    # 智谱 AI (推荐，性价比高)
    ZHIPU_API_KEY: Optional[str] = os.getenv("ZHIPU_API_KEY")
    ZHIPU_BASE_URL: str = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    ZHIPU_MODEL: str = os.getenv("ZHIPU_MODEL", "glm-4-flash")

    # DeepSeek
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # LLM 优先级（按顺序尝试）
    LLM_PROVIDERS: List[str] = ast.literal_eval(os.getenv("LLM_PROVIDERS", '["zhipu", "deepseek", "openai"]'))

    # ==================== 微信数据库配置 ====================
    # 微信数据库路径（可选，默认自动检测）
    WX_DB_PATH: Optional[str] = os.getenv("WX_DB_PATH")

    # 微信数据目录（Windows 默认路径）
    WX_DATA_DIR: str = os.getenv(
        "WX_DATA_DIR",
        os.path.expanduser("~/Documents/WeChat Files")
    )

    # ==================== 目标群聊配置 ====================
    # 目标群聊名称列表（支持 .env 预设）
    TARGET_ROOMS: List[str] = ast.literal_eval(os.getenv("TARGET_ROOMS", "[]"))

    # ==================== 消息过滤配置 ====================
    # 要处理的消息类型（1=文本）
    MSG_TYPES: List[int] = ast.literal_eval(os.getenv("MSG_TYPES", "[1]"))

    # 消息时间范围（每天的开始和结束时间）
    MSG_TIME_START: str = os.getenv("MSG_TIME_START", "00:00")
    MSG_TIME_END: str = os.getenv("MSG_TIME_END", "23:59")

    # 单次处理最大消息数（防止 token 溢出）
    MAX_MESSAGES: int = int(os.getenv("MAX_MESSAGES", "500"))

    # ==================== 总结配置 ====================
    # 时区
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Shanghai")

    # 报告输出目录
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./output")

    # ==================== 应用配置 ====================
    # 调试模式
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """
        获取可用的 LLM 配置（按优先级）

        Returns:
            包含 api_key, base_url, model 的字典

        Raises:
            ValueError: 如果没有可用的 LLM 配置
        """
        providers = {
            "zhipu": {
                "api_key": cls.ZHIPU_API_KEY,
                "base_url": cls.ZHIPU_BASE_URL,
                "model": cls.ZHIPU_MODEL,
                "name": "智谱 AI"
            },
            "deepseek": {
                "api_key": cls.DEEPSEEK_API_KEY,
                "base_url": cls.DEEPSEEK_BASE_URL,
                "model": cls.DEEPSEEK_MODEL,
                "name": "DeepSeek"
            },
            "openai": {
                "api_key": cls.OPENAI_API_KEY,
                "base_url": cls.OPENAI_BASE_URL,
                "model": cls.OPENAI_MODEL,
                "name": "OpenAI"
            }
        }

        # 按优先级查找可用的配置
        for provider in cls.LLM_PROVIDERS:
            config = providers.get(provider)
            if config and config["api_key"]:
                return config

        raise ValueError(
            "未找到可用的 LLM API Key，请配置以下至少一个："
            "ZHIPU_API_KEY、DEEPSEEK_API_KEY、OPENAI_API_KEY"
        )

    @classmethod
    def validate(cls) -> bool:
        """
        验证配置是否完整

        Returns:
            True 如果配置有效

        Raises:
            ValueError: 如果配置无效
        """
        # 验证 LLM 配置
        try:
            cls.get_llm_config()
        except ValueError as e:
            raise ValueError(f"LLM 配置无效: {e}")

        # 验证输出目录
        if cls.OUTPUT_DIR:
            os.makedirs(cls.OUTPUT_DIR, exist_ok=True)

        return True

    @classmethod
    def get_wx_db_path(cls, wx_id: str) -> str:
        """
        获取指定微信账号的数据库路径

        Args:
            wx_id: 微信账号 ID

        Returns:
            数据库文件的完整路径
        """
        if cls.WX_DB_PATH:
            return cls.WX_DB_PATH
        return os.path.join(cls.WX_DATA_DIR, wx_id, "MSG")

    @classmethod
    def print_config(cls):
        """打印当前配置（隐藏敏感信息）"""
        llm_config = cls.get_llm_config()
        print("=" * 50)
        print("当前配置:")
        print(f"  LLM 提供商: {llm_config['name']}")
        print(f"  LLM 模型: {llm_config['model']}")
        print(f"  API Key: {'*' * 20}{llm_config['api_key'][-4:] if llm_config['api_key'] else 'None'}")
        print(f"  目标群聊: {cls.TARGET_ROOMS if cls.TARGET_ROOMS else '交互选择'}")
        print(f"  时区: {cls.TIMEZONE}")
        print(f"  最大消息数: {cls.MAX_MESSAGES}")
        print("=" * 50)
