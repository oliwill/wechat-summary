import { contextBridge, ipcRenderer } from 'electron'

// Expose protected methods to renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // WeChat operations
  getWechatPath: () => ipcRenderer.invoke('get-wechat-path'),
  getWechatInfo: () => ipcRenderer.invoke('get-wechat-info'),
  openWechatDb: (dbPath: string, key?: string) => ipcRenderer.invoke('open-wechat-db', dbPath, key),
  getChatGroups: () => ipcRenderer.invoke('get-chat-groups'),
  getMessages: (groupId: string, startTime: number, endTime: number) => 
    ipcRenderer.invoke('get-messages', groupId, startTime, endTime),
  closeWechatDb: () => ipcRenderer.invoke('close-wechat-db'),
  
  // LLM operations
  generateSummary: (config: any, request: any) => 
    ipcRenderer.invoke('generate-summary', config, request),
  
  // File system operations
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  readDirectory: (dirPath: string) => ipcRenderer.invoke('read-directory', dirPath),
  readFile: (filePath: string) => ipcRenderer.invoke('read-file', filePath),
  fileExists: (filePath: string) => ipcRenderer.invoke('file-exists', filePath),
  
  // External links
  openExternal: (url: string) => ipcRenderer.invoke('open-external', url),
  
  // App info
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // Logging
  log: (message: string) => ipcRenderer.invoke('log', message),
})

// Type declarations for renderer
declare global {
  interface Window {
    electronAPI: {
      getWechatPath: () => Promise<{ basePath: string; users: string[] } | null>
      getWechatInfo: () => Promise<{ basePath: string; wxid: string; msgPath: string } | null>
      openWechatDb: (dbPath: string, key?: string) => Promise<{ success: boolean; error?: string }>
      getChatGroups: () => Promise<Array<{ id: string; name: string; memberCount: number; messageCount: number }>>
      getMessages: (groupId: string, startTime: number, endTime: number) => Promise<Array<{
        id: number
        msgId: string
        createTime: number
        sender: string
        content: string
        type: number
      }>>
      closeWechatDb: () => Promise<void>
      generateSummary: (config: any, request: any) => Promise<{ summary: string; error?: string }>
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
