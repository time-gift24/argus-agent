import test from 'node:test'
import assert from 'node:assert/strict'

import { routes } from './routes.js'

test('routes expose dedicated MCP create and edit pages', () => {
  const paths = routes.map((route) => route.path)

  assert(paths.includes('/mcp'))
  assert(paths.includes('/mcp/new'))
  assert(paths.includes('/mcp/:id/edit'))
})

test('provider and MCP editor routes require authentication', () => {
  const protectedPaths = routes
    .filter((route) => route.meta?.requiresAuth)
    .map((route) => route.path)

  assert.deepEqual(
    protectedPaths.sort(),
    ['/mcp/:id/edit', '/mcp/new', '/providers/:id/edit', '/providers/new'].sort()
  )
})
