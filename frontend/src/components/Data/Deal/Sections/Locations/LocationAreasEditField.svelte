<script lang="ts">
  import type {
    FeatureCollection,
    GeoJsonObject,
    MultiPolygon as MultiPolygonType,
  } from "geojson"
  import { Overlay as OLOverlay, type Feature, type Map } from "ol"
  import { GeoJSON } from "ol/format"
  import { type MultiPolygon } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { Vector as VectorSource } from "ol/source"
  import { Fill, Stroke, Style } from "ol/style"
  import { mount, onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { quintOut } from "svelte/easing"
  import { crossfade } from "svelte/transition"
  import { twMerge } from "tailwind-merge"

  import { areaChoices, createLabels } from "$lib/fieldChoices"
  import { newNanoid } from "$lib/helpers"
  import type { components } from "$lib/openAPI"
  import { validate } from "$lib/utils/geojsonValidation"

  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import { fitMapToFeatures } from "$components/Map/mapstuff.svelte.js"
  import Overlay from "$components/Overlay.svelte"

  import LocationAreaTooltip from "./LocationAreaTooltip.svelte"
  import { AREA_TYPE_COLOR_MAP, AREA_TYPES } from "./locations"

  interface Props {
    map: Map
    areas: components["schemas"]["LocationArea"][]
    isSelectedEntry: boolean
    onchange?: () => void
  }

  let { map, areas = $bindable(), isSelectedEntry, onchange }: Props = $props()

  const readOpts = { dataProjection: "EPSG:4326", featureProjection: "EPSG:3857" }
  const polygonVectorSource = new VectorSource()

  let showAddAreaOverlay = $state(false)
  let toAddFiles: FileList | undefined = $state()

  let selectedAreaType: components["schemas"]["LocationAreaTypeEnum"] | null =
    $state(null)

  let areaTypeLabels = $derived(
    createLabels<components["schemas"]["LocationAreaTypeEnum"]>($areaChoices.type),
  )

  const createCurrentGroups = () =>
    AREA_TYPES.reduce(
      (acc, val) => ({
        ...acc,
        [val]: areas.filter(a => a.type === val).findIndex(a => a.current),
      }),
      {},
    ) as { [key in components["schemas"]["LocationAreaTypeEnum"]]: number }

  let currentGroups = $state(createCurrentGroups())

  $effect(() => {
    currentGroups = createCurrentGroups()
  })

  async function createPolygonOverlay(feature: Feature<MultiPolygon>) {
    const overlayContainerDiv = document.createElement("div")
    mount(LocationAreaTooltip, { target: overlayContainerDiv, props: { feature } })
    return new OLOverlay({
      element: overlayContainerDiv,
      position: feature.getGeometry()?.getFirstCoordinate(),
      positioning: "bottom-center",
      offset: [-30, -30, -30, -30],
      autoPan: { animation: { duration: 300 } },
    })
  }

  let hiddenMap: { [id: string]: boolean } = $state({})

  const areaFeatures = $derived.by(() => {
    const _areaFeatures = []
    for (const area of areas) {
      if (hiddenMap?.[area.nid] === true) continue
      const areaFeat = new GeoJSON().readFeature(area.area, readOpts) as Feature
      areaFeat.setProperties({
        nid: area.nid,
        type: area.type,
        date: area.date ?? "",
        current: !!area.current,
      })

      areaFeat.setStyle(
        new Style({
          stroke: new Stroke({ lineDash: [5, 5], color: "black", width: 1.5 }),
          fill: new Fill({
            color: isSelectedEntry
              ? `${AREA_TYPE_COLOR_MAP[area.type]}99`
              : "#7A7A7A99",
          }),
        }),
      )
      _areaFeatures.push(areaFeat)
    }
    return _areaFeatures
  })

  onMount(() => {
    map.addLayer(new VectorLayer({ source: polygonVectorSource }))

    map.on("pointermove", evt => {
      const feature = map!.forEachFeatureAtPixel(
        evt.pixel,
        feature => feature as Feature<MultiPolygon>,
      )

      if (feature && polygonVectorSource.hasFeature(feature)) {
        createPolygonOverlay(feature as Feature<MultiPolygon>).then(newOverlay => {
          map.addOverlay(newOverlay)
          map.getOverlays().forEach(overlay => {
            if (overlay !== newOverlay) map!.removeOverlay(overlay)
          })
        })
      } else {
        map.getOverlays().forEach(overlay => map!.removeOverlay(overlay))
      }
    })
  })

  onDestroy(() => {
    polygonVectorSource.clear()
  })

  $effect(() => {
    polygonVectorSource.clear()
    if (areaFeatures.length) {
      polygonVectorSource.addFeatures(areaFeatures)
      fitMapToFeatures(map)
    }
  })

  const uploadFiles = (e: SubmitEvent): void => {
    e.preventDefault()
    const reader = new FileReader()

    reader.addEventListener("load", event => {
      const geoJsonObject: GeoJsonObject = JSON.parse(event.target?.result as string)

      try {
        validate(geoJsonObject)
      } catch (e) {
        window.alert((e as Error).message)
        return
      }

      const feature = (geoJsonObject as FeatureCollection<MultiPolygonType>).features[0]

      const existingIds = areas.map(entry => entry.nid)
      areas = [
        ...areas,
        {
          id: null!,
          nid: newNanoid(existingIds),
          type: selectedAreaType!,
          current: !areas.filter(a => a.type === selectedAreaType).some(a => a.current),
          area: feature.geometry,
          date: "",
        },
      ]

      showAddAreaOverlay = false
      toAddFiles = undefined
      onchange?.()
    })

    if (toAddFiles) {
      reader.readAsText(toAddFiles[0])
    }
  }

  const updateCurrent = (
    areaType: components["schemas"]["LocationAreaTypeEnum"],
    nid: string,
  ) => {
    areas = [
      ...areas.filter(a => a.type !== areaType),
      ...areas
        .filter(a => a.type === areaType)
        .map(a => ({ ...a, current: a.nid === nid })),
    ]
    onchange?.()
  }

  const deleteArea = (nid: string) => {
    if (confirm($_("Delete area?"))) {
      areas = areas.filter(a => a.nid !== nid)
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
</script>

<div class="flex flex-col gap-2">
  {#each AREA_TYPES as areaType}
    {@const areasOfType = areas.filter(a => a.type === areaType)}

    <div>
      <Label2 value={areaTypeLabels[areaType]} class="mb-4 w-full font-semibold" />
      <div class="grid gap-2 lg:grid-cols-2">
        {#each areasOfType as val, index}
          {@const isVisible = !hiddenMap[val.nid]}

          <div
            class:border-violet-400={val.current}
            class={cardClass}
            in:receive={{ key: val.nid }}
            out:send={{ key: val.nid }}
          >
            <Date bind:value={val.date} name="area_{val.nid}_date" {onchange} />

            <label class={labelClass}>
              {$_("Current")}
              <input
                type="radio"
                class={twMerge(
                  "size-5 accent-violet-400 ",
                  areasOfType.length > 0 && currentGroups[areaType] < 0
                    ? "ring-2 ring-red-600"
                    : "",
                )}
                bind:group={currentGroups[areaType]}
                name="{areaType}_current"
                required={areasOfType.length > 0 && currentGroups[areaType] < 0}
                disabled={!val.area}
                value={index}
                onchange={() => updateCurrent(areaType, val.nid)}
              />
            </label>

            <label class={labelClass} for="area_{val.nid}_type">
              {$_("Type")}
              <select
                bind:value={val.type}
                {onchange}
                name="area_{val.nid}_type"
                class="inpt w-auto"
              >
                {#each AREA_TYPES as areaType}
                  <option value={areaType}>{areaTypeLabels[areaType]}</option>
                {/each}
              </select>
            </label>

            <div class="flex justify-between">
              <button
                type="button"
                title={isVisible ? $_("Hide") : $_("Show")}
                onclick={() => (hiddenMap[val.nid] = !hiddenMap[val.nid])}
              >
                {#if isVisible}
                  <EyeSlashIcon class="h-5 w-5" />
                {:else}
                  <EyeIcon class="h-5 w-5" />
                {/if}
              </button>
              <button
                type="button"
                onclick={() => deleteArea(val.nid)}
                title={$_("Remove entry")}
              >
                <TrashIcon class="h-5 w-5 text-red-600" />
              </button>
            </div>
          </div>
        {/each}

        <AddButton
          onclick={() => {
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
  onclose={() => (toAddFiles = undefined)}
  showSubmit
  onsubmit={uploadFiles}
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
