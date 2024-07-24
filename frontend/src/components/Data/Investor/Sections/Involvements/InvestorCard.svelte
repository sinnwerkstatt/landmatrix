<script lang="ts">
  import type { Involvement } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let involvement: Involvement

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"

  const is_deleted = (inv: Involvement) => inv.other_investor.deleted
  const is_draft_only = (inv: Involvement) => inv.other_investor.draft_only
</script>

<div
  class="relative flex flex-col gap-1 border border-pelorous p-2"
  class:bg-red-200={is_deleted(involvement)}
  class:bg-yellow-100={is_draft_only(involvement)}
  class:text-black={is_deleted(involvement) || is_draft_only(involvement)}
>
  {#if involvement.other_investor}
    {#if is_deleted(involvement)}
      <div
        class="absolute bottom-2 left-0 right-0 flex items-center justify-center text-3xl italic opacity-30"
      >
        DELETED
      </div>
    {:else if is_draft_only(involvement)}
      <div
        class="absolute bottom-2 left-0 right-0 flex items-center justify-center text-3xl italic opacity-30"
      >
        DRAFT
      </div>
    {/if}
    <DisplayField
      fieldname="id"
      {labelClass}
      model="investor"
      showLabel
      value={involvement.other_investor.id}
      {valueClass}
      {wrapperClass}
    />
    <DisplayField
      fieldname="name"
      {labelClass}
      model="investor"
      showLabel
      value={involvement.other_investor.selected_version.name}
      {valueClass}
      {wrapperClass}
      extras={{
        investorNameUnknown: involvement.other_investor.selected_version.name_unknown,
      }}
    />
    <DisplayField
      fieldname="country_id"
      {labelClass}
      model="investor"
      showLabel
      value={involvement.other_investor.selected_version.country_id}
      {valueClass}
      {wrapperClass}
    />
    <DisplayField
      fieldname="classification"
      {labelClass}
      model="investor"
      showLabel
      value={involvement.other_investor.selected_version.classification}
      {valueClass}
      {wrapperClass}
    />
  {:else}
    couldn't find the investor. # TODO
    <!--     TODO Kurt  http://localhost:9000/investor/45014 -->
  {/if}
  <hr class="my-2 w-1/2" />

  <DisplayField
    fieldname="involvement.relationship"
    {labelClass}
    showLabel
    value={involvement.relationship}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="involvement.parent_relation"
    {labelClass}
    showLabel
    value={involvement.parent_relation}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="involvement.investment_type"
    {labelClass}
    showLabel
    value={involvement.investment_type}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="involvement.percentage"
    {labelClass}
    showLabel
    value={involvement.percentage}
    {valueClass}
    {wrapperClass}
  />

  <DisplayField
    fieldname="involvement.loans_amount"
    {labelClass}
    showLabel
    value={involvement.loans_amount}
    {valueClass}
    {wrapperClass}
    extras={{ currency: involvement.loans_currency_id }}
  />

  <DisplayField
    fieldname="involvement.loans_date"
    {labelClass}
    showLabel
    value={involvement.loans_date}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="involvement.comment"
    {labelClass}
    showLabel
    value={involvement.comment}
    {valueClass}
    {wrapperClass}
  />
</div>
