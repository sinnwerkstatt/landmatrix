<script lang="ts">
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/state"

  import { loading } from "$lib/stores/basics"
  import { isReporterOrAbove } from "$lib/utils/permissions"

  import InvestorManageHeader from "$components/Data/Investor/InvestorManageHeader.svelte"
  import { INVESTOR_SECTIONS } from "$components/Data/Investor/Sections/constants"
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"
  import SectionNav from "$components/Data/SectionNav.svelte"
  import HeaderDatesWDownload from "$components/HeaderDatesWDownload.svelte"
  import ManageHeaderOldVersionNote from "$components/New/ManageHeaderOldVersionNote.svelte"

  let { data, children } = $props()

  const reloadInvestor = async () => {
    loading.set(true)
    await invalidate("investor:detail")
    loading.set(false)
  }
</script>

<svelte:head>
  <title>{$_("Investor")} #{data.investor.id}</title>
</svelte:head>

<div class="display-grid container mx-auto pt-2">
  <div style="grid-area: header">
    <ManageHeaderOldVersionNote obj={data.investor} />

    {#if isReporterOrAbove(page.data.user)}
      <InvestorManageHeader investor={data.investor} on:reload={reloadInvestor} />
    {:else}
      <div class="my-4 md:flex md:flex-row md:justify-between">
        <h1 class="heading3 mb-0 mt-3">
          {#if data.investor.selected_version.name_unknown}
            <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
          {:else}
            {data.investor.selected_version.name}
          {/if}
          <small>#{data.investor.id}</small>
        </h1>
        <HeaderDatesWDownload obj={data.investor} />
      </div>
    {/if}
  </div>

  <div class="sticky top-0 z-[10]" style="grid-area: sidenav">
    <SectionNav
      sections={INVESTOR_SECTIONS.map(s => ({
        slug: s,
        label: $investorSectionLookup[s].label,
      }))}
      baseUrl={data.baseUrl}
    />
  </div>

  <div class="mt-2 px-4 lg:min-h-[92dvh]" style="grid-area: main">
    {@render children?.()}
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
      grid-template-rows: auto auto 100dvh;
      grid-template-columns: 100%;
      grid-template-areas:
        "header"
        "sidenav"
        "main";
    }
  }
</style>
