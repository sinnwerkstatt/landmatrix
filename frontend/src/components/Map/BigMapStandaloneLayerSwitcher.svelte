<script lang="ts">
  import LayerGroup from "$components/icons/LayerGroup.svelte"
  import { baseLayers, selectedLayers } from "$components/Map/mapstuff.svelte"

  let shown: boolean = $state(false)
</script>

<div
  role="presentation"
  class="absolute right-[10px] top-[10px] z-10 rounded border-2 border-black/30 bg-white px-2 pb-2 pt-1"
  onmouseleave={() => (shown = false)}
>
  {#if !shown}
    <LayerGroup
      class="inline h-5 w-5 text-orange"
      onfocus={() => (shown = true)}
      onmouseover={() => (shown = true)}
    />
  {:else}
    <ul>
      {#each baseLayers as layer}
        <li class="p-1">
          {#if layer.id === selectedLayers.baseLayer}
            <div>{layer.name}</div>
          {:else}
            <button
              onclick={() => (selectedLayers.baseLayer = layer.id)}
              class="text-orange"
              type="button"
            >
              {layer.name}
            </button>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>
