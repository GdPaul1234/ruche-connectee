export function cookieGetValueByKey(key: string) {
  return document.cookie
    .split('; ')
    .map(item => item.split('='))
    .find(([k]) => k === key)?.at(1)
}

export function cookieSetValue(key: string, value: string, options: Record<string, string | null> = {}) {
  const setOption = ([k, v]: [string, string | null]) => v ? `${k}=${v}` : k

  const cookieOptions = Object.entries(options)
    .map(setOption)
    .join('; ')

  document.cookie = `${key}=${value}; ${cookieOptions}`
}
