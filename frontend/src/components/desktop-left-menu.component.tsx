import IconComponent from "./icon.component";
import logo from '../ressources/ruche.png'

type Hive = {
  id: number
  name: string
}

interface Props {
  hives: Hive[]
  className?: string
}

function HiveListComponent({ hives }: Props) {

  return <ul className="flex flex-col gap-4">
    {hives.map(hive => <li className="flex" key={hive.id}>
      <IconComponent className="rounded-l-lg flex-none" logo={logo} small />
      <div className="w-full rounded-r-lg px-2 bg-amber-100">
        <div>{hive.name}</div>
        <div className="text-sm font-medium text-slate-700">Subtitle</div>
      </div>
    </li>)}
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
