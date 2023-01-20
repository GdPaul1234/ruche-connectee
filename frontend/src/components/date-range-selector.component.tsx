import React, { useState, useContext } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { DateRange, DateRangePicker } from 'react-date-range'
import { ViewportContext } from './contexts/viewport.context'

import 'react-date-range/dist/styles.css'
import 'react-date-range/dist/theme/default.css'
import { formatDate } from '../services/date.service'

export type DateRangePropsSelector = {
  state: { startDate?: Date, endDate?: Date, key?: string }[],
  setState: (state: DateRangePropsSelector['state']) => void
}

function Button(props: React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>) {
  return <button {...props} className={`${props.className} rounded-md hover:bg-gray-400 bg-gray-200 p-2`} />
}

export function DateRangeSelectorComponent({ state: propState, setState: propSetState }: DateRangePropsSelector) {
  const [isOpen, setIsOpen] = useState(false)
  const [state, setState] = useState(propState)

  const { isMobile } = useContext(ViewportContext)

  function onSelectionChange(newState: typeof state) {
    setState(newState)
  }

  function handleValidate() {
    propSetState(state)
    setIsOpen(false)
  }

  return <>
    <div className="flex justify-center">
      <Button className='' onClick={() => setIsOpen(true)}>
        {[state[0].startDate, state[0].endDate].map(date => formatDate(date!)).join(' - ')}
      </Button>
    </div>

    <Transition appear show={isOpen} as={React.Fragment}>
      <Dialog as="div" className="relative z-10" open={isOpen} onClose={() => setIsOpen(false)}>
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className='mx-auto p-4 rounded-xl drop-shadow-xl bg-white'>
            <Dialog.Title className='mb-4 text-xl'>Sélection de la période</Dialog.Title>
            {!isMobile && <DateRangePicker
              onChange={item => onSelectionChange([item.selection])}
              moveRangeOnFirstSelection={false}
              months={2}
              ranges={state}
              direction={'horizontal'}
            />}
            {isMobile && <DateRange
              onChange={item => onSelectionChange([item.selection])}
              moveRangeOnFirstSelection={false}
              ranges={state}
            />}

            <div className="flex w-full justify-center">
              <Button onClick={handleValidate}>Valider</Button>
            </div>
          </Dialog.Panel>
        </div>
      </Dialog>
    </Transition>
  </>


}
