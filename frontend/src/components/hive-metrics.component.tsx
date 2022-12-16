import { Hive } from '../services/hive.service'

import HumidityIcon from '../ressources/humidity_icon.png'
import TemperatureIcon from '../ressources/temperature_icon.png'
import WeightIcon from '../ressources/weight_icon.png'
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
      battery: BatteryIcon
    }
    return logoFinder[name]
  }

  return <section>
    <IconComponent rounded small logo={logoForMetricName()} />
    <div className="text-base md:text-sm w-28 md:w-16">
      <div className="text-ellipsis overflow-hidden">{name}</div>
      <div className="text-sm md:text-xs font-medium text-slate-700">{value} Met</div>
    </div>
  </section>
}

export default function HiveMetricsComponent({ sensors }: {
  sensors: Hive['sensors_values']
}) {
  return <div className="grid grid-flow-col gap-4 auto-cols-max">
    {Object.keys(sensors).map(key => <HiveMetric
      key={key}
      name={key as keyof Hive['sensors_values']}
      value={sensors[key as keyof Hive['sensors_values']]}
    />)}
  </div>
}
