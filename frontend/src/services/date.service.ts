export function formatDate(date: Date) {
  return Intl.DateTimeFormat(navigator.language, { dateStyle: 'short' }).format(date)
}
