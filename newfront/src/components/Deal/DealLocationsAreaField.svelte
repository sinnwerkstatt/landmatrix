<script lang="ts">
  import type { GeoJSON } from "geojson";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import type { Area, AreaFeature, Location } from "$lib/types/deal";
  import {
    getFeatures,
    setCurrentProperty,
    setFeatures,
    setTypeProperty,
  } from "$components/Deal/dealLocationAreaFeatures";
  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte";
  import EyeIcon from "$components/icons/EyeIcon.svelte";
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import TrashIcon from "$components/icons/TrashIcon.svelte";
  import Overlay from "$components/Overlay.svelte";

  const dispatch = createEventDispatcher();

  export let areaType: Area;
  export let activeLocationID: string;
  export let locations: Location[];
  export let currentHoverFeature: AreaFeature | null;
  export let hiddenFeatures: AreaFeature[];

  let showAddAreaOverlay = false;
  let toAddFiles;

  $: title = {
    production_area: $_("Production areas"),
    contract_area: $_("Contract areas"),
    intended_area: $_("Intended areas"),
  }[areaType];

  $: activeLocation = locations.find((location) => location.id === activeLocationID);

  // bind area type
  const getAreaFeatures = (location: Location) => getFeatures(areaType, location);
  const hasAreaFeatures = (location: Location) => getAreaFeatures(location).length > 0;
  const setAreaFeatures = (location: Location, features: AreaFeature[]) => {
    setFeatures(areaType, location, features);

    // signal update
    locations = locations;
    dispatch("change");
  };

  $: current = getAreaFeatures(activeLocation).findIndex(
    (feature) => feature.properties.current
  );

  function uploadFiles() {
    const reader = new FileReader();

    reader.addEventListener("load", (event) => {
      const geoJsonObject: GeoJSON = JSON.parse(event.target?.result as string);

      let features = getAreaFeatures(activeLocation);

      switch (geoJsonObject.type) {
        case "Feature":
          features = [...features, setTypeProperty(areaType)(geoJsonObject)];
          break;
        case "FeatureCollection":
          features = [
            ...features,
            ...geoJsonObject.features.map(setTypeProperty(areaType)),
          ];
          break;
        default:
          console.error("Unsupported GeoJsonType");
      }

      setAreaFeatures(activeLocation, features);
      showAddAreaOverlay = false;
    });

    reader.readAsText(toAddFiles[0]);
  }

  const toggleVisibility = (feature: AreaFeature) => {
    hiddenFeatures = hiddenFeatures.includes(feature)
      ? hiddenFeatures.filter((f) => f !== feature)
      : [...hiddenFeatures, feature];
  };

  function removeFeature(feature: AreaFeature) {
    const remainingFeatures = getAreaFeatures(activeLocation).filter(
      (f) => f !== feature
    );

    setAreaFeatures(activeLocation, remainingFeatures);
  }

  function updateCurrent(index: number) {
    const updatedFeatures: AreaFeature[] = getAreaFeatures(activeLocation).map(
      setCurrentProperty(index)
    );

    setAreaFeatures(activeLocation, updatedFeatures);
  }
</script>

<div class="grid grid-cols-10 justify-between my-3">
  <div class="pr-2 col-span-2">
    <div class="text-lg font-medium">{title}</div>
  </div>
  {#if hasAreaFeatures(activeLocation)}
    <table class="flex-auto col-span-8">
      <thead>
        <tr>
          <th class="font-normal" />
          <th class="font-normal">{$_("Current")}</th>
          <th class="font-normal">{$_("Date")}</th>
          <th class="font-normal">{$_("Type")}</th>
          <th class="font-normal" />
        </tr>
      </thead>
      <tbody>
        {#each getAreaFeatures(activeLocation) as feat, i}
          <tr
            on:mouseover={() => (currentHoverFeature = feat)}
            on:focus={() => (currentHoverFeature = feat)}
            on:mouseout={() => (currentHoverFeature = null)}
            on:blur={() => (currentHoverFeature = null)}
            class="px-1
            {feat === currentHoverFeature ? 'border border-4 border-orange-400' : ''}
            {hiddenFeatures.includes(feat) ? 'bg-gray-200' : ''}"
          >
            <td class="text-center px-1" on:click={() => toggleVisibility(feat)}>
              {#if hiddenFeatures.includes(feat)}
                <div title="Show">
                  <EyeSlashIcon class="h-5 w-5" />
                </div>
              {:else}
                <div title="Hide"><EyeIcon class="h-5 w-5" /></div>
              {/if}
            </td>
            <td class="text-center px-1" on:click={() => updateCurrent(i)}>
              <input
                type="radio"
                bind:group={current}
                value={i}
                name="{areaType}_{i}_current"
                required={current === -1}
              />
            </td>
            <td class="px-1">
              <LowLevelDateYearField
                bind:value={feat.properties.date}
                name="{areaType}_{i}_year"
                required
                emitUndefinedOnEmpty
              />
            </td>
            <td class="px-1">
              <select
                bind:value={feat.properties.type}
                on:change
                name="{areaType}_{i}_type"
                class="inpt w-auto"
              >
                <option value="production_area">{$_("Production area")}</option>
                <option value="contract_area">{$_("Contract area")}</option>
                <option value="intended_area">{$_("Intended area")}</option>
              </select>
            </td>
            <td class="p-1">
              <button
                type="button"
                on:click={() => confirm($_("Delete feature?")) && removeFeature(feat)}
              >
                <TrashIcon class="w-5 h-5 text-red-600" />
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <button
      type="button"
      class="btn btn-slim btn-secondary flex justify-center items-center"
      on:click={() => (showAddAreaOverlay = true)}
    >
      <PlusIcon />
      {$_("Add")}
    </button>
  {/if}
</div>

<Overlay
  bind:visible={showAddAreaOverlay}
  title={$_("Add GeoJSON")}
  on:close={() => (toAddFiles = undefined)}
>
  <div class="mb-2 font-bold">{$_("File")}</div>
  <input
    bind:files={toAddFiles}
    type="file"
    accept=".geojson,application/geo+json,application/json"
  />

  <!--  <select bind:value={toAddFeature.type} class="inpt w-auto" required>-->
  <!--    <option value>&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</option>-->
  <!--    <option value="production_area">{$_("Production area")}</option>-->
  <!--    <option value="contract_area">{$_("Contract area")}</option>-->
  <!--    <option value="intended_area">{$_("Intended area")}</option>-->
  <!--  </select>-->

  <div class="block mt-6 text-right flex items-center">
    <button
      type="button"
      class="btn btn-primary"
      on:click={uploadFiles}
      disabled={!toAddFiles}
    >
      <PlusIcon />
      {$_("Add GeoJSON")}
    </button>
  </div>
</Overlay>
