<script lang="ts">
  import type { Involvement } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let involvement: Involvement

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"
</script>

<div class="flex flex-col gap-1 border border-pelorous p-2">
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
    value={involvement.other_investor.name}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="country"
    {labelClass}
    model="investor"
    showLabel
    value={involvement.other_investor.country_id}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="classification"
    {labelClass}
    model="investor"
    showLabel
    value={involvement.other_investor.classification}
    {valueClass}
    {wrapperClass}
  />
  ---
  <DisplayField
    fieldname="involvement.relationship"
    {labelClass}
    showLabel
    value={involvement.relationship}
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
  <!--{#if involvement.loans_amount}-->
  <!--  <div class="flex flex-wrap justify-between gap-4">-->
  <!--    <div class=LABEL_CLASS>{$_("Loan")}</div>-->
  <!--    <div>{involvement.loans_amount} {involvement.loans_currency}</div>-->
  <!--  </div>-->
  <!--{/if}-->

  <DisplayField
    fieldname="involvement.percentage"
    {labelClass}
    showLabel
    value={involvement.percentage}
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
