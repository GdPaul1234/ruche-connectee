import { Disclosure } from "@headlessui/react"
import { ChevronUpIcon } from '@heroicons/react/20/solid'

import { getAlertResponse, AlertResponse } from "../services/hive.service"
import { HiveBaseSensorPage, sensorLoader, SensorLoaderArgs } from "../components/hive-sensor-chart-page.component"
import { formatDate } from "../services/date.service"

export const loader = (loaderArgs: SensorLoaderArgs) => sensorLoader(getAlertResponse, loaderArgs)
export function HiveAlertPage() {
  return <HiveBaseSensorPage
    chartType="bar"
    footerChildren={rawValue => <HiveAlertFooter sensorRawValue={rawValue as AlertResponse} />} />
}

function HiveAlertFooter({ sensorRawValue }: {
  sensorRawValue: AlertResponse
}) {
  return <>
    {sensorRawValue.alert
      .filter(_ => _.value > 0)
      .map(rawValue => <section key={rawValue.updatedAt} className="mb-4">
        <Disclosure>
          {({ open }) => (
            <>
              <Disclosure.Button className="flex w-full justify-between rounded-lg bg-gray-100 px-4 py-2 text-left text-sm font-medium text-slate-700 hover:bg-gray-200 focus:outline-none focus-visible:ring focus-visible:ring-gray-500 focus-visible:ring-opacity-75">
                <h3 className="text-xl font-semibold">
                  {formatDate(new Date(rawValue.updatedAt), { dateStyle: 'full' })} ({rawValue.value})
                </h3>
                <ChevronUpIcon
                  className={`${open ? 'rotate-180 transform' : ''} h-5 w-5`}
                />
              </Disclosure.Button>
              <Disclosure.Panel className="px-2 md:px-4 pt-4 pb-2">
                <ul>
                  {rawValue.messages.map(message => <li key={message.updatedAt} className="md:flex md:justify-between rounded-md bg-gray-50 p-2 mb-2">
                    <div className="font-semibold py-1">{message.type}</div>
                    <div className="py-1">{message.message}</div>
                    <div className="font-light py-1">{formatDate(new Date(message.updatedAt), { timeStyle: 'short' })}</div>
                  </li>)}
                </ul>
              </Disclosure.Panel>
            </>
          )}
        </Disclosure>
      </section>)}
  </>
}
