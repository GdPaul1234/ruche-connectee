import { lazy, Suspense } from "react"
import { Outlet, useLoaderData } from "react-router-dom"
import { useMediaQuery } from "usehooks-ts"
import { ViewportContext } from "../components/contexts/viewport.context"
import { getHives } from "../services/hive.service"
import { BehiveOut, User } from "../generated"
import { getUserInformation } from "../services/user.service"

const DesktopLeftMenuComponent = lazy(() => import("../components/desktop-left-menu.component"))
const MobileMainMenuComponent = lazy(() => import("../components/mobile-main-menu.component"))

export async function loader() {
  return {
    hives: await getHives(),
    user: await getUserInformation()
  }
}

export default function Root() {
  const isMobile = useMediaQuery('(max-width: 640px)')
  const { hives, user } = useLoaderData() as { hives: BehiveOut[], user: User }

  return <main className="container mx-auto grid grid-cols-2 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-12 gap-2">
    <ViewportContext.Provider value={{ isMobile }}>
      {!isMobile && <Suspense fallback={<div>Loading...</div>}>
        <DesktopLeftMenuComponent className="col-span-2" hives={hives} user={user} />
        <div className="md:col-start-3 md:col-end-7 lg:col-end-9 xl:col-end-13">
          <Outlet />
        </div>
      </Suspense>}

      {isMobile && <Suspense fallback={<div>Loading...</div>}>
        <MobileMainMenuComponent className="col-span-2 mx-8" hives={hives} />
        <div className="col-span-full mx-8">
          <Outlet />
        </div>
      </Suspense>}
    </ViewportContext.Provider>
  </main>

}
