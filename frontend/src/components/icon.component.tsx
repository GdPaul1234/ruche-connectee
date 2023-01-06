interface Props {
  className?: string
  rounded?: boolean
  small?: boolean
  hoverable?: boolean
  active?: boolean
  logo: string
}

export default function IconComponent({ className, rounded, small, hoverable, active = true, logo }: Props) {
  const containerSize = () => small ? 'h-14 w-14' : 'h-24 w-28'
  const logoSize = () => small ? 'h-16 w-16' : 'h-28 w-28'
  const marginSize = () => small ? 'mt-[-12px]' : 'mt-[-24px]'
  const roundedBorder = () => rounded ? 'rounded-md' : ''

  const hoverableDiv = () => {
    if (hoverable) return active ? 'border border-indigo-600 bg-amber-200' : 'hover:bg-amber-200 bg-amber-100'
    return 'bg-amber-200'
  }

  const hoverableIcon = () => {
    if (hoverable && !active) return 'hover:opacity-100 opacity-40'
    return ''
  }

  return <div className={`${roundedBorder()} ${containerSize()} ${hoverableDiv()} ${className}`}>
    <img className={`block absolute ${logoSize()} ${marginSize()} ${hoverableIcon()}`} src={logo} alt="Hive logo" />
  </div>
}
