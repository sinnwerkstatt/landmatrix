<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { beforeNavigate, goto, invalidateAll } from "$app/navigation"
  import { page } from "$app/stores"

  import { investorSections } from "$lib/sections"
  import type { Investor } from "$lib/types/investor"
  import { Role } from "$lib/types/investor"
  import { removeEmptyEntries } from "$lib/utils/data_processing"

  import EditField from "$components/Fields/EditField.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import ManageOverlay from "$components/Management/ManageOverlay.svelte"
  import SubmodelEditSection from "$components/Management/SubmodelEditSection.svelte"

  export let investor: Investor
  export let investorID: number
  export let investorVersion: number

  let originalInvestor = JSON.stringify(investor)
  let savingInProgress = false
  let showReallyQuitOverlay = false
  $: activeTab = $page.url.hash || "#general"
  $: formChanged = JSON.stringify(investor) !== originalInvestor
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

  async function saveInvestor(hash: string) {
    const currentForm: HTMLFormElement | null =
      document.querySelector<HTMLFormElement>(activeTab)
    if (!currentForm) {
      toast.push("Internal error. Can not grab the form. Try reloading the page.", {
        classes: ["error"],
      })
      return
    }

    if (!currentForm.checkValidity()) return currentForm.reportValidity()

    investor.investors = removeEmptyEntries(investor.investors ?? [])
    investor.datasources = removeEmptyEntries(investor.datasources ?? [])

    savingInProgress = true

    const { data, error } = await ($page.data.urqlClient as Client)
      .mutation<{ investor_edit: { investorId: number; investorVersion?: number } }>(
        gql`
          mutation ($id: Int!, $version: Int, $payload: Payload) {
            investor_edit(id: $id, version: $version, payload: $payload) {
              investorId
              investorVersion
            }
          }
        `,
        {
          id: investorID ? +investorID : -1,
          version: investorVersion ? +investorVersion : null,
          payload: {
            ...investor,
            versions: undefined,
            comments: undefined,
            workflowinfos: undefined,
            ventures: undefined,
            involvements: undefined,
          },
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
        `/investor/edit/${data.investor_edit.investorId}/${
          data.investor_edit.investorVersion
        }${hash ?? ""}`,
      )
      // update original investor only after route change
      originalInvestor = JSON.stringify(investor)
    }

    savingInProgress = false
  }

  const onClickClose = async (force: boolean) => {
    if (formChanged && !force) showReallyQuitOverlay = true
    else {
      await invalidateAll()
      if (!investorID) await goto("/")
      else await goto(`/investor/${investorID}/${investorVersion ?? ""}`)
    }
  }

  const onClickTab = async (e: PointerEvent) => {
    if (savingInProgress) return

    const hash = (e.target as HTMLAnchorElement).hash
    if (formChanged) {
      await saveInvestor(hash)
    } else {
      await goto(hash)
    }
  }
</script>

<div class="container mx-auto flex h-full min-h-full flex-col">
  <div class="border-b border-orange md:flex md:flex-row md:justify-between">
    <h1>
      {investorID ? $_("Editing Investor #") + investorID : $_("Adding new investor")}
    </h1>
    <div class="my-5 flex items-center">
      <button
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!formChanged || savingInProgress}
        on:click={() => saveInvestor(location.hash)}
        type="submit"
      >
        {#if savingInProgress}
          <LoadingSpinner /> {$_("Saving...")}
        {:else}
          {$_("Save")}
        {/if}
      </button>
      {#if investorID}
        <button class="btn btn-secondary mx-2" on:click={() => onClickClose(false)}>
          {$_("Close")}
        </button>
      {:else}
        <button
          class="btn btn-gray mx-2"
          on:click={() => goto(`/investor/${investorID}/${investorVersion ?? ""}`)}
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
            {#if name}
              <a
                href={target}
                class={activeTab === target ? "text-lm-dark dark:text-white" : ""}
                on:click|preventDefault={onClickTab}
              >
                {name}
              </a>
            {:else}
              <hr />
            {/if}
          </li>
        {/each}
      </ul>
    </nav>
    <div class="w-full flex-auto overflow-y-auto pl-4 pr-2 pb-16">
      {#if activeTab === "#general"}
        <section>
          <form id="general">
            {#each $investorSections.general_info as subsection}
              <div class="mt-2 space-y-4">
                <h3 class="my-0">{subsection.name}</h3>
                {#each subsection.fields as fieldname}
                  <EditField
                    model="investor"
                    {fieldname}
                    bind:value={investor[fieldname]}
                  />
                {/each}
              </div>
            {/each}
            <slot />
          </form>
        </section>
      {/if}
      {#if activeTab === "#parent_companies"}
        <SubmodelEditSection
          id="parent_companies"
          model="involvement"
          modelName={$_("Parent company")}
          bind:entries={investor.investors}
          entriesFilter={i => i.role === Role.PARENT}
          newEntryExtras={{ role: Role.PARENT }}
        />
      {/if}
      {#if activeTab === "#tertiary_investors"}
        <SubmodelEditSection
          id="tertiary_investors"
          model="involvement"
          modelName={$_("Tertiary investor/lender")}
          bind:entries={investor.investors}
          entriesFilter={i => i.role === "LENDER"}
          newEntryExtras={{ role: "LENDER" }}
          fields={[
            "investor",
            "investment_type",
            "percentage",
            "loans_amount",
            "loans_currency",
            "loans_date",
            "comment",
          ]}
        />
      {/if}
      {#if activeTab === "#data_sources"}
        <SubmodelEditSection
          model="datasource"
          modelName={$_("Data source")}
          bind:entries={investor.datasources}
          id="data_sources"
        />
      {/if}
    </div>
  </div>
</div>

{#if showReallyQuitOverlay}
  <ManageOverlay
    bind:visible={showReallyQuitOverlay}
    on:submit={() => onClickClose(true)}
    title={$_("Quit without saving?")}
  >
    <div class="font-medium">{$_("Do you really want to close the editor?")}</div>
  </ManageOverlay>
{/if}
