<script lang="ts">
  import type { FeatureCollection, GeoJsonObject, MultiPolygon, Polygon } from "geojson"
  import type { Map } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { quintOut } from "svelte/easing"
  import { crossfade } from "svelte/transition"

  import { areaTypeMap } from "$lib/stores/maps"
  import type {
    Area,
    AreaFeature,
    AreaFeatureLayer,
    AreaType,
  } from "$lib/types/newtypes"
  import { validate } from "$lib/utils/geojsonValidation"
  import {
    AREA_TYPES,
    areaToFeature,
    createAreaFeaturesLayer,
  } from "$lib/utils/location"

  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import CurrentRadio from "$components/Fields/Edit2/JSONFieldComponents/CurrentRadio.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let map: Map | undefined
  export let areas: Area[]

  export let isSelectedEntry: boolean

  let showAddAreaOverlay = false
  let toAddFiles: FileList | undefined

  let selectedAreaType: AreaType | null = null

  $: currentGroups = AREA_TYPES.reduce(
    (acc, val) => ({
      ...acc,
      [val]: areas.filter(a => a.type === val).findIndex(a => a.current),
    }),
    {},
  ) as { [key in (typeof AREA_TYPES)[number]]: number }

  let features: AreaFeature[]
  let layer: AreaFeatureLayer

  $: features = areas.map(areaToFeature)

  $: if (map && layer) {
    map.removeLayer(layer)
    layer = createAreaFeaturesLayer(features, isSelectedEntry)
    map.addLayer(layer)
  }

  onMount(() => {
    layer = createAreaFeaturesLayer(features, isSelectedEntry)
  })

  onDestroy(() => {
    if (map) {
      map.removeLayer(layer)
    }
  })

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
          type: selectedAreaType!,
          current: !areas.filter(a => a.type === selectedAreaType).some(a => a.current),
          date: "",
          area: feature.geometry,
        },
      ]

      showAddAreaOverlay = false
      toAddFiles = undefined
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

  const [send, receive] = crossfade({
    duration: d => Math.sqrt(d * 200),

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    fallback(node, params) {
      const style = getComputedStyle(node)
      const transform = style.transform === "none" ? "" : style.transform

      return {
        duration: 600,
        easing: quintOut,
        css: t => `
				transform: ${transform} scale(${t});
				opacity: ${t}
			`,
      }
    },
  })

  // TODO: Use index, because new features don't have an id yet
  // OR: Add nanoid to areas
  $: toggleVisibility = (id: number) => {
    features = features.map(f =>
      f.properties.id === id
        ? {
            ...f,
            properties: {
              ...f.properties,
              visible: !f.properties.visible,
            },
          }
        : f,
    )
  }
</script>

<div class="flex flex-col gap-2">
  {#each AREA_TYPES as areaType}
    {@const areasOfType = areas.filter(a => a.type === areaType)}

    <div>
      <Label2 value={$areaTypeMap[areaType]} class="mb-4 w-full font-semibold" />
      <div class="grid gap-2 lg:grid-cols-2">
        {#each areasOfType as val, i}
          {@const feature = features.find(f => f.properties.id === val.id)}

          <div
            class:border-violet-400={val.current}
            class={cardClass}
            in:receive={{ key: val.id }}
            out:send={{ key: val.id }}
          >
            <Date bind:value={val.date} name="area_{val.id}" />
            <CurrentRadio
              bind:group={currentGroups[areaType]}
              name="{areaType}_current"
              required={areasOfType.length > 0 && currentGroups[areaType] < 0}
              disabled={!val.area}
              value={i}
              on:change={() => updateCurrent(areaType, i)}
            />

            <label class={labelClass} for="area_{val.id}_type">
              {$_("Type")}
              <select
                bind:value={val.type}
                on:change
                name="area_{val.id}_type"
                class="inpt w-auto"
              >
                {#each AREA_TYPES as areaType}
                  <option value={areaType}>{$areaTypeMap[areaType]}</option>
                {/each}
              </select>
            </label>

            <div class="flex justify-between">
              <button
                type="button"
                title={feature?.properties.visible ? $_("Hide") : $_("Show")}
                on:click={() => toggleVisibility(val.id)}
              >
                {#if feature?.properties.visible}
                  <EyeSlashIcon class="h-5 w-5" />
                {:else}
                  <EyeIcon class="h-5 w-5" />
                {/if}
              </button>
              <button
                type="button"
                on:click={() => deleteArea(areaType, i)}
                title={$_("Remove entry")}
              >
                <TrashIcon
                  class="h-5 w-5 {!(areasOfType.length <= 1)
                    ? 'text-red-600'
                    : 'text-gray-200'}"
                />
              </button>
            </div>
          </div>
        {/each}

        <AddButton
          on:click={() => {
            showAddAreaOverlay = true
            selectedAreaType = areaType
          }}
        />
      </div>
    </div>
  {/each}
</div>

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
