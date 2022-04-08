<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { pageQuery } from "$lib/queries";
  import type { WagtailPage } from "$lib/types/wagtail";

  export const load: Load = async ({ url }) => {
    const page = await pageQuery(url);
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
  }[page.meta?.type.split(".")[1]];
</script>

<svelte:head>
  <title>{page.title}</title>
</svelte:head>

{#if wagtailPage}
  <svelte:component this={wagtailPage} {page} />
{:else}
  Dieser Seitentyp existiert nicht: {page?.meta?.type}
{/if}
