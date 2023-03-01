import { useContext } from "react"
import { NavLink, useLocation } from "react-router-dom"
import { ViewportContext } from "./contexts/viewport.context"

import IconComponent from "./icon.component"
import logo from '../ressources/ruche.png'
import AlertIcon from '../ressources/alert_icon.png'
import BatteryIcon from '../ressources/battery_icon.png'


import { BehiveOut, User } from "../generated"

type Hive = Pick<BehiveOut, 'id' | 'name' | 'last_metrics'>
export interface Props {
  hives: Hive[]
  user: User
  className?: string
}

function HiveListItemComponent({ id, name, last_metrics }: Hive) {
  const location = useLocation()
  const isActive = location.pathname.includes(`/hives/${id}`)

  return <li className={`rounded-md ${isActive && 'border border-indigo-600'}`}>
    <NavLink to={`/hives/${id}`} className="flex">
      <IconComponent small active={isActive} className="rounded-l-lg flex-none" logo={logo} />
      <div className={`flex flex-col justify-center w-full rounded-r-lg px-2 ${isActive ? 'bg-amber-200' : 'hover:bg-amber-200 bg-amber-100'}`}>
        <div className="-mt-1.5">{name}</div>
        <div className="flex flex-wrap gap-x-1">
          <div className="text-sm text-slate-700">
            <img className="inline w-4" src={BatteryIcon} alt="battery" />&nbsp;:&nbsp;
            {last_metrics.battery.value}&nbsp;{last_metrics.battery.unit}
          </div>
          <span className="text-sm text-slate-700">
            <img className="inline w-4" src={AlertIcon} alt="battery" />&nbsp;:&nbsp;
            {last_metrics.alert.value}
          </span>
        </div>
      </div>
    </NavLink>
  </li>
}

function MobileHiveListItemComponent({ id, name }: Hive) {
  const location = useLocation()
  const isActive = location.pathname.includes(`/hives/${id}`)

  return <li className={`${isActive && 'border border-indigo-600'}`}>
    <NavLink to={`/hives/${id}`} className="flex flex-col">
      <IconComponent rounded active={isActive} logo={logo} />
      <div className="text-lg text-center">{name}</div>

    </NavLink>
  </li>
}

export default function HiveListSelectorComponent({ hives }: Pick<Props, 'hives'>) {
  const { isMobile } = useContext(ViewportContext)
  const ListItemRenderer = isMobile ? MobileHiveListItemComponent : HiveListItemComponent

  return <ul className="grid grid-cols-2 md:grid-cols-1 gap-8 md:gap-4">
    {hives.map(hive => <ListItemRenderer key={hive.id} {...hive} />)}
  </ul>
}
