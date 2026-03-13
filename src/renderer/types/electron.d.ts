export {}

declare global {
  interface Window {
    electronAPI?: {
      getWechatPath: () => Promise<{
        basePath: string
        users: string[]
      } | null>
      selectDirectory: () => Promise<string | null>
      readDirectory: (
        dirPath: string
      ) => Promise<Array<{ name: string; isDirectory: boolean; path: string }>>
      openExternal: (url: string) => Promise<void>
      getAppVersion: () => Promise<string>
      log: (message: string) => Promise<void>
    }
  }
}
