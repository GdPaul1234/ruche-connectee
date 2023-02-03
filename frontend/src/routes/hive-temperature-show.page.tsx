import { getHiveTemperature } from "../services/hive.service"
import { HiveBaseSensorPage, sensorLoader, SensorLoaderArgs } from "../components/hive-sensor-chart-page.component"

export const loader = (loaderArgs: SensorLoaderArgs) => sensorLoader(getHiveTemperature, loaderArgs)
export const HiveTemperaturePage = () => <HiveBaseSensorPage chartType="line" />

