<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"

  import { fieldChoices, simpleInvestors } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"
  import { getCsrfToken } from "$lib/utils"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import CountryEditField from "$components/Fields/Edit2/CountryEditField.svelte"
  import TextEditField from "$components/Fields/Edit2/TextEditField.svelte"
  import EditField from "$components/Fields/EditField.svelte"
  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"
  import Modal from "$components/Modal.svelte"

  export let value: number | null

  export let extras: { required?: boolean; creatable?: boolean } = {}

  console.log({ extras })

  interface InvestorItem {
    id: number | null
    name: string
    created?: boolean
  }

  class NewInvestor {
    name: string = ""
    country_id: number | null = null
    classification: string = ""
    homepage: string = ""
    opencorporates: string = ""
    comment: string = ""
  }

  let newInvestor: NewInvestor | undefined = new NewInvestor()
  let showNewInvestorForm = false

  const onInvestorInput = (e: CustomEvent<InvestorItem | null>) => {
    const investorItem = e.detail
    console.log(e.type, investorItem)

    if (investorItem && investorItem.created) {
      newInvestor = new NewInvestor()
      newInvestor.name = investorItem.name

      showNewInvestorForm = true
      return
    }

    newInvestor = undefined
    showNewInvestorForm = false

    if (!investorItem) {
      value = null
      return
    }

    value = investorItem.id
  }

  const addNewInvestor = async (e: SubmitEvent) => {
    const form = e.target as HTMLFormElement
    console.log(form)

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
      const newI = { id: retJson.investorID, name: newInvestor!.name }
      $simpleInvestors.push(newI)
      value = newI.id
      newInvestor = undefined
      showNewInvestorForm = false
    }
  }

  const itemFilter = (label: string, filterText: string, option: InvestorItem) => {
    const filterTextLower = filterText.toLowerCase()
    return option.name.toLowerCase().includes(filterTextLower)
  }
</script>

<VirtualListSelect
  creatable={extras.creatable}
  disabled={showNewInvestorForm}
  {itemFilter}
  items={$simpleInvestors}
  label="name"
  on:input={onInvestorInput}
  placeholder={$_("Select investor")}
  required={extras.required}
  value={$simpleInvestors.find(i => i.id === value)}
>
  <svelte:fragment let:selection slot="selection">
    {#if selection.created}
      <div class="font-semibold italic">[new investor]</div>
    {:else}
      {selection.name} (#{selection.id})
    {/if}
  </svelte:fragment>
  <svelte:fragment let:item slot="item">
    {#if item.created}
      {$_("Create")}: {item.name}
    {:else}
      #{item.id}: {item.name}
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
          bind:value={newInvestor.country_id}
          extras={{ required: true }}
          fieldname="country_id"
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
    <button class="butn butn-flat butn-primary" type="submit">{$_("Save")}</button>
    <button
      class="butn butn-flat butn-cancel mx-2"
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
