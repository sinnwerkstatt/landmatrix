<script lang="ts">
  import { _ } from "svelte-i18n"

  import LayerGroup from "$components/icons/LayerGroup.svelte"

  import { getBaseLayers, visibleLayer } from "./layers"

  let shown
</script>

<div
  class="absolute right-[10px] top-[10px] z-10 rounded border-2 border-black/30 bg-white px-2 pb-2 pt-1"
  on:mouseleave={() => (shown = false)}
>
  {#if !shown}
    <LayerGroup
      class="inline h-5 w-5 text-orange"
      on:focus={() => (shown = true)}
      on:mouseover={() => (shown = true)}
    />
  {:else}
    <ul>
      {#each getBaseLayers($_) as layer}
        <li class="p-1">
          {#if layer.id === $visibleLayer}
            <div>{layer.name}</div>
          {:else}
            <button
              on:click|preventDefault={() => visibleLayer.set(layer.id)}
              class="text-orange"
            >
              {layer.name}
            </button>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>
