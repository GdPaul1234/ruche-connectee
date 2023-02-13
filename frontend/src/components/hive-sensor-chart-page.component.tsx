import { useLoaderData, useNavigate, useSearchParams } from "react-router-dom"
import { DateRangeSelectorComponent } from "../components/date-range-selector.component"

import { ApiSensorResponse, apiSensorResponseToChartData } from "../services/chart.service"
import { initDateRangeState, useNavigateOnDateRange } from "../hooks/date-range.hook"
import { lazy } from "react"
import { ChartProps } from "react-chartjs-2"

export type SensorLoaderArgs = {
  request: Request
  params: Partial<Record<'hiveId', string>>
}

type LoaderFetcher = (hiveId: string, fromDate: Date, toDate: Date) => unknown

export async function sensorLoader(fetcher: LoaderFetcher, { request, params }: SensorLoaderArgs) {
  const url = new URL(request.url)
  const start = new Date(+(url.searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)))
  const end = new Date(+(url.searchParams.get('end') || Date.now()))

  if (params.hiveId) return fetcher(params.hiveId, start, end)
}

const ChartLine = lazy(() => import("./chart-line.component"))
const ChartBar = lazy(() => import("./chart-bar.component"))

export function HiveBaseSensorPage({ chartType, footerChildren }: {
  chartType: 'line' | 'bar'
  footerChildren?: (sensorResponse: ApiSensorResponse) => React.ReactNode
}) {
  const [searchParams] = useSearchParams()
  const sensorRawValues = useLoaderData() as ApiSensorResponse
  const sensorChartData = apiSensorResponseToChartData(chartType, sensorRawValues)

  const navigate = useNavigate()

  const state = initDateRangeState({
    start: new Date(searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)),
    end: new Date(searchParams.get('end') || Date.now())
  })

  const onDateRangeChange = useNavigateOnDateRange(state, navigate)

  return <article className="w-full mt-1">
    <section className="flex justify-center pt-2 pb-4 bg-white rounded-b-lg sticky top-0 z-10">
      <DateRangeSelectorComponent state={state} setState={newState => onDateRangeChange(newState)} />
    </section>

    <section>
      {chartType === 'line' && <ChartLine data={sensorChartData as ChartProps<'line'>['data']} />}
      {chartType === 'bar' && <ChartBar data={sensorChartData as ChartProps<'bar'>['data']} />}
    </section>

    <section className="mt-4">
      {footerChildren && footerChildren(sensorRawValues)}
    </section>
  </article>
}
