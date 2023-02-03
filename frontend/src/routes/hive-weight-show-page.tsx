import { getHiveWeight } from "../services/hive.service"
import { HiveBaseSensorPage, sensorLoader, SensorLoaderArgs } from "../components/hive-sensor-chart-page.component"

export const loader = (loaderArgs: SensorLoaderArgs) => sensorLoader(getHiveWeight, loaderArgs)
export const HiveWeightPage = () => <HiveBaseSensorPage chartType="line" />
