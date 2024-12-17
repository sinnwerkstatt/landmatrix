import type { RequestHandler } from "./$types"

export const trailingSlash = "ignore"

// https://sentry.sinnwerkstatt.com/organizations/sentry/issues/5223
// TODO: Add error handler
// NOTE: Using svelte fetch will results in an endless loop, why?
export const GET: RequestHandler = async ({ url, locals }) => {
  return await fetch(url.href, {
    credentials: "include",
    headers: { Cookie: locals.cookie },
  })
}
