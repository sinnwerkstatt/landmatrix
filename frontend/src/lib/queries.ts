import type { LoadEvent } from "@sveltejs/kit"
import { error } from "@sveltejs/kit"

export async function pageQuery(url: URL, fetch: LoadEvent["fetch"]) {
  const page_url =
    url.pathname === "/wagtail-preview"
      ? `/api/wagtail/v2/page_preview/1/?content_type=${encodeURIComponent(
          url.searchParams.get("content_type") ?? "",
        )}&token=${encodeURIComponent(url.searchParams.get("token") ?? "")}&format=json`
      : `/api/wagtail/v2/pages/find/?html_path=${url.pathname}`

  const res = await fetch(page_url, { headers: { Accept: "application/json" } })
  if (!res.ok) error(res.status, (await res.json()).message)

  return await res.json()
}
