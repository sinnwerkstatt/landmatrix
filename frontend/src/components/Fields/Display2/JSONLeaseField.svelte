<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONLeaseFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"
  import HouseholdIcon from "$components/icons/HouseholdIcon.svelte"
  import TractorIcon from "$components/icons/TractorIcon.svelte"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    value: JSONLeaseFieldType[]
    fieldname?: string
  }

  let { value, fieldname = "" }: Props = $props()
</script>

<ul>
  {#each value ?? [] as val, i}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.area}
        <span class="mx-2">
          <CircleNotchIcon />
          {val.area.toLocaleString("fr").replace(",", ".")}
          {$_("ha")}
        </span>
      {/if}
      {#if val.farmers}
        <span class="mx-2">
          <TractorIcon />
          {val.farmers.toLocaleString("fr").replace(",", ".")}
        </span>
      {/if}
      {#if val.households}
        <span class="mx-2">
          <HouseholdIcon />
          {val.households.toLocaleString("fr").replace(",", ".")}
        </span>
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
