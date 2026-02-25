# 微信群讨论自动总结工具 - 项目概述

## 一句话介绍

一个可以自动总结美股微信群讨论内容的工具，每天早上自动生成结构化报告。

## 核心功能

- 📊 自动提取群讨论主题
- 💬 记录详细讨论内容和结论
- 📈 识别讨论中的股票及观点
- 🤖 使用 LLM 智能分析
- 📅 自动按时间筛选（昨天 00:00-23:59）
- 🤖 支持跨天讨论处理
- 📝 生成 Markdown 格式报告

## 技术栈

```
Python 3.8+
├── Wechaty          # 微信机器人框架
├── OpenAI SDK       # LLM API 客户端
├── python-dotenv    # 环境变量管理
└── lxml            # XML 解析
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 WECHATY_TOKEN 和 DEEPSEEK_API_KEY

# 3. 运行测试
python test.py

# 4. 运行主程序
python main.py
```

## 成本预估

### DeepSeek API（推荐）
- **每日成本**：约 0.15 元
- **每月成本**：约 4.5 元

### OpenAI API
- **每日成本**：约 1.0 元
- **每月成本**：约 30 元

## 文件结构

```
wechat-summary/
├── main.py              # 主程序
├── test.py              # 测试脚本
├── config.py            # 配置管理
├── time_manager.py      # 时间管理
├── wechat_manager.py    # 微信消息获取
├── llm_analyzer.py      # LLM 分析器
├── report_generator.py  # 报告生成
├── requirements.txt     # 依赖列表
├── .env.example         # 配置示例
├── README.md            # 完整文档
├── QUICKSTART.md        # 快速入门
└── SUMMARY.md           # 项目总结
```

## 使用场景

- 📈 美股群交流总结
- 💰 投资复盘记录
- 📰 市场动态收集
- 🎯 关键信息提取

## 项目特点

✅ **功能完整**：满足所有需求
✅ **使用简单**：5 分钟快速上手
✅ **成本低廉**：每月几块钱
✅ **文档齐全**：有完整的文档和测试
✅ **易于扩展**：模块化设计

## 文档索引

- **README.md**：完整使用文档（推荐先读）
- **QUICKSTART.md**：5 分钟快速入门
- **SUMMARY.md**：项目总结和费用预估

## 联系方式

如有问题，请查看文档或提交 Issue。

---

**开发时间**：2025-08-21
**开发者**：Abo
**用户**：包子
