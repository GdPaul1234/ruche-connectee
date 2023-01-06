import HiveListSelectorComponent from "../components/hive-list-selector.component"

export default function HivePageIndex() {
  const hives = Array.from({ length: 3 }, (_, i) => ({ name: `Ruche ${i + 1}`, id: i })) // TODO: use loader

  return <>
    <h2 className="mb-8 text-xl text-yellow-500 font-semibold">Gérer mes ruches</h2>
    <HiveListSelectorComponent hives={hives} />
  </>

}
