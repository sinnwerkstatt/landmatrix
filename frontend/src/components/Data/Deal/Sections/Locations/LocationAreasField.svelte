<script lang="ts">
  import { Feature, type Map } from "ol"
  import { GeoJSON } from "ol/format"
  import { MultiPolygon, Point } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { Vector as VectorSource } from "ol/source"
  import { getArea } from "ol/sphere"
  import { Fill, Stroke, Style } from "ol/style"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import { areaChoices, createLabels } from "$lib/fieldChoices"
  import type { components } from "$lib/openAPI"

  import { createPolygonTooltipOverlay } from "$components/Data/Deal/Sections/Locations/locations.js"
  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import {
    dateCurrentFormat,
    formatArea,
  } from "$components/Fields/Display2/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"

  import { AREA_TYPE_COLOR_MAP } from "./locations"

  interface Props {
    map: Map
    areas: components["schemas"]["LocationArea"][]
    fieldname: string
    label?: string
    wrapperClass?: string
    labelClass?: string
    valueClass?: string
    isSelectedEntry: boolean
  }

  let {
    map,
    areas,
    fieldname,
    label = "",
    wrapperClass = WRAPPER_CLASS,
    labelClass = LABEL_CLASS,
    valueClass = VALUE_CLASS,
    isSelectedEntry,
  }: Props = $props()

  const readOpts = { dataProjection: "EPSG:4326", featureProjection: "EPSG:3857" }
  const polygonVectorSource = new VectorSource()

  let visibleMap: { [id: string]: boolean } | undefined = $state()
  $effect(() => {
    visibleMap = areas.reduce((acc, value) => ({ ...acc, [value.nid]: true }), {})
  })

  let hoverMapID: string | undefined = $state()

  const updateHoverMapState = async (_hMapID?: string) => {
    let haveHit = false
    if (_hMapID)
      polygonVectorSource.forEachFeature(ft => {
        const prps = ft.getProperties()
        if (prps.nid === _hMapID) {
          haveHit = true
          createPolygonTooltipOverlay(ft as Feature<MultiPolygon>).then(newOverlay => {
            map.addOverlay(newOverlay)
            map.getOverlays().forEach(overlay => {
              if (overlay !== newOverlay) map!.removeOverlay(overlay)
            })
          })
        }
      })
    if (!haveHit) {
      map!.getOverlays().forEach(overlay => map!.removeOverlay(overlay))
    }
  }
  $effect(() => {
    updateHoverMapState(hoverMapID)
  })

  const areaFeatures = $derived.by(() => {
    const _areaFeatures = []
    for (const area of areas) {
      if (visibleMap?.[area.nid] === false) continue
      const areaFeat = new GeoJSON().readFeature(area.area, readOpts) as Feature
      areaFeat.setProperties({
        nid: area.nid,
        type: area.type,
        date: area.date ?? "",
        current: !!area.current,
        visible: true,
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

  $effect(() => {
    polygonVectorSource.clear()

    if (areaFeatures.length) {
      polygonVectorSource.addFeatures(areaFeatures)
      // map.getView().fit(polygonVectorSource.getExtent(), {
      //   padding: [150, 150, 150, 150],
      //   maxZoom: 13,
      // })
    }
  })

  onMount(() => {
    map.addLayer(new VectorLayer({ source: polygonVectorSource }))

    map.on("pointermove", evt => {
      const feature = map!.forEachFeatureAtPixel(
        evt.pixel,
        feature => feature as Feature<Point>,
      )

      hoverMapID =
        feature && polygonVectorSource.hasFeature(feature)
          ? feature.getProperties().nid
          : undefined
    })
  })

  let areaTypeLabels = $derived(
    createLabels<components["schemas"]["LocationAreaTypeEnum"]>($areaChoices.type),
  )

  let createAreaDisplay = $derived(
    (area: components["schemas"]["LocationArea"]): string => {
      const typeDisplay = areaTypeLabels[area.type]

      const areaFeat = (
        new GeoJSON().readFeature(area.area, readOpts) as Feature
      ).getGeometry()

      const areaDisplay = areaFeat
        ? `${formatArea(getArea(areaFeat))} ${$_("ha")}`
        : "--"
      const dateCurrentDisplay = dateCurrentFormat(area)

      return `${typeDisplay} (${areaDisplay}) ${dateCurrentDisplay}`
    },
  )
</script>

{#if areas.length > 0 && visibleMap}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}

    <div class={valueClass}>
      <ul class="flex flex-col gap-1">
        {#each areas as area (area.nid)}
          {@const inputName = "area-visibility-toggle"}
          {@const inputId = `${inputName}-${area.nid}`}

          <li
            class={twMerge(
              "inline-flex p-0.5",
              area.current ? "font-bold" : "",
              hoverMapID === area.nid ? "text-gray-400" : "",
            )}
            onmouseenter={() => (hoverMapID = area.nid)}
            onmouseleave={() => (hoverMapID = undefined)}
            style:--color={AREA_TYPE_COLOR_MAP[area.type]}
          >
            <input
              class="peer appearance-none"
              id={inputId}
              name={inputName}
              type="checkbox"
              onclick={e => {
                e.preventDefault()
                if (!visibleMap) return
                visibleMap[area.nid] = !visibleMap[area.nid]
              }}
            />
            <label
              for={inputId}
              class="inline-flex cursor-pointer peer-focus-visible:outline"
              title={(visibleMap[area.nid] ? $_("Hide") : $_("Show")) +
                " " +
                $_("area")}
            >
              <span class="inline-flex w-fit">
                {#if visibleMap[area.nid]}
                  <EyeIcon class="mr-1 h-5 w-5" />
                {:else}
                  <EyeSlashIcon class="mr-1 h-5 w-5" />
                {/if}
              </span>
              {createAreaDisplay(area)}
            </label>
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}

<!--<style lang="postcss">-->
<!--  .colored {-->
<!--    /*color: var(&#45;&#45;color, black);*/-->
<!--    /*background-color: var(&#45;&#45;color);*/-->
<!--    @apply text-gray-400;-->
<!--  }-->
<!--</style>-->
