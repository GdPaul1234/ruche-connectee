import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, TimeScale, LineElement, Filler, Title, Tooltip, Legend } from 'chart.js'
import { ChartProps, Line } from 'react-chartjs-2'
import 'chartjs-adapter-luxon'

ChartJS.register(CategoryScale, TimeScale, LinearScale, PointElement, LineElement, Filler, Title, Tooltip, Legend)

export const defaultOptions: ChartProps<'line'>['options'] = {
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

export default function ChartLineComponent({ options = defaultOptions, data }: {
  options?: ChartProps<'line'>['options']
  data: ChartProps<'line'>['data']
}) {
  return <div className="relative h-96 lg:h-[400px] 2xl:h-[500px]">
    <Line options={options} data={data} />
  </div>
}
