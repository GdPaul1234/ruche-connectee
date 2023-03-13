import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, TimeScale, LineElement, Filler, Title, Tooltip, Legend } from 'chart.js'
import { ChartProps, Scatter } from 'react-chartjs-2'
import 'chartjs-adapter-luxon'
import { ScatterChartData } from '../services/chart.service'

ChartJS.register(CategoryScale, TimeScale, LinearScale, PointElement, LineElement, Filler, Title, Tooltip, Legend)

export const defaultOptions: ChartProps<'scatter'>['options'] = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
  },
  scales: {
    x: {
      type: 'time',
      time: {
        tooltipFormat: 'DD T',
        displayFormats: { hour: 'd LLL, T' }
      }
    },
    y: { beginAtZero: true }
  }
}

export default function ChartScatterLineComponent({ options = defaultOptions, data }: {
  options?: ChartProps<'scatter'>['options']
  data: ScatterChartData
}) {
  return <div className="relative h-96 lg:h-[400px] 2xl:h-[500px]">
    <Scatter options={options} data={data} />
  </div>
}
