<script lang="ts">
  import type { WagtailStreamfield } from "$lib/types/wagtail";
  import { blockMap } from "$components/Wagtail/blocks";

  export let content: WagtailStreamfield = [];
</script>

<div class={$$props.class + " container mx-auto pt-6 pb-0 streamfield"}>
  {#each content as { type, value }}
    {#if blockMap[type]}
      <svelte:component this={blockMap[type]} bind:value />
    {:else}
      <div class="bg-red-100">
        Unknown block: <strong>"{type}"</strong>
        <pre class="text-xs">
          {JSON.stringify(value, null, 2)}
        </pre>
      </div>
    {/if}
  {/each}
</div>
