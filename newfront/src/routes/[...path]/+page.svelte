<script lang="ts">
  import BasePage from "$views/BasePage.svelte";
  import ObservatoryPage from "$views/ObservatoryPage.svelte";
  import type { WagtailPage } from "$lib/types/wagtail";

  // import type { PageData } from "./$types";
  // export let data: PageData;
  export let data: {
    page: WagtailPage;
  };

  $: wagtailPage = {
    WagtailRootPage: BasePage,
    WagtailPage: BasePage,
    ObservatoryPage: ObservatoryPage,
  }[data.page.meta?.type.split(".")[1]];
</script>

<svelte:head>
  <title>{data.page.title}</title>
</svelte:head>

{#if wagtailPage}
  <svelte:component this={wagtailPage} page={data.page} />
{:else}
  Dieser Seitentyp existiert nicht: {data.page?.meta?.type}
{/if}
