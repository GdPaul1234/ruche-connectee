import IconComponent from "./icon.component";
import logo from '../ressources/ruche.png'
import { NavLink, useLocation } from "react-router-dom";

type Hive = {
  id: number
  name: string
}

interface Props {
  hives: Hive[]
  className?: string
}

function HiveListItemComponent({ id, name }: Props['hives'][number]) {
  const location = useLocation()
  const isActive = location.pathname.includes(`/hives/${id}`)

  return <li className={`rounded-md ${isActive && 'border border-indigo-600'}`}>
    <NavLink to={`/hives/${id}`} className="flex" >
      <IconComponent small hoverable active={isActive} className="rounded-l-lg flex-none" logo={logo} />
      <div className={`w-full rounded-r-lg px-2 ${isActive ? 'bg-amber-200' : 'bg-amber-100'}`}>
        <div>{name}</div>
        <div className="text-sm font-medium text-slate-700">Subtitle</div>
      </div>
    </NavLink>
  </li>
}

function HiveListComponent({ hives }: Props) {
  return <ul className="flex flex-col gap-4">
    {hives.map(hive => <HiveListItemComponent key={hive.id} {...hive} />)}
  </ul>
}

export default function DesktopLeftMenuComponent({ hives, className }: Props) {
  return <header className={`mt-4 p-2 ${className}`}>
    <h1 className=" text-2xl ">Bonjour Paul</h1>
    <div className="mb-2 text-slate-700">{new Date().toLocaleDateString(navigator.language, { dateStyle: 'medium' })}</div>

    <h2 className="mb-4 text-xl text-yellow-500 font-semibold">Mes ruches</h2>
    <HiveListComponent hives={hives} />
  </header>
}
