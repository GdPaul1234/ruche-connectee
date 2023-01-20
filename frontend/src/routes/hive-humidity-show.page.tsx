import { useLoaderData, useNavigate, useSearchParams } from "react-router-dom"

import { ChartLineComponent } from "../components/chart-line.component"
import { apiSensorResponseToChartData } from "../services/chart.service"
import { getHiveHumidity, TemperatureHumidityResponse } from "../services/hive.service"
import { useState } from "react"


import { DateRangePropsSelector, DateRangeSelectorComponent } from "../components/date-range-selector.component"

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
  const [searchParams, setSearchParams] = useSearchParams()
  const temperatures = useLoaderData() as TemperatureHumidityResponse
  const temperatureData = apiSensorResponseToChartData(temperatures)

  const navigate = useNavigate()

  const [state, setState] = useState<DateRangePropsSelector['state']>([
    {
      startDate: new Date(searchParams.get('start') || (Date.now() - 7 * 24 * 3600 * 1000)),
      endDate: new Date(searchParams.get('end') || Date.now()),
      key: 'selection'
    }
  ])

  function onDateRangeChange(newState: typeof state) {
    const params = {
      start: newState[0].startDate!.getTime().toFixed(),
      stop: newState[0].endDate!.getTime().toFixed()
    } as const

    setSearchParams(params)
    setState(newState)
    navigate(`?${searchParams.toString()}`)
  }

  return <article className="w-full">
    <DateRangeSelectorComponent state={state} setState={newState => onDateRangeChange(newState)} />
    <ChartLineComponent data={temperatureData} />
  </article>
}
