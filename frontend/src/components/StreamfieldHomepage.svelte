<script lang="ts">
  import type { WagtailStreamfield } from "$lib/types/wagtail"

  import { blockMap } from "$components/Wagtail/blocks"

  export let content: WagtailStreamfield = []
</script>

<div class={$$props.class ?? ""} data-class="streamfield">
  {#each content as { type, value }}
    {#if blockMap[type]}
      <svelte:component this={blockMap[type]} {value} />
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
