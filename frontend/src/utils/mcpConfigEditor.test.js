import test from 'node:test'
import assert from 'node:assert/strict'

import {
  createEmptyMcpConfigForm,
  getMcpConfigPageMeta,
  populateMcpConfigForm,
} from './mcpConfigEditor.js'

test('createEmptyMcpConfigForm returns the default create-page shape', () => {
  assert.deepEqual(createEmptyMcpConfigForm(), {
    name: '',
    description: '',
    transport: 'http',
    command: '',
    argsStr: '',
    envStr: '',
    url: '',
    headersStr: '',
  })
})

test('populateMcpConfigForm formats saved config values for the editor while keeping secrets blank', () => {
  assert.deepEqual(
    populateMcpConfigForm({
      name: 'Filesystem',
      description: 'Workspace access',
      transport: 'stdio',
      command: 'npx',
      args: ['--root', '/tmp/my dir'],
      url: null,
    }),
    {
      name: 'Filesystem',
      description: 'Workspace access',
      transport: 'stdio',
      command: 'npx',
      argsStr: '[\n  "--root",\n  "/tmp/my dir"\n]',
      envStr: '',
      url: '',
      headersStr: '',
    }
  )
})

test('getMcpConfigPageMeta returns nested breadcrumbs for edit pages', () => {
  assert.deepEqual(
    getMcpConfigPageMeta({ isEdit: true, name: 'Filesystem' }),
    {
      title: '编辑配置',
      description: '调整当前 MCP 配置，并保留未重新输入的敏感字段。',
      breadcrumbs: [
        { label: 'MCP 服务', to: '/mcp' },
        { label: '编辑 - Filesystem', to: null },
      ],
    }
  )
})
