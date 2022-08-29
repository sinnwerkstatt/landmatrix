import type { LoadEvent } from "@sveltejs/kit"
import { error } from "@sveltejs/kit"

const RESTEndpoint = `${import.meta.env.VITE_BASE_URL}/wagtailapi/v2`

export async function pageQuery(url: URL, fetch: LoadEvent["fetch"]) {
  const page_url =
    url.pathname === "/wagtail-preview"
      ? `${RESTEndpoint}/page_preview/1/?content_type=${encodeURIComponent(
          url.searchParams.get("content_type") ?? "",
        )}&token=${encodeURIComponent(url.searchParams.get("token") ?? "")}&format=json`
      : `${RESTEndpoint}/pages/find/?html_path=${url.pathname}`

  const res = await fetch(page_url, { headers: { Accept: "application/json" } })
  if (!res.ok) throw error(res.status, (await res.json()).message)

  return await res.json()
}
