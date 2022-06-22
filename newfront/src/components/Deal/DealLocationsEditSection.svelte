<script lang="ts">
  import type { Feature } from "geojson";
  import type { Layer, Map as LMap } from "leaflet";
  import { GeoJSON, LatLngBounds, Marker, Path } from "leaflet?client";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { slide } from "svelte/transition";
  import { newNanoid } from "$lib/helpers";
  import type { Location } from "$lib/types/deal";
  import type { Country } from "$lib/types/wagtail";
  import { isEmptySubmodel } from "$lib/utils/data_processing";
  import LocationGoogleField from "$components/Fields/Edit/LocationGoogleField.svelte";
  import PointField from "$components/Fields/Edit/PointField.svelte";
  import EditField from "$components/Fields/EditField.svelte";
  import CursorMoveIcon from "$components/icons/CursorMoveIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import TrashIcon from "$components/icons/TrashIcon.svelte";
  import BigMap from "$components/Map/BigMap.svelte";
  import DealLocationsAreaField from "./DealLocationsAreaField.svelte";

  export let model = "location";
  export let modelName = "Location";
  export let locations: Location[] = [];
  export let country: Country;

  let currentHoverFeature: Feature | null;
  let hiddenFeatures: Feature[] = [];
  let activeFeatureGroup: GeoJSON;
  let hoverLocationID: string;
  let activeLocationID: string | undefined;
  let bigmap: LMap;

  let cursorsMovable = false;

  let locationFGs = new Map<string, GeoJSON>();
  // const geoman_opts = {
  //   position: "topleft" as ControlPosition,
  //   drawCircle: false,
  //   drawCircleMarker: false,
  //   drawRectangle: false,
  //   drawPolyline: false,
  //   drawPolygon: false,
  //   cutPolygon: false,
  //   drawMarker: false,
  // };

  const areaTypes = ["production_area", "contract_area", "intended_area"];
  const colormap = {
    contract_area: "#ff00ff",
    intended_area: "#66ff33",
    production_area: "#ff0000",
    "": "#ffe600",
  };

  const geojsonOptions = {
    style: (feature: Feature) => {
      if (currentHoverFeature === feature) {
        return { color: "orange" };
      }
      return { color: colormap[feature.properties.type] };
    },
    onEachFeature: (feature: Feature, layer: Layer) => {
      if (layer instanceof Path) {
        layer.addEventListener("mouseover", () => {
          if (hiddenFeatures.includes(feature)) return;
          layer.setStyle({ color: "orange" });
          currentHoverFeature = feature;
        });
        layer.addEventListener("mouseout", () => {
          if (hiddenFeatures.includes(feature)) return;
          layer.setStyle({ color: colormap[feature.properties.type] });
          currentHoverFeature = null;
        });
      }

      if (layer instanceof Marker) {
        layer.addEventListener("mouseover", () => {
          hoverLocationID = feature.properties?.id;
        });
        layer.addEventListener("mouseout", () => {
          hoverLocationID = null;
        });
        layer.addEventListener("dragend", () => {
          const activeLocation = locations.find((l) => l.id === activeLocationID);
          const latlng = layer.getLatLng();
          activeLocation.point = {
            lat: parseFloat(latlng.lat.toFixed(5)),
            lng: parseFloat(latlng.lng.toFixed(5)),
          };
          locations = locations;
        });
        layer.addEventListener("click", () => {
          activeLocationID = locations.find((l) => l.id === feature.properties?.id)?.id;
        });
      }
    },
  };

  function _updateGeoJSON() {
    locations?.forEach((loc) => {
      const fg = locationFGs.get(loc.id) ?? _addNewLayerGroup(loc.id);
      fg.clearLayers();
      if (loc.areas) fg.addData(loc.areas);
      if (loc.point) {
        let pt = new Marker(loc.point).toGeoJSON();
        pt.properties = { id: loc.id }; //, name: loc.name, type: "point" };
        fg.addData(pt);
      }
    });
    _fitBounds();
  }

  function _fitBounds() {
    let bounds = new LatLngBounds([]);
    locationFGs.forEach((value) => {
      bounds.extend(value.getBounds());
    });
    if (bounds.isValid()) bounds = bounds.pad(0.5);
    else {
      bounds = new LatLngBounds([
        [country.point_lat_min, country.point_lon_min],
        [country.point_lat_max, country.point_lon_max],
      ]);
    }
    bigmap.fitBounds(bounds);
  }

  function _addNewLayerGroup(id: string): GeoJSON {
    let fg = new GeoJSON(undefined, geojsonOptions);
    locationFGs.set(id, fg);
    bigmap.addLayer(fg);
    return fg;
  }

  function removeEntry(entry: Location) {
    if (isEmptySubmodel(entry)) {
      locations = locations.filter((x) => x.id !== entry.id);
      return;
    }
    const areYouSure = confirm(`${$_("Remove")} ${$_(modelName)} ${entry.id}?`);
    if (areYouSure === true) locations = locations.filter((x) => x.id !== entry.id);
  }

  function addEntry() {
    const currentIDs = locations.map((x) => x.id.toString());
    const newEntry: Location = { id: newNanoid(currentIDs) };
    locations = [...locations, newEntry];
    activeLocationID = newEntry.id;
    _updateGeoJSON();
  }

  const onMapReady = (event: CustomEvent<LMap>) => {
    bigmap = event.detail;
    _updateGeoJSON();
    _fitBounds();
  };

  const onGoogleLocationAutocomplete = (
    event: CustomEvent<{ latLng: [number, number]; viewport: unknown }>
  ) => {
    const activeLocation = locations.find((l) => l.id === activeLocationID);
    activeLocation.point = {
      lat: parseFloat(event.detail.latLng[0].toFixed(5)),
      lng: parseFloat(event.detail.latLng[1].toFixed(5)),
    };
    locations = locations;
    _updateGeoJSON();
  };

  const onActivateLocation = (location: Location) => {
    if (activeLocationID === location.id) {
      activeLocationID = undefined;
      return;
    }
    activeLocationID = location.id;

    if (!locationFGs.get(activeLocationID)) _addNewLayerGroup(activeLocationID);
    activeFeatureGroup = locationFGs.get(activeLocationID);

    locationFGs.forEach((value, key) => {
      value.eachLayer((l: Layer) => {
        let relevant_element = l?._icon || l._path;
        if (key !== activeLocationID) relevant_element.classList.add("leaflet-hidden");
        else relevant_element.classList.remove("leaflet-hidden");
      });
    });
  };

  const onCountryChange = () =>
    country &&
    bigmap?.fitBounds([
      [country.point_lat_min, country.point_lon_min],
      [country.point_lat_max, country.point_lon_max],
    ]);

  const onToggleMarkerMovable = () => {
    cursorsMovable = !cursorsMovable;
    bigmap.eachLayer((l: Marker) => {
      if (l?._icon) {
        console.log(l);
        if (cursorsMovable) l.dragging.enable();
        else l.dragging.disable();
      }

      // if (key !== activeLocationID) relevant_element.classList.add("leaflet-hidden");
      // else relevant_element.classList.remove("leaflet-hidden");
    });
  };

  const highlightFeatureInMap = () => {
    locationFGs
      .get(activeLocationID)
      .getLayers()
      .filter((l) => l.feature.geometry.type === "Polygon")
      .filter((l) => !hiddenFeatures.includes(l.feature))
      .forEach((l) =>
        l.feature === currentHoverFeature
          ? l.setStyle({
              color: "orange",
            })
          : l.setStyle({
              color: colormap[l.feature.properties.type],
            })
      );
  };

  const updateVisibility = () => {
    locationFGs
      .get(activeLocationID)
      .getLayers()
      .filter((l) => l.feature.geometry.type === "Polygon")
      .forEach((l) =>
        hiddenFeatures.includes(l.feature)
          ? l.setStyle({
              color: "rgba(0,0,0,0)",
            })
          : l.setStyle({
              color: colormap[l.feature.properties.type],
            })
      );
  };
  onMount(() => {
    if (locations?.length > 0) onActivateLocation(locations[0]);
  });
</script>

<form id="locations">
  <!--  <pre class="text-[10px]">{JSON.stringify(locations, null, 2)}</pre>-->
  <EditField
    bind:value={country}
    disabled={locations && locations.length > 0}
    labelClasses="w-1/4"
    valueClasses="w-3/4"
    wrapperClasses="flex my-3"
    fieldname="country"
    on:change={onCountryChange}
  />

  {#if country}
    <section class="flex flex-wrap">
      <div class="lg:w-1/3 pr-3">
        {#each locations as loc, index}
          <div
            class="border {hoverLocationID === loc.id
              ? 'border-orange-400'
              : 'border-white'}"
          >
            <h3 on:click={() => onActivateLocation(loc)} class="bg-gray-200 p-2">
              {index + 1}. {$_(modelName)}
              <small class="text-sm text-gray-500">#{loc.id}</small>
              <TrashIcon
                class="w-6 h-8 text-red-600 float-right cursor-pointer"
                on:click={() => removeEntry(loc)}
              />
            </h3>
            {#if activeLocationID === loc.id}
              <div transition:slide={{ duration: 200 }} class="">
                <EditField
                  fieldname="level_of_accuracy"
                  bind:value={loc["level_of_accuracy"]}
                  {model}
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
                    {model}
                    wrapperClasses="flex flex-col"
                    labelClasses="mb-2"
                    valueClasses="mb-4"
                  />
                {/each}
              </div>
            {/if}
          </div>
        {/each}
        <div class="mt-6">
          <button
            type="button"
            class="btn btn-primary flex items-center"
            on:click={addEntry}
          >
            <PlusIcon class="w-5 h-6 mr-2 -ml-2" />
            {$_("Add")}
            {$_(modelName)}
          </button>
        </div>
      </div>
      <div class="min-h-[30rem] w-full lg:w-2/3">
        <BigMap
          containerClass="min-h-[30rem] h-[50%] mt-5"
          options={{ center: [0, 0] }}
          on:ready={onMapReady}
        >
          <div class="absolute bottom-2 left-2">
            <button
              type="button"
              class="absolute bottom-[10px] z-10 px-2 pt-0.5 pb-1.5 rounded border-2 border-black/30 {cursorsMovable
                ? 'bg-orange text-white'
                : 'bg-white text-orange'}"
              on:click={onToggleMarkerMovable}
              title={(cursorsMovable ? "Disable" : "Enable") +
                " " +
                $_("moving of markers")}
            >
              <CursorMoveIcon />
            </button>
          </div>
        </BigMap>
        <div>
          {#if activeLocationID}
            {#each areaTypes as areaType}
              <DealLocationsAreaField
                {areaType}
                bind:locations
                bind:activeLocationID
                bind:currentHoverFeature
                bind:hiddenFeatures
                on:change={_updateGeoJSON}
                on:toggleVisibility={updateVisibility}
                on:hoverFeature={highlightFeatureInMap}
              />
            {/each}
          {/if}
        </div>
      </div>
    </section>
  {/if}
</form>
