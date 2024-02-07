<script lang="ts">
  import * as turf from "@turf/turf"
  import type { FeatureCollection, GeoJsonObject, MultiPolygon, Polygon } from "geojson"
  import { _ } from "svelte-i18n"

  import { areaTypeMap } from "$lib/stores"
  import type { Area, AreaType } from "$lib/types/newtypes"
  import { validate } from "$lib/utils/geojsonValidation"
  import { AREA_TYPES } from "$lib/utils/location"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"
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

      const feature = (geoJsonObject as FeatureCollection<Polygon | MultiPolygon>)
        .features[0]

      areas = [
        ...areas,
        {
          id: null,
          type: "production_area",
          current: !areas.some(a => a.type === "production_area" && a.current),
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

  type CurrentGroupLookup = { [key in AreaType]: number }
  let currentGroupLookup: CurrentGroupLookup

  $: currentGroupLookup = AREA_TYPES.reduce(
    (acc, val) => ({
      ...acc,
      [val]: areas.filter(a => a.type === val).findIndex(a => a.current),
    }),
    {} as CurrentGroupLookup,
  )

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

{#each AREA_TYPES as areaType}
  {@const areasOfType = areas.filter(a => a.type === areaType)}

  {#if areasOfType.length}
    <div class="m-0.5">
      <div class="font-bold">{$areaTypeMap[areaType] + "s:"}</div>
      <table class="w-full">
        <thead>
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
              <td class="px-1" on:click={() => updateCurrent(areaType, i)}>
                <input
                  type="radio"
                  bind:group={currentGroupLookup[areaType]}
                  value={i}
                  name="{areaType}_current"
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
                <button type="button" on:click={() => deleteArea(areaType, i)}>
                  <TrashIcon class="h-5 w-5 text-red-600" />
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <div class="m-0.5 font-bold">
      {$_("No {areaType}s.", {
        values: { areaType: $areaTypeMap[areaType] },
      })}
    </div>
  {/if}
{/each}
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
