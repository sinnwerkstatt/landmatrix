<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { type Involvement } from "$lib/types/data"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import CurrencySelect from "$components/Fields/Edit2/CurrencySelect.svelte"
  import EditField from "$components/Fields/EditField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let involvements: Involvement[]
  export let tertiary = false
  export let investorID: number

  $: model = tertiary ? $_("Tertiary investor/lender") : $_("Parent company")

  let activeEntryIdx: number

  enum Role {
    PARENT = "PARENT",
    LENDER = "LENDER",
  }
  const createEmptyEntry = (id: string): Involvement => ({
    id: id,
    parent_investor_id: null,
    child_investor_id: investorID,
    role: tertiary ? Role.LENDER : Role.PARENT,
    loans_currency_id: null,
    investment_type: [],
    percentage: null,
    loans_amount: null,
    loans_date: null,
    parent_relation: null,
    comment: "",
  })

  let involvementsCopy = structuredClone<Involvement[]>(
    involvements.length ? involvements : [createEmptyEntry(newNanoid())],
  )
  $: involvements = involvementsCopy.filter(val => !!val.parent_investor_id)

  $: filteredInvolvements = involvementsCopy.filter(
    i =>
      i.child_investor_id === investorID &&
      i.role === (tertiary ? Role.LENDER : Role.PARENT),
  )

  const addEntry = () => {
    const currentIDs = involvementsCopy.map(entry => entry.id.toString())
    involvementsCopy = [...involvementsCopy, createEmptyEntry(newNanoid(currentIDs))]
    activeEntryIdx = filteredInvolvements.length
  }

  const removeEntry = (c: Involvement) => {
    if (!isEmptySubmodel(c, ["id", "child_investor_id", "role"])) {
      const areYouSure = confirm(`${$_("Remove")} ${model} #${c.id}?`)
      if (!areYouSure) return
    }
    involvementsCopy = involvementsCopy.filter(x => x.id !== c.id)
    activeEntryIdx = filteredInvolvements.length - 1
  }

  const toggleActiveEntry = (index: number) =>
    (activeEntryIdx = activeEntryIdx === index ? -1 : index)

  onMount(() => {
    activeEntryIdx = filteredInvolvements.length - 1
  })
</script>

<section class="my-6 flex flex-wrap">
  <form class="w-full" id={tertiary ? "tertiary_investors" : "parent_companies"}>
    {#each filteredInvolvements as involvement, index}
      <div>
        <div
          class="my-2 flex flex-row items-center justify-between bg-gray-200 dark:bg-gray-700"
        >
          <div
            role="button"
            class="flex-grow p-2"
            on:click={() => toggleActiveEntry(index)}
            on:keydown={e => e.code === "Enter" && toggleActiveEntry(index)}
            tabindex="0"
          >
            <h3 class="m-0">
              {index + 1}. {model}
              <small class="text-sm text-gray-500">
                {#if involvement.parent_investor_id}
                  #{involvement.parent_investor_id}
                {/if}
              </small>
            </h3>
          </div>
          <button
            class="flex-initial p-2"
            on:click|stopPropagation={() => removeEntry(involvement)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if activeEntryIdx === index}
          <div transition:slide={{ duration: 200 }}>
            <div class="grid lg:grid-cols-2 lg:gap-4">
              <EditField
                fieldname="involvement.parent_investor_id"
                bind:value={involvement.parent_investor_id}
                showLabel
              />
              <EditField
                fieldname="involvement.parent_relation"
                bind:value={involvement.parent_relation}
                showLabel
              />
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div class="col-span-2">
                <EditField
                  fieldname="involvement.investment_type"
                  bind:value={involvement.investment_type}
                  showLabel
                />
              </div>
              <EditField
                fieldname="involvement.percentage"
                bind:value={involvement.percentage}
                showLabel
              />
            </div>

            <div class="grid grid-cols-3 gap-4">
              <EditField
                fieldname="involvement.loans_amount"
                bind:value={involvement.loans_amount}
                showLabel
              />
              <div class="flex items-center">
                <CurrencySelect bind:value={involvement.loans_currency_id} />
              </div>

              <EditField
                fieldname="involvement.loans_date"
                bind:value={involvement.loans_date}
                showLabel
              />
            </div>

            <EditField
              fieldname="involvement.comment"
              bind:value={involvement.comment}
              showLabel
            />
          </div>
        {/if}
      </div>
    {/each}
    <div class="mt-6">
      <button
        class="btn btn-secondary flex items-center"
        on:click={addEntry}
        type="button"
      >
        <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
        {$_("Add")}
        {model}
      </button>
    </div>
  </form>
</section>
