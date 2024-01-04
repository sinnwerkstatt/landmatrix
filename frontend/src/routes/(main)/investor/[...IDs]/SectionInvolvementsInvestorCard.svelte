<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { Involvement } from "$lib/types/newtypes"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import IDField from "$components/Fields/Display2/IDField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let involvement: Involvement

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"
</script>

<div class="flex flex-col gap-1 border border-pelorous p-2">
  <IDField
    label={$_("ID")}
    value={involvement.other_investor.id}
    fieldname="investor.id"
    {wrapperClass}
    {labelClass}
    {valueClass}
    model="investor"
  />
  <TextField
    label={$_("Name")}
    value={involvement.other_investor.name}
    fieldname="investor.name"
    {wrapperClass}
    {labelClass}
    {valueClass}
  />
  <CountryField
    label={$_("Country of registration")}
    value={involvement.other_investor.country}
    fieldname="country"
    {wrapperClass}
    {labelClass}
    {valueClass}
  />
  <TextField
    label={$_("Classification")}
    value={involvement.other_investor.classification}
    fieldname="investor.classification"
    choices={$fieldChoices.investor.classification}
    {wrapperClass}
    {labelClass}
    {valueClass}
  />
  ---
  <TextField
    label={$_("Relationship")}
    value={involvement.relationship}
    fieldname="investor.relationship"
    {wrapperClass}
    {labelClass}
    {valueClass}
  />
  <TextField
    label={$_("Investment type")}
    value={involvement.investment_type}
    fieldname="investor.investment_type"
    choices={$fieldChoices.involvement.investment_type}
    {wrapperClass}
    {labelClass}
    {valueClass}
  />
  <!--{#if involvement.loans_amount}-->
  <!--  <div class="flex flex-wrap justify-between gap-4">-->
  <!--    <div class=LABEL_CLASS>{$_("Loan")}</div>-->
  <!--    <div>{involvement.loans_amount} {involvement.loans_currency}</div>-->
  <!--  </div>-->
  <!--{/if}-->

  <DecimalField
    label={$_("Ownership share")}
    value={involvement.percentage}
    fieldname="involvement.percentage"
    {wrapperClass}
    {labelClass}
    {valueClass}
    unit="%"
  />
  <TextField
    label={$_("Comment")}
    value={involvement.comment}
    fieldname="investor.comment"
    {wrapperClass}
    {labelClass}
    {valueClass}
  />
</div>
