import { useLoaderData } from "react-router-dom"
import HiveListSelectorComponent from "../components/hive-list-selector.component"
import { BehiveOut } from "../generated"
import { getHives } from "../services/hive.service"

export async function loader() {
  return getHives()
}

export default function HivePageIndex() {
  const hives = useLoaderData() as BehiveOut[]

  return <>
    <h2 className="mb-8 text-xl text-yellow-500 font-semibold">Gérer mes ruches</h2>
    <HiveListSelectorComponent hives={hives} />
  </>

}
