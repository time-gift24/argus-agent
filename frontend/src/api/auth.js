import client from './client'

export function devLogin(username) {
  return client.get('/auth/login', {
    headers: { 'X-Dev-User': username },
  })
}
