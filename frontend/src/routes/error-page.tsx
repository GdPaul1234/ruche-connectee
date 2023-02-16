import { Link, useRouteError } from "react-router-dom"
import ErrorBoxComponent from "../components/error-box.component"
import { ApiError } from "../generated"

export default function ErrorPage() {
  const error = useRouteError() as ApiError

  return <main className="container m-8">
    <ErrorBoxComponent className="max-w-lg" error={error} />
    {error.status === 401 && <Link className="text-blue-800 underline" to="/login">Se connecter</Link>}
  </main>
}
