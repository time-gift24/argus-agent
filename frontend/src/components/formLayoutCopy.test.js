import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))

function readComponent(name) {
  return readFileSync(resolve(__dirname, name), 'utf8')
}

test('PageBodyShell keeps the page header lightweight', () => {
  const source = readComponent('PageBodyShell.vue')

  assert.doesNotMatch(source, /sticky\s+\$\{PAGE_BODY_STICKY_TOP_CLASS\}/)
  assert.doesNotMatch(source, /rounded-\[2rem\]/)
  assert.doesNotMatch(source, /backdrop-blur/)
  assert.match(source, /<div class="mx-auto max-w-7xl">/)
  assert.match(source, /<div class="min-h-5 flex items-center">/)
  assert.doesNotMatch(source, /sm:flex-row sm:items-center sm:justify-between/)
})

test('ProviderConfigForm omits oversized repeated section headings', () => {
  const source = readComponent('ProviderConfigForm.vue')

  assert.doesNotMatch(source, /Provider 信息/)
  assert.doesNotMatch(source, /连接参数/)
  assert.doesNotMatch(source, /测试当前表单配置/)
})

test('McpConfigForm omits oversized repeated section headings', () => {
  const source = readComponent('McpConfigForm.vue')

  assert.doesNotMatch(source, /新增 MCP 配置/)
  assert.doesNotMatch(source, /配置概览/)
  assert.doesNotMatch(source, /连接参数/)
  assert.doesNotMatch(source, /测试未保存配置/)
  assert.doesNotMatch(source, /敏感字段保留规则/)
})
