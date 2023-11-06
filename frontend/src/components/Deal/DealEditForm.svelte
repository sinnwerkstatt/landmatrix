<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { beforeNavigate, goto, invalidateAll } from "$app/navigation"
  import { page } from "$app/stores"

  import { dealSections } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"
  import { removeEmptyEntries, discardEmptyFields } from "$lib/utils/data_processing"

  import DealEditSection from "$components/Deal/DealEditSection.svelte"
  import DealLocationsEditSection from "$components/Deal/DealLocationsEditSection.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ManageOverlay from "$components/Management/ManageOverlay.svelte"
  import SubmodelEditSection from "$components/Management/SubmodelEditSection.svelte"

  export let deal: Deal
  export let dealID: number
  export let dealVersion: number

  let originalDeal = JSON.stringify(discardEmptyFields(deal))
  let savingInProgress = false
  let showReallyQuitOverlay = false
  $: activeTab = $page.url.hash || "#locations"
  $: formChanged = JSON.stringify(discardEmptyFields(deal)) !== originalDeal
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

  beforeNavigate(({ type, cancel }) => {
    // browser navigation buttons
    if (type === "popstate")
      if (formChanged && !showReallyQuitOverlay) {
        showReallyQuitOverlay = true
        cancel()
      }
  })

  const isFormValid = (): boolean => {
    const currentForm: HTMLFormElement | null =
      document.querySelector<HTMLFormElement>(activeTab)

    if (!currentForm) {
      toast.push("Internal error. Can not grab the form. Try reloading the page.", {
        classes: ["error"],
      })
      return false
    }

    return currentForm.reportValidity()
  }

  const saveDeal = async (): Promise<void> => {
    savingInProgress = true

    deal.locations = removeEmptyEntries(deal.locations ?? [])
    deal.contracts = removeEmptyEntries(deal.contracts ?? [])
    deal.datasources = removeEmptyEntries(deal.datasources ?? [])

    const { data, error } = await ($page.data.urqlClient as Client)
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

    if (error) {
      const message = error.networkError
        ? "Network Error: Please check your internet connection."
        : error.graphQLErrors.map(e => e.message).includes("EDITING_OLD_VERSION")
        ? "You are trying to edit an old version!"
        : `GraphQLError: ${error.message}`

      toast.push(message, { classes: ["error"] })
    } else if (!data) {
      toast.push("Unknown Problem: Please contact support.", { classes: ["error"] })
    } else {
      await goto(
        `/deal/edit/${data.deal_edit.dealId}/${data.deal_edit.dealVersion}${location.hash}`,
      )
      // update original deal only after route change
      originalDeal = JSON.stringify(discardEmptyFields(deal))
    }

    savingInProgress = false
  }

  const onClickClose = async (force = false): Promise<void> => {
    if (formChanged && !force) {
      showReallyQuitOverlay = true
      return
    }

    await invalidateAll() // discard changes

    if (!dealID) {
      await goto("/")
    } else {
      await goto(`/deal/${dealID}/${dealVersion ?? ""}`)
    }
  }

  const onClickSave = async (): Promise<void> => {
    if (savingInProgress || !isFormValid()) {
      return
    }

    if (formChanged) {
      await saveDeal()
    }
  }

  const onClickTab = async (e: PointerEvent): Promise<void> => {
    if (savingInProgress || !isFormValid()) {
      return
    }

    if (formChanged) {
      await saveDeal()
    }

    const hash = (e.target as HTMLAnchorElement).hash
    await goto(hash)
  }
</script>

<div class="container mx-auto flex h-full min-h-full flex-col">
  <div class="border-b border-orange md:flex md:flex-row md:justify-between">
    <h1>
      {dealID ? $_("Editing deal #") + dealID : $_("Adding new deal")}
    </h1>
    <div class="my-5 flex items-center">
      <button
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!formChanged || savingInProgress}
        on:click|preventDefault={() => onClickSave()}
      >
        {#if savingInProgress}
          <LoadingSpinner /> {$_("Saving...")}
        {:else}
          {$_("Save")}
        {/if}
      </button>
      <button
        class="btn btn-gray mx-2"
        class:disabled={savingInProgress}
        on:click|preventDefault={() => onClickClose()}
      >
        {dealID ? $_("Close") : $_("Cancel")}
      </button>
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
            <a
              href={target}
              class={activeTab === target ? "text-lm-dark dark:text-white" : ""}
              on:click|preventDefault={onClickTab}
            >
              {name}
            </a>
          </li>
        {/each}
      </ul>
    </nav>
    <div class="w-full flex-auto overflow-y-auto pb-16 pl-4 pr-2">
      {#if activeTab === "#locations"}
        <DealLocationsEditSection
          bind:locations={deal.locations}
          bind:country={deal.country}
        />
      {/if}
      {#if activeTab === "#general"}
        <DealEditSection bind:deal sections={$dealSections.general_info} id="general" />
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
        <DealEditSection
          bind:deal
          sections={$dealSections.employment}
          id="employment"
        />
      {/if}
      {#if activeTab === "#investor_info"}
        <DealEditSection
          bind:deal
          sections={$dealSections.investor_info}
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
          sections={$dealSections.local_communities}
          id="local_communities"
        />
      {/if}
      {#if activeTab === "#former_use"}
        <DealEditSection
          bind:deal
          sections={$dealSections.former_use}
          id="former_use"
        />
      {/if}
      {#if activeTab === "#produce_info"}
        <DealEditSection
          bind:deal
          sections={$dealSections.produce_info}
          id="produce_info"
        />
      {/if}
      {#if activeTab === "#water"}
        <DealEditSection bind:deal sections={$dealSections.water} id="water" />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <DealEditSection
          bind:deal
          sections={$dealSections.gender_related_info}
          id="gender_related_info"
        />
      {/if}
      {#if activeTab === "#overall_comment"}
        <DealEditSection
          bind:deal
          sections={$dealSections.overall_comment}
          id="overall_comment"
        />
      {/if}
    </div>
  </div>
</div>

{#if showReallyQuitOverlay}
  <ManageOverlay
    bind:visible={showReallyQuitOverlay}
    title={$_("Quit without saving?")}
    on:submit={() => onClickClose(true)}
  >
    <div class="font-medium">{$_("Do you really want to close the editor?")}</div>
  </ManageOverlay>
{/if}
