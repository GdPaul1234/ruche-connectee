import { useLoaderData, useSearchParams } from "react-router-dom"

import { ChartLineComponent } from "../components/chart-line.component"
import { apiSensorResponseToChartData } from "../services/chart.service"
import { getHiveTemperature, TemperatureResponse } from "../services/hive.service"
import { useContext, useState } from "react"
import { ViewportContext } from "../components/contexts/viewport.context"


import { DateRangePropsSelector, DateRangeSelectorComponent } from "../components/date-range-selector.component"

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
  const temperatureData = apiSensorResponseToChartData(temperatures)

  const [state, setState] = useState<DateRangePropsSelector['state']>([
    {
      startDate: new Date(searchParams.get('start') || (Date.now() - 7 * 24 * 3600)),
      endDate: new Date(searchParams.get('end') || Date.now()),
      key: 'selection'
    }
  ])

  const { isMobile } = useContext(ViewportContext)


  return <article className="w-full">
    <DateRangeSelectorComponent state={state} setState={setState} />
    <ChartLineComponent data={temperatureData} />
  </article>
}
