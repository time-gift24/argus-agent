import test from 'node:test'
import assert from 'node:assert/strict'

import { normalizeBreadcrumbs } from './pageShell.js'

test('normalizeBreadcrumbs returns a consistent object shape for mixed inputs', () => {
  assert.deepEqual(
    normalizeBreadcrumbs([
      { label: 'LLM 提供商', to: '/providers' },
      '新增提供商',
    ]),
    [
      { label: 'LLM 提供商', to: '/providers' },
      { label: '新增提供商', to: null },
    ]
  )
})

test('normalizeBreadcrumbs trims labels and treats blank links as null', () => {
  assert.deepEqual(
    normalizeBreadcrumbs([
      { label: ' MCP 服务 ', to: '   ' },
      { label: ' 编辑配置 ', to: '/mcp/123/edit' },
    ]),
    [
      { label: 'MCP 服务', to: null },
      { label: '编辑配置', to: '/mcp/123/edit' },
    ]
  )
})

test('normalizeBreadcrumbs rejects empty breadcrumb labels', () => {
  assert.throws(
    () => normalizeBreadcrumbs([{ label: '   ', to: '/providers' }]),
    /面包屑文案不能为空/
  )
})
