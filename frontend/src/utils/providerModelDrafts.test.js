import test from 'node:test'
import assert from 'node:assert/strict'

import {
  addProviderModelDraft,
  buildProviderPayload,
  removeProviderModelDraft,
} from './providerModelDrafts.js'

test('addProviderModelDraft trims model names and rejects duplicates', () => {
  assert.deepEqual(addProviderModelDraft([], '  gpt-4o  '), {
    error: '',
    models: ['gpt-4o'],
  })

  assert.deepEqual(addProviderModelDraft(['gpt-4o'], 'gpt-4o'), {
    error: "模型 'gpt-4o' 已存在",
    models: ['gpt-4o'],
  })
})

test('removeProviderModelDraft removes the requested model name', () => {
  assert.deepEqual(
    removeProviderModelDraft(['gpt-4o', 'gpt-4o-mini'], 'gpt-4o'),
    ['gpt-4o-mini']
  )
})

test('buildProviderPayload includes initial models during create flow only', () => {
  const form = {
    name: '  OpenAI  ',
    api_key: '  sk-test  ',
    base_url: '   ',
    models: [' gpt-4o ', 'gpt-4o-mini'],
  }

  assert.deepEqual(buildProviderPayload(form, { includeModels: true }), {
    name: 'OpenAI',
    config: {
      api_key: 'sk-test',
      base_url: null,
    },
    models: ['gpt-4o', 'gpt-4o-mini'],
  })

  assert.deepEqual(buildProviderPayload(form, { includeModels: false }), {
    name: 'OpenAI',
    config: {
      api_key: 'sk-test',
      base_url: null,
    },
  })
})
