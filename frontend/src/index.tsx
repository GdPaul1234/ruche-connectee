import React from 'react'
import ReactDOM from 'react-dom/client'
import reportWebVitals from './reportWebVitals'
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import './index.css'

import Root from './routes/root'
import HivePage, { loader as hiveLoader } from './routes/hive-show.page'
import HivePageIndex from './routes/hive-index.page'
import HiveTemperaturePage, { loader as hiveTemperatureLoader } from './routes/hive-temperature-show.page'
import HiveHumidityPage, { loader as hiveHumidityLoader } from './routes/hive-humidity-show.page'
import HiveWeightPage, { loader as hiveWeightLoader } from './routes/hive-weight-show-page'
import HiveBatteryPage, { loader as hiveBatteryLoader } from './routes/hive-battery-show-page'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
)

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    children: [
      {
        path: 'hives',
        element: <HivePageIndex />
      },
      {
        path: 'hives/:hiveId',
        element: <HivePage />,
        loader: hiveLoader,
        children: [
          { path: 'temperature', element: <HiveTemperaturePage />, loader: hiveTemperatureLoader },
          { path: 'humidity', element: <HiveHumidityPage />, loader: hiveHumidityLoader },
          { path: 'weight', element: <HiveWeightPage />, loader: hiveWeightLoader },
          { path: 'battery', element: <HiveBatteryPage />, loader: hiveBatteryLoader },
          { path: 'alert', element: <div>Alert</div> },
          { path: '*', element: <div>Alert</div>, index: true }
        ]
      }
    ]
  }
])

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
