import DesktopLeftMenuComponent from "../components/desktop-left-menu.component";

export default function Root() {
  return <main>
    <DesktopLeftMenuComponent hives={Array.from({ length: 3 }, (_, i) => ({ name: `Ruche ${i + 1}`, id: i }))} />
  </main>
}
