<script lang="ts">
  import type { WagtailStreamfield } from "$lib/types/wagtail"

  import { blockMap } from "$components/Wagtail/blocks"

  export let content: WagtailStreamfield = []
</script>

<div class="streamfield container mx-auto px-10 pb-0 pt-6 {$$props.class ?? ''}">
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

<style lang="postcss">
  :global(.streamfield ol) {
    @apply list-decimal pl-4;
  }
  :global(.streamfield ul) {
    @apply mb-4 list-disc pl-4;
  }
  :global(.streamfield h2) {
    @apply text-3xl font-bold;
  }
  :global(.streamfield p) {
    @apply mb-4;
  }
</style>
