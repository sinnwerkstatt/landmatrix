import type { LoadEvent } from "@sveltejs/kit";
import { RESTEndpoint } from "$lib/index";

export async function pageQuery(url: URL, fetch: LoadEvent["fetch"]) {
  const page_url =
    url.pathname === "/wagtail-preview"
      ? `${RESTEndpoint}/page_preview/1/?content_type=${encodeURIComponent(
          url.searchParams.get("content_type") ?? ""
        )}&token=${encodeURIComponent(url.searchParams.get("token") ?? "")}&format=json`
      : `${RESTEndpoint}/pages/find/?html_path=${url.pathname}`;

  const res = await fetch(page_url, { headers: { Accept: "application/json" } });
  if (!res.ok)
    return { status: res.status, error: new Error((await res.json()).message) };

  return await res.json();
}
