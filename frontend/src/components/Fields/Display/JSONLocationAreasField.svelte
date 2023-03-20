<script lang="ts">
  import { _ } from "svelte-i18n"
  import { createEventDispatcher } from "svelte"
  import type { Feature } from "geojson"
  import { area } from "@turf/turf"

  import type { AreaFeatureCollection, AreaType } from "$lib/types/deal"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers.js"
  import type { FormField } from "$components/Fields/fields"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"

  export let value: AreaFeatureCollection
  // svelte-ignore unused-export-let
  export let model
  export let formfield: FormField

  const dispatch = createEventDispatcher()

  let features: Feature[]
  $: features = (value?.features ?? []).map(
    (feature: Feature): Feature => ({
      ...feature,
      properties: {
        ...feature.properties,
        visible: !!feature.properties?.current,
      },
    }),
  )

  const onClick = (index: number) => {
    features = features.map((f, i) => (i === index ? toggleVisibility(f) : f))
    dispatch("toggleVisibility", { index, location: features[0].properties.id })
  }
  const toggleVisibility = (feature: Feature): Feature => ({
    ...feature,
    properties: {
      ...feature.properties,
      visible: !feature.properties?.visible,
    },
  })

  $: getAreaLabel = (areaType: AreaType): string =>
    ({
      production_area: $_("Production"),
      contract_area: $_("Contract"),
      intended_area: $_("Intended"),
    }[areaType])

  const formatArea = (area: number) =>
    (area / 10000)
      .toFixed(2)
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, " ")
</script>

<div data-name={formfield?.name ?? ""}>
  {#each features as feature, index}
    <div class:font-bold={feature.properties.current} class="flex">
      <div on:click={() => onClick(index)} class="cursor-pointer">
        {#if feature.properties.visible}
          <span title="Hide">
            <EyeIcon class="h-5 w-5" />
          </span>
        {:else}
          <span title="Show">
            <EyeSlashIcon class="h-5 w-5" />
          </span>
        {/if}
      </div>
      <span class="px-1">{getAreaLabel(feature.properties.type)}</span>
      <span class="px-1">({formatArea(area(feature))} {$_("ha")})</span>
      <span class="px-1">{dateCurrentFormat(feature.properties)}</span>
    </div>
  {/each}
</div>

<!--<style lang="css">-->
<!--  .contract_area {-->
<!--    color: #ff00ff;-->
<!--  }-->
<!--  .intended_area {-->
<!--    color: #66ff33;-->
<!--  }-->
<!--  .production_area {-->
<!--    color: #ff0000;-->
<!--  }-->
<!--</style>-->
