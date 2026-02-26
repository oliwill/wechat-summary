# 群讨论自动总结工具

基于微信电脑版本地数据库的群消息总结工具，零封号风险，合规安全。

[![GitHub](https://img.shields.io/badge/GitHub-微信%20群%20总结-blue)](https://github.com/oliwill/wechat-summary)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 功能特点

- 📊 自动分析群消息，提取讨论主题
- 💬 详细记录讨论内容和结论
- 📈 识别讨论中的个股及观点
- 🤖 基于 LLM 智能分析（支持智谱 AI、DeepSeek、OpenAI）
- 📅 按时间范围筛选消息
- 📝 生成 Markdown 格式报告
- ✅ **零封号风险**（使用微信官方备份功能）
- 🔒 **合规安全**（仅分析个人数据）

## 核心变化

| 原方案 | 新方案 |
|--------|--------|
| Wechaty（网页协议） | 微信电脑版 MSG.db |
| 实时监听 | 本地数据库读取 |
| 高封号风险 | 零风险合规 |

## 技术栈

- **Python 3.8+**
- **PyWxDump** - 微信数据库解密
- **OpenAI SDK** - LLM API 客户端
- **SQLite** - 微信数据库读取

## 快速开始

### 1. 安装依赖

```bash
cd wechat-summary
pip install pywxdump-mini python-dotenv openai lxml
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# LLM API 配置（推荐智谱 AI）
ZHIPU_API_KEY=your-zhipu-api-key-here
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# 目标群组（可选，运行时可交互选择）
TARGET_ROOMS=["美股交流群1", "美股策略群"]
```

### 3. 微信电脑版备份

首次使用前，需要在微信电脑版中备份聊天记录：

1. 打开微信电脑版
2. 设置 → 聊天记录备份 → 备份到电脑
3. 备份完成后，数据存储在 `~/Documents/WeChat Files/[wxid]/MSG/`

### 4. 获取 LLM API Key

**智谱 AI（推荐）**：
1. 访问 https://open.bigmodel.cn/
2. 使用 GitHub 登录
3. 创建 API Key

## 使用方法

### 列出所有群聊

```bash
python main.py --list-rooms
```

### 分析昨天的消息

```bash
python main.py
```

### 指定群组和日期

```bash
python main.py --room "美股群" --date 2025-02-25
```

### 分析今天的消息

```bash
python main.py --today
```

### 查看配置

```bash
python main.py --config
```

## 输出示例

```markdown
# 群讨论总结

**时间范围：** 2025-02-25
**总结日期：** 2025-02-26

## 📊 讨论概览
共讨论了 3 个话题

## 📌 话题 1: 苹果公司财报讨论
### 💬 讨论内容
大家关注 AAPL 今天的股价表现，新发布会消息影响很大...

### ✅ 结论
苹果财报季预期积极，iPhone 16 销量值得期待。

### 📈 具体个股
**苹果 AAPL**
- 股价预期上涨，机构看好 Q4 表现
```

## 成本预估

| 提供商 | 日成本 | 月成本 |
|--------|--------|--------|
| 智谱 AI GLM 4 Flash | ~¥0.10 | ~¥3 |
| DeepSeek | ~¥0.15 | ~¥4.5 |
| OpenAI | ~¥1.0 | ~¥30 |

*基于 100 条消息/天估算*

## 配置说明

### LLM API 配置

支持三种 LLM API（按优先级尝试）：

```bash
# 智谱 AI（推荐）
ZHIPU_API_KEY=sk-xxx
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# DeepSeek
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com

# OpenAI
OPENAI_API_KEY=sk-xxx
```

### 消息过滤配置

```bash
# 消息类型（1=文本）
MSG_TYPES=[1]

# 时间范围
MSG_TIME_START=00:00
MSG_TIME_END=23:59

# 最大消息数（防止 token 溢出）
MAX_MESSAGES=500
```

## 工作流程

```
微信电脑版备份 → MSG.db → PyWxDump 解密 →
消息过滤 → LLM 分析 → 报告生成 → Markdown 输出
```

## 项目结构

```
wechat-summary/
├── main.py              # 主程序入口
├── config.py            # 配置管理
├── wx_db_reader.py      # 微信数据库读取器
├── time_filter.py       # 消息过滤器
├── llm_analyzer.py      # LLM 分析器
├── report_generator.py  # 报告生成器
├── requirements.txt     # 依赖列表
└── backup/              # 旧代码备份（Wechaty 方案）
```

## 常见问题

### 1. 数据库连接失败

确保已在微信电脑版中备份聊天记录到电脑。

### 2. 未找到群聊

运行 `python main.py --list-rooms` 查看可用的群聊列表。

### 3. LLM 分析失败

检查 API Key 是否有效，确认配额充足。

### 4. 数据库加密

微信数据库使用 SQLCipher 加密，PyWxDump 会自动提取密钥。

## 合规说明

- ✅ 仅分析个人微信账号的聊天记录
- ✅ 使用微信官方备份功能，不使用第三方协议
- ✅ 不涉及未经授权的数据获取
- ⚠️ 请勿用于非法用途

## 许可证

MIT License

## 致谢

- [PyWxDump](https://github.com/TEST-AUDIT/PyWxDump) - 微信数据库解密工具
