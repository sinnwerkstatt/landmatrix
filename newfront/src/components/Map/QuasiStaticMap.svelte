<script lang="ts">
  import type { MarkerOptions } from "leaflet";
  import { DivIcon, FeatureGroup, Marker } from "leaflet?client";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { filters } from "$lib/filters";
  import { countries, regions } from "$lib/stores";
  import type { Marker as MarkerType } from "$lib/types/wagtail";
  import BigMap from "$components/Map/BigMap.svelte";
  import { styleCircle } from "./map_helper";

  export let countryID: number;
  export let regionID: number;
  export let markers: MarkerType[] = [];

  let map;
  let featureGroup;

  function focusMap() {
    if (regionID) {
      const reg = $regions.find((r) => r.id === regionID);
      map.fitBounds(
        [
          [reg.point_lat_min, reg.point_lon_min],
          [reg.point_lat_max, reg.point_lon_max],
        ],
        { animate: false }
      );
    } else if (countryID) {
      const country = $countries.find((c) => c.id === countryID);
      map.setView([country.point_lat, country.point_lon], 4, {
        animate: false,
      });
    } else map.fitWorld({ animate: false });
  }

  $: if (map && markers) {
    if (!featureGroup) featureGroup = new FeatureGroup();
    else featureGroup.clearLayers();
    featureGroup.addTo(map);

    if (regionID) drawRegionMarkers();
    else if (countryID) drawCountryMarkers();
    else drawGlobalMarkers();

    focusMap();
  }

  const LMCircleClass =
    "group opacity-90 text-sm rounded-full text-center !flex justify-center items-center drop-shadow-marker";

  function drawGlobalMarkers() {
    for (let mark of markers) {
      let circle = new Marker(mark.coordinates, {
        icon: new DivIcon({ className: LMCircleClass }),
        regionId: mark.region_id,
      } as MarkerOptions);
      featureGroup.addLayer(circle);
      const country_name = $regions.find((r) => r.id === mark.region_id).name;
      styleCircle(circle, mark.count / 50, country_name, true, 30);
    }
  }

  function drawRegionMarkers() {
    for (let mark of markers) {
      let circle = new Marker(mark.coordinates, {
        icon: new DivIcon({ className: LMCircleClass }),
        countryId: mark.country_id,
      } as MarkerOptions);
      featureGroup.addLayer(circle);
      styleCircle(circle, mark.count / 20, mark.count.toString(), true, 15);
    }
  }

  function drawCountryMarkers() {
    for (let mark of markers) featureGroup.addLayer(new Marker(mark.coordinates));
  }

  const onClickMap = async () => {
    if (regionID) {
      $filters.region_id = regionID;
      $filters.country_id = undefined;
    } else if (countryID) {
      $filters.region_id = undefined;
      $filters.country_id = countryID;
    }
    await goto("/map");
  };
</script>

<div
  class="mt-6 w-full min-h-[300px] h-[30vh] relative border border-orange shadow-md cursor-pointer hover:border-orange-300"
  on:click={onClickMap}
>
  <div
    class="group absolute w-full h-full z-[1000] bg-transparent flex hover:bg-orange/20 transition duration-300"
  >
    <span
      class="invisible opacity-0 self-center text-center w-full z-1 text-[4rem] font-bold text-white group-hover:opacity-100  group-hover:visible hover-text transition duration-500"
    >
      {$_("Go to map")}
    </span>
  </div>
  <BigMap
    options={{
      zoomControl: false,
      dragging: false,
      doubleClickZoom: false,
      boxZoom: false,
      center: [12, 30],
    }}
    containerClass="min-h-full h-full"
    showLayerSwitcher={false}
    on:ready={(m) => (map = m.detail)}
  />
</div>
