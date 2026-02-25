# 智谱 AI GLM 使用指南

## 优势

- ✅ **性价比高**：比 OpenAI 更便宜
- ✅ **中文支持好**：GLM 4.7 在中文理解上表现出色
- ✅ **速度快**：响应速度快
- ✅ **免费额度**：新用户有免费额度

## 获取 API Key

1. **注册账号**
   - 访问：https://open.bigmodel.cn/
   - 使用 GitHub 登录（推荐）

2. **获取 API Key**
   - 登录后进入：https://open.bigmodel.cn/usercenter/apikeys
   - 点击「创建新的 API Key」
   - 复制生成的 Key（以 `sk-` 开头）

3. **查看定价**
   - GLM 4.7 Flash：约 0.001 元/千 token（推荐）
   - GLM 4 Plus：约 0.01 元/千 token
   - GLM 4 Air：约 0.0005 元/千 token

## 使用方式

### 方式一：直接使用（已配置）

工具已经配置好使用 GLM 4.7 Flash，只需配置 API Key：

```bash
cd /home/z/.openclaw/workspace/wechat-summary
nano .env
```

修改为：
```bash
WECHATY_TOKEN=你的wechaty_token
ZHIPU_API_KEY=你的zhipu_api_key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 方式二：测试模式

不配置 API Key 时，使用测试模式（模拟数据）：

```bash
python test_zhipu.py
```

### 方式三：正式运行

```bash
python main_v2.py
```

## 模型选择

工具默认使用 `glm-4.7-flash`，你也可以在代码中选择其他模型：

| 模型 | 特点 | 价格 |
|------|------|------|
| `glm-4.7-flash` | 速度快，性价比高 | ⭐⭐⭐⭐⭐ |
| `glm-4-plus` | 性能更强 | ⭐⭐⭐⭐ |
| `glm-4-air` | 最便宜 | ⭐⭐⭐⭐⭐ |

修改 `llm_analyzer_v2.py` 中的 `model` 参数：

```python
analyzer = LLMAnalyzer(api_key, base_url, model="glm-4-plus")
```

## 费用预估

### 每天 100 条消息（平均 500 tokens/条）

- **GLM 4.7 Flash**：
  - 输入：100条 × 500tokens × 0.001元 = 0.05元
  - 输出：100条 × 500tokens × 0.001元 = 0.05元
  - **合计：约 0.1 元/天**

- **GLM 4 Plus**：
  - 输入：100条 × 500tokens × 0.01元 = 0.5元
  - 输出：100条 × 500tokens × 0.01元 = 0.5元
  - **合计：约 1.0 元/天**

### 每月成本

- **GLM 4.7 Flash**：约 3 元/月
- **GLM 4 Plus**：约 30 元/月

## 常见问题

### 1. API Key 无效

确保 API Key 是正确的，以 `sk-` 开头，并且没有被泄露。

### 2. 调用次数超限

检查是否超过了免费额度，或者购买了额外的 token。

### 3. 连接错误

检查网络连接，确保能访问 open.bigmodel.cn。

## 对比其他 API

| API 提供商 | 每天 100 条消息成本 | 推荐度 |
|-----------|-------------------|--------|
| 智谱 AI GLM 4.7 Flash | 0.1 元 | ⭐⭐⭐⭐⭐ |
| 智谱 AI GLM 4 Plus | 1.0 元 | ⭐⭐⭐⭐ |
| DeepSeek | 0.15 元 | ⭐⭐⭐⭐⭐ |
| OpenAI GPT-3.5 | 1.0 元 | ⭐⭐⭐ |
| OpenAI GPT-4o-mini | 1.5 元 | ⭐⭐⭐ |

## 建议

**推荐使用智谱 AI GLM 4.7 Flash**，性价比最高！

---

**注册地址**：https://open.bigmodel.cn/
**API Key 地址**：https://open.bigmodel.cn/usercenter/apikeys
