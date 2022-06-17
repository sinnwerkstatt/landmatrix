<script lang="ts">
  import type { Feature } from "geojson";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import type { Location } from "$lib/types/deal";
  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import Overlay from "$components/Overlay.svelte";
  import MinusIcon from "../icons/MinusIcon.svelte";

  const dispatch = createEventDispatcher();

  type Area = "production_area" | "contract_area" | "intended_area";

  export let areaType: Area;
  export let locations: Location[];
  export let activeLocationID: string;
  export let currentHoverFeature: Feature | null;

  let showAddAreaOverlay = false;
  let toAddFiles;

  $: title = {
    production_area: $_("Production areas"),
    contract_area: $_("Contract areas"),
    intended_area: $_("Intended areas"),
  }[areaType];

  $: areaFeatures =
    locations
      .find((loc) => loc.id === activeLocationID)
      .areas?.features?.filter((feature) => feature.properties.type === areaType) ?? [];

  $: current = areaFeatures.findIndex((feature) => feature.properties.current);

  const onLocationAreaHover = (feature) => {
    currentHoverFeature = feature;
    dispatch("hoverFeature");
  };
  const onLocationAreaMouseOut = () => {
    currentHoverFeature = null;
    dispatch("hoverFeature");
  };

  function uploadFiles() {
    const reader = new FileReader();
    reader.addEventListener("load", (event) => {
      let result = JSON.parse(event.target?.result as string);

      const feats = result.features.map((f: Feature) => ({
        ...f,
        properties: { ...f.properties, type: areaType },
      }));

      let actAreas = locations.find((l) => l.id === activeLocationID).areas;
      actAreas.features = [...actAreas.features, ...feats];
      locations = locations;
      dispatch("change");
      showAddAreaOverlay = false;
    });
    reader.readAsText(toAddFiles[0]);
  }

  function removeFeature(e) {
    let actAreas = locations.find((l) => l.id === activeLocationID).areas;
    actAreas.features = actAreas.features.filter((f) => f !== e);
    locations = locations;
    dispatch("change");
  }

  function updateCurrent(index: number) {
    const activeIndex = locations.findIndex((l) => l.id === activeLocationID);

    locations[activeIndex] = updateCurrentForLocation(locations[activeIndex], index);
    locations = locations;
  }

  function updateCurrentForLocation(location: Location, index: number): Location {
    let otherFeatures = location.areas.features.filter(
      (f) => f.properties.type !== areaType
    );

    let areaFeatures = location.areas.features
      .filter((f) => f.properties.type === areaType)
      .map((feature, i) => ({
        ...feature,
        properties: {
          ...feature.properties,
          current: i === index ? true : undefined,
        },
      }));

    return {
      ...location,
      areas: { ...location.areas, features: [...otherFeatures, ...areaFeatures] },
    } as Location;
  }
</script>

<div class="grid grid-cols-10 justify-between my-3">
  <div class="pr-2 col-span-2">
    <div class="text-lg font-medium">{title}</div>
    {#if areaFeatures.length === 0}
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
  <table class="flex-auto col-span-8">
    <thead>
      {#if areaFeatures.length > 0}
        <tr>
          <th class="font-normal">{$_("Current")}</th>
          <th class="font-normal">{$_("Date")}</th>
          <th class="font-normal">{$_("Type")}</th>
          <th />
        </tr>
      {/if}
    </thead>
    <tbody>
      {#each areaFeatures as feat, i}
        <tr
          on:mouseover={() => onLocationAreaHover(feat)}
          on:mouseout={() => onLocationAreaMouseOut()}
          class="px-1 {feat === currentHoverFeature ? 'border border-orange-400' : ''}"
        >
          <td class="text-center px-1" on:click={() => updateCurrent(i)}>
            <input
              type="radio"
              bind:group={current}
              value={i}
              name="{areaType}_current"
            />
          </td>
          <td class="px-1">
            <LowLevelDateYearField
              bind:value={feat.properties.date}
              emitUndefinedOnEmpty
            />
          </td>
          <td class="px-1">
            <select bind:value={feat.properties.type} on:change class="inpt w-auto">
              <option value="production_area">{$_("Production area")}</option>
              <option value="contract_area">{$_("Contract area")}</option>
              <option value="intended_area">{$_("Intended area")}</option>
            </select>
          </td>
          <td class="p-1">
            <button type="button" on:click={() => (showAddAreaOverlay = true)}>
              <PlusIcon class="w-5 h-5 text-black" />
            </button>
            <button
              type="button"
              disabled={areaFeatures.length <= 1}
              on:click={() => removeFeature(feat)}
            >
              <MinusIcon class="w-5 h-5 text-red-600" />
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
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
