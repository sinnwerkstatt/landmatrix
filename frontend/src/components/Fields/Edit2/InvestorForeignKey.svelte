<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"

  import { fieldChoices, simpleInvestors } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"
  import { getCsrfToken } from "$lib/utils"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import CountryEditField from "$components/Fields/Edit2/CountryEditField.svelte"
  import TextEditField from "$components/Fields/Edit2/TextEditField.svelte"
  import InvestorSelect from "$components/LowLevel/InvestorSelect.svelte"

  type Investor = {
    id?: number
    name: string
    created?: boolean
  }
  export let value: Investor | null
  export let fieldname: string = "operating_company"
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  class NewInvestor {
    name: string = ""
    country: Country | null = null
    classification: string = ""
    homepage: string = ""
    opencorporates: string = ""
    comment: string = ""
  }
  let newInvestor: NewInvestor = new NewInvestor()
  let newInvestorForm: HTMLFormElement
  let showNewInvestorForm = false

  const onInvestorInput = (e: CustomEvent) => {
    const investorItem: Investor = e.detail

    if (investorItem && investorItem.created) {
      newInvestor.name = investorItem.name
      showNewInvestorForm = true
    } else {
      newInvestor = new NewInvestor()
      showNewInvestorForm = false
    }
  }

  const addNewInvestor = async () => {
    if (!newInvestorForm.checkValidity()) {
      newInvestorForm.reportValidity()
      return
    }
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
    // console.log(retJson)
    if (ret.ok) {
      const newI = { id: retJson.investorID, name: newInvestor.name }
      $simpleInvestors.push(newI)
      value = newI
      newInvestor = new NewInvestor()
      showNewInvestorForm = false
    }
  }

  //   }
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <InvestorSelect
      bind:value
      investors={$simpleInvestors}
      creatable
      name="operating_company"
      on:input={onInvestorInput}
      disabled={showNewInvestorForm}
    />

    {#if !showNewInvestorForm && value}
      <div class="container p-2">
        <a href="/investor/{value.id}" rel="noreferrer" target="_blank">
          {$_("Show details for investor")}
        </a>
      </div>
    {/if}
    {#if showNewInvestorForm}
      <form
        bind:this={newInvestorForm}
        class="my-6"
        on:submit|preventDefault={addNewInvestor}
      >
        <div class="container">
          <TextEditField
            bind:value={newInvestor.name}
            fieldname="investor.name"
            label={$_("Name")}
          />
          <CountryEditField
            bind:value={newInvestor.country}
            fieldname="investor.country"
            label={$_("Country of registration/origin")}
            required
          />
          <ChoicesEditField
            bind:value={newInvestor.classification}
            choices={$fieldChoices.investor.classification}
            fieldname="investor.classification"
            label={$_("Classification")}
          />

          <TextEditField
            bind:value={newInvestor.homepage}
            fieldname="investor.homepage"
            label={$_("Investor homepage")}
            isURL
          />
          <TextEditField
            bind:value={newInvestor.opencorporates}
            fieldname="investor.opencorporates"
            label={$_("Opencorporates link")}
            isURL
          />
          <TextEditField
            bind:value={newInvestor.comment}
            fieldname="investor.comment"
            label={$_("Comment")}
            multiline
          />
        </div>
        <button type="submit" class="butn butn-flat butn-primary">{$_("Save")}</button>
        <button
          type="reset"
          class="butn butn-flat butn-cancel mx-2"
          on:click={() => {
            showNewInvestorForm = false
            newInvestor = new NewInvestor()
            value = null
          }}
        >
          {$_("Cancel")}
        </button>
      </form>
    {/if}
  </div>
</div>
