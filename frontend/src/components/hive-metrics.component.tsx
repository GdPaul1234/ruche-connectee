import { useContext } from 'react'
import { NavLink, useLocation } from 'react-router-dom'

import { ViewportContext } from './contexts/viewport.context'

import HumidityIcon from '../ressources/humidity_icon.png'
import TemperatureIcon from '../ressources/temperature_icon.png'
import WeightIcon from '../ressources/weight_icon.png'
import AlertIcon from '../ressources/alert_icon.png'
import BatteryIcon from '../ressources/battery_icon.png'
import IconComponent from './icon.component'

import { BehiveOut, BehiveMetrics } from '../generated'

const logoIcons = {
  humidity: HumidityIcon,
  temperature: TemperatureIcon,
  weight: WeightIcon,
  alert: AlertIcon,
  battery: BatteryIcon,
} as const

function HiveMetric({ name, value }: {
  name: keyof typeof logoIcons
  value: { value: number | string, unit: string | null }
}) {
  function logoForMetricName() {
    return logoIcons[name]
  }

  const location = useLocation()
  const isActive = location.pathname.endsWith(`/${name}`)
  const { isMobile } = useContext(ViewportContext)

  return <NavLink to={name}>
    <IconComponent rounded small={!isMobile} hoverable active={isActive} activeBorder logo={logoForMetricName()} />
    <div className="text-base md:text-sm w-28 md:w-16">
      <div className="text-ellipsis overflow-hidden">{name}</div>
      <div className="text-sm md:text-xs font-medium text-slate-700">{`${value.value} ${value.unit ?? ''}`}</div>
    </div>
  </NavLink>
}

export default function HiveMetricsComponent({ name, sensors }: {
  name: BehiveOut['name']
  sensors: BehiveMetrics
}) {
  const { isMobile } = useContext(ViewportContext)
  const gridColumn = isMobile ? 'grid-cols-2' : 'grid-flow-col'

  const sensorValues = [
    ...Object.keys(sensors).reduce(
      (acc, value) => value.startsWith('temperature') ? acc.add('temperature') : acc.add(value),
      new Set<string>()
    )
  ].map(key => {
    if (key === 'temperature') {
      return {
        key,
        value: {
          unit: null,
          value: `${sensors['temperature_indoor'].value}/${sensors['temperature_outdoor'].value} °C`
        }
      }
    }
    return { key, value: sensors[key as keyof BehiveMetrics] }
  })

  return <div className={`grid ${gridColumn} gap-8 md:gap-4 auto-cols-max`}>
    {isMobile && <h2 className='col-span-full text-xl text-yellow-500 font-semibold'>Gérer la ruche {name}</h2>}
    {sensorValues.map(({ key, value }) => <HiveMetric
      key={key}
      name={key as keyof typeof logoIcons}
      value={value}
    />)}
  </div>
}
