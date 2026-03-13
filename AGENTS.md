# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-13
**Commit:** ba60aa7
**Branch:** (see git)

## OVERVIEW

WeChat Summary - Electron + React desktop app that reads local WeChat chat logs and generates AI-powered group chat summaries using LLM (OpenAI/Claude/Azure).

## STRUCTURE

```
wechat-summary/
├── src/
│   ├── main/           # Electron main process
│   │   ├── main.ts     # App entry, IPC handlers
│   │   ├── wechat-db.ts    # SQLite DB access (better-sqlite3)
│   │   └── llm-client.ts   # LLM API calls
│   ├── preload/         # Context bridge
│   │   └── preload.ts
│   └── renderer/       # React frontend
│       ├── App.tsx     # Main UI component
│       ├── main.tsx   # React entry
│       └── styles/    # CSS
├── package.json        # Electron 33, React 18, Vite 5
├── vite.config.ts
└── tsconfig.json       # Strict mode
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| App entry | `src/main/main.ts` | BrowserWindow, IPC handlers |
| WeChat DB | `src/main/wechat-db.ts` | better-sqlite3 wrapper |
| LLM logic | `src/main/llm-client.ts` | OpenAI/Anthropic/Azure API |
| UI | `src/renderer/App.tsx` | React component |
| Preload bridge | `src/preload/preload.ts` | Exposes electronAPI |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| main.ts | module | src/main/main.ts | App lifecycle, window mgmt |
| WeChatDB | class | src/main/wechat-db.ts | DB operations |
| generateSummary | fn | src/main/llm-client.ts | LLM API wrapper |
| App | component | src/renderer/App.tsx | Main UI |
| WeChatInfo | interface | src/renderer/App.tsx | Type definitions |

## CONVENTIONS

- **TypeScript**: Strict mode enabled, no implicit any
- **React**: Functional components with hooks
- **Electron**: Context isolation enabled, preload bridge
- **Build**: Vite for renderer, tsc for main/preload

## ANTI-PATTERNS (THIS PROJECT)

- `src/renderer/App.tsx`: Has unused parameters (groupName, start, end) - minor issue
- Electron API types incomplete - uses `window.electronAPI?` with implicit any

## BUILD COMMANDS

```bash
npm run dev          # Dev mode (Vite + Electron)
npm run build        # Build renderer + electron
npm run dist         # Package .exe
```

## GOTCHAS

- Windows path handling in `wechat-db.ts` (uses `\\` separators)
- better-sqlite3 requires native rebuild: `npm rebuild better-sqlite3`
- Database path: `Documents/WeChat Files/[wxid]/Msg/MSG.db`
