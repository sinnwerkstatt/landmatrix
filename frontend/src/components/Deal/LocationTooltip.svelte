<script lang="ts">
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores"
  import type { AreaFeature, PointFeature } from "$lib/types/deal"
  import { isPoint, isPolygon } from "$lib/utils/geojsonHelpers"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"
  import NanoIDField from "$components/Fields/Display2/NanoIDField.svelte"

  export let feature: PointFeature | AreaFeature
</script>

<div>
  <NanoIDField value={feature.properties.id.toString()} />

  <div>{$_("Name")}: {feature.properties.name}</div>

  {#if isPoint(feature)}
    <div>{$_("Point")}: {feature.geometry.coordinates}</div>
  {:else if isPolygon(feature)}
    <div>{$_("Type")}: {$areaTypeMap[feature.properties.type]}</div>
    <div>{$_("Size")}: {formatArea(feature.properties.area)} {$_("ha")}</div>
  {/if}
</div>
