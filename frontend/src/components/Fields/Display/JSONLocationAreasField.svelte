<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { AreaFeatureCollection, AreaType, FeatureProps } from "$lib/types/deal"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers.js"
  import type { FormField } from "$components/Fields/fields"

  export let value: AreaFeatureCollection
  // svelte-ignore unused-export-let
  export let model
  export let formfield: FormField

  let properties: FeatureProps[]
  $: properties = (value?.features ?? []).map(feat => feat.properties)

  const getAreaLabel = (areaType: AreaType) =>
    ({
      production_area: $_("Production areas"),
      contract_area: $_("Contract areas"),
      intended_area: $_("Intended areas"),
    }[areaType])
</script>

<div data-name={formfield?.name ?? ""}>
  {#each properties as prop}
    <div class:font-bold={prop.current}>
      <span>{dateCurrentFormat(prop)}</span>
      {#if prop.type}
        <span>{getAreaLabel(prop.type)}</span>
      {/if}
    </div>
  {/each}
</div>
