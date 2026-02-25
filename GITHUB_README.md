# 微信群讨论自动总结工具

自动总结美股微信群、Discord 群讨论内容的工具，每天早上自动生成结构化报告。

## ✨ 功能特点

- 📊 自动分析群消息，提取讨论主题
- 💬 详细记录讨论内容和结论
- 📈 识别讨论中的个股及观点
- 🤖 基于 LLM 智能分析（支持 GLM 4.7、DeepSeek、OpenAI）
- 📅 自动按时间筛选（昨天 00:00-23:59）
- 🤖 支持跨天讨论处理
- 📝 生成 Markdown 格式报告

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Node.js 16+（Wechaty 需要）
- 智谱 AI GLM / DeepSeek / OpenAI API Key

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/你的用户名/wechat-summary.git
cd wechat-summary
```

2. **安装依赖**

```bash
# Python 依赖
pip install --break-system-packages wechaty wechaty-puppet-service

# Node.js 依赖（Wechaty 需要）
npm install wechaty-puppet-wechat4u
```

3. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

4. **配置 API Key**

编辑 `.env` 文件：

```bash
# 智谱 AI GLM（推荐）
ZHIPU_API_KEY=你的api_key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# 或 DeepSeek
# DEEPSEEK_API_KEY=你的api_key
# DEEPSEEK_BASE_URL=https://api.deepseek.com

# 或 OpenAI
# OPENAI_API_KEY=你的api_key
```

5. **运行测试**

```bash
# Mock 模式测试（不调用真实 API）
python main_mock.py

# 测试完整功能
python test_zhipu.py
```

## 📁 项目结构

```
wechat-summary/
├── main_mock.py          # Mock 版本主程序（开发测试）⭐
├── wechat_manager_mock.py # Mock 微信管理器 ⭐
├── llm_analyzer_v2.py    # LLM 分析器
├── report_generator.py   # 报告生成
├── config_simple.py      # 配置管理
├── requirements.txt      # Python 依赖
├── .env.example          # 配置示例
├── README.md             # 完整文档
├── START_HERE.md         # 快速开始 ⭐
└── ZHIPU_GUIDE.md        # 智谱 AI 指南
```

## 🔧 开发模式

### Mock 模式

使用 Mock 数据进行开发测试：

```bash
python main_mock.py
```

### 真实 API 模式

替换 `wechat_manager_mock.py` 中的 Mock 代码为真实的 API 调用：

```python
# 开发完成后，替换为真实的 API
class WeChatManager:
    def __init__(self, use_mock: bool = False):  # 默认改为 False
        self.use_mock = use_mock

    async def login(self):
        if not self.use_mock:
            # 调用真实的 Wechaty API
            await self.client.start()

    async def get_messages(self, date_range: tuple):
        if not self.use_mock:
            # 调用真实的 Wechaty API
            return await self.client.get_messages(date_range)
```

## 📖 文档

- **START_HERE.md** - 5 分钟快速开始
- **README.md** - 完整使用文档
- **ZHIPU_GUIDE.md** - 智谱 AI 使用指南
- **SETUP_COMPLETE.md** - 配置完成总结

## 💰 费用预估

### 智谱 AI GLM 4.7 Flash

- **每日成本**：约 0.10 元（100 条消息）
- **每月成本**：约 3 元
- **免费额度**：新用户有免费额度

### 对比

| API 提供商 | 每日成本 | 每月成本 | 推荐度 |
|-----------|---------|---------|--------|
| 智谱 AI GLM 4.7 Flash | 0.10 元 | 3 元 | ⭐⭐⭐⭐⭐ |
| DeepSeek | 0.15 元 | 4.5 元 | ⭐⭐⭐⭐⭐ |
| OpenAI | 1.0 元 | 30 元 | ⭐⭐⭐ |

## 🔮 后续计划

- [ ] 实现 Wechaty 真实 API 集成
- [ ] 实现企业微信 API 集成
- [ ] 实现飞书 API 集成
- [ ] 支持 Discord Bot
- [ ] Web 界面
- [ ] 历史数据对比

## 📝 API 集成指南

### Wechaty 集成

1. 安装 Node.js 依赖：

```bash
npm install wechaty-puppet-wechat4u
```

2. 修改 `wechat_manager_mock.py`：

```python
# 导入 Wechaty
from wechaty import Wechaty
from wechaty_puppet_wechat4u import WechatyPuppetWechat4u

class WeChatManager:
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        if not self.use_mock:
            self.client = Wechaty(WechatyPuppetWechat4u())
```

3. 调用真实 API

参考：https://github.com/wechaty/wechaty

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

Abo (AI 助手) | 用户：包子

## 📞 支持

如有问题，请查看文档或提交 Issue。
