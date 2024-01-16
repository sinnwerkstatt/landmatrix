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

  import EditSectionGeneralInfo from "./EditSectionGeneralInfo.svelte"

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
    { target: "#datasources", name: $_("Data sources") },
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
    // TODO do we need this? should happen automatically
    //   if (!currentForm.checkValidity()) return currentForm.reportValidity()
    savingInProgress = true

    // TODO
    // investor.selected_version.investors = removeEmptyEntries(
    //   investor.selected_version.investors ?? [],
    // )
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
        body: JSON.stringify({ version: investor.selected_version }),
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

    if (retJson.versionID !== investor.selected_version.id) {
      toast.push("Created a new draft", { classes: ["success"] })
      await goto(`/investor/${investor.id}/${retJson.newVersionID}/`)
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

<div class="container mx-auto flex h-full min-h-full flex-col">
  <div class="border-b border-orange md:flex md:flex-row md:justify-between">
    <h1 class="heading4 mt-3">
      {data.investorID
        ? $_("Editing Investor #") + data.investorID
        : $_("Adding new investor")}
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
      {#if data.investorID}
        <button class="btn btn-secondary mx-2" on:click={() => onClickClose(false)}>
          {$_("Close")}
        </button>
      {:else}
        <button
          class="btn btn-gray mx-2"
          on:click={() => goto(`/investor/${data.investorID}/${data.versionID ?? ""}`)}
        >
          {$_("Cancel")}
        </button>
      {/if}
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
      {#if activeTab === "#general"}
        <EditSectionGeneralInfo bind:investor />
      {/if}
      {#if activeTab === "#parent_companies"}
        <!--        <SubmodelEditSection-->
        <!--          id="parent_companies"-->
        <!--          model="involvement"-->
        <!--          modelName={$_("Parent company")}-->
        <!--          bind:entries={investor.investors}-->
        <!--          entriesFilter={i => i.role === Role.PARENT}-->
        <!--          newEntryExtras={{ role: Role.PARENT }}-->
        <!--        />-->
      {/if}
      {#if activeTab === "#tertiary_investors"}
        <!--        <SubmodelEditSection-->
        <!--          id="tertiary_investors"-->
        <!--          model="involvement"-->
        <!--          modelName={$_("Tertiary investor/lender")}-->
        <!--          bind:entries={investor.investors}-->
        <!--          entriesFilter={i => i.role === "LENDER"}-->
        <!--          newEntryExtras={{ role: "LENDER" }}-->
        <!--          fields={[-->
        <!--            "investor",-->
        <!--            "investment_type",-->
        <!--            "percentage",-->
        <!--            "loans_amount",-->
        <!--            "loans_currency",-->
        <!--            "loans_date",-->
        <!--            "comment",-->
        <!--          ]}-->
        <!--        />-->
      {/if}
      {#if activeTab === "#datasources"}
        <EditSectionDataSources
          bind:datasources={investor.selected_version.datasources}
        />
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
