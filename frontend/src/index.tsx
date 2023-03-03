import React from 'react'
import ReactDOM from 'react-dom/client'
import reportWebVitals from './reportWebVitals'
import { createBrowserRouter, LoaderFunction, RouterProvider } from "react-router-dom"
import './index.css'

import Root, { loader as rootLoader } from './routes/root'
import HivePage, { loader as hiveLoader } from './routes/hive-show.page'
import HivePageIndex, { loader as hivesLoader } from './routes/hive-index.page'
import { HiveTemperaturePage, loader as hiveTemperatureLoader } from './routes/hive-temperature-show.page'
import { HiveHumidityPage, loader as hiveHumidityLoader } from './routes/hive-humidity-show.page'
import { HiveWeightPage, loader as hiveWeightLoader } from './routes/hive-weight-show-page'
import { HiveBatteryPage, loader as hiveBatteryLoader } from './routes/hive-battery-show-page'
import { HiveAlertPage, loader as hiveAlertLoader } from './routes/hive-alert-show-page'
import LoginPage, { action as loginAction } from './routes/login-page'

import { OpenAPI } from './generated/core/OpenAPI'
import { cookieGetValueByKey } from './services/cookie.service'
import ErrorPage from './routes/error-page'

OpenAPI.BASE = ''
OpenAPI.WITH_CREDENTIALS = true
OpenAPI.CREDENTIALS = 'include'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
)

function withAuthHeader(loader: LoaderFunction): LoaderFunction {
  OpenAPI.TOKEN = cookieGetValueByKey('session')
  return loader
}

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage />, action: loginAction, errorElement: <LoginPage /> },
  {
    path: '/', element: <Root />, loader: withAuthHeader(rootLoader), errorElement: <ErrorPage />,
    children: [
      { path: 'hives', element: <HivePageIndex />, loader: withAuthHeader(hivesLoader), errorElement: <ErrorPage /> },
      {
        path: 'hives/:hiveId', element: <HivePage />, loader: withAuthHeader(hiveLoader), errorElement: <ErrorPage />,
        children: [
          { path: 'temperature', element: <HiveTemperaturePage />, errorElement: <ErrorPage />, loader: withAuthHeader(hiveTemperatureLoader) },
          { path: 'humidity', element: <HiveHumidityPage />, errorElement: <ErrorPage />, loader: withAuthHeader(hiveHumidityLoader) },
          { path: 'weight', element: <HiveWeightPage />, errorElement: <ErrorPage />, loader: withAuthHeader(hiveWeightLoader) },
          { path: 'battery', element: <HiveBatteryPage />, errorElement: <ErrorPage />, loader: withAuthHeader(hiveBatteryLoader) },
          { path: 'alert', element: <HiveAlertPage />, errorElement: <ErrorPage />, loader: withAuthHeader(hiveAlertLoader) },
          { path: '*', element: <div>Sélectionner une rubrique pour commencer</div>, index: true }
        ]
      },
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
