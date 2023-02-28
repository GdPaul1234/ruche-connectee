import { NavigateFunction } from "react-router-dom"
import { DateRangePropsSelector } from "../components/date-range-selector.component"

export function initDateRangeState(initialState: Record<"start" | "end", Date>) {
  return [
    {
      startDate: initialState.start,
      endDate: initialState.end,
      key: 'selection'
    }
  ]
}

export function useNavigateOnDateRange(
  state: DateRangePropsSelector['state'],
  navigate: NavigateFunction
) {
  function onDateRangeChange(newState: typeof state) {
    const searchParams = new URLSearchParams()
    searchParams.append('start', newState[0].startDate!.getTime().toFixed())
    searchParams.append('end', newState[0].endDate!.getTime().toFixed())
    navigate(`?${searchParams.toString()}`)
  }

  return onDateRangeChange
}
