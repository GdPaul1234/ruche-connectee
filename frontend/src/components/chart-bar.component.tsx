import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, BarElement, Filler, Title, Tooltip, Legend } from 'chart.js'
import { ChartProps, Bar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, PointElement, BarElement, Filler, Title, Tooltip, Legend)

export const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' as const },
  }
}

export default function ChartBarComponent({ options = defaultOptions, data }: {
  options?: ChartProps<'bar'>['options']
  data: ChartProps<'bar'>['data']
}) {
  return <div className="relative h-64 lg:h-[200px] xl:h-[240px]">
    <Bar options={options} data={data} />
  </div>
}
