import React from 'react'
import ReactDOM from 'react-dom/client'
import reportWebVitals from './reportWebVitals'
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import './index.css'

import Root from './routes/root'
import HivePage, { loader as hiveLoader } from './routes/hive-show.page'
import HivePageIndex from './routes/hive-index.page'

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
          { path: 'temperature', element: <div>Temperature</div> },
          { path: 'humidity', element: <div>Humidity</div> },
          { path: 'weight', element: <div>Weight</div> },
          { path: 'battery', element: <div>Battery</div> },
          { path: 'alert', element: <div>Alert</div> }
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
