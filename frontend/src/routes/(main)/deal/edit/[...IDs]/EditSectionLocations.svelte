<script lang="ts">
  import type { Point } from "geojson"
  import type { GeoJSON, Layer, Map } from "leaflet"
  import { Control, geoJson } from "leaflet"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import {
    Location2,
    type PointFeature,
    type PointFeatureProps,
  } from "$lib/types/newtypes"
  import type { Country } from "$lib/types/wagtail"
  import { isEmptySubmodel } from "$lib/utils/data_processing"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"
  import { createPointFeatures, fitBounds } from "$lib/utils/location"

  import LocationLegend from "$components/Deal/LocationLegend.svelte"
  import LocationTooltip from "$components/Deal/LocationTooltip.svelte"
  import EditField from "$components/Fields/EditField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasEditField from "./LocationAreasEditField.svelte"

  export let locations: Location2[]
  export let country: Country | undefined

  let activeEntryIdx = -1

  let map: Map | undefined
  let locationsPointLayer: GeoJSON<PointFeatureProps, Point>

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail

    const legend = new Control({ position: "bottomleft" })
    legend.onAdd = () => createComponentAsDiv(LocationLegend)
    map.addControl(legend)

    map.addLayer(locationsPointLayer)
    fitBounds(locationsPointLayer, map)
  }

  $: if (map && locationsPointLayer) {
    map.removeLayer(locationsPointLayer)
    locationsPointLayer = createLayer(locations)
    map.addLayer(locationsPointLayer)
    fitBounds(locationsPointLayer, map)
  }

  const addEntry = () => {
    const currentIDs = locations.map(entry => entry.nid)
    locations = [...locations, new Location2(newNanoid(currentIDs))]
    activeEntryIdx = -1
  }

  const toggleActiveEntry = (index: number) => {
    activeEntryIdx = activeEntryIdx === index ? -1 : index
  }

  const removeEntry = (c: Location2) => {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Location")} #${c.nid}?`)
      if (!areYouSure) return
    }
    locations = locations.filter(x => x.nid !== c.nid)
  }

  $: onGoogleAutocomplete = (point: Point) => {
    locations[activeEntryIdx].point = point
  }

  const createLayer = (locations: Location2[]) =>
    geoJson(createPointFeatures(locations), {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        const tooltipElement = createComponentAsDiv(LocationTooltip, { feature })
        layer.bindPopup(tooltipElement, { keepInView: true })
        layer.on("click", () =>
          toggleActiveEntry(locations.findIndex(l => l.nid === feature.properties.id)),
        )
        layer.on("mouseover", () => layer.openPopup())
        layer.on("mouseout", () => layer.closePopup())
      },
    })

  onMount(() => {
    locationsPointLayer = createLayer(locations)
  })

  onDestroy(() => {
    if (map && locationsPointLayer) {
      map.removeLayer(locationsPointLayer)
    }
  })
</script>

<section class="lg:h-full">
  <form class="flex flex-wrap lg:h-full" id="locations">
    <div class="w-full overflow-y-auto p-2 lg:h-full lg:w-2/5">
      {#each locations as location, index}
        <div class="location-entry">
          <div
            class="my-2 flex flex-row items-center justify-between bg-gray-200 dark:bg-gray-700"
          >
            <h3 class="flex-grow">
              <button
                type="button"
                class="w-full p-2 text-left"
                on:click={() => toggleActiveEntry(index)}
              >
                {index + 1}. {$_("Location")}
                <small class="text-sm text-gray-500">
                  #{location.nid}
                </small>
              </button>
            </h3>
            <button
              type="button"
              class="flex-initial p-2"
              on:click={() => removeEntry(location)}
            >
              <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
            </button>
          </div>
          {#if activeEntryIdx === index}
            <div class="grid gap-2" transition:slide={{ duration: 200 }}>
              <EditField
                fieldname="location.level_of_accuracy"
                bind:value={location.level_of_accuracy}
                extras={{ required: true }}
                showLabel
              />
              <EditField
                fieldname="location.name"
                bind:value={location.name}
                extras={{
                  countryCode: country?.code_alpha2,
                  onGoogleAutocomplete,
                }}
                showLabel
              />
              <EditField
                fieldname="location.point"
                bind:value={location.point}
                showLabel
              />
              <EditField
                fieldname="location.description"
                bind:value={location.description}
                showLabel
              />
              <EditField
                fieldname="location.facility_name"
                bind:value={location.facility_name}
                showLabel
              />
              <EditField
                fieldname="location.comment"
                bind:value={location.comment}
                showLabel
              />
            </div>
          {/if}
        </div>
      {/each}
      <div class="mt-6">
        <button
          class="btn btn-primary flex items-center"
          on:click={addEntry}
          type="button"
        >
          <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
          {$_("Add")}
          {$_("Location")}
        </button>
      </div>
    </div>
    <div class="w-full p-2 lg:h-full lg:w-3/5">
      <BigMap
        containerClass="h-[400px]"
        on:ready={onMapReady}
        options={{ center: [0, 0] }}
      />
      <div class="overflow-y-auto">
        {#if activeEntryIdx !== -1}
          <LocationAreasEditField bind:areas={locations[activeEntryIdx].areas} />
        {/if}
      </div>
    </div>
  </form>
</section>
