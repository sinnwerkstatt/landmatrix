<script lang="ts">
  import { _, locale } from "svelte-i18n"

  import { page } from "$app/stores"

  import { pageQuery } from "$lib/queries"
  import { loading } from "$lib/stores"

  import BasePage from "./BasePage.svelte"
  import HomePage from "./HomePage.svelte"
  import ObservatoryPage from "./ObservatoryPage.svelte"

  export let data

  $: wagtailPage = {
    WagtailRootPage: HomePage,
    WagtailPage: BasePage,
    ObservatoryPage: ObservatoryPage,
  }[data.page.meta?.type.split(".")[1]]

  let loadedLocale = $locale

  async function reloadOnLocale(newLocale) {
    if (newLocale != loadedLocale) {
      loading.set(true)
      data = { ...data, page: await pageQuery($page.url, fetch) }
      loadedLocale = newLocale
      loading.set(false)
    }
  }

  $: reloadOnLocale($locale)
</script>

<svelte:head>
  <title>{data.page.title} | {$_("Land Matrix")}</title>
</svelte:head>

{#if wagtailPage}
  <svelte:component this={wagtailPage} page={data.page} />
{:else}
  Dieser Seitentyp existiert nicht: {data.page?.meta?.type}
{/if}
