import HiveListSelectorComponent, { Props } from './hive-list-selector.component'

export default function DesktopLeftMenuComponent({ hives, className }: Props) {
  return <header className={`mt-4 p-2 ${className}`}>
    <h1 className=' text-2xl '>Bonjour Paul</h1>
    <div className='mb-2 text-slate-700'>{new Date().toLocaleDateString(navigator.language, { dateStyle: 'medium' })}</div>

    <h2 className='mb-4 text-xl text-yellow-500 font-semibold'>Mes ruches</h2>
    <HiveListSelectorComponent hives={hives} />
  </header>
}
