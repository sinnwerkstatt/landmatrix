<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import type { WagtailPage } from "$lib/types/wagtail";
  import { RESTEndpoint } from "$lib";

  export const load: Load = async ({ url, fetch }) => {
    const page_url =
      url.pathname === "/wagtail-preview"
        ? `${RESTEndpoint}/page_preview/1/?content_type=${encodeURIComponent(
            url.searchParams.get("content_type")
          )}&token=${encodeURIComponent(url.searchParams.get("token"))}&format=json`
        : `${RESTEndpoint}/pages/find/?html_path=${url.pathname}`;

    const res = await fetch(page_url, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok)
      return { status: res.status, error: new Error((await res.json()).message) };

    let page = await res.json();
    return { props: { page } };
  };
</script>

<script lang="ts">
  import BasePage from "$views/BasePage.svelte";
  import ObservatoryPage from "$views/ObservatoryPage.svelte";

  export let page: WagtailPage;

  $: wagtailPage = {
    WagtailRootPage: BasePage,
    WagtailPage: BasePage,
    ObservatoryPage: ObservatoryPage,
  }[page.meta.type.split(".")[1]];
</script>

<svelte:head>
  <title>{page.title}</title>
</svelte:head>

{#if wagtailPage}
  <svelte:component this={wagtailPage} {page} />
{:else}
  Dieser Seitentyp existiert nicht: {page.meta.type.split(".")[1]}
{/if}
