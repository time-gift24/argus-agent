import client from './client'

export function listInternal() {
  return client.get('/internal-providers')
}

export function list() {
  return client.get('/providers')
}

export function create(data) {
  return client.post('/providers', data)
}

export function remove(id) {
  return client.delete(`/providers/${id}`)
}

export function get(id) {
  return client.get(`/providers/${id}`)
}

export function update(id, data) {
  return client.patch(`/providers/${id}`, data)
}

export function setDefault(id) {
  return client.put(`/providers/${id}/default`)
}

// ── Provider Models ──────────────────────────────────────────────────────────

export function listModels(providerId) {
  return client.get(`/providers/${providerId}/models`)
}

export function addModel(providerId, name) {
  return client.post(`/providers/${providerId}/models`, { name })
}

export function deleteModel(providerId, modelId) {
  return client.delete(`/providers/${providerId}/models/${modelId}`)
}

export function setDefaultModel(providerId, modelId) {
  return client.put(`/providers/${providerId}/models/${modelId}/default`)
}

export function testModel(providerId, modelId) {
  return client.post(`/providers/${providerId}/models/${modelId}/test`)
}
