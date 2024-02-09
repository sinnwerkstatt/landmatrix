<script lang="ts">
  import type { Feature } from "geojson"
  import type { GeoJSONOptions, Layer, LeafletMouseEvent, Map as LMap } from "leaflet"
  import { GeoJSON, LatLngBounds, Marker, Path, Polygon } from "leaflet?client"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import type { Location } from "$lib/types/deal"
  import type { Country } from "$lib/types/wagtail"
  import { isEmptySubmodel } from "$lib/utils/data_processing"
  import { AREA_TYPE_COLOR_MAP, AREA_TYPES, padBounds } from "$lib/utils/location"

  import PointField from "$components/Fields/Edit/PointField.svelte"
  import LocationGoogleField from "$components/Fields/Edit2/LocationGoogleEditField.svelte"
  import EditField from "$components/Fields/EditField.svelte"
  import LocationDot from "$components/icons/LocationDot.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import DealLocationsAreaField from "./DealLocationsAreaField.svelte"

  export let locations: Location[] = []
  export let country: Country | undefined
  let currentHoverFeature: Feature | null = null
  let hiddenFeatures: Feature[] = []
  let hoverLocationID: string | null = null
  let activeLocationID: string | null = null
  let bigmap: LMap

  let markerMode = false

  let locationFGs = new Map<string, GeoJSON>()

  // type guards
  const isPath = (layer: Layer): layer is Path => layer instanceof Path
  const isMarker = (layer: Layer): layer is Marker => layer instanceof Marker
  const isPolygon = (layer): layer is Polygon => layer instanceof Polygon

  const geojsonOptions: GeoJSONOptions = {
    onEachFeature: (feature: Feature, layer: Layer) => {
      if (isPath(layer)) {
        layer.addEventListener("mouseover", () => {
          currentHoverFeature = feature
        })
        layer.addEventListener("mouseout", () => {
          currentHoverFeature = null
        })
      }

      if (isMarker(layer)) {
        layer.addEventListener("mouseover", () => {
          hoverLocationID = feature.properties?.id
        })
        layer.addEventListener("mouseout", () => {
          hoverLocationID = null
        })
        layer.addEventListener("dragend", () => {
          const activeLocation = locations.find(l => l.id === activeLocationID)
          const latlng = layer.getLatLng()
          activeLocation.point = {
            lat: parseFloat(latlng.lat.toFixed(5)),
            lng: parseFloat(latlng.lng.toFixed(5)),
          }
          locations = locations
        })
        layer.addEventListener("click", () => {
          const activeLocation = locations.find(l => l.id === feature.properties?.id)
          onActivateLocation(activeLocation)
        })
      }
    },
  }

  function _updateGeoJSON(fitBounds = true) {
    locations?.forEach(loc => {
      const fg = locationFGs.get(loc.id) ?? _addNewLayerGroup(loc.id)
      fg.clearLayers()
      if (loc.areas) fg.addData(loc.areas)
      if (loc.point && loc.point.lat && loc.point.lng) {
        let pt = new Marker(loc.point).toGeoJSON()
        pt.properties = { id: loc.id } //, name: loc.name, type: "point" };
        fg.addData(pt)
      }
    })
    if (fitBounds) _fitBounds()
    hiddenFeatures = hiddenFeatures // trigger reevaluation of styling
    updateLocationVisibility()
  }

  function _fitBounds() {
    let bounds = new LatLngBounds([])
    locationFGs.forEach(value => {
      bounds.extend(value.getBounds())
    })
    if (bounds.isValid()) {
      bounds = padBounds(bounds)
    } else if (country) {
      bounds = new LatLngBounds([
        [country.point_lat_min, country.point_lon_min],
        [country.point_lat_max, country.point_lon_max],
      ])
    }
    bigmap.fitBounds(bounds)
  }

  function _addNewLayerGroup(id: string): GeoJSON {
    let fg = new GeoJSON(undefined, geojsonOptions)
    locationFGs.set(id, fg)
    bigmap.addLayer(fg)
    return fg
  }

  function _removeLayerGroup(id: string): void {
    locationFGs.get(id).clearLayers()
    locationFGs.delete(id)
  }

  function removeEntry(entry: Location) {
    if (!isEmptySubmodel(entry)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Location")} ${entry.id}?`)
      if (!areYouSure) {
        return
      }
    }

    locations = locations.filter(x => x.id !== entry.id)
    _removeLayerGroup(entry.id)
    if (entry.id === activeLocationID) {
      activeLocationID = null
    }
  }

  function addEntry() {
    const currentIDs = locations.map(x => x.id.toString())
    const newEntry: Location = { id: newNanoid(currentIDs) }
    locations = [...locations, newEntry]
    _updateGeoJSON()
    onActivateLocation(newEntry)
  }

  const onMapReady = (event: CustomEvent<LMap>) => {
    bigmap = event.detail
    _updateGeoJSON()
    _fitBounds()
  }

  const onGoogleLocationAutocomplete = (
    event: CustomEvent<{ latLng: [number, number]; viewport: unknown }>,
  ) => {
    const activeLocation = locations.find(l => l.id === activeLocationID)
    activeLocation.point = {
      lat: parseFloat(event.detail.latLng[0].toFixed(5)),
      lng: parseFloat(event.detail.latLng[1].toFixed(5)),
    }
    locations = locations
    _updateGeoJSON()
  }

  const onActivateLocation = (location: Location) => {
    if (activeLocationID === location.id) {
      activeLocationID = null
      markerMode = false
    } else {
      activeLocationID = location.id
      if (!locationFGs.get(activeLocationID)) {
        _addNewLayerGroup(activeLocationID)
      }
    }
    updateLocationVisibility()
  }

  const updateLocationVisibility = () =>
    locationFGs.forEach((value, key) => {
      value.eachLayer((layer: Layer) => {
        if (isMarker(layer) || isPath(layer)) {
          const element = layer.getElement()
          if (key !== activeLocationID) element?.classList.add("leaflet-hidden")
          else element?.classList.remove("leaflet-hidden")
        }
      })
    })

  const onCountryChange = () =>
    country &&
    bigmap?.fitBounds([
      [country.point_lat_min, country.point_lon_min],
      [country.point_lat_max, country.point_lon_max],
    ])

  const updateActiveLocationMarker = (event: LeafletMouseEvent) => {
    const activeLocation = locations.find(l => l.id === activeLocationID)
    activeLocation.point = {
      lat: parseFloat(event.latlng.lat.toFixed(5)),
      lng: parseFloat(event.latlng.lng.toFixed(5)),
    }
    locations = locations
    _updateGeoJSON(false)
  }

  $: if (bigmap && locations) {
    if (markerMode) {
      bigmap.addEventListener("click", updateActiveLocationMarker)
      bigmap.eachLayer((layer: Layer) => {
        if (isMarker(layer) && layer.dragging) layer.dragging.enable()
      })
    } else {
      bigmap.removeEventListener("click", updateActiveLocationMarker)
      bigmap.eachLayer((layer: Layer) => {
        if (isMarker(layer) && layer.dragging) layer.dragging.disable()
      })
    }
  }

  $: {
    // adjust style for hove and visibility state
    if (activeLocationID) {
      locationFGs
        .get(activeLocationID)
        .getLayers()
        .filter(isPolygon)
        .forEach(layer => {
          if (layer.feature) {
            const defaultStyle = {
              dashArray: "5, 5",
              dashOffset: "0",
              fillOpacity: 0.4,
              color: "#000000",
              weight: 1.5,
              fillColor: AREA_TYPE_COLOR_MAP[layer.feature.properties.type],
            }

            if (hiddenFeatures.includes(layer.feature)) {
              layer.setStyle({
                color: "rgba(0,0,0,0)",
                fillColor: "rgba(0,0,0,0)",
              })
            } else if (layer.feature === currentHoverFeature) {
              layer.setStyle({ ...defaultStyle, color: "#000000", weight: 3 })
            } else {
              layer.setStyle(defaultStyle)
            }
          }
        })
    }
  }

  onMount(() => {
    if (locations?.length > 0) onActivateLocation(locations[0])
  })
</script>

<form id="locations">
  <EditField
    bind:value={country}
    disabled={locations && locations.length > 0}
    labelClasses="w-1/4"
    valueClasses="w-3/4"
    wrapperClasses="flex my-3 items-center"
    fieldname="country"
    on:change={onCountryChange}
  />

  {#if country}
    <section class="isolate flex flex-wrap">
      <div class="pr-3 lg:w-1/3">
        {#each locations as loc, index}
          <div
            class="mt-4 border-4 bg-gray-50 p-2 dark:bg-gray-800 {hoverLocationID ===
            loc.id
              ? 'border-orange-400'
              : activeLocationID === loc.id
                ? 'border-gray-700 dark:border-gray-600'
                : 'border-gray-100 dark:border-gray-700'}"
          >
            <div class="flex flex-row items-center justify-between">
              <button
                class="flex-grow cursor-pointer p-2 text-left"
                on:click={() => onActivateLocation(loc)}
              >
                <h3 class="m-0">
                  {index + 1}. {$_("Location")}
                  <small class="text-sm text-gray-500">#{loc.id}</small>
                </h3>
              </button>
              <button class="flex-initial p-2" on:click={() => removeEntry(loc)}>
                <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
              </button>
            </div>
            {#if activeLocationID === loc.id}
              <div transition:slide={{ duration: 200 }} class="mt-4">
                <EditField
                  fieldname="level_of_accuracy"
                  bind:value={loc["level_of_accuracy"]}
                  model="location"
                  wrapperClasses="flex flex-col"
                  labelClasses="mb-1"
                  valueClasses="mb-3"
                />
                <div class="flex flex-col">
                  <div class="mb-1">{$_("Location")}</div>
                  <div class="mb-3">
                    <LocationGoogleField
                      bind:value={loc.name}
                      countryCode={country.code_alpha2}
                      on:change={onGoogleLocationAutocomplete}
                    />
                  </div>
                </div>

                <div class="flex flex-col">
                  <div class="mb-1">{$_("Point")}</div>
                  <div class="mb-3">
                    <PointField bind:value={loc.point} on:input={_updateGeoJSON} />
                  </div>
                </div>
                {#each ["description", "facility_name", "comment"] as fieldname}
                  <EditField
                    {fieldname}
                    bind:value={loc[fieldname]}
                    model="location"
                    wrapperClasses="flex flex-col"
                    labelClasses="mb-2"
                    valueClasses="mb-4"
                  />
                {/each}
              </div>
            {/if}
          </div>
        {/each}
        <div class="mt-4">
          <button
            type="button"
            class="btn btn-primary flex items-center"
            on:click={addEntry}
          >
            <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
            {$_("Add")}
            {$_("Location")}
          </button>
        </div>
      </div>
      <div class="mt-4 h-[30rem] w-full lg:w-2/3">
        <BigMap
          containerClass="h-[30rem]"
          options={{ center: [0, 0] }}
          on:ready={onMapReady}
        >
          {#if activeLocationID}
            <div
              class="absolute bottom-2 left-2 {markerMode
                ? 'bg-orange text-white'
                : 'bg-white text-orange'}"
            >
              <button
                type="button"
                class="z-10 rounded border-2 border-black/30 px-2 pb-1.5 pt-0.5"
                on:click={() => {
                  markerMode = !markerMode
                }}
                title="Create or move point"
              >
                <LocationDot class="inline h-5 w-5" />
              </button>
            </div>
          {/if}
        </BigMap>
        <div>
          {#if locations.length && activeLocationID}
            {#each AREA_TYPES as areaType}
              <DealLocationsAreaField
                {areaType}
                bind:locations
                bind:activeLocationID
                bind:currentHoverFeature
                bind:hiddenFeatures
                on:change={_updateGeoJSON}
              />
            {/each}
          {/if}
        </div>
      </div>
    </section>
  {/if}
</form>

<style>
  :global(path.leaflet-hidden) {
    display: none;
  }

  :global(img.leaflet-hidden) {
    opacity: 0.6;
    filter: saturate(0);
  }
</style>
