<script lang="ts">
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { loading } from "$lib/stores/basics"
  import { UserRole } from "$lib/types/newtypes"

  import DealManageHeader from "$components/Data/Deal/DealManageHeader.svelte"
  import { DEAL_SECTIONS } from "$components/Data/Deal/Sections/constants"
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"
  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import HeaderDatesWDownload from "$components/HeaderDatesWDownload.svelte"
  import ManageHeaderOldVersionNote from "$components/New/ManageHeaderOldVersionNote.svelte"
  import SectionNav from "$components/SectionNav.svelte"

  export let data

  const reloadDeal = async () => {
    loading.set(true)
    await invalidate("deal:detail")
    loading.set(false)
  }
</script>

<svelte:head>
  <title>{$_("Deal")} #{data.deal.id}</title>
</svelte:head>

<div class="display-grid container mx-auto pt-2">
  <div style="grid-area: header">
    <ManageHeaderOldVersionNote obj={data.deal} />
    {#if $page.data.user?.role > UserRole.ANYBODY}
      <DealManageHeader deal={data.deal} on:reload={reloadDeal} />
    {:else}
      <div class="my-4 md:flex md:flex-row md:justify-between">
        <div class="flex flex-col">
          <h1 class="heading3 mb-0 mt-3">
            {$_("Deal")}
            #{data.deal.id}
            {#if data.deal.selected_version.id !== data.deal.active_version_id}
              <span class="text-[0.9em]">
                {$_("Version")} #{data.deal.selected_version.id}
              </span>
            {/if}
          </h1>
          <div class="heading4 my-0">
            <CountryField value={data.deal.country_id} />
          </div>
        </div>
        <HeaderDatesWDownload obj={data.deal} />
      </div>
    {/if}
  </div>

  <div class="sticky top-0 z-[100]" style="grid-area: sidenav">
    <SectionNav
      sections={DEAL_SECTIONS.map(s => ({
        slug: s,
        label: $dealSectionLookup[s].label,
      }))}
      baseUrl={data.baseUrl}
    />
  </div>

  <div class="h-full px-4 pb-20" style="grid-area: main">
    <slot />
  </div>
</div>

<style>
  .display-grid {
    display: grid;
    align-items: start;
    grid-template-rows: auto 1fr;
    grid-template-columns: repeat(6, 1fr);
    grid-template-areas:
      "header header header header header header"
      "sidenav main main main main main";

    @media (width <= 1024px) {
      grid-template-rows: auto auto 100vh;
      grid-template-columns: 100%;
      grid-template-areas:
        "header"
        "sidenav"
        "main";
    }
  }
</style>
