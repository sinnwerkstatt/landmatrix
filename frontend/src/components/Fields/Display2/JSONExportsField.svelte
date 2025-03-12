<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/fieldChoices"
  import type { JSONExportsFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"
  import PlaneIcon from "$components/icons/PlaneIcon.svelte"
  import WeightIcon from "$components/icons/WeightIcon.svelte"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    value?: JSONExportsFieldType[]
    extras?: { choices: ValueLabelEntry[] }
    fieldname?: string
  }

  let { value = [], extras = { choices: [] }, fieldname = "" }: Props = $props()

  const getLabel = (value: string) =>
    extras.choices.find(c => value === c.value)?.label ?? value
</script>

<ul>
  {#each value ?? [] as val, i}
    <li class:font-bold={val.current}>
      {#if val.choices && extras.choices.length}
        <span>
          {val.choices.map(getLabel).join(", ")}
        </span>
      {/if}
      <span>{dateCurrentFormat(val)}</span>
      {#if val.area}
        <span>
          <CircleNotchIcon />
          {val.area.toLocaleString("fr").replace(",", ".")}
          {$_("ha")}
        </span>
      {/if}
      {#if val.yield}
        <span class="mx-2">
          <WeightIcon />
          {val.yield.toLocaleString("fr").replace(",", ".")}
          {$_("tons")}
        </span>
      {/if}
      {#if val.export}
        <span class="mx-2">
          <PlaneIcon />
          {val.export.toLocaleString("fr").replace(",", ".")} %
        </span>
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
