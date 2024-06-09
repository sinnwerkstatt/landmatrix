<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { beforeNavigate, goto, invalidate } from "$app/navigation"

  import type { DealHull } from "$lib/types/newtypes"
  import { getCsrfToken } from "$lib/utils"
  import { removeEmptyEntries } from "$lib/utils/data_processing"

  import { DEAL_SECTIONS } from "$components/Data/Deal/Sections/constants"
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"
  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ModalReallyQuit from "$components/ModalReallyQuit.svelte"
  import SectionNav from "$components/SectionNav.svelte"

  import { mutableDeal } from "./store"

  export let data

  let savingInProgress = false
  let showReallyQuitOverlay = false

  $: $mutableDeal = structuredClone(data.deal)
  $: hasBeenEdited = JSON.stringify(data.deal) !== JSON.stringify($mutableDeal)

  beforeNavigate(({ type, cancel, to }) => {
    // if hasNavigatedToOtherSection
    if (type === "link" && to?.url.pathname.includes(data.baseUrl)) {
      if (savingInProgress || !isFormValid()) {
        cancel()
        return
      }

      if (hasBeenEdited) {
        saveDeal($mutableDeal).then(success => (success ? goto(to?.url) : null))
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

  const saveDeal = async (deal: DealHull): Promise<boolean> => {
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
      await goto(`/deal/edit/${deal.id}/${retBody.versionID}/${data.dealSection}`)
    } else {
      toast.push("Saved data", { classes: ["success"] })
      await invalidate("deal:detail")
    }
    savingInProgress = false
    return true
  }

  const isFormValid = (): boolean => {
    const currentForm: HTMLFormElement | null =
      document.querySelector<HTMLFormElement>("form")

    if (!currentForm) {
      toast.push("Internal error. Can not grab the form. Try reloading the page.", {
        classes: ["error"],
      })
      return false
    }

    return currentForm.reportValidity()
  }

  const onClickClose = async (force = false): Promise<void> => {
    if (hasBeenEdited && !force) {
      showReallyQuitOverlay = true
      return
    }

    await invalidate("deal:detail") // discard changes

    if (!data.dealID) await goto("/")
    else await goto(`/deal/${data.dealID}/${data.dealVersion ?? ""}`)
  }

  const onClickSave = async (): Promise<void> => {
    if (savingInProgress || !isFormValid()) return
    if (hasBeenEdited) await saveDeal($mutableDeal)
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
      {data.dealID ? $_("Editing deal #") + data.dealID : $_("Adding new deal")}
      <span class="text-[0.8em]">
        <CountryField value={data.deal.country_id} />
      </span>
    </h1>
    <div class="my-2 flex items-center gap-2 lg:my-5">
      <button
        class="btn btn-primary flex items-center gap-2"
        class:disabled={!hasBeenEdited || savingInProgress}
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

  <div style="grid-area: sidenav">
    <SectionNav
      sections={DEAL_SECTIONS.filter(s => s !== "history").map(s => ({
        slug: s,
        label: $dealSectionLookup[s].label,
      }))}
      baseUrl={data.baseUrl}
    />
  </div>

  <div class="overflow-y-auto px-4" style="grid-area: main">
    <slot />
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
