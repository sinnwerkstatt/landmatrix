<script context="module" lang="ts">
  import { request } from "graphql-request";
  import type { Load } from "@sveltejs/kit";
  import { deal_gql_query } from "./queries";
  import { GQLEndpoint } from "$lib";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
    };
    const result = await request(GQLEndpoint, deal_gql_query, variables);
    return { props: { deal: result.deal } };
  };
</script>

<script lang="ts">
  import { page } from "$app/stores";
  import type { Deal } from "$lib/types/deal";
  import { _ } from "svelte-i18n";
  import DealSection from "$components/Deal/DealSection.svelte";
  import { deal_sections } from "./deal_sections";

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
  <h1>Deal {dealID}</h1>
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
      {#if activeTab === "#employment"}
        <DealSection {deal} sections={deal_sections.employment} />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealSection {deal} sections={deal_sections.investor_info} />
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
          <h4><i class="fa fa-download" /> Download</h4>
          <a target="_blank" href={download_link("xlsx")}>XLSX</a><br />
          <a target="_blank" href={download_link("csv")}>CSV</a>
        </section>
      {/if}
    </div>
  </div>
</div>

<pre>{JSON.stringify(deal, null, 2)}</pre>
