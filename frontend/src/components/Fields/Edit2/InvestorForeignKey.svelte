<script lang="ts">
  import { _ } from "svelte-i18n"

  import { simpleInvestors } from "$lib/stores"
  import type { SimpleInvestor } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import EditField from "$components/Fields/EditField.svelte"
  import VirtualListSelect, {
    type FilterFn,
  } from "$components/LowLevel/VirtualListSelect.svelte"
  import Modal from "$components/Modal.svelte"

  export let value: number | null

  export let extras: {
    required?: boolean
    creatable?: boolean
    excludeIds?: number[]
  } = {}

  interface InvestorItem extends SimpleInvestor {
    created?: boolean
  }

  class NewInvestor {
    name: string = ""
    country: number | null = null
    classification: string = ""
    homepage: string = ""
    opencorporates: string = ""
    comment: string = ""
  }

  let newInvestor: NewInvestor | undefined
  let showNewInvestorForm = false

  let items: InvestorItem[]
  $: items = $simpleInvestors
    .filter(i => !i.deleted)
    .filter(i => !(extras.excludeIds ?? []).includes(i.id))

  let listValue: InvestorItem | undefined
  $: listValue = $simpleInvestors.find(i => i.id === value)

  const onInvestorInput = (e: CustomEvent<InvestorItem | null>) => {
    const investorItem = e.detail

    if (investorItem && investorItem.created) {
      newInvestor = new NewInvestor()
      newInvestor.name = investorItem.name
      showNewInvestorForm = true
      return
    }

    newInvestor = undefined
    showNewInvestorForm = false

    value = investorItem ? investorItem.id : null
  }

  const addNewInvestor = async () => {
    const ret = await fetch(`/api/investors/`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ version: newInvestor }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    const retJson = await ret.json()

    if (ret.ok) {
      const newI: InvestorItem = {
        id: retJson.investorID,
        name: newInvestor!.name,
        active: false,
        deleted: false,
      }
      value = newI.id
      // FIXME: Dirty hack to show select newInvestor in dropdown
      $simpleInvestors.push(newI)
      newInvestor = undefined
      showNewInvestorForm = false
    }
  }

  const itemFilter: FilterFn<InvestorItem> = (label, filterText, item) => {
    const filterTextLower = filterText.toLowerCase()
    return (
      item.name?.toLowerCase().includes(filterTextLower) ||
      item.id?.toString().includes(filterTextLower)
    )
  }
</script>

<VirtualListSelect
  creatable={extras.creatable}
  disabled={showNewInvestorForm}
  {itemFilter}
  {items}
  label="name"
  on:input={onInvestorInput}
  placeholder={$_("Select investor")}
  required={extras.required}
  value={listValue}
>
  <svelte:fragment let:selection slot="selection">
    {#if selection.created}
      <div class="font-semibold italic">[new investor]</div>
    {:else}
      {#if selection.deleted}
        <span class="font-bold text-red">
          {$_("Deleted")}:
        </span>
      {:else if !selection.active}
        <span class="font-bold text-purple">
          {$_("Draft")}:
        </span>
      {/if}
      {selection.name} (#{selection.id})
    {/if}
  </svelte:fragment>
  <svelte:fragment let:item slot="item">
    {#if item.created}
      {$_("Create")}: {item.name}
    {:else}
      {#if !item.active}
        <span class="font-bold text-purple">
          {$_("Draft")}:
        </span>
      {/if}
      {item.name} (#{item.id})
    {/if}
  </svelte:fragment>
</VirtualListSelect>

{#if !showNewInvestorForm && value}
  <div class="container p-2">
    <a href="/investor/{value}/" rel="noreferrer" target="_blank" class="investor">
      {$_("Show details for investor")}
    </a>
  </div>
{/if}

<Modal bind:open={showNewInvestorForm} class="min-w-[60%]">
  <form class="my-6 block" on:submit|preventDefault={addNewInvestor}>
    <div class="heading4">{$_("Create new investor")}</div>
    {#if newInvestor}
      <div class="container">
        <EditField
          bind:value={newInvestor.name}
          fieldname="name"
          model="investor"
          showLabel
        />
        <EditField
          bind:value={newInvestor.country}
          extras={{ required: true }}
          fieldname="country"
          model="investor"
          showLabel
        />
        <EditField
          bind:value={newInvestor.classification}
          fieldname="classification"
          model="investor"
          showLabel
        />
        <EditField
          bind:value={newInvestor.homepage}
          fieldname="homepage"
          model="investor"
          showLabel
        />
        <EditField
          bind:value={newInvestor.opencorporates}
          fieldname="opencorporates"
          model="investor"
          showLabel
        />
        <EditField
          bind:value={newInvestor.comment}
          fieldname="comment"
          model="investor"
          showLabel
        />
      </div>
    {/if}
    <button class="btn btn-flat btn-primary" type="submit">{$_("Save")}</button>
    <button
      class="btn btn-flat btn-cancel mx-2"
      on:click={() => {
        showNewInvestorForm = false
        newInvestor = undefined
        value = null
      }}
      type="reset"
    >
      {$_("Cancel")}
    </button>
  </form>
</Modal>
