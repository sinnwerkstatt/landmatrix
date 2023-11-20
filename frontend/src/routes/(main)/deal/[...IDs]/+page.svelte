<script lang="ts">
  import { gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { loading } from "$lib/stores"
  import { UserRole } from "$lib/types/user"

  import HeaderDates from "$components/HeaderDates.svelte"

  import DealManageHeader from "./DealManageHeader.svelte"
  import SectionDataSources from "./SectionDataSources.svelte"
  import SectionGeneralInfo from "./SectionGeneralInfo.svelte"
  import SectionHistory from "./SectionHistory.svelte"
  import SectionLocations from "./SectionLocations.svelte"

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
    await invalidate(`/api/deal/${data.dealID}/`)
    loading.set(false)
  }

  // const downloadLink = (format: string): string =>
  //   `/api/legacy_export/?deal_id=${data.dealID}&subset=UNFILTERED&format=${format}`

  // let investor: Investor
  // async function fetchInvestor() {
  //   if (!deal.operating_company?.id) return
  //
  //   const ret = await $page.data.urqlClient
  //     .query<{ investor: Investor }>(
  //       gql`
  //         query ($id: Int!) {
  //           investor(id: $id) {
  //             id
  //             name
  //             classification
  //             country {
  //               id
  //               name
  //             }
  //             homepage
  //             comment
  //             deals {
  //               id
  //               country {
  //                 id
  //                 name
  //               }
  //               intention_of_investment
  //               implementation_status
  //               negotiation_status
  //               intended_size
  //               contract_size
  //             }
  //           }
  //         }
  //       `,
  //       { id: deal?.operating_company?.id },
  //     )
  //     .toPromise()
  //
  //   if (ret.error || !ret.data) {
  //     console.error(ret.error)
  //   } else {
  //     investor = ret.data.investor
  //   }
  // }
  // onMount(fetchInvestor)
</script>

<svelte:head>
  <title>
    {$_("Deal")} #{data.deal.id}
  </title>
</svelte:head>

<div class="container mx-auto min-h-full">
  {#if $page.data.user?.role > UserRole.ANYBODY}
    <DealManageHeader
      deal={data.deal}
      dealVersion={data.dealVersion}
      on:reload={reloadDeal}
    />
  {:else}
    <div class="md:flex md:flex-row md:justify-between">
      <h1 class="heading3 mt-3">
        {$_("Deal")}
        #{data.deal.id}
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
                class={activeTab === target ? "text-lm-dark dark:text-white" : ""}
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
      <!--      {#if activeTab === "#contracts"}-->
      <!--        <DealSubmodelSection-->
      <!--          model="contract"-->
      <!--          modelName="Contract"-->
      <!--          entries={deal.contracts}-->
      <!--        />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#employment"}-->
      <!--        <DealSection {deal} sections={$dealSections.employment} />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#investor_info"}-->
      <!--        <DealSection {deal} sections={$dealSections.investor_info}>-->
      <!--          {#if investor}-->
      <!--            <h4 class="mb-2">-->
      <!--              Network of parent companies and tertiary investors/lenders-->
      <!--            </h4>-->
      <!--            <InvestorGraph {investor} initDepth={5} />-->
      <!--          {/if}-->
      <!--        </DealSection>-->
      <!--      {/if}-->
      {#if activeTab === "#data_sources"}
        <SectionDataSources version={data.deal.selected_version} />
      {/if}
      <!--      {#if activeTab === "#local_communities"}-->
      <!--        <DealSection {deal} sections={$dealSections.local_communities} />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#former_use"}-->
      <!--        <DealSection {deal} sections={$dealSections.former_use} />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#produce_info"}-->
      <!--        <DealSection {deal} sections={$dealSections.produce_info} />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#water"}-->
      <!--        <DealSection {deal} sections={$dealSections.water} />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#gender_related_info"}-->
      <!--        <DealSection {deal} sections={$dealSections.gender_related_info} />-->
      <!--      {/if}-->
      <!--      {#if activeTab === "#overall_comment"}-->
      <!--        <DealSection {deal} sections={$dealSections.overall_comment} />-->
      <!--      {/if}-->
      {#if activeTab === "#history"}
        <SectionHistory
          deal={data.deal}
          dealID={data.dealID}
          dealVersion={data.dealVersion}
        />
      {/if}
      <!--      {#if activeTab === "#actions"}-->
      <!--        <section>-->
      <!--          <h3>{$_("Download")}</h3>-->

      <!--          <a-->
      <!--            target="_blank"-->
      <!--            href={downloadLink("xlsx")}-->
      <!--            rel="noreferrer"-->
      <!--            data-sveltekit-reload-->
      <!--          >-->
      <!--            <DownloadIcon />-->
      <!--            {$_("Excel document")}-->
      <!--          </a>-->
      <!--          <br />-->
      <!--          <a-->
      <!--            target="_blank"-->
      <!--            href={downloadLink("csv")}-->
      <!--            rel="noreferrer"-->
      <!--            data-sveltekit-reload-->
      <!--          >-->
      <!--            <DownloadIcon />-->
      <!--            {$_("CSV file")}-->
      <!--          </a>-->
      <!--        </section>-->
      <!--      {/if}-->
    </div>
  </div>
</div>
