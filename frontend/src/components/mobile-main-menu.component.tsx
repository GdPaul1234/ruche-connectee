import { Link, useLocation } from "react-router-dom"
import HiveListSelectorComponent, { Props } from "./hive-list-selector.component"

import website_logo from '../ressources/logo192.png'
import back_icon from '../ressources/back_icon.png'

export default function MobileMainMenuComponent({ hives, className }: Props) {
  const location = useLocation()

  const shouldShowHives = !location.pathname.includes('hives')
  const shouldShowBackButton = location.pathname !== '/'

  return <header className={`relative ${className}`}>
    {shouldShowBackButton && <Link
      to={location.pathname.slice(0, location.pathname.lastIndexOf('/'))}
      className="absolute bottom-4 hover:opacity-60"
    >
      <img src={back_icon} className="w-10 h-10" alt="go back" />
    </Link>}

    <Link to='/' className="w-full hover:opacity-60">
      <img src={website_logo} className="w-20 h-20 m-auto" alt="logo" />
    </Link>

    {shouldShowHives && <>
      <h2 className="mb-8 text-xl text-yellow-500 font-semibold">Mes ruches</h2>
      <HiveListSelectorComponent hives={hives} />
    </>}
  </header>
}
