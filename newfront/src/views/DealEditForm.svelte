<script lang="ts">
  import { gql } from "graphql-tag";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { client } from "$lib/apolloClient";
  import { dealSections } from "$lib/sections";
  import type { Deal } from "$lib/types/deal";
  import type { Contract, DataSource, Location } from "$lib/types/deal";
  import { removeEmptyEntries } from "$lib/utils/data_processing";
  import DealEditSection from "$components/Deal/DealEditSection.svelte";
  import DealLocationsEditSection from "$components/Deal/DealLocationsEditSection.svelte";
  import DealSubmodelEditSection from "$components/Deal/DealSubmodelEditSection.svelte";
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";

  export let deal: Deal;
  export let dealID: number;
  export let dealVersion: number;

  let originalDeal = JSON.stringify(deal);
  let savingInProgress = false;
  let showReallyQuitOverlay = false;
  $: activeTab = $page.url.hash || "#locations";
  $: formChanged = JSON.stringify(deal) !== originalDeal;
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
  ];

  async function saveDeal(hash: string) {
    const currentForm = document.querySelector<HTMLFormElement>(activeTab);
    console.log(currentForm);
    if (!currentForm.checkValidity()) {
      currentForm.reportValidity();
      return;
    }
    savingInProgress = true;
    deal.locations = removeEmptyEntries<Location>(deal.locations);
    deal.contracts = removeEmptyEntries<Contract>(deal.contracts);
    deal.datasources = removeEmptyEntries<DataSource>(deal.datasources);

    const { data } = await $client.mutate({
      mutation: gql`
        mutation ($id: Int!, $version: Int, $payload: Payload) {
          deal_edit(id: $id, version: $version, payload: $payload) {
            dealId
            dealVersion
          }
        }
      `,
      variables: {
        id: dealID ? +dealID : -1,
        version: dealVersion ? +dealVersion : null,
        payload: { ...deal, versions: null, comments: null, workflowinfos: null },
      },
    });
    const { deal_edit } = data;
    originalDeal = JSON.stringify(deal);
    savingInProgress = false;

    if (location.hash !== hash || +dealVersion !== +deal_edit.dealVersion) {
      await goto(
        `/deal/edit/${deal_edit.dealId}/${deal_edit.dealVersion}${hash ?? ""}`
      );
    }
  }

  const onClickClose = async (force: boolean) => {
    if (formChanged && !force) showReallyQuitOverlay = true;
    else if (!dealID) await goto("/");
    else await goto(`/deal/${dealID}${dealVersion ? "/" + dealVersion : ""}`);
  };
</script>

<div class="container mx-auto min-h-full h-full flex flex-col">
  <div class="md:flex md:flex-row md:justify-between border-b border-orange">
    <h1>
      {dealID ? $_("Editing Deal #") + dealID : $_("Adding new deal")}
      {#if deal.country}{$_("in")} {deal.country.name}{/if}
    </h1>
    <div class="flex items-center my-5">
      <button
        type="submit"
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!formChanged || savingInProgress}
        on:click={() => saveDeal(location.hash)}
      >
        {#if savingInProgress}
          <LoadingSpinner /> {$_("Saving...")}
        {:else}
          {$_("Save")}
        {/if}
      </button>
      {#if dealID}
        <button class="btn btn-secondary mx-2" on:click={() => onClickClose(false)}>
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
        <DealLocationsEditSection
          bind:locations={deal.locations}
          bind:country={deal.country}
        />
      {/if}
      {#if activeTab === "#general"}
        <DealEditSection bind:deal sections={dealSections.general_info} id="general" />
      {/if}
      {#if activeTab === "#contracts"}
        <DealSubmodelEditSection
          model="contract"
          modelName="Contract"
          bind:entries={deal.contracts}
          id="contracts"
        />
      {/if}
      {#if activeTab === "#employment"}
        <DealEditSection bind:deal sections={dealSections.employment} id="employment" />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealEditSection
          bind:deal
          sections={dealSections.investor_info}
          id="investor_info"
        />
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelEditSection
          model="datasource"
          modelName="Data source"
          bind:entries={deal.datasources}
          id="data_sources"
        />
      {/if}
      {#if activeTab === "#local_communities"}
        <DealEditSection
          bind:deal
          sections={dealSections.local_communities}
          id="local_communities"
        />
      {/if}
      {#if activeTab === "#former_use"}
        <DealEditSection bind:deal sections={dealSections.former_use} id="former_use" />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealEditSection
          bind:deal
          sections={dealSections.produce_info}
          id="produce_info"
        />
      {/if}
      {#if activeTab === "#water"}
        <DealEditSection bind:deal sections={dealSections.water} id="water" />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealEditSection
          bind:deal
          sections={dealSections.gender_related_info}
          id="gender_related_info"
        />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealEditSection
          bind:deal
          sections={dealSections.overall_comment}
          id="overall_comment"
        />
      {/if}
    </div>
  </div>
</div>

<ManageOverlay bind:visible={showReallyQuitOverlay} title={$_("Quit without saving?")}>
  <div class="font-medium">{$_("Do you really want to close deal editor?")}</div>
</ManageOverlay>
