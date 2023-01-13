import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { ChartProps, Line } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export const defaultOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' as const },
  },
}

export function ChartLineComponent({ options = defaultOptions, data }: {
  options?: ChartProps<'line'>['options']
  data: ChartProps<'line'>['data']
}) {
  return <div className="relative">
    <Line options={options} data={data} />
  </div>
}
