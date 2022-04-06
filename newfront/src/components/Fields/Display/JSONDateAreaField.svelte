<script lang="ts">
  import { date_and_current } from "$components/Fields/Display/jsonHelpers.ts";

  export let value: boolean;

  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="jsondatearea_field whitespace-nowrap">
  {#each vals as val}
    <div class={() => (val.current ? "font-bold" : "")}>
      <span>{date_and_current(val)} </span>
      {#if val.area}
        {val.area.toLocaleString("fr")} ha
      {/if}
    </div>
  {/each}
</div>
