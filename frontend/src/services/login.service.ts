import { TokensService } from '../generated'

export async function postLogin(username: string, password: string) {
  return TokensService.loginForAccessTokenApiTokenPost({
    formData: { username, password }
  })
}
