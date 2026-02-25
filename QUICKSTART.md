# 快速入门指南

## 5 分钟快速开始

### 第 1 步：安装依赖

```bash
cd wechat-summary
pip install -r requirements.txt
```

### 第 2 步：配置 API Key

1. **DeepSeek API Key**（推荐，免费额度大）
   - 访问：https://platform.deepseek.com/
   - 注册并获取 API Key

2. **Wechaty Token**
   - 访问：https://wechaty.io
   - 注册并获取 Token

编辑 `.env` 文件：

```bash
WECHATY_TOKEN=你的wechaty_token
DEEPSEEK_API_KEY=你的deepseek_api_key
```

### 第 3 步：运行测试

```bash
python test.py
```

### 第 4 步：运行主程序

```bash
python main.py
```

## 配置群聊

编辑 `.env` 文件：

```bash
# 方式 1：使用群名称
TARGET_GROUPS=["美股交流群1", "美股策略群"]

# 方式 2：使用群 ID（更精确）
GROUP_IDS=["7273788767", "1234567890"]
```

## 设置自动任务

每天早上 9 点自动总结：

```bash
# 编辑 crontab
crontab -e

# 添加这行
0 9 * * * cd /path/to/wechat-summary && python main.py
```

## 费用预估

- DeepSeek：约 0.02 元/天（约 0.6 元/月）
- OpenAI：约 0.1 元/天（约 3 元/月）

## 常见问题

### 找不到群聊？

检查群名称是否正确，或者使用群 ID。

### 分析失败？

检查 API Key 是否有效，网络是否正常。

### Token 超限？

如果消息量太大，可以调整代码中的消息数量限制。
