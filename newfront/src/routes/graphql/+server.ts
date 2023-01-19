import type { RequestHandler } from "./$types"

export const trailingSlash = "ignore"

export const POST: RequestHandler = async ({ request, url, locals }) => {
  const req = await request.text()
  return await fetch(url.href, {
    method: "POST",
    body: req,
    credentials: "include",
    headers: {
      Accept: "application/graphql+json, application/json",
      "Content-Type": "application/json",
      Cookie: locals.cookie,
    },
  })
}
