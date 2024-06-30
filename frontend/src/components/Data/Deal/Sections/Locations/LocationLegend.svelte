<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createLabels, fieldChoices } from "$lib/stores"
  import type { AreaType } from "$lib/types/data"

  import { AREA_TYPE_COLOR_MAP, AREA_TYPES } from "./locations"

  $: areaTypeLabels = createLabels<AreaType>($fieldChoices.area.type)
</script>

<div class="border border-black bg-white p-3 font-sans text-gray-700">
  <div class="mb-1 text-center text-sm">
    <strong>{$_("Legend")}</strong>
  </div>
  {#each AREA_TYPES as areaType}
    <div class="flex items-center">
      <div class="h-[14px] w-[14px] border border-dashed border-black">
        <div
          class="colored h-full w-full opacity-60"
          style:--color={AREA_TYPE_COLOR_MAP[areaType]}
        />
      </div>
      <span class="pl-2 text-xs">
        {areaTypeLabels[areaType]}
      </span>
    </div>
  {/each}
</div>

<style lang="css">
  .colored {
    background-color: var(--color, transparent);
  }
</style>
