<script lang="ts">
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: JSONCurrentDateChoiceFieldType = []

  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-gray-700 dark:text-white md:w-7/12 lg:w-8/12"

  export let choices: { value: string; label: string }[]

  // $: flat_choices = formfield.choices
  //   ? Object.fromEntries(formfield.choices.map(c => [c.value, c.label]))
  //   : {}
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <ul>
        {#each value ?? [] as val}
          <li class:font-bold={val.current}>
            <span>{dateCurrentFormat(val)}</span>
            {choices.find(c => c.value === val.choice)?.label ?? ""}
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}
