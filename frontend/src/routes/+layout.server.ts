import type { LayoutServerLoad } from "./$types"

export const trailingSlash = "always"

export const load: LayoutServerLoad = async event => {
  return { locale: event.locals.locale }
}
