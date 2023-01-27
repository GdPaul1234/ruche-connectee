import { getAlertResponse } from "../services/hive.service"
import { HiveBaseSensorPage, sensorLoader, SensorLoaderArgs } from "../components/hive-sensor-chart-page.component"

export const loader = (loaderArgs: SensorLoaderArgs) => sensorLoader(getAlertResponse, loaderArgs)
export function HiveAlertPage() {
  return <HiveBaseSensorPage chartType="bar">
    children

    TODO: pass fetched data as props
  </HiveBaseSensorPage>
}
