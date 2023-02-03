export function formatDate(date: Date, options: Intl.DateTimeFormatOptions = { dateStyle: 'short' }) {
  return Intl.DateTimeFormat(navigator.language, options).format(date)
}
