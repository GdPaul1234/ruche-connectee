import { useLoaderData, useNavigate, useSearchParams } from "react-router-dom"
import { DateRangeSelectorComponent } from "../components/date-range-selector.component"

import { ChartLineComponent } from "../components/chart-line.component"
import { apiSensorResponseToChartData } from "../services/chart.service"
import { getHiveHumidity, TemperatureHumidityResponse } from "../services/hive.service"
import { initDateRangeState, useNavigateOnDateRange } from "../hooks/date-range.hook"

type LoaderArgs = {
  request: Request
  params: Partial<Record<'hiveId', string>>
}

export async function loader({ request, params }: LoaderArgs) {
  const url = new URL(request.url)
  const start = url.searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)
  const stop = url.searchParams.get('end') || Date.now()

  if (params.hiveId) return getHiveHumidity(+params.hiveId, +start, +stop)
}

export default function HiveHumidityPage() {
  const [searchParams] = useSearchParams()
  const temperatures = useLoaderData() as TemperatureHumidityResponse
  const temperatureData = apiSensorResponseToChartData(temperatures)

  const navigate = useNavigate()

  const state = initDateRangeState({
    start: new Date(searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)),
    end: new Date(searchParams.get('end') || Date.now())
  })

  const onDateRangeChange = useNavigateOnDateRange(state, navigate)

  return <article className="w-full">
    <DateRangeSelectorComponent state={state} setState={newState => onDateRangeChange(newState)} />
    <ChartLineComponent data={temperatureData} />
  </article>
}
