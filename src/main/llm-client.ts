export interface LLMConfig {
  provider: 'openai' | 'azure' | 'anthropic'
  apiKey: string
  model?: string
  baseUrl?: string
}

export interface SummaryRequest {
  messages: Array<{
    sender: string
    content: string
    time: number
  }>
  groupName: string
  startDate: string
  endDate: string
}

export interface SummaryResponse {
  summary: string
  error?: string
}

/**
 * Chat summary prompt template
 */
const SUMMARY_PROMPT_TEMPLATE = `你是一位专业的中文群聊总结助手，专门负责分析和总结微信群聊记录。你需要从繁杂的群聊中提取关键信息，生成一份全面、简洁且易读的群聊报告。

## 群聊信息
- 群名称: {groupName}
- 时间范围: {startDate} - {endDate}
- 消息数量: {messageCount}条

## 聊天记录
{chatMessages}

## 输出格式要求

1. 开头：1-2段自然语言概括当天最核心、最劲爆的内容
2. 正文：用分类+要点的形式呈现有价值的信息
3. 结尾：固定格式"本简报由AI自动生成"

## 分类参考（根据实际内容灵活选用，没有就不写）
• 🛠️ 工具技巧/实战经验
• 📚 资源推荐
• 📰 行业动态
• 💬 观点碰撞
• 😂 群友趣事

## 格式规范
• 不要使用markdown格式（不要用**加粗**、不要用#标题）
• 列表统一用 • 开头
• 子分类用普通文字，不加任何符号
• 链接保持原样，不要加方括号
• 适当用emoji增加可读性，但不要过多

## 内容规范
• 重点突出，过滤不重要的闲聊
• 语言通俗，保留群友的生动表达
• 保留关键人名，体现信息来源
• 工具名、链接要保留完整

请严格按照以上格式生成群聊总结：`

/**
 * Format messages for LLM input
 */
function formatMessages(messages: SummaryRequest['messages']): string {
  return messages.map(m => {
    const time = new Date(m.time * 1000).toLocaleString('zh-CN')
    return `[${time}] ${m.sender}: ${m.content}`
  }).join('\n\n')
}

/**
 * Build prompt for summary
 */
export function buildSummaryPrompt(request: SummaryRequest): string {
  const formattedMessages = formatMessages(request.messages)
  
  return SUMMARY_PROMPT_TEMPLATE
    .replace('{groupName}', request.groupName)
    .replace('{startDate}', request.startDate)
    .replace('{endDate}', request.endDate)
    .replace('{messageCount}', request.messages.length.toString())
    .replace('{chatMessages}', formattedMessages)
}

/**
 * Call LLM API to generate summary
 */
export async function generateSummary(
  config: LLMConfig,
  request: SummaryRequest
): Promise<SummaryResponse> {
  const prompt = buildSummaryPrompt(request)

  try {
    let response: Response

    if (config.provider === 'openai') {
      response = await fetch(config.baseUrl || 'https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${config.apiKey}`
        },
        body: JSON.stringify({
          model: config.model || 'gpt-3.5-turbo',
          messages: [
            { role: 'system', content: '你是一个专业的群聊总结助手，擅长从聊天记录中提取有价值的信息。' },
            { role: 'user', content: prompt }
          ],
          temperature: 0.7,
          max_tokens: 2000
        })
      })

      if (!response.ok) {
        const error = await response.text()
        return { summary: '', error: `OpenAI API错误: ${error}` }
      }

      const data = await response.json() as any
      return { summary: data.choices[0]?.message?.content || '' }
    }
    
    if (config.provider === 'anthropic') {
      response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': config.apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: config.model || 'claude-3-haiku-20240307',
          max_tokens: 2000,
          messages: [
            { role: 'user', content: prompt }
          ]
        })
      })

      if (!response.ok) {
        const error = await response.text()
        return { summary: '', error: `Anthropic API错误: ${error}` }
      }

      const data = await response.json() as any
      return { summary: data.content[0]?.text || '' }
    }

    // Azure OpenAI
    if (config.provider === 'azure') {
      const azureEndpoint = config.baseUrl || process.env.AZURE_OPENAI_ENDPOINT
      const deploymentName = config.model || 'gpt-35-turbo'
      
      response = await fetch(`${azureEndpoint}/openai/deployments/${deploymentName}/chat/completions?api-version=2024-02-15-preview`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'api-key': config.apiKey
        },
        body: JSON.stringify({
          messages: [
            { role: 'system', content: '你是一个专业的群聊总结助手，擅长从聊天记录中提取有价值的信息。' },
            { role: 'user', content: prompt }
          ],
          temperature: 0.7,
          max_tokens: 2000
        })
      })

      if (!response.ok) {
        const error = await response.text()
        return { summary: '', error: `Azure API错误: ${error}` }
      }

      const data = await response.json() as any
      return { summary: data.choices[0]?.message?.content || '' }
    }

    return { summary: '', error: '不支持的LLM提供商' }
  } catch (error) {
    return { 
      summary: '', 
      error: error instanceof Error ? error.message : '未知错误' 
    }
  }
}

export default {
  buildSummaryPrompt,
  generateSummary
}
