import { breadcrumb } from './pageShell.js'
import { formatArgsForEditor } from './mcpConfigForm.js'

export function createEmptyMcpConfigForm() {
  return {
    name: '',
    description: '',
    transport: 'http',
    command: '',
    argsStr: '',
    envStr: '',
    url: '',
    headersStr: '',
  }
}

export function populateMcpConfigForm(config) {
  return {
    name: config.name || '',
    description: config.description || '',
    transport: config.transport || 'http',
    command: config.command || '',
    argsStr: formatArgsForEditor(config.args),
    envStr: '',
    url: config.url || '',
    headersStr: '',
  }
}

export function getMcpConfigPageMeta({ isEdit, name = '' }) {
  if (isEdit) {
    return {
      title: '编辑配置',
      description: '调整当前 MCP 配置，并保留未重新输入的敏感字段。',
      breadcrumbs: [
        breadcrumb('MCP 服务', '/mcp'),
        breadcrumb(`编辑 - ${name || '...'}`),
      ],
    }
  }

  return {
    title: '新增配置',
    description: '创建新的 MCP Server 配置，并在保存前验证未落库的连接参数。',
    breadcrumbs: [
      breadcrumb('MCP 服务', '/mcp'),
      breadcrumb('新增配置'),
    ],
  }
}
