#!/usr/bin/env python3
"""
微信群消息总结工具 - 主程序

基于微信电脑版本地数据库的合规方案
"""
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from wx_db_reader import WxDbReader, WxAccount
from time_filter import TimeFilter, DateRange
from llm_analyzer import LLMAnalyzer
from report_generator import ReportGenerator


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="微信群消息总结工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                    # 使用 .env 预设配置
  python main.py --room "美股群"     # 指定群组
  python main.py --date 2025-02-25  # 指定日期
  python main.py --list-rooms       # 列出所有群组
  python main.py --yesterday        # 昨天的消息
        """
    )

    parser.add_argument(
        "--room", "-r",
        help="目标群组名称（可多次指定）",
        action="append",
        dest="rooms"
    )

    parser.add_argument(
        "--date", "-d",
        help="指定日期 (YYYY-MM-DD)",
        type=str
    )

    parser.add_argument(
        "--list-rooms", "-l",
        help="列出所有群聊并退出",
        action="store_true"
    )

    parser.add_argument(
        "--yesterday", "-y",
        help="分析昨天的消息（默认）",
        action="store_true"
    )

    parser.add_argument(
        "--today", "-t",
        help="分析今天的消息",
        action="store_true"
    )

    parser.add_argument(
        "--output", "-o",
        help="输出文件路径",
        type=str
    )

    parser.add_argument(
        "--wxid",
        help="指定微信账号 ID",
        type=str
    )

    parser.add_argument(
        "--config",
        help="显示当前配置",
        action="store_true"
    )

    return parser.parse_args()


def select_account(accounts: list) -> WxAccount:
    """交互式选择微信账号"""
    if not accounts:
        print("❌ 未找到微信账号")
        print("\n请确保：")
        print("  1. 已安装微信电脑版")
        print("  2. 已登录账号")
        print("  3. 至少登录过一次（数据目录已创建）")
        sys.exit(1)

    if len(accounts) == 1:
        return accounts[0]

    print("\n检测到多个微信账号：")
    for i, acc in enumerate(accounts, 1):
        print(f"  [{i}] {acc.wxid}")

    while True:
        try:
            choice = input("\n请选择账号 [1]: ").strip()
            if not choice:
                return accounts[0]
            index = int(choice) - 1
            if 0 <= index < len(accounts):
                return accounts[index]
            print("❌ 无效选择")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ 取消")
            sys.exit(1)


def select_rooms(chatrooms: list, target_rooms: list = None) -> list:
    """选择目标群聊"""
    if not chatrooms:
        print("❌ 未找到群聊")
        sys.exit(1)

    # 如果预设了目标群组，尝试匹配
    if target_rooms:
        matched = []
        for room in chatrooms:
            for target in target_rooms:
                if target in room.get("name", "") or target in room.get("wxid", ""):
                    matched.append(room)
                    break
        if matched:
            return matched

    print(f"\n检测到 {len(chatrooms)} 个群聊：")
    for i, room in enumerate(chatrooms[:20], 1):  # 最多显示 20 个
        name = room.get("name") or room.get("nickname") or room.get("wxid", "")
        print(f"  [{i}] {name}")

    if len(chatrooms) > 20:
        print(f"  ... 还有 {len(chatrooms) - 20} 个群聊")

    while True:
        try:
            choice = input("\n请选择群组 (如: 1,3,5 或 all): ").strip()
            if choice.lower() == "all":
                return chatrooms
            if not choice:
                return [chatrooms[0]]

            indices = [int(x.strip()) - 1 for x in choice.split(",")]
            selected = [chatrooms[i] for i in indices if 0 <= i < len(chatrooms)]
            if selected:
                return selected
            print("❌ 无效选择")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ 取消")
            sys.exit(1)


def list_rooms(reader: WxDbReader):
    """列出所有群聊"""
    chatrooms = reader.get_chatrooms()

    print(f"\n共找到 {len(chatrooms)} 个群聊：\n")
    for i, room in enumerate(chatrooms, 1):
        wxid = room.get("wxid", "")
        name = room.get("name") or room.get("nickname", "")
        print(f"  [{i:2d}] {name}")
        if wxid and wxid != name:
            print(f"       ID: {wxid}")

    reader.close()


def analyze_messages(messages: list, date_range: tuple,
                     llm_config: dict, output_file: str = None):
    """分析消息并生成报告"""
    if not messages:
        print("❌ 没有找到符合条件的消息")
        return

    print(f"\n📊 找到 {len(messages)} 条消息")

    # 初始化 LLM 分析器
    print(f"\n🤖 使用 {llm_config['name']} ({llm_config['model']}) 分析...")
    analyzer = LLMAnalyzer(
        api_key=llm_config['api_key'],
        base_url=llm_config['base_url'],
        model=llm_config['model']
    )

    # 分析
    result = analyzer.analyze_discussions(messages, date_range)

    if not result.get("success"):
        print(f"\n❌ LLM 分析失败: {result.get('error')}")
        sys.exit(1)

    # 生成报告
    generator = ReportGenerator()
    report = generator.generate(result['data'], date_range)

    # 保存报告
    if output_file is None:
        start_time, _ = date_range
        date_str = start_time.strftime("%Y-%m-%d")
        output_file = f"summary_{date_str}.md"

    # 确保输出目录存在
    output_dir = Config.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ 报告已保存: {output_path}")

    # 打印使用情况
    usage = result.get('usage', {})
    if usage:
        print(f"\n📈 Token 使用: {usage.get('total_tokens', 0)}")


def main():
    """主函数"""
    args = parse_args()

    # 显示配置
    if args.config:
        try:
            Config.print_config()
            return
        except Exception as e:
            print(f"❌ 配置错误: {e}")
            sys.exit(1)

    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("\n请检查 .env 文件配置")
        sys.exit(1)

    # 获取 LLM 配置
    llm_config = Config.get_llm_config()

    # 获取微信账号列表
    try:
        accounts = WxDbReader.get_wx_accounts(Config.WX_DATA_DIR)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 选择账号
    if args.wxid:
        # 查找指定账号
        account = next((a for a in accounts if a.wxid == args.wxid), None)
        if not account:
            print(f"❌ 未找到微信账号: {args.wxid}")
            sys.exit(1)
    else:
        account = select_account(accounts)

    print(f"\n✅ 使用账号: {account.wxid}")

    # 初始化数据库读取器
    try:
        reader = WxDbReader(account)
        reader.connect_db()
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n提示：请确保已在微信电脑版中备份聊天记录到电脑")
        sys.exit(1)

    # 列出群聊
    if args.list_rooms:
        list_rooms(reader)
        return

    # 获取日期范围
    if args.date:
        start, end = DateRange.specific_date(args.date)
    elif args.today:
        start, end = DateRange.today()
    else:
        start, end = DateRange.yesterday()

    # 获取目标群组
    target_rooms = args.rooms or Config.TARGET_ROOMS

    if target_rooms:
        print(f"\n🎯 目标群组: {', '.join(target_rooms)}")
    else:
        # 交互式选择群组
        chatrooms = reader.get_chatrooms()
        selected_rooms = select_rooms(chatrooms, target_rooms)
        target_rooms = [r.get("wxid") for r in selected_rooms]

    # 读取消息
    print(f"\n📅 时间范围: {DateRange.format_range(start, end)}")
    print("📖 正在读取消息...")

    all_messages = []
    for room_id in target_rooms:
        messages = reader.get_messages(
            room_wxid=room_id,
            start_time=start,
            end_time=end,
            msg_types=Config.MSG_TYPES,
            limit=Config.MAX_MESSAGES
        )
        all_messages.extend(messages)

    reader.close()

    # 过滤消息
    all_messages = TimeFilter.filter_content(all_messages, min_length=1)
    all_messages = TimeFilter.filter_system_messages(all_messages)
    all_messages = TimeFilter.sort_by_time(all_messages)

    # 限制消息数量
    if len(all_messages) > Config.MAX_MESSAGES:
        all_messages = TimeFilter.limit_messages(
            all_messages,
            Config.MAX_MESSAGES,
            strategy="recent"
        )

    # 分析并生成报告
    analyze_messages(all_messages, (start, end), llm_config, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
        sys.exit(0)
