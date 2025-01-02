<script lang="ts">
  import type { ValueLabelEntry } from "$lib/fieldChoices"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"

  interface Extras {
    choices?: ValueLabelEntry[]
  }

  interface Props {
    value?: JSONCurrentDateChoiceFieldType[]
    extras?: Extras
  }

  let { value = [], extras = {} }: Props = $props()
  let choices = $derived(extras.choices ?? [])
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {choices.find(c => c.value === val.choice)?.label ?? val.choice ?? ""}
    </li>
  {/each}
</ul>
