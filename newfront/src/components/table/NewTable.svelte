<script lang="ts">
  import VirtualList from "svelte-tiny-virtual-list";
  import type { Deal } from "$lib/types/deal";
  import type { Investor } from "$lib/types/investor";

  export let columns: string[];
  export let sortBy: string;
  export let objects: Array<Deal | Investor>;
</script>

<div class="grid">
  {#each columns as col}
    <div class="grid">
      {col}
    </div>
  {/each}
  <!--  <VirtualList ></VirtualList>-->
</div>
