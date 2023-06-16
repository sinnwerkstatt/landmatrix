<script lang="ts">
  import { _ } from "svelte-i18n"

  import { formfields } from "$lib/stores"

  import DecimalField from "$components/Fields/Edit/DecimalField.svelte"
  import TextField from "$components/Fields/Edit/TextField.svelte"
  import type { FormField } from "$components/Fields/fields"

  import BooleanField from "./Edit/BooleanField.svelte"
  import CharField from "./Edit/CharField.svelte"
  import CountryForeignKey from "./Edit/CountryForeignKey.svelte"
  import CurrencyForeignKey from "./Edit/CurrencyForeignKey.svelte"
  import DateField from "./Edit/DateField.svelte"
  import EmailField from "./Edit/EmailField.svelte"
  import FileField from "./Edit/FileField.svelte"
  import InvestorForeignKey from "./Edit/InvestorForeignKey.svelte"
  import JSONActorsField from "./Edit/JSONActorsField.svelte"
  import JSONDateAreaChoicesField from "./Edit/JSONDateAreaChoicesField.svelte"
  import JSONDateAreaField from "./Edit/JSONDateAreaField.svelte"
  import JSONDateChoiceField from "./Edit/JSONDateChoiceField.svelte"
  import JSONExportsField from "./Edit/JSONExportsField.svelte"
  import JSONJobsField from "./Edit/JSONJobsField.svelte"
  import JSONLeaseField from "./Edit/JSONLeaseField.svelte"
  import SimpleArrayField from "./Edit/SimpleArrayField.svelte"
  import TypedChoiceField from "./Edit/TypedChoiceField.svelte"
  import URLField from "./Edit/URLField.svelte"

  export let fieldname: string
  export let value
  export let model = "deal"

  export let showLabel = true
  export let wrapperClasses = "mb-3 leading-5 flex flex-col"
  export let labelClasses = "font-semibold mb-4 w-full"
  export let valueClasses = "text-lm-dark dark:text-white px-3 mb-10 w-full"
  export let disabled = false

  let formfield: FormField
  $: formfield = { name: fieldname, ...$formfields[model][fieldname] }

  $: field = {
    CountryForeignKey: CountryForeignKey,
    CurrencyForeignKey: CurrencyForeignKey,
    DateField: DateField,
    DecimalField: DecimalField,
    EmailField: EmailField,
    FloatField: DecimalField,
    IntegerField: DecimalField,
    InvestorForeignKey: InvestorForeignKey,
    JSONActorsField: JSONActorsField,
    JSONDateAreaChoicesField: JSONDateAreaChoicesField,
    JSONDateAreaField: JSONDateAreaField,
    JSONDateChoiceField: JSONDateChoiceField,
    JSONExportsField: JSONExportsField,
    JSONJobsField: JSONJobsField,
    JSONLeaseField: JSONLeaseField,
    SimpleArrayField: SimpleArrayField,
    TypedChoiceField: TypedChoiceField,
    URLField: URLField,
  }[formfield.class]
</script>

<div
  data-class={formfield?.class ?? ""}
  data-name={formfield?.name ?? ""}
  class={wrapperClasses}
>
  {#if showLabel}
    <div class={labelClasses}>
      {$_(formfield.label)}
    </div>
  {/if}
  <div class={valueClasses}>
    {#if formfield.class === "FileField"}
      <FileField bind:value {model} {formfield} on:change />
    {:else if formfield.class === "TextField"}
      <TextField bind:value {formfield} on:change />
    {:else if ["CharField", "OCIDField"].includes(formfield.class)}
      <CharField bind:value {formfield} on:change />
    {:else if ["BooleanField", "NullBooleanField"].includes(formfield.class)}
      <BooleanField bind:value {formfield} on:change />
    {:else if field}
      <svelte:component
        this={field}
        bind:value
        {model}
        {disabled}
        {formfield}
        on:change
      />
    {:else}
      <span class="italic text-red-600">Unknown field: {formfield.class}</span>
    {/if}
  </div>
</div>
