import { useContext } from 'react'
import { NavLink, useLocation } from 'react-router-dom'

import { Hive } from '../services/hive.service'
import { ViewportContext } from './contexts/viewport.context'

import HumidityIcon from '../ressources/humidity_icon.png'
import TemperatureIcon from '../ressources/temperature_icon.png'
import WeightIcon from '../ressources/weight_icon.png'
import AlertIcon from '../ressources/alert_icon.png'
import BatteryIcon from '../ressources/battery_icon.png'
import IconComponent from './icon.component'

function HiveMetric({ name, value }: {
  name: keyof Hive['sensors_values']
  value: number | string
}) {
  function logoForMetricName() {
    const logoFinder = {
      humidity: HumidityIcon,
      temperature: TemperatureIcon,
      weight: WeightIcon,
      alert: AlertIcon,
      battery: BatteryIcon,
    }
    return logoFinder[name]
  }

  const location = useLocation()
  const isActive = location.pathname.endsWith(`/${name}`)
  const { isMobile } = useContext(ViewportContext)

  return <NavLink to={name}>
    <IconComponent rounded small={!isMobile} hoverable active={isActive} activeBorder logo={logoForMetricName()} />
    <div className="text-base md:text-sm w-28 md:w-16">
      <div className="text-ellipsis overflow-hidden">{name}</div>
      <div className="text-sm md:text-xs font-medium text-slate-700">{value} Met</div>
    </div>
  </NavLink>
}

export default function HiveMetricsComponent({ name, sensors }: {
  name: Hive['name']
  sensors: Hive['sensors_values']
}) {
  const { isMobile } = useContext(ViewportContext)
  const gridColumn = isMobile ? 'grid-cols-2' : 'grid-flow-col'

  return <div className={`grid ${gridColumn} gap-8 md:gap-4 auto-cols-max`}>
    {isMobile && <h2 className='col-span-full text-xl text-yellow-500 font-semibold'>Gérer la ruche {name}</h2>}
    {Object.keys(sensors).map(key => <HiveMetric
      key={key}
      name={key as keyof Hive['sensors_values']}
      value={sensors[key as keyof Hive['sensors_values']]}
    />)}
  </div>
}