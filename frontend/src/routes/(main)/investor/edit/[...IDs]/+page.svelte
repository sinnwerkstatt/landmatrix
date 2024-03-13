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
  import ModalReallyQuit from "$components/ModalReallyQuit.svelte"

  import EditSectionGeneralInfo from "./EditSectionGeneralInfo.svelte"
  import EditSectionInvolvements from "./EditSectionInvolvements.svelte"

  export let data
  let investor = data.investor
  $: investor = data.investor

  let savingInProgress = false
  let showReallyQuitOverlay = false
  $: activeTab = $page.url.hash || "#general"
  $: formChanged = JSON.stringify(investor) !== data.originalInvestor
  $: tabs = [
    { target: "#general", name: $_("General info") },
    { target: "#parent_companies", name: $_("Parent companies") },
    { target: "#tertiary_investors", name: $_("Tertiary investors/lenders") },
    { target: "#data_sources", name: $_("Data sources") },
  ]
  beforeNavigate(({ type, cancel }) => {
    // browser navigation buttons
    if (type === "popstate")
      if (formChanged && !showReallyQuitOverlay) {
        showReallyQuitOverlay = true
        cancel()
      }
  })
  const saveInvestor = async (): Promise<boolean> => {
    savingInProgress = true

    investor.selected_version.datasources = removeEmptyEntries(
      investor.selected_version.datasources ?? [],
    )

    const ret = await fetch(
      data.versionID
        ? `/api/investorversions/${data.versionID}/`
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
      await goto(`/investor/edit/${data.investorID}/${retBody.versionID}/${activeTab}`)
    } else {
      toast.push("Saved data", { classes: ["success"] })
      await invalidate("investor:detail")
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

    await invalidate("investor:detail") // discard changes

    if (!data.investorID) await goto("/")
    else await goto(`/investor/${data.investorID}/${data.versionID ?? ""}`)
  }

  const onClickSave = async (): Promise<void> => {
    if (savingInProgress || !isFormValid()) return
    if (formChanged) await saveInvestor()
  }

  const onClickTab: MouseEventHandler<HTMLAnchorElement> = async e => {
    if (savingInProgress || !isFormValid()) return

    if (formChanged) {
      const success = await saveInvestor()
      if (!success) return
    }

    const hash = (e.target as HTMLAnchorElement).hash
    await goto(hash)
  }
</script>

<div class="editgrid container mx-auto h-full max-h-full">
  <div
    class="mx-2 flex items-center justify-between border-b border-pelorous"
    style="grid-area: header"
  >
    <h1 class="heading4 my-2 mt-3">
      {data.investorID
        ? $_("Editing Investor #") + data.investorID
        : $_("Adding new investor")}
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
      {#if data.investorID}
        <button class="btn btn-cancel" on:click={() => onClickClose(false)}>
          {$_("Close")}
        </button>
      {:else}
        <a
          class="btn btn-cancel mx-2"
          href="/investor/{data.investorID}/{data.versionID ?? ''}"
        >
          {$_("Cancel")}
        </a>
      {/if}
    </div>
  </div>

  <nav
    class="overflow-x-auto whitespace-nowrap p-2 lg:whitespace-normal"
    style="grid-area: sidenav"
  >
    <ul>
      {#each tabs as { target, name }}
        <li
          class="border-pelorous py-2 pr-4 {activeTab === target
            ? 'border-r-4'
            : 'border-r'}"
        >
          <a
            href={target}
            class={activeTab === target ? "text-gray-700 dark:text-white" : "investor"}
            on:click|preventDefault={onClickTab}
          >
            {name}
          </a>
        </li>
      {/each}
    </ul>
  </nav>

  <div class="overflow-y-auto px-4 pb-20" style="grid-area: main">
    {#if activeTab === "#general"}
      <EditSectionGeneralInfo bind:investor />
    {/if}
    {#if activeTab === "#parent_companies"}
      <EditSectionInvolvements
        bind:involvements={investor.involvements}
        investorID={data.investorID}
      />
    {/if}
    {#if activeTab === "#tertiary_investors"}
      <EditSectionInvolvements
        bind:involvements={investor.involvements}
        tertiary
        investorID={data.investorID}
      />
    {/if}
    {#if activeTab === "#data_sources"}
      <EditSectionDataSources
        bind:datasources={investor.selected_version.datasources}
        investorModel
      />
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
