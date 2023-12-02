<script lang="ts">
  import { gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

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
    const { error, data } = await $page.data.urqlClient
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
        {},
      )
      .toPromise()

    if (error || !data) {
      console.error(error)
      return
    }
    investors = data.investors
  }

  onMount(() => {
    getInvestors()
  })

  let newInvestor: Investor = {} as Investor
  let newInvestorForm: HTMLFormElement
  let showNewInvestorForm = false

  async function addNewInvestor() {
    if (!newInvestorForm.checkValidity()) {
      newInvestorForm.reportValidity()
      return
    }
    const { error, data } = await $page.data.urqlClient
      .mutation<{
        investor_edit: {
          investorId: number
          investorVersion: number
        }
      }>(
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

    if (error || !data) {
      console.error(error)
      return
    }

    const newI = { id: data.investor_edit.investorId, name: newInvestor.name }
    investors.push(newI)
    value = newI
    newInvestor = {} as Investor
    showNewInvestorForm = false
  }
</script>

<InvestorSelect
  bind:value
  {investors}
  creatable
  name={formfield.name}
  on:input={e => {
    const investorItem = e.detail
    if (investorItem && investorItem.created) {
      newInvestor = { name: investorItem.name }
      showNewInvestorForm = true
    }
  }}
/>
{#if !showNewInvestorForm && value}
  <div class="container p-2">
    <a href="/investor/{value.id}" rel="noreferrer" target="_blank">
      {$_("Show details for investor")}
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
