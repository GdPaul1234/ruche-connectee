export default function IconComponent({
  className,
  rounded,
  small,
  hoverable,
  active = true,
  activeBorder,
  logo }: {
    className?: string
    rounded?: boolean
    small?: boolean
    hoverable?: boolean
    active?: boolean
    activeBorder?: boolean
    logo: string
  }) {
  const containerSize = () => small ? 'h-14 w-14' : 'h-24 w-28'
  const logoSize = () => small ? 'h-16 w-16' : 'h-28 w-28'
  const marginSize = () => small ? 'mt-[-12px]' : 'mt-[-24px]'
  const roundedBorder = () => rounded ? 'rounded-md' : ''
  const hoverableIcon = () => hoverable && !active && 'hover:opacity-100 opacity-40'

  const hoverableDiv = () => {
    if (hoverable) {
      if (active) return activeBorder ? 'border border-indigo-600 bg-amber-200' : 'bg-amber-200'
      return 'hover:bg-amber-200 bg-amber-100'
    }

    return 'bg-amber-200'
  }

  return <div className={`${roundedBorder()} ${containerSize()} ${hoverableDiv()} ${className}`}>
    <img className={`block absolute ${logoSize()} ${marginSize()} ${hoverableIcon()}`} src={logo} alt="Hive logo" />
  </div>
}
