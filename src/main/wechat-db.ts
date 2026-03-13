import Database from 'better-sqlite3'
import path from 'path'
import fs from 'fs'
import os from 'os'

export interface WeChatUser {
  wxid: string
  nickname: string
}

export interface ChatGroup {
  id: string
  name: string
  memberCount: number
  messageCount: number
}

export interface ChatMessage {
  id: number
  msgId: string
  createTime: number
  sender: string
  content: string
  type: number
}

export interface WeChatPath {
  basePath: string
  wxid: string
  msgPath: string
}

export class WeChatDB {
  private db: Database.Database | null = null
  private key: string = ''
  private wxid: string = ''

  /**
   * Get WeChat data directory path
   * Tries multiple common installation locations
   */
  static getWeChatPath(): WeChatPath | null {
    const possiblePaths: WeChatPath[] = []

    // Path 1: User Documents (most common)
    const homeDir = os.homedir()
    const documentsPath = path.join(homeDir, 'Documents')
    const wechatPath1 = path.join(documentsPath, 'WeChat Files')
    if (fs.existsSync(wechatPath1)) {
      const wxid = WeChatDB.findFirstUserDir(wechatPath1)
      if (wxid) {
        possiblePaths.push({
          basePath: wechatPath1,
          wxid,
          msgPath: path.join(wechatPath1, wxid, 'Msg', 'MSG.db')
        })
      }
    }

    // Path 2: Program Files (x86) - like user's system
    const programFilesX86Path = path.join('D:\\Program Files (x86)', 'Tencent', 'WeChat', 'WeChat Files')
    if (fs.existsSync(programFilesX86Path)) {
      const wxid = WeChatDB.findFirstUserDir(programFilesX86Path)
      if (wxid) {
        possiblePaths.push({
          basePath: programFilesX86Path,
          wxid,
          msgPath: path.join(programFilesX86Path, wxid, 'Msg', 'MSG.db')
        })
      }
    }

    // Path 3: Program Files
    const programFilesPath = path.join('D:\\Program Files', 'Tencent', 'WeChat', 'WeChat Files')
    if (fs.existsSync(programFilesPath)) {
      const wxid = WeChatDB.findFirstUserDir(programFilesPath)
      if (wxid) {
        possiblePaths.push({
          basePath: programFilesPath,
          wxid,
          msgPath: path.join(programFilesPath, wxid, 'Msg', 'MSG.db')
        })
      }
    }

    // Path 4: AppData
    const appDataPath = process.env.APPDATA || ''
    if (appDataPath) {
      const wechatAppDataPath = path.join(appDataPath, 'Tencent', 'WeChat', 'WeChat Files')
      if (fs.existsSync(wechatAppDataPath)) {
        const wxid = WeChatDB.findFirstUserDir(wechatAppDataPath)
        if (wxid) {
          possiblePaths.push({
            basePath: wechatAppDataPath,
            wxid,
            msgPath: path.join(wechatAppDataPath, wxid, 'Msg', 'MSG.db')
          })
        }
      }
    }

    // Return first found path, or null if none found
    return possiblePaths.length > 0 ? possiblePaths[0] : null
  }

  /**
   * Helper to find first user directory with Msg folder
   */
  private static findFirstUserDir(basePath: string): string | null {
    try {
      const dirs = fs.readdirSync(basePath).filter(d => {
        const fullPath = path.join(basePath, d)
        return fs.statSync(fullPath).isDirectory() && fs.existsSync(path.join(fullPath, 'Msg'))
      })
      return dirs.length > 0 ? dirs[0] : null
    } catch {
      return null
    }
  }

  /**
   * Try to find WeChat process key from memory
   * This is a simplified version - full implementation would use native bindings
   */
  async extractKey(): Promise<string> {
    // For demo purposes, we'll use a placeholder
    // In production, this would use memory reading techniques
    // Reference: PyWxDump approach
    return ''
  }

  /**
   * Open WeChat database with optional key
   */
  open(dbPath: string, key?: string): boolean {
    try {
      // For unencrypted databases
      this.db = new Database(dbPath, { readonly: true })
      return true
    } catch (error) {
      console.error('Failed to open database:', error)
      return false
    }
  }

  /**
   * Get all chat groups
   */
  getChatGroups(): ChatGroup[] {
    if (!this.db) return []

    try {
      // Query chat rooms from Contact table
      // Note: Actual table structure may vary
      const stmt = this.db.prepare(`
        SELECT UserName, NickName, 
               (SELECT COUNT(*) FROM ChatRoom WHERE ChatRoom.UserName = Contact.UserName) as memberCount
        FROM Contact 
        WHERE Type = 2 AND NickName IS NOT NULL
        ORDER BY NickName
        LIMIT 100
      `)

      const rows = stmt.all() as any[]
      
      return rows.map(row => ({
        id: row.UserName || '',
        name: row.Nickname || row.UserName || 'Unknown',
        memberCount: row.memberCount || 0,
        messageCount: 0
      }))
    } catch (error) {
      console.error('Failed to get chat groups:', error)
      return []
    }
  }

  /**
   * Get messages from a specific group within time range
   */
  getMessages(groupId: string, startTime: number, endTime: number): ChatMessage[] {
    if (!this.db) return []

    try {
      const stmt = this.db.prepare(`
        SELECT MsgId, CreateTime, StrTalker, StrContent, Type
        FROM MSG
        WHERE StrTalker = ? AND CreateTime >= ? AND CreateTime <= ?
        ORDER BY CreateTime DESC
        LIMIT 1000
      `)

      const rows = stmt.all(groupId, startTime, endTime) as any[]

      return rows.map(row => ({
        id: row.MsgId || 0,
        msgId: row.MsgId?.toString() || '',
        createTime: row.CreateTime || 0,
        sender: row.StrTalker || '',
        content: row.StrContent || '',
        type: row.Type || 0
      }))
    } catch (error) {
      console.error('Failed to get messages:', error)
      return []
    }
  }

  /**
   * Get message count for a group
   */
  getMessageCount(groupId: string): number {
    if (!this.db) return 0

    try {
      const stmt = this.db.prepare(`
        SELECT COUNT(*) as count FROM MSG WHERE StrTalker = ?
      `)
      const result = stmt.get(groupId) as { count: number }
      return result?.count || 0
    } catch {
      return 0
    }
  }

  /**
   * Close database connection
   */
  close() {
    if (this.db) {
      this.db.close()
      this.db = null
    }
  }
}

export default WeChatDB
