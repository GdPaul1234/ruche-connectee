import { useLoaderData, useNavigate, useSearchParams } from "react-router-dom"
import { DateRangeSelectorComponent } from "../components/date-range-selector.component"

import { ApiSensorResponse, apiSensorResponseToChartData } from "../services/chart.service"
import { initDateRangeState, useNavigateOnDateRange } from "../hooks/date-range.hook"
import { lazy } from "react"

export type SensorLoaderArgs = {
  request: Request
  params: Partial<Record<'hiveId', string>>
}

type LoaderFetcher = (hiveId: number, start: number, stop: number) => unknown

export async function sensorLoader(fetcher: LoaderFetcher, { request, params }: SensorLoaderArgs) {
  const url = new URL(request.url)
  const start = url.searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)
  const stop = url.searchParams.get('end') || Date.now()

  if (params.hiveId) return fetcher(+params.hiveId, +start, +stop)
}

const ChartLine = lazy(() => import("./chart-line.component"))

export function HiveBaseSensorPage({ chartType }: {
  chartType: 'line'
}) {
  const [searchParams] = useSearchParams()
  const sensorRawValues = useLoaderData() as ApiSensorResponse
  const sensorChartData = apiSensorResponseToChartData(sensorRawValues)

  const navigate = useNavigate()

  const state = initDateRangeState({
    start: new Date(searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)),
    end: new Date(searchParams.get('end') || Date.now())
  })

  const onDateRangeChange = useNavigateOnDateRange(state, navigate)

  return <article className="w-full">
    <DateRangeSelectorComponent state={state} setState={newState => onDateRangeChange(newState)} />

    {chartType === 'line' && <ChartLine data={sensorChartData} />}
  </article>
}
