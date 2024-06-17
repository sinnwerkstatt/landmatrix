<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { beforeNavigate, goto, invalidate } from "$app/navigation"

  import { getCsrfToken } from "$lib/utils"
  import { removeEmptyEntries } from "$lib/utils/data_processing"

  import { INVESTOR_EDIT_SECTIONS } from "$components/Data/Investor/Sections/constants"
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"
  import SectionNav from "$components/Data/SectionNav.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ModalReallyQuit from "$components/ModalReallyQuit.svelte"

  import { mutableInvestor, type MutableInvestor } from "./store"

  export let data

  let savingInProgress = false
  let showReallyQuitOverlay = false

  $: $mutableInvestor = structuredClone(data.investor) as MutableInvestor
  $: hasBeenEdited = JSON.stringify(data.investor) !== JSON.stringify($mutableInvestor)

  beforeNavigate(({ type, cancel, to }) => {
    // if hasNavigatedToOtherSection
    if (type === "link" && to?.url.pathname.includes(data.baseUrl)) {
      if (savingInProgress || !isFormValid()) {
        cancel()
        return
      }

      if (hasBeenEdited) {
        saveInvestor($mutableInvestor).then(success => (success ? goto(to?.url) : null))
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
  const saveInvestor = async (investor: MutableInvestor): Promise<boolean> => {
    savingInProgress = true

    investor.selected_version.datasources = removeEmptyEntries(
      investor.selected_version.datasources ?? [],
    )

    const ret = await fetch(
      data.investorVersion
        ? `/api/investorversions/${data.investorVersion}/`
        : `/api/investors/${data.investorID}/`,
      {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({
          version: {
            ...investor.selected_version,
            involvements: investor.involvements,
          },
        }),
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

    if (retBody.versionID !== investor.selected_version.id) {
      toast.push("Created a new draft", { classes: ["success"] })
      await goto(
        `/investor/edit/${data.investorID}/${retBody.versionID}/${data.investorSection}`,
      )
    } else {
      toast.push("Saved data", { classes: ["success"] })
      await invalidate("investor:detail")
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

    await invalidate("investor:detail") // discard changes

    if (!data.investorID) await goto("/")
    else await goto(`/investor/${data.investorID}/${data.investorVersion ?? ""}`)
  }

  const onClickSave = async (): Promise<void> => {
    if (savingInProgress || !isFormValid()) return
    if (hasBeenEdited) await saveInvestor($mutableInvestor)
  }
</script>

<svelte:head>
  <title>{$_("Investor Edit")} #{data.investor.id}</title>
</svelte:head>

<div class="editgrid container mx-auto h-full max-h-full">
  <div
    class="mx-2 flex flex-wrap items-center justify-between border-b border-orange"
    style="grid-area: header"
  >
    <h1 class="heading3 mb-0 mt-3">
      {$_("Editing")}
      {#if data.investor.selected_version.name_unknown}
        <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
      {:else}
        {data.investor.selected_version.name}
      {/if}
      <small>#{data.investor.id}</small>
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
        {data.investorID ? $_("Close") : $_("Cancel")}
      </button>
    </div>
  </div>

  <div style="grid-area: sidenav">
    <SectionNav
      sections={INVESTOR_EDIT_SECTIONS.map(s => ({
        slug: s,
        label: $investorSectionLookup[s].label,
      }))}
      baseUrl={data.baseUrl}
    />
  </div>

  <div class="mt-2 overflow-y-auto px-4 pb-20" style="grid-area: main">
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
