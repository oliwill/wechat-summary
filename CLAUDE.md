# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python tool for automatically summarizing WeChat group discussions using LLM analysis. **Based on WeChat PC local database** - a compliant solution that avoids account ban risks.

**Key Change**: Migrated from Wechaty (web protocol, high ban risk) to WeChat PC local database reading (official backup feature, zero risk).

## Dependencies

```bash
pip install pywxdump-mini python-dotenv openai lxml
```

## Commands

### Running the Application

```bash
# Use .env preset configuration
python main.py

# Specify group
python main.py --room "美股群"

# Specify date
python main.py --date 2025-02-25

# List all chatrooms
python main.py --list-rooms

# Today's messages
python main.py --today

# Show current configuration
python main.py --config
```

### WeChat PC Preparation

**Before first use**:
1. Open WeChat PC
2. Settings → Chat Record Backup → Backup to Computer
3. Backup completed messages are stored at: `~/Documents/WeChat Files/[wxid]/MSG/`

## Architecture

### Data Flow

```
WeChat PC Backup → MSG.db (SQLite) → PyWxDump Decrypt →
Message Filtering → LLM Analysis → JSON Parsing → Report Generation → Markdown Output
```

### Core Components

| Component | File | Purpose |
|-----------|------|---------|
| Entry Point | `main.py` | Orchestrates workflow, CLI args, interactive selection |
| DB Reader | `wx_db_reader.py` | WeChat database decryption, message/chatroom reading |
| Filter | `time_filter.py` | Time/room/message type filtering |
| LLM Analyzer | `llm_analyzer.py` | Multi-provider LLM interface (Zhipu/DeepSeek/OpenAI) |
| Report Generator | `report_generator.py` | Markdown output formatting |
| Configuration | `config.py` | Environment-based config, LLM provider priority |

### Backup Directory

Old Wechaty-based files moved to `backup/`:
- `wechat_manager.py` - Wechaty integration (deprecated)
- `main_v2.py` - Old main program (deprecated)
- `test_*.py` - Old test files (deprecated)

## Configuration

### Required Environment Variables (.env)

```bash
# LLM API (at least one required)
ZHIPU_API_KEY=sk-xxx                    # Recommended: https://open.bigmodel.cn/
# DEEPSEEK_API_KEY=sk-xxx               # Alternative
# OPENAI_API_KEY=sk-xxx                 # Alternative

# WeChat database (auto-detected, usually no need to modify)
WX_DATA_DIR=~/Documents/WeChat Files

# Target groups (optional, can be selected interactively)
# TARGET_ROOMS=["美股交流群1", "美股策略群"]

# Message filtering
MSG_TYPES=[1]              # 1=text only
MSG_TIME_START=00:00
MSG_TIME_END=23:59
MAX_MESSAGES=500

# Output
OUTPUT_DIR=./output
TIMEZONE=Asia/Shanghai
```

### API Key Sources

1. **Zhipu GLM**: https://open.bigmodel.cn/ (cheapest for Chinese)
2. **DeepSeek**: https://platform.deepseek.com/
3. **OpenAI**: https://platform.openai.com/

## LLM Output Schema

```json
{
  "topics": [
    {
      "title": "话题标题",
      "discussion": "详细讨论内容",
      "conclusion": "结论",
      "stocks": [
        {"name": "股票名称", "code": "股票代码", "view": "看法"}
      ]
    }
  ]
}
```

## Important Constraints

- **Message Limit**: 500 messages max per run (token overflow prevention)
- **Time Filter**: Defaults to yesterday 00:00-23:59
- **Manual Backup Required**: User must backup chat records via WeChat PC first
- **Database Encryption**: WeChat databases are encrypted, requires PyWxDump for key extraction

## Cost Reference (100 messages/day)

| Provider | Cost/Month |
|----------|------------|
| Zhipu GLM 4 Flash | ~3 元 |
| DeepSeek | ~4.5 元 |
| OpenAI | ~30 元 |

## Compliance & Risks

| Aspect | Status |
|--------|--------|
| Account Ban Risk | ❌ None (uses official backup feature) |
| Legal Compliance | ✅ Personal data analysis only |
| Dependency | ⚠️ Requires WeChat PC, PyWxDump version compatibility |
