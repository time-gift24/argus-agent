import test from 'node:test'
import assert from 'node:assert/strict'

import {
  buildMcpConfigPayload,
  formatArgsForEditor,
} from './mcpConfigForm.js'

test('formatArgsForEditor and buildMcpConfigPayload preserve spaced stdio args', () => {
  const args = ['--project', '/tmp/my dir', '--label=alpha beta']
  const argsStr = formatArgsForEditor(args)

  const payload = buildMcpConfigPayload({
    name: 'Filesystem',
    description: '',
    transport: 'stdio',
    command: 'npx',
    argsStr,
    envStr: '',
    url: '',
    headersStr: '',
  })

  assert.deepEqual(payload.args, args)
})

test('buildMcpConfigPayload rejects non-array stdio args input', () => {
  assert.throws(
    () => buildMcpConfigPayload({
      name: 'Filesystem',
      description: '',
      transport: 'stdio',
      command: 'npx',
      argsStr: '{"not":"an array"}',
      envStr: '',
      url: '',
      headersStr: '',
    }),
    /Args 必须是 JSON 数组/
  )
})

test('buildMcpConfigPayload rejects invalid headers json shape', () => {
  assert.throws(
    () => buildMcpConfigPayload({
      name: 'Remote',
      description: '',
      transport: 'http',
      command: '',
      argsStr: '',
      envStr: '',
      url: 'https://example.com/mcp',
      headersStr: '["Authorization"]',
    }),
    /Headers 必须是 JSON 对象/
  )
})
