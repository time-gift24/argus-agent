import client from './client'

export function list() {
  return client.get('/mcp-configs')
}

export function create(data) {
  return client.post('/mcp-configs', data)
}

export function update(id, data) {
  return client.patch(`/mcp-configs/${id}`, data)
}

export function remove(id) {
  return client.delete(`/mcp-configs/${id}`)
}

export function testSaved(id) {
  return client.post(`/mcp-configs/${id}/test`)
}

export function testConfig(data) {
  return client.post('/mcp-configs/test-config', data)
}

export function getTools(id) {
  return client.get(`/mcp-configs/${id}/tools`)
}
