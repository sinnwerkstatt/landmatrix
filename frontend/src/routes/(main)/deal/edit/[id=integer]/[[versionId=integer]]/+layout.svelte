<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { beforeNavigate, goto, invalidate } from "$app/navigation"

  import type { Contract, DealDataSource, MutableDealHull } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import { isEmptyDataSource } from "$components/Data/DataSources/dataSources"
  import { DEAL_SECTIONS } from "$components/Data/Deal/Sections/constants"
  import { isEmptyContract } from "$components/Data/Deal/Sections/Contracts/contracts"
  import { isEmptyLocation } from "$components/Data/Deal/Sections/Locations/locations"
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"
  import SectionNav from "$components/Data/SectionNav.svelte"
  import { getMutableObject } from "$components/Data/stores"
  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ModalReallyQuit from "$components/ModalReallyQuit.svelte"
  import ReviewChangesModal from "$components/Quotations/ReviewChangesModal.svelte"

  let { data, children } = $props()

  let savingInProgress = $state(false)
  let showReallyQuitOverlay = $state(false)

  const mutableDeal = getMutableObject("deal")
  const hasBeenEdited = $derived(
    JSON.stringify(data.deal) !== JSON.stringify($mutableDeal),
  )

  beforeNavigate(({ type, cancel, to }) => {
    // if hasNavigatedToOtherSection
    if (type === "link" && to?.url.pathname.includes(data.baseUrl)) {
      if (savingInProgress || !isFormValid()) {
        cancel()
        return
      }
    }

    // browser navigation
    // TODO: extend this for any navigation
    if (type === "popstate")
      if (hasBeenEdited && !showReallyQuitOverlay) {
        showReallyQuitOverlay = true
        cancel()
        return
      }
  })

  const cleanDeal = (deal: MutableDealHull): void => {
    deal.selected_version.locations = (deal.selected_version.locations ?? []).filter(
      x => !isEmptyLocation(x),
    )
    deal.selected_version.contracts = (deal.selected_version.contracts ?? []).filter(
      x => !isEmptyContract(x as Contract),
    )
    deal.selected_version.datasources = (
      deal.selected_version.datasources ?? []
    ).filter(x => !isEmptyDataSource(x as DealDataSource))
  }

  const saveDeal = async (deal: MutableDealHull): Promise<boolean> => {
    cleanDeal(deal)

    savingInProgress = true

    const ret = await fetch(
      data.dealVersion
        ? `/api/dealversions/${data.dealVersion}/`
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
      console.error("PUT Error:", e)
      console.error("Raw Response:", await ret.text())

      toast.push(
        "We received an unexpected error from the backend. For details, check the browser console",
        { classes: ["error"] },
      )

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
      await goto(`/deal/edit/${deal.id}/${retBody.versionID}/`)
    } else {
      toast.push("Saved data", { classes: ["success"] })
      await invalidate("deal:detail")
    }

    savingInProgress = false
    return true
  }

  const isFormValid = (): boolean => {
    const currentForms = document.querySelectorAll<HTMLFormElement>("form")

    if (currentForms.length === 0) {
      toast.push("Internal error. Can not grab the form. Try reloading the page.", {
        classes: ["error"],
      })
      return false
    }

    return [...currentForms].every(f => f.reportValidity())
  }

  const onClickClose = async (force = false): Promise<void> => {
    if (hasBeenEdited && !force) {
      showReallyQuitOverlay = true
      return
    }

    await invalidate("deal:detail") // discard changes
    await goto(
      data.dealVersion
        ? `/deal/${data.dealID}/${data.dealVersion}/`
        : `/deal/${data.dealID}/`,
    )
  }

  let showReviewChangesModal = $state(false)

  const onClickSave = async () => {
    if (savingInProgress || !isFormValid()) return

    if (!showReviewChangesModal) {
      cleanDeal($mutableDeal)
      showReviewChangesModal = true
    } else {
      await saveDeal($mutableDeal)
      showReviewChangesModal = false
    }
  }
</script>

<svelte:head>
  <title>{$_("Deal Edit")} #{data.deal.id}</title>
</svelte:head>

<div class="editgrid container mx-auto h-full max-h-full">
  <div
    class="mx-2 flex flex-wrap items-center justify-between border-b border-orange"
    style="grid-area: header"
  >
    <h1 class="heading4 my-2 mt-3 flex items-baseline gap-2">
      {$_("Editing") + " " + $_("Deal") + ` #${data.deal.id}`}
      <span class="text-[0.8em]">
        <CountryField value={data.deal.country_id} />
      </span>
    </h1>
    <div class="my-2 flex items-center gap-2 lg:my-5">
      <button
        class="btn btn-primary flex items-center gap-2"
        class:disabled={!hasBeenEdited || savingInProgress}
        type="button"
        onclick={onClickSave}
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
        type="button"
        onclick={() => onClickClose()}
      >
        {$_("Close")}
      </button>
    </div>
  </div>

  <div style="grid-area: sidenav">
    <SectionNav
      sections={DEAL_SECTIONS.filter(s => s !== "history").map(s => ({
        slug: s,
        label: $dealSectionLookup[s].label,
      }))}
      baseUrl={data.baseUrl}
    />
  </div>

  <div class="mt-2 overflow-y-auto px-4 pb-20" style="grid-area: main">
    {@render children?.()}
  </div>
</div>

<ModalReallyQuit bind:open={showReallyQuitOverlay} onclick={() => onClickClose(true)} />

{#if showReviewChangesModal}
  <ReviewChangesModal
    bind:open={showReviewChangesModal}
    onclick={onClickSave}
    oldObject={data.deal}
    newObject={mutableDeal}
  />
{/if}

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
