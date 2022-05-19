<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { client } from "$lib/apolloClient";
  import type { Deal } from "$lib/types/deal";
  import { deal_gql_query } from "../queries";

  export const load: Load = async ({ params }) => {
    let [dealID, versionID] = params.IDs.split("/").map((x) => (x ? +x : undefined));

    const { data } = await get(client).query<{ deal: Deal[] }>({
      query: deal_gql_query,
      variables: { id: +dealID, version: versionID },
    });
    return {
      props: { dealID, versionID, deal: JSON.parse(JSON.stringify(data.deal)) },
    };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import DealEditSection from "$components/Deal/DealEditSection.svelte";
  import DealLocationsSection from "$components/Deal/DealLocationsSection.svelte";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte";
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte";
  import { deal_sections } from "../deal_sections";

  export let deal: Deal;
  export let dealID: number;
  export let versionID: number;

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

  let original_deal = "";
  let saving_in_progress = false;
  let show_really_quit_overlay = false;

  $: form_changed = JSON.stringify(deal) !== original_deal;
  function saveButtonPressed() {
    console.log("x");
  }
  function quitEditor() {
    console.log("y");
  }
</script>

<div class="container mx-auto min-h-full h-full flex flex-col">
  <div class="md:flex md:flex-row md:justify-between border-b border-orange">
    <h1>
      Editing deal {dealID}
      {#if deal.country}in {deal.country.name}{/if}
    </h1>
    <div class="flex items-center my-5">
      <button
        type="submit"
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!form_changed || saving_in_progress}
        on:click={saveButtonPressed}
      >
        {#if saving_in_progress}
          <LoadingSpinner /> {$_("Saving...")}
        {:else}
          {$_("Save")}
        {/if}
      </button>
      {#if dealID}
        <button class="btn btn-secondary mx-2" on:click={() => quitEditor(false)}>
          {$_("Close")}
        </button>
      {:else}
        <a class="btn btn-gray btn-sm mx-2" on:click={() => goto(-1)}>
          {$_("Cancel")}
        </a>
      {/if}
      <!--            <span>{{ $t("Leaves edit mode") }}</span>-->
    </div>
  </div>
  <div class="flex h-full overflow-y-hidden">
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
    <div class="pl-4 flex-auto w-full overflow-y-auto pr-2 pb-16">
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
    </div>
  </div>
</div>
