<script lang="ts">
  import type { Involvement, Model, Mutable } from "$lib/types/data"

  import CurrencySelect from "$components/Fields/Edit2/CurrencySelect.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    entry: Mutable<Involvement>
    model?: Model
    extras?: { excludeIds?: number[] }
  }

  let { entry = $bindable(), model = "investor", extras = {} }: Props = $props()
</script>

<div class="grid lg:grid-cols-2 lg:gap-4">
  <EditField
    fieldname="involvement.parent_investor_id"
    bind:value={entry.parent_investor_id}
    {model}
    {extras}
    showLabel
  />
  <EditField
    fieldname="involvement.parent_relation"
    bind:value={entry.parent_relation}
    {model}
    showLabel
  />
</div>

<div class="grid grid-cols-3 gap-4">
  <div class="col-span-2">
    <EditField
      fieldname="involvement.investment_type"
      bind:value={entry.investment_type}
      {model}
      showLabel
    />
  </div>
  <EditField
    fieldname="involvement.percentage"
    bind:value={entry.percentage}
    {model}
    showLabel
  />
</div>

<div class="grid grid-cols-3 gap-4">
  <EditField
    fieldname="involvement.loans_amount"
    bind:value={entry.loans_amount}
    {model}
    showLabel
  />

  <div class="flex items-center">
    <CurrencySelect bind:value={entry.loans_currency_id} />
  </div>

  <EditField
    fieldname="involvement.loans_date"
    bind:value={entry.loans_date}
    {model}
    showLabel
  />
</div>

<EditField
  fieldname="involvement.comment"
  bind:value={entry.comment}
  {model}
  showLabel
/>
