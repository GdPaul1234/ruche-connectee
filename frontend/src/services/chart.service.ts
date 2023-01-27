import { ChartProps } from "react-chartjs-2"
import { formatDate } from "./date.service"

type ApiSensorResponse = Record<string, { updatedAt: string, value: number }[]>
type ChartData = ChartProps<'line'>['data']

const borderColors = ['#da7e4b', '#868b91']
const backgroundColors = ['rgba(225, 185, 134, 0.1)', 'rgba(136, 174, 236, 0.1)']

export function apiSensorResponseToChartData(apiResponse: ApiSensorResponse): ChartData {
  const keys = Object.keys(apiResponse)

  return {
    labels: apiResponse[keys[0]].map(data => formatDate(new Date(data.updatedAt))),
    datasets: keys.map((label, i) => ({
      label,
      data: apiResponse[label].map(data => data.value),
      borderColor: borderColors[i],
      backgroundColor: backgroundColors[i],
      fill: true
    }))
  }
}
