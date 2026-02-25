# 快速开始指南

## 5 分钟配置使用

### 第 1 步：注册智谱 AI（免费）

1. 访问：https://open.bigmodel.cn/
2. 点击「登录」 → 使用 GitHub 登录
3. 进入：https://open.bigmodel.cn/usercenter/apikeys
4. 点击「创建新的 API Key」
5. 复制 Key（以 `sk-` 开头）

### 第 2 步：配置

```bash
cd /home/z/.openclaw/workspace/wechat-summary
nano .env
```

修改为：
```bash
WECHATY_TOKEN=你的wechaty_token
ZHIPU_API_KEY=sk-你的真实key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 第 3 步：测试

```bash
python test_zhipu.py
```

**预期输出**：
```
✅ 所有测试完成！
```

### 第 4 步：正式运行

```bash
python main_v2.py
```

**会提示**：
1. 扫码登录微信
2. 监听群消息
3. 生成报告

### 第 5 步：设置自动任务

每天早上 9 点自动总结：

```bash
crontab -e
```

添加这行：
```
0 9 * * * cd /home/z/.openclaw/workspace/wechat-summary && python main_v2.py >> summary.log 2>&1
```

---

## 费用

- 每天约 0.10 元（100 条消息）
- 每月约 3 元
- 新用户有免费额度

---

## 文件说明

- `main_v2.py` - 主程序（推荐使用）⭐
- `test_zhipu.py` - 测试脚本 ⭐
- `README.md` - 完整文档
- `SETUP_COMPLETE.md` - 配置完成总结

---

## 获取 Wechaty Token

1. 访问：https://wechaty.io
2. 注册并登录
3. 获取 Token
4. 填入 `.env`

---

**需要帮助？** 查看 README.md
