<script lang="ts">
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores/maps"
  import type { AreaFeature, PointFeature } from "$lib/types/newtypes"
  import { isPoint, isPolygon } from "$lib/utils/geojsonHelpers"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let feature: PointFeature | AreaFeature
</script>

{#if isPoint(feature)}
  <DisplayField value={feature.properties.id} fieldname="location.nid" />
  <div>{$_("Name")}: {feature.properties.name}</div>
  <div>{$_("Point")}: {feature.geometry.coordinates}</div>
{:else if isPolygon(feature)}
  <div>{$_("Type")}: {$areaTypeMap[feature.properties.type]}</div>
  <div>{$_("Size")}: {formatArea(feature.properties.area)} {$_("ha")}</div>
{/if}
