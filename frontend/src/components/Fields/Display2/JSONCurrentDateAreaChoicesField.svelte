<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/fieldChoices"
  import type { JSONCurrentDateAreaChoicesFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Extras {
    choices: ValueLabelEntry[]
  }

  interface Props {
    value?: JSONCurrentDateAreaChoicesFieldType[]
    fieldname?: string
    extras?: Extras
  }

  let { value = [], extras = { choices: [] }, fieldname = "" }: Props = $props()

  const getLabel = (value: string) =>
    extras.choices.find(c => value === c.value)?.label ?? value
</script>

<ul>
  {#each value ?? [] as val, i}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>

      {#if val.choices && extras.choices.length}
        <span>
          {val.choices.map(getLabel).join(", ")}
        </span>
      {/if}
      {#if val.area}
        ({val.area.toLocaleString("fr").replace(",", ".")}
        {$_("ha")})
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
