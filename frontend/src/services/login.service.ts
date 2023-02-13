import { TokensService } from '../generated/services/TokensService'

export async function postLogin(username: string, password: string) {
  return TokensService.loginForAccessTokenApiTokenPost({
    formData: { username, password }
  })
}
