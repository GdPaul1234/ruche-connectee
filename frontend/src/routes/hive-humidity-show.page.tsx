import { getHiveHumidity } from "../services/hive.service"
import { HiveBaseSensorPage, sensorLoader, SensorLoaderArgs } from "../components/hive-sensor-chart-page.component"

export const loader = (loaderArgs: SensorLoaderArgs) => sensorLoader(getHiveHumidity, loaderArgs)
export const HiveHumidityPage = () => <HiveBaseSensorPage chartType="scatter" />
