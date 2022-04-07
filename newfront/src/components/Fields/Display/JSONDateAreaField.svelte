<script lang="ts">
  import {
    date_and_current,
    JSONDateAreaFieldType,
  } from "$components/Fields/Display/jsonHelpers.ts";

  export let value: JSONDateAreaFieldType[] = [];
</script>

<div class="jsondatearea_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{date_and_current(val)} </span>
      {#if val.area}
        {val.area.toLocaleString("fr")} ha
      {/if}
    </div>
  {/each}
</div>
