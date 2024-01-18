<script lang="ts">
  import * as turf from "@turf/turf"
  import type { FeatureCollection, GeoJsonObject } from "geojson"
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores"
  import type { Area, AreaType } from "$lib/types/newtypes"
  import { validate } from "$lib/utils/geojsonValidation"
  import { AREA_TYPES } from "$lib/utils/location"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"
  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let areas: Area[]

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

      const feature = (geoJsonObject as FeatureCollection).features[0]

      console.log("new feature", feature)

      showAddAreaOverlay = false
    })

    if (toAddFiles) {
      reader.readAsText(toAddFiles[0])
    }
  }

  let current: { [key in AreaType]: number | null }
  $: current = {
    contract_area:
      areas.filter(a => a.type === "contract_area").find(a => a.current)?.id ?? null,
    production_area:
      areas.filter(a => a.type === "production_area").find(a => a.current)?.id ?? null,
    intended_area:
      areas.filter(a => a.type === "intended_area").find(a => a.current)?.id ?? null,
  }

  const updateCurrent = (areaType: AreaType, id: number) => {
    areas = areas.map(a => (a.type === areaType ? { ...a, current: a.id === id } : a))
  }
  const deleteArea = (id: number) => {
    if (confirm($_("Delete area?"))) {
      areas = areas.filter(a => a.id !== id)
    }
  }
</script>

<table class="w-full">
  <thead class="font-normal">
    <tr class="font-normal">
      <th class="w-3/12">{$_("Info")}</th>
      <th class="w-2/12">{$_("Current")}</th>
      <th class="w-3/12">{$_("Date")}</th>
      <th class="w-3/12">{$_("Type")}</th>
      <th class="w-1/12">{$_("Delete")}</th>
    </tr>
  </thead>
  <tbody>
    {#each AREA_TYPES as areaType}
      {@const areasOfType = areas.filter(a => a.type === areaType)}
      {#each areasOfType as area}
        <tr class="text-left">
          <td class="px-1">
            <EyeSlashIcon class="h-5 w-5" />
            {formatArea(turf.area(area.area)) + " " + $_("ha")}
          </td>
          <td class="px-1" on:click={() => updateCurrent(areaType, area.id)}>
            <input
              type="radio"
              bind:group={current[areaType]}
              value={area.id}
              name="{areaType}_current"
              required={true}
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
          <td class="p-1">
            <button type="button" on:click={() => deleteArea(area.id)}>
              <TrashIcon class="h-5 w-5 text-red-600" />
            </button>
          </td>
        </tr>
      {/each}
      {#if areasOfType.length > 0}
        <tr class="border-b border-black">
          <td colspan="5"></td>
        </tr>
      {/if}
    {/each}
  </tbody>
</table>
<button
  class="btn btn-slim btn-secondary flex items-center"
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
