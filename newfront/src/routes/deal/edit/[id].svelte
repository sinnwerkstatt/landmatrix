<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { client } from "$lib/apolloClient";
  import type { Deal } from "$lib/types/deal";
  import { deal_gql_query } from "../queries";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
    };
    const { data } = await client.query<{ deal: Deal[] }>({
      query: deal_gql_query,
      variables,
    });
    return { props: { deal: { ...data.deal } } };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import DealEditSection from "$components/Deal/DealEditSection.svelte";
  import DealLocationsSection from "$components/Deal/DealLocationsSection.svelte";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte";
  import DownloadIcon from "$components/icons/DownloadIcon.svelte";
  import { deal_sections } from "../deal_sections";

  export let deal: Deal;
  $: dealID = $page.params.id;

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
    { target: "#history", name: $_("Deal History") },
    { target: "#actions", name: $_("Actions") },
  ];

  const download_link = function (format: string): string {
    return `/api/legacy_export/?deal_id=${dealID}&subset=UNFILTERED&format=${format}`;
  };
</script>

<div class="container mx-auto min-h-full">
  <div class="md:flex md:flex-row md:justify-between">
    <h1>
      Editing deal {dealID}
      {#if deal.country}in {deal.country.name}{/if}
    </h1>
  </div>
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
        <DealEditSection {deal} sections={deal_sections.general_info} />
      {/if}
      {#if activeTab === "#contracts"}
        <DealSubmodelSection
          model="contract"
          modelName="Contract"
          entries={deal.contracts}
        />
      {/if}
      {#if activeTab === "#employment"}
        <DealEditSection {deal} sections={deal_sections.employment} />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealEditSection {deal} sections={deal_sections.investor_info} />
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelSection
          model="datasource"
          modelName="Data source"
          entries={deal.datasources}
        />
      {/if}
      {#if activeTab === "#local_communities"}
        <DealEditSection {deal} sections={deal_sections.local_communities} />
      {/if}
      {#if activeTab === "#former_use"}
        <DealEditSection {deal} sections={deal_sections.former_use} />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealEditSection {deal} sections={deal_sections.produce_info} />
      {/if}
      {#if activeTab === "#water"}
        <DealEditSection {deal} sections={deal_sections.water} />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealEditSection {deal} sections={deal_sections.gender_related_info} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealEditSection {deal} sections={deal_sections.overall_comment} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <section>
          <!--          <DealHistory {deal} {dealId} {dealVersion} />-->
        </section>
      {/if}
      {#if activeTab === "#actions"}
        <section>
          <h3>Download</h3>

          <a target="_blank" href={download_link("xlsx")}>
            <DownloadIcon /> Excel-Dokument
          </a><br />
          <a target="_blank" href={download_link("csv")}><DownloadIcon /> CSV-Datei</a>
        </section>
      {/if}
    </div>
  </div>
</div>
