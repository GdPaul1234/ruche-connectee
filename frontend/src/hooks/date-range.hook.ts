import { NavigateFunction, useSearchParams } from "react-router-dom"
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
  const [searchParams, setSearchParams] = useSearchParams()

  function onDateRangeChange(newState: typeof state) {
    const params = {
      start: newState[0].startDate!.getTime().toFixed(),
      stop: newState[0].endDate!.getTime().toFixed()
    } as const

    setSearchParams(params)
    navigate(`?${searchParams.toString()}`)
  }

  return onDateRangeChange
}
