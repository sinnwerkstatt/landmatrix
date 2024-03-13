<script lang="ts">
  import type { FeatureCollection, GeoJsonObject, MultiPolygon, Polygon } from "geojson"
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores"
  import type { Area, AreaType } from "$lib/types/newtypes"
  import { validate } from "$lib/utils/geojsonValidation"
  import { AREA_TYPE_COLOR_MAP, AREA_TYPES } from "$lib/utils/location"

  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let areas: Area[]

  let selectedAreaType: AreaType = "production_area"

  let areasOfType: Area[]
  $: areasOfType = areas.filter(a => a.type === selectedAreaType)

  let currentGroup: number
  $: currentGroup = areasOfType.findIndex(a => a.current)

  let showAddAreaOverlay = false
  let toAddFiles: FileList | undefined

  const uploadFiles = (): void => {
    const reader = new FileReader()

    reader.addEventListener("load", event => {
      const geoJsonObject: GeoJsonObject = JSON.parse(event.target?.result as string)

      try {
        validate(geoJsonObject)
      } catch (e) {
        window.alert((e as Error).message)
        return
      }

      const feature = (geoJsonObject as FeatureCollection<Polygon | MultiPolygon>)
        .features[0]

      areas = [
        ...areas,
        {
          id: null,
          type: selectedAreaType,
          current: !areasOfType.some(a => a.current),
          date: "",
          area: feature.geometry,
        },
      ]

      showAddAreaOverlay = false
    })

    if (toAddFiles) {
      reader.readAsText(toAddFiles[0])
    }
  }

  const updateCurrent = (areaType: AreaType, index: number) => {
    areas = [
      ...areas.filter(a => a.type !== areaType),
      ...areas
        .filter(a => a.type === areaType)
        .map((a, i) => ({ ...a, current: index === i })),
    ]
  }

  const deleteArea = (areaType: AreaType, index: number) => {
    if (confirm($_("Delete area?"))) {
      areas = [
        ...areas.filter(a => a.type !== areaType),
        ...areas.filter((a, i) => a.type === areaType && i !== index),
      ]
    }
  }
</script>

<ol class="flex justify-between gap-3 p-2">
  {#each AREA_TYPES as areaType}
    <li>
      <button
        class="btn btn-flat colored"
        class:is-selected={selectedAreaType === areaType}
        style:--color={AREA_TYPE_COLOR_MAP[areaType]}
        on:click|preventDefault={() => (selectedAreaType = areaType)}
      >
        {$areaTypeMap[areaType]}
      </button>
    </li>
  {/each}
</ol>

<div class="m-0.5">
  <table class="w-full">
    <thead class="mb-5">
      <tr>
        <th class="w-1/12 font-normal">{$_("Info")}</th>
        <th class="w-2/12 font-normal">{$_("Current")}</th>
        <th class="w-3/12 font-normal">{$_("Date")}</th>
        <th class="w-5/12 font-normal">{$_("Type")}</th>
        <th class="w-1/12 font-normal">{$_("Delete")}</th>
      </tr>
    </thead>
    <tbody>
      {#each areasOfType as area, i}
        <tr class="text-left">
          <td class="px-1">
            <EyeSlashIcon class="h-5 w-5" />
            <!--{formatArea(turf.area(area.area)) + " " + $_("ha")}-->
          </td>
          <td class="px-1" on:click={() => updateCurrent(selectedAreaType, i)}>
            <input
              type="radio"
              bind:group={currentGroup}
              value={i}
              name="{selectedAreaType}_current"
              required
            />
          </td>
          <td class="px-1">
            <LowLevelDateYearField bind:value={area.date} name="area_{area.id}" />
          </td>
          <td class="px-1">
            <select
              bind:value={area.type}
              on:change
              name="area_{area.id}_type"
              class="inpt w-auto"
            >
              {#each AREA_TYPES as areaType}
                <option value={areaType}>{$areaTypeMap[areaType]}</option>
              {/each}
            </select>
          </td>
          <td class="px-1">
            <button type="button" on:click={() => deleteArea(selectedAreaType, i)}>
              <TrashIcon class="h-5 w-5 text-red-600" />
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<button
  class="btn btn-flat btn-secondary flex items-center"
  on:click={() => (showAddAreaOverlay = true)}
>
  <PlusIcon />
  {$_("Add")}
  {$_("Area")}
</button>

<Overlay
  bind:visible={showAddAreaOverlay}
  title={$_("Add GeoJSON")}
  on:close={() => (toAddFiles = undefined)}
  showSubmit
  on:submit={uploadFiles}
  submitDisabled={!toAddFiles || !toAddFiles.length}
>
  <label class="flex w-full items-center gap-2">
    <b class="w-1/4">{$_("File")}</b>
    <input
      bind:files={toAddFiles}
      type="file"
      accept=".geojson,application/geo+json,application/json"
    />
  </label>
</Overlay>

<style lang="css">
  .colored.is-selected {
    border-color: var(--color, transparent);
  }
</style>
