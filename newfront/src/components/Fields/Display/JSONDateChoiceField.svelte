<script lang="ts">
  import { ImplementationStatus, NegotiationStatus } from "$lib/types/deal"

  import {
    dateCurrentFormat,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts"
  import type { FormField } from "$components/Fields/fields"

  type JSONDateChoiceFieldType = {
    current?: boolean
    date: string
    choice: NegotiationStatus | ImplementationStatus
  }

  export let formfield: FormField
  export let value: JSONDateChoiceFieldType[] = []
</script>

<div class="jsondatechoice_field whitespace-nowrap">
  {#each value ?? [] as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.choice}
        {mapChoices(val.choice, formfield.choices)}
      {/if}
    </div>
  {/each}
</div>
