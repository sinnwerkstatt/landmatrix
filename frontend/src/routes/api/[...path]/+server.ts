import type { RequestHandler } from "./$types"

export const trailingSlash = "ignore"

export const GET: RequestHandler = async ({ url, locals }) => {
  return await fetch(url.href, {
    credentials: "include",
    headers: { Cookie: locals.cookie },
  })
}
