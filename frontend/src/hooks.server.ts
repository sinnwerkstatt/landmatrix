import type { Handle } from "@sveltejs/kit"

import { supportedLanguages } from "$lib/i18n/i18n"

const langRE = /django_language=(.*?)($|;| )/

function checkBrowserLanguages(request: Request): string {
  let languages
  try {
    languages = request.headers
      ?.get("accept-language")
      ?.split(",")
      ?.map(l => {
        return l.split(";")[0]
      }) ?? ["en"]
  } catch {
    languages = ["en"]
  }
  for (const language of languages)
    for (const supportedLanguage of supportedLanguages)
      if (language.startsWith(supportedLanguage)) return supportedLanguage
  return "en"
}

export const handle: Handle = async ({ event, resolve }) => {
  let lang = checkBrowserLanguages(event.request)

  const cookies = event.request.headers.get("cookie") ?? undefined
  if (cookies) {
    event.locals.cookie = cookies
    const match = event.locals.cookie.match(langRE)
    lang = match?.[1] ?? "en"
  }
  event.locals.locale = lang

  return resolve(event, {
    // filterSerializedResponseHeaders: name => name === "content-type",
    filterSerializedResponseHeaders(name) {
      // SvelteKit doesn't serialize any headers on server-side fetches by default but openapi-fetch uses this header for empty responses.
      return name === "content-length"
    },
  })
}
