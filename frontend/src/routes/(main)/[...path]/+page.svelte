<script lang="ts">
  import { _, locale } from "svelte-i18n"

  import { page } from "$app/state"

  import { pageQuery } from "$lib/queries"
  import { loading } from "$lib/stores/basics"
  import { isStaff } from "$lib/utils/permissions"

  import WagtailBird from "$components/Wagtail/WagtailBird.svelte"

  import BasePage from "./BasePage.svelte"
  import HomePage from "./HomePage.svelte"
  import ObservatoryPage from "./ObservatoryPage.svelte"

  let { data = $bindable() } = $props()

  let wagtailPage = $derived(
    {
      WagtailRootPage: HomePage,
      WagtailPage: BasePage,
      ObservatoryPage: ObservatoryPage,
    }[data.page.meta?.type.split(".")[1]],
  )

  let loadedLocale = $locale

  const reloadOnLocale = async (newLocale?: string | null) => {
    if (newLocale !== loadedLocale) {
      loading.set(true)
      data = { ...data, page: await pageQuery(page.url, fetch) }
      loadedLocale = newLocale
      loading.set(false)
    }
  }

  $effect(() => {
    reloadOnLocale($locale)
  })
</script>

<svelte:head>
  <title>{data.page.title} | {$_("Land Matrix")}</title>
</svelte:head>

{#if wagtailPage}
  {@const SvelteComponent = wagtailPage}
  <SvelteComponent page={data.page} />
{:else}
  Dieser Seitentyp existiert nicht: {data.page?.meta?.type}
{/if}

{#if isStaff(data.user)}
  <WagtailBird page={data.page} />
{/if}
