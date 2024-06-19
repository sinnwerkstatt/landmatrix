<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createLabels, fieldChoices } from "$lib/stores"
  import type { AreaFeature, AreaType, PointFeature } from "$lib/types/data"
  import { isPoint, isPolygon } from "$lib/utils/geojsonHelpers"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"

  export let feature: PointFeature | AreaFeature

  $: areaTypeLabels = createLabels<AreaType>($fieldChoices.area.type)
</script>

{#if isPoint(feature)}
  <div class="mb-2">
    <a class="font-mono text-lg" href="#{feature.properties.id}">
      #{feature.properties.id}
    </a>
  </div>
  <div>
    <b>{$_("Name")}</b>
    : {feature.properties.name}
  </div>
  <div>
    <b>{$_("Point")}</b>
    : {feature.geometry.coordinates}
  </div>
{:else if isPolygon(feature)}
  <div>
    <b>{$_("Type")}</b>
    : {areaTypeLabels[feature.properties.type]}
  </div>
  <div>
    <b>{$_("Size")}</b>
    : {formatArea(feature.properties.area)}
    {$_("ha")}
  </div>
{/if}
