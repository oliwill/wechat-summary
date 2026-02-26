#!/usr/bin/env python3
"""
测试脚本 - 模拟数据测试
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from time_manager import TimeManager
from llm_analyzer_v2 import LLMAnalyzer
from report_generator import ReportGenerator


# 模拟数据
def create_mock_messages():
    """创建模拟消息"""
    messages = []
    start_time = datetime(2024, 8, 20, 9, 0, 0)
    timestamps = [
        (start_time + timedelta(minutes=i)).timestamp()
        for i in range(100)
    ]

    messages_data = [
        {"sender": "用户A", "content": "大家看下AAPL今天的表现，感觉挺强的"},
        {"sender": "用户B", "content": "是的，苹果新发布会消息影响很大"},
        {"sender": "用户C", "content": "TSLA怎么样？"},
        {"sender": "用户D", "content": "特斯拉 FSD 进展不错，值得关注"},
        {"sender": "用户A", "content": "NVDA 呢？"},
        {"sender": "用户B", "content": "英伟达数据中心业务增长很快，AI需求旺盛"},
        {"sender": "用户E", "content": "现在大盘怎么样？"},
        {"sender": "用户F", "content": "科技股整体表现不错，纳斯达克涨了 1.5%"},
        {"sender": "用户G", "content": "各位对下周美联储加息预期怎么看？"},
        {"sender": "用户A", "content": "应该不会加息了，通胀已经控制住了"},
        {"sender": "用户B", "content": "AMD 感觉被低估了，可以考虑建仓"},
        {"sender": "用户C", "content": "同意，GPU 渠道库存消化得差不多了"},
        {"sender": "用户D", "content": "我看好周五的财报季表现"},
    ]

    for i in range(len(messages_data)):
        messages.append({
            "timestamp": timestamps[i],
            "sender": messages_data[i]["sender"],
            "content": messages_data[i]["content"]
        })

    return messages


def test_time_manager():
    """测试时间管理"""
    print("=== 测试时间管理 ===")
    start, end = TimeManager.get_yesterday_range()
    print(f"昨天开始: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"昨天结束: {end.strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def test_analyzer():
    """测试 LLM 分析器"""
    print("=== 测试 LLM 分析器 ===")

    # 优先使用智谱 AI GLM，如果没有则使用 DeepSeek
    api_key = "test-key"  # 这个不会被真正调用

    # 使用测试模式（不调用真实 API）
    analyzer = LLMAnalyzer(api_key, "https://test.com", model="glm-4-flash")

    # 创建模拟数据
    messages = create_mock_messages()
    start, end = TimeManager.get_yesterday_range()

    print(f"创建的模拟消息数: {len(messages)}")
    print(f"时间范围: {start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}")

    # 分析
    result = analyzer.analyze_discussions(messages, (start, end))

    if result.get("success"):
        print(f"✅ 分析成功")
        topics = result["data"]["topics"]
        print(f"   提取的话题数: {len(topics)}")

        for idx, topic in enumerate(topics, 1):
            print(f"\n   话题 {idx}: {topic.get('title', '未命名')}")
            print(f"   股票数: {len(topic.get('stocks', []))}")

    else:
        print(f"❌ 分析失败: {result.get('error')}")

    print()


def test_report_generator():
    """测试报告生成"""
    print("=== 测试报告生成 ===")

    mock_result = {
        "topics": [
            {
                "title": "苹果公司财报讨论",
                "discussion": "大家关注 AAPL 今天的股价表现，新发布会消息影响很大，机构普遍看好 Q4 表现。",
                "conclusion": "苹果财报季预期积极，iPhone 16 销量值得期待。",
                "stocks": [
                    {"name": "苹果", "code": "AAPL", "view": "股价预期上涨，机构看好 Q4 表现"}
                ]
            },
            {
                "title": "特斯拉和英伟达讨论",
                "discussion": "TSLA FSD 进展不错，NVDA 数据中心业务增长很快，AI 需求旺盛。",
                "conclusion": "科技股整体表现不错，纳斯达克涨了 1.5%。",
                "stocks": [
                    {"name": "特斯拉", "code": "TSLA", "view": "FSD 进展不错，值得关注"},
                    {"name": "英伟达", "code": "NVDA", "view": "数据中心业务增长快，AI 需求旺盛"}
                ]
            },
            {
                "title": "美联储加息预期讨论",
                "discussion": "下周美联储加息预期，大家讨论认为应该不会加息了。",
                "conclusion": "通胀控制良好，预计不会加息。",
                "stocks": [
                    {"name": "美联储", "code": "FED", "view": "货币政策转向宽松"}
                ]
            },
            {
                "title": "AMD 建仓建议",
                "discussion": "AMD 被低估，GPU 渠道库存消化得差不多了。",
                "conclusion": "看好 AMD 后续表现，可考虑建仓。",
                "stocks": [
                    {"name": "AMD", "code": "AMD", "view": "被低估，值得建仓"}
                ]
            }
        ]
    }

    start, end = TimeManager.get_yesterday_range()

    report_gen = ReportGenerator()
    report = report_gen.generate(mock_result, (start, end))

    print("生成的报告预览：")
    print("=" * 50)
    print(report[:500] + "...")
    print("=" * 50)
    print()


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("微信群讨论总结工具 - 测试脚本（智谱 AI 版）")
    print("=" * 60)
    print()

    test_time_manager()
    test_analyzer()
    test_report_generator()

    print("✅ 所有测试完成！")


if __name__ == "__main__":
    main()
