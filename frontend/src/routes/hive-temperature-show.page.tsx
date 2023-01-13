import { useLoaderData, useSearchParams } from "react-router-dom"
import { ChartLineComponent } from "../components/chart-line.component"
import { apiSensorResponseToChartData } from "../services/chart.service"
import { getHiveTemperature, TemperatureResponse } from "../services/hive.service"

type LoaderArgs = {
  request: Request
  params: Partial<Record<'hiveId', string>>
}

export async function loader({ request, params }: LoaderArgs) {
  const url = new URL(request.url)
  const start = url.searchParams.get('start') || (Date.now() - 7 * 24 * 3600)
  const stop = url.searchParams.get('end') || Date.now()

  if (params.hiveId) return getHiveTemperature(+params.hiveId, +start, +stop)
}

export default function HiveTemperaturePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const temperatures = useLoaderData() as TemperatureResponse

  const start = new Date(+searchParams.get('start')!)
  const end = new Date(+searchParams.get('end')!)
  const temperatureData = apiSensorResponseToChartData(temperatures)

  return <article className="w-full">
    <ChartLineComponent data={temperatureData} />
  </article>
}
