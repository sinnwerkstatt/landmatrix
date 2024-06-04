<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"
  import type { MouseEventHandler } from "svelte/elements"

  import { beforeNavigate, goto, invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { getCsrfToken } from "$lib/utils"
  import { removeEmptyEntries } from "$lib/utils/data_processing"

  import EditSectionDataSources from "$components/EditSectionDataSources.svelte"
  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ModalReallyQuit from "$components/ModalReallyQuit.svelte"

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

  let deal: (typeof data)["deal"]
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

    let retBody
    try {
      retBody = await ret.clone().json()
    } catch (e) {
      retBody = await ret.text()
      toast.push(
        "We received an unexpected error from the backend. For details, check the browser console",
        { classes: ["error"] },
      )
      console.error(retBody)
      savingInProgress = false
      return false
    }

    if (ret.status === 400) {
      toast.push(
        Object.entries(retBody)
          .map(([k, v]) => `<p><b>${k}</b><br/>${v}<br/><p>`)
          .join(""),
        { classes: ["error"] },
      )
      savingInProgress = false
      return false
    }
    if (!ret.ok) {
      toast.push(`Unexpected error: ${JSON.stringify(retBody)}`, { classes: ["error"] })
      savingInProgress = false
      return false
    }

    if (retBody.versionID !== deal.selected_version.id) {
      toast.push("Created a new draft", { classes: ["success"] })
      await goto(`/deal/edit/${deal.id}/${retBody.versionID}/${activeTab}`)
    } else {
      toast.push("Saved data", { classes: ["success"] })
      await invalidate("deal:detail")
    }
    savingInProgress = false
    return true
  }

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

<div class="editgrid container mx-auto h-full max-h-full">
  <div
    class="mx-2 flex flex-wrap items-center justify-between border-b border-orange"
    style="grid-area: header"
  >
    <h1 class="heading4 my-2 mt-3 flex items-baseline gap-2">
      {data.dealID ? $_("Editing deal #") + data.dealID : $_("Adding new deal")}
      <span class="text-[0.8em]">
        <CountryField value={data.deal.country_id} />
      </span>
    </h1>
    <div class="my-2 flex items-center gap-2 lg:my-5">
      <button
        class="btn btn-primary flex items-center gap-2"
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
        class="btn btn-cancel"
        class:disabled={savingInProgress}
        on:click|preventDefault={() => onClickClose()}
      >
        {data.dealID ? $_("Close") : $_("Cancel")}
      </button>
    </div>
  </div>

  <nav
    class="overflow-x-auto whitespace-nowrap p-2 lg:whitespace-normal"
    style="grid-area: sidenav"
  >
    <ul class="flex lg:flex-col">
      {#each tabs as { target, name }}
        <li
          class="border-orange py-3 pr-4 text-center leading-tight lg:text-left {activeTab ===
          target
            ? 'border-b-4 font-semibold lg:border-0 lg:border-r-4'
            : 'border-b lg:border-0 lg:border-r'}"
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
  <div class="overflow-y-auto px-4" style="grid-area: main">
    {#if activeTab === "#locations"}
      <EditSectionLocations
        bind:locations={deal.selected_version.locations}
        country={$page.data.countries.find(c => c.id === deal.country_id)}
      />
    {/if}
    {#if activeTab === "#general"}
      <EditSectionGeneralInfo bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#contracts"}
      <EditSectionContracts bind:contracts={deal.selected_version.contracts} />
    {/if}
    {#if activeTab === "#employment"}
      <EditSectionEmployment bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#investor_info"}
      <EditSectionInvestorInfo bind:deal />
    {/if}
    {#if activeTab === "#data_sources"}
      <EditSectionDataSources bind:datasources={deal.selected_version.datasources} />
    {/if}
    {#if activeTab === "#local_communities"}
      <EditSectionLocalCommunities bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#former_use"}
      <EditSectionFormerUse bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#produce_info"}
      <EditSectionProduceInfo bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#water"}
      <EditSectionWater bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#gender_related_info"}
      <EditSectionGenderRelatedInfo bind:version={deal.selected_version} />
    {/if}
    {#if activeTab === "#overall_comment"}
      <EditSectionOverallComment bind:version={deal.selected_version} />
    {/if}
  </div>
</div>

<ModalReallyQuit
  bind:open={showReallyQuitOverlay}
  on:click={() => onClickClose(true)}
/>

<style>
  .editgrid {
    display: grid;
    grid-template-rows: auto 1fr;
    grid-template-columns: repeat(6, 1fr);
    grid-template-areas:
      "header header header header header header"
      "sidenav main main main main main";

    @media (width <= 1024px) {
      grid-template-rows: auto auto 1fr;
      grid-template-columns: 1fr;
      grid-template-areas:
        "header"
        "sidenav"
        "main";
    }
  }
</style>
