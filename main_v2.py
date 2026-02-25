#!/usr/bin/env python3
"""
微信群讨论总结工具 - 主程序
"""

import asyncio
import argparse
import sys
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_simple import Config
from time_manager import TimeManager
from llm_analyzer_v2 import LLMAnalyzer
from report_generator import ReportGenerator


async def main():
    """主程序"""
    parser = argparse.ArgumentParser(description='微信群讨论总结工具')
    parser.add_argument('--group', type=str, help='指定群聊名称或ID')
    parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)，默认为昨天')
    parser.add_argument('--test', action='store_true', help='仅测试模式，不发送 LLM 请求')
    args = parser.parse_args()

    try:
        # 验证配置
        Config.validate()
        print("✅ 配置验证通过")

        # 获取昨天的日期范围
        yesterday_start, yesterday_end = TimeManager.get_yesterday_range()

        # 如果指定了日期
        if args.date:
            try:
                target_date = datetime.strptime(args.date, "%Y-%m-%d")
                yesterday_start = datetime.combine(target_date.date(), datetime.min.time())
                yesterday_end = datetime.combine(target_date.date(), datetime.max.time())
                print(f"📅 指定日期：{args.date}")
            except ValueError:
                print(f"❌ 日期格式错误，请使用 YYYY-MM-DD 格式")
                sys.exit(1)

        print(f"⏰ 时间范围：{yesterday_start.strftime('%Y-%m-%d %H:%M')} - {yesterday_end.strftime('%H:%M')}")

        # 初始化 LLM 分析器
        if args.test:
            print("🔍 测试模式：使用模拟数据")
            analyzer = LLMAnalyzer("test", "https://test.com", model="glm-4.7-flash")
            # 使用测试模式时，我们用模拟数据
            from test_v2 import create_mock_messages
            messages = create_mock_messages()
        else:
            # 优先使用智谱 AI GLM，如果没有则使用 DeepSeek
            if Config.ZHIPU_API_KEY:
                print("🤖 使用智谱 AI GLM API")
                analyzer = LLMAnalyzer(Config.ZHIPU_API_KEY, Config.ZHIPU_BASE_URL, model="glm-4.7-flash")
            elif Config.DEEPSEEK_API_KEY:
                print("🤖 使用 DeepSeek API")
                analyzer = LLMAnalyzer(Config.DEEPSEEK_API_KEY, Config.DEEPSEEK_BASE_URL)
            elif Config.OPENAI_API_KEY:
                print("🤖 使用 OpenAI API")
                analyzer = LLMAnalyzer(Config.OPENAI_API_KEY, "https://api.openai.com/v1", model="gpt-3.5-turbo")
            else:
                print("❌ 未配置 LLM API Key")
                print("\n请选择以下方式之一：")
                print("1. 使用智谱 AI GLM：https://open.bigmodel.cn/")
                print("2. 使用 DeepSeek：https://platform.deepseek.com/")
                print("3. 使用 OpenAI：https://platform.openai.com/")
                sys.exit(1)

            # 如果不是测试模式，需要微信消息
            print("📥 正在获取微信消息...")

            # 这里需要导入微信管理器
            from wechat_manager import WeChatManager
            wechat_mgr = WeChatManager(Config.WECHATY_TOKEN, Config.GROUP_IDS)
            await wechat_mgr.login()
            messages = await wechat_mgr.get_messages((yesterday_start, yesterday_end))
            await wechat_mgr.stop()

        if not messages:
            print("⚠️  未找到消息")
            sys.exit(0)

        print(f"✅ 获取到 {len(messages)} 条消息")

        # 分析讨论
        print("🤖 正在分析讨论内容...")
        result = analyzer.analyze_discussions(messages, (yesterday_start, yesterday_end))

        if not result.get("success"):
            print(f"❌ 分析失败: {result.get('error')}")
            sys.exit(1)

        print(f"✅ 分析完成")

        # 生成报告
        report_gen = ReportGenerator()
        report = report_gen.generate(result, (yesterday_start, yesterday_end))

        # 打印报告
        report_gen.print_report(report)

        # 保存报告
        filepath = report_gen.save_report(report)
        print(f"\n✅ 报告已保存到：{filepath}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
