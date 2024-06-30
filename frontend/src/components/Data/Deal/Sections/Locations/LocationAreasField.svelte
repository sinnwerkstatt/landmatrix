<script lang="ts">
  import { area as turfArea } from "@turf/turf"
  import type { GeoJSON, Map } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { createLabels, fieldChoices } from "$lib/stores"
  import type { Area, AreaFeature, AreaFeatureLayer, AreaType } from "$lib/types/data"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import {
    dateCurrentFormat,
    formatArea,
  } from "$components/Fields/Display2/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"

  import {
    AREA_TYPE_COLOR_MAP,
    areaToFeature,
    createAreaFeaturesLayer,
    fitBounds,
  } from "./locations"

  export let map: Map | undefined
  export let areas: Area[]
  export let fieldname: string
  export let label = ""

  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  // Reflexive so that features change on browser navigation
  let layer: AreaFeatureLayer

  let visibleMap: { [id: string]: boolean }
  $: visibleMap = areas.reduce((acc, value) => ({ ...acc, [value.nid]: true }), {})
  let hoverMap: { [id: string]: boolean }
  $: hoverMap = areas.reduce((acc, value) => ({ ...acc, [value.nid]: false }), {})

  $: if (map) {
    layer && map.removeLayer(layer)
    layer = createAreaFeaturesLayer(areas.map(areaToFeature))
    layer.eachLayer(layer => {
      const l = layer as GeoJSON
      const feature: AreaFeature = l.feature as never

      l.addEventListener("mouseover", () => (hoverMap[feature.id!] = true))
      l.addEventListener("mouseout", () => (hoverMap[feature.id!] = false))
    })
    map.addLayer(layer)

    fitBounds(map)
  }

  $: if (map && layer) {
    layer.eachLayer(layer => {
      const l = layer as GeoJSON
      const feature: AreaFeature = l.feature as never

      l.setStyle({
        opacity: visibleMap[feature.id!] ? 1 : 0,
        fillOpacity: visibleMap[feature.id!] ? 0.6 : 0,
      })
    })
  }

  $: if (map && layer) {
    layer.eachLayer(layer => {
      const l = layer as GeoJSON
      const feature: AreaFeature = l.feature as never

      if (visibleMap[feature.id!] && hoverMap[feature.id!]) {
        l.openPopup()
      } else {
        l.closePopup()
      }
    })
  }

  onMount(() => {
    layer = createAreaFeaturesLayer(areas.map(areaToFeature))
  })

  onDestroy(() => {
    if (map && layer) {
      map.removeLayer(layer)
    }
  })

  $: areaTypeLabels = createLabels<AreaType>($fieldChoices.area.type)

  $: createAreaDisplay = (area: Area): string => {
    const feature = areaToFeature(area)
    const typeDisplay = areaTypeLabels[area.type]
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

    <div class={valueClass}>
      <ul class="flex flex-col gap-1">
        {#each areas as area (area.nid)}
          {@const inputName = "area-visibility-toggle"}
          {@const inputId = `${inputName}-${area.nid}`}

          <li
            class="inline-flex p-0.5"
            class:font-bold={!!area.current}
            on:mouseenter={() => (hoverMap[area.nid] = true)}
            on:mouseleave={() => (hoverMap[area.nid] = false)}
            class:colored={hoverMap[area.nid]}
            style:--color={AREA_TYPE_COLOR_MAP[area.type]}
          >
            <input
              class="peer appearance-none"
              id={inputId}
              name={inputName}
              type="checkbox"
              on:click|preventDefault={() => {
                visibleMap[area.nid] = !visibleMap[area.nid]
              }}
            />
            <label
              for={inputId}
              class="inline-flex cursor-pointer peer-focus-visible:outline"
              title={(visibleMap[area.nid] ? $_("Hide") : $_("Show")) +
                " " +
                $_("area")}
            >
              <span class="inline-flex w-fit">
                {#if visibleMap[area.nid]}
                  <EyeIcon class="mr-1 h-5 w-5" />
                {:else}
                  <EyeSlashIcon class="mr-1 h-5 w-5" />
                {/if}
              </span>
              {createAreaDisplay(area)}
            </label>
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}

<style lang="postcss">
  .colored {
    /*color: var(--color, black);*/
    /*background-color: var(--color);*/
    @apply text-gray-400;
  }
</style>
