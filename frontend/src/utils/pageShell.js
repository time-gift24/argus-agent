export const PAGE_BODY_STICKY_TOP_CLASS = 'top-[4.5rem]'

function normalizeBreadcrumbItem(item) {
  if (typeof item === 'string') {
    const label = item.trim()
    if (!label) {
      throw new Error('面包屑文案不能为空')
    }
    return { label, to: null }
  }

  if (!item || typeof item !== 'object') {
    throw new Error('面包屑项必须是字符串或对象')
  }

  const label = `${item.label ?? ''}`.trim()
  if (!label) {
    throw new Error('面包屑文案不能为空')
  }

  const to = typeof item.to === 'string' && item.to.trim() ? item.to.trim() : null
  return { label, to }
}

export function normalizeBreadcrumbs(items = []) {
  if (!Array.isArray(items)) {
    throw new Error('面包屑必须是数组')
  }

  return items.map(normalizeBreadcrumbItem)
}

export function breadcrumb(label, to = null) {
  return normalizeBreadcrumbs([{ label, to }])[0]
}
