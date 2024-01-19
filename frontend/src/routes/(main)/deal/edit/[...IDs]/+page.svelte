<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"
  import type { MouseEventHandler } from "svelte/elements"

  import { beforeNavigate, goto, invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { getCsrfToken } from "$lib/utils"
  import { removeEmptyEntries } from "$lib/utils/data_processing"

  import EditSectionDataSources from "$components/EditSectionDataSources.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import Modal from "$components/Modal.svelte"

  import EditSectionContracts from "./EditSectionContracts.svelte"
  import EditSectionEmployment from "./EditSectionEmployment.svelte"
  import EditSectionFormerUse from "./EditSectionFormerUse.svelte"
  import EditSectionGenderRelatedInfo from "./EditSectionGenderRelatedInfo.svelte"
  import EditSectionGeneralInfo from "./EditSectionGeneralInfo.svelte"
  import EditSectionInvestorInfo from "./EditSectionInvestorInfo.svelte"
  import EditSectionLocalCommunities from "./EditSectionLocalCommunities.svelte"
  import EditSectionLocations from "./EditSectionLocations.svelte"
  import EditSectionOverallComment from "./EditSectionOverallComment.svelte"
  import EditSectionProduceInfo from "./EditSectionProduceInfo.svelte"
  import EditSectionWater from "./EditSectionWater.svelte"

  export let data
  let deal = data.deal
  $: deal = data.deal

  let savingInProgress = false
  let showReallyQuitOverlay = false
  $: activeTab = $page.url.hash || "#locations"
  $: formChanged = JSON.stringify(deal) !== data.originalDeal
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

  const saveDeal = async (): Promise<boolean> => {
    savingInProgress = true

    deal.selected_version.locations = removeEmptyEntries(
      deal.selected_version.locations ?? [],
    )
    deal.selected_version.contracts = removeEmptyEntries(
      deal.selected_version.contracts ?? [],
    )
    deal.selected_version.datasources = removeEmptyEntries(
      deal.selected_version.datasources ?? [],
    )

    const ret = await fetch(
      data.versionID
        ? `/api/dealversions/${data.versionID}/`
        : `/api/deals/${data.dealID}/`,
      {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({ version: deal.selected_version }),
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      },
    )
    const retJson = await ret.json()

    if (ret.status === 400) {
      toast.push(
        Object.entries(retJson)
          .map(([k, v]) => `<p><b>${k}</b><br/>${v}<br/><p>`)
          .join(""),
        { classes: ["error"] },
      )
      savingInProgress = false
      return false
    }
    if (!ret.ok) {
      toast.push(`Unexpected error: ${JSON.stringify(retJson)}`, { classes: ["error"] })
      savingInProgress = false
      return false
    }

    if (retJson.versionID !== deal.selected_version.id) {
      toast.push("Created a new draft", { classes: ["success"] })
      await goto(`/deal/edit/${deal.id}/${retJson.versionID}/`)
    } else {
      toast.push("Saved data", { classes: ["success"] })
      await invalidate("deal:detail")
    }
    savingInProgress = false
    return true
  }

  const onClickClose = async (force = false): Promise<void> => {
    if (formChanged && !force) {
      showReallyQuitOverlay = true
      return
    }

    await invalidate("deal:detail") // discard changes

    if (!data.dealID) await goto("/")
    else await goto(`/deal/${data.dealID}/${data.versionID ?? ""}`)
  }

  const onClickSave = async (): Promise<void> => {
    if (savingInProgress || !isFormValid()) return
    if (formChanged) await saveDeal()
  }

  const onClickTab: MouseEventHandler<HTMLAnchorElement> = async e => {
    if (savingInProgress || !isFormValid()) return

    if (formChanged) {
      const success = await saveDeal()
      if (!success) return
    }

    const hash = (e.target as HTMLAnchorElement).hash
    await goto(hash)
  }
</script>

<div class="container mx-auto flex h-full min-h-full flex-col">
  <div class="border-b border-orange md:flex md:flex-row md:justify-between">
    <h1 class="heading4 mt-3 flex flex-col gap-2">
      {data.dealID ? $_("Editing deal #") + data.dealID : $_("Adding new deal")}
      <span style="font-size: 0.8em;">{data.deal.country.name}</span>
    </h1>
    <div class="my-5 flex items-center">
      <button
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!formChanged || savingInProgress}
        on:click|preventDefault={onClickSave}
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
        {data.dealID ? $_("Close") : $_("Cancel")}
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
              class={activeTab === target ? "text-gray-700 dark:text-white" : ""}
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
        <EditSectionLocations
          bind:locations={deal.selected_version.locations}
          country={deal.country}
        />
      {/if}
      {#if activeTab === "#general"}
        <EditSectionGeneralInfo bind:deal />
      {/if}
      {#if activeTab === "#contracts"}
        <EditSectionContracts bind:contracts={deal.selected_version.contracts} />
      {/if}
      {#if activeTab === "#employment"}
        <EditSectionEmployment bind:deal />
      {/if}
      {#if activeTab === "#investor_info"}
        <EditSectionInvestorInfo bind:deal />
      {/if}
      {#if activeTab === "#data_sources"}
        <EditSectionDataSources bind:datasources={deal.selected_version.datasources} />
      {/if}
      {#if activeTab === "#local_communities"}
        <EditSectionLocalCommunities bind:deal />
      {/if}
      {#if activeTab === "#former_use"}
        <EditSectionFormerUse bind:deal />
      {/if}
      {#if activeTab === "#produce_info"}
        <EditSectionProduceInfo bind:deal />
      {/if}
      {#if activeTab === "#water"}
        <EditSectionWater bind:deal />
      {/if}
      {#if activeTab === "#gender_related_info"}
        <EditSectionGenderRelatedInfo bind:deal />
      {/if}
      {#if activeTab === "#overall_comment"}
        <EditSectionOverallComment bind:deal />
      {/if}
    </div>
  </div>
</div>

<Modal bind:open={showReallyQuitOverlay} dismissible>
  <h2 class="heading4">{$_("Quit without saving?")}</h2>
  <hr />
  <div class="mb-12 mt-6 text-lg">
    {$_("Do you really want to close the editor?")}
    <br />
    {$_("All unsaved changes will be lost.")}
  </div>
  <div class="flex justify-end gap-4">
    <button
      class="butn-outline"
      on:click={() => (showReallyQuitOverlay = false)}
      autofocus
    >
      Continue editing
    </button>
    <button class="butn butn-yellow" on:click={() => onClickClose(true)}>
      Quit without saving
    </button>
  </div>
</Modal>
