<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { request } from "graphql-request";
  import { GQLEndpoint } from "$lib";
  import { deal_gql_query } from "./queries";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
    };
    const result = await request(GQLEndpoint, deal_gql_query, variables);
    return { props: { deal: result.deal } };
  };
</script>

<script lang="ts">
  import dayjs from "dayjs";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import type { Deal } from "$lib/types/deal";
  import DealSection from "$components/Deal/DealSection.svelte";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte";
  import DownloadIcon from "../../components/icons/DownloadIcon.svelte";
  import { deal_sections, deal_submodel_sections } from "./deal_sections";

  export let deal: Deal;
  const dealID = $page.params.id;

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

<div class="container mx-auto">
  <div class="md:flex md:flex-row md:justify-between">
    <h1>
      Deal {dealID}
      {#if deal.country}in {deal.country.name}{/if}
    </h1>
    <div class="flex items-center bg-gray-50 rounded p-3 my-2 w-auto">
      <div class="dates-header">
        Created<br />
        {dayjs(deal.created_at).format("DD/MM/YYYY")}
      </div>
      <div class="dates-header">
        Last update<br />
        {dayjs(deal.modified_at).format("DD/MM/YYYY")}
      </div>
      <div class="dates-header">
        Last full update<br />
        {dayjs(deal.fully_updated_at).format("DD/MM/YYYY")}
      </div>
    </div>
  </div>
  <div class="flex">
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
      {#if activeTab === "#general"}
        <DealSection {deal} sections={deal_sections.general_info} />
      {/if}
      {#if activeTab === "#contracts"}
        <DealSubmodelSection
          {deal}
          entries={deal.contracts}
          fields={deal_submodel_sections.contract}
          model="contract"
          modelName="Contract"
        />
      {/if}
      {#if activeTab === "#employment"}
        <DealSection {deal} sections={deal_sections.employment} />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealSection {deal} sections={deal_sections.investor_info} />
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelSection
          {deal}
          entries={deal.datasources}
          fields={deal_submodel_sections.datasource}
          model="datasource"
          modelName="Data source"
        />
      {/if}
      {#if activeTab === "#local_communities"}
        <DealSection {deal} sections={deal_sections.local_communities} />
      {/if}
      {#if activeTab === "#former_use"}
        <DealSection {deal} sections={deal_sections.former_use} />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealSection {deal} sections={deal_sections.produce_info} />
      {/if}
      {#if activeTab === "#water"}
        <DealSection {deal} sections={deal_sections.water} />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealSection {deal} sections={deal_sections.gender_related_info} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealSection {deal} sections={deal_sections.overall_comment} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <section>
          <!--          <DealHistory {deal} {dealId} {dealVersion} />-->
        </section>
      {/if}
      {#if activeTab === "#actions"}
        <section>
          <h3>Download</h3>

          <a target="_blank" href={download_link("xlsx")}
            ><DownloadIcon /> Excel-Dokument</a
          ><br />
          <a target="_blank" href={download_link("csv")}><DownloadIcon /> CSV-Datei</a>
        </section>
      {/if}
    </div>
  </div>
</div>

<style>
  .dates-header {
    @apply mr-10 md:mx-5 text-xs md:text-sm text-lm-dark;
  }
</style>
