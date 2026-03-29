export function normalizeProviderModelName(value) {
  return String(value ?? '').trim()
}

export function addProviderModelDraft(models, rawName) {
  const name = normalizeProviderModelName(rawName)
  if (!name) {
    return {
      error: '请输入模型名称',
      models: [...models],
    }
  }

  if (models.includes(name)) {
    return {
      error: `模型 '${name}' 已存在`,
      models: [...models],
    }
  }

  return {
    error: '',
    models: [...models, name],
  }
}

export function removeProviderModelDraft(models, targetName) {
  return models.filter((name) => name !== targetName)
}

export function buildProviderPayload(form, { includeModels = false } = {}) {
  const payload = {
    name: form.name.trim(),
    config: {
      api_key: form.api_key.trim(),
      base_url: form.base_url.trim() || null,
    },
  }

  if (includeModels) {
    payload.models = (form.models ?? [])
      .map((name) => normalizeProviderModelName(name))
      .filter(Boolean)
  }

  return payload
}
