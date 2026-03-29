function parseJson(raw, label) {
  try {
    return JSON.parse(raw)
  } catch {
    throw new Error(`${label} JSON 格式错误`)
  }
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

export function formatArgsForEditor(args) {
  if (!Array.isArray(args) || args.length === 0) return ''
  return JSON.stringify(args, null, 2)
}

export function parseArgsFromEditor(raw) {
  if (!raw.trim()) return []

  const parsed = parseJson(raw, 'Args')
  if (!Array.isArray(parsed)) {
    throw new Error('Args 必须是 JSON 数组')
  }
  if (parsed.some(item => typeof item !== 'string')) {
    throw new Error('Args 必须是字符串数组')
  }

  return parsed
}

export function parseJsonObjectInput(raw, label) {
  if (!raw.trim()) return undefined

  const parsed = parseJson(raw, label)
  if (!isPlainObject(parsed)) {
    throw new Error(`${label} 必须是 JSON 对象`)
  }
  if (Object.values(parsed).some(value => typeof value !== 'string')) {
    throw new Error(`${label} 的值必须是字符串`)
  }

  return parsed
}

export function buildMcpConfigPayload(form) {
  const name = form.name.trim()
  const description = form.description.trim()
  if (!name) {
    throw new Error('名称为必填项')
  }

  const payload = {
    name,
    description: description || null,
    transport: form.transport,
  }

  if (form.transport === 'stdio') {
    const command = form.command.trim()
    if (!command) {
      throw new Error('Command 为必填项')
    }
    payload.command = command
    payload.args = parseArgsFromEditor(form.argsStr)

    const env = parseJsonObjectInput(form.envStr, '环境变量')
    if (env !== undefined) {
      payload.env = env
    }
  } else {
    const url = form.url.trim()
    if (!url) {
      throw new Error('URL 为必填项')
    }
    payload.url = url

    const headers = parseJsonObjectInput(form.headersStr, 'Headers')
    if (headers !== undefined) {
      payload.headers = headers
    }
  }

  return payload
}
