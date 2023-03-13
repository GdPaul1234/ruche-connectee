import { ChartProps } from "react-chartjs-2"
import { DateTime } from "luxon"
import 'chartjs-adapter-luxon'

import { SensorOut } from "../generated"

export type ApiSensorResponse = Record<string, SensorOut['values']>
export type SimpleChartData = ChartProps<'line'>['data'] | ChartProps<'bar'>['data']
export type ScatterChartData = ChartProps<'scatter', { x: DateTime, y: number }[]>['data']

const borderColors = ['#da7e4b', '#868b91']
const backgroundOpacity = (chartType: 'line' | 'bar') => chartType === 'bar' ? 1 : 0.1
const backgroundColors = (chartType: 'line' | 'bar') => [
  `rgba(225, 185, 134, ${backgroundOpacity(chartType)})`,
  `rgba(136, 174, 236, ${backgroundOpacity(chartType)})`
]

export function apiSensorResponseToChartData(chartType: 'line' | 'bar' | 'scatter', apiResponse: ApiSensorResponse) {
  if (chartType === 'scatter') return apiSensorResponseToScatterChartData(apiResponse)
  return apiSensorResponseToSimpleChartData(chartType, apiResponse)
}

function apiSensorResponseToSimpleChartData(chartType: 'line' | 'bar', apiResponse: ApiSensorResponse): SimpleChartData {
  const keys = Object.keys(apiResponse)

  return {
    labels: apiResponse[keys[0]].map(data => DateTime.fromISO(data.updated_at)),
    datasets: keys.map((label, i) => ({
      label,
      data: apiResponse[label].map(data => data.value),
      borderColor: borderColors[i],
      backgroundColor: backgroundColors(chartType)[i],
      lineTension: 0.2, // smooth graph
      fill: true
    }))
  } as SimpleChartData
}

function apiSensorResponseToScatterChartData(apiResponse: ApiSensorResponse): ScatterChartData {
  const keys = Object.keys(apiResponse)

  return {
    datasets: keys.map((label, i) => ({
      label,
      data: apiResponse[label].map(data => ({
        x: DateTime.fromISO(data.updated_at),
        y: data.value
      })),
      borderColor: borderColors[i],
      backgroundColor: backgroundColors('line')[i],
      lineTension: 0.2, // smooth graph
      showLine: true,
      fill: true
    }))
  } as ScatterChartData
}
