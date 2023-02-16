import { ApiError } from "../generated"

export default function ErrorBoxComponent({ error, className = '' }: {
  error: ApiError,
  className?: string
}) {
  return <div className={`${className} p-2 bg-red-200 border-l border-red-700`}>
    <h2 className="mb-2 text-xl text-red-500 font-semibold">{error.statusText}</h2>
    <p className="text-red-900">{error.body.detail}</p>
  </div>
}
