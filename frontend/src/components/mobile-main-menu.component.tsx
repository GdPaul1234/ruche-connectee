import { Link, useLocation } from "react-router-dom"
import HiveListSelectorComponent, { Props } from "./hive-list-selector.component"

import website_logo from '../ressources/logo192.png'

export default function MobileMainMenuComponent({ hives, className }: Props) {
  const location = useLocation()
  const shouldShowHives = !location.pathname.includes('hives')

  return <header className={`${className}`}>
    <Link to='/' className="w-full">
      <img src={website_logo} className="w-20 h-20 m-auto" alt="logo" />
    </Link>

    {shouldShowHives && <>
      <h2 className="mb-8 text-xl text-yellow-500 font-semibold">Mes ruches</h2>
      <HiveListSelectorComponent hives={hives} />
    </>}
  </header>
}
