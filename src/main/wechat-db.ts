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
   */
  static getWeChatPath(): WeChatPath | null {
    const homeDir = os.homedir()
    const documentsPath = path.join(homeDir, 'Documents')
    const wechatBasePath = path.join(documentsPath, 'WeChat Files')

    if (!fs.existsSync(wechatBasePath)) {
      return null
    }

    // Find the user directory (contains WeChat files)
    const dirs = fs.readdirSync(wechatBasePath).filter(d => {
      const fullPath = path.join(wechatBasePath, d)
      return fs.statSync(fullPath).isDirectory() && fs.existsSync(path.join(fullPath, 'Msg'))
    })

    if (dirs.length === 0) {
      return null
    }

    // Use the first user directory
    const wxid = dirs[0]
    const msgPath = path.join(wechatBasePath, wxid, 'Msg')

    return {
      basePath: wechatBasePath,
      wxid,
      msgPath
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
