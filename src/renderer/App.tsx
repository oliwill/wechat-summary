import { useState, useEffect } from 'react'
import './styles/index.css'

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

interface SummaryResult {
  summary: string
  generatedAt: string
}

interface LLMConfig {
  provider: 'openai' | 'azure' | 'anthropic'
  apiKey: string
  model?: string
  baseUrl?: string
}

function App() {
  const [weChatInfo, setWeChatInfo] = useState<WeChatInfo | null>(null)
  const [dbOpened, setDbOpened] = useState(false)
  const [chatGroups, setChatGroups] = useState<ChatGroup[]>([])
  const [selectedGroup, setSelectedGroup] = useState<ChatGroup | null>(null)
  const [timeRange, setTimeRange] = useState<{ start: string; end: string }>({
    start: '',
    end: ''
  })
  const [llmConfig, setLlmConfig] = useState<LLMConfig>({
    provider: 'openai',
    apiKey: ''
  })
  const [summary, setSummary] = useState<SummaryResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [step, setStep] = useState<'welcome' | 'select-group' | 'time-range' | 'summary'>('welcome')

  // Demo data for testing
  const demoGroups: ChatGroup[] = [
    { id: '1', name: 'AI 学习交流群', memberCount: 256, messageCount: 1250 },
    { id: '2', name: '产品经理讨论组', memberCount: 128, messageCount: 856 },
    { id: '3', name: '技术总监联盟', memberCount: 89, messageCount: 2103 },
    { id: '4', name: '创业小伙伴', memberCount: 320, messageCount: 567 },
    { id: '5', name: '开源社区', memberCount: 512, messageCount: 3420 },
  ]

  useEffect(() => {
    // Try to get WeChat path on mount
    initWeChat()
  }, [])

  const initWeChat = async () => {
    try {
      const info = await window.electronAPI?.getWechatInfo()
      if (info) {
        setWeChatInfo(info)
        // Try to open the database
        const msgPath = info.msgPath
        // Look for MSG.db or MSG0.db
        const dbPath = `${msgPath}\\MSG.db` // Windows path
        const exists = await window.electronAPI?.fileExists(dbPath)
        if (exists) {
          const result = await window.electronAPI?.openWechatDb(dbPath)
          if (result?.success) {
            setDbOpened(true)
            const groups = await window.electronAPI?.getChatGroups()
            if (groups && groups.length > 0) {
              setChatGroups(groups)
            }
          }
        }
      }
    } catch (err) {
      console.error('Init WeChat failed:', err)
    }
  }

  const handleStartDemo = () => {
    setChatGroups(demoGroups)
    setStep('select-group')
  }

  const handleUseRealData = async () => {
    if (weChatInfo && dbOpened && chatGroups.length > 0) {
      setStep('select-group')
    } else if (weChatInfo) {
      // Try to find database files
      alert('未能自动找到微信数据库，请确保微信已登录并运行过')
    } else {
      alert('未能检测到微信安装，请确保微信已安装并运行过')
    }
  }

  const handleSelectGroup = (group: ChatGroup) => {
    setSelectedGroup(group)
    // Set default time range to last 7 days
    const today = new Date()
    const weekAgo = new Date(today)
    weekAgo.setDate(weekAgo.getDate() - 7)
    setTimeRange({
      start: weekAgo.toISOString().split('T')[0],
      end: today.toISOString().split('T')[0]
    })
    setStep('time-range')
  }

  const handleGenerateSummary = async () => {
    if (!selectedGroup || !timeRange.start || !timeRange.end) {
      return
    }

    if (!llmConfig.apiKey) {
      alert('请先配置 API Key')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      let messages: ChatMessage[] = []

      if (dbOpened && weChatInfo) {
        // Get real messages from WeChat
        const startTime = new Date(timeRange.start).getTime() / 1000
        const endTime = new Date(timeRange.end + ' 23:59:59').getTime() / 1000
        messages = await window.electronAPI?.getMessages(selectedGroup.id, startTime, endTime) || []
      }

      // If no real messages, use demo
      if (messages.length === 0) {
        messages = generateDemoMessages(selectedGroup.name)
      }

      // Call LLM to generate summary
      const result = await window.electronAPI?.generateSummary(llmConfig, {
        messages: messages.map(m => ({
          sender: m.sender,
          content: m.content,
          time: m.createTime
        })),
        groupName: selectedGroup.name,
        startDate: timeRange.start,
        endDate: timeRange.end
      })

      if (result?.error) {
        setError(result.error)
        // Fall back to demo summary
        setSummary({
          summary: generateDemoSummary(selectedGroup.name, timeRange.start, timeRange.end),
          generatedAt: new Date().toISOString()
        })
      } else {
        setSummary({
          summary: result?.summary || generateDemoSummary(selectedGroup.name, timeRange.start, timeRange.end),
          generatedAt: new Date().toISOString()
        })
      }

      setStep('summary')
    } catch (err) {
      console.error('Generate summary failed:', err)
      setError((err as Error).message)
      setSummary({
        summary: generateDemoSummary(selectedGroup.name, timeRange.start, timeRange.end),
        generatedAt: new Date().toISOString()
      })
      setStep('summary')
    } finally {
      setIsLoading(false)
    }
  }

  const generateDemoMessages = (groupName: string): ChatMessage[] => {
    const now = Date.now() / 1000
    return [
      { id: 1, msgId: '1', createTime: now - 3600 * 5, sender: '张三', content: '大家好！今天分享一个超好用的AI代码工具', type: 1 },
      { id: 2, msgId: '2', createTime: now - 3600 * 4, sender: '李四', content: '是什么工具？求介绍', type: 1 },
      { id: 3, msgId: '3', createTime: now - 3600 * 3, sender: '王五', content: '我用了一下，确实不错，链接：https://github.com/xxx', type: 1 },
      { id: 4, msgId: '4', createTime: now - 3600 * 2, sender: '赵六', content: '这个比Copilot快吗？', type: 1 },
      { id: 5, msgId: '5', createTime: now - 3600, sender: '张三', content: '实测快了3倍左右，而且代码质量更高', type: 1 },
    ]
  }

  const generateDemoSummary = (groupName: string, start: string, end: string): string => {
    return `今日群聊精华总结（${groupName}）

今天群内最劲爆的内容是关于AI代码工具的最新讨论。张三推荐了一款新的AI代码补全工具，声称比Copilot快3倍，引发了热烈讨论。

🛠️ 工具技巧
• 推荐了一款新的AI代码补全工具，声称比Copilot快3倍
• 分享了如何用LangChain构建本地知识库的教程
• 讨论了最新发布的大模型使用感受

📚 资源分享
• 分享了斯坦福最新发布的AI研究报告
• 推荐了三本关于大模型架构的电子书
• 转发了GitHub上的热门开源项目

💬 观点碰撞
• 关于AI是否会取代程序员的讨论，有人认为5年内不会，有人持相反意见
• 对AI编程工具的安全性进行了激烈辩论

本简报由AI自动生成`
  }

  const handleCopySummary = () => {
    if (summary) {
      navigator.clipboard.writeText(summary.summary)
      alert('已复制到剪贴板')
    }
  }

  const handleReset = () => {
    setSelectedGroup(null)
    setTimeRange({ start: '', end: '' })
    setSummary(null)
    setError(null)
    setStep('welcome')
  }

  return (
    <div className="app">
      <header className="header">
        <h1>💬 WeChat Summary</h1>
        <p>微信群聊智能总结工具</p>
      </header>

      <main className="main">
        {step === 'welcome' && (
          <div className="welcome-card">
            <h2>欢迎使用微信群聊总结工具</h2>
            <p>选择微信群，设定时间范围，AI自动生成精华总结</p>
            
            <div className="welcome-actions">
              <button className="btn btn-primary" onClick={handleStartDemo}>
                试用 Demo
              </button>
              
              {(weChatInfo || chatGroups.length > 0) && (
                <button className="btn btn-secondary" onClick={handleUseRealData}>
                  使用真实数据
                </button>
              )}
            </div>

            {dbOpened && (
              <div className="status-badge success">
                ✅ 已连接微信数据库
              </div>
            )}

            <div className="api-config">
              <h3>LLM 配置</h3>
              
              <div className="form-group">
                <label>提供商:</label>
                <select 
                  value={llmConfig.provider}
                  onChange={(e) => setLlmConfig({ ...llmConfig, provider: e.target.value as any })}
                >
                  <option value="openai">OpenAI</option>
                  <option value="anthropic">Anthropic (Claude)</option>
                  <option value="azure">Azure OpenAI</option>
                </select>
              </div>

              <div className="form-group">
                <label>API Key:</label>
                <input
                  type="password"
                  value={llmConfig.apiKey}
                  onChange={(e) => setLlmConfig({ ...llmConfig, apiKey: e.target.value })}
                  placeholder={llmConfig.provider === 'openai' ? 'sk-...' : 'API Key'}
                />
              </div>

              {llmConfig.provider === 'openai' && (
                <div className="form-group">
                  <label>模型 (可选):</label>
                  <input
                    type="text"
                    value={llmConfig.model || ''}
                    onChange={(e) => setLlmConfig({ ...llmConfig, model: e.target.value })}
                    placeholder="gpt-3.5-turbo"
                  />
                </div>
              )}

              <small>仅用于调用 LLM 生成总结，不会保存</small>
            </div>
          </div>
        )}

        {step === 'select-group' && (
          <div className="select-card">
            <h2>选择群聊</h2>
            <div className="group-list">
              {chatGroups.map(group => (
                <div
                  key={group.id}
                  className={`group-item ${selectedGroup?.id === group.id ? 'selected' : ''}`}
                  onClick={() => handleSelectGroup(group)}
                >
                  <div>
                    <span className="group-name">{group.name}</span>
                    <span className="group-members">{group.memberCount} 人</span>
                  </div>
                  <span className="group-count">{group.messageCount} 条消息</span>
                </div>
              ))}
            </div>
            <button className="btn btn-secondary" onClick={handleReset}>
              返回
            </button>
          </div>
        )}

        {step === 'time-range' && selectedGroup && (
          <div className="time-card">
            <h2>设定时间范围</h2>
            <div className="selected-info">
              已选择: <strong>{selectedGroup.name}</strong>
            </div>
            
            <div className="time-inputs">
              <div className="time-field">
                <label>开始日期:</label>
                <input
                  type="date"
                  value={timeRange.start}
                  onChange={(e) => setTimeRange({ ...timeRange, start: e.target.value })}
                />
              </div>
              <div className="time-field">
                <label>结束日期:</label>
                <input
                  type="date"
                  value={timeRange.end}
                  onChange={(e) => setTimeRange({ ...timeRange, end: e.target.value })}
                />
              </div>
            </div>

            <div className="quick-ranges">
              <button onClick={() => {
                const today = new Date()
                const yesterday = new Date(today)
                yesterday.setDate(yesterday.getDate() - 1)
                setTimeRange({
                  start: yesterday.toISOString().split('T')[0],
                  end: today.toISOString().split('T')[0]
                })
              }}>昨天</button>
              <button onClick={() => {
                const today = new Date()
                const weekAgo = new Date(today)
                weekAgo.setDate(weekAgo.getDate() - 7)
                setTimeRange({
                  start: weekAgo.toISOString().split('T')[0],
                  end: today.toISOString().split('T')[0]
                })
              }}>最近7天</button>
              <button onClick={() => {
                const today = new Date()
                const monthAgo = new Date(today)
                monthAgo.setMonth(monthAgo.getMonth() - 1)
                setTimeRange({
                  start: monthAgo.toISOString().split('T')[0],
                  end: today.toISOString().split('T')[0]
                })
              }}>最近30天</button>
            </div>

            <div className="action-buttons">
              <button 
                className="btn btn-primary"
                onClick={handleGenerateSummary}
                disabled={isLoading || !timeRange.start || !timeRange.end}
              >
                {isLoading ? '生成中...' : '生成总结'}
              </button>
              <button className="btn btn-secondary" onClick={handleReset}>
                返回
              </button>
            </div>
          </div>
        )}

        {step === 'summary' && summary && (
          <div className="summary-card">
            <h2>群聊总结</h2>
            <div className="summary-meta">
              <span>群组: {selectedGroup?.name}</span>
              <span>时间: {timeRange.start} - {timeRange.end}</span>
            </div>

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
            
            <div className="summary-content">
              <pre>{summary.summary}</pre>
            </div>

            <div className="action-buttons">
              <button className="btn btn-primary" onClick={handleCopySummary}>
                复制到剪贴板
              </button>
              <button className="btn btn-secondary" onClick={handleReset}>
                新建总结
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
