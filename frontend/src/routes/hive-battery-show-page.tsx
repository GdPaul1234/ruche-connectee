import { getBatteryResponse } from "../services/hive.service"
import { HiveBaseSensorPage, sensorLoader, SensorLoaderArgs } from "../components/hive-sensor-chart-page.component"

export const loader = (loaderArgs: SensorLoaderArgs) => sensorLoader(getBatteryResponse, loaderArgs)
export const HiveBatteryPage = () => <HiveBaseSensorPage chartType="line" />
