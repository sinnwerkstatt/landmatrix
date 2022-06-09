<script lang="ts">
  import type { Feature, GeoJsonObject } from "geojson";
  import type { ControlPosition, Layer, Map as LMap } from "leaflet";
  import { GeoJSON, LatLngBounds, Marker } from "leaflet?client";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { slide } from "svelte/transition";
  import { newNanoid } from "$lib/helpers";
  import type { Location } from "$lib/types/deal";
  import type { Country } from "$lib/types/wagtail";
  import { isEmptySubmodel } from "$lib/utils/data_processing";
  import EditField from "$components/Fields/EditField.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import TrashIcon from "$components/icons/TrashIcon.svelte";
  import BigMap from "$components/Map/BigMap.svelte";
  import FileField from "../Fields/Edit/FileField.svelte";
  import LocationGoogleField from "../Fields/Edit/LocationGoogleField.svelte";
  import LowLevelDateYearField from "../Fields/Edit/LowLevelDateYearField.svelte";
  import PointField from "../Fields/Edit/PointField.svelte";
  import Overlay from "../Overlay.svelte";

  export let model = "location";
  export let modelName = "Location";
  export let locations: Location[] = [];
  export let country: Country;

  let activeFeatureGroup: GeoJSON;
  let hoverLocationID: string;
  let activeLocationID: string;
  let bigmap: LMap;
  let showAddAreaOverlay = false;
  let toAddArea = { file: undefined, area: "" };

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
  const geojsonOptions = {
    onEachFeature: (feature: Feature, layer: Layer) => {
      // highlight location in list on map-hover
      layer.addEventListener(
        "mouseover",
        () => (hoverLocationID = feature.properties?.id)
      );
      layer.addEventListener("mouseout", () => (hoverLocationID = null));

      if (feature.geometry.type === "Point") {
        layer.addEventListener("click", () => {
          activeLocationID = locations.find((l) => l.id === feature.properties?.id)?.id;
        });
      } else {
        // _addPropertiesPopup(layer, feature);
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
    // console.log(fg);
    // fg.on("pm:update", _featuresChanged);
    // fg.on("pm:dragend", _featuresChanged);
    // fg.on("pm:rotateend", _featuresChanged);
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
      // bigmap?.pm?.removeControls();
      return;
    }
    activeLocationID = location.id;

    if (!locationFGs.get(activeLocationID)) _addNewLayerGroup(activeLocationID);
    activeFeatureGroup = locationFGs.get(activeLocationID);
    // console.log(activeFeatureGroup);

    // let drawMarker = true;
    // activeFeatureGroup.eachLayer((l) => {
    //   if (l.feature.geometry.type === "Point") drawMarker = false;
    // });

    // bigmap?.pm?.setGlobalOptions({ layerGroup: activeFeatureGroup });
    // bigmap?.pm?.addControls({ ...geoman_opts, drawMarker });

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

  const onLocationAreaHover = (loc) => {
    console.log(loc);
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
              ? 'border-orange-300'
              : 'border-white'}"
          >
            <h3 on:click={() => onActivateLocation(loc)}>
              {index + 1}. {$_(modelName)}
              <small class="text-sm text-gray-500">#{loc.id}</small>
              <TrashIcon
                class="w-6 h-6 text-red-600 float-right cursor-pointer"
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
      <div class="min-h-[52rem] w-full lg:w-2/3">
        <BigMap
          containerClass="min-h-[50%] h-[50%] mt-5"
          options={{ center: [0, 0] }}
          on:ready={onMapReady}
        />
        <div>
          {#if activeLocationID}
            <div>{$_("Areas")}</div>
            <table>
              <thead>
                <tr>
                  <th>{$_("Current")}</th>
                  <th>{$_("Date")}</th>
                  <th>{$_("Type")}</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {#each locations.find((l) => l.id === activeLocationID)?.areas?.features ?? [] as feat}
                  <tr
                    on:mouseover={() => onLocationAreaHover(feat)}
                    on:focus={() => onLocationAreaHover(feat)}
                    class="px-1"
                  >
                    <td class="text-center px-1">
                      <input type="checkbox" bind:checked={feat.properties.current} />
                    </td>
                    <td class="px-1">
                      <LowLevelDateYearField bind:value={feat.properties.date} />
                    </td>
                    <td class="px-1">
                      <select bind:value={feat.properties.type} class="inpt w-auto">
                        <option value="contract_area">{$_("Contract area")}</option>
                        <option value="intended_area">{$_("Intended area")}</option>
                        <option value="production_area">{$_("Production area")}</option>
                      </select>
                    </td>
                    <td class="px-2">
                      <TrashIcon
                        class="w-6 h-6 text-red-600 float-right cursor-pointer"
                      />
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>

            <div class="mt-4">
              <button
                type="button"
                class="btn btn-slim btn-secondary flex justify-center items-center"
                on:click={() => (showAddAreaOverlay = true)}
              >
                <PlusIcon />
                {$_("Add")}
              </button>
            </div>
          {/if}
        </div>
      </div>
    </section>
  {/if}
</form>

<Overlay bind:visible={showAddAreaOverlay} title={$_("Add GeoJSON")}>
  <div class="mb-2 font-bold">{$_("File")}</div>
  <FileField
    bind:value={toAddArea.file}
    uploadFunction={() => {}}
    accept=".geojson,application/geo+json,application/json"
  />

  <select bind:value={toAddArea.type} class="inpt w-auto">
    <option value="contract_area">{$_("Contract area")}</option>
    <option value="intended_area">{$_("Intended area")}</option>
    <option value="production_area">{$_("Production area")}</option>
  </select>

  <div class="block mt-6 text-right flex items-center">
    <button type="button" class="btn btn-primary"
      ><PlusIcon /> {$_("Add GeoJSON")}</button
    >
  </div>
</Overlay>
