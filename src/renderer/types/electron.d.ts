export {}

interface WeChatInfo {
  basePath: string
  wxid: string
  msgPath: string
}

interface ChatGroup {
  id: string
  name: string
  memberCount: number
  messageCount: number
}

interface ChatMessage {
  id: number
  msgId: string
  createTime: number
  sender: string
  content: string
  type: number
}

interface LLMConfig {
  provider: 'openai' | 'azure' | 'anthropic' | 'zhipu'
  apiKey: string
  model?: string
  baseUrl?: string
}

interface SummaryRequest {
  messages: Array<{
    sender: string
    content: string
    time: number
  }>
  groupName: string
  startDate: string
  endDate: string
}

interface SummaryResponse {
  summary: string
  error?: string
}

declare global {
  interface Window {
    electronAPI?: {
      getWechatPath: () => Promise<{ basePath: string; users: string[] } | null>
      getWechatInfo: () => Promise<WeChatInfo | null>
      openWechatDb: (dbPath: string, key?: string) => Promise<{ success: boolean; error?: string }>
      getChatGroups: () => Promise<ChatGroup[]>
      getMessages: (groupId: string, startTime: number, endTime: number) => Promise<ChatMessage[]>
      closeWechatDb: () => Promise<void>
      generateSummary: (config: LLMConfig, request: SummaryRequest) => Promise<SummaryResponse>
      selectDirectory: () => Promise<string | null>
      readDirectory: (dirPath: string) => Promise<Array<{ name: string; isDirectory: boolean; path: string }>>
      readFile: (filePath: string) => Promise<Buffer | null>
      fileExists: (filePath: string) => Promise<boolean>
      openExternal: (url: string) => Promise<void>
      getAppVersion: () => Promise<string>
      log: (message: string) => Promise<void>
    }
  }
}
