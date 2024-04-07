import type { LoadEvent, NumericRange } from "@sveltejs/kit"
import { error } from "@sveltejs/kit"

const WAGTAIL_API_BASE_URL = "/api/wagtail/v2"

export async function pageQuery(url: URL, fetch: LoadEvent["fetch"]) {
  const pageUrl = url.pathname.startsWith("/wagtail-preview")
    ? `/page_preview/1/?${url.searchParams}&format=json`
    : `/pages/find/?html_path=${url.pathname}`

  const res = await fetch(WAGTAIL_API_BASE_URL + pageUrl, {
    headers: { Accept: "application/json" },
  })
  const resJson = await res.json()
  if (!res.ok) error(res.status as NumericRange<400, 599>, resJson.message)

  return resJson
}
