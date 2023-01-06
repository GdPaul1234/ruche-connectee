import { lazy, Suspense } from "react"
import { Outlet } from "react-router-dom"
import { useMediaQuery } from "usehooks-ts"
import { ViewportContext } from "../components/contexts/viewport.context"

const DesktopLeftMenuComponent = lazy(() => import("../components/desktop-left-menu.component"))
const MobileMainMenuComponent = lazy(() => import("../components/mobile-main-menu.component"))

export default function Root() {
  const isMobile = useMediaQuery('(max-width: 640px)')

  const hives = Array.from({ length: 3 }, (_, i) => ({ name: `Ruche ${i + 1}`, id: i }))

  return <main className="container mx-auto grid grid-cols-2 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-12 gap-2">
    <ViewportContext.Provider value={{ isMobile }}>
      {!isMobile && <Suspense fallback={<div>Loading...</div>}>
        <DesktopLeftMenuComponent className="col-span-2" hives={hives} />
        <div className="md:col-start-3 md:col-end-6 lg:col-end-8 xl:col-end-12">
          <Outlet />
        </div>
      </Suspense>}

      {isMobile && <Suspense fallback={<div>Loading...</div>}>
        <MobileMainMenuComponent className="col-span-2 mx-2" hives={hives} />
        <div className="col-span-full">
          <Outlet />
        </div>
      </Suspense>}
    </ViewportContext.Provider>
  </main>

}
