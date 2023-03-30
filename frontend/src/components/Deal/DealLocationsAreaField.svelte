<script lang="ts">
  import classNames from "classnames"
  import type { FeatureCollection, GeoJsonObject } from "geojson"
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import type { AreaFeature, AreaType, Location } from "$lib/types/deal"
  import { validate } from "$lib/utils/geojsonValidation"
  import { setProperty, createFeatureCollection } from "$lib/utils/geojsonHelpers"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Overlay from "$components/Overlay.svelte"

  const dispatch = createEventDispatcher()

  export let areaType: AreaType
  export let activeLocationID: string
  export let locations: Location[]
  export let currentHoverFeature: AreaFeature | null
  export let hiddenFeatures: AreaFeature[]

  let showAddAreaOverlay = false
  let toAddFiles: FileList

  $: title = {
    production_area: $_("Production areas"),
    contract_area: $_("Contract areas"),
    intended_area: $_("Intended areas"),
  }[areaType]

  $: activeLocation = locations.find(location => location.id === activeLocationID)
  $: areaFeatures = getFeatures(areaType, activeLocation)
  $: hasAreaFeatures = areaFeatures.length > 0
  $: current = areaFeatures.findIndex(feature => feature.properties.current)

  function getFeatures(areaType: AreaType, location: Location): AreaFeature[] {
    const activeAreas = location.areas ?? createFeatureCollection([])
    const features = activeAreas.features as AreaFeature[]
    return features.filter(
      (feature: AreaFeature) => feature.properties.type === areaType,
    )
  }

  function setAreaFeatures(location: Location, features: AreaFeature[]): void {
    const activeAreas = location.areas ?? createFeatureCollection([])
    const otherFeatures = activeAreas.features.filter(
      (feature: AreaFeature) => feature.properties.type !== areaType,
    )

    activeAreas.features = [...features, ...otherFeatures]
    location.areas = activeAreas.features.length > 0 ? activeAreas : undefined

    // signal update
    locations = locations
    dispatch("change")
  }

  function uploadFiles(): void {
    const reader = new FileReader()

    reader.addEventListener("load", event => {
      const geoJsonObject: GeoJsonObject = JSON.parse(event.target?.result as string)

      try {
        validate(geoJsonObject)
      } catch (e) {
        window.alert((e as Error).message)
        return
      }

      const feature = (geoJsonObject as FeatureCollection).features[0]

      setAreaFeatures(activeLocation, [
        ...areaFeatures,
        setProperty("type", areaType, feature),
      ])

      showAddAreaOverlay = false
    })

    reader.readAsText(toAddFiles[0])
  }

  function toggleVisibility(feature: AreaFeature): void {
    hiddenFeatures = hiddenFeatures.includes(feature)
      ? hiddenFeatures.filter(f => f !== feature)
      : [...hiddenFeatures, feature]
  }

  function removeFeature(feature: AreaFeature): void {
    setAreaFeatures(
      activeLocation,
      areaFeatures.filter(f => f !== feature),
    )
  }

  function updateCurrent(index: number): void {
    setAreaFeatures(
      activeLocation,
      areaFeatures.map((f: AreaFeature, i) =>
        setProperty("current", i === index ? true : undefined, f),
      ),
    )
  }
</script>

<div class="my-3 grid grid-cols-10 justify-between">
  <div class="col-span-2 pr-2">
    <div class="text-lg font-medium">{title}</div>
    <button
      type="button"
      class="btn btn-slim btn-secondary flex items-center justify-center"
      on:click={() => (showAddAreaOverlay = true)}
    >
      <PlusIcon />
      {$_("Add")}
    </button>
  </div>
  {#if hasAreaFeatures}
    <table class="col-span-8 flex-auto">
      <thead>
        <tr>
          <th class="font-normal" />
          <th class="pr-2 text-center font-normal">{$_("Current")}</th>
          <th class="font-normal">{$_("Date")}</th>
          <th class="font-normal">{$_("Type")}</th>
          <th class="font-normal" />
        </tr>
      </thead>
      <tbody>
        {#each areaFeatures as feat, i}
          <tr
            on:mouseover={() => (currentHoverFeature = feat)}
            on:focus={() => (currentHoverFeature = feat)}
            on:mouseout={() => (currentHoverFeature = null)}
            on:blur={() => (currentHoverFeature = null)}
            class={classNames(
              "px-1",
              feat === currentHoverFeature ? "border border-4 border-orange-400" : "",
              hiddenFeatures.includes(feat) ? "bg-gray-200" : "",
            )}
          >
            <td class="px-1 text-center" on:click={() => toggleVisibility(feat)}>
              {#if hiddenFeatures.includes(feat)}
                <div title="Show">
                  <EyeSlashIcon class="h-5 w-5" />
                </div>
              {:else}
                <div title="Hide"><EyeIcon class="h-5 w-5" /></div>
              {/if}
            </td>
            <td class="px-1 text-center" on:click={() => updateCurrent(i)}>
              <input
                type="radio"
                bind:group={current}
                required={hasAreaFeatures}
                value={i}
                name="{areaType}_current"
              />
            </td>
            <td class="px-1">
              <LowLevelDateYearField
                bind:value={feat.properties.date}
                name="{areaType}_{i}_year"
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
                <TrashIcon class="h-5 w-5 text-red-600" />
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>

<Overlay
  bind:visible={showAddAreaOverlay}
  title={$_("Add GeoJSON")}
  on:close={() => (toAddFiles = undefined)}
  showSubmit
  on:submit={uploadFiles}
  submitDisabled={!toAddFiles || !toAddFiles.length}
>
  <div class="flex gap-2">
    <div class="mb-2 font-bold">{$_("File")}</div>
    <input
      bind:files={toAddFiles}
      type="file"
      accept=".geojson,application/geo+json,application/json"
    />
  </div>
</Overlay>
