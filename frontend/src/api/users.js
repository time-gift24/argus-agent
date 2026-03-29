import client from './client'

export function getProfile() {
  return client.get('/me')
}

export function updateProfile(data) {
  return client.patch('/me', data)
}
