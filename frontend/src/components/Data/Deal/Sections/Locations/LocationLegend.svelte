<script lang="ts">
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import { areaChoices, createLabels } from "$lib/fieldChoices"
  import type { AreaType } from "$lib/types/data"

  import { AREA_TYPE_COLOR_MAP, AREA_TYPES } from "./locations"

  interface Props {
    rightCorner?: boolean
  }
  let { rightCorner }: Props = $props()

  let areaTypeLabels = $derived(createLabels<AreaType>($areaChoices.type))
</script>

<div
  class={twMerge(
    "absolute border border-black bg-white p-3 font-sans text-gray-700",
    rightCorner ? "bottom-6 right-1" : "bottom-1 left-1",
  )}
>
  <div class="mb-1 text-center text-sm">
    <strong>{$_("Legend")}</strong>
  </div>
  {#each AREA_TYPES as areaType}
    <div class="flex items-center">
      <div class="h-[14px] w-[14px] border border-dashed border-black">
        <div
          class="h-full w-full opacity-60"
          style="background-color: {AREA_TYPE_COLOR_MAP[areaType]};"
        ></div>
      </div>
      <span class="pl-2 text-xs">
        {areaTypeLabels[areaType]}
      </span>
    </div>
  {/each}
</div>
