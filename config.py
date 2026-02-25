import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 微信配置
    WECHATY_PUPPET = os.getenv("WECHATY_PUPPET", "wechaty_puppet_wechat")
    WECHATY_PUPPET_SERVER_PORT = int(os.getenv("WECHATY_PUPPET_SERVER_PORT", "8080"))
    WECHATY_TOKEN = os.getenv("WECHATY_TOKEN")

    # LLM API 配置（优先使用 DeepSeek）
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # 群聊配置
    TARGET_GROUPS = eval(os.getenv("TARGET_GROUPS", '["美股交流群1", "美股策略群"]'))
    GROUP_IDS = eval(os.getenv("GROUP_IDS", '[]'))

    # 总结配置
    SUMMARY_TIME = os.getenv("SUMMARY_TIME", "09:00")
    TIMEZONE = os.getenv("TIMEZONE", "Asia/Shanghai")

    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.WECHATY_TOKEN:
            raise ValueError("WECHATY_TOKEN 未设置，请配置微信登录 token")
        if not cls.DEEPSEEK_API_KEY and not cls.OPENAI_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 和 OPENAI_API_KEY 至少需要配置一个")
        return True
