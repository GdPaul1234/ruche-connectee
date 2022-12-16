import { useLoaderData } from "react-router-dom"
import HiveMetricsComponent from "../components/hive-metrics.component"
import { getHive, Hive } from "../services/hive.service"

type LoaderArgs = {
  params: Partial<Record<'hiveId', string>>
}

export async function loader({ params }: LoaderArgs) {
  if (params.hiveId) return getHive(+params.hiveId)
}

export default function HivePage() {
  const hive = useLoaderData() as Hive

  return <div className="mt-7">
    <HiveMetricsComponent sensors={hive.sensors_values} />
  </div>
}
