import { Outlet } from "react-router-dom";
import DesktopLeftMenuComponent from "../components/desktop-left-menu.component";

export default function Root() {
  return <main className="container mx-auto grid grid-cols-6 lg:grid-cols-12 gap-2">
    <DesktopLeftMenuComponent className="col-span-2" hives={Array.from({ length: 3 }, (_, i) => ({ name: `Ruche ${i + 1}`, id: i }))} />
    <div className="col-span-4 lg:col-span-10">
      <Outlet />
    </div>
  </main>
}
