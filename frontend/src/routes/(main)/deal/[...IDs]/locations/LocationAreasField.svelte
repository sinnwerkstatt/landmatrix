<script lang="ts">
  import { area } from "@turf/turf"
  import { geoJson, type Map } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores/maps"
  import type { AreaType } from "$lib/types/deal"
  import type { Area, AreaFeature, AreaFeatureLayer } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import {
    dateCurrentFormat,
    formatArea,
  } from "$components/Fields/Display2/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"

  export const AREA_TYPE_COLOR_MAP: { [key in AreaType]: string } = {
    contract_area: "#ff00ff",
    intended_area: "#66ff33",
    production_area: "#ff0000",
  }

  export let map: Map | undefined
  export let areas: Area[]
  export let fieldname: string
  export let label = ""

  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let isSelectedEntry: boolean

  // TODO Marcus refactor since pure
  const areaToFeature = (area: Area): AreaFeature => ({
    type: "Feature",
    geometry: area.area,
    properties: {
      id: area.id as number,
      type: area.type,
      date: area.date,
      current: area.current,
      visible: area.current,
    },
  })

  // TODO Marcus refactor since pure
  const createLayer = (
    features: AreaFeature[],
    isSelectedEntry: boolean,
  ): AreaFeatureLayer =>
    geoJson(features, {
      filter: feature => feature.properties.visible,
      style: feature => ({
        weight: 1.5,
        color: "black",
        dashArray: "5, 5",
        dashOffset: "0",
        fillColor: isSelectedEntry
          ? feature
            ? AREA_TYPE_COLOR_MAP[feature.properties.type]
            : ""
          : "grey",
        fillOpacity: 0.4,
      }),
    })

  let features: AreaFeature[] = areas.map(areaToFeature)
  let layer: AreaFeatureLayer

  $: if (map && layer) {
    map.removeLayer(layer)
    layer = createLayer(features, isSelectedEntry)
    map.addLayer(layer)
    // fitBounds(layer, map)
  }

  onMount(() => {
    layer = createLayer(features, isSelectedEntry)
  })

  onDestroy(() => {
    if (map) {
      map.removeLayer(layer)
    }
  })

  const isVisible = (feature: AreaFeature): boolean => feature.properties.visible
  const isCurrent = (feature: AreaFeature): boolean => !!feature.properties.current

  $: createAreaDisplay = (feature: AreaFeature): string => {
    const typeDisplay = $areaTypeMap[feature.properties.type]
    const areaDisplay = formatArea(area(feature)) + " " + $_("ha")
    const dateCurrentDisplay = dateCurrentFormat(feature.properties)
    return `${typeDisplay} (${areaDisplay}) ${dateCurrentDisplay}`
  }
</script>

{#if areas.length > 0}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <ul class={valueClass}>
      {#each features as feature}
        <li class:font-bold={isCurrent(feature)}>
          <label
            class="inline-flex cursor-pointer"
            title={isVisible(feature) ? $_("Hide") : $_("Show")}
          >
            <input
              class="appearance-none"
              name="visibility_toggle_area_feature_{feature.properties.id}"
              type="checkbox"
              bind:checked={feature.properties.visible}
            />
            {#if isVisible(feature)}
              <EyeIcon class="mr-1 h-5 w-5" />
            {:else}
              <EyeSlashIcon class="mr-1 h-5 w-5" />
            {/if}
            {createAreaDisplay(feature)}
          </label>
        </li>
      {/each}
    </ul>
  </div>
{/if}
