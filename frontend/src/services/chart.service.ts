import { ChartProps } from "react-chartjs-2"
import { formatDate } from "./date.service"

export type ApiSensorResponse = Record<string, { updatedAt: string, value: number }[]>
type ChartData = ChartProps<'line'>['data'] | ChartProps<'bar'>['data']

const borderColors = ['#da7e4b', '#868b91']
const backgroundOpacity = (chartType: 'line' | 'bar') => chartType === 'bar' ? 1 : 0.1
const backgroundColors = (chartType: 'line' | 'bar') => [
  `rgba(225, 185, 134, ${backgroundOpacity(chartType)})`,
  `rgba(136, 174, 236, ${backgroundOpacity(chartType)})`
]

export function apiSensorResponseToChartData(chartType: 'line' | 'bar', apiResponse: ApiSensorResponse): ChartData {
  const keys = Object.keys(apiResponse)

  return {
    labels: apiResponse[keys[0]].map(data => formatDate(new Date(data.updatedAt))),
    datasets: keys.map((label, i) => ({
      label,
      data: apiResponse[label].map(data => data.value),
      borderColor: borderColors[i],
      backgroundColor: backgroundColors(chartType)[i],
      lineTension: 0.2, // smooth graph
      fill: true
    }))
  }
}
