<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { deal_gql_query } from "$lib/deal_queries"
  import { dealSections } from "$lib/sections.js"
  import { loading } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import { UserRole } from "$lib/types/user"

  import DealHistory from "$components/Deal/DealHistory.svelte"
  import DealLocationsSection from "$components/Deal/DealLocationsSection.svelte"
  import DealSection from "$components/Deal/DealSection.svelte"
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte"
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import InvestorGraph from "$components/Investor/InvestorGraph.svelte"
  import DealManageHeader from "$components/Management/DealManageHeader.svelte"

  // import type { PageData } from "./$types";
  //
  // export let data: PageData;
  export let data: { deal: Deal; dealID: number; dealVersion: number }

  let deal: Deal = data.deal
  $: deal = data.deal

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

  async function reloadDeal() {
    console.log("Deal detail: reload")
    loading.set(true)

    const ret = await ($page.data.urqlClient as Client)
      .query<{ deal: Deal }>(
        deal_gql_query,
        { id: data.dealID, version: data.dealVersion },
        { requestPolicy: "network-only" },
      )
      .toPromise()

    if (ret.error || !ret.data) {
      console.error(ret.error)
    } else {
      deal = ret.data.deal
    }

    loading.set(false)
  }

  const downloadLink = (format: string): string =>
    `/api/legacy_export/?deal_id=${data.dealID}&subset=UNFILTERED&format=${format}`

  let investor: Investor
  async function fetchInvestor() {
    if (!deal.operating_company?.id) return

    const ret = await ($page.data.urqlClient as Client)
      .query<{ investor: Investor }>(
        gql`
          query ($id: Int!) {
            investor(
              id: $id
              involvements_depth: 5
              involvements_include_ventures: false
            ) {
              id
              name
              classification
              country {
                id
                name
              }
              homepage
              comment
              involvements
            }
          }
        `,
        { id: deal?.operating_company?.id },
      )
      .toPromise()

    if (ret.error || !ret.data) {
      console.error(ret.error)
    } else {
      investor = ret.data.investor
    }
  }
  onMount(fetchInvestor)
</script>

<svelte:head>
  <title>
    {$_("Deal")} #{deal.id}
  </title>
</svelte:head>

<div class="container mx-auto min-h-full">
  {#if $page.data.user?.role > UserRole.ANYBODY}
    <DealManageHeader {deal} dealVersion={data.dealVersion} on:reload={reloadDeal} />
  {:else}
    <div class="md:flex md:flex-row md:justify-between">
      <h1>
        {$_("Deal")}
        #{deal.id}
      </h1>
      <div class="my-2 flex w-auto items-center rounded bg-gray-50 p-3">
        <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
          {$_("Created")}
          <br />
          <DateTimeField value={deal.created_at} />
        </div>
        <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
          {$_("Last update")}
          <br />
          <DateTimeField value={deal.modified_at} />
        </div>
        <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
          {$_("Last full update")}
          <br />
          <DateTimeField value={deal.fully_updated_at} />
        </div>
      </div>
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
              <a href={target} class:text-black={activeTab === target}>{name}</a>
            {:else}
              <hr />
            {/if}
          </li>
        {/each}
      </ul>
    </nav>
    <div class="mb-12 w-5/6 pl-4">
      {#if activeTab === "#locations"}
        <DealLocationsSection {deal} />
      {/if}
      {#if activeTab === "#general"}
        <DealSection {deal} sections={$dealSections.general_info} />
      {/if}
      {#if activeTab === "#contracts"}
        <DealSubmodelSection
          model="contract"
          modelName="Contract"
          entries={deal.contracts}
        />
      {/if}
      {#if activeTab === "#employment"}
        <DealSection {deal} sections={$dealSections.employment} />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealSection {deal} sections={$dealSections.investor_info}>
          {#if investor}
            <h4 class="mb-2">
              Network of parent companies and tertiary investors/lenders
            </h4>
            <InvestorGraph {investor} />
          {/if}
        </DealSection>
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelSection
          model="datasource"
          modelName="Data source"
          entries={deal.datasources}
        />
      {/if}
      {#if activeTab === "#local_communities"}
        <DealSection {deal} sections={$dealSections.local_communities} />
      {/if}
      {#if activeTab === "#former_use"}
        <DealSection {deal} sections={$dealSections.former_use} />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealSection {deal} sections={$dealSections.produce_info} />
      {/if}
      {#if activeTab === "#water"}
        <DealSection {deal} sections={$dealSections.water} />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealSection {deal} sections={$dealSections.gender_related_info} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealSection {deal} sections={$dealSections.overall_comment} />
      {/if}
      {#if activeTab === "#history"}
        <DealHistory {deal} dealID={data.dealID} dealVersion={data.dealVersion} />
      {/if}
      {#if activeTab === "#actions"}
        <section>
          <h3>{$_("Download")}</h3>

          <a
            target="_blank"
            href={downloadLink("xlsx")}
            rel="noreferrer"
            data-sveltekit-reload
          >
            <DownloadIcon />
            {$_("Excel document")}
          </a>
          <br />
          <a
            target="_blank"
            href={downloadLink("csv")}
            rel="noreferrer"
            data-sveltekit-reload
          >
            <DownloadIcon />
            {$_("CSV file")}
          </a>
        </section>
      {/if}
    </div>
  </div>
</div>
