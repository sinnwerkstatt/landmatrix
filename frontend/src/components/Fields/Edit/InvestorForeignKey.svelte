<script lang="ts">
  import { gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { page } from "$app/stores"

  import EditField from "$components/Fields/EditField.svelte"
  import type { FormField } from "$components/Fields/fields"
  import InvestorSelect from "$components/LowLevel/InvestorSelect.svelte"

  export let value: Investor
  export let formfield: FormField

  type Investor = {
    id?: number
    name: string
  }

  let investors: Investor[] = []

  async function getInvestors() {
    const { data } = await $page.data.urqlClient
      .query<{
        investors: Investor[]
      }>(
        gql`
          query {
            investors(
              sort: "name"
              limit: 0
              subset: UNFILTERED
              filters: [{ field: "status", value: 4, exclusion: true }]
            ) {
              id
              name
            }
          }
        `,
      )
      .toPromise()
    investors = [...data.investors]
  }

  onMount(() => {
    getInvestors()
  })

  let newInvestor: Investor = {} as Investor
  let newInvestorForm: HTMLFormElement
  let showNewInvestorForm = false

  function initCreateNewInvestor(name: string) {
    newInvestor = { name }
    showNewInvestorForm = true
  }

  async function addNewInvestor() {
    if (!newInvestorForm.checkValidity()) {
      newInvestorForm.reportValidity()
      return
    }
    const res = await $page.data.urqlClient
      .mutation(
        gql`
          mutation ($payload: Payload) {
            investor_edit(id: -1, payload: $payload) {
              investorId
              investorVersion
            }
          }
        `,
        { payload: newInvestor },
      )
      .toPromise()

    if (res.error) {
      console.error(res.error)
    } else {
      const { data } = res
      let newI = { id: data.investor_edit.investorId, name: newInvestor.name }
      investors.push(newI)
      value = newI
      newInvestor = {} as Investor
      showNewInvestorForm = false
    }
  }
</script>

<div class="investor_foreignkey_field">
  <InvestorSelect
    bind:value
    {investors}
    creatable
    name={formfield.name}
    on:input={e => {
      const value = e.detail
      if (value && value.created) {
        initCreateNewInvestor(value.name)
      }
    }}
  />
  {#if !showNewInvestorForm && value}
    <div class="container p-2">
      <a href="/investor/{value.id}" class="investor-link">
        {$_("Show details for investor")} #{value.id}
        {value.name}
      </a>
    </div>
  {/if}
  {#if showNewInvestorForm}
    <form bind:this={newInvestorForm} on:submit|preventDefault={addNewInvestor}>
      <div class="container">
        {#each ["name", "country", "classification", "homepage", "opencorporates", "comment"] as fieldname}
          <EditField
            {fieldname}
            bind:value={newInvestor[fieldname]}
            model="investor"
            wrapperClasses="flex justify-center items-center my-2"
            labelClasses="font-bold w-5/12"
            valueClasses="w-7/12 mb-1"
          />
        {/each}
      </div>
      <button type="submit" class="btn btn-primary">{$_("Save")}</button>
      <button
        type="reset"
        class="btn btn-gray mx-2"
        on:click={() => {
          showNewInvestorForm = false
          value = undefined
        }}
      >
        {$_("Cancel")}
      </button>
    </form>
  {/if}
</div>
