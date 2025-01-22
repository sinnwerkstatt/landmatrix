<script lang="ts">
  import { Feature, MapBrowserEvent, type Map } from "ol"
  import { Point } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { fromLonLat } from "ol/proj"
  import { Vector as VectorSource } from "ol/source"
  import * as R from "ramda"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/state"

  import { filters } from "$lib/filters"
  import { dealsNG } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"
  import { type DealHull } from "$lib/types/data"
  import { debounce } from "$lib/utils"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import {
    createMarkerTooltipOverlay,
    createStyledPoint,
    displayDealsCount,
    markerStyle,
    regionHoverInteraction,
  } from "$components/Map/mapHelper"
  import {
    baseLayers,
    contextLayers,
    selectedLayers,
  } from "$components/Map/mapstuff.svelte"
  import OLMap from "$components/Map/OLMap.svelte"
  import { createCoordinatesMap } from "$components/Map/utils"

  const ZOOM_LEVEL = {
    REGION_CLUSTERS: 2,
    COUNTRY_CLUSTERS: 4,
    DEAL_CLUSTERS: 6,
  }
  const REGION_COORDINATES: { [key: number]: [number, number] } = {
    2: [17.082249, 6.06433],
    9: [140.0188, -22.7359],
    21: [-105.2551, 54.526],
    142: [100.6197, 34.0479],
    150: [37.9587, 52.0055],
    419: [-61.3269, -4.442],
  }

  let bigmap: Map | undefined
  let currentZoom: number | undefined
  const markersVectorSource = new VectorSource({})
  let skipMapRefresh = false

  let countryCoords = $derived(createCoordinatesMap(page.data.countries))

  const regionCircleClick = (evt: MapBrowserEvent<UIEvent>) => {
    const feature = bigmap?.forEachFeatureAtPixel(
      evt.pixel,
      feature => feature as Feature<Point>,
    )
    if (feature) $filters.region_id = feature.getProperties().regionID
  }

  const countryCircleClick = (evt: MapBrowserEvent<UIEvent>) => {
    const feature = bigmap?.forEachFeatureAtPixel(
      evt.pixel,
      feature => feature as Feature<Point>,
    )
    if (feature) $filters.country_id = feature.getProperties().countryID
  }
  const singleMarkerClick = (evt: MapBrowserEvent<UIEvent>) => {
    if (!bigmap) return

    const feature = bigmap.forEachFeatureAtPixel(
      evt.pixel,
      feature => feature as Feature<Point>,
    )

    if (feature) {
      createMarkerTooltipOverlay(feature).then(ovrl => {
        bigmap!.addOverlay(ovrl)
        bigmap!.getOverlays().forEach(overlay => {
          if (overlay !== ovrl) bigmap!.removeOverlay(overlay)
        })
      })
    } else bigmap.getOverlays().forEach(overlay => bigmap!.removeOverlay(overlay))
  }

  function bigMapIsReady(_map: Map) {
    bigmap = _map

    if (!browser) return
    bigmap.on("moveend", () => refreshMap())
    bigmap.on("change:size", () => refreshMap())

    bigmap.addLayer(
      new VectorLayer({ source: markersVectorSource, style: () => markerStyle }),
    )

    flyToCountryOrRegion($filters.country_id, $filters.region_id)
  }

  const _refreshMap = (): void => {
    if (!bigmap || $dealsNG.length === 0 || skipMapRefresh) return

    currentZoom = bigmap.getView().getZoom()
    if (!currentZoom) return

    markersVectorSource.clear(true)
    bigmap.removeInteraction(regionHoverInteraction)
    bigmap.un("click", regionCircleClick)
    bigmap.un("click", countryCircleClick)
    bigmap.un("click", singleMarkerClick)

    const totalDealSizeCalculator = R.reduce<DealHull, number>(
      (acc, deal) => acc + (deal.selected_version.deal_size ?? 0),
      0,
    )

    if (currentZoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !$filters.country_id) {
      // cluster by LM region
      R.pipe(
        R.groupBy(R.pipe(R.prop("region_id"), R.toString)),
        R.forEachObjIndexed((deals, regionId) => {
          if (regionId === "undefined" || !deals) return

          const hectares = totalDealSizeCalculator(deals)
          const feature = createStyledPoint(
            fromLonLat(REGION_COORDINATES[+regionId]),
            $displayDealsCount
              ? Math.max(Math.log(deals.length) * 9, 40)
              : Math.max(Math.log(hectares) * 4, 40),
            page.data.regions.find(r => r.id === +regionId)?.name ?? "",
            $displayDealsCount
              ? `${deals.length} ${$_("locations")}`
              : `${hectares.toLocaleString("fr").replace(",", ".")} ${$_("hectares")}`,
          )
          feature.setProperties({ regionID: +regionId })

          markersVectorSource.addFeature(feature)
        }),
      )($dealsNG)

      bigmap.addInteraction(regionHoverInteraction)
      bigmap.on("click", regionCircleClick)
    } else if (currentZoom < ZOOM_LEVEL.DEAL_CLUSTERS) {
      // cluster by country
      R.pipe(
        R.groupBy(R.pipe(R.prop("country_id"), R.toString)),
        R.forEachObjIndexed((deals, countryId) => {
          if (countryId === "undefined" || !deals) return

          const hectares = totalDealSizeCalculator(deals)
          const feature = createStyledPoint(
            fromLonLat(countryCoords[+countryId]),
            $displayDealsCount
              ? Math.max(Math.log(deals.length) * 9, 40)
              : Math.max(Math.log(hectares) * 4, 40),
            page.data.countries.find(c => c.id === +countryId)?.name ?? "",
            $displayDealsCount
              ? `${deals.length} ${$_("locations")}`
              : `${hectares.toLocaleString("fr").replace(",", ".")} ${$_("hectares")}`,
          )
          feature.setProperties({ countryID: +countryId })

          markersVectorSource.addFeature(feature)
        }),
      )($dealsNG)

      bigmap.addInteraction(regionHoverInteraction)
      bigmap.on("click", countryCircleClick)
    } else {
      // show all deals / markers
      for (const deal of $dealsNG) {
        if (!deal.selected_version.locations) continue

        for (const loc of deal.selected_version.locations) {
          if (!loc.point) continue

          const feature = new Feature({
            geometry: new Point(fromLonLat(loc.point.coordinates!)),
          })

          feature.setProperties({
            deal: deal,
            // deal_id: deal.id,
            location: loc,
            // deal_size: deal.selected_version.deal_size,
            // region_id: deal.region_id,
            // country_id: deal.country_id,
          })
          markersVectorSource.addFeature(feature)
        }
      }

      bigmap.on("click", singleMarkerClick)
    }
  }
  const refreshMap = debounce(_refreshMap)

  async function flyToCountryOrRegion(country_id?: number, region_id?: number) {
    if (country_id && region_id) return // skip ambiguous destinations
    if (!browser || !bigmap) return

    const mapView = bigmap.getView()
    let coords: [number, number] = [0, 0]
    let zoom = ZOOM_LEVEL.REGION_CLUSTERS
    if (country_id) {
      coords = countryCoords[country_id]
      zoom = ZOOM_LEVEL.DEAL_CLUSTERS
    } else if (region_id) {
      coords = REGION_COORDINATES[region_id]
      zoom = ZOOM_LEVEL.COUNTRY_CLUSTERS
    }
    if (currentZoom && zoom < currentZoom) {
      // zooming out, apply filter after flying to avoid loading of pins for entire region
      skipMapRefresh = true
      mapView.animate({ center: fromLonLat(coords), zoom: zoom, duration: 300 })
      setTimeout(() => {
        skipMapRefresh = false
        refreshMap()
      }, 1000)
    } else {
      // zooming in, apply filter before flying
      refreshMap()
      setTimeout(
        () =>
          mapView.animate({ center: fromLonLat(coords), zoom: zoom, duration: 300 }),
        700,
      )
    }
  }

  $effect(() => {
    flyToCountryOrRegion($filters.country_id, $filters.region_id)
  })

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })

  const unsubsribeMapRefresher = displayDealsCount.subscribe(() => refreshMap())
  onDestroy(() => {
    unsubsribeMapRefresher()
  })
</script>

<DataContainer>
  <div class="h-full w-full">
    <OLMap
      containerClass="min-h-full h-full"
      mapReady={bigMapIsReady}
      options={{
        minZoom: 0,
        zoom: ZOOM_LEVEL.REGION_CLUSTERS,
        center: [30, 12],
        zoomControl: false,
      }}
    />
  </div>

  {#snippet FilterBarSnippet()}
    <h2 class="heading5 my-2 px-2">{$_("Map settings")}</h2>
    <!--      <FilterCollapse expanded title={$_("Displayed data")}>-->
    <!--        <label class="block">-->
    <!--          <input-->
    <!--            bind:group={$displayDealsCount}-->
    <!--            name="deals-count-display"-->
    <!--            class="radio-btn"-->
    <!--            type="radio"-->
    <!--            value={true}-->
    <!--          />-->
    <!--          {$_("Number of deal locations")}-->
    <!--        </label>-->
    <!--        <label class="block">-->
    <!--          <input-->
    <!--            bind:group={$displayDealsCount}-->
    <!--            name="deals-count-display"-->
    <!--            class="radio-btn"-->
    <!--            type="radio"-->
    <!--            value={false}-->
    <!--          />-->
    <!--          {$_("Area (ha)")}-->
    <!--        </label>-->
    <!--      </FilterCollapse>-->

    <FilterCollapse expanded title={$_("Base layer")}>
      {#each baseLayers as layer}
        <label class="block">
          <input
            type="radio"
            name="base-layer-switch"
            bind:group={selectedLayers.baseLayer}
            value={layer.id}
            class="radio-btn"
          />
          {layer.name}
        </label>
      {/each}
    </FilterCollapse>

    <FilterCollapse title={$_("Context layers")}>
      {#each contextLayers as layer}
        <label class="block">
          <input
            type="checkbox"
            bind:group={selectedLayers.contextLayers}
            value={layer.id}
            class="checkbox-btn"
          />
          {layer.name}
          {#if selectedLayers.contextLayers.includes(layer.id)}
            <img
              alt="Legend for {layer.name}"
              src={layer.legend}
              class="mb-4 ml-4 mt-2 border"
              loading="lazy"
            />
          {/if}
        </label>
      {/each}
    </FilterCollapse>
  {/snippet}
</DataContainer>
