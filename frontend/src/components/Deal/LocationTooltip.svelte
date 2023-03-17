<script lang="ts">
  import type { Feature, Point, Polygon } from "geojson"
  import type { Feature as TurfFeature } from "@turf/turf"
  import { area } from "@turf/turf"
  import { _ } from "svelte-i18n"

  import type { AreaType } from "$lib/types/deal"

  import NanoIDField from "$components/Fields/Display/NanoIDField.svelte"

  export let feature: Feature

  const formatArea = (area: number) =>
    (area / 10000)
      .toFixed(2)
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, " ")

  const isPoint = (feature: Feature): feature is Feature<Point> =>
    feature.geometry.type === "Point"

  const isPolygon = (feature: Feature): feature is Feature<Polygon> =>
    feature.geometry.type === "Polygon"

  // TODO: Move to svelte store?
  let areaTypeMap: { [key in AreaType]: string }
  $: areaTypeMap = {
    intended_area: $_("Intended area"),
    production_area: $_("Production area"),
    contract_area: $_("Contract area"),
  }

  $: areaType = areaTypeMap[feature.properties.type]

  $: areaSize = formatArea(area(feature as TurfFeature))
</script>

<div>
  <NanoIDField value={feature.properties.id} />

  <div>{$_("Name")}: {feature.properties.name}</div>

  {#if isPoint(feature)}
    <div>{$_("Point")}: {feature.geometry.coordinates}</div>
  {:else if isPolygon(feature)}
    <div>{$_("Type")}: {areaType}</div>
    <div>{$_("Size")}: {areaSize} {$_("ha")}</div>
  {/if}
</div>
