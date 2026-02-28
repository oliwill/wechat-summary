"""报告生成模块"""
import os
from typing import List, Dict, Any
from datetime import datetime


class ReportGenerator:
    """报告生成器"""

    def __init__(self):
        pass

    def generate(self, analysis_result: Dict[str, Any],
                 date_range: tuple) -> str:
        """
        生成 Markdown 格式的总结报告

        Args:
            analysis_result: LLM 分析结果
            date_range: 时间范围 (start, end)

        Returns:
            Markdown 格式的报告
        """
        start_time, end_time = date_range
        topics = analysis_result.get("topics", [])

        # 构建报告
        report = self._build_report(topics, start_time, end_time)
        return report

    def _build_report(self, topics: List[Dict[str, Any]],
                      start_time: datetime, end_time: datetime) -> str:
        """构建 Markdown 报告"""

        lines = []
        lines.append("# 群讨论总结")
        lines.append(
            f"\n**时间范围：** {start_time.strftime('%Y-%m-%d')} "
            f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        )
        lines.append(f"**总结日期：** {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("")

        # 总览
        lines.append("## 📊 讨论概览")
        lines.append(f"共讨论了 {len(topics)} 个话题")
        lines.append("")

        # 话题列表
        for idx, topic in enumerate(topics, 1):
            title = topic.get('title', '未命名话题')
            lines.append(f"## 📌 话题 {idx}: {title}")
            lines.append("")

            # 讨论内容
            discussion = topic.get('discussion', '')
            if discussion:
                lines.append("### 💬 讨论内容")
                lines.append(discussion)
                lines.append("")

            # 结论
            conclusion = topic.get('conclusion', '')
            if conclusion:
                lines.append("### ✅ 结论")
                lines.append(conclusion)
                lines.append("")

            # 股票信息
            stocks = topic.get('stocks', [])
            if stocks:
                lines.append("### 📈 具体个股")
                for stock in stocks:
                    name = stock.get('name', '未知')
                    code = stock.get('code', '')
                    view = stock.get('view', '')
                    lines.append(f"**{name} {code}**")
                    if view:
                        lines.append(f"- {view}")
                    lines.append("")
            else:
                lines.append("### 📈 具体个股")
                lines.append("*未提及具体个股*")
                lines.append("")

        return "\n".join(lines)

    def save_report(self, report: str, filename: str = None):
        """
        保存报告到文件

        Args:
            report: Markdown 报告内容
            filename: 文件名，默认为时间戳命名的文件
        """
        if filename is None:
            filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        else:
            if not filename.endswith('.md'):
                filename += '.md'

        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        return filepath

    def print_report(self, report: str):
        """打印报告到控制台"""
        print(report)
