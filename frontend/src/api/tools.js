import client from './client'

export function list() {
  return client.get('/tools/')
}

export function remove(id) {
  return client.delete(`/tools/${id}`)
}
