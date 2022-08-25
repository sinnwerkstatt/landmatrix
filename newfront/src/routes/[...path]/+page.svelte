<script lang="ts">
  import BasePage from "$views/BasePage.svelte";
  import ObservatoryPage from "$views/ObservatoryPage.svelte";
  import { locale } from "svelte-i18n";
  import { page } from "$app/stores";
  import { pageQuery } from "$lib/queries";
  import { loading } from "$lib/stores";
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

  let loadedLocale = $locale;

  async function reloadOnLocale(newLocale) {
    if (newLocale != loadedLocale) {
      loading.set(true);
      data = { ...data, page: await pageQuery($page.url, fetch) };
      loadedLocale = newLocale;
      loading.set(false);
    }
  }

  $: reloadOnLocale($locale);
</script>

<svelte:head>
  <title>{data.page.title}</title>
</svelte:head>

{#if wagtailPage}
  <svelte:component this={wagtailPage} page={data.page} />
{:else}
  Dieser Seitentyp existiert nicht: {data.page?.meta?.type}
{/if}
