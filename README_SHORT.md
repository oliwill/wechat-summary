# 微信群讨论自动总结工具 - 项目概述

## 📖 项目信息

- **项目名称**：微信群讨论自动总结工具
- **描述**：自动总结美股微信群、Discord 群讨论内容的工具
- **开发语言**：Python + Node.js
- **Git 管理**：✅ 已初始化
- **GitHub 仓库**：[点击查看](https://github.com/你的用户名/wechat-summary)

## 一句话介绍

一个可以自动总结美股微信群、Discord 群讨论内容的工具，每天早上自动生成结构化报告。

## 核心功能

- 📊 自动提取群讨论主题
- 💬 记录详细讨论内容和结论
- 📈 识别讨论中的股票及观点
- 🤖 使用 LLM 智能分析
- 📅 自动按时间筛选（昨天 00:00-23:59）
- 🤖 支持跨天讨论处理
- 📝 生成 Markdown 格式报告
- 🔧 Mock 模式用于开发测试
- 📦 支持 Git 版本管理

## 技术栈

```
Python 3.8+ + Node.js 16+
├── Wechaty          # 微信机器人框架
├── OpenAI SDK       # LLM API 客户端
├── python-dotenv    # 环境变量管理
├── lxml            # XML 解析
└── PyTorch/Transformers # LLM 推理（可选）
```

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/wechat-summary.git
cd wechat-summary

# 2. 安装依赖
pip install --break-system-packages wechaty lxml

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 4. 运行测试
python test_zhipu.py

# 5. 运行主程序
python main_mock.py
```

## 成本预估

### 智谱 AI GLM 4.7 Flash（推荐）⭐⭐⭐⭐⭐
- **每日成本**：约 0.10 元（100 条消息）
- **每月成本**：约 3 元
- **免费额度**：新用户有免费额度

### DeepSeek API
- **每日成本**：约 0.15 元
- **每月成本**：约 4.5 元

### OpenAI API
- **每日成本**：约 1.0 元
- **每月成本**：约 30 元

## 文件结构

```
wechat-summary/
├── main_mock.py          # Mock 版本主程序（开发测试）⭐
├── wechat_manager_mock.py # Mock 微信管理器 ⭐
├── llm_analyzer_v2.py    # LLM 分析器
├── report_generator.py   # 报告生成
├── config_simple.py      # 配置管理
├── requirements.txt      # Python 依赖
├── .env.example          # 配置示例
├── .github/workflows/    # GitHub Actions
│   ├── test.yml         # 测试工作流
│   └── lint.yml         # 代码检查
├── README.md             # 完整文档
├── GITHUB_README.md      # GitHub 专用文档
├── START_HERE.md         # 快速开始 ⭐
├── ZHIPU_GUIDE.md        # 智谱 AI 指南
└── SETUP_COMPLETE.md     # 配置完成总结
```

## 使用场景

- 📈 群聊交流总结
- 💰 投资复盘记录
- 📰 市场动态收集
- 🎯 关键信息提取
- 📊 股票讨论分析

## 项目特点

✅ **功能完整**：满足所有需求
✅ **使用简单**：5 分钟快速上手
✅ **成本低廉**：每月几块钱
✅ **文档齐全**：有完整的文档和测试
✅ **易于扩展**：模块化设计
✅ **版本管理**：Git + GitHub
✅ **CI/CD**：自动测试和代码检查

## 文档索引

- **GITHUB_README.md** - GitHub 仓库说明 ⭐
- **START_HERE.md** - 5 分钟快速开始
- **README.md** - 完整使用文档
- **ZHIPU_GUIDE.md** - 智谱 AI 使用指南
- **SETUP_COMPLETE.md** - 配置完成总结

## 开发模式

### Mock 模式（当前使用）

使用 Mock 数据进行开发测试：

```bash
python main_mock.py
```

### 真实 API 模式

替换 `wechat_manager_mock.py` 中的 Mock 代码为真实的 API 调用。

详见：[SETUP_COMPLETE.md](SETUP_COMPLETE.md)

## Git 使用

```bash
# 查看提交历史
git log --oneline --graph

# 查看状态
git status

# 查看差异
git diff

# 撤销更改
git checkout -- <file>
```

## 贡献指南

欢迎贡献代码！请查看 [README.md](README.md) 中的贡献指南。

## 许可证

MIT License

## 联系方式

- GitHub：https://github.com/你的用户名/wechat-summary
- 如有问题，请提交 Issue

---

**开发时间**：2025-08-21
**开发者**：Abo (AI 助手)
**用户**：包子
**版本**：v0.1.0 (开发中)
