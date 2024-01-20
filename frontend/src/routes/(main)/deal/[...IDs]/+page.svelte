<script lang="ts">
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { loading } from "$lib/stores"
  import { UserRole } from "$lib/types/user"

  import HeaderDates from "$components/HeaderDates.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import SectionDataSources from "$components/SectionDataSources.svelte"
  import SectionHistory from "$components/SectionHistory.svelte"

  import DealManageHeader from "./DealManageHeader.svelte"
  import SectionContracts from "./SectionContracts.svelte"
  import SectionEmployment from "./SectionEmployment.svelte"
  import SectionFormerUse from "./SectionFormerUse.svelte"
  import SectionGender from "./SectionGender.svelte"
  import SectionGeneralInfo from "./SectionGeneralInfo.svelte"
  import SectionInvestorInfo from "./SectionInvestorInfo.svelte"
  import SectionLocalCommunities from "./SectionLocalCommunities.svelte"
  import SectionLocations from "./SectionLocations.svelte"
  import SectionOverallComment from "./SectionOverallComment.svelte"
  import SectionProduceInfo from "./SectionProduceInfo.svelte"
  import SectionWater from "./SectionWater.svelte"

  export let data

  $: activeTab = $page.url.hash.split("/")[0] || "#locations"

  $: tabs = [
    { target: "#locations", name: $_("Locations") },
    { target: "#general", name: $_("General info") },
    { target: "#contracts", name: $_("Contracts") },
    { target: "#employment", name: $_("Employment") },
    { target: "#investor_info", name: $_("Investor info") },
    { target: "#data_sources", name: $_("Data sources") },
    {
      target: "#local_communities",
      name: $_("Local communities / indigenous peoples"),
    },
    { target: "#former_use", name: $_("Former use") },
    { target: "#produce_info", name: $_("Produce info") },
    { target: "#water", name: $_("Water") },
    { target: "#gender_related_info", name: $_("Gender-related info") },
    { target: "#overall_comment", name: $_("Overall comment") },
    { target: "#blank1", name: null },
    { target: "#history", name: $_("Deal history") },
    { target: "#actions", name: $_("Actions") },
  ]

  const reloadDeal = async () => {
    loading.set(true)
    await invalidate("deal:detail")
    loading.set(false)
  }

  const downloadLink = (format: string): string =>
    `/api/legacy_export/?deal_id=${data.dealID}&subset=UNFILTERED&format=${format}`
</script>

<svelte:head>
  <title>
    {$_("Deal")} #{data.deal.id}
  </title>
</svelte:head>

<div class="container mx-auto mt-8 min-h-full">
  {#if ![data.deal.active_version_id, data.deal.draft_version_id].includes(data.deal.selected_version.id)}
    <div
      class="rounded border border-orange-500 bg-orange-200 px-4 py-2 text-lg dark:bg-orange-800"
    >
      <span class="whitespace-nowrap">
        {$_("Please note: you are viewing an old version of this deal.")}
      </span>

      <span class="whitespace-nowrap">
        {$_("The current version can be found here:")}
        <a href="/deal/{data.deal.id}/" class="text-pelorous hover:text-pelorous-300">
          {$_("Deal")} #{data.deal.id}
        </a>
      </span>
    </div>
  {/if}
  {#if $page.data.user?.role > UserRole.ANYBODY}
    <DealManageHeader deal={data.deal} on:reload={reloadDeal} />
  {:else}
    <div class="my-4 md:flex md:flex-row md:justify-between">
      <h1 class="heading3 mt-3">
        {$_("Deal")}
        #{data.deal.id}
        {#if data.deal.selected_version.id !== data.deal.active_version_id}
          <span class="text-[0.9em]">
            {$_("Version")} #{data.deal.selected_version.id}
          </span>
        {/if}
      </h1>
      <HeaderDates obj={data.deal} />
    </div>
  {/if}
  <div class="flex min-h-full">
    <nav class="w-1/6 p-2">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="border-orange py-2 pr-4 {activeTab === target
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
    <div class="mb-12 w-5/6 pl-4">
      {#if activeTab === "#locations"}
        <SectionLocations version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#general"}
        <SectionGeneralInfo version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#contracts"}
        <SectionContracts version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#employment"}
        <SectionEmployment version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#investor_info"}
        <SectionInvestorInfo version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#data_sources"}
        <SectionDataSources version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#local_communities"}
        <SectionLocalCommunities version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#former_use"}
        <SectionFormerUse version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#produce_info"}
        <SectionProduceInfo version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#water"}
        <SectionWater version={data.deal.selected_version} />
      {/if}

      {#if activeTab === "#gender_related_info"}
        <SectionGender version={data.deal.selected_version} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <SectionOverallComment version={data.deal.selected_version} />
      {/if}

      {#if activeTab === "#history"}
        <SectionHistory obj={data.deal} />
      {/if}
      {#if activeTab === "#actions"}
        <section>
          <h3 class="heading3 mb-12">{$_("Download")}</h3>
          <div class="flex flex-col gap-8 text-lg font-semibold md:flex-row">
            <a
              target="_blank"
              href={downloadLink("xlsx")}
              rel="noreferrer"
              class="rounded border border-gray-300 bg-gray-50 px-4 py-2"
              data-sveltekit-reload
            >
              <DownloadIcon />
              {$_("Excel document")}
            </a>

            <a
              target="_blank"
              href={downloadLink("csv")}
              rel="noreferrer"
              class="rounded border border-gray-300 bg-gray-50 px-4 py-2"
              data-sveltekit-reload
            >
              <DownloadIcon />
              {$_("CSV file")}
            </a>
          </div>
        </section>
      {/if}
    </div>
  </div>
</div>
