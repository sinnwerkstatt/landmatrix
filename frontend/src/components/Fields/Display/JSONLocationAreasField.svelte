<script lang="ts">
  import { _ } from "svelte-i18n"
  import { createEventDispatcher } from "svelte"
  import type { FeatureCollection } from "geojson"

  import { areaTypeMap } from "$lib/stores"
  import type { EnhancedAreaFeature } from "$lib/types/deal"

  const dispatch = createEventDispatcher<{
    toggleVisibility: { locationId: string; featureId: string }
  }>()

  import { dateCurrentFormat, formatArea } from "$components/Fields/Display/jsonHelpers"
  import type { FormField } from "$components/Fields/fields"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"

  export let value: FeatureCollection
  export const model: "deal" | "investor" = "deal"
  export let formfield: FormField

  let features: EnhancedAreaFeature[]
  $: features = value?.features ?? []

  const toggleVisibility = (featureId: string) => {
    const locationId: string = features.find(f => f.id === featureId).properties.id
    dispatch("toggleVisibility", { locationId, featureId })
  }
</script>

<ul>
  {#each features as feature}
    <li class:font-bold={feature.properties.current} class="flex">
      <button
        class="flex cursor-pointer p-1 text-left"
        on:click={() => toggleVisibility(feature.id)}
        title={feature.properties.visible ? $_("Hide") : $_("Show")}
      >
        <span class="flex-initial px-1">
          {#if feature.properties.visible}
            <EyeIcon class="h-5 w-5" />
          {:else}
            <EyeSlashIcon class="h-5 w-5" />
          {/if}
        </span>
        <span class="px-1">
          {$areaTypeMap[feature.properties.type]}
          ({formatArea(feature.properties.area)}
          {$_("ha")})
          {dateCurrentFormat(feature.properties)}
        </span>
      </button>
    </li>
  {/each}
</ul>
