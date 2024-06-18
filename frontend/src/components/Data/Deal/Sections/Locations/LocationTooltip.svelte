<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createLabels, fieldChoices } from "$lib/stores"
  import type { AreaFeature, AreaType, PointFeature } from "$lib/types/data"
  import { isPoint, isPolygon } from "$lib/utils/geojsonHelpers"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let feature: PointFeature | AreaFeature

  $: areaTypeLabels = createLabels<AreaType>($fieldChoices.area.type)
</script>

{#if isPoint(feature)}
  <DisplayField value={feature.properties.id} fieldname="location.nid" />
  <div>{$_("Name")}: {feature.properties.name}</div>
  <div>{$_("Point")}: {feature.geometry.coordinates}</div>
{:else if isPolygon(feature)}
  <div>
    {$_("Type")}: {areaTypeLabels[feature.properties.type]}
  </div>
  <div>{$_("Size")}: {formatArea(feature.properties.area)} {$_("ha")}</div>
{/if}
