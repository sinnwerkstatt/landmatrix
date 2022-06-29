<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import type { Deal } from "$lib/types/deal";
  import { deal_gql_query } from "./queries";

  export const load: Load = async ({ params, stuff }) => {
    let [dealID, dealVersion] = params.IDs.split("/").map((x) => (x ? +x : undefined));

    if (!dealID) return { status: 404, error: `Deal not found` };

    const { data } = await stuff.secureApolloClient.query<{ deal: Deal }>({
      query: deal_gql_query,
      variables: { id: dealID, version: dealVersion, subset: "UNFILTERED" },
    });
    return { props: { dealID, dealVersion, deal: data.deal } };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { dealSections } from "$lib/deal_sections";
  import DealLocationsSection from "$components/Deal/DealLocationsSection.svelte";
  import DealSection from "$components/Deal/DealSection.svelte";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte";
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte";
  import DownloadIcon from "$components/icons/DownloadIcon.svelte";
  import DealManageHeader from "$components/Management/DealManageHeader.svelte";

  export let deal: Deal;
  export let dealID: number;
  export let dealVersion: number;

  $: activeTab = $page.url.hash || "#locations";

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
  ];

  const download_link = function (format: string): string {
    return `/api/legacy_export/?deal_id=${dealID}&subset=UNFILTERED&format=${format}`;
  };
</script>

<svelte:head>
  <title
    >{$_("Deal")}
    {deal.id}
  </title>
</svelte:head>

<div class="container mx-auto min-h-full">
  {#if $page.stuff.user?.is_authenticated}
    <DealManageHeader {deal} {dealVersion} />
  {:else}
    <div class="md:flex md:flex-row md:ju<stify-between">
      <h1>
        {$_("Deal")}
        {deal.id}
        {#if deal.country}{$_("in")} {deal.country.name}{/if}
      </h1>
      <div class="flex items-center bg-gray-50 rounded p-3 my-2 w-auto">
        <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
          {$_("Created")}<br />
          <DateTimeField value={deal.created_at} />
        </div>
        <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
          {$_("Last update")}<br />
          <DateTimeField value={deal.modified_at} />
        </div>
        <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
          {$_("Last full update")}<br />
          <DateTimeField value={deal.fully_updated_at} />
        </div>
      </div>
    </div>
  {/if}
  <div class="flex min-h-full">
    <nav class="p-2 flex-initial">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="py-2 pr-4 border-orange {activeTab === target
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
    <div class="pl-4 flex-auto w-full">
      {#if activeTab === "#locations"}
        <DealLocationsSection {deal} />
      {/if}
      {#if activeTab === "#general"}
        <DealSection {deal} sections={dealSections.general_info} />
      {/if}
      {#if activeTab === "#contracts"}
        <DealSubmodelSection
          model="contract"
          modelName="Contract"
          entries={deal.contracts}
        />
      {/if}
      {#if activeTab === "#employment"}
        <DealSection {deal} sections={dealSections.employment} />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealSection {deal} sections={dealSections.investor_info} />
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelSection
          model="datasource"
          modelName="Data source"
          entries={deal.datasources}
        />
      {/if}
      {#if activeTab === "#local_communities"}
        <DealSection {deal} sections={dealSections.local_communities} />
      {/if}
      {#if activeTab === "#former_use"}
        <DealSection {deal} sections={dealSections.former_use} />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealSection {deal} sections={dealSections.produce_info} />
      {/if}
      {#if activeTab === "#water"}
        <DealSection {deal} sections={dealSections.water} />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealSection {deal} sections={dealSections.gender_related_info} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealSection {deal} sections={dealSections.overall_comment} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <section>
          <!--          <DealHistory {deal} {dealId} {dealVersion} />-->
        </section>
      {/if}
      {#if activeTab === "#actions"}
        <section>
          <h3>{$_("Download")}</h3>

          <a target="_blank" href={download_link("xlsx")}>
            <DownloadIcon />
            {$_("Excel document")}
          </a><br />
          <a target="_blank" href={download_link("csv")}>
            <DownloadIcon />
            {$_("CSV file")}
          </a>
        </section>
      {/if}
    </div>
  </div>
</div>
