interface Props {
  className?: string
  rounded?: boolean
  small?: boolean
  logo: string
}

export default function IconComponent({ className, rounded, small, logo }: Props) {
  const containerSize = () => small ? 'h-14 w-14' : 'h-24 w-28'
  const logoSize = () => small ? 'h-16 w-16' : 'h-28 w-28'
  const marginSize = () => small ? 'mt-[-12px]' : 'mt-[-24px]'
  const roundedBorder = () => rounded ? 'rounded-md' : ''

  return <div className={`${roundedBorder()} ${containerSize()} bg-amber-200 ${className}`}>
    <img className={`block absolute ${logoSize()} ${marginSize()}`} src={logo} alt="Hive logo" />
  </div>
}
