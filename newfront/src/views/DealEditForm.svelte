<script lang="ts">
  import { error } from "@sveltejs/kit"
  import { Client, gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import { getDealSections } from "$lib/sections"
  import type { Contract, DataSource, Deal, Location as LamaLoc } from "$lib/types/deal"
  import { removeEmptyEntries } from "$lib/utils/data_processing"

  import DealEditSection from "$components/Deal/DealEditSection.svelte"
  import DealLocationsEditSection from "$components/Deal/DealLocationsEditSection.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ManageOverlay from "$components/Management/ManageOverlay.svelte"
  import SubmodelEditSection from "$components/Management/SubmodelEditSection.svelte"

  export let deal: Deal
  export let dealID: number
  export let dealVersion: number

  let originalDeal = JSON.stringify(deal)
  let savingInProgress = false
  let showReallyQuitOverlay = false
  $: activeTab = $page.url.hash || "#locations"
  $: formChanged = JSON.stringify(deal) !== originalDeal
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
  ]

  async function saveDeal(hash: string) {
    const currentForm: HTMLFormElement | null =
      document.querySelector<HTMLFormElement>(activeTab)
    if (!currentForm) throw error(500, "can not grab the form")

    if (!currentForm.checkValidity()) {
      currentForm.reportValidity()
      return
    }
    savingInProgress = true
    deal.locations = removeEmptyEntries<LamaLoc>(deal.locations)
    deal.contracts = removeEmptyEntries<Contract>(deal.contracts)
    deal.datasources = removeEmptyEntries<DataSource>(deal.datasources)

    const ret = await ($page.data.urqlClient as Client)
      .mutation<{ deal_edit: { dealId: number; dealVersion?: number } }>(
        gql`
          mutation ($id: Int!, $version: Int, $payload: Payload) {
            deal_edit(id: $id, version: $version, payload: $payload) {
              dealId
              dealVersion
            }
          }
        `,
        {
          id: dealID ? +dealID : -1,
          version: dealVersion ? +dealVersion : null,
          payload: { ...deal, versions: null, comments: null, workflowinfos: null },
        },
      )
      .toPromise()
    const deal_edit = ret.data?.deal_edit
    if (!deal_edit) throw error(500, `Problem with edit: ${ret.error}`)

    originalDeal = JSON.stringify(deal)
    savingInProgress = false

    if (location.hash !== hash || +dealVersion !== +deal_edit.dealVersion) {
      await goto(`/deal/edit/${deal_edit.dealId}/${deal_edit.dealVersion}${hash ?? ""}`)
    }
  }

  const onClickClose = async (force: boolean) => {
    if (formChanged && !force) showReallyQuitOverlay = true
    else if (!dealID) await goto("/")
    else await goto(`/deal/${dealID}/${dealVersion ?? ""}`)
  }
  $: dealSections = getDealSections($_)
</script>

<div class="container mx-auto flex h-full min-h-full flex-col">
  <div class="border-b border-orange md:flex md:flex-row md:justify-between">
    <h1>
      {dealID ? $_("Editing deal #") + dealID : $_("Adding new deal")}
    </h1>
    <div class="my-5 flex items-center">
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
        <button
          class="btn btn-gray btn-sm mx-2"
          on:click={() => goto(`/deal/${dealID}/${dealVersion ?? ""}`)}
        >
          {$_("Cancel")}
        </button>
      {/if}
      <!--            <span>{{ $t("Leaves edit mode") }}</span>-->
    </div>
  </div>
  <div class="flex h-full overflow-y-hidden">
    <nav class="flex-initial p-2">
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
    <div class="w-full flex-auto overflow-y-auto pl-4 pr-2 pb-16">
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
        <SubmodelEditSection
          model="contract"
          modelName={$_("Contract")}
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
        <SubmodelEditSection
          model="datasource"
          modelName={$_("Data source")}
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

<ManageOverlay
  bind:visible={showReallyQuitOverlay}
  title={$_("Quit without saving?")}
  on:submit={() => onClickClose(true)}
>
  <div class="font-medium">{$_("Do you really want to close the editor?")}</div>
</ManageOverlay>
