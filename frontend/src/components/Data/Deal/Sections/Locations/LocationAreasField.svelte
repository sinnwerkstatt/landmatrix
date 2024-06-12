<script lang="ts">
  import { area as turfArea } from "@turf/turf"
  import { type Map } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores/maps"
  import type { Area, AreaFeature, AreaFeatureLayer } from "$lib/types/newtypes"
  import {
    areaToFeature,
    createAreaFeaturesLayer,
    isCurrent,
    isVisible,
  } from "$lib/utils/location"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import {
    dateCurrentFormat,
    formatArea,
  } from "$components/Fields/Display2/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"

  export let map: Map | undefined
  export let areas: Area[]
  export let fieldname: string
  export let label = ""

  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let isSelectedEntry: boolean

  let features: AreaFeature[] = areas.map(areaToFeature)
  let layer: AreaFeatureLayer

  $: if (map && layer) {
    map.removeLayer(layer)
    layer = createAreaFeaturesLayer(features, isSelectedEntry)
    map.addLayer(layer)
  }

  onMount(() => {
    layer = createAreaFeaturesLayer(features, isSelectedEntry)
  })

  onDestroy(() => {
    if (map) {
      map.removeLayer(layer)
    }
  })

  $: createAreaDisplay = (feature: AreaFeature): string => {
    const typeDisplay = $areaTypeMap[feature.properties.type]
    const areaDisplay = formatArea(turfArea(feature)) + " " + $_("ha")
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
