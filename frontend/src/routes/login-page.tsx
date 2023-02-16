import { Form, redirect, useRouteError } from "react-router-dom"
import ErrorBoxComponent from "../components/error-box.component"
import { ApiError, OpenAPI } from "../generated"

import website_logo from '../ressources/logo192.png'
import { cookieSetValue } from "../services/cookie.service"
import { postLogin } from "../services/login.service"

export async function action({ request }: {
  request: Request
}) {
  const formData = await request.formData()

  const response = await postLogin(
    formData.get("username") as string,
    formData.get("password") as string
  )

  OpenAPI.TOKEN = response.access_token
  cookieSetValue('session', OpenAPI.TOKEN, { 'max-age': '1800', 'samesite': 'strict' })

  return redirect('/')
}

export default function LoginPage() {
  const error = useRouteError() as ApiError

  const labelClassName = "block mb-2"
  const inputClassName = "w-full border border-gray-300 px-3 py-2 rounded-md text-gray-900 focus:z-10 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"

  return <main className="max-w-sm mx-6 md:mx-auto">
    <div className="flex flex-col items-center">
      <img className="w-32 h-32" src={website_logo} alt="Superhive logo" />
      <h1 className="text-2xl text-center m-[-8px]">Se connecter à votre compte Superhive</h1>
    </div>

    {error && <ErrorBoxComponent className="mt-8" error={error} />}

    <Form className="mt-8" method="post">
      <div>
        <label className={labelClassName} htmlFor="username">Nom d'utilisateur</label>
        <input className={inputClassName} required type="text" name="username" id="username" />
      </div>

      <div className="mt-4">
        <label className={labelClassName} htmlFor="password">Mot de passe</label>
        <input className={inputClassName} required type="password" name="password" id="password" />
      </div>

      <button type="submit" className="mt-6 w-full rounded-md hover:bg-gray-400 bg-gray-200 p-2">Connexion</button>
    </Form>
  </main>
}
