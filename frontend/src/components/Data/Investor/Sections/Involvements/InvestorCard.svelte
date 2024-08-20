<script lang="ts">
  import { _ } from "svelte-i18n"

  import { simpleInvestors } from "$lib/stores"
  import {
    InvolvementRole,
    type Involvement,
    type SimpleInvestor,
  } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let involvement: Involvement
  export let isParent: boolean = false

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"

  let otherInvestor: SimpleInvestor
  $: otherInvestor =
    $simpleInvestors.find(
      simpleInvestor =>
        simpleInvestor.id ===
        (isParent ? involvement.parent_investor_id : involvement.child_investor_id),
    ) || ({} as SimpleInvestor)

  let relationshipMap: { [key in InvolvementRole]: { parent: string; child: string } }
  $: relationshipMap = {
    [InvolvementRole.PARENT]: {
      parent: $_("Parent company"),
      child: $_("Subsidiary company"),
    },
    [InvolvementRole.LENDER]: {
      parent: $_("Tertiary investor/lender"),
      child: $_("Beneficiary company"),
    },
  }

  $: relationship = relationshipMap[involvement.role][isParent ? "parent" : "child"]
</script>

<div
  class="relative flex flex-col gap-1 border border-pelorous p-2"
  class:bg-red-200={otherInvestor.deleted}
  class:bg-yellow-100={"active" in otherInvestor && !otherInvestor.active}
  class:text-black={otherInvestor.deleted || !otherInvestor.active}
>
  {#if otherInvestor}
    {#if otherInvestor.deleted}
      <div
        class="absolute bottom-2 left-0 right-0 flex items-center justify-center text-3xl italic opacity-30"
      >
        {$_("Deleted")}
      </div>
    {:else if !otherInvestor.active}
      <div
        class="absolute bottom-2 left-0 right-0 flex items-center justify-center text-3xl italic opacity-30"
      >
        {$_("Draft")}
      </div>
    {/if}
    <DisplayField
      fieldname="id"
      {labelClass}
      model="investor"
      showLabel
      value={otherInvestor.id}
      {valueClass}
      {wrapperClass}
    />
    <DisplayField
      fieldname="name"
      {labelClass}
      model="investor"
      showLabel
      value={otherInvestor.name}
      {valueClass}
      {wrapperClass}
      extras={{
        investorNameUnknown: otherInvestor.name_unknown,
      }}
    />
    <DisplayField
      fieldname="country_id"
      {labelClass}
      model="investor"
      showLabel
      value={otherInvestor.country_id}
      {valueClass}
      {wrapperClass}
    />
    <DisplayField
      fieldname="classification"
      {labelClass}
      model="investor"
      showLabel
      value={otherInvestor.classification}
      {valueClass}
      {wrapperClass}
    />
  {/if}

  <hr class="my-2 w-1/2" />

  <DisplayField
    fieldname="involvement.relationship"
    {labelClass}
    showLabel
    value={relationship}
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
