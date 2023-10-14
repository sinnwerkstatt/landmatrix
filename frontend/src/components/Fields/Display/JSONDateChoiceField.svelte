<script lang="ts">
  import { _ } from "svelte-i18n"

  import { ImplementationStatus, NegotiationStatus } from "$lib/types/deal"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers.ts"
  import type { FormField } from "$components/Fields/fields"

  type JSONDateChoiceFieldType = {
    current?: boolean
    date: string
    choice: NegotiationStatus | ImplementationStatus
  }

  export let formfield: FormField
  export let value: JSONDateChoiceFieldType[] = []

  $: flat_choices = formfield.choices
    ? Object.fromEntries(formfield.choices.map(c => [c.value, c.label]))
    : {}
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.choice}
        <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
        {$_(flat_choices[val.choice])}
      {/if}
    </li>
  {/each}
</ul>
