import { NavigateFunction } from 'react-router-dom'
import { TokensService } from '../generated'
import { cookieSetValue } from './cookie.service'

export async function postLogin(username: string, password: string) {
  return TokensService.loginForAccessTokenApiTokenPost({
    formData: { username, password }
  })
}

export function logout(navigate: NavigateFunction) {
  cookieSetValue('session', '', { 'max-age': '0', 'samesite': 'strict' })
  navigate('/login')
}
