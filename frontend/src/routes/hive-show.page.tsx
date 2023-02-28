import { useContext } from "react"
import { Outlet, useLoaderData, useLocation } from "react-router-dom"

import { ViewportContext } from "../components/contexts/viewport.context"
import HiveMetricsComponent from "../components/hive-metrics.component"

import { getHive, sensorTypeValues } from "../services/hive.service"
import { BehiveOut } from "../generated"

type LoaderArgs = {
  params: Partial<Record<'hiveId', string>>
}

export async function loader({ params }: LoaderArgs) {
  if (params.hiveId) return getHive(params.hiveId)
}

export default function HivePage() {
  const hive = useLoaderData() as BehiveOut

  const location = useLocation()
  const { isMobile } = useContext(ViewportContext)

  const shouldShowMetrics = !isMobile || !sensorTypeValues.some(sensor => location.pathname.includes(`/${sensor}`))

  return <div className="md:mt-7">
    {shouldShowMetrics && <HiveMetricsComponent name={hive.name} sensors={hive.last_metrics} />}
    <Outlet />
  </div>
}
