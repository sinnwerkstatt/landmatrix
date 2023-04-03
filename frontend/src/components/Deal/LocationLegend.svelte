<script lang="ts">
  import { _ } from "svelte-i18n"

  import { AREA_TYPES, AREA_TYPE_COLOR_MAP } from "$lib/utils/location"
  import { areaTypeMap } from "$lib/stores"
</script>

<div class="border border-black bg-lm-light p-3 font-sans text-lm-dark">
  <div class="mb-1 text-center text-base">
    <strong>{$_("Legend")}</strong>
  </div>
  {#each AREA_TYPES as areaType}
    <div class="flex items-center">
      <div
        class="colored h-[14px] w-[14px] border border-dashed border-black opacity-70"
        style:--color={AREA_TYPE_COLOR_MAP[areaType]}
      />
      <div class="pl-2 text-sm">
        {$areaTypeMap[areaType]}
      </div>
    </div>
  {/each}
</div>

<style lang="css">
  .colored {
    background-color: var(--color, transparent);
  }
</style>
