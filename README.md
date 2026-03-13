# WeChat Summary (微信群聊总结工具)

一个基于 Electron + React 的桌面应用，可以读取微信聊天记录并使用 AI 生成群聊精华总结。

![WeChat Summary](https://img.shields.io/badge/WeChat-Summary-blue)
![Electron](https://img.shields.io/badge/Electron-33.4-green)
![React](https://img.shields.io/badge/React-18.3-blue)
![License](https://img.shields.io/badge/License-ISC-green)

## 功能特性

- 📱 读取本地微信聊天记录数据库
- 🤖 支持多种 LLM 提供商：OpenAI、Anthropic (Claude)、Azure OpenAI
- 📝 自动生成群聊精华总结
- 🖥️ 跨平台桌面应用 (Windows/macOS/Linux)
- 🔒 本地处理，数据不上传服务器

## 系统要求

- Windows 10/11 或 macOS 10.15+
- 已安装微信并登录过
- Node.js 18+ (开发环境)
- LLM API Key (OpenAI/Claude/Azure)

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/oliwill/wechat-summary.git
cd wechat-summary

# 安装依赖
npm install
```

### 开发模式

```bash
npm run dev
```

这会同时启动 Vite 开发服务器和 Electron 应用。

### 构建

```bash
# 构建前端和 Electron 代码
npm run build

# 打包为可执行文件
npm run dist
```

打包后的可执行文件位于 `release` 目录下。

## 使用说明

### 1. 启动应用

运行构建后的可执行文件或 `npm run dev` 启动开发模式。

### 2. 配置 LLM

首次使用时需要在界面中配置 LLM：

| 提供商 | API Key 获取方式 |
|--------|------------------|
| OpenAI | [OpenAI API Keys](https://platform.openai.com/api-keys) |
| Anthropic | [Anthropic Console](https://console.anthropic.com/) |
| Azure | Azure OpenAI Service |

可选配置：
- **模型**：使用自定义模型（默认：gpt-3.5-turbo / claude-3-haiku）
- **Base URL**：自定义 API 端点（适用于代理或私有部署）

### 3. 选择群聊

应用会自动检测本地微信数据：
- 点击「使用真实数据」自动读取
- 或点击「试用 Demo」查看示例

### 4. 生成总结

1. 选择目标群聊
2. 设置时间范围（昨天/最近7天/最近30天/自定义）
3. 点击「生成总结」
4. 复制结果到剪贴板

## 项目结构

```
wechat-summary/
├── src/
│   ├── main/           # Electron 主进程
│   │   ├── main.ts     # 应用入口
│   │   ├── wechat-db.ts    # 微信数据库读取
│   │   └── llm-client.ts   # LLM API 调用
│   ├── preload/        # 预加载脚本
│   │   └── preload.ts
│   └── renderer/       # React 前端
│       ├── App.tsx     # 主应用组件
│       ├── main.tsx   # React 入口
│       └── styles/    # 样式文件
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 技术栈

- **前端框架**：React 18 + TypeScript
- **桌面框架**：Electron 33
- **构建工具**：Vite 5
- **数据库**：better-sqlite3 (读取微信本地数据)
- **AI 集成**：OpenAI API / Anthropic API / Azure OpenAI

## 注意事项

1. **数据安全**：所有数据处理均在本地进行，API Key 仅用于调用 LLM，不会保存到任何服务器
2. **微信数据库**：微信数据库通常位于 `Documents/WeChat Files/[微信号]/Msg/` 目录
3. **数据库加密**：部分微信版本数据库可能加密，需要额外处理
4. **API 费用**：使用 LLM API 会产生费用，请注意控制使用量

## 常见问题

### Q: 无法读取微信数据？
A: 确保微信已正常登录并运行过，数据才会写入本地数据库。

### Q: API 调用失败？
A: 检查 API Key 是否正确，网络是否可达，或尝试更换模型。

### Q: 总结生成不理想？
A: 可以尝试调整时间范围，或更换不同的 LLM 提供商/模型。

## 许可证

ISC License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

本简报由 AI 自动生成
