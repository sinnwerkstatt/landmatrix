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
  import { dealSections } from "$lib/deal_sections";
  import DealEditSection from "$components/Deal/DealEditSection.svelte";
  import DealLocationsSection from "$components/Deal/DealLocationsSection.svelte";
  import DealSubmodelEditSection from "$components/Deal/DealSubmodelEditSection.svelte";
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte";

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
    { target: "#history", name: $_("Deal history") },
    { target: "#actions", name: $_("Actions") },
  ];

  let originalDeal = JSON.stringify(deal);

  let savingInProgress = false;
  let show_really_quit_overlay = false;

  $: formChanged = JSON.stringify(deal) !== originalDeal;
  function saveButtonPressed() {
    savingInProgress = true;
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
      <!--{originalDeal}<br /><br />-->
      <!--{JSON.stringify(deal)}<br /><br />-->
      x{formChanged}x
      <button
        type="submit"
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!formChanged || savingInProgress}
        on:click={saveButtonPressed}
      >
        {#if savingInProgress}
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
        <button class="btn btn-gray btn-sm mx-2" on:click={() => goto(-1)}>
          {$_("Cancel")}
        </button>
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
        <DealLocationsSection bind:deal />
      {/if}
      {#if activeTab === "#general"}
        <DealEditSection bind:deal sections={dealSections.general_info} />
      {/if}
      {#if activeTab === "#contracts"}
        <DealSubmodelEditSection
          model="contract"
          modelName="Contract"
          bind:entries={deal.contracts}
        />
      {/if}
      {#if activeTab === "#employment"}
        <DealEditSection bind:deal sections={dealSections.employment} />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealEditSection bind:deal sections={dealSections.investor_info} />
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelEditSection
          model="datasource"
          modelName="Data source"
          bind:entries={deal.datasources}
        />
      {/if}
      {#if activeTab === "#local_communities"}
        <DealEditSection bind:deal sections={dealSections.local_communities} />
      {/if}
      {#if activeTab === "#former_use"}
        <DealEditSection bind:deal sections={dealSections.former_use} />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealEditSection bind:deal sections={dealSections.produce_info} />
      {/if}
      {#if activeTab === "#water"}
        <DealEditSection bind:deal sections={dealSections.water} />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealEditSection bind:deal sections={dealSections.gender_related_info} />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealEditSection bind:deal sections={dealSections.overall_comment} />
      {/if}
    </div>
  </div>
</div>
