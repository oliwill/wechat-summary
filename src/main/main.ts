import { app, BrowserWindow, ipcMain, dialog, shell } from 'electron'
import path from 'path'
import fs from 'fs'
import { WeChatDB } from './wechat-db'
import { generateSummary, LLMConfig, SummaryRequest } from './llm-client'

// Disable GPU for stability
app.disableHardwareAcceleration()

let mainWindow: BrowserWindow | null = null
let wechatDB: WeChatDB | null = null

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'WeChat Summary - 微信群聊总结',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, '../preload/preload.js'),
    },
    show: false,
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow?.show()
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    const appDir = path.join(__dirname, '..')
    mainWindow.loadFile(path.join(appDir, '../dist/index.html'))
  }

  mainWindow.on('closed', () => {
    mainWindow = null
    if (wechatDB) {
      wechatDB.close()
    }
  })
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// ==================== IPC Handlers ====================

// Get WeChat data path
ipcMain.handle('get-wechat-path', async () => {
  const documentsPath = app.getPath('documents')
  const wechatPath = path.join(documentsPath, 'WeChat Files')
  
  if (!fs.existsSync(wechatPath)) {
    return null
  }
  
  const users = fs.readdirSync(wechatPath).filter(item => {
    const itemPath = path.join(wechatPath, item)
    return fs.statSync(itemPath).isDirectory()
  })
  
  return {
    basePath: wechatPath,
    users
  }
})

// Get WeChat installation info
ipcMain.handle('get-wechat-info', async () => {
  const wechatPath = WeChatDB.getWeChatPath()
  return wechatPath
})

// Open WeChat database
ipcMain.handle('open-wechat-db', async (_, dbPath: string, key?: string) => {
  try {
    wechatDB = new WeChatDB()
    const success = wechatDB.open(dbPath, key)
    return { success }
  } catch (error) {
    return { success: false, error: (error as Error).message }
  }
})

// Get chat groups
ipcMain.handle('get-chat-groups', async () => {
  if (!wechatDB) return []
  return wechatDB.getChatGroups()
})

// Get messages from group
ipcMain.handle('get-messages', async (_, groupId: string, startTime: number, endTime: number) => {
  if (!wechatDB) return []
  return wechatDB.getMessages(groupId, startTime, endTime)
})

// Close WeChat database
ipcMain.handle('close-wechat-db', async () => {
  if (wechatDB) {
    wechatDB.close()
    wechatDB = null
  }
})

// Generate summary with LLM
ipcMain.handle('generate-summary', async (_, config: LLMConfig, request: SummaryRequest) => {
  return await generateSummary(config, request)
})

// Select directory dialog
ipcMain.handle('select-directory', async () => {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openDirectory']
  })
  return result.canceled ? null : result.filePaths[0]
})

// Read directory contents
ipcMain.handle('read-directory', async (_, dirPath: string) => {
  try {
    const items = fs.readdirSync(dirPath, { withFileTypes: true })
    return items.map(item => ({
      name: item.name,
      isDirectory: item.isDirectory(),
      path: path.join(dirPath, item.name)
    }))
  } catch (error) {
    return []
  }
})

// Read file
ipcMain.handle('read-file', async (_, filePath: string) => {
  try {
    return fs.readFileSync(filePath)
  } catch (error) {
    return null
  }
})

// File exists
ipcMain.handle('file-exists', async (_, filePath: string) => {
  return fs.existsSync(filePath)
})

// Open external link
ipcMain.handle('open-external', async (_, url: string) => {
  await shell.openExternal(url)
})

// Get app version
ipcMain.handle('get-app-version', () => {
  return app.getVersion()
})

// Log message
ipcMain.handle('log', (_, message: string) => {
  console.log(`[Renderer] ${message}`)
})
