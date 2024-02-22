<script lang="ts">
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { loading } from "$lib/stores"
  import { UserRole } from "$lib/types/user"

  import HeaderDates from "$components/HeaderDates.svelte"
  import InvolvementsGraph from "$components/New/InvolvementsGraph/InvolvementsGraph.svelte"
  import SectionDataSources from "$components/SectionDataSources.svelte"
  import SectionHistory from "$components/SectionHistory.svelte"

  import InvestorManageHeader from "./InvestorManageHeader.svelte"
  import SectionGeneralInfo from "./SectionGeneralInfo.svelte"
  import SectionInvolvements from "./SectionInvolvements.svelte"

  export let data

  $: activeTab = $page.url.hash.split("/")[0] || "#general"

  $: allTabs = [
    { target: "#general", name: $_("General info") },
    { target: "#involvements", name: $_("Involvements") },
    { target: "#network_graph", name: $_("Network graph") },
    { target: "#data_sources", name: $_("Data sources") },
    { target: "#history", name: $_("Version history") },
  ]

  $: tabs =
    data.investor.selected_version.datasources.length > 0
      ? allTabs
      : allTabs.filter(tab => tab.target !== "#data_sources")

  const reloadInvestor = async () => {
    loading.set(true)
    await invalidate("investor:detail")
    loading.set(false)
  }
</script>

<svelte:head>
  <title>{data.investor.selected_version.name} #{data.investor.id}</title>
</svelte:head>

<div class="container mx-auto mb-12 mt-8 min-h-full">
  {#if $page.data.user?.role > UserRole.ANYBODY}
    <InvestorManageHeader investor={data.investor} on:reload={reloadInvestor} />
  {:else}
    <div class="md:flex md:flex-row md:justify-between">
      <h1 class="heading3 mt-3">
        {#if data.investor.selected_version.name_unknown}
          <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
        {:else}
          {data.investor.selected_version.name}
        {/if}
        <small>#{data.investor.id}</small>
      </h1>
      <HeaderDates obj={data.investor} />
    </div>
  {/if}

  <div class="flex min-h-full">
    <nav class="w-1/6 p-2">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="whitespace-nowrap border-orange py-2 pr-20 {activeTab === target
              ? 'border-r-4'
              : 'border-r'}"
          >
            {#if name}
              <a
                href={target}
                class={activeTab === target ? "text-gray-700 dark:text-white" : ""}
              >
                {name}
              </a>
            {:else}
              <hr />
            {/if}
          </li>
        {/each}
      </ul>
    </nav>
    <div class="w-5/6 px-4">
      {#if activeTab === "#general"}
        <SectionGeneralInfo version={data.investor.selected_version} />
      {/if}
      {#if activeTab === "#involvements"}
        <SectionInvolvements investor={data.investor} />
      {/if}
      {#if activeTab === "#data_sources"}
        <SectionDataSources version={data.investor.selected_version} />
      {/if}
      {#if activeTab === "#history"}
        <SectionHistory obj={data.investor} />
      {/if}

      {#if activeTab === "#network_graph"}
        {#if data.investor.selected_version.status === "ACTIVATED"}
          <InvolvementsGraph investor_id={data.investor.id} />
        {:else}
          <div class="m-10 bg-neutral-200 px-12 py-24 text-center text-zinc-700">
            {@html $_(
              "The investor network diagram is not visible in draft mode. Go to {liveLink} to see it.",
              {
                values: {
                  liveLink: `<a href="/investor/${data.investorID}/#network_graph">/investor/${data.investorID}/</a>`,
                },
              },
            )}
          </div>
        {/if}
      {/if}
    </div>
  </div>
</div>
