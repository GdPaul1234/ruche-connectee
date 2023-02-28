import { UsersService } from "../generated";

export async function getUserInformation() {
  return UsersService.readUsersMeApiUsersMeGet()
}
