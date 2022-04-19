<script lang="ts">
  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers";
  import type { JSONDateAreaFieldType } from "$components/Fields/Display/jsonHelpers";

  export let value: JSONDateAreaFieldType[] = [];
</script>

<div class="jsondatearea_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)} </span>
      {#if val.area}
        {val.area.toLocaleString("fr")} ha
      {/if}
    </div>
  {/each}
</div>
